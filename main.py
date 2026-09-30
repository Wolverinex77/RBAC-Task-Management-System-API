from fastapi import FastAPI
from routers.auth_route import router as auth_router
from routers.team_route import router as team_router
from routers.project_route import router as project_router
from routers.task_route import router as task_router
from models.users import User
from models.tasks import Task
from models.team_members import Teams,TeamMembers
from models.project import Project
from database import engine,Base

Base.metadata.create_all(engine)

app=FastAPI()
app.include_router(auth_router)
app.include_router(team_router)
app.include_router(project_router)
app.include_router(task_router)

