# Secure User Management API

A FastAPI application implementing secure user management with password hashing, PostgreSQL database integration, comprehensive testing, and CI/CD pipeline.

## 🚀 Features

- **Secure User Registration**: User accounts with hashed passwords using bcrypt
- **SQLAlchemy ORM**: Database models with unique constraints for username and email
- **Pydantic Validation**: Request/response validation with type safety
- **Comprehensive Testing**: Unit and integration tests with pytest
- **CI/CD Pipeline**: Automated testing and Docker image deployment via GitHub Actions
- **Docker Support**: Containerized application with Docker and Docker Compose
- **RESTful API**: FastAPI endpoints for user CRUD operations

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (or use Docker Compose)
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/jr987-NJIT/IS601_Module10_Jyothsna.git
cd IS601_Module10_Jyothsna
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## 🏃 Running the Application

### Option 1: Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Option 2: Local Development

```bash
# Start PostgreSQL (or use Docker)
docker run -d --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=userdb \
  -p 5432:5432 \
  postgres:15-alpine

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/test_security.py tests/test_schemas.py -v

# Integration tests only
pytest tests/test_integration.py -v
```

### Run Tests with Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html --cov-report=term-missing
```

View coverage report by opening `htmlcov/index.html` in your browser.

### Test Categories

- **Unit Tests**: `test_security.py`, `test_schemas.py`
  - Password hashing and verification
  - Pydantic schema validation
  - Security utilities

- **Integration Tests**: `test_integration.py`
  - User creation with database constraints
  - Email uniqueness validation
  - Username uniqueness validation
  - API endpoint functionality
  - Password security in database

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/users/` | Create new user |
| GET | `/users/` | List all users |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/username/{username}` | Get user by username |
| DELETE | `/users/{user_id}` | Delete user |

### Example Usage

**Create a User:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepassword123"
  }'
```

**Get All Users:**
```bash
curl "http://localhost:8000/users/"
```

## 🐳 Docker Hub

The Docker image is automatically built and pushed to Docker Hub via GitHub Actions.

**Docker Hub Repository**: https://hub.docker.com/r/[your-username]/secure-user-api

### Pull and Run the Image

```bash
# Pull the latest image
docker pull [your-dockerhub-username]/secure-user-api:latest

# Run the container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/userdb \
  [your-dockerhub-username]/secure-user-api:latest
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Workflow Steps

1. **Test Job**
   - Runs on every push and pull request
   - Sets up Python 3.11 environment
   - Spins up PostgreSQL test database
   - Runs unit tests
   - Runs integration tests
   - Generates coverage report

2. **Build and Push Job** (main branch only)
   - Builds Docker image
   - Pushes to Docker Hub with tags:
     - `latest`
     - Git SHA
     - Semantic version (if tagged)

3. **Security Scan Job**
   - Scans Docker image for vulnerabilities using Trivy
   - Uploads results to GitHub Security

### Setting Up CI/CD

Add the following secrets to your GitHub repository (Settings → Secrets → Actions):

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

## 🏗️ Project Structure

```
IS601_Module10_Jyothsna/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models/
│   │   ├── __init__.py      # User model
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py      # Pydantic schemas
│   │   └── user.py
│   └── utils/
│       ├── __init__.py      # Security utilities
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── test_security.py     # Unit tests for security
│   ├── test_schemas.py      # Unit tests for schemas
│   └── test_integration.py  # Integration tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow
├── .env.example             # Environment variables template
├── .gitignore
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image definition
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using bcrypt before storage
- **No Plain Text**: Passwords never stored or returned in plain text
- **Unique Constraints**: Database-level uniqueness for usernames and emails
- **Input Validation**: Pydantic schemas validate all input data
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Environment Variables**: Sensitive data stored in environment variables

## 🧩 Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation using Python type hints
- **Passlib**: Password hashing library with bcrypt
- **Pytest**: Testing framework
- **Docker**: Containerization
- **GitHub Actions**: CI/CD automation
- **Trivy**: Security vulnerability scanning

## 📝 Testing Strategy

### Unit Tests
- Test individual functions in isolation
- Mock external dependencies
- Focus on business logic and validation

### Integration Tests
- Test full request/response cycle
- Use real database (SQLite for tests)
- Verify database constraints
- Test API endpoints end-to-end

## 🎓 Learning Outcomes Addressed

- **CLO3**: Automated testing with pytest
- **CLO4**: GitHub Actions CI/CD pipeline
- **CLO9**: Docker containerization
- **CLO11**: SQL database integration with SQLAlchemy
- **CLO12**: JSON serialization with Pydantic
- **CLO13**: Secure authentication with password hashing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Jyothsna Reddy
- GitHub: [@jr987-NJIT](https://github.com/jr987-NJIT)
- Repository: [IS601_Module10_Jyothsna](https://github.com/jr987-NJIT/IS601_Module10_Jyothsna)

## 🙏 Acknowledgments

- Course: IS601 - Web Systems Development
- Institution: NJIT
- Module: 10 - Secure User Authentication

---

**Note**: Remember to update the Docker Hub repository URL and add your Docker Hub credentials to GitHub secrets before pushing to the main branch.
