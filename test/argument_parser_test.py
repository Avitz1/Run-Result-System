import pytest
from cli.utils.argument_parser import ArgumentParser


def test_validate_arguments_no_file_no_data_should_log_error_and_exit(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool"]
    parse_args_assert_exit_code_and_error_message(
        test_args, monkeypatch, capsys, ArgumentParser.Constants.ERROR_RESULT_FILE_OR_DATA, 2)


def test_validate_arguments_both_file_and_data_should_log_error_and_exit(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool", "-f", "result.json", "--data", '{"key": "value"}']
    parse_args_assert_exit_code_and_error_message(
        test_args, monkeypatch, capsys, ArgumentParser.Constants.ERROR_EXCLUSIVE_RESULT_FILE_OR_DATA, 2)


def test_validate_arguments_valid_args_with_file_should_not_exit_or_log(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool", "-f", "result.json"]
    parse_args_assert_no_error(capsys, monkeypatch, test_args)


def test_validate_arguments_valid_args_with_data_should_not_exit_or_log(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool", "--data", '{"key": "value"}']
    parse_args_assert_no_error(capsys, monkeypatch, test_args)


def parse_args_assert_exit_code_and_error_message(args, monkeypatch, capsys, error_message, exit_code):
    monkeypatch.setattr('sys.argv', args)
    parser = ArgumentParser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_arguments()
    captured = capsys.readouterr()
    assert error_message in captured.err
    assert excinfo.type == SystemExit
    assert excinfo.value.code == exit_code


def parse_args_assert_no_error(capsys, monkeypatch, test_args):
    monkeypatch.setattr('sys.argv', test_args)
    parser = ArgumentParser()
    parser.args = parser.parse_arguments()
    try:
        parser.validate_arguments()
    except SystemExit:
        pytest.fail("validate_arguments() raised SystemExit unexpectedly!")
    captured = capsys.readouterr()
    assert captured.err == ""


if __name__ == "__main__":
    pytest.main()
