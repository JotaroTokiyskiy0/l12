"""CRUD operations for Exercise model."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Exercise
from app.schemas import ExerciseCreate, ExerciseUpdate


def get_exercise(db: Session, exercise_id: int) -> Optional[Exercise]:
    """Get an exercise by ID."""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_exercises(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
) -> List[Exercise]:
    """Get a list of exercises with optional category filter."""
    query = db.query(Exercise)
    if category:
        query = query.filter(Exercise.category == category)
    return query.offset(skip).limit(limit).all()


def create_exercise(db: Session, exercise: ExerciseCreate) -> Exercise:
    """Create a new exercise."""
    db_exercise = Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def update_exercise(
    db: Session, exercise_id: int, exercise: ExerciseUpdate
) -> Optional[Exercise]:
    """Update an existing exercise."""
    db_exercise = get_exercise(db, exercise_id)
    if not db_exercise:
        return None
    update_data = exercise.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exercise, key, value)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int) -> bool:
    """Delete an exercise by ID. Returns True if deleted."""
    db_exercise = get_exercise(db, exercise_id)
    if not db_exercise:
        return False
    db.delete(db_exercise)
    db.commit()
    return True