import functools
import time

from config import settings
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker


def init_db():
    # Configure the engine with a connection pool
    engine = create_engine(
        settings.db_uri.unicode_string(), 
        pool_size=5, 
        pool_recycle=3600,  # Recycle connections after 1 hour
        pool_pre_ping=True  # Check the connection for liveness before using it
    )
    SessionLocal = sessionmaker(bind=engine)
    return engine, SessionLocal


def robust(func):
    @functools.wraps(func)
    def wrapper_robust(*args, **kwargs):
        for _ in range(settings.max_retries):
            try:
                return func(*args, **kwargs)
            except (exc.OperationalError, exc.DBAPIError) as e:
                print(f"Database error encountered: {e}. Retrying...")
                time.sleep(1)
        else:
            print("Failed to execute the operation after several retries.")
    return wrapper_robust
