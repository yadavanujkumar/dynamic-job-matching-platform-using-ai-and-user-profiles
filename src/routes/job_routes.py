from flask import Blueprint, request, jsonify
from src.services.job_service import JobService
from src.services.matching_service import MatchingService

job_routes = Blueprint('job_routes', __name__)

# Initialize services
job_service = JobService()
matching_service = MatchingService()

@job_routes.route('/jobs', methods=['POST'])
def create_job():
    """
    Endpoint to create a new job posting.
    Expects JSON payload with job details.
    """
    try:
        job_data = request.json
        if not job_data:
            return jsonify({"error": "Invalid input"}), 400
        
        created_job = job_service.create_job(job_data)
        return jsonify({"message": "Job created successfully", "job": created_job}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_routes.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Endpoint to update an existing job posting.
    Expects JSON payload with updated job details.
    """
    try:
        job_data = request.json
        if not job_data:
            return jsonify({"error": "Invalid input"}), 400
        
        updated_job = job_service.update_job(job_id, job_data)
        if not updated_job:
            return jsonify({"error": "Job not found"}), 404
        
        return jsonify({"message": "Job updated successfully", "job": updated_job}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_routes.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    Endpoint to delete a job posting by ID.
    """
    try:
        deleted = job_service.delete_job(job_id)
        if not deleted:
            return jsonify({"error": "Job not found"}), 404
        
        return jsonify({"message": "Job deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_routes.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Endpoint to retrieve a job posting by ID.
    """
    try:
        job = job_service.get_job(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        return jsonify({"job": job}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_routes.route('/jobs', methods=['GET'])
def get_all_jobs():
    """
    Endpoint to retrieve all job postings.
    """
    try:
        jobs = job_service.get_all_jobs()
        return jsonify({"jobs": jobs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_routes.route('/jobs/match', methods=['POST'])
def match_jobs():
    """
    Endpoint for AI-based job matching.
    Expects JSON payload with user profile data.
    """
    try:
        user_profile = request.json
        if not user_profile:
            return jsonify({"error": "Invalid input"}), 400
        
        matched_jobs = matching_service.match_jobs(user_profile)
        return jsonify({"message": "Matching successful", "matched_jobs": matched_jobs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500