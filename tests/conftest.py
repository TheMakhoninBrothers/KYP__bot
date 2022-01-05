from collections import namedtuple

import pytest

from app.modules.helpers import WrongFormat

Message = namedtuple('Message', ['text', 'html_text'], defaults=[None])


class TestData:
    """Тестовые данные"""

    def __init__(self, input_data, output_data):
        self.input = input_data
        self.output = output_data


@pytest.fixture()
def positive__messages_for_find_record_by_id():
    """Тестовые данные для поиска по id"""
    return (
        TestData('/get', None),
        TestData('/get 1', 1),
    )


@pytest.fixture()
def negative__messages_for_find_record_by_id():
    """Тестовые данные для поиска по id"""
    return (
        TestData('/get @', WrongFormat),
        TestData('/get 1 2 3', WrongFormat),
    )
