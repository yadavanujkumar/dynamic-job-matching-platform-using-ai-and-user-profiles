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

def initialize_database():
    """
    Initializes the database by creating all tables defined in ORM models.
    """
    try:
        # Import all models to ensure they are registered with Base
        from src.models import job_model, user_model
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")


def init_db():
    """
    Alias for initialize_database for backward compatibility
    """
    initialize_database()