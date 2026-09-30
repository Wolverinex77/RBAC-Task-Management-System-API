from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import TIMESTAMP, ForeignKey, Integer,String,Boolean,text
from datetime import datetime
from database import Base
# from models.team_members import Teams
class Project(Base):
    __tablename__ = "projects"  # table name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True),
    server_default=text("now()")
    )    
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    # Optional: relationship to Team (M-1)
    team = relationship("Teams", back_populates="projects")
    tasks=relationship("Task",back_populates="project")
    #1-M