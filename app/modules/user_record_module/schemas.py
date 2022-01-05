from pydantic import BaseModel
import typing


class Record(BaseModel):
    """Сохранённая запись пользователя"""
    tags: typing.List[str]
    text: str


class RecordFromDB(Record):
    """Сохраненная запись пользователя из БД"""
    id: int
