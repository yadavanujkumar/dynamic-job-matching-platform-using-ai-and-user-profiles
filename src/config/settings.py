import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Application Settings
APP_NAME = "Dynamic Job Matching Platform"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database Configuration
DATABASE = {
    "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
    "NAME": os.getenv("DB_NAME", "job_matching_db"),
    "USER": os.getenv("DB_USER", "postgres"),
    "PASSWORD": os.getenv("DB_PASSWORD", "password"),
    "HOST": os.getenv("DB_HOST", "localhost"),
    "PORT": os.getenv("DB_PORT", "5432"),
}

# AI Model Settings
AI_MODEL_PATH = os.getenv("AI_MODEL_PATH", "/models/job_matching_model.pkl")
AI_MODEL_TIMEOUT = int(os.getenv("AI_MODEL_TIMEOUT", "30"))  # Timeout in seconds

# API Keys
THIRD_PARTY_API_KEYS = {
    "linkedin": os.getenv("LINKEDIN_API_KEY", ""),
    "indeed": os.getenv("INDEED_API_KEY", ""),
    "glassdoor": os.getenv("GLASSDOOR_API_KEY", ""),
}

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Static and Media Files
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.getenv("STATIC_ROOT", "/var/www/static/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/var/www/media/")

# Pagination Settings
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))

# Email Configuration
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("true", "1")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "your-email@example.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "your-email-password")

# Feature Flags
FEATURE_FLAGS = {
    "enable_ai_matching": os.getenv("ENABLE_AI_MATCHING", "True").lower() in ("true", "1"),
    "enable_user_profiles": os.getenv("ENABLE_USER_PROFILES", "True").lower() in ("true", "1"),
}

# Docker Settings
DOCKER_ENABLED = os.getenv("DOCKER_ENABLED", "False").lower() in ("true", "1")

# Security Settings
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() in ("true", "1")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1")
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() in ("true", "1")

# Miscellaneous
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "en,es,fr").split(",")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")