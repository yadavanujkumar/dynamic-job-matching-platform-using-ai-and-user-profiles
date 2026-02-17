import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_user_profiles():
    return [
        {"id": 1, "name": "Alice", "skills": ["Python", "Machine Learning"], "experience": 5},
        {"id": 2, "name": "Bob", "skills": ["JavaScript", "React"], "experience": 3},
        {"id": 3, "name": "Charlie", "skills": ["Docker", "Kubernetes"], "experience": 7},
        {"id": 4, "name": "Diana", "skills": ["Python", "Data Analysis"], "experience": 4},
    ]

@pytest.fixture
def mock_jobs():
    return [
        {"id": 101, "title": "Python Developer", "required_skills": ["Python"], "min_experience": 3},
        {"id": 102, "title": "Frontend Developer", "required_skills": ["JavaScript", "React"], "min_experience": 2},
        {"id": 103, "title": "DevOps Engineer", "required_skills": ["Docker", "Kubernetes"], "min_experience": 5},
        {"id": 104, "title": "Data Analyst", "required_skills": ["Python", "Data Analysis"], "min_experience": 3},
    ]

@pytest.fixture
def mock_matching_results():
    return [
        {"user_id": 1, "job_id": 101},
        {"user_id": 2, "job_id": 102},
        {"user_id": 3, "job_id": 103},
        {"user_id": 4, "job_id": 104},
    ]

def test_get_user_profiles(mock_user_profiles):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == mock_user_profiles

def test_get_jobs(mock_jobs):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() == mock_jobs

def test_match_jobs(mock_user_profiles, mock_jobs, mock_matching_results):
    response = client.post("/match", json={"users": mock_user_profiles, "jobs": mock_jobs})
    assert response.status_code == 200
    assert response.json() == mock_matching_results

def test_get_matching_results(mock_matching_results):
    response = client.get("/matches")
    assert response.status_code == 200
    assert response.json() == mock_matching_results

def test_invalid_user_profile():
    response = client.post("/users", json={"id": 5, "name": "Eve", "skills": [], "experience": -1})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid user profile data"}

def test_invalid_job_posting():
    response = client.post("/jobs", json={"id": 105, "title": "Invalid Job", "required_skills": [], "min_experience": -1})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid job posting data"}

def test_no_matching_jobs():
    user_profiles = [{"id": 5, "name": "Eve", "skills": ["C++"], "experience": 1}]
    jobs = [{"id": 106, "title": "Senior Developer", "required_skills": ["Java"], "min_experience": 10}]
    response = client.post("/match", json={"users": user_profiles, "jobs": jobs})
    assert response.status_code == 200
    assert response.json() == []