"""
This module processes run results from a specified tool.
It can read results from a file or directly from provided JSON data.
"""

import argparse
import configparser
import json
import os
import sys
import logging

from utils.argument_parser import ArgumentParser
from utils.data_loader import DataLoader
from database.database_client import Database


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    config_file = os.path.join(os.path.dirname(__file__), "config.ini")
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
    except FileNotFoundError or json.JSONDecodeError as e:
        logging.error("Error loading data: %s", e)
        sys.exit(1)

    Database().store_run_result(args.tool, data)


if __name__ == "__main__":
    main()
