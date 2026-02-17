#!/usr/bin/env python3
"""
Demo script showcasing the Dynamic Job Matching Platform features
"""
import requests
import json
import time
from typing import Dict

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_response(response: requests.Response, title: str = "Response"):
    """Print formatted response"""
    print(f"{title}:")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print(f"Status Code: {response.status_code}\n")


def main():
    print("🎯 Dynamic Job Matching Platform - Demo")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✓ Server is running")
        print_response(response, "Welcome Message")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running. Please start the server first:")
        print("   ./start.sh")
        return
    
    # Create sample jobs
    print_section("1. Creating Sample Job Postings")
    
    jobs = [
        {
            "title": "Senior Python Developer",
            "description": "We're looking for an experienced Python developer with ML expertise",
            "required_skills": ["Python", "Machine Learning", "Docker", "AWS"],
            "location": "San Francisco, CA",
            "company": "TechCorp",
            "salary_min": 120000,
            "salary_max": 180000,
            "experience_years": 5
        },
        {
            "title": "Data Scientist",
            "description": "Join our data science team to build predictive models",
            "required_skills": ["Python", "Machine Learning", "Statistics", "SQL"],
            "location": "New York, NY",
            "company": "DataCo",
            "salary_min": 100000,
            "salary_max": 150000,
            "experience_years": 3
        },
        {
            "title": "Frontend Developer",
            "description": "Build beautiful user interfaces with React",
            "required_skills": ["JavaScript", "React", "HTML", "CSS"],
            "location": "Austin, TX",
            "company": "WebDev Inc",
            "salary_min": 90000,
            "salary_max": 130000,
            "experience_years": 2
        }
    ]
    
    for i, job in enumerate(jobs, 1):
        response = requests.post(f"{BASE_URL}/jobs/", json=job)
        print(f"Created job {i}: {job['title']} (Status: {response.status_code})")
    
    # Get all jobs
    print_section("2. Retrieving All Jobs")
    response = requests.get(f"{BASE_URL}/jobs/")
    print_response(response, "All Jobs")
    
    # Test job filtering
    print_section("3. Filtering Jobs by Skill")
    response = requests.get(f"{BASE_URL}/jobs/?skill=Python")
    data = response.json()
    print(f"Found {data['count']} jobs matching 'Python':")
    for job in data['jobs']:
        print(f"  - {job['title']} at {job['company']}")
    
    # Register a user
    print_section("4. Registering a User")
    user_data = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "password": "securepassword123",
        "skills": ["Python", "Machine Learning", "Docker"]
    }
    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print_response(response, "User Registration")
    
    # Login
    print_section("5. User Login")
    login_data = {
        "email": "alice@example.com",
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    token_data = response.json()
    print_response(response, "Login Response")
    token = token_data.get("token")
    
    # Get user profile
    if token:
        print_section("6. Getting User Profile")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
        print_response(response, "User Profile")
        
        # Update profile
        print_section("7. Updating User Profile")
        profile_update = {
            "experience_years": 5,
            "desired_location": "San Francisco",
            "bio": "Experienced ML engineer passionate about AI"
        }
        response = requests.put(f"{BASE_URL}/users/profile", json=profile_update, headers=headers)
        print_response(response, "Updated Profile")
    
    # AI-Powered Job Matching
    print_section("8. AI-Powered Job Matching")
    match_request = {
        "skills": ["Python", "Machine Learning", "Docker"],
        "experience_years": 4,
        "desired_location": "San Francisco"
    }
    response = requests.post(f"{BASE_URL}/jobs/match", json=match_request)
    match_data = response.json()
    
    print(f"Matched {match_data['count']} jobs:")
    print()
    
    for i, match in enumerate(match_data['matched_jobs'], 1):
        job = match['job']
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Overall Score: {match['overall_score']*100:.1f}%")
        print(f"   - Skill Match: {match['skill_match']*100:.1f}%")
        print(f"   - Text Similarity: {match['text_similarity']*100:.1f}%")
        print(f"   - Experience Match: {match['experience_match']*100:.1f}%")
        print(f"   - Location Match: {match['location_match']*100:.1f}%")
        print(f"   Explanation: {match['match_explanation']}")
        print()
    
    print_section("Demo Complete!")
    print("✅ All features demonstrated successfully!")
    print("\n💡 Tip: Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    main()
