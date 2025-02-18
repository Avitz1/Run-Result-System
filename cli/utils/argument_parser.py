"""
This module configures and wraps python's argparse.ArgumentParser class which is used to parse and validate the command
line arguments.
"""

import argparse
from typing import Optional


class ArgumentParser:
    class Constants:
        DESCRIPTION = "Process run results."
        TOOL_HELP = "The tool that was run"
        RESULT_FILE_HELP = "The file containing the results"
        DATA_HELP = "The data in JSON format"
        ERROR_RESULT_FILE_OR_DATA = "Either the result file or the data must be specified"
        ERROR_EXCLUSIVE_RESULT_FILE_OR_DATA = "Only one of the result file or the data must be specified"

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=self.Constants.DESCRIPTION)
        self.parser.add_argument("--tool", required=True, help=self.Constants.TOOL_HELP)
        self.parser.add_argument("-f", "--result_file", help=self.Constants.RESULT_FILE_HELP)
        self.parser.add_argument("--data", help=self.Constants.DATA_HELP)
        self.args: Optional[argparse.Namespace] = None

    def parse_arguments(self) -> argparse.Namespace:
        self.args = self.parser.parse_args()
        self.validate_arguments()
        return self.args

    def validate_arguments(self) -> None:
        if not self.args.result_file and not self.args.data:
            self.parser.error(self.Constants.ERROR_RESULT_FILE_OR_DATA)
        if self.args.result_file and self.args.data:
            self.parser.error(self.Constants.ERROR_EXCLUSIVE_RESULT_FILE_OR_DATA)