from datetime import date
from typing import Optional, Union, Literal
from .base_entity import BaseEntity

FeeType = Literal["doctor", "medication", "lab", "other"]

class Fee(BaseEntity):
    """Represents a fee charged to a patient."""
    
    def __init__(
        self,
        patient_id: int,
        amount: float,
        fee_type: FeeType,
        description: str,
        date: str
    ) -> None:
        """Initialize a new Fee."""
        super().__init__()
        self._patient_id = patient_id
        self._amount = amount
        self._fee_type = fee_type
        self._description = description
        self._date = date
        self._paid = False
    
    @property
    def patient_id(self) -> int:
        """Get the patient ID."""
        return self._patient_id
    
    @property
    def amount(self) -> float:
        """Get the fee amount."""
        return self._amount
    
    @property
    def fee_type(self) -> FeeType:
        """Get the fee type."""
        return self._fee_type
    
    @property
    def description(self) -> str:
        """Get the fee description."""
        return self._description
    
    @property
    def date(self) -> str:
        """Get the fee date."""
        return self._date
    
    @property
    def paid(self) -> bool:
        """Get the payment status."""
        return self._paid
    
    def mark_as_paid(self) -> None:
        """Mark the fee as paid."""
        self._paid = True