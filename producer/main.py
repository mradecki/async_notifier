import os
import time
import random
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ["DB_URI"]

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Example(Base):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

def insert_row():
    session = SessionLocal()
    try:
        new_entry = Example(name=f"Random name {random.randint(1, 1000)}")
        session.add(new_entry)
        session.commit()
        print(f"Inserted row with ID: {new_entry.id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def main():
    while True:
        insert_row()
        sleep_time = random.randint(5, 15)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
