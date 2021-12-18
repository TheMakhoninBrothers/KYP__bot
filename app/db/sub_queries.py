import typing
from collections.abc import Iterable

from app import db


def add_filter_in_text(query, sub_strings: typing.Union[typing.List[str], str]):
    """Добавить фильтр поля текст по подстроке."""
    if isinstance(sub_strings, Iterable):
        for sub_string in sub_strings:
            query = add_filter_by_substring(query, db.Record.text, sub_string)
    elif isinstance(sub_strings, str):
        query = add_filter_by_substring(query, db.Record.text, sub_strings)
    return query


def add_filter_by_substring(query, field, sub_string: str):
    """Добавить фильтр по подстроке"""
    return query.filter(field.ilike(f'%{sub_string}%'))
