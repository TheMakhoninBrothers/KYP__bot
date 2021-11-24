from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from configs.db import DB_URL

Base = declarative_base()
engine = sql.create_engine(DB_URL)

connection = engine.connect()
SessionFactory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(SessionFactory)


class User(Base):
    """Пользователь"""
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, primary_key=True)
    created_at = sql.Column(sql.DateTime, default=datetime.now(), nullable=False)


class TelegramUser(Base):
    """Пользователь авторизованный в телеграмм"""
    __tablename__ = 'telegram_users'
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.VARCHAR(255), nullable=True)
    telegram_id = sql.Column(sql.VARCHAR(10), nullable=False)

    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)

    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref=backref('client', uselist=False))


class Record(Base):
    __tablename__ = 'records'
    id = sql.Column(sql.Integer, primary_key=True)
    text = sql.Column(sql.VARCHAR(3000), nullable=False)

    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref=backref('records'))
