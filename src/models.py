from sqlalchemy import MetaData, Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class ReferalLink(Base):
    __tablename__ = 'referal_links'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),
                     unique=True)
    link = Column(String, unique=True, nullable=True)
    life_time = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    user = relationship('User', back_populates='referal_link')


class Invited(Base):
    __tablename__ = 'invited'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_inviting_id = Column(Integer, ForeignKey('users.id'),
                              unique=False)
    user_invited_id = Column(Integer, ForeignKey('users.id'),
                             unique=True)
    referal_head = Column(String, unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    date_registration = Column(DateTime, server_default=func.now())
    refresh_token = Column(String)

    referal_link = relationship(
        'ReferalLink', backref='user_links', uselist=False, lazy='select')
    inviter = relationship(
        'Invited', backref='user_inviter', uselist=True, lazy='select', foreign_keys=[Invited.user_inviting_id]
    )
    invited = relationship(
        'Invited', backref='user_invited', uselist=False, lazy='select', foreign_keys=[Invited.user_invited_id]
    )
# class UsedLinks(Base):
#     __tablename__ = 'used_links'

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     link = Column(String, unique=True, nullable=True)
#     user = Relationship('User', back_populates='id')
