"""Тесты функций сохранения и загрузки данных."""

import os
import tempfile

from storage import load_data, save_data


def test_save_and_load_data() -> None:
    """Данные сохраняются и загружаются без потерь."""
    data = [{"id": 1, "name": "test"}]
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        save_data(filename, data)
        loaded = load_data(filename, [])
        assert loaded == data


def test_load_data_missing_file() -> None:
    """При отсутствии файла возвращается значение по умолчанию."""
    default = [{"id": 0}]
    loaded = load_data("nonexistent_file.json", default)
    assert loaded == default
