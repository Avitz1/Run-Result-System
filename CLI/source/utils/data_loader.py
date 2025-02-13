import argparse
import json
import logging


class DataLoader:
    def __init__(self, args):
        self.args = args

    def load_data(self):
        if self.args.result_file:
            return self._load_from_file(self.args.result_file)
        if self.args.data:
            return self._load_from_json(self.args.data)
        return None

    def _load_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logging.error("The result file does not exist: %s", file_path)
            raise argparse.ArgumentTypeError("The result file does not exist")

    def _load_from_json(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            logging.error("The data provided is not valid JSON: %s", e)
            raise argparse.ArgumentTypeError("The data provided is not valid JSON")
