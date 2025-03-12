from typing import Tuple, List, Optional
from .base_entity import BaseEntity

class Prescription(BaseEntity):
    def __init__(
        self, 
        patient_id: int,
        doctor_id: int,
        medication: str, 
        dosage: str,
        amount: float
    ) -> None:
        super().__init__()
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._medication = medication
        self._dosage = dosage
        self._amount = amount
        self._feedback: Tuple[bool, str] = (False, "")
        self._is_approved = False
    
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
    def dosage(self) -> str:
        return self._dosage
        
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def feedback(self) -> Tuple[bool, str]:
        return self._feedback
    
    @feedback.setter
    def feedback(self, value: Tuple[bool, str]) -> None:
        self._feedback = value
    
    @property
    def is_approved(self) -> bool:
        return self._is_approved
    
    @is_approved.setter
    def is_approved(self, value: bool) -> None:
        self._is_approved = value