import argparse
import json
import logging


class DataLoader:
    def __init__(self, args):
        self.args = args

    def load_data(self):
        if self.args.result_file:
            return _load_from_file(self.args.result_file)
        if self.args.data:
            return _load_from_json(self.args.data)
        return None


def _load_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error("The result file does not exist: %s", file_path)
        raise FileNotFoundError(f"The result file does not exist: {file_path}")


def _load_from_json(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logging.error("The data provided is not valid JSON: %s", e)
        raise json.JSONDecodeError(f"The data provided is not valid JSON: {e}", e.doc, e.pos)
