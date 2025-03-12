from datetime import date, time
from typing import Optional
from .base_entity import BaseEntity

class Admission(BaseEntity):
    """Represents a patient admission record in the hospital system."""
    
    def __init__(
        self,
        patient_id: int,
        doctor_id: int,
        admission_date: date,
        admission_time: time
    ) -> None:
        """Initialize a new admission record.
        
        Args:
            patient_id: The ID of the admitted patient
            doctor_id: The ID of the attending doctor
            admission_date: The date of admission
            admission_time: The time of admission
        """
        super().__init__()  # Generate the unique ID using the base class
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._date = admission_date
        self._time = admission_time
    
    @property
    def patient_id(self) -> int:
        """Get the patient's ID."""
        return self._patient_id
    
    @property
    def doctor_id(self) -> int:
        """Get the doctor's ID."""
        return self._doctor_id
    
    @property
    def date(self) -> date:
        """Get the admission date."""
        return self._date
    
    @property
    def time(self) -> time:
        """Get the admission time."""
        return self._time