from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from src.services.matching_service import MatchingService

router = APIRouter()

# Initialize services
matching_service = MatchingService()


# Pydantic models for request/response validation
class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    required_skills: List[str] = Field(..., min_items=1)
    location: str = Field(..., min_length=1)
    company: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    experience_years: Optional[int] = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_skills: List[str]
    location: str
    company: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    experience_years: Optional[int]


class JobMatchRequest(BaseModel):
    skills: List[str] = Field(..., min_items=1)
    preferences: Optional[Dict] = Field(default_factory=dict)
    experience_years: Optional[int] = 0
    desired_location: Optional[str] = None


# In-memory storage for demonstration (replace with database in production)
jobs_db = {}
job_id_counter = 1


@router.post("/", response_model=Dict, status_code=201)
async def create_job(job: JobCreate):
    """
    Create a new job posting with validation.
    """
    global job_id_counter
    job_id = job_id_counter
    job_id_counter += 1
    
    job_data = job.dict()
    job_data["id"] = job_id
    jobs_db[job_id] = job_data
    
    return {"message": "Job created successfully", "job": job_data}


@router.get("/", response_model=Dict)
async def get_all_jobs(
    location: Optional[str] = Query(None, description="Filter by location"),
    skill: Optional[str] = Query(None, description="Filter by skill"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of jobs to return")
):
    """
    Retrieve all job postings with optional filters.
    """
    jobs = list(jobs_db.values())
    
    # Apply filters
    if location:
        jobs = [j for j in jobs if location.lower() in j.get("location", "").lower()]
    
    if skill:
        jobs = [j for j in jobs if any(skill.lower() in s.lower() for s in j.get("required_skills", []))]
    
    jobs = jobs[:limit]
    
    return {"jobs": jobs, "count": len(jobs)}


@router.get("/{job_id}", response_model=Dict)
async def get_job(job_id: int):
    """
    Retrieve a specific job posting by ID.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"job": jobs_db[job_id]}


@router.put("/{job_id}", response_model=Dict)
async def update_job(job_id: int, job: JobCreate):
    """
    Update an existing job posting.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = job.dict()
    job_data["id"] = job_id
    jobs_db[job_id] = job_data
    
    return {"message": "Job updated successfully", "job": job_data}


@router.delete("/{job_id}", response_model=Dict)
async def delete_job(job_id: int):
    """
    Delete a job posting by ID.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs_db[job_id]
    return {"message": "Job deleted successfully"}


@router.post("/match", response_model=Dict)
async def match_jobs(request: JobMatchRequest):
    """
    AI-powered endpoint to match jobs with user profile.
    Uses advanced NLP and machine learning for intelligent matching.
    """
    try:
        if not jobs_db:
            return {"message": "No jobs available for matching", "matched_jobs": [], "count": 0}
        
        user_profile = request.dict()
        job_postings = list(jobs_db.values())
        
        # Use the enhanced matching service
        matched_jobs = matching_service.match_jobs_with_scores(user_profile, job_postings)
        
        return {
            "message": "Matching completed successfully",
            "matched_jobs": matched_jobs,
            "count": len(matched_jobs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")