import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class MatchingService:
    """
    MatchingService contains the core logic for AI-based job matching.
    Implements algorithms to match user profiles with job postings based on skills, preferences, and other criteria.
    """

    def __init__(self):
        """
        Initialize the MatchingService with any required configurations.
        """
        pass

    def calculate_similarity(self, user_vector: np.ndarray, job_vector: np.ndarray) -> float:
        """
        Calculate the similarity between a user profile vector and a job posting vector using cosine similarity.

        Args:
            user_vector (np.ndarray): The vector representation of the user's profile.
            job_vector (np.ndarray): The vector representation of the job posting.

        Returns:
            float: The similarity score between the user and the job.
        """
        similarity = cosine_similarity(user_vector.reshape(1, -1), job_vector.reshape(1, -1))
        return similarity[0][0]

    def match_jobs(self, user_profile: Dict, job_postings: List[Dict]) -> List[Dict]:
        """
        Match user profiles with job postings based on skills, preferences, and other criteria.

        Args:
            user_profile (Dict): The user's profile containing skills, preferences, and other attributes.
            job_postings (List[Dict]): A list of job postings, each containing required skills and attributes.

        Returns:
            List[Dict]: A list of job postings sorted by relevance to the user's profile.
        """
        user_vector = self._generate_user_vector(user_profile)
        job_vectors = [self._generate_job_vector(job) for job in job_postings]

        # Calculate similarity scores for each job posting
        scores = [
            {"job": job, "score": self.calculate_similarity(user_vector, job_vector)}
            for job, job_vector in zip(job_postings, job_vectors)
        ]

        # Sort jobs by similarity score in descending order
        sorted_jobs = sorted(scores, key=lambda x: x["score"], reverse=True)

        # Return sorted job postings
        return [job["job"] for job in sorted_jobs]

    def _generate_user_vector(self, user_profile: Dict) -> np.ndarray:
        """
        Generate a vector representation of the user's profile.

        Args:
            user_profile (Dict): The user's profile containing skills, preferences, and other attributes.

        Returns:
            np.ndarray: The vector representation of the user's profile.
        """
        # Example: Convert skills and preferences into a numerical vector
        skills = user_profile.get("skills", [])
        preferences = user_profile.get("preferences", [])
        vector = self._encode_features(skills + preferences)
        return vector

    def _generate_job_vector(self, job_posting: Dict) -> np.ndarray:
        """
        Generate a vector representation of a job posting.

        Args:
            job_posting (Dict): The job posting containing required skills and attributes.

        Returns:
            np.ndarray: The vector representation of the job posting.
        """
        # Example: Convert required skills and attributes into a numerical vector
        required_skills = job_posting.get("required_skills", [])
        attributes = job_posting.get("attributes", [])
        vector = self._encode_features(required_skills + attributes)
        return vector

    def _encode_features(self, features: List[str]) -> np.ndarray:
        """
        Encode a list of features into a numerical vector.

        Args:
            features (List[str]): A list of features (skills, preferences, attributes).

        Returns:
            np.ndarray: The encoded numerical vector.
        """
        # Example: Mock encoding using a simple hash-based approach
        feature_set = set(features)
        vector = np.zeros(100)  # Assume a fixed vector size of 100
        for feature in feature_set:
            index = hash(feature) % 100
            vector[index] += 1
        return vector