from datetime import datetime
from pydantic import BaseModel
class ProjectBase(BaseModel):
    name:str
class ProjectCreate(ProjectBase):
    pass
class ProjectResponse(ProjectBase):
    id:int
    name:str
    team_id:int
    created_at:datetime
    is_archived:bool
    model_config = {
        "from_attributes": True  # replaces 'orm_mode' in Pydantic v2
    }