from typing import Literal, Optional, Tuple
from .base_entity import BaseEntity

UserType = Literal["User", "Admin", "Doctor", "Receptionist"]

class AccessPermission:
    def __init__(self, access, access_link):
        self.access = access
        self.access_link = access_link
        
    def to_dict(self):
        return {
            "access": self.access,
            "access_link": self.access_link
        }

class User(BaseEntity):
    """Base user class for system authentication and role management."""
    
    def __init__(
        self,
        id: int,
        username: str, 
        password_hash: str,
        user_type: UserType = "user",
    ) -> None:
        """Initialize a new User.
        
        Args:
            id: The user's unique identifier
            username: The user's login username
            password_hash: The user's hashed password
            user_type: The type of user (defaults to "user")
            email: The user's email address (optional)
        """
        # Use provided ID instead of generating one from BaseEntity
        self._id = id
        self._username = username
        self._password_hash = password_hash
        self._user_type = user_type
        self._profile_image_directory = "Profile-Icon.png"
        self._access_permissions = []
        self._tasks = []
        self._weekly_tasks = []
        self._emergency_tasks = []
    
    @property
    def id(self) -> int:
        """Get the user's ID."""
        return self._id
    
    @property
    def username(self) -> str:
        """Get the user's username."""
        return self._username
    
    @property
    def password_hash(self) -> str:
        """Get the user's hashed password (should only be used for authentication)."""
        return self._password_hash
    
    @property
    def user_type(self) -> UserType:
        """Get the user's type."""
        return self._user_type
    
    
    def add_access_permission(self, access, access_link):
        self._access_permissions.append(AccessPermission(access, access_link))
        
    def add_task(self, task):
        self._tasks.append(task)
        
    def add_weekly_task(self, task):
        self._weekly_tasks.append(task)
        
    def add_emergency_task(self, task):
        self._emergency_tasks.append(task)
        
    def to_dict(self) -> dict:
        """Convert user to dictionary representation (for API responses)."""
        return {
            "id": self.id,
            "username": self.username,
            "user_type": self.user_type,
            "allow_access": [perm.to_dict() for perm in self._access_permissions],
            "profile_image_directory": self._profile_image_directory,
            "tasks": [task.to_dict() for task in self._tasks],
            "weekly_tasks": [task.to_dict() for task in self._weekly_tasks],
            "emergency_tasks": [task.to_dict() for task in self._emergency_tasks]
        }