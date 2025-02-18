import pytest
from cli.utils.argument_parser import ArgumentParser


def test_validate_arguments_no_file_or_data(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool"]
    monkeypatch.setattr('sys.argv', test_args)
    parser = ArgumentParser()
    with pytest.raises(SystemExit):
        parser.parse_arguments()
    captured = capsys.readouterr()
    assert ArgumentParser.Constants.ERROR_RESULT_FILE_OR_DATA in captured.err


def test_validate_arguments_both_file_and_data(monkeypatch, capsys):
    test_args = ["prog", "--tool", "some_tool", "-f", "result.json", "--data", '{"key": "value"}']
    monkeypatch.setattr('sys.argv', test_args)
    parser = ArgumentParser()
    with pytest.raises(SystemExit):
        parser.parse_arguments()
    captured = capsys.readouterr()
    assert ArgumentParser.Constants.ERROR_EXCLUSIVE_RESULT_FILE_OR_DATA in captured.err


def test_validate_arguments_only_result_file(monkeypatch):
    test_args = ["prog", "--tool", "some_tool", "-f", "result.json"]
    monkeypatch.setattr('sys.argv', test_args)
    parser = ArgumentParser()
    parser.args = parser.parse_arguments()
    try:
        parser.validate_arguments()
    except SystemExit:
        pytest.fail("validate_arguments() raised SystemExit unexpectedly!")


def test_validate_arguments_only_data(monkeypatch):
    test_args = ["prog", "--tool", "some_tool", "--data", '{"key": "value"}']
    monkeypatch.setattr('sys.argv', test_args)
    parser = ArgumentParser()
    parser.args = parser.parse_arguments()
    try:
        parser.validate_arguments()
    except SystemExit:
        pytest.fail("validate_arguments() raised SystemExit unexpectedly!")


if __name__ == "__main__":
    pytest.main()
