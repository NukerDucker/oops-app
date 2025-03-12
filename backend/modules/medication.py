from datetime import date
from typing import Optional
from .base_entity import BaseEntity


class Medication(BaseEntity):
    """Represents a medication record in the hospital system.
    
    Contains information about patient symptoms, diagnosis,
    prescribed treatment, and treatment status.
    """
    
    def __init__(
        self,
        symptoms: str,
        diagnosis: str,
        treatment: str,
        treatment_date: date,
        finished: bool = False
    ) -> None:
        """Initialize a new medication record.
        
        Args:
            symptoms: Patient's reported symptoms
            diagnosis: Doctor's diagnosis
            treatment: Prescribed treatment
            treatment_date: Date when treatment was prescribed
            finished: Whether treatment is complete (defaults to False)
        """
        super().__init__()  # Generate the unique ID using the base class
        self._symptoms = symptoms
        self._diagnosis = diagnosis
        self._treatment = treatment
        self._date = treatment_date
        self._finished = finished
    
    @property
    def medication_id(self) -> int:
        """Get the medication's unique identifier."""
        return self.id
        
    @property
    def symptoms(self) -> str:
        """Get the patient's reported symptoms."""
        return self._symptoms
    
    @property
    def diagnosis(self) -> str:
        """Get the doctor's diagnosis."""
        return self._diagnosis
    
    @property
    def treatment(self) -> str:
        """Get the prescribed treatment."""
        return self._treatment
    
    @property
    def date(self) -> date:
        """Get the date when treatment was prescribed."""
        return self._date
    
    @property
    def finished(self) -> bool:
        """Check if the treatment is complete."""
        return self._finished
    
    @finished.setter
    def finished(self, state: bool) -> None:
        """Set the completion status of the treatment.
        
        Args:
            state: Whether the treatment is complete
        """
        self._finished = state
    
    def get_summary(self) -> str:
        """Get a formatted string summary of the medication.
        
        Returns:
            A multi-line string with medication details
        """
        return (
            f"Treatment ID: {self.id}\n"
            f"Symptoms    : {self._symptoms}\n"
            f"Diagnosis   : {self._diagnosis}\n"
            f"Treatment   : {self._treatment}\n"
            f"Date        : {self._date}\n"
            f"Status      : {'Completed' if self._finished else 'Ongoing'}"
        )