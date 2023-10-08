# models.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Example(Base):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
