from typing import Tuple, Optional, Any
from .base_entity import BaseEntity
from .patient import Patient
from .system_registry import get_system

class Nurse(BaseEntity):
    """Represents a nurse in the hospital system."""
    
    def __init__(
        self, 
        name: str, 
        surname: str, 
        password: str
    ) -> None:
        """Initialize a new nurse.
        
        Args:
            name: The nurse's first name
            surname: The nurse's last name
            password: The nurse's password for system access
        """
        super().__init__()  # Generate the unique ID using the base class
        self._name = name
        self._surname = surname
        self._password = password
        self._is_assisting_lab_test = False
    
    @property
    def nurse_id(self) -> int:
        """Get the nurse's unique identifier."""
        return self.id
    
    @property
    def name(self) -> str:
        """Get the nurse's first name."""
        return self._name
    
    @property
    def surname(self) -> str:
        """Get the nurse's last name."""
        return self._surname
    
    @property
    def is_assisting_lab_test(self) -> bool:
        """Check if the nurse is currently assisting with a lab test."""
        return self._is_assisting_lab_test
    
    @is_assisting_lab_test.setter
    def is_assisting_lab_test(self, status: bool) -> None:
        """Set the nurse's lab test assistance status.
        
        Args:
            status: Whether the nurse is assisting with a lab test
        """
        self._is_assisting_lab_test = status
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change the nurse's password.
        
        Args:
            old_password: The current password for verification
            new_password: The new password to set
            
        Returns:
            A tuple of (success, message)
        """
        if old_password == self._password:
            self._password = new_password
            return True, "Success: Password changed"
        return False, "Error: Invalid password"
    
    def administer_treatment(self, patient_id: int, medicine: str) -> Tuple[bool, str]:
        """Administer treatment to a patient.
        
        Args:
            patient_id: The ID of the patient
            medicine: The medicine to administer
            
        Returns:
            A tuple of (success, message)
        """
        system = get_system()
        if not system:
            return False, "Error: System not available"
            
        patient = system.get_patient_from_id(patient_id)
        if not patient:
            return False, "Error: Patient not found"
            
        # Implementation would depend on how medications are tracked
        # This is a placeholder implementation
        return True, f"Success: Administered {medicine} to patient {patient.name}"
    
    def assist_lab_test(self, test_id: int) -> Tuple[bool, str]:
        """Assist with a laboratory test.
        
        Args:
            test_id: The ID of the laboratory test
            
        Returns:
            A tuple of (success, message)
        """
        if self._is_assisting_lab_test:
            return False, "Error: Already assisting with another lab test"
            
        self._is_assisting_lab_test = True
        # Additional implementation would depend on how lab tests are tracked
        return True, f"Success: Now assisting with lab test #{test_id}"