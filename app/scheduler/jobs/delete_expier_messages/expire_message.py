from datetime import datetime, timedelta

from pydantic import BaseModel


class ExpireMessage(BaseModel):
    """Просроченное сообщение"""
    chat_id: int
    message_id: int
    created_at: datetime
    expire_timedelta: timedelta
