"""
Module: models
Purpose: Defines SQLAlchemy ORM models for the Test Task Management Service.
Author: Gemini
Created: 2026-03-09
Notes: This module contains the database models for Test Tasks.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TestTask(Base):
    """
    Represents a single test task in the system.

    Attributes:
        id (int): Primary key, unique identifier for the test task.
        name (str): The name of the test task.
        description (str): A detailed description of the test task.
        status (str): The current status of the test task (e.g., "pending", "running", "completed", "failed").
        created_at (datetime): Timestamp when the test task was created.
        updated_at (datetime): Timestamp when the test task was last updated.
        is_active (bool): Flag indicating if the test task is active.
    """
    __tablename__ = "test_tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<TestTask(id={self.id}, name='{self.name}', status='{self.status}')>"
