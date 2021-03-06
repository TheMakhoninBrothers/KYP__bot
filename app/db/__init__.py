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
    created_at = sql.Column(sql.DateTime, default=datetime.now(), nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)
    telegram_data = relationship('UserFromTelegram', uselist=False)


class UserFromTelegram(Base):
    """Пользователь, авторизованный в телеграмм"""
    __tablename__ = 'users_from_telegram'

    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.VARCHAR(255), unique=True)
    chat_id = sql.Column(sql.NUMERIC(10), nullable=False, unique=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    inactive_at = sql.Column(sql.DateTime)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)
    user = relationship('User', uselist=False)


class Record(Base):
    """Запись пользователя"""
    __tablename__ = 'records'

    id = sql.Column(sql.Integer, primary_key=True)
    text = sql.Column(sql.VARCHAR(3000), nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)

    user = relationship('User', backref=backref('records'))


class UserPrivateMessage(Base):
    """История сообщений пользователя"""
    __tablename__ = 'user_private_messages'

    id = sql.Column(sql.Integer, primary_key=True)
    message_id = sql.Column(sql.Integer, nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users_from_telegram.id', ondelete='CASCADE'), nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)

    user = relationship('UserFromTelegram', backref=backref('steps'))
