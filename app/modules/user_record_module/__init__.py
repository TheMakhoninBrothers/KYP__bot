import typing

from sqlalchemy.exc import NoResultFound

from app import db
from app.db import queries
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
        tags = []
        for tag in record.tags:
            tag_from_db = db.Session().query(db.Tag).filter_by(name=tag, user_id=self._user.id).one_or_none()
            if not tag_from_db:
                new_tag = db.Tag(name=tag, user_id=self._user.id)
                tags.append(new_tag)
                db.Session().add(new_tag)
            else:
                tags.append(tag_from_db)
        new_record.tags = tags
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
                tags=[tag.name for tag in record.tags]
            )
        except NoResultFound:
            raise exc.RecordNotFounded(record_id)

    def find_all(self, tags: typing.Optional[typing.List[str]] = None) -> typing.List[RecordFromDB]:
        """
        Поиск всех записей пользователя.
        tags - реализует поиск по тегам.
        """
        if tags:
            query = queries.find_records__by_tags(self._user, tags)
            return [
                RecordFromDB(id=item[0].id, text=item[0].text, tags=[tag.name for tag in item[0].tags])
                for item in query.all()
            ]
        query = queries.find_records_by__user(self._user)
        return [
            RecordFromDB(id=item.id, text=item.text, tags=[tag.name for tag in item.tags])
            for item in query.all()
        ]

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
