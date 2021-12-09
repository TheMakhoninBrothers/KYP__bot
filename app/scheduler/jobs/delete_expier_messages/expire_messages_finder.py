import typing
from datetime import timedelta, datetime

from app import db
from .expire_message import ExpireMessage


class ExpireMessagesFinder:
    """Поисковик сообщений, которые просрочились."""

    def __init__(self, expire_time: timedelta):
        self._expire_time = expire_time

    def search(self) -> typing.List[ExpireMessage]:
        """Найти просроченные сообщения"""
        query = db.Session().query(db.UserHistory).filter(
            db.UserHistory.create_at < (datetime.now() - self._expire_time))
        return query.all()
