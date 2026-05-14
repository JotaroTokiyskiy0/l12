"""FastAPI application for the fitness training platform."""

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.schemas import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app import crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Training Platform API",
    description="API для управления упражнениями на платформе спортивных тренировок",
    version="1.0.0",
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """Redirect to the static index page."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


@app.get("/exercises", response_model=List[ExerciseResponse])
def read_exercises(
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """Get a list of all exercises with optional category filter."""
    exercises = crud.get_exercises(db, skip=skip, limit=limit, category=category)
    return exercises


@app.post(
    "/exercises",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
):
    """Create a new exercise."""
    return crud.create_exercise(db=db, exercise=exercise)


@app.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
def read_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
):
    """Get details of a specific exercise by ID."""
    db_exercise = crud.get_exercise(db, exercise_id=exercise_id)
    if db_exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found",
        )
    return db_exercise


@app.put("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise: ExerciseUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing exercise."""
    db_exercise = crud.update_exercise(db, exercise_id=exercise_id, exercise=exercise)
    if db_exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found",
        )
    return db_exercise


@app.delete("/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
):
    """Delete an exercise by ID."""
    deleted = crud.delete_exercise(db, exercise_id=exercise_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found",
        )
    return None