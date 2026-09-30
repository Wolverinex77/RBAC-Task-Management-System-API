# exceptions.py
class TeamError(Exception):
    """Base class for all team-related exceptions."""
    pass

class TeamNotFoundError(TeamError):
    pass

class NotTeamMemberError(TeamError):
    pass

class UserNotFoundError(TeamError):
    pass

class UserAlreadyInTeamError(TeamError):
    pass
class ProjectError(Exception):
    pass
class ProjectNotFoundError(ProjectError):
    def __init__(self, message: str,
                 project_id:int):
        super().__init__(message)
        self.project_id=project_id
class NotPartOfProject(ProjectError):
    def __init__(self, message: str,
                user_id:int,
                project_id:int
    ):
        super().__init__(message)
        self.user_id = user_id
        self.project_id = project_id
        
class ProjectAlreadyArchived(ProjectError):
    pass
class ArchivedProjectConflict(ProjectError):
    pass

class TaskException(Exception):
    pass

class UserNotPartOfProject(TaskException):
    def __init__(
        self,
        message: str,
        user_id: int | None = None,
        project_id: int | None = None
    ):  
        super().__init__(message)
        self.user_id = user_id
        self.project_id = project_id
class InvalidAssignedUserTeam(TaskException):
    pass
class TaskNotFound(TaskException):
    """Raised when the task is not found"""
    pass
class TaskPermissionError(TaskException):
    """Raised when the user is not assigned to the task"""
    pass
class InvalidTaskStateTransition(TaskException):
    """Raised when the requested state transition is invalid"""
    pass
# Forbidden (403) exceptions
class Forbidden(TaskException):
    """Raised when the user does not have permission to perform the action"""
    pass
# Conflict (409) exceptions
class Conflict(TaskException):
    """Raised when the requested action conflicts with current state"""
    pass
class TaskNotFoundForProject(TaskException):
    pass
