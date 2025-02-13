import configparser
import http
import unittest
from unittest.mock import patch, MagicMock

import requests

from cli.source.utils.run_result_client import RunResultClient
from cli.source.model.publish_result_model import PublishResultRequest


class TestRUnResultClient(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.add_section("GENERAL")
        self.config.set("GENERAL", "run_result_server_url", "http://example.com")
        self.config.set("GENERAL", "retries", "2")
        self.config.set("GENERAL", "retry_backoff", "1")
        self.sender = RunResultClient(self.config)

    @patch("sys.exit")
    @patch("cli.source.utils.run_result_client.logging.error")
    def test_init_no_api_url(self, mock_log_error, mock_exit):
        config = configparser.ConfigParser()
        config.add_section("GENERAL")
        config.set("GENERAL", "run_result_server_url", "")
        RunResultClient(config)
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

        mock_post.assert_called_once_with("http://example.com", json=publish_request.to_json())
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
