import re
import typing
from configs.bot import SEARCH_TAGS_REGEX


def parse_tags(message_text: str, pattern: typing.Optional[str] = None):
    """Запарсить теги в строке"""
    pattern = pattern or SEARCH_TAGS_REGEX
    sub_strings = re.findall(fr'{pattern}', message_text)
    return [item.replace('#', '').lower() for item in sub_strings]
