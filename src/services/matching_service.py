import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import re


class MatchingService:
    """
    Enhanced MatchingService with advanced NLP and ML for job matching.
    Implements TF-IDF vectorization and multi-factor scoring algorithms.
    """
    
    # Scoring constants
    NEUTRAL_SCORE = 0.5  # Score when no data is available for comparison
    SKILL_WEIGHT = 0.45
    TEXT_WEIGHT = 0.30
    EXPERIENCE_WEIGHT = 0.15
    LOCATION_WEIGHT = 0.10

    def __init__(self):
        """
        Initialize the MatchingService with TF-IDF vectorizer.
        """
        self.tfidf_vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=500,
            ngram_range=(1, 2)
        )
        
        # Skill synonyms for better matching
        self.skill_synonyms = {
            'python': ['py', 'python3'],
            'javascript': ['js', 'node', 'nodejs', 'ecmascript'],
            'machine learning': ['ml', 'machinelearning', 'ai'],
            'artificial intelligence': ['ai', 'ml', 'deep learning'],
            'sql': ['mysql', 'postgresql', 'database'],
            'aws': ['amazon web services', 'cloud'],
            'docker': ['containers', 'containerization'],
            'kubernetes': ['k8s', 'container orchestration'],
        }
        
        # Setup logger
        from src.utils.logger import setup_logger
        self.logger = setup_logger(__name__)

    def calculate_similarity(self, user_vector: np.ndarray, job_vector: np.ndarray) -> float:
        """
        Calculate cosine similarity between user profile and job posting vectors.

        Args:
            user_vector: The vector representation of the user's profile
            job_vector: The vector representation of the job posting

        Returns:
            Similarity score between 0 and 1
        """
        similarity = cosine_similarity(user_vector.reshape(1, -1), job_vector.reshape(1, -1))
        return float(similarity[0][0])

    def match_jobs(self, user_profile: Dict, job_postings: List[Dict] = None) -> List[Dict]:
        """
        Match user profiles with job postings (backward compatible method).

        Args:
            user_profile: User's profile with skills, preferences, etc.
            job_postings: List of job postings (optional, for backward compatibility)

        Returns:
            List of job postings sorted by relevance
        """
        if not job_postings:
            return []
        
        matched = self.match_jobs_with_scores(user_profile, job_postings)
        return [item['job'] for item in matched]

    def match_jobs_with_scores(self, user_profile: Dict, job_postings: List[Dict]) -> List[Dict]:
        """
        Match user profile with job postings and return jobs with detailed scores.

        Args:
            user_profile: User's profile containing skills, preferences, experience, etc.
            job_postings: List of available job postings

        Returns:
            List of dictionaries containing job and matching details
        """
        if not job_postings:
            return []

        results = []
        
        for job in job_postings:
            # Calculate multiple scoring factors
            skill_score = self._calculate_skill_match(
                user_profile.get("skills", []),
                job.get("required_skills", [])
            )
            
            text_score = self._calculate_text_similarity(
                user_profile,
                job
            )
            
            experience_score = self._calculate_experience_match(
                user_profile.get("experience_years", 0),
                job.get("experience_years", 0)
            )
            
            location_score = self._calculate_location_match(
                user_profile.get("desired_location", ""),
                job.get("location", "")
            )
            
            # Weighted overall score (skill matching is most important)
            overall_score = (
                skill_score * self.SKILL_WEIGHT +
                text_score * self.TEXT_WEIGHT +
                experience_score * self.EXPERIENCE_WEIGHT +
                location_score * self.LOCATION_WEIGHT
            )
            
            results.append({
                "job": job,
                "overall_score": round(overall_score, 3),
                "skill_match": round(skill_score, 3),
                "text_similarity": round(text_score, 3),
                "experience_match": round(experience_score, 3),
                "location_match": round(location_score, 3),
                "match_explanation": self._generate_match_explanation(
                    skill_score, text_score, experience_score, location_score
                )
            })

        # Sort by overall score in descending order
        results.sort(key=lambda x: x["overall_score"], reverse=True)
        return results

    def _calculate_skill_match(self, user_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculate skill matching score with synonym support.

        Args:
            user_skills: List of user's skills
            job_skills: List of required job skills

        Returns:
            Score between 0 and 1
        """
        if not job_skills:
            return self.NEUTRAL_SCORE  # Neutral score if no skills specified
        
        if not user_skills:
            return 0.0
        
        # Normalize skills to lowercase
        user_skills_normalized = [self._normalize_skill(s) for s in user_skills]
        job_skills_normalized = [self._normalize_skill(s) for s in job_skills]
        
        # Count matches considering synonyms
        matches = 0
        for job_skill in job_skills_normalized:
            if self._skill_matches(job_skill, user_skills_normalized):
                matches += 1
        
        # Calculate score based on coverage of required skills
        score = matches / len(job_skills_normalized) if job_skills_normalized else 0
        
        # Bonus for having more skills than required (up to 1.0)
        if score > 0:
            bonus = min(len(user_skills_normalized) / len(job_skills_normalized), 1.0) * 0.1
            score = min(score + bonus, 1.0)
        
        return score

    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name to lowercase and remove extra spaces."""
        return re.sub(r'\s+', ' ', skill.lower().strip())

    def _skill_matches(self, job_skill: str, user_skills: List[str]) -> bool:
        """
        Check if a job skill matches any user skill, considering synonyms.
        """
        # Direct match
        if job_skill in user_skills:
            return True
        
        # Check synonyms
        for skill, synonyms in self.skill_synonyms.items():
            if job_skill == skill or job_skill in synonyms:
                # Job skill is in our synonym map, check if user has any synonym
                if skill in user_skills or any(syn in user_skills for syn in synonyms):
                    return True
            
            # Check if user skill is in synonym map
            if any(user_skill == skill or user_skill in synonyms for user_skill in user_skills):
                if job_skill == skill or job_skill in synonyms:
                    return True
        
        return False

    def _calculate_text_similarity(self, user_profile: Dict, job: Dict) -> float:
        """
        Calculate text similarity using TF-IDF vectorization.

        Args:
            user_profile: User profile dictionary
            job: Job posting dictionary

        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Create text representations
            user_text = self._create_text_representation(user_profile)
            job_text = self._create_text_representation(job)
            
            if not user_text or not job_text:
                return 0.0
            
            # Vectorize texts
            vectors = self.tfidf_vectorizer.fit_transform([user_text, job_text])
            
            # Calculate similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            # Log the exception and fallback to simple keyword matching
            self.logger.warning(f"TF-IDF vectorization failed: {e}. Using fallback keyword matching.")
            return self._simple_keyword_match(user_profile, job)

    def _create_text_representation(self, data: Dict) -> str:
        """
        Create a text representation from dictionary data.
        """
        text_parts = []
        
        # Add skills
        if 'skills' in data and isinstance(data['skills'], list):
            text_parts.extend(data['skills'])
        
        # Add description
        if 'description' in data:
            text_parts.append(str(data['description']))
        
        if 'bio' in data:
            text_parts.append(str(data['bio']))
        
        # Add title
        if 'title' in data:
            text_parts.append(str(data['title']))
        
        # Add preferences text
        if 'preferences' in data and isinstance(data['preferences'], dict):
            for key, value in data['preferences'].items():
                if isinstance(value, (str, int, float)):
                    text_parts.append(f"{key} {value}")
        
        return ' '.join(text_parts)

    def _simple_keyword_match(self, user_profile: Dict, job: Dict) -> float:
        """
        Fallback method for text matching using simple keyword overlap.
        """
        user_words = set(self._create_text_representation(user_profile).lower().split())
        job_words = set(self._create_text_representation(job).lower().split())
        
        if not user_words or not job_words:
            return 0.0
        
        common = user_words.intersection(job_words)
        return len(common) / max(len(user_words), len(job_words))

    def _calculate_experience_match(self, user_exp: int, job_exp: int) -> float:
        """
        Calculate experience matching score.

        Args:
            user_exp: User's years of experience
            job_exp: Job's required years of experience

        Returns:
            Score between 0 and 1
        """
        if job_exp == 0:
            return 1.0  # No specific requirement
        
        if user_exp >= job_exp:
            # Has required experience or more
            return 1.0
        else:
            # Partial credit based on how close they are
            return max(user_exp / job_exp, 0.0)

    def _calculate_location_match(self, user_location: str, job_location: str) -> float:
        """
        Calculate location matching score.

        Args:
            user_location: User's desired location
            job_location: Job's location

        Returns:
            Score between 0 and 1
        """
        if not user_location:
            return self.NEUTRAL_SCORE  # Neutral if user has no preference
        
        if not job_location:
            return self.NEUTRAL_SCORE
        
        user_loc_lower = user_location.lower().strip()
        job_loc_lower = job_location.lower().strip()
        
        # Exact match
        if user_loc_lower == job_loc_lower:
            return 1.0
        
        # Partial match (city/state contained in the other)
        if user_loc_lower in job_loc_lower or job_loc_lower in user_loc_lower:
            return 0.8
        
        # Check for "remote" keyword
        if 'remote' in user_loc_lower or 'remote' in job_loc_lower:
            if 'remote' in user_loc_lower and 'remote' in job_loc_lower:
                return 1.0
            else:
                return 0.3
        
        return 0.0

    def _generate_match_explanation(
        self,
        skill_score: float,
        text_score: float,
        experience_score: float,
        location_score: float
    ) -> str:
        """
        Generate a human-readable explanation of the match.
        """
        explanations = []
        
        if skill_score >= 0.8:
            explanations.append("Excellent skill match")
        elif skill_score >= 0.6:
            explanations.append("Good skill match")
        elif skill_score >= 0.4:
            explanations.append("Moderate skill match")
        else:
            explanations.append("Limited skill match")
        
        if experience_score >= 0.8:
            explanations.append("meets experience requirements")
        elif experience_score >= 0.5:
            explanations.append("close to experience requirements")
        
        if location_score >= 0.8:
            explanations.append("great location fit")
        elif location_score >= 0.5:
            explanations.append("acceptable location")
        
        return ", ".join(explanations) if explanations else "Basic match"

    def _generate_user_vector(self, user_profile: Dict) -> np.ndarray:
        """
        Generate a vector representation of the user's profile (legacy method).
        """
        skills = user_profile.get("skills", [])
        preferences = user_profile.get("preferences", {})
        
        # Create text for vectorization
        text = ' '.join(skills)
        if isinstance(preferences, dict):
            text += ' ' + ' '.join(str(v) for v in preferences.values() if v)
        
        return self._encode_features(skills)

    def _generate_job_vector(self, job_posting: Dict) -> np.ndarray:
        """
        Generate a vector representation of a job posting (legacy method).
        """
        required_skills = job_posting.get("required_skills", [])
        return self._encode_features(required_skills)

    def _encode_features(self, features: List[str]) -> np.ndarray:
        """
        Encode features into a numerical vector (legacy method for backward compatibility).
        """
        feature_set = set(self._normalize_skill(f) for f in features)
        vector = np.zeros(100)
        for feature in feature_set:
            index = hash(feature) % 100
            vector[index] += 1
        return vector