import unittest
from unittest.mock import patch, mock_open, MagicMock
import argparse
import json
import configparser
from datetime import datetime
import pytz
import requests

# Import the classes and functions from your module
from process_run_results import (
    read_config, ArgumentParser, DataLoader, PublishRequestCreator, RequestSender, main
)
from model.publish_result_model import PublishResultRequest


class TestReadConfig(unittest.TestCase):
    @patch("configparser.ConfigParser.read")
    def test_read_config(self, mock_read):
        config_file = "test_config.ini"
        config = read_config(config_file)
        mock_read.assert_called_once_with(config_file)


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

    @patch("argparse.ArgumentParser.error")
    def test_validate_arguments(self, mock_error):
        # Test missing tool argument
        self.arg_parser.args = argparse.Namespace(tool=None, result_file=None, data=None)
        with self.assertRaises(SystemExit):
            self.arg_parser.validate_arguments()
        mock_error.assert_called_once_with("The tool must be specified")

        # Test missing result_file and data arguments
        self.arg_parser.args = argparse.Namespace(tool="test_tool", result_file=None, data=None)
        with self.assertRaises(SystemExit):
            self.arg_parser.validate_arguments()
        mock_error.assert_called_with("Either the result file or the data must be specified")

        # Test both result_file and data arguments provided
        self.arg_parser.args = argparse.Namespace(
            tool="test_tool", result_file="file.json", data='{"key": "value"}'
        )
        with self.assertRaises(SystemExit):
            self.arg_parser.validate_arguments()
        mock_error.assert_called_with("Only one of the result file or the data must be specified")


class TestDataLoader(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_from_file(self, mock_file):
        args = argparse.Namespace(result_file="file.json", data=None)
        data_loader = DataLoader(args)
        data = data_loader._load_from_file("file.json")
        self.assertEqual(data, '{"key": "value"}')

    @patch("process_run_results.logging.error")
    def test_load_from_file_not_found(self, mock_log_error):
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

    @patch("process_run_results.logging.error")
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


class TestPublishRequestCreator(unittest.TestCase):
    @patch("process_run_results.datetime")
    def test_create_request(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 2, 13, 5, 39, 5, tzinfo=pytz.utc)
        tool = "test_tool"
        data = {"key": "value"}

        request = PublishRequestCreator.create_request(tool, data)
        self.assertIsInstance(request, PublishResultRequest)
        self.assertEqual(request.tool, tool)
        self.assertEqual(request.data, data)
        self.assertEqual(request.time, "2025-02-13T05:39:05Z")


class TestRequestSender(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.add_section("GENERAL")
        self.config.set("GENERAL", "run_result_server_url", "http://example.com")
        self.config.set("GENERAL", "retries", "2")
        self.config.set("GENERAL", "retry_backoff", "1")
        self.sender = RequestSender(self.config)

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
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mock_post.return_value = mock_response

        publish_request = PublishResultRequest(tool="test_tool", data={"key": "value"}, time="2025-02-13T05:39:05Z")
        self.sender.send_data(publish_request)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)


if __name__ == "__main__":
    unittest.main()