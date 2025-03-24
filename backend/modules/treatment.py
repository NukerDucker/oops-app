from datetime import date
from typing import Optional
from .base_entity import BaseEntity
from .prescription import Prescription

class Treatment(BaseEntity):
    
    def __init__(
        self,
        symptoms: str,
        diagnosis: str,
        treatment: str,
        treatment_date: date,
        finished: bool = False
    ) -> None:
        super().__init__()  
        self._symptoms = symptoms
        self._diagnosis = diagnosis
        self._treatment = treatment
        self._date = treatment_date
        self._finished = finished
    
    @property
    def treatment_id(self) -> int:
        return self.id
        
    @property
    def symptoms(self) -> str:
        return self._symptoms
    
    @property
    def diagnosis(self) -> str:
        return self._diagnosis
    
    @property
    def treatment(self) -> str:
        return self._treatment
    
    @property
    def date(self) -> date:
        return self._date
    
    @property
    def finished(self) -> bool:
        return self._finished
    
    @finished.setter
    def finished(self, state: bool) -> None:
        self._finished = state
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "symptoms": self._symptoms,
            "diagnosis": self._diagnosis,
            "treatment": self._treatment,
            "date": self._date.isoformat() if self._date else None,
            "finished": self._finished
        }