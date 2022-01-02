from app.modules.message_parsers import parse_tags


def test_positive__parse_tags(positive__messages_for_parse_tags):
    """
    Позитивный тест.
    Парсер тегов.
    """
    for test_data in positive__messages_for_parse_tags:
        assert parse_tags(test_data.input) == test_data.output
