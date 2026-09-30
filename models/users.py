from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import TIMESTAMP, ForeignKey, Integer,String,Boolean,text
from datetime import datetime
from database import Base


class User(Base):
    __tablename__="members"
    id:Mapped[int]=mapped_column(
        Integer,primary_key=True,nullable=False
    )
    email:Mapped[str]=mapped_column(String,nullable=False,index=True,unique=True)
    hashed_password:Mapped[str]=mapped_column(String,nullable=False)
    role:Mapped[str]=mapped_column(String,index=True,default="member")
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True),
    server_default=text("now()"))
    team_members=relationship("TeamMembers",back_populates="user")
        #“User is linked to many rows in the TeamMember table”
    tasks=relationship("Task",back_populates='user')
