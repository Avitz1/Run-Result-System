import sys
import logging
from typing import Any, Dict
from jsonschema import ValidationError

from tools.tools_registry import ToolRegistry
from cli.utils.argument_parser import ArgumentParser
from cli.utils.data_loader import DataLoader
from database.database_client import Database, DatabaseConnectionError


class Constants:
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    ERROR_TOOL_NOT_REGISTERED = "Tool %s is not registered"
    INFO_RUN_RESULT_STORED = "Run result stored successfully"
    ERROR_DATABASE = "Database error: %s"
    ERROR_FAILED_TO_STORE = "Failed to store run result: %s"
    ERROR_DATA_LOADING_FAILED = "Data loading failed"
    ERROR_INPUT_DOES_NOT_MATCH_SCHEMA = "Input does not match schema: %s"


def validate_tool(tool_name: str) -> bool:
    """
    Validate if the tool is registered in the ToolRegistry.

    :param tool_name: The name of the tool
    :return: True if the tool is registered, False otherwise
    """
    tool = ToolRegistry.get_tool(tool_name)
    if tool is None:
        logging.error(Constants.ERROR_TOOL_NOT_REGISTERED, tool_name)
        return False
    return True


def validate_result_data(tool_name: str, result_data: Dict[str, Any]) -> bool:
    """
    Validate the result data against the tool's schema.

    :param tool_name: The name of the tool
    :param result_data: The result data to validate
    :return: True if the result data is valid, False otherwise
    """
    tool = ToolRegistry.get_tool(tool_name)
    try:
        tool.validate_result(result_data)
        return True
    except ValidationError as e:
        logging.error(Constants.ERROR_INPUT_DOES_NOT_MATCH_SCHEMA, e)
        return False


def store_result_in_database(tool_name: str, result_data: Dict[str, Any]) -> bool:
    """
    Store the result data in the database.

    :param tool_name: The name of the tool
    :param result_data: The result data to store
    :return: True if the result was stored successfully, False otherwise
    """
    try:
        db = Database()
        db.store_run_result(tool_name, result_data)
        logging.info(Constants.INFO_RUN_RESULT_STORED)
        return True
    except DatabaseConnectionError as e:
        logging.error(Constants.ERROR_DATABASE, e)
        return False


def store_run_result(tool_name: str, result_data: Dict[str, Any]) -> bool:
    """
    Store run result in the database.

    :param tool_name: The name of the tool
    :param result_data: The result data to store
    :return: True if the result was stored successfully, False otherwise
    """
    if not (validate_tool(tool_name) and validate_result_data(tool_name, result_data)):
        return False

    return store_result_in_database(tool_name, result_data)


def main() -> None:
    """
    Main function to process run results from a specified tool.
    """
    logging.basicConfig(level=logging.INFO, format=Constants.LOGGING_FORMAT)

    arg_parser = ArgumentParser()
    args = arg_parser.parse_arguments()

    data_loader = DataLoader(args)
    data = data_loader.load_data()

    if data is None:
        logging.error(Constants.ERROR_DATA_LOADING_FAILED)
        sys.exit(1)

    if not store_run_result(args.tool, data):
        sys.exit(1)


if __name__ == "__main__":
    main()
