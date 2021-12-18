import re
import typing

from configs.bot import SEARCH_TAGS_REGEX
from .base_exc import CommandNotFounded, WrongFormat, CommandDoesNotExist


def parse_tags(message_text: str, pattern: typing.Optional[str] = None):
    """Парсинг тегов в строке"""
    if '/' in message_text:
        raise WrongFormat(message_text)
    pattern = pattern or SEARCH_TAGS_REGEX
    sub_strings = re.findall(fr'{pattern}', message_text)
    return [item.replace('#', '').lower() for item in sub_strings]


def parse_record_id(command: str, text: str) -> typing.Optional[int]:
    """Парсинг номера записи"""
    if not text.startswith(command):
        raise CommandNotFounded(command, text)
    count_command_letters = len(command)
    total_letters = len(text)
    if count_command_letters == total_letters:
        return None
    try:
        return int(text[count_command_letters:].strip())
    except ValueError:
        raise WrongFormat(text)
