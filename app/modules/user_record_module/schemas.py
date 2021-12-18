from pydantic import BaseModel


class Record(BaseModel):
    """Сохранённая запись пользователя"""
    text: str


class RecordFromDB(Record):
    """Сохраненная запись пользователя из БД"""
    id: int
