import re
import typing

from .user_record_module.schemas import Record

TAGS_PATTERN = r'(#\w+)|(<>.+<>)'


def parse_tags(message: str) -> typing.List[str]:
    """Парсинг тегов"""
    tags = [item[0] for item in re.findall(TAGS_PATTERN, message)]
    return serialize_tags(tags)


def serialize_tags(tags: typing.List[str]) -> typing.List[str]:
    """Привести теги к единому формату"""
    handled_data = []
    for tag in tags:
        if tag:
            tag = tag.replace('#', '')
            tag = tag.lower()
            handled_data.append(tag)
    return handled_data


def parse_new_record(message: str) -> Record:
    """Парсинг информации в сообщении"""
    tags = parse_tags(message)
    return Record(tags=tags, text=message)
