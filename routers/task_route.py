from fastapi import Depends,APIRouter,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from auth import require_admin,get_current_user
from schemas.task_schema import TaskAuditSchema, TaskCreate, TaskRead,TaskUpdate
from models.users import User
from services import task_service
import exceptions
from typing import List
router=APIRouter(prefix="/tasks",tags=["Tasks"])
@router.post("/",response_model=TaskRead)
def create_task(data:TaskCreate,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        response=task_service.create_task(data,db,current_user)
        
    except exceptions.ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.ArchivedProjectConflict as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.NotPartOfProject as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.UserNotPartOfProject as e:
        raise HTTPException(
        status_code=403,
        detail=str(e)  
    )
    except exceptions.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.InvalidAssignedUserTeam as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    return response
@router.post("/{id}/change-state",response_model=TaskRead)
def update_task(id:int,state:TaskUpdate,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    ...
    try:
        response=task_service.update_task_state(id,state,db,current_user)
    except exceptions.TaskPermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    except exceptions.InvalidTaskStateTransition as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    return response
@router.post("/{id}/archive-task",response_model=TaskRead)
def create_archive_task(id:int,db:Session=Depends(get_db),team_lead:User=Depends(require_admin)):
    try:
        response=task_service.archieve_task(id,db,team_lead)
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except exceptions.Forbidden as e:
        raise HTTPException(status_code=403, detail=str(e))
    except exceptions.Conflict as e:
        raise HTTPException(status_code=409, detail=str(e))
    return response

@router.get("/{id}/audit",response_model=List[TaskAuditSchema])
def read_audit(id:int,db:Session=Depends(get_db),team_lead:User=Depends(require_admin)):
    try:
        response=task_service.view_audits(id,db,team_lead)
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except exceptions.NotTeamMemberError:
        raise HTTPException(status_code=403, detail="Forbidden")
    except exceptions.TaskNotFoundForProject:
         raise HTTPException(status_code=404, detail="Task not found in this project")
    return response