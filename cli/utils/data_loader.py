"""This module is responsible for loading the data from the source, either a file or a string, and returning it as a
dictionary."""
import argparse
import json
import logging
from typing import Optional, Dict

ERROR_FILE_NOT_FOUND = "The result file does not exist: %s"
ERROR_INVALID_JSON = "The data provided is not valid JSON: %s"


class DataLoader:
    def __init__(self, args: argparse.Namespace):
        self.args = args

    def load_data(self) -> Optional[Dict[str, any]]:
        if self.args.result_file:
            return _load_json(self.args.result_file, from_file=True)
        if self.args.data:
            return _load_json(self.args.data, from_file=False)
        return None


def _load_json(source: str, from_file: bool) -> Optional[Dict[str, any]]:
    try:
        if from_file:
            with open(source) as file:
                return json.load(file)
        else:
            return json.loads(source)
    except FileNotFoundError:
        logging.error(ERROR_FILE_NOT_FOUND, source)
        return None
    except json.JSONDecodeError as e:
        logging.error(ERROR_INVALID_JSON, e)
        return None
