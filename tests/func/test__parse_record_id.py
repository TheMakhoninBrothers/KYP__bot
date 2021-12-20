import pytest

from app.modules.helpers import parse_record_id


def test_positive__input_data(positive__messages_for_find_record_by_id):
    """Позитивный тест"""
    for test_data in positive__messages_for_find_record_by_id:
        assert parse_record_id('/get', test_data.input) == test_data.output


def test_negative__input_data(negative__messages_for_find_record_by_id):
    """Негативный тест"""
    for test_data in negative__messages_for_find_record_by_id:
        with pytest.raises(test_data.output):
            assert parse_record_id('/get', test_data.input)
