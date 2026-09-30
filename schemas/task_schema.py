from pydantic import BaseModel, Field
from typing import Optional,Literal
from datetime import datetime
class TaskBase(BaseModel):
    project_id: int
    assigned_to: int
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
class TaskCreate(TaskBase):
    pass
class TaskUpdate(BaseModel):
    state: Literal['in-progress', 'done']

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    state: str = Field(..., max_length=50)
    model_config = {
        "from_attributes": True
    }
class TaskAuditSchema(BaseModel):
    id: int
    task_id: int
    user_id: int
    old_state: str
    new_state: str
    timestamp: datetime

    model_config = {
        "from_attributes": True  # replaces 'orm_mode' in Pydantic v2
    }
