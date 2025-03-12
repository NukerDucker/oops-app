from typing import List, Tuple, Optional
from .base_entity import BaseEntity
from .fee import Fee
from .lab_result import LabResult
from .medication import Medication
from .prescription import Prescription
from . import utils

class Patient(BaseEntity):
    """Represents a patient in the hospital system."""
    
    def __init__(
        self, 
        name: str, 
        age: int, 
        gender: str
    ) -> None:
        """Initialize a new patient.
        
        Args:
            name: The patient's name
            age: The patient's age
            gender: The patient's gender
        """
        super().__init__()  # Generate the unique ID using the base class
        self._name = name
        self._age = age
        self._gender = gender
        self._history: List[str] = []
        self._medications: List[Medication] = []
        self._fees: List[Fee] = []
        self._lab_results: List[LabResult] = []
        self._prescription_history: List[Prescription] = []
    
    @property
    def patient_id(self) -> int:
        """Get the patient's unique identifier."""
        return self.id
    
    @property
    def name(self) -> str:
        """Get the patient's name."""
        return self._name
    
    @property
    def age(self) -> int:
        """Get the patient's age."""
        return self._age
    
    @property
    def gender(self) -> str:
        """Get the patient's gender."""
        return self._gender
    
    @property
    def history(self) -> List[str]:
        """Get the patient's medical history."""
        return self._history
    
    def add_history_entry(self, entry: str) -> None:
        """Add an entry to the patient's medical history.
        
        Args:
            entry: The history entry to add
        """
        self._history.append(entry)
    
    @property
    def current_medications(self) -> List[Medication]:
        """Get all of the patient's current medications."""
        return [med for med in self._medications if not med.finished]
    
    def generate_report(self) -> str:
        """Generate a comprehensive patient report.
        
        Returns:
            A formatted string containing patient information
        """
        report = [
            f"Patient Report for {self._name} (ID: {self.id})",
            f"Age: {self._age}",
            f"Gender: {self._gender}",
            "\nMedical History:",
        ]
        
        if not self._history:
            report.append("  No history records")
        else:
            for entry in self._history:
                report.append(f"  - {entry}")
        
        report.append("\nCurrent Medications:")
        current_meds = self.current_medications
        if not current_meds:
            report.append("  No current medications")
        else:
            for med in current_meds:
                report.append(f"  - {med.treatment} (for {med.diagnosis})")
        
        report.append("\nLab Results:")
        if not self._lab_results:
            report.append("  No lab results")
        else:
            for result in self._lab_results:
                report.append(f"  - Test #{result.lab_id}: {result.result}")
        
        report.append("\nFees:")
        total_fees = sum(fee.amount for fee in self._fees)
        report.append(f"  Total: ${total_fees:.2f}")
        
        return "\n".join(report)
    
    def add_fee(self, fee: Fee) -> None:
        """Add a fee to the patient's account.
        
        Args:
            fee: The fee to add
        """
        self._fees.append(fee)
    
    def remove_fee(self, fee: Fee) -> Tuple[bool, str]:
        """Remove a fee from the patient's account.
        
        Args:
            fee: The fee to remove
            
        Returns:
            A tuple of (success, message)
        """
        delete_at_index = utils.get_object_index_in_container(
            self._fees, fee, lambda obj: obj.id
        )
        if delete_at_index == -1:
            return False, "Error: Could not find fee in patient's list"
        del self._fees[delete_at_index]
        return True, "Success: Removed fee from patient"
    
    @property
    def fees(self) -> List[Fee]:
        """Get all fees associated with the patient."""
        return self._fees
    
    def add_lab_result(self, lab_result: LabResult) -> None:
        """Add a lab result to the patient's record.
        
        Args:
            lab_result: The laboratory result to add
        """
        self._lab_results.append(lab_result)
    
    @property
    def lab_results(self) -> List[LabResult]:
        """Get all laboratory results for the patient."""
        return self._lab_results
    
    def add_medication(self, medication: Medication) -> None:
        """Add a medication to the patient's record.
        
        Args:
            medication: The medication to add
        """
        self._medications.append(medication)
    
    @property
    def medications(self) -> List[Medication]:
        """Get all medications for the patient."""
        return self._medications
    
    def add_prescription(self, prescription: Prescription) -> None:
        """Add a prescription to the patient's history.
        
        Args:
            prescription: The prescription to add
        """
        self._prescription_history.append(prescription)
    
    @property
    def prescriptions(self) -> List[Prescription]:
        """Get all prescriptions for the patient."""
        return self._prescription_history
    
    def calculate_total_fees(self) -> float:
        """Calculate the total amount of all fees.
        
        Returns:
            The total fees amount
        """
        return sum(fee.amount for fee in self._fees)