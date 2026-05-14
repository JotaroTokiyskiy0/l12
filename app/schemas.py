"""Pydantic schemas for request/response validation."""

from typing import Optional

from pydantic import BaseModel, Field


class ExerciseBase(BaseModel):
    """Base schema with common exercise fields."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    difficulty: str = Field(..., pattern=r"^(лёгкий|средний|сложный)$")
    calories_per_hour: float = Field(..., ge=0.0)


class ExerciseCreate(ExerciseBase):
    """Schema for creating an exercise."""
    pass


class ExerciseUpdate(BaseModel):
    """Schema for updating an exercise. All fields optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    difficulty: Optional[str] = Field(
        None, pattern=r"^(лёгкий|средний|сложный)$"
    )
    calories_per_hour: Optional[float] = Field(None, ge=0.0)


class ExerciseResponse(ExerciseBase):
    """Schema for returning an exercise."""

    id: int

    model_config = {"from_attributes": True}
