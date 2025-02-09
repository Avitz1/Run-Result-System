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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from model.publish_result_model import PublishResultRequest


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
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

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
        elif self.args.data:
            try:
                return json.loads(self.args.data)
            except json.JSONDecodeError:
                self.parser.error("The data provided is not valid JSON")
        return self.args.data

    def create_request(self) -> PublishResultRequest:
        """
        Sends the data to the server
        """
        datetime_str = datetime.now(pytz.utc).isoformat()
        datetime_str = datetime_str.replace("+00:00", "Z")
        return PublishResultRequest(
            tool=self.args.tool,
            data=self.load_data(),
            time=datetime_str
        )

    def send_data(self, publish_request: PublishResultRequest):
        """
        Sends the data to the server
        """
        api_url = self.config.get("GENERAL", "run_result_server_url")
        retries = self.config.getint("GENERAL", "retries", fallback=3)
        retry_backoff = self.config.getint("GENERAL", "retry_backoff", fallback=5)

        if not api_url:
            raise ValueError("API URL not configured.")

        print(f"Attempting to send POST request to: {api_url}")

        attempt = 0
        while attempt < retries:
            try:
                response = requests.post(api_url, json=publish_request.toJSON())
                if response.status_code == http.HTTPStatus.BAD_REQUEST:
                    print(f"Error: {response.json()['error']}")
                    break
                response.raise_for_status()
                print(f"Data uploaded successfully, it should be exposed in our UI shortly.")
                break
            except requests.exceptions.RequestException as e:
                print(f"Error sending request: {e}")
                time.sleep(retry_backoff)
                attempt += 1
        else:
            print(f"Failed to send request after {retries} attempts.")


def main():
    processor = RunResultProcessor()
    processor.parse_arguments()
    processor.validate_arguments()
    publish_request = processor.create_request()
    processor.send_data(publish_request)


if __name__ == "__main__":
    main()
