from fastapi import Depends,APIRouter,HTTPException
from database import get_db
from schemas.project_schema import ProjectCreate,ProjectResponse
from sqlalchemy.orm import Session
from models.users import User
from auth import require_admin,get_current_user
from services import project_service,task_service
import exceptions
from typing import List
from schemas.task_schema import TaskRead
router=APIRouter(prefix="/projects",tags=["Project"])
@router.post("/",response_model=ProjectResponse)
def create_project(data:ProjectCreate,db:Session=Depends(get_db),current_user: User = Depends(require_admin)):
    ...
    try:
        response=project_service.create_projects(data,db,current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return response
@router.get("/{project_id}",response_model=ProjectResponse)
def read_project(project_id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    ...
    try:
        response=project_service.read_project(project_id,db,current_user) 
    except exceptions.ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.NotPartOfProject as e:
            raise HTTPException(status_code=404, detail=str(e))
    return response
@router.post("/{project_id}/archieve",response_model=ProjectResponse)
def create_archieve(project_id:int,db:Session=Depends(get_db),team_lead: User = Depends(require_admin)):
    ...
    try:
        response=project_service.create_archieve(project_id,db,team_lead)
    except exceptions.ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.NotPartOfProject as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.ProjectAlreadyArchived as e:
        raise HTTPException(status_code=404, detail=str(e))

    return response
@router.get("/{id}/tasks",response_model=List[TaskRead])
def read_tasks(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        response=task_service.read_tasks(id,db,current_user)
       
    except exceptions.ProjectNotFoundError as e:
        raise HTTPException(status_code=404,detail=str(e))
    except exceptions.NotTeamMemberError as e:
        raise HTTPException(status_code=404,detail=str(e))
    except exceptions.NotPartOfProject as e:
            raise HTTPException(status_code=404,detail=str(e))
    except exceptions.TaskNotFoundForProject as e:
            raise HTTPException(status_code=404,detail=str(e))
    return response
    