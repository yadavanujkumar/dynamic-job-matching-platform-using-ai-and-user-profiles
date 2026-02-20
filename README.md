# Dynamic Job Matching Platform Using AI and User Profiles

An AI-powered platform that intelligently matches job opportunities with user profiles using advanced machine learning algorithms and natural language processing.

## ✨ Recent Enhancements

This platform has been significantly enhanced from its basic version with the following improvements:

### 🎯 Advanced AI Matching
- **Sophisticated Scoring Algorithm**: Multi-factor weighted scoring (skills 45%, text 30%, experience 15%, location 10%)
- **TF-IDF Vectorization**: Semantic text analysis for better job-profile matching
- **Skill Synonym Detection**: Smart matching that recognizes related skills (e.g., "Python" ↔ "Python3")
- **Match Explanations**: Human-readable explanations for each job match
- **Confidence Metrics**: Detailed breakdown of matching scores

### 🛠️ Technical Improvements
- **Full FastAPI Implementation**: Complete migration from Flask to FastAPI with async support
- **Pydantic Validation**: Strong input validation and type checking
- **JWT Authentication**: Secure user authentication with token-based auth
- **Modular Architecture**: Proper Python package structure with `__init__.py` files
- **Error Handling**: Comprehensive exception handling and logging
- **SQLite Fallback**: Automatic fallback to SQLite if PostgreSQL unavailable

### 📊 Enhanced API Features
- **Smart Job Filtering**: Filter jobs by location, skills, and other criteria
- **Detailed Match Results**: Jobs returned with confidence scores and explanations
- **User Profile Management**: Complete user registration, login, and profile updates
- **Better Documentation**: Extensive API examples and Swagger UI

## 🚀 Features

- **AI-Powered Matching**: Advanced multi-factor algorithm for intelligent job-candidate matching
- **Natural Language Processing**: TF-IDF vectorization and semantic analysis
- **RESTful API**: Built with FastAPI for high-performance, async operations
- **Database Integration**: Flexible database support (PostgreSQL/SQLite) with SQLAlchemy ORM
- **JWT Authentication**: Secure token-based user authentication
- **Docker Support**: Containerized application for easy deployment
- **Comprehensive Testing**: Full test suite with pytest
- **Code Quality**: Pre-commit hooks, Black, isort, and Flake8 for code formatting and linting

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite is used as fallback)
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/dynamic-job-matching-platform-using-ai-and-user-profiles.git
   cd dynamic-job-matching-platform-using-ai-and-user-profiles
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the `.env` file and update it with your configuration:
   - Database credentials
   - API keys
   - Other environment-specific settings

5. **Run the application**
   ```bash
   # Set PYTHONPATH to current directory
   export PYTHONPATH=$(pwd)
   python src/main.py
   ```

   The API will be available at `http://localhost:8000`
   
   Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`

### Quick Start

For a quick start without manual setup:

```bash
# Make the start script executable and run it
chmod +x start.sh
./start.sh
```

This script will:
- Check Python and pip installation
- Create a virtual environment
- Install all dependencies
- Start the server on http://localhost:8000

### Run Demo

Once the server is running, open a new terminal and run the demo script:

```bash
python demo.py
```

This interactive demo will showcase:
- Creating job postings
- Filtering jobs by skills
- User registration and authentication
- Profile management
- AI-powered job matching with detailed scores

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**
   ```bash
   docker build -t job-matching-platform .
   docker run -p 8000:8000 job-matching-platform
   ```

## 📁 Project Structure

```
dynamic-job-matching-platform-using-ai-and-user-profiles/
├── src/
│   ├── config/          # Configuration files
│   ├── database/        # Database models and connection
│   ├── models/          # Data models
│   ├── routes/          # API route handlers
│   │   ├── job_routes.py
│   │   └── user_routes.py
│   ├── services/        # Business logic services
│   │   └── matching_service.py  # AI matching algorithm
│   ├── utils/           # Utility modules (logging, exceptions)
│   └── main.py          # Application entry point
├── tests/               # Test suite
├── demo.py              # Interactive demo script
├── start.sh             # Quick start script
├── .env                 # Environment variables
├── .gitignore          # Git ignore rules
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker image definition
└── requirements.txt    # Python dependencies
```

## 🔧 API Endpoints

### Root
- `GET /` - Welcome message and API information

### Jobs
- `GET /jobs/` - List all jobs (with optional filters: `location`, `skill`, `limit`)
- `POST /jobs/` - Create a new job posting
- `GET /jobs/{id}` - Get job details by ID
- `PUT /jobs/{id}` - Update job information
- `DELETE /jobs/{id}` - Delete a job
- `POST /jobs/match` - **AI-powered job matching** - matches jobs to user profile with detailed scores

### Users
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and receive JWT token
- `GET /users/profile` - Get current user profile (requires authentication)
- `PUT /users/profile` - Update current user profile (requires authentication)

### Example API Calls

**Create a Job:**
```bash
curl -X POST http://localhost:8000/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "Looking for an experienced Python developer",
    "required_skills": ["Python", "Machine Learning", "Docker"],
    "location": "San Francisco, CA",
    "company": "TechCorp",
    "salary_min": 120000,
    "salary_max": 180000,
    "experience_years": 5
  }'
```

**Match Jobs to User Profile:**
```bash
curl -X POST http://localhost:8000/jobs/match \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Machine Learning", "Docker"],
    "experience_years": 4,
    "desired_location": "San Francisco"
  }'
```

**Register User:**
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secure123",
    "skills": ["Python", "ML"]
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secure123"}'
```

For detailed API documentation, visit `http://localhost:8000/docs` (FastAPI auto-generated Swagger UI)

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_specific.py
```

## 🤖 Machine Learning Models

The platform now uses **advanced AI/ML algorithms** for intelligent job matching:

### Matching Algorithm Features:
- **TF-IDF Vectorization**: Converts job descriptions and user profiles into meaningful text vectors
- **Skill Synonym Detection**: Recognizes related skills (e.g., "JavaScript" matches "JS", "Node.js")
- **Multi-Factor Scoring**: Weighted algorithm combining:
  - **Skill Match (45%)**: Measures coverage of required skills
  - **Text Similarity (30%)**: Semantic similarity using TF-IDF cosine similarity
  - **Experience Match (15%)**: Compares years of experience
  - **Location Match (10%)**: Geographic compatibility with remote work support
- **Match Explanations**: Human-readable explanations for each match
- **Confidence Scores**: Detailed breakdown of each matching factor

### Technology Stack:
- **scikit-learn**: TF-IDF vectorization, cosine similarity
- **NumPy**: Vector operations and numerical computations
- **Natural Language Processing**: Text preprocessing and feature extraction

### Example Matching Result:
```json
{
  "job": {
    "title": "Senior Python Developer",
    "required_skills": ["Python", "Machine Learning", "Docker", "AWS"],
    "location": "San Francisco, CA"
  },
  "overall_score": 0.597,
  "skill_match": 0.825,
  "text_similarity": 0.087,
  "experience_match": 0.8,
  "location_match": 0.8,
  "match_explanation": "Excellent skill match, meets experience requirements, great location fit"
}
```

The matching algorithm intelligently ranks jobs based on multiple factors, providing transparency into why each job was recommended.

## 📊 Tech Stack

**Backend Framework:**
- FastAPI (async Python web framework with automatic API documentation)
- Uvicorn (ASGI server for high-performance async operations)
- Pydantic (data validation and settings management)

**Machine Learning:**
- scikit-learn (TF-IDF vectorization, cosine similarity)
- NumPy (numerical computations and vector operations)

**Database:**
- SQLAlchemy 2.0+ (ORM with async support)
- SQLite (default, with PostgreSQL support)

**Security:**
- PyJWT (JSON Web Token authentication)
- Werkzeug (secure password hashing with PBKDF2)

**Development Tools:**
- pytest (testing framework)
- httpx (async HTTP client for testing)

## 🔒 Environment Variables

Configure the application by setting these environment variables (optional, defaults provided):

```env
# Database Configuration
DATABASE_URL=sqlite:///./dynamic_job_matching.db  # Default: SQLite
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname  # For PostgreSQL
DB_ECHO=false  # Set to 'true' to enable SQL query logging

# Security (REQUIRED for production)
SECRET_KEY=your-super-secret-key-min-32-chars-long  # For JWT token signing

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**⚠️ Security Warning:** Always set a strong `SECRET_KEY` in production. The application will warn you if using the default development key.

## 🚧 Development

### Code Formatting

The project uses automated code formatting:

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with Flake8
flake8 src/ tests/
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Yadav Anuj Kumar**
- GitHub: [@yadavanujkumar](https://github.com/yadavanujkumar)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yadavanujkumar/dynamic-job-matching-platform-using-ai-and-user-profiles/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
