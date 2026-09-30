from fastapi import Depends,APIRouter, HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserCreate, UserLogin,UserResponse
from services import user_service
router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/register",response_model=UserResponse)
def create_user(data:UserCreate,db:Session=Depends(get_db)):
    try:
        response=user_service.register_user(data,db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response

@router.post("/login",tags=["Authentication"])
def create_login(data:UserLogin,db:Session=Depends(get_db)):
    try:
        access_token=user_service.login_user(data,db)
        return {
            "access_token": access_token,
            "token_type": "bearer"
            }
    except ValueError as e:
        if e ==("Invalid Password"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
        if e == ("Invalid Email"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
        