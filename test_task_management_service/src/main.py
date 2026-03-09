"""
Module: main
Purpose: FastAPI application for the Test Task Management Service.
Author: Gemini
Created: 2026-03-09
Notes: Provides CRUD operations for Test Tasks.
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models, database

app = FastAPI(title="Test Task Management Service")

# Pydantic models for request and response
class TestTaskBase(BaseModel):
    name: str
    description: str | None = None

class TestTaskCreate(TestTaskBase):
    pass

class TestTaskUpdate(TestTaskBase):
    status: str | None = None
    is_active: bool | None = None

class TestTaskResponse(TestTaskBase):
    id: int
    status: str
    created_at: str # Will be formatted as ISO string
    updated_at: str # Will be formatted as ISO string
    is_active: bool

    class Config:
        from_attributes = True

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    """
    Event handler that runs when the application starts up.
    Initializes the database tables.
    """
    database.init_db()

@app.get("/", response_model=str)
def read_root():
    """
    Root endpoint for the service.
    """
    return "Test Task Management Service is running!"

@app.post("/tasks/", response_model=TestTaskResponse, status_code=status.HTTP_201_CREATED)
def create_test_task(task: TestTaskCreate, db: Session = Depends(get_db)):
    """
    Create a new test task.
    """
    db_task = models.TestTask(name=task.name, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TestTaskResponse])
def read_test_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of test tasks.
    """
    tasks = db.query(models.TestTask).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TestTaskResponse)
def read_test_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single test task by its ID.
    """
    task = db.query(models.TestTask).filter(models.TestTask.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TestTaskResponse)
def update_test_task(task_id: int, task: TestTaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing test task.
    """
    db_task = db.query(models.TestTask).filter(models.TestTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a test task by its ID.
    """
    db_task = db.query(models.TestTask).filter(models.TestTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test task not found")

    db.delete(db_task)
    db.commit()
    return
