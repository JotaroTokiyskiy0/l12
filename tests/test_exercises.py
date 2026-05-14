"""Tests for the Exercise CRUD API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# In-memory SQLite database for tests
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def create_sample_exercise() -> dict:
    """Helper to create a sample exercise via API."""
    response = client.post(
        "/exercises",
        json={
            "name": "Жим лёжа",
            "description": "Базовое силовое упражнение",
            "category": "силовая",
            "difficulty": "средний",
            "calories_per_hour": 300.0,
        },
    )
    return response.json()


class TestCreateExercise:
    """Tests for POST /exercises."""

    def test_create_exercise_success(self):
        """Test creating a valid exercise returns 201."""
        response = client.post(
            "/exercises",
            json={
                "name": "Бег на месте",
                "description": "Кардио упражнение",
                "category": "кардио",
                "difficulty": "лёгкий",
                "calories_per_hour": 500.0,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Бег на месте"
        assert data["category"] == "кардио"
        assert data["difficulty"] == "лёгкий"
        assert data["calories_per_hour"] == 500.0
        assert "id" in data

    def test_create_exercise_invalid_difficulty(self):
        """Test creating with invalid difficulty returns 422."""
        response = client.post(
            "/exercises",
            json={
                "name": "Тест",
                "category": "силовая",
                "difficulty": "неверный",
                "calories_per_hour": 100.0,
            },
        )
        assert response.status_code == 422

    def test_create_exercise_negative_calories(self):
        """Test creating with negative calories returns 422."""
        response = client.post(
            "/exercises",
            json={
                "name": "Тест",
                "category": "силовая",
                "difficulty": "лёгкий",
                "calories_per_hour": -10.0,
            },
        )
        assert response.status_code == 422

    def test_create_exercise_empty_name(self):
        """Test creating with empty name returns 422."""
        response = client.post(
            "/exercises",
            json={
                "name": "",
                "category": "силовая",
                "difficulty": "лёгкий",
                "calories_per_hour": 100.0,
            },
        )
        assert response.status_code == 422


class TestReadExercises:
    """Tests for GET /exercises."""

    def test_read_exercises_empty(self):
        """Test getting exercises when database is empty."""
        response = client.get("/exercises")
        assert response.status_code == 200
        assert response.json() == []

    def test_read_exercises_with_data(self):
        """Test getting exercises with existing data."""
        create_sample_exercise()
        response = client.get("/exercises")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Жим лёжа"

    def test_read_exercises_filter_by_category(self):
        """Test filtering exercises by category."""
        create_sample_exercise()
        client.post(
            "/exercises",
            json={
                "name": "Плавание",
                "category": "кардио",
                "difficulty": "средний",
                "calories_per_hour": 400.0,
            },
        )
        response = client.get("/exercises?category=силовая")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["category"] == "силовая"

    def test_read_exercises_pagination(self):
        """Test pagination of exercises."""
        for i in range(5):
            client.post(
                "/exercises",
                json={
                    "name": f"Упражнение {i}",
                    "category": "силовая",
                    "difficulty": "средний",
                    "calories_per_hour": 200.0,
                },
            )
        response = client.get("/exercises?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestReadExercise:
    """Tests for GET /exercises/{id}."""

    def test_read_exercise_by_id(self):
        """Test getting an exercise by ID."""
        created = create_sample_exercise()
        response = client.get(f"/exercises/{created['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "Жим лёжа"

    def test_read_exercise_not_found(self):
        """Test getting a non-existent exercise returns 404."""
        response = client.get("/exercises/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUpdateExercise:
    """Tests for PUT /exercises/{id}."""

    def test_update_exercise_success(self):
        """Test updating an exercise successfully."""
        created = create_sample_exercise()
        response = client.put(
            f"/exercises/{created['id']}",
            json={
                "name": "Жим лёжа обновлённый",
                "calories_per_hour": 350.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Жим лёжа обновлённый"
        assert data["calories_per_hour"] == 350.0

    def test_update_exercise_not_found(self):
        """Test updating a non-existent exercise returns 404."""
        response = client.put(
            "/exercises/9999",
            json={"name": "Не существует"},
        )
        assert response.status_code == 404

    def test_update_exercise_invalid_data(self):
        """Test updating with invalid data returns 422."""
        created = create_sample_exercise()
        response = client.put(
            f"/exercises/{created['id']}",
            json={"calories_per_hour": -50.0},
        )
        assert response.status_code == 422


class TestDeleteExercise:
    """Tests for DELETE /exercises/{id}."""

    def test_delete_exercise_success(self):
        """Test deleting an exercise successfully."""
        created = create_sample_exercise()
        response = client.delete(f"/exercises/{created['id']}")
        assert response.status_code == 204
        # Verify it's deleted
        get_response = client.get(f"/exercises/{created['id']}")
        assert get_response.status_code == 404

    def test_delete_exercise_not_found(self):
        """Test deleting a non-existent exercise returns 404."""
        response = client.delete("/exercises/9999")
        assert response.status_code == 404