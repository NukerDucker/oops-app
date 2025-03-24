from typing import Tuple, List, Optional
from .base_entity import BaseEntity
from .medication import Medication
from datetime import date

class Prescription(BaseEntity):
    def __init__(
        self, 
        patient_id: int,
        doctor_id: int,
        medication: Medication, 
        date: date,
        start_date: date,
        end_date: date,
    ) -> None:
        super().__init__()
        if not isinstance(start_date, date):
            raise ValueError("Start date must be a date object")
        self._start_date = start_date
        
        if not isinstance(end_date, date):
            raise ValueError("End date must be a date object")
        if end_date < start_date:
            raise ValueError("End date cannot be before start date")
        self._end_date = end_date
        
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._medication = medication
        self._date = date
    
    @property
    def prescription_id(self) -> int:
        return self.id
    
    @property
    def patient_id(self) -> int:
        return self._patient_id
    
    @property
    def doctor_id(self) -> int:
        return self._doctor_id
    
    @property
    def medication(self) -> str:
        return self._medication
    
    @property
    def start_date(self) -> date:
        return self._start_date
    
    @property
    def end_date(self) -> date:
        return self._end_date

    @property
    def date(self) -> date:
        return self._date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self._patient_id,
            "doctor_id": self._doctor_id,
            "medication": self._medication,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "date": self._date
        }