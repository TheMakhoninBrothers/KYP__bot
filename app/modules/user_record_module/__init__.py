import typing

from sqlalchemy.exc import NoResultFound

from app import db
from app.db import queries, sub_queries
from . import exc
from .schemas import Record, RecordFromDB


class UserRecordModule:
    """
    Репозиторий.
    Чтение и сохранение записей пользователя.
    """

    def __init__(self, chat_id: int):
        self._chat_id = chat_id
        self._user: db.User = queries.find_user_by__chat_id(chat_id).one()

    def add(self, record: Record) -> RecordFromDB:
        """Добавление записи пользователем"""
        new_record = db.Record(user=self._user, text=record.text)
        db.Session().add(new_record)
        db.Session().commit()
        return RecordFromDB(id=new_record.id, **record.dict())

    def find(self, record_id: int) -> RecordFromDB:
        """Поиск записи пользователя по номеру"""
        try:
            record = queries.find_records_by__user(self._user).filter(db.Record.id == record_id).one()
            return RecordFromDB(
                id=record.id,
                text=record.text,
            )
        except NoResultFound:
            raise exc.RecordNotFounded(record_id)

    def find_all(self, **kwargs) -> typing.List[RecordFromDB]:
        """
        Поиск всех записей пользователя.
        **kwargs - можно передать фильтр параметры.
        :key text - принимает str и List[str]. Добавляет поиск по подстроке в поле text.
        """
        sub_query = queries.find_records_by__user(self._user)
        if kwargs.get('text'):
            sub_query = sub_queries.add_filter_by_substring_for__record(sub_query, kwargs['text'])

        return [RecordFromDB(id=item.id, text=item.text) for item in sub_query.all()]

    def delete(self, record_id: int):
        """Удаление записи пользователя"""
        try:
            record = queries.find_records_by__user(self._user).filter(db.Record.id == record_id).one()
            db.Session().delete(record)
            db.Session().commit()
        except NoResultFound:
            raise exc.RecordNotFounded(record_id)


__all__ = [
    'Record',
    'RecordFromDB',
    'UserRecordModule',
]
