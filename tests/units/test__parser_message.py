import typing

import pytest

from app.modules import message_parsers
from tests.conftest import Message

testdata = \
    [
        (
            '/add #server #work working server with #test apps username@megahost <>1#234#5678<> #credential',
            ['server', 'work', 'test', 'credential']
        ),
        (
            '/add #server #work working server with apps',
            ['server', 'work']
        )
    ]


@pytest.mark.parametrize('message,expected', testdata)
def test_positive__parse_tags(message: str, expected: typing.List[str]):
    """
    Позитивный тест.
    Парсер тегов.
    """
    assert message_parsers.parse_tags(message) == expected


testdata = \
    [
        (
            'server #test', ['server', 'test']
        ),
        (
            '#server#test', ['server', 'test']
        ),
        (
            'server test', ['server', 'test']
        )
    ]


@pytest.mark.parametrize('message,expected', testdata)
def test_positive__search_by_tags(message: str, expected: typing.List[str]):
    """
    Позитивный тест
    Парсер сообщения для поиска по тегам
    :param positive_parse_message__search_by_tags:
    :return:
    """
    message = Message(text=message, html_text=message)
    assert message_parsers.parse_message__search_by_tags(message) == expected


testdata = \
    [
        ('/add server', 'server'),
        ('server', 'server'),
        ('/add server $/asdf3$', 'server $/asdf3$')
    ]


@pytest.mark.parametrize('message,expected', testdata)
def test_positive__cut_command(message: str, expected: str):
    assert message_parsers.cut_command(message) == expected
