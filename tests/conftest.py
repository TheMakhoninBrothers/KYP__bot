import pytest


class TestData:

    def __init__(self, input_data, output_data):
        self.input = input_data
        self.output = output_data


@pytest.fixture()
def messages_for_search_by_tags():
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
