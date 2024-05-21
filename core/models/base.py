from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer


class Base(DeclarativeBase):

    __abstract__ = True
