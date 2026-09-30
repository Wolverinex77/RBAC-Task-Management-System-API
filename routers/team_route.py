from fastapi import Depends,APIRouter,HTTPException
from database import get_db
from schemas.team_schema import TeamCreate,TeamResponse
from schemas.user_schema import UserBase
from sqlalchemy.orm import Session
from auth import require_admin,get_current_user
from models.users import User
from services import team_service
import exceptions
router=APIRouter(prefix="/teams",tags=["Teams"])

#Add team (Team Lead)
@router.post("/",response_model=TeamResponse)
def create_team(data:TeamCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    
        return team_service.create_team(data,db,user)
   
#Add User to Admin (Team Lead)
@router.post("/{id}/add-user")
def create_team_member(id: int,user_email:UserBase,current_user: User = Depends(require_admin), db: Session = Depends(get_db)):

    try:
        msg=team_service.create_team_members(id,user_email,current_user,db)
    except exceptions.TeamNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.NotTeamMemberError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except exceptions.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.UserAlreadyInTeamError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return msg


   
    
        
    