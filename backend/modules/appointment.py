from datetime import date, time
from typing import Optional
from .base_entity import BaseEntity

class Appointment(BaseEntity):
    """Represents a scheduled appointment in the hospital system."""
    
    def __init__(
        self, 
        patient_id: int, 
        doctor_id: int, 
        appointment_date: date, 
        appointment_time: time
    ) -> None:
        """Initialize a new appointment.
        
        Args:
            patient_id: The ID of the patient for this appointment
            doctor_id: The ID of the doctor for this appointment
            appointment_date: The scheduled date of the appointment
            appointment_time: The scheduled time of the appointment
        """
        super().__init__()  # Generate the unique ID using the base class
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._date = appointment_date
        self._time = appointment_time
    
    @property
    def appointment_id(self) -> int:
        """Get the appointment's unique identifier."""
        return self.id  # Using the id property from BaseEntity
    
    @property
    def patient_id(self) -> int:
        """Get the ID of the patient for this appointment."""
        return self._patient_id
    
    @patient_id.setter
    def patient_id(self, value: int) -> None:
        """Set the ID of the patient for this appointment."""
        self._patient_id = value
    
    @property
    def doctor_id(self) -> int:
        """Get the ID of the doctor for this appointment."""
        return self._doctor_id
    
    @doctor_id.setter
    def doctor_id(self, value: int) -> None:
        """Set the ID of the doctor for this appointment."""
        self._doctor_id = value
    
    @property
    def date(self) -> date:
        """Get the scheduled date of the appointment."""
        return self._date
    
    @date.setter
    def date(self, value: date) -> None:
        """Set the scheduled date of the appointment."""
        self._date = value
    
    @property
    def time(self) -> time:
        """Get the scheduled time of the appointment."""
        return self._time
    
    @time.setter
    def time(self, value: time) -> None:
        """Set the scheduled time of the appointment."""
        self._time = value