from datetime import date
from typing import Optional, Union, Literal
from .base_entity import BaseEntity

FeeType = Literal["doctor", "medication", "lab", "other"]

class Fee(BaseEntity):
    
    def __init__(
        self,
        patient_id: int,
        amount: float,
        fee_type: FeeType,
        description: str,
        date: str
    ) -> None:
        super().__init__()
        self._patient_id = patient_id
        self._amount = amount
        self._fee_type = fee_type
        self._description = description
        self._date = date
        self._paid = False
    
    @property
    def patient_id(self) -> int:
        return self._patient_id
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def fee_type(self) -> FeeType:
        return self._fee_type
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def date(self) -> str:
        return self._date
    
    @property
    def paid(self) -> bool:
        return self._paid
    
    def mark_as_paid(self) -> None:
        self._paid = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self._patient_id,
            "amount": self._amount,
            "fee_type": self._fee_type,
            "description": self._description,
            "date": self._date,
            "paid": self._paid
        }