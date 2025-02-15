"""
This module processes run results from a specified tool.
It can read results from a file or directly from provided JSON data.
"""

import argparse
import configparser
import os
import sys
from datetime import datetime
import pytz
import logging

from utils.argument_parser import ArgumentParser
from utils.data_loader import DataLoader
from utils.run_result_client import RunResultClient
from model.publish_result_model import PublishResultRequest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    arg_parser = ArgumentParser()
    try:
        args = arg_parser.parse_arguments()
        arg_parser.validate_arguments()
    except argparse.ArgumentTypeError as e:
        logging.error("Error parsing arguments: %s", e)
        sys.exit(1)

    data_loader = DataLoader(args)
    try:
        data = data_loader.load_data()
    except argparse.ArgumentTypeError as e:
        logging.error("Error loading data: %s", e)
        sys.exit(1)
    project = data.get('project')
    user = data.get('user')
    if not project or not user:
        logging.error("Project and user must be provided")
        sys.exit(1)
    publish_request = PublishResultRequest(tool=args.tool, data=data, project=project, user=user, time=datetime.now(pytz.utc).isoformat())

    client = RunResultClient(config)
    try:
        client.send_data(publish_request)
    except Exception as e:
        logging.error("Error sending data: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
