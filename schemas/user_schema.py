import datetime
from pydantic import EmailStr
from pydantic import BaseModel,field_validator
from datetime import datetime
import re
class UserBase(BaseModel):
    email:EmailStr
class UserCreate(UserBase):
    hashed_password:str
    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{8,}$"
        if not re.match(pattern, v):
            raise ValueError("Password is too weak")
        return v
class UserResponse(UserBase):
    id:int
    created_at:datetime
    role:str
    model_config = {
        "from_attributes": True  # replaces 'orm_mode' in Pydantic v2
    }
class UserLogin(UserBase):
    email:str
    password:str