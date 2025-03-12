from typing import ClassVar

class BaseEntity:
    """Base class for all entities that require unique identification."""
    
    current_id: ClassVar[int] = 0
    
    @classmethod
    def generate_id(cls) -> int:
        """Generate a unique identifier.
        
        Returns:
            int: A new unique identifier
        """
        cls.current_id += 1
        return cls.current_id
    
    def __init__(self) -> None:
        """Initialize the base entity with a unique ID."""
        self._id = self.__class__.generate_id()
    
    @property
    def id(self) -> int:
        """Get the entity's unique identifier.
        
        Returns:
            int: The unique identifier
        """
        return self._id