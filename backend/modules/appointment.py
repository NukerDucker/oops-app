from datetime import date as date_type, time as time_type
from typing import Optional, Tuple, Literal
from .base_entity import BaseEntity

# Define valid status values as lowercase to ensure consistency
StatusType = Literal["scheduled", "completed", "cancelled", "no-show"]
VALID_STATUSES = ["scheduled", "completed", "cancelled", "no-show"]

class Appointment(BaseEntity):
    
    def __init__(
        self, 
        patient_id: int, 
        doctor_id: int, 
        date: date_type, 
        time: time_type,
        status: str = "scheduled",
        about: Optional[str] = None
    ) -> None:
        super().__init__()  
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            raise ValueError("Patient ID must be a positive integer")
        self._patient_id = patient_id
        
        if not isinstance(doctor_id, int) or doctor_id <= 0:
            raise ValueError("Doctor ID must be a positive integer")
        self._doctor_id = doctor_id
        
        if not isinstance(date, date_type):
            raise ValueError("Appointment date must be a date object")
        self._date = date
        
        if not isinstance(time, time_type):
            raise ValueError("Appointment time must be a time object")
        self._time = time
        
        # Normalize status to lowercase
        status_lower = status.lower() if status else "scheduled"
        if status_lower not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        self._status = status_lower
        
        # Initialize about field
        self._about = about
    
    @property
    def appointment_id(self) -> int:
        return self.id  
    
    @property
    def patient_id(self) -> int:
        return self._patient_id
    
    def update_patient_id(self, value: int) -> Tuple[bool, str]:
        if not isinstance(value, int) or value <= 0:
            return False, "Error: Patient ID must be a positive integer"
        self._patient_id = value
        return True, "Success: Patient ID updated"
    
    @property
    def doctor_id(self) -> int:
        return self._doctor_id
    
    def update_doctor_id(self, value: int) -> Tuple[bool, str]:
        if not isinstance(value, int) or value <= 0:
            return False, "Error: Doctor ID must be a positive integer"
        self._doctor_id = value
        return True, "Success: Doctor ID updated"
    
    @property
    def date(self) -> date_type:
        return self._date
    
    def update_date(self, value: date_type) -> Tuple[bool, str]:
        if not isinstance(value, date_type):
            return False, "Error: Date must be a date object"
        self._date = value
        return True, "Success: Appointment date updated"
    
    @property
    def time(self) -> time_type:
        return self._time
    
    def update_time(self, value: time_type) -> Tuple[bool, str]:
        if not isinstance(value, time_type):
            return False, "Error: Time must be a time object"
        self._time = value
        return True, "Success: Appointment time updated"
    
    @property
    def status(self) -> str:
        return self._status
    
    def update_status(self, value: str) -> Tuple[bool, str]:
        value_lower = value.lower() if value else ""
        if not isinstance(value, str) or value_lower not in VALID_STATUSES:
            return False, f"Error: Status must be one of {VALID_STATUSES}"
        self._status = value_lower
        return True, "Success: Appointment status updated"
    
    def is_completed(self) -> bool:
        return self._status == "completed"
    
    def is_active(self) -> bool:
        return self._status == "scheduled"
    
    def cancel(self) -> Tuple[bool, str]:
        if self._status == "completed":
            return False, "Error: Cannot cancel a completed appointment"
        self._status = "cancelled"
        return True, "Success: Appointment cancelled"
    
    def mark_completed(self) -> Tuple[bool, str]:
        if self._status == "cancelled" or self._status == "no-show":
            return False, f"Error: Cannot complete a {self._status} appointment"
        self._status = "completed"
        return True, "Success: Appointment marked as completed"
    
    def mark_no_show(self) -> Tuple[bool, str]:
        if self._status != "scheduled":
            return False, "Error: Only scheduled appointments can be marked as no-show"
        self._status = "no-show"
        return True, "Success: Appointment marked as no-show"

    @property
    def about(self) -> Optional[str]:
        return self._about
    
    def update_about(self, value: str) -> Tuple[bool, str]:
        if not isinstance(value, str):
            return False, "Error: About must be a string"
        self._about = value
        return True, "Success: Appointment about updated"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self._patient_id,
            "doctor_id": self._doctor_id,
            "date": self._date.isoformat() if self._date else None,
            "time": self._time.isoformat() if self._time else None,
            "status": self._status,
            "about": self._about
        }

