from auth import hash_password,verify_password,create_access_token
from schemas.user_schema import UserCreate, UserLogin
from sqlalchemy.orm import Session
from models.users import User
def register_user(data:UserCreate,db:Session):
    ...
    hashed=hash_password(data.hashed_password)
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
                raise ValueError("Email already registered")  # <-- generic Python error
    user=User(
        email=data.email,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def login_user(data:UserLogin,db:Session):
    ...
    user=db.query(User).filter(User.email==data.email).first()
    if not user:
        raise ValueError("Invalid Email")
    password=verify_password(data.password,hashed=user.hashed_password)
    if not password:
        raise ValueError("Invalid Password")
    token=create_access_token(user.id,user.role)
    return token