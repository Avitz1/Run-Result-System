import json
import logging


class DataLoader:
    def __init__(self, args):
        self.args = args

    def load_data(self):
        if self.args.result_file:
            return _load_json(self.args.result_file, from_file=True)
        if self.args.data:
            return _load_json(self.args.data, from_file=False)
        return None


def _load_json(source, from_file):
    try:
        if from_file:
            with open(source) as file:
                return json.load(file)
        else:
            return json.loads(source)
    except FileNotFoundError:
        logging.error("The result file does not exist: %s", source)
        return None
    except json.JSONDecodeError as e:
        logging.error("The data provided is not valid JSON: %s", e)
        return None