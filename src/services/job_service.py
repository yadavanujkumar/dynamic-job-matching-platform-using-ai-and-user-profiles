import uuid
from datetime import datetime
from typing import List, Dict, Optional

from src.database.job_repository import JobRepository
from src.models.job import Job
from src.utils.exceptions import JobNotFoundException, InvalidJobDataException


class JobService:
    def __init__(self, job_repository: JobRepository):
        """
        Initializes the JobService with a JobRepository instance.
        :param job_repository: Instance of JobRepository for database operations.
        """
        self.job_repository = job_repository

    def create_job(self, job_data: Dict) -> Job:
        """
        Creates a new job posting.
        :param job_data: Dictionary containing job details.
        :return: The created Job object.
        """
        required_fields = ["title", "description", "company_name", "location", "salary", "skills_required"]
        for field in required_fields:
            if field not in job_data or not job_data[field]:
                raise InvalidJobDataException(f"Missing or invalid field: {field}")

        job_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        job = Job(
            id=job_id,
            title=job_data["title"],
            description=job_data["description"],
            company_name=job_data["company_name"],
            location=job_data["location"],
            salary=job_data["salary"],
            skills_required=job_data["skills_required"],
            created_at=created_at,
            updated_at=created_at,
        )
        self.job_repository.save(job)
        return job

    def update_job(self, job_id: str, updated_data: Dict) -> Job:
        """
        Updates an existing job posting.
        :param job_id: ID of the job to update.
        :param updated_data: Dictionary containing updated job details.
        :return: The updated Job object.
        """
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise JobNotFoundException(f"Job with ID {job_id} not found.")

        for key, value in updated_data.items():
            if hasattr(job, key) and value:
                setattr(job, key, value)

        job.updated_at = datetime.utcnow()
        self.job_repository.save(job)
        return job

    def get_job_by_id(self, job_id: str) -> Job:
        """
        Retrieves a job posting by its ID.
        :param job_id: ID of the job to retrieve.
        :return: The Job object.
        """
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise JobNotFoundException(f"Job with ID {job_id} not found.")
        return job

    def get_all_jobs(self) -> List[Job]:
        """
        Retrieves all job postings.
        :return: List of Job objects.
        """
        return self.job_repository.get_all()

    def search_jobs(self, filters: Dict) -> List[Job]:
        """
        Searches for jobs based on filters.
        :param filters: Dictionary containing search criteria (e.g., location, skills_required).
        :return: List of Job objects matching the criteria.
        """
        jobs = self.job_repository.get_all()
        filtered_jobs = []

        for job in jobs:
            match = True
            for key, value in filters.items():
                if hasattr(job, key) and value:
                    job_value = getattr(job, key)
                    if isinstance(job_value, list):
                        if not any(skill.lower() in [v.lower() for v in job_value] for skill in value):
                            match = False
                            break
                    elif isinstance(job_value, str):
                        if value.lower() not in job_value.lower():
                            match = False
                            break
                    else:
                        if job_value != value:
                            match = False
                            break
            if match:
                filtered_jobs.append(job)

        return filtered_jobs

    def delete_job(self, job_id: str) -> None:
        """
        Deletes a job posting by its ID.
        :param job_id: ID of the job to delete.
        """
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise JobNotFoundException(f"Job with ID {job_id} not found.")
        self.job_repository.delete(job_id)