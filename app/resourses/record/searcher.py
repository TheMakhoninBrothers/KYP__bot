import typing

from .repository import RecordRepository
from .schemas import RecordFromDB
from ..user.repository import TelegramUserRepository


class RecordSearcher:
    """Поисковик записей."""

    def __init__(self, chat_id: str):
        self.user = TelegramUserRepository.read(str(chat_id))

    def by_tags(self, *tags) -> typing.List[RecordFromDB]:
        """Поиск по тегам."""
        return RecordRepository.read_all(user_chat_id=self.user.chat_id,
                                         text=[f'#{tag}' for tag in tags],
                                         )
