from schemas.team_schema import TeamCreate
from sqlalchemy.orm import Session
from models.users import User
from sqlalchemy.exc import IntegrityError
from schemas.user_schema import UserBase
from models.team_members import Teams,TeamMembers
import exceptions

def create_team(data:TeamCreate,db:Session,user:User):
    team=Teams(name=data.name)
    db.add(team)
    db.commit()
    db.refresh(team)
    user.role='admin'
    team_lead=TeamMembers(user_id=user.id,team_id=team.id,role='admin')
    db.add(team_lead)
    db.commit()  
    return team
def create_team_members(id:int,user_email:UserBase,current_user:User,db:Session):
    team = db.get(Teams, id)
    if not team:
        raise exceptions.TeamNotFoundError(f"Team with id {id} not found")

    # Check if current user is a member of this team (team admin check)
    team_membership = db.query(TeamMembers).filter(
        TeamMembers.user_id == current_user.id,
        TeamMembers.team_id == team.id
    ).first()
    if not team_membership:
        raise exceptions.NotTeamMemberError("You are not part of this team")
   # Fetch the user to add
    user_to_add = db.query(User).filter(User.email==user_email.email).first()
    if not user_to_add:
        raise exceptions.UserNotFoundError("User not Found")
    # Create membership
    team_member = TeamMembers(user_id=user_to_add.id, team_id=team.id, role='member')
    try:
        db.add(team_member)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise exceptions.UserAlreadyInTeamError("User already in the team")
    return {"detail": "User added successfully"}
