import json
import logging
import pytest
import sys
from unittest.mock import patch, MagicMock
from cli.store_run_results import store_run_result, main, Constants
from jsonschema.exceptions import ValidationError


@patch('cli.store_run_results.Database', autospec=True)
def test_for_unregistered_tool_should_log_error_and_should_not_persist_to_db(mock_database_class, caplog):
    with patch('tools.tools_registry.ToolRegistry.get_tool', return_value=None):
        result = store_run_result("nonexistent_tool", {})
        assert not result
        assert Constants.ERROR_TOOL_NOT_REGISTERED % "nonexistent_tool" in caplog.text
        assert not mock_database_class.called


@patch('cli.store_run_results.Database', autospec=True)
def test_when_input_does_not_match_schema_should_log_error_and_should_not_persist_to_db(mock_database_class, caplog):
    with patch('tools.tool_base.Tool.validate_result', side_effect=ValidationError("Schema error")):
        result = store_run_result("prime", {})
    assert not result
    assert Constants.ERROR_INPUT_DOES_NOT_MATCH_SCHEMA % "Schema error" in caplog.text
    assert not mock_database_class.called


@patch('cli.store_run_results.Database', autospec=True)
def test_cli_e2e_happy_path(mock_database_class, caplog):

    mock_db_instance = mock_database_class.return_value
    mock_db_instance.store_run_result.return_value = None

    test_args = ["store_run_results.py", "--tool", "prime", "-f", "test_run_result.json"]

    try:
        with caplog.at_level(logging.INFO):
            with patch.object(sys, 'argv', test_args):
                main()
    except SystemExit:
        pytest.fail("main() raised SystemExit unexpectedly!")

    with open('test_run_result.json') as f:
        data = json.load(f)

    mock_db_instance.store_run_result.assert_called_once_with("prime", data)
    assert Constants.INFO_RUN_RESULT_STORED in caplog.text


if __name__ == "__main__":
    pytest.main()
