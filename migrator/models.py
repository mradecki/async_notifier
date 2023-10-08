from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Example(Base):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True)
    name = Column(String)
