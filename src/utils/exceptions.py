"""
Custom exceptions for the Dynamic Job Matching Platform
"""


class BaseJobMatchingException(Exception):
    """Base exception class for all custom exceptions"""
    pass


class JobNotFoundException(BaseJobMatchingException):
    """Raised when a job is not found in the database"""
    pass


class UserNotFoundException(BaseJobMatchingException):
    """Raised when a user is not found in the database"""
    pass


class InvalidJobDataException(BaseJobMatchingException):
    """Raised when job data is invalid or incomplete"""
    pass


class InvalidUserDataException(BaseJobMatchingException):
    """Raised when user data is invalid or incomplete"""
    pass


class MatchingServiceException(BaseJobMatchingException):
    """Raised when there's an error in the matching service"""
    pass


class DatabaseException(BaseJobMatchingException):
    """Raised when there's a database-related error"""
    pass
