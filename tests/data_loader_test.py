import argparse
import unittest
from unittest.mock import patch, mock_open

from cli.source.utils.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_from_file(self, mock_file):
        args = argparse.Namespace(result_file="file.json", data=None)
        data_loader = DataLoader(args)
        data = _load_from_file("file.json")
        self.assertEqual(data, '{"key": "value"}')

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("cli.source.utils.data_loader.logging.error")
    def test_load_from_file_not_found(self, mock_log_error, mock_file):
        args = argparse.Namespace(result_file="missing_file.json", data=None)
        data_loader = DataLoader(args)
        with self.assertRaises(argparse.ArgumentTypeError):
            _load_from_file("missing_file.json")
        mock_log_error.assert_called_with("The result file does not exist: %s", "missing_file.json")

    def test_load_from_json(self):
        args = argparse.Namespace(result_file=None, data='{"key": "value"}')
        data_loader = DataLoader(args)
        data = _load_from_json('{"key": "value"}')
        self.assertEqual(data, {"key": "value"})

    @patch("cli.source.utils.data_loader.logging.error")
    def test_load_from_json_invalid(self, mock_log_error):
        args = argparse.Namespace(result_file=None, data='invalid_json')
        data_loader = DataLoader(args)
        with self.assertRaises(argparse.ArgumentTypeError):
            _load_from_json('invalid_json')
        mock_log_error.assert_called_with("The data provided is not valid JSON: %s", unittest.mock.ANY)

    @patch.object(DataLoader, "_load_from_file")
    @patch.object(DataLoader, "_load_from_json")
    def test_load_data(self, mock_load_from_json, mock_load_from_file):
        args = argparse.Namespace(result_file="file.json", data=None)
        data_loader = DataLoader(args)
        data_loader.load_data()
        mock_load_from_file.assert_called_once_with("file.json")

        args = argparse.Namespace(result_file=None, data='{"key": "value"}')
        data_loader = DataLoader(args)
        data_loader.load_data()
        mock_load_from_json.assert_called_once_with('{"key": "value"}')


if __name__ == "__main__":
    unittest.main()