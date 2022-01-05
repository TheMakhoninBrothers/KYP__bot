import typing

from .base_exc import CommandNotFounded, WrongFormat


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


def delete_duplicate_items(items: typing.List[typing.Any]):
    """Убрать дубликаты из списка"""
    return list(set(items))
