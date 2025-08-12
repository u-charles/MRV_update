# db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Read DATABASE_URL from environment (Streamlit Secrets or env var),
# otherwise use local SQLite for development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./edumrv.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def init_db(seed_initial_factors: bool = True):
    """
    Create DB schema and optionally seed emission factors (only if table empty).
    Call at app startup.
    """
    Base.metadata.create_all(bind=engine)

    # lazy import to avoid circular import on startup
    from .crud import count_emission_factors, insert_emission_factor_if_empty
    try:
        db = SessionLocal()
        if seed_initial_factors and count_emission_factors(db) == 0:
            insert_emission_factor_if_empty(db)
        db.close()
    except Exception:
        # ignore seeding errors on some cloud initializations
        pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
