from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Job(Base):
    """
    Job model representing job postings in the Dynamic Job Matching Platform.
    """
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)  # Comma-separated list of skills
    location = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, location={self.location})>"

# Database setup
DATABASE_URL = "sqlite:///jobs.db"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example usage
if __name__ == "__main__":
    # Create a new session
    session = SessionLocal()

    # Add mock data
    mock_jobs = [
        Job(
            title="Senior Software Engineer",
            description="Develop and maintain scalable software solutions.",
            required_skills="Python, Docker, SQLAlchemy, JavaScript",
            location="San Francisco, CA"
        ),
        Job(
            title="Data Scientist",
            description="Analyze data and build predictive models.",
            required_skills="Python, Machine Learning, SQL, Data Visualization",
            location="New York, NY"
        ),
        Job(
            title="Frontend Developer",
            description="Create responsive and user-friendly web interfaces.",
            required_skills="JavaScript, React, HTML, CSS",
            location="Austin, TX"
        ),
        Job(
            title="DevOps Engineer",
            description="Implement CI/CD pipelines and manage cloud infrastructure.",
            required_skills="Docker, Kubernetes, AWS, Linux",
            location="Seattle, WA"
        )
    ]

    # Add jobs to the database
    session.bulk_save_objects(mock_jobs)
    session.commit()

    # Query and print all jobs
    jobs = session.query(Job).all()
    for job in jobs:
        print(job)

    # Close the session
    session.close()