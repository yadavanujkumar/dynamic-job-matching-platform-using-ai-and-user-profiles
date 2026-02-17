import unittest
from datetime import datetime
from models import UserProfile, Job, Match
from unittest.mock import patch

class TestUserProfileModel(unittest.TestCase):
    def setUp(self):
        self.valid_user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "skills": ["Python", "Machine Learning", "Docker"],
            "experience_years": 5,
            "created_at": datetime.now(),
        }

    def test_user_profile_creation(self):
        user = UserProfile(**self.valid_user_data)
        self.assertEqual(user.id, self.valid_user_data["id"])
        self.assertEqual(user.name, self.valid_user_data["name"])
        self.assertEqual(user.email, self.valid_user_data["email"])
        self.assertEqual(user.skills, self.valid_user_data["skills"])
        self.assertEqual(user.experience_years, self.valid_user_data["experience_years"])
        self.assertIsInstance(user.created_at, datetime)

    def test_user_profile_invalid_email(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data["email"] = "invalid-email"
        with self.assertRaises(ValueError):
            UserProfile(**invalid_data)

    def test_user_profile_missing_required_field(self):
        invalid_data = self.valid_user_data.copy()
        del invalid_data["name"]
        with self.assertRaises(KeyError):
            UserProfile(**invalid_data)


class TestJobModel(unittest.TestCase):
    def setUp(self):
        self.valid_job_data = {
            "id": 101,
            "title": "Senior Software Engineer",
            "description": "Develop and maintain software solutions.",
            "required_skills": ["Python", "Docker", "JavaScript"],
            "posted_at": datetime.now(),
        }

    def test_job_creation(self):
        job = Job(**self.valid_job_data)
        self.assertEqual(job.id, self.valid_job_data["id"])
        self.assertEqual(job.title, self.valid_job_data["title"])
        self.assertEqual(job.description, self.valid_job_data["description"])
        self.assertEqual(job.required_skills, self.valid_job_data["required_skills"])
        self.assertIsInstance(job.posted_at, datetime)

    def test_job_missing_required_field(self):
        invalid_data = self.valid_job_data.copy()
        del invalid_data["title"]
        with self.assertRaises(KeyError):
            Job(**invalid_data)

    def test_job_invalid_skills_type(self):
        invalid_data = self.valid_job_data.copy()
        invalid_data["required_skills"] = "Python, Docker, JavaScript"
        with self.assertRaises(TypeError):
            Job(**invalid_data)


class TestMatchModel(unittest.TestCase):
    def setUp(self):
        self.valid_match_data = {
            "id": 1001,
            "user_id": 1,
            "job_id": 101,
            "score": 0.85,
            "matched_at": datetime.now(),
        }

    def test_match_creation(self):
        match = Match(**self.valid_match_data)
        self.assertEqual(match.id, self.valid_match_data["id"])
        self.assertEqual(match.user_id, self.valid_match_data["user_id"])
        self.assertEqual(match.job_id, self.valid_match_data["job_id"])
        self.assertAlmostEqual(match.score, self.valid_match_data["score"], places=2)
        self.assertIsInstance(match.matched_at, datetime)

    def test_match_invalid_score(self):
        invalid_data = self.valid_match_data.copy()
        invalid_data["score"] = 1.5  # Score should be between 0 and 1
        with self.assertRaises(ValueError):
            Match(**invalid_data)

    def test_match_missing_required_field(self):
        invalid_data = self.valid_match_data.copy()
        del invalid_data["user_id"]
        with self.assertRaises(KeyError):
            Match(**invalid_data)


if __name__ == "__main__":
    unittest.main()