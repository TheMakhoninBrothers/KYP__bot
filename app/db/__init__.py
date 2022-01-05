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
    user = relationship('User', backref=backref('telegram', uselist=False), uselist=False)


records_tags_link = sql.Table(
    'pivot_records_tags',
    Base.metadata,
    sql.Column('record_id', sql.ForeignKey('records.id')),
    sql.Column('tag_id', sql.ForeignKey('tags.id')),
    sql.Column('created_at', sql.DateTime, default=datetime.now, nullable=False),
    sql.Column('updated_at', sql.DateTime, default=None, onupdate=datetime.now),
    sql.PrimaryKeyConstraint('record_id', 'tag_id'),
)


class Record(Base):
    """Запись пользователя"""
    __tablename__ = 'records'

    id = sql.Column(sql.Integer, primary_key=True)
    text = sql.Column(sql.VARCHAR(3000), nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)
    tags = relationship('Tag', backref=backref('records'), secondary=records_tags_link)
    user = relationship('User', backref=backref('records'))


class Tag(Base):
    """Тэг пользователя"""
    __tablename__ = 'tags'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = sql.Column(sql.VARCHAR(100), nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)

    __table_args__ = \
        (
            sql.UniqueConstraint('user_id', 'name', name='_user_tag_uc'),
        )


class UserPrivateMessage(Base):
    """История сообщений пользователя"""
    __tablename__ = 'user_private_messages'

    id = sql.Column(sql.Integer, primary_key=True)
    message_id = sql.Column(sql.Integer, nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users_from_telegram.id', ondelete='CASCADE'), nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.now, nullable=False)
    updated_at = sql.Column(sql.DateTime, default=None, onupdate=datetime.now)

    user = relationship('UserFromTelegram', backref=backref('steps'))
