from app.modules.helpers import parse_tags

import pytest


def test_positive__input_data(positive__messages_for_search_by_tags):
    for test_data in positive__messages_for_search_by_tags:
        assert parse_tags(test_data.input) == test_data.output


def test_negative__input_data(negative__messages_for_search_by_tags):
    for test_data in negative__messages_for_search_by_tags:
        with pytest.raises(test_data.output):
            parse_tags(test_data.input)
