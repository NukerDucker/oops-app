from datetime import date, time
from typing import Optional
from .base_entity import BaseEntity

class LabRequest(BaseEntity):
    """Represents a laboratory test request in the hospital system."""
    
    def __init__(
        self, 
        patient_id: int, 
        request_type: str, 
        request_date: date, 
        request_time: time
    ) -> None:
        """Initialize a new laboratory request.
        
        Args:
            patient_id: The ID of the patient for this lab request
            request_type: The type of laboratory test requested
            request_date: The date when the test was requested
            request_time: The time when the test was requested
        """
        super().__init__()  # Generate the unique ID using the base class
        self._patient_id = patient_id
        self._type = request_type
        self._date = request_date
        self._time = request_time
    
    @property
    def request_id(self) -> int:
        """Get the lab request's unique identifier."""
        return self.id
    
    @property
    def patient_id(self) -> int:
        """Get the ID of the patient associated with this request."""
        return self._patient_id
    
    @property
    def type(self) -> str:
        """Get the type of laboratory test requested."""
        return self._type
    
    @property
    def date(self) -> date:
        """Get the date when the test was requested."""
        return self._date
    
    @property
    def time(self) -> time:
        """Get the time when the test was requested."""
        return self._time