from typing import List, Tuple, Optional
from .base_entity import BaseEntity
from .lab_request import LabRequest
from .lab_result import LabResult
from .patient import Patient
from .system_registry import get_system

class LabPersonnel(BaseEntity):
    """Represents a laboratory personnel in the hospital system."""
    
    def __init__(
        self, 
        name: str, 
        surname: str, 
        password: str
    ) -> None:
        """Initialize a new laboratory personnel.
        
        Args:
            name: The personnel's first name
            surname: The personnel's last name
            password: The personnel's password for system access
        """
        super().__init__()  # Generate the unique ID using the base class
        self._name = name
        self._surname = surname
        self._password = password
        self._pending_labs: List[LabRequest] = []
    
    @property
    def personnel_id(self) -> int:
        """Get the personnel's unique identifier."""
        return self.id
    
    @property
    def name(self) -> str:
        """Get the personnel's first name."""
        return self._name
    
    @property
    def surname(self) -> str:
        """Get the personnel's last name."""
        return self._surname
    
    @property
    def pending_labs(self) -> List[LabRequest]:
        """Get the list of pending lab requests."""
        return self._pending_labs
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change the personnel's password.
        
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
    
    def assign_lab_test(self, lab_request: LabRequest) -> None:
        """Assign a lab test to this personnel.
        
        Args:
            lab_request: The laboratory request to assign
        """
        self._pending_labs.append(lab_request)
    
    def return_lab_result_to_patient(self, lab_request_id: int, lab_result: LabResult) -> Tuple[bool, str]:
        """Process and return lab test results to a patient.
        
        Args:
            lab_request_id: The ID of the lab request
            lab_result: The laboratory test results
            
        Returns:
            A tuple of (success, message)
        """
        # Find the matching lab request
        target_index = -1
        for i, pending_lab in enumerate(self._pending_labs):
            if pending_lab.id == lab_request_id:  # Using property instead of getter
                target_index = i
                break
                
        if target_index == -1:
            return False, "Error: Unable to find the pending lab request"
        
        # Get the patient from the system
        system = get_system()
        if system is None:
            return False, "Error: System not available"
            
        patient_id = self._pending_labs[target_index].patient_id
        patient = system.get_patient_from_id(patient_id)
        
        if patient is None:
            return False, "Error: Unable to find patient of the lab request"
            
        # Remove the pending lab and add the result to the patient
        del self._pending_labs[target_index]
        patient.add_lab_result(lab_result)
        return True, "Success: Added lab result to patient"