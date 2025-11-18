"""Integration tests for database operations and API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create and drop database tables for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestRootEndpoints:
    """Test suite for root and health endpoints."""
    
    def test_read_root(self):
        """Test root endpoint returns correct message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestUserCreation:
    """Test suite for user creation endpoint."""
    
    def test_create_user_success(self):
        """Test successful user creation."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data
        assert "password_hash" not in data
        assert "id" in data
        assert "created_at" in data
    
    def test_create_user_duplicate_username(self):
        """Test that duplicate username is rejected."""
        user_data = {
            "username": "testuser",
            "email": "test1@example.com",
            "password": "securepass123"
        }
        # Create first user
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        
        # Try to create user with same username
        user_data2 = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "securepass123"
        }
        response2 = client.post("/users/", json=user_data2)
        assert response2.status_code == 400
        assert "Username already registered" in response2.json()["detail"]
    
    def test_create_user_duplicate_email(self):
        """Test that duplicate email is rejected."""
        user_data = {
            "username": "testuser1",
            "email": "test@example.com",
            "password": "securepass123"
        }
        # Create first user
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        
        # Try to create user with same email
        user_data2 = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "securepass123"
        }
        response2 = client.post("/users/", json=user_data2)
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]
    
    def test_create_user_invalid_email(self):
        """Test that invalid email format is rejected."""
        user_data = {
            "username": "testuser",
            "email": "notanemail",
            "password": "securepass123"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_user_short_password(self):
        """Test that short password is rejected."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "short"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_user_short_username(self):
        """Test that short username is rejected."""
        user_data = {
            "username": "ab",
            "email": "test@example.com",
            "password": "securepass123"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validation error


class TestUserRetrieval:
    """Test suite for user retrieval endpoints."""
    
    def test_get_users_empty(self):
        """Test getting users when database is empty."""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_users_with_data(self):
        """Test getting users when database has users."""
        # Create test users
        user1 = {"username": "user1", "email": "user1@example.com", "password": "pass123456"}
        user2 = {"username": "user2", "email": "user2@example.com", "password": "pass123456"}
        client.post("/users/", json=user1)
        client.post("/users/", json=user2)
        
        response = client.get("/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2
        assert users[0]["username"] == "user1"
        assert users[1]["username"] == "user2"
    
    def test_get_user_by_id(self):
        """Test getting a specific user by ID."""
        # Create a user
        user_data = {"username": "testuser", "email": "test@example.com", "password": "pass123456"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Retrieve user by ID
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"
    
    def test_get_user_by_id_not_found(self):
        """Test getting a non-existent user by ID."""
        response = client.get("/users/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_user_by_username(self):
        """Test getting a user by username."""
        # Create a user
        user_data = {"username": "testuser", "email": "test@example.com", "password": "pass123456"}
        client.post("/users/", json=user_data)
        
        # Retrieve user by username
        response = client.get("/users/username/testuser")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
    
    def test_get_user_by_username_not_found(self):
        """Test getting a non-existent user by username."""
        response = client.get("/users/username/nonexistent")
        assert response.status_code == 404


class TestUserDeletion:
    """Test suite for user deletion endpoint."""
    
    def test_delete_user_success(self):
        """Test successful user deletion."""
        # Create a user
        user_data = {"username": "testuser", "email": "test@example.com", "password": "pass123456"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        response = client.delete("/users/9999")
        assert response.status_code == 404


class TestPasswordSecurity:
    """Test suite for password security in database."""
    
    def test_password_is_hashed(self):
        """Test that passwords are hashed in the database."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "plainpassword123"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        # Check database directly
        db = TestingSessionLocal()
        user = db.query(User).filter(User.username == "testuser").first()
        assert user is not None
        assert user.password_hash != "plainpassword123"
        assert user.password_hash.startswith("$2b$")  # Bcrypt hash format
        db.close()
    
    def test_password_not_returned_in_response(self):
        """Test that password is never returned in API responses."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "plainpassword123"
        }
        response = client.post("/users/", json=user_data)
        data = response.json()
        
        assert "password" not in data
        assert "password_hash" not in data
