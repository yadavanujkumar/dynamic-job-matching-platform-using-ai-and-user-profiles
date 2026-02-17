from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Base class for ORM models
Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dynamic_job_matching")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a scoped session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    """
    Dependency to get the database session.
    Ensures proper session management.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all tables defined in ORM models.
    """
    import src.database.models  # Import all models to ensure they are registered with Base
    Base.metadata.create_all(bind=engine)