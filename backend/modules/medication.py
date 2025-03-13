from typing import Tuple
from datetime import date
from .base_entity import BaseEntity

class Medication(BaseEntity):
    """
    Represents a medication prescribed to a patient.
    
    Stores:
    - Medication name and dosage information
    - Start and end dates
    - Status tracking
    
    Does NOT store:
    - Patient information (stored in Patient class)
    - Prescription details (stored in Prescription class)
    """
    
    def __init__(
        self,
        patient_id: int,
        name: str,
        dosage: str,
        start_date: date,
        end_date: date,
        notes: str = ""
    ) -> None:
        """Initialize a new Medication with validation."""
        super().__init__()
        
        # Validate inputs
        if not isinstance(patient_id, int) or patient_id <= 0:
            raise ValueError("Patient ID must be a positive integer")
        self._patient_id = patient_id
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Medication name must be a non-empty string")
        self._name = name
        
        if not isinstance(dosage, str) or not dosage.strip():
            raise ValueError("Dosage must be a non-empty string")
        self._dosage = dosage
        
        if not isinstance(start_date, date):
            raise ValueError("Start date must be a date object")
        self._start_date = start_date
        
        if not isinstance(end_date, date):
            raise ValueError("End date must be a date object")
        if end_date < start_date:
            raise ValueError("End date cannot be before start date")
        self._end_date = end_date
        
        if not isinstance(notes, str):
            raise ValueError("Notes must be a string")
        self._notes = notes
        
        self._active = True
    
    @property
    def patient_id(self) -> int:
        """Get the patient ID this medication belongs to."""
        return self._patient_id
    
    @property
    def name(self) -> str:
        """Get the medication name."""
        return self._name
    
    @property
    def dosage(self) -> str:
        """Get the medication dosage."""
        return self._dosage
    
    @property
    def start_date(self) -> date:
        """Get the medication start date."""
        return self._start_date
    
    @property
    def end_date(self) -> date:
        """Get the medication end date."""
        return self._end_date
    
    @property
    def notes(self) -> str:
        """Get any additional notes."""
        return self._notes
    
    @property
    def active(self) -> bool:
        """Check if the medication is currently active."""
        return self._active
    
    @property
    def finished(self) -> bool:
        """Check if the medication course is finished (based on end date)."""
        return date.today() > self._end_date
    
    def stop_medication(self) -> Tuple[bool, str]:
        """Discontinue the medication."""
        if not self._active:
            return False, "Error: Medication is already inactive"
        self._active = False
        return True, "Success: Medication discontinued"