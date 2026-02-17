# Dynamic Job Matching Platform Using AI and User Profiles

An AI-powered platform that intelligently matches job opportunities with user profiles using advanced machine learning algorithms and natural language processing.

## 🚀 Features

- **AI-Powered Matching**: Leverages machine learning models (TensorFlow, PyTorch, scikit-learn) to match jobs with user profiles
- **Natural Language Processing**: Uses advanced NLP libraries (Transformers, NLTK, spaCy) for analyzing job descriptions and user skills
- **RESTful API**: Built with FastAPI for high-performance, async operations
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **Web Scraping**: Automated job data collection using BeautifulSoup and requests
- **Docker Support**: Containerized application for easy deployment
- **Comprehensive Testing**: Full test suite with pytest
- **Code Quality**: Pre-commit hooks, Black, isort, and Flake8 for code formatting and linting

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
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
   python src/main.py
   ```

   The API will be available at `http://localhost:8000`

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
│   ├── models/          # AI/ML models
│   ├── routes/          # API route handlers
│   │   ├── job_routes.py
│   │   └── user_routes.py
│   ├── services/        # Business logic services
│   └── main.py          # Application entry point
├── tests/               # Test suite
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
- `GET /jobs` - List all jobs
- `POST /jobs` - Create a new job posting
- `GET /jobs/{id}` - Get job details
- `PUT /jobs/{id}` - Update job information
- `DELETE /jobs/{id}` - Delete a job

### Users
- `GET /users` - List all users
- `POST /users` - Create a new user profile
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user profile
- `DELETE /users/{id}` - Delete a user

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

The platform uses multiple ML approaches:

- **TensorFlow/Keras**: Deep learning models for complex pattern recognition
- **PyTorch**: Neural networks for profile and job embeddings
- **scikit-learn**: Traditional ML algorithms for classification and clustering
- **Transformers**: Pre-trained language models for text understanding
- **NLTK & spaCy**: Text preprocessing and feature extraction

## 📊 Tech Stack

**Backend Framework:**
- FastAPI (async Python web framework)
- Uvicorn (ASGI server)

**Machine Learning:**
- TensorFlow 2.13.0
- PyTorch 2.0.1
- scikit-learn 1.3.0
- Transformers 4.31.0
- NLTK 3.8.1
- spaCy 3.6.0

**Database:**
- PostgreSQL
- SQLAlchemy 2.0.20
- psycopg2-binary 2.9.7

**Data Processing:**
- NumPy 1.25.2
- Pandas 2.0.3

**Web Scraping:**
- BeautifulSoup4 4.12.2
- Requests 2.31.0
- lxml 4.9.3

**Development Tools:**
- pytest (testing)
- Black (code formatting)
- isort (import sorting)
- Flake8 (linting)
- pre-commit (git hooks)

## 🔒 Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/jobmatching
SECRET_KEY=your-secret-key
DEBUG=True
PORT=8000
```

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
