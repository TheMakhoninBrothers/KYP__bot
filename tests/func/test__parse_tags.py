from app.resourses.helpers import parse_tags


def test_positive__input_data(messages_for_search_by_tags):
    for test_data in messages_for_search_by_tags:
        assert parse_tags(test_data.input) == test_data.output
