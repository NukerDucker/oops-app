from datetime import date, time
from typing import Optional, Tuple
from .base_entity import BaseEntity

class Appointment(BaseEntity):
    
    def __init__(
        self, 
        patient_id: int, 
        doctor_id: int, 
        appointment_date: date, 
        appointment_time: time
    ) -> None:
        super().__init__()  
        
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            raise ValueError("Patient ID must be a positive integer")
        self._patient_id = patient_id
        
        
        if not isinstance(doctor_id, int) or doctor_id <= 0:
            raise ValueError("Doctor ID must be a positive integer")
        self._doctor_id = doctor_id
        
        
        if not isinstance(appointment_date, date):
            raise ValueError("Appointment date must be a date object")
        self._date = appointment_date
        
        
        if not isinstance(appointment_time, time):
            raise ValueError("Appointment time must be a time object")
        self._time = appointment_time
        
        
        self._status = "scheduled"  
    
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
    def date(self) -> date:
        return self._date
    
    def update_date(self, value: date) -> Tuple[bool, str]:
        if not isinstance(value, date):
            return False, "Error: Date must be a date object"
        self._date = value
        return True, "Success: Appointment date updated"
    
    @property
    def time(self) -> time:
        return self._time
    
    def update_time(self, value: time) -> Tuple[bool, str]:
        if not isinstance(value, time):
            return False, "Error: Time must be a time object"
        self._time = value
        return True, "Success: Appointment time updated"
    
    @property
    def status(self) -> str:
        return self._status
    
    def update_status(self, value: str) -> Tuple[bool, str]:
        valid_statuses = ["scheduled", "completed", "cancelled", "no-show"]
        if not isinstance(value, str) or value not in valid_statuses:
            return False, f"Error: Status must be one of {valid_statuses}"
        self._status = value
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
