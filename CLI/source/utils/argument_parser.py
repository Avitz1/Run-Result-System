import argparse


class ArgumentParser:
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
        return self.args

    def validate_arguments(self):
        if not self.args.tool or self.args.tool.isspace():
            self.parser.error("The tool must be specified")
        if not self.args.result_file and not self.args.data:
            self.parser.error("Either the result file or the data must be specified")
        if self.args.result_file and self.args.data:
            self.parser.error("Only one of the result file or the data must be specified")
