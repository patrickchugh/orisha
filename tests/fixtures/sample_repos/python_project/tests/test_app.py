"""Tests for the application module."""

import pytest

from sample_project.app import User, UserService, create_app


class TestUser:
    """Tests for User entity."""

    def test_create_user(self) -> None:
        """Test user creation."""
        user = User(id=1, name="Test User", email="test@example.com")
        assert user.id == 1
        assert user.name == "Test User"
        assert user.email == "test@example.com"

    def test_user_to_dict(self) -> None:
        """Test user serialization."""
        user = User(id=1, name="Test", email="test@example.com", age=25)
        data = user.to_dict()
        assert data["id"] == 1
        assert data["name"] == "Test"
        assert data["age"] == 25


class TestUserService:
    """Tests for UserService."""

    def test_create_user(self) -> None:
        """Test creating a user through service."""
        service = UserService()
        user = service.create_user("Test", "test@example.com")
        assert user.id == 1
        assert user.name == "Test"

    def test_get_user(self) -> None:
        """Test getting a user by ID."""
        service = UserService()
        created = service.create_user("Test", "test@example.com")
        retrieved = service.get_user(created.id)
        assert retrieved == created

    def test_list_users(self) -> None:
        """Test listing all users."""
        service = UserService()
        service.create_user("User1", "user1@example.com")
        service.create_user("User2", "user2@example.com")
        users = service.list_users()
        assert len(users) == 2


class TestFlaskApp:
    """Tests for Flask application."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app()
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_health_check(self, client) -> None:
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"
