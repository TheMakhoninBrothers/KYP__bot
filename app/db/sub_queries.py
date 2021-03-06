import typing
from collections.abc import Iterable

from app import db


def add_filter_by_substring_for__record(query, sub_strings: typing.Union[typing.List[str], str]):
    """Добавление фильтра по подстроке в записи пользователя"""
    if isinstance(sub_strings, Iterable):
        for sub_string in sub_strings:
            query = add_filter_by_substring(query, db.Record.text, sub_string)
    elif isinstance(sub_strings, str):
        query = add_filter_by_substring(query, db.Record.text, sub_strings)
    return query


def add_filter_by_substring(query, field, sub_string: str):
    """Добавление фильтра по подстроке"""
    return query.filter(field.ilike(f'%{sub_string}%'))
