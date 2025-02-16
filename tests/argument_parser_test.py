import argparse
import unittest
from unittest.mock import patch

from cli.source.utils.argument_parser import ArgumentParser


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


if __name__ == "__main__":
    unittest.main()
