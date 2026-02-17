import unittest
from unittest.mock import patch, MagicMock
from services.job_service import JobService
from services.user_service import UserService

class TestJobService(unittest.TestCase):
    def setUp(self):
        self.job_service = JobService()

    @patch('services.job_service.JobRepository')
    def test_get_jobs_for_user(self, MockJobRepository):
        # Mocking the repository
        mock_repo = MockJobRepository.return_value
        mock_repo.get_jobs.return_value = [
            {"id": 1, "title": "Software Engineer", "skills": ["Python", "Docker"]},
            {"id": 2, "title": "Data Scientist", "skills": ["Python", "Machine Learning"]},
            {"id": 3, "title": "Frontend Developer", "skills": ["JavaScript", "React"]}
        ]

        user_profile = {
            "id": 101,
            "name": "Alice",
            "skills": ["Python", "Docker", "Machine Learning"]
        }

        # Call the service method
        jobs = self.job_service.get_jobs_for_user(user_profile)

        # Assert the results
        self.assertEqual(len(jobs), 2)
        self.assertIn({"id": 1, "title": "Software Engineer", "skills": ["Python", "Docker"]}, jobs)
        self.assertIn({"id": 2, "title": "Data Scientist", "skills": ["Python", "Machine Learning"]}, jobs)

    @patch('services.job_service.JobRepository')
    def test_get_jobs_for_user_no_match(self, MockJobRepository):
        # Mocking the repository
        mock_repo = MockJobRepository.return_value
        mock_repo.get_jobs.return_value = [
            {"id": 1, "title": "Software Engineer", "skills": ["Python", "Docker"]},
            {"id": 2, "title": "Data Scientist", "skills": ["Python", "Machine Learning"]},
            {"id": 3, "title": "Frontend Developer", "skills": ["JavaScript", "React"]}
        ]

        user_profile = {
            "id": 102,
            "name": "Bob",
            "skills": ["Ruby", "PHP"]
        }

        # Call the service method
        jobs = self.job_service.get_jobs_for_user(user_profile)

        # Assert the results
        self.assertEqual(len(jobs), 0)

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    @patch('services.user_service.UserRepository')
    def test_get_user_profile(self, MockUserRepository):
        # Mocking the repository
        mock_repo = MockUserRepository.return_value
        mock_repo.get_user.return_value = {
            "id": 101,
            "name": "Alice",
            "skills": ["Python", "Docker", "Machine Learning"]
        }

        user_id = 101

        # Call the service method
        user_profile = self.user_service.get_user_profile(user_id)

        # Assert the results
        self.assertEqual(user_profile["id"], 101)
        self.assertEqual(user_profile["name"], "Alice")
        self.assertIn("Python", user_profile["skills"])
        self.assertIn("Docker", user_profile["skills"])
        self.assertIn("Machine Learning", user_profile["skills"])

    @patch('services.user_service.UserRepository')
    def test_get_user_profile_not_found(self, MockUserRepository):
        # Mocking the repository
        mock_repo = MockUserRepository.return_value
        mock_repo.get_user.return_value = None

        user_id = 999

        # Call the service method
        user_profile = self.user_service.get_user_profile(user_id)

        # Assert the results
        self.assertIsNone(user_profile)

if __name__ == '__main__':
    unittest.main()