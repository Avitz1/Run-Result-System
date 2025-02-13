"""
This module processes run results from a specified tool.
It can read results from a file or directly from provided JSON data.
"""

import argparse
import configparser
import http
import json
import os
import sys
import time
from datetime import datetime
import pytz
import requests
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from model.publish_result_model import PublishResultRequest


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


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


class PublishRequestCreator:
    @staticmethod
    def create_request(tool, data):
        datetime_str = datetime.now(pytz.utc).isoformat().replace("+00:00", "Z")
        return PublishResultRequest(
            tool=tool,
            data=data,
            time=datetime_str
        )


class RequestSender:
    def __init__(self, config):
        self.api_url = config.get("GENERAL", "run_result_server_url")
        self.retries = config.getint("GENERAL", "retries", fallback=3)
        self.retry_backoff = config.getint("GENERAL", "retry_backoff", fallback=5)

        if not self.api_url:
            logging.error("API URL not configured.")
            sys.exit(1)

    def send_data(self, publish_request):

        attempt = 0
        while attempt < self.retries:
            try:
                response = requests.post(self.api_url, json=publish_request.toJSON())
                if response.status_code == http.HTTPStatus.BAD_REQUEST:
                    logging.error("Error: %s", response.json().get('error', 'Unknown error'))
                    break
                response.raise_for_status()
                logging.info("Data uploaded successfully, it should be exposed in our UI shortly.")
                break
            except requests.exceptions.RequestException as e:
                logging.error("Error sending request: %s", e)
                time.sleep(self.retry_backoff)
                attempt += 1
        else:
            logging.error("Failed to send request after %d attempts.", self.retries)
            SystemExit(1)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = read_config(config_file)

    arg_parser = ArgumentParser()
    args = arg_parser.parse_arguments()
    arg_parser.validate_arguments()

    data_loader = DataLoader(args)
    try:
        data = data_loader.load_data()
    except argparse.ArgumentTypeError as e:
        logging.critical("Error loading data: %s", e)
        SystemExit(1)

    publish_request = PublishRequestCreator.create_request(args.tool, data)

    sender = RequestSender(config)
    sender.send_data(publish_request)


if __name__ == "__main__":
    main()
