from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from configs.db import DB_URL


def create_scoped_session(db_url: str):
    """Создание фабрики сессий"""
    engine = sql.create_engine(db_url)
    return scoped_session(sessionmaker(bind=engine))


Base = declarative_base()

Session = create_scoped_session(db_url=DB_URL)


class User(Base):
    """Пользователь"""
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True)
    created_at = sql.Column(sql.DateTime, default=datetime.now())
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now, nullable=True)
    telegram_data = relationship('TelegramUser', backref='general_data', uselist=False)


class TelegramUser(Base):
    """Пользователь, авторизованный в телеграмм"""
    __tablename__ = 'telegram_users'

    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.VARCHAR(255), nullable=True)
    chat_id = sql.Column(sql.NUMERIC(10))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    inactive_at = sql.Column(sql.DateTime, nullable=True)
    created_at = sql.Column(sql.DateTime, default=datetime.now)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now, nullable=True)


class Record(Base):
    """Запись пользователя"""
    __tablename__ = 'records'

    id = sql.Column(sql.Integer, primary_key=True)
    text = sql.Column(sql.VARCHAR(3000))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = sql.Column(sql.DateTime, default=datetime.now)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now, nullable=True)

    user = relationship('User', backref=backref('records'))


class UserPrivateMessage(Base):
    """История сообщений пользователя"""
    __tablename__ = 'user_private_messages'

    id = sql.Column(sql.Integer, primary_key=True)
    message_id = sql.Column(sql.Integer)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('telegram_users.id', ondelete='CASCADE'))
    created_at = sql.Column(sql.DateTime, default=datetime.now)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now, nullable=True)

    user = relationship('TelegramUser', backref=backref('steps'))
