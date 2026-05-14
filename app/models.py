"""SQLAlchemy models for the fitness platform."""

from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship

from app.database import Base


# Association table for many-to-many: workout <-> exercise
workout_exercises = Table(
    "workout_exercises",
    Base.metadata,
    Column("workout_id", Integer, ForeignKey("workouts.id"), primary_key=True),
    Column("exercise_id", Integer, ForeignKey("exercises.id"), primary_key=True),
)


class Exercise(Base):
    """Exercise model for the fitness training platform."""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)
    calories_per_hour = Column(Float, nullable=False, default=0.0)

    # Relationships
    workouts = relationship("Workout", secondary=workout_exercises, back_populates="exercises")
    progress_records = relationship("Progress", back_populates="exercise")


class Workout(Base):
    """Workout model — a session containing multiple exercises."""

    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    exercises = relationship("Exercise", secondary=workout_exercises, back_populates="workouts")


class Progress(Base):
    """Progress model — tracks user progress for each exercise."""

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    user_name = Column(String(100), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="progress_records")