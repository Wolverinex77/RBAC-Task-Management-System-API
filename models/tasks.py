from __future__ import annotations
from sqlalchemy import Integer, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import datetime
from database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.project import Project  # Only for type checking, no runtime import

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False)

    # Use DB-side timestamp for UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    updated_at :Mapped[datetime | None]=mapped_column(
    TIMESTAMP,
    nullable=False,
    server_default=text('now()'),  # sets default to current time
    onupdate=text('now()')         # updates timestamp on row update
        )
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    user=relationship("User",back_populates='tasks')
    #M-1