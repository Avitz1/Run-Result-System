"""
This module processes run results from a specified tool.
It can read results from a file or directly from provided JSON data.
"""

import argparse
import json


class RunResult:
    """
    Represents the results of a tool run.
    """

    def __init__(self, tool: str, run_results: str):
        self.tool = tool
        self.data = run_results


class RunResultProcessor:
    """
    Processes the command line arguments and generates the RunResult object
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Process run results.")
        self.parser.add_argument("--tool", type=str, help="the tool that was run")
        self.parser.add_argument(
            "-f", "--result_file", type=str, help="the file containing the results"
        )
        self.parser.add_argument("--data", type=str, help="the data in JSON format")
        self.args = None

    def parse_arguments(self):
        self.args = self.parser.parse_args()

    def validate_arguments(self):
        """
        Validates the arguments passed to the script
        """
        if (
            self.args.tool is None
            or len(self.args.tool) == 0
            or self.args.tool.isspace()
        ):
            self.parser.error("The tool must be specified")
        if self.args.result_file is None and self.args.data is None:
            self.parser.error("Either the result file or the data must be specified")
        elif self.args.result_file is not None and self.args.data is not None:
            self.parser.error(
                "Only one of the result file or the data must be specified"
            )

        if self.args.data:
            try:
                json.loads(self.args.data)
            except json.JSONDecodeError:
                self.parser.error("The data provided is not valid JSON")

    def load_data(self):
        """
        Loads the data from the specified source
        """
        if self.args.result_file:
            try:
                with open(self.args.result_file, "r", encoding="utf-8") as file:
                    return file.read()
            except FileNotFoundError:
                self.parser.error("The result file does not exist")
        return self.args.data

    def process_results(self) -> RunResult:
        data = self.load_data()
        return RunResult(self.args.tool, data)


def process_command() -> RunResult:
    processor = RunResultProcessor()
    processor.parse_arguments()
    processor.validate_arguments()
    return processor.process_results()


def send_data(run_result: RunResult):
    pass


def main():
    run_result = process_command()
    send_data(run_result)


if __name__ == "__main__":
    main()
