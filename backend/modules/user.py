from typing import Literal, Tuple
from .base_entity import BaseEntity

UserType = Literal["doctor", "receptionist"]

class User(BaseEntity):
    """Base user class for system authentication and role management."""
    
    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        user_type: UserType
    ) -> None:
        """Initialize a new User.
        
        Args:
            name: The user's full name
            username: The user's login username
            password: The user's password
            user_type: The type of user (doctor/receptionist)
        """
        super().__init__()  # Generate the unique ID using the base class
        self._name = name
        self._username = username
        self._password = password
        self._user_type = user_type
    
    @property
    def name(self) -> str:
        """Get the user's name."""
        return self._name
    
    @property
    def username(self) -> str:
        """Get the user's username."""
        return self._username
    
    @property
    def user_type(self) -> UserType:
        """Get the user's type."""
        return self._user_type
    
    @property
    def password(self) -> str:
        """Get the user's password (should only be used for authentication)."""
        return self._password
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change the user's password.
        
        Args:
            old_password: The current password for verification
            new_password: The new password to set
            
        Returns:
            A tuple of (success, message)
        """
        if old_password == self._password:
            self._password = new_password
            return True, "Success: Password changed"
        return False, "Error: Invalid password"