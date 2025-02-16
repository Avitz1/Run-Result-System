"""
This module processes run results from a specified tool.
It can read results from a file or directly from provided JSON data.
"""

import argparse
import sys
import logging

from tools.tools_registry import ToolRegistry
from utils.argument_parser import ArgumentParser
from utils.data_loader import DataLoader
from database.database_client import Database


def store_run_result(tool_name, result_data):
    tool = ToolRegistry.get_tool(tool_name)
    tool.validate_result(result_data)
    db = Database()
    db.store_run_result(tool_name, result_data)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    arg_parser = ArgumentParser()
    try:
        args = arg_parser.parse_arguments()
        arg_parser.validate_arguments()
    except argparse.ArgumentTypeError as e:
        logging.error("Error parsing arguments: %s", e)
        sys.exit(1)

    data_loader = DataLoader(args)
    data = data_loader.load_data()

    if data is None:
        logging.error("Error loading data")
        sys.exit(1)

    store_run_result(args.tool, data)


if __name__ == "__main__":
    main()
