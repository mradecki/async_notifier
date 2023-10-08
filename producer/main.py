import random
import time

from config import settings
from database import init_db, robust
from models import Base, Example


@robust
def insert_row(session):
    try:
        new_entry = Example(name=f"Random name {random.randint(1, 1000)}")
        session.add(new_entry)
        session.commit()
        print(f"Inserted row with ID: {new_entry.id}")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise  # Re-raise the exception for the decorator to catch and handle

def main():
    engine, SessionLocal = init_db()

    while True:
        session = SessionLocal()  # Create a session for this iteration
        insert_row(session)
        session.close()  # Close the session after using it

        print(f"Sleeping for {settings.sleep_time} seconds...")
        time.sleep(settings.sleep_time)

if __name__ == "__main__":
    main()
