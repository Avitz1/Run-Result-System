import configparser
import http
import unittest
from unittest.mock import patch, mock_open, MagicMock
import argparse

import requests

from cli.source.store_run_results import ArgumentParser, DataLoader, RequestSender
from model.publish_result_model import PublishResultRequest


class TestArgumentParser(unittest.TestCase):
    def setUp(self):
        self.arg_parser = ArgumentParser()

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_arguments(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            tool="test_tool", result_file=None, data='{"key": "value"}'
        )
        args = self.arg_parser.parse_arguments()
        self.assertEqual(args.tool, "test_tool")
        self.assertEqual(args.data, '{"key": "value"}')

    @patch("sys.exit")
    def test_validate_arguments_missing_tool(self, mock_exit):
        self.arg_parser.args = argparse.Namespace(tool=None, result_file=None, data="{}")
        self.arg_parser.validate_arguments()
        mock_exit.assert_called_once_with(2)

    @patch("sys.exit")
    def test_validate_arguments_missing_result_file_and_data(self, mock_exit):
        self.arg_parser.args = argparse.Namespace(tool="test_tool", result_file=None, data=None)
        self.arg_parser.validate_arguments()
        mock_exit.assert_called_once_with(2)

    @patch("sys.exit")
    def test_validate_arguments_both_result_file_and_data_provided(self, mock_exit):
        self.arg_parser.args = argparse.Namespace(
            tool="test_tool", result_file="file.json", data='{"key": "value"}'
        )
        self.arg_parser.validate_arguments()
        mock_exit.assert_called_once_with(2)


class TestDataLoader(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_from_file(self, mock_file):
        args = argparse.Namespace(result_file="file.json", data=None)
        data_loader = DataLoader(args)
        data = data_loader._load_from_file("file.json")
        self.assertEqual(data, '{"key": "value"}')

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("cli.source.store_run_results.logging.error")
    def test_load_from_file_not_found(self, mock_log_error, mock_file):
        args = argparse.Namespace(result_file="missing_file.json", data=None)
        data_loader = DataLoader(args)
        with self.assertRaises(argparse.ArgumentTypeError):
            data_loader._load_from_file("missing_file.json")
        mock_log_error.assert_called_with("The result file does not exist: %s", "missing_file.json")

    def test_load_from_json(self):
        args = argparse.Namespace(result_file=None, data='{"key": "value"}')
        data_loader = DataLoader(args)
        data = data_loader._load_from_json('{"key": "value"}')
        self.assertEqual(data, {"key": "value"})

    @patch("cli.source.store_run_results.logging.error")
    def test_load_from_json_invalid(self, mock_log_error):
        args = argparse.Namespace(result_file=None, data='invalid_json')
        data_loader = DataLoader(args)
        with self.assertRaises(argparse.ArgumentTypeError):
            data_loader._load_from_json('invalid_json')
        mock_log_error.assert_called_with("The data provided is not valid JSON: %s", unittest.mock.ANY)

    @patch.object(DataLoader, "_load_from_file")
    @patch.object(DataLoader, "_load_from_json")
    def test_load_data(self, mock_load_from_json, mock_load_from_file):
        # Test loading from file
        args = argparse.Namespace(result_file="file.json", data=None)
        data_loader = DataLoader(args)
        data_loader.load_data()
        mock_load_from_file.assert_called_once_with("file.json")

        # Test loading from JSON data
        args = argparse.Namespace(result_file=None, data='{"key": "value"}')
        data_loader = DataLoader(args)
        data_loader.load_data()
        mock_load_from_json.assert_called_once_with('{"key": "value"}')


class TestRequestSender(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.add_section("GENERAL")
        self.config.set("GENERAL", "run_result_server_url", "http://example.com")
        self.config.set("GENERAL", "retries", "2")
        self.config.set("GENERAL", "retry_backoff", "1")
        self.sender = RequestSender(self.config)

    @patch("sys.exit")
    @patch("cli.source.store_run_results.logging.error")
    def test_init_no_api_url(self, mock_log_error, mock_exit):
        config = configparser.ConfigParser()
        config.add_section("GENERAL")
        config.set("GENERAL", "run_result_server_url", "")
        RequestSender(config)
        mock_log_error.assert_called_once_with("API URL not configured.")
        mock_exit.assert_called_once_with(1)

    @patch("requests.post")
    @patch("time.sleep", return_value=None)
    def test_send_data_success(self, mock_sleep, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = http.HTTPStatus.OK
        mock_post.return_value = mock_response

        publish_request = PublishResultRequest(tool="test_tool", data={"key": "value"}, time="2025-02-13T05:39:05Z")
        self.sender.send_data(publish_request)

        mock_post.assert_called_once_with("http://example.com", json=publish_request.toJSON())
        mock_sleep.assert_not_called()

    @patch("requests.post")
    @patch("time.sleep", return_value=None)
    def test_send_data_failure(self, mock_sleep, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = http.HTTPStatus.BAD_REQUEST
        mock_response.json.return_value = {"error": "Bad Request"}
        mock_post.return_value = mock_response

        publish_request = PublishResultRequest(tool="test_tool", data={"key": "value"}, time="2025-02-13T05:39:05Z")
        self.sender.send_data(publish_request)

        self.assertEqual(mock_post.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("requests.post")
    @patch("time.sleep", return_value=None)
    def test_send_data_retry(self, mock_sleep, mock_post):
        mock_post.side_effect = [
            requests.exceptions.RequestException,
            MagicMock(status_code=http.HTTPStatus.OK)
        ]

        publish_request = PublishResultRequest(tool="test_tool", data={"key": "value"}, time="2025-02-13T05:39:05Z")
        self.sender.send_data(publish_request)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)


if __name__ == "__main__":
    unittest.main()
