from sqlalchemy.orm import Session
from models.team_members import TeamMembers
from models.users import User
from schemas.project_schema import ProjectCreate
from models.project import Project
import exceptions
def create_projects(data:ProjectCreate,db:Session,admin:User):
    ...
    is_member=db.query(TeamMembers).filter(TeamMembers.user_id==admin.id,TeamMembers.role == "admin").first()
    if not is_member:
        raise ValueError("Admin not part of any team")
    admin_team_id=is_member.team_id
    project=Project(name=data.name,team_id=admin_team_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
def read_project(id:int,db:Session,current_user:User):
    ...
    project=db.get(Project,id)
    if not project:
        raise exceptions.ProjectNotFoundError("Project not found",
                                              project_id=id)
    # user_team=project.team #M-1
    team_member=db.query(TeamMembers).filter(TeamMembers.user_id==current_user.id,TeamMembers.team_id==project.team_id).first()
    if not team_member:
        raise exceptions.NotPartOfProject("You are not a part of this Project"
        ,user_id=current_user.id,
        project_id=id)
    return project
def create_archieve(id:int,db:Session,team_lead:User):
    ...
    project=db.get(Project,id)
    if not project:
        raise exceptions.ProjectNotFoundError("Project not found",
                                              project_id=id)   
    # user_team=project.team #M-1
    team_member=db.query(TeamMembers).filter(TeamMembers.user_id==team_lead.id,TeamMembers.team_id==project.team_id,TeamMembers.role=="admin").first()
    if not team_member:
        raise exceptions.NotPartOfProject("You are not a part of this Project"
        ,user_id=team_lead.id,
        project_id=id)
    if project.is_archived == True:
        raise exceptions.ProjectAlreadyArchived("Project is already archived")
    project.is_archived=True
    db.commit()
    db.refresh(project)
    return project
