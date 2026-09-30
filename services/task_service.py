from models.users import User
from sqlalchemy.orm import Session
import exceptions
from models.project import Project
from schemas.task_schema import TaskCreate,TaskUpdate
from models.team_members import TeamMembers
from models.tasks import Task
from models.task_audit import TaskAudit
from datetime import datetime,timezone
from sqlalchemy.orm import joinedload


from enum import Enum

class TaskState(str, Enum):
    OPEN = "todo"
    IN_PROGRESS = "in-progress"
    COMPLETED = "done"
    ARCHIVED = "archived"
def create_task(data:TaskCreate,db:Session,current_user:User):
    ...
    
    project=db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise exceptions.ProjectNotFoundError("Project not found",
                                              project_id=data.project_id)
    if project.is_archived:
        raise exceptions.ArchivedProjectConflict(
            "Cannot create task in an archived project"
        )
    
    '''
    Any team member may assign a task to any other member of the same team.
    '''
    team_member=db.query(TeamMembers).filter(TeamMembers.user_id == current_user.id,TeamMembers.team_id == project.team_id).first()
    if not team_member:
        raise exceptions.NotPartOfProject("You are not a part of this Project"
        ,user_id=current_user.id,
        project_id=project.id)
    user=db.query(User).filter(User.id == data.assigned_to).first()
    if not user:
        raise exceptions.UserNotFoundError("User not found")
    # Assigned user must belong to the Project
    assinged_user=db.query(TeamMembers).filter(TeamMembers.user_id == data.assigned_to,TeamMembers.team_id == project.team_id).first()
    if not assinged_user:
        raise exceptions.UserNotPartOfProject(
        "Assigned user is not part of this project",
        user_id=data.assigned_to,
        project_id=project.id
            )
    task=Task(
        project_id=data.project_id,
        assigned_to=data.assigned_to,
        title=data.title,
        description=data.description,
        state=TaskState.OPEN
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
def update_task_state(id:int,user_state:TaskUpdate,db:Session,current_user:User):
    ...
    task=db.get(Task,id)
    if not task:
       raise exceptions.TaskNotFound("Task not found")
   

    if task.state == TaskState.ARCHIVED:
        raise exceptions.Conflict("Archived tasks cannot be modified")

   
    if task.assigned_to != current_user.id:
        raise exceptions.TaskPermissionError("You are not assigned to this task")
    old_state=task.state
    if task.state == TaskState.OPEN and user_state.state == TaskState.IN_PROGRESS:
        task.state = TaskState.IN_PROGRESS
    elif task.state == TaskState.IN_PROGRESS and user_state.state == TaskState.COMPLETED:
        task.state = TaskState.COMPLETED
        task.completed_at = datetime.now(timezone.utc)

    else:
        raise exceptions.InvalidTaskStateTransition("Invalid state transition")
    new_state=task.state
    task_audit=TaskAudit(task_id=task.id,
              user_id=current_user.id,
              old_state=old_state,
              new_state=new_state)
    db.add(task_audit)
    db.commit() # Commit both tasks.
    db.refresh(task)
    return task
def archieve_task(id:int,db:Session,team_lead:User):
    ...
    task=db.get(Task,id)
    if not task:
            raise exceptions.TaskNotFound("Task not found")
    is_admin=db.query(TeamMembers).filter(TeamMembers.role == team_lead.role)
    if not is_admin:
            raise exceptions.Forbidden("Only team leads can archive tasks")

    
    if task.state == TaskState.ARCHIVED:
        raise exceptions.Conflict(
            "Task is already archived"
        )

    if task.state != TaskState.COMPLETED:
        raise exceptions.Conflict(
            "Only completed tasks can be archived"
        )
    task.state = TaskState.ARCHIVED
    db.commit()
    db.refresh(task)
    return task
def read_tasks(id:int,db:Session,current_user:User):
    project=db.get(Project,id)
    if not project:
        raise exceptions.ProjectNotFoundError("Project not found",project_id=id)
    
    team_member=db.query(TeamMembers).filter(TeamMembers.user_id ==current_user.id,TeamMembers.team_id == project.team_id).first()
    if not team_member:
        raise exceptions.NotTeamMemberError("User is not a member of this project's team")

    tasks=project.tasks
    #Used relationship here (1-M)
    if not tasks:
        raise exceptions.TaskNotFoundForProject("Task not found for this project")
    return tasks
def view_audits(id:int,db:Session,team_lead:User):
    ...
    task=db.get(Task,id)
    if not task:
        raise exceptions.TaskNotFound("task not found")
    
    project=task.project
    team_id = project.team_id
    team_member = db.query(TeamMembers).filter(
        TeamMembers.user_id == team_lead.id,
        TeamMembers.team_id == team_id,
        TeamMembers.role   == 'admin').first()
    if not team_member:
        exceptions.NotTeamMemberError("User is not an admin of this team")
    tasks = db.query(Task).filter(Task.project_id == project.id).first()
    if not tasks:
        raise exceptions.TaskNotFoundForProject(
            "No tasks found in this project"
        )
    audits=db.query(TaskAudit).filter(TaskAudit.task_id == id).all()
        # task_obj = db.query(Task).options(joinedload(Task.project)).filter(Task.id == id).first()
    return audits

    
