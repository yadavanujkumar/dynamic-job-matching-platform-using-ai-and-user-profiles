from sqlalchemy import Column, String, Integer, Text, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    skills = Column(JSON, nullable=False)  # List of skills as JSON
    preferences = Column(JSON, nullable=True)  # User preferences as JSON
    bio = Column(Text, nullable=True)  # Optional user bio

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

# Database setup
DATABASE_URL = "sqlite:///./job_matching.db"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

# Session setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example usage
if __name__ == "__main__":
    # Create a new session
    session = SessionLocal()

    # Add a sample user
    sample_user = User(
        name="John Doe",
        email="john.doe@example.com",
        skills=["Python", "Machine Learning", "Docker"],
        preferences={"remote": True, "preferred_roles": ["Data Scientist", "AI Engineer"]},
        bio="Experienced software engineer with a passion for AI and data science."
    )

    session.add(sample_user)
    session.commit()

    # Query users
    users = session.query(User).all()
    for user in users:
        print(user)

    session.close()