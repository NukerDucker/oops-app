from datetime import date
from typing import Optional, Union
from .base_entity import BaseEntity

class Fee(BaseEntity):
    """Represents a fee charged to a patient in the hospital system."""
    
    def __init__(
        self, 
        amount: float, 
        fee_date: date, 
        patient_id: int
    ) -> None:
        """Initialize a new fee record.
        
        Args:
            amount: The fee amount
            fee_date: The date when the fee was charged
            patient_id: The ID of the patient associated with this fee
        """
        super().__init__()  # Generate the unique ID using the base class
        self._amount = amount
        self._date = fee_date
        self._patient_id = patient_id
    
    @property
    def fee_id(self) -> int:
        """Get the fee's unique identifier."""
        return self.id
    
    @property
    def amount(self) -> float:
        """Get the fee amount."""
        return self._amount
    
    @property
    def date(self) -> date:
        """Get the date when the fee was charged."""
        return self._date
    
    @property
    def patient_id(self) -> int:
        """Get the ID of the patient associated with this fee."""
        return self._patient_id