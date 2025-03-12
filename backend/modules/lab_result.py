from typing import Any
from .base_entity import BaseEntity

class LabResult(BaseEntity):
    """Represents laboratory test results in the hospital system.
    
    This class stores the lab test results for a patient including the test ID
    and the actual test result data.
    """
    
    def __init__(self, result: Any) -> None:
        """Initialize a new laboratory result.
        
        Args:
            result: The data containing the laboratory test results
        """
        super().__init__()  # Generate the unique ID using the base class
        self._result = result
    
    @property
    def lab_id(self) -> int:
        """Get the laboratory result's unique identifier."""
        return self.id
    
    @property
    def result(self) -> Any:
        """Get the laboratory test result data."""
        return self._result
    
    @result.setter
    def result(self, value: Any) -> None:
        """Update the laboratory test result data.
        
        Args:
            value: The new result data
        """
        self._result = value