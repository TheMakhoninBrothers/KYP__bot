import pytest

from app.modules.helpers import WrongFormat


class TestData:

    def __init__(self, input_data, output_data):
        self.input = input_data
        self.output = output_data


@pytest.fixture()
def positive__messages_for_search_by_tags():
    """Тестовые данные для поиска по тегам"""
    return (
        TestData('#SERVER', ['server']),
        TestData('#SERVER #WORK', ['server', 'work']),
        TestData('#SERVER#WORK', ['server', 'work']),
        TestData('#SERVER##', ['server']),
        TestData('server', ['server']),
        TestData('serverhome', ['serverhome']),
        TestData('server home', ['server', 'home']),
        TestData('#server home #m9', ['server', 'home', 'm9']),
    )


@pytest.fixture()
def negative__messages_for_search_by_tags():
    """Тестовые данные для поиска по тегам"""
    return (
        TestData('/gets', WrongFormat),
        TestData('server /add', WrongFormat)
    )


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
