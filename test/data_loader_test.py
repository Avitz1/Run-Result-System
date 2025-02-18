import pytest
import argparse
import json
from cli.utils.data_loader import DataLoader, _load_json, ERROR_FILE_NOT_FOUND, ERROR_INVALID_JSON


def test_load_json_from_existing_valid_file_should_return_data_and_log_nothing(monkeypatch, tmp_path, caplog):
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    result = _load_json(str(file_path), from_file=True)

    file_path.unlink()
    assert result == data
    assert caplog.text == ""


def test_load_data_from_valid_json_string_should_return_data_and_log_nothing():
    data = '{"key": "value"}'
    args = argparse.Namespace(result_file=None, data=data)
    data_loader = DataLoader(args)
    result = data_loader.load_data()
    assert result == json.loads(data)


def test_load_json_from_non_existing_file_should_log_error_and_return_null(monkeypatch, tmp_path, caplog):
    result = _load_json("nonexistent.json", from_file=True)
    assert result is None
    assert ERROR_FILE_NOT_FOUND % "nonexistent.json" in caplog.text


def test_load_invalid_json_from_file_should_log_error_and_return_null(monkeypatch, tmp_path, caplog):
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        f.write("{key: value}")

    result = _load_json(str(file_path), from_file=True)

    file_path.unlink()

    assert result is None
    assert ERROR_INVALID_JSON.replace("%s", "") in caplog.text


def test_load_json_from_invalid_json_string_should_log_error_and_return_null(caplog):
    data = "{key: value}"
    result = _load_json(data, from_file=False)
    assert result is None
    assert ERROR_INVALID_JSON.replace("%s", "") in caplog.text


if __name__ == "__main__":
    pytest.main()