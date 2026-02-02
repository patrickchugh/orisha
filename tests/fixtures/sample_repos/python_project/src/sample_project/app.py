"""Main application module."""

from dataclasses import dataclass
from typing import Any

from flask import Flask, jsonify, request
from pydantic import BaseModel


class UserRequest(BaseModel):
    """User creation request model."""

    name: str
    email: str
    age: int | None = None


@dataclass
class User:
    """User entity."""

    id: int
    name: str
    email: str
    age: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
        }


class UserService:
    """Service for managing users."""

    def __init__(self) -> None:
        """Initialize user service."""
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, name: str, email: str, age: int | None = None) -> User:
        """Create a new user."""
        user = User(
            id=self._next_id,
            name=name,
            email=email,
            age=age,
        )
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> User | None:
        """Get a user by ID."""
        return self._users.get(user_id)

    def list_users(self) -> list[User]:
        """List all users."""
        return list(self._users.values())


def create_app() -> Flask:
    """Create Flask application."""
    app = Flask(__name__)
    service = UserService()

    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy"})

    @app.route("/users", methods=["GET"])
    def list_users():
        """List all users."""
        users = service.list_users()
        return jsonify([u.to_dict() for u in users])

    @app.route("/users", methods=["POST"])
    def create_user():
        """Create a new user."""
        data = UserRequest.model_validate(request.json)
        user = service.create_user(
            name=data.name,
            email=data.email,
            age=data.age,
        )
        return jsonify(user.to_dict()), 201

    @app.route("/users/<int:user_id>")
    def get_user(user_id: int):
        """Get a user by ID."""
        user = service.get_user(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
