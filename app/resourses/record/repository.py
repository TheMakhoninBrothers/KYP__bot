import typing

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
    def read_all(cls, user_chat_id: typing.Optional[str]) -> typing.List[RecordFromDB]:
        query = db.Session().query(db.Record)
        if user_chat_id:
            query = query.join(db.User, db.TelegramUser).filter(db.TelegramUser.telegram_id == user_chat_id)
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


__all__ = ['RecordRepository']
