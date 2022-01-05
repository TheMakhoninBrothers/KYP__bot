import re
import typing

from aiogram.types import Message

from .user_record_module.schemas import Record

TAGS_PATTERN = r'(#\w+)|(<>.+<>)'
SEC_PATTERN = r'<>[\d\w\!@#$%^&*()<>]+<>'
SEARCH_TAGS_PATTERN = r'\w+'
DETECT_COMMAND = r'^\/[\w]+'


def parse_security_data(message: str) -> typing.List[str]:
    """Парсинг секретной информации"""
    security_data = re.findall(SEC_PATTERN, message)
    return serialize_security_data(security_data)


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


def serialize_security_data(security_data: typing.List[str]) -> typing.List[str]:
    """Привести теги к единому формату"""
    handled_data = []
    for data in security_data:
        if data:
            data = data.strip()
            data = data.replace('<>', '')
            handled_data.append(data)
    return handled_data


def cut_command(message: str) -> str:
    """Обрезание команды в строке"""
    return re.sub(DETECT_COMMAND, '', message).strip()


def parse_message__add_record(message: Message) -> Record:
    """Парсинг информации в сообщении"""
    html_text = cut_command(message.html_text)
    tags = parse_tags(html_text)
    return Record(tags=tags, text=html_text)


def parse_message__search_by_tags(message: Message) -> typing.List[str]:
    """Парсинг тегов в строке"""
    sub_strings = re.findall(SEARCH_TAGS_PATTERN, message.text)
    return sub_strings
