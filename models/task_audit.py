from sqlalchemy import Integer, String, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import datetime
from database import Base
class TaskAudit(Base):
    __tablename__='task_audit'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer,ForeignKey('task.id'),nullable=False)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('members.id'),nullable=False)
    old_state: Mapped[str] = mapped_column(String(50), nullable=False)
    new_state: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )