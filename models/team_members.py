from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import TIMESTAMP, ForeignKey, Integer,String,Boolean,text
from datetime import datetime
from database import Base
# from models.project import Project

class TeamMembers(Base):
    __tablename__="team_members"
    user_id:Mapped[int]=mapped_column(ForeignKey("members.id"),primary_key=True)
    team_id:Mapped[int]=mapped_column(ForeignKey("teams.id"),primary_key=True)
    role:Mapped[str]=mapped_column(String,nullable=False)
    user=relationship("User",back_populates="team_members")
    team=relationship("Teams",back_populates="team_members")

class Teams(Base):
    __tablename__="teams"
    id:Mapped[int]=mapped_column(
        Integer,primary_key=True,nullable=False
    )
    name:Mapped[str]=mapped_column(
    String,nullable=False
        )
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True),
    server_default=text("now()")
    )
    team_members=relationship("TeamMembers",back_populates="team")
    projects=relationship("Project",back_populates="team")
    
    
    

    