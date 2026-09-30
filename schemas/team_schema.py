from datetime import datetime
from pydantic import BaseModel
class TeamBase(BaseModel):
    name:str
class TeamCreate(TeamBase):
    pass
    
class TeamResponse(TeamBase):
    id:int
    created_at:datetime
    model_config = {
        "from_attributes": True  # replaces 'orm_mode' in Pydantic v2
    }
    