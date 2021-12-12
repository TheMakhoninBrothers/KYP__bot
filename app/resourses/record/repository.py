import typing
from collections.abc import Iterable

from app import db
from .schemas import Record, RecordFromDB


class RecordRepository:

    @classmethod
    def is_exist(cls, **kwargs):
        pass

    @classmethod
    def create(cls, record: Record) -> RecordFromDB:
        query = db.Session().query(db.User).join(db.TelegramUser).filter(db.TelegramUser.telegram_id == record.chat_id)
        user = query.one()
        new_record = db.Record(user=user,
                               text=record.text,
                               )
        db.Session().add(new_record)
        db.Session().commit()
        return RecordFromDB(id=new_record.id,
                            **record.dict()
                            )

    @classmethod
    def read(cls, record_id: int):
        record = db.Session().query(db.Record).get(record_id)
        return RecordFromDB(id=record.id,
                            text=record.text,
                            chat_id=record.user.client.telegram_id,
                            )

    @classmethod
    def read_all(cls, user_chat_id: typing.Optional[str] = None, **kwargs) -> typing.List[RecordFromDB]:
        """
        Получить все записи пользователя с user_chat_id.
        **kwargs - можно передать фильтр параметры.
        :key text - принимает str и List[str]. Добавляет поиск по подстроке в поле text.
        """
        query = db.Session().query(db.Record)
        if user_chat_id:
            query = query.join(db.User, db.TelegramUser).filter(db.TelegramUser.telegram_id == user_chat_id)
        if kwargs.get('text'):
            query = cls._add_filter_in_text(query, kwargs['text'])
        return [RecordFromDB(id=item.id,
                             text=item.text,
                             chat_id=item.user.client.telegram_id,
                             )
                for item in query.all()]

    @classmethod
    def delete(cls, record_id: int):
        record = db.Session().query(db.Record).get(record_id)
        db.Session().delete(record)
        db.Session().commit()

    @classmethod
    def _add_filter_in_text(cls, query, sub_strings: typing.Union[typing.List[str], str]):
        """Добавить фильтр поля текст по подстроке."""
        if isinstance(sub_strings, Iterable):
            for sub_string in sub_strings:
                query = cls._add_filter_by_substring(query, db.Record.text, sub_string)
        elif isinstance(sub_strings, str):
            query = cls._add_filter_by_substring(query, db.Record.text, sub_strings)
        return query

    @classmethod
    def _add_filter_by_substring(cls, query, field, sub_string: str):
        """Добавить фильтр по подстроке"""
        return query.filter(field.ilike(f'%{sub_string}%'))


__all__ = ['RecordRepository']
