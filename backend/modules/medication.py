from typing import Tuple, Optional
from datetime import date
from .base_entity import BaseEntity

class Medication(BaseEntity):
    
    def __init__(
        self,
        patient_id: int,
        name: str,
        quantity: str,
        start_date: date,
        end_date: date,
        notes: str
    ) -> None:
        super().__init__()
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            raise ValueError("Patient ID must be a positive integer")
        self._patient_id = patient_id
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Medication name must be a non-empty string")
        self._name = name
        
        if not isinstance(quantity, str) or not quantity.strip():
            raise ValueError("Quantity must be a non-empty string")
        self._quantity = quantity
        
        if not isinstance(start_date, date):
            raise ValueError("Start date must be a date object")
        self._start_date = start_date
        
        if not isinstance(end_date, date):
            raise ValueError("End date must be a date object")
        self._end_date = end_date
        
        if not isinstance(notes, str):
            raise ValueError("Notes must be a string")
        self._notes = notes
        
        self._active = True
    
    @property
    def patient_id(self) -> int:
        return self._patient_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def quantity(self) -> str:
        return self._quantity
    
    @property
    def start_date(self) -> date:
        return self._start_date
    
    @property
    def end_date(self) -> date:
        return self._end_date
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @property
    def active(self) -> bool:
        return self._active
    
    @property
    def finished(self) -> bool:
        return date.today() > self._end_date
    
    def stop_medication(self) -> Tuple[bool, str]:
        if not self._active:
            return False, "Error: Medication is already inactive"
        self._active = False
        return True, "Success: Medication discontinued"
    
    def update_notes(self, value: str) -> Tuple[bool, str]:
        if not isinstance(value, str):
            return False, "Error: Notes must be a string"
        self._notes = value
        return True, "Success: Notes updated"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self._patient_id,
            "name": self._name,
            "quantity": self._quantity,
            "start_date": self._start_date.isoformat() if self._start_date else None,
            "end_date": self._end_date.isoformat() if self._end_date else None,
            "notes": self._notes,
            "active": self._active
        }
