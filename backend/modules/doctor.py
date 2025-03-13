from typing import List, Tuple, Optional
from .user import User
from .patient import Patient
from .appointment import Appointment
from .lab_result import LabResult
from .prescription import Prescription
from .medication import Medication
from .treatment import Treatment

# We'll use dependency injection rather than global imports
class Doctor(User):
    """
    Represents a doctor in the hospital system.
    
    Stores:
    - Name, username, password (inherited from User)
    - Medical speciality
    - List of invalid prescriptions
    
    Does NOT store:
    - Patient information (stored in Patient class)
    - Appointment information (stored in Appointment class)
    - System-wide configuration
    - Lab results (stored in Patient class)
    - Medication information (stored in Medication class)
    """
    
    def __init__(
        self, 
        name: str,
        username: str,
        password: str,
        speciality: str,
        system_service
    ) -> None:
        """Initialize a new Doctor with validation.
        
        Args:
            name: The doctor's name
            username: The doctor's username
            password: The doctor's password
            speciality: The doctor's medical speciality
            system_service: Service for accessing system-wide operations
        """
        super().__init__(name, username, password, "doctor")
        
        # Validate speciality
        if not isinstance(speciality, str) or not speciality.strip():
            raise ValueError("Doctor speciality must be a non-empty string")
        self._speciality = speciality
        
        self._invalid_prescriptions: List[Prescription] = []
        self._system_service = system_service
    
    @property
    def doctor_id(self) -> int:
        """Get the doctor's unique identifier."""
        return self.id
    
    @property
    def speciality(self) -> str:
        """Get the doctor's medical speciality."""
        return self._speciality
    
    def update_speciality(self, value: str) -> Tuple[bool, str]:
        """Update the doctor's speciality with validation."""
        if not isinstance(value, str) or not value.strip():
            return False, "Error: Speciality must be a non-empty string"
        self._speciality = value
        return True, "Success: Speciality updated"
    
    def view_patient_record(self, patient_id: int) -> Optional[Patient]:
        """Retrieve a patient's record with validation."""
        if not isinstance(patient_id, int) or patient_id <= 0:
            return None
        return self._system_service.get_patient_from_id(patient_id)

    # Lab Result Management
    def add_lab_result(self, patient_id: int, lab_result: LabResult) -> Tuple[bool, str]:
        """Add lab result to patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(lab_result, LabResult):
            return False, "Error: Invalid lab result object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.add_lab_result(lab_result)
    
    def edit_lab_result(self, patient_id: int, lab_result_id: int, updated_result: LabResult) -> Tuple[bool, str]:
        """Edit lab result in patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(lab_result_id, int) or lab_result_id <= 0:
            return False, "Error: Lab result ID must be a positive integer"
        if not isinstance(updated_result, LabResult):
            return False, "Error: Invalid lab result object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.update_lab_result(lab_result_id, updated_result)
    
    def delete_lab_result(self, patient_id: int, lab_result_id: int) -> Tuple[bool, str]:
        """Delete lab result from patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(lab_result_id, int) or lab_result_id <= 0:
            return False, "Error: Lab result ID must be a positive integer"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_lab_result(lab_result_id)
    
    # Prescription Management
    def add_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        """Add prescription to a patient with validation."""
        if not isinstance(prescription, Prescription):
            return False, "Error: Invalid prescription object"
            
        result = self._system_service.verify_prescription(prescription)
        if not result[0]:
            self._invalid_prescriptions.append(prescription)
        return result
    
    def edit_prescription(self, patient_id: int, prescription_id: int, updated_prescription: Prescription) -> Tuple[bool, str]:
        """Edit prescription in patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return False, "Error: Prescription ID must be a positive integer"
        if not isinstance(updated_prescription, Prescription):
            return False, "Error: Invalid prescription object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.update_prescription(prescription_id, updated_prescription)
    
    def delete_prescription(self, patient_id: int, prescription_id: int) -> Tuple[bool, str]:
        """Delete prescription from patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return False, "Error: Prescription ID must be a positive integer"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_prescription(prescription_id)
        
    # Treatment Management
    def add_treatment(self, patient_id: int, treatment: Treatment) -> Tuple[bool, str]:
        """Add treatment to patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(treatment, Treatment):
            return False, "Error: Invalid treatment object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.add_treatment(treatment)
    
    def edit_treatment(self, patient_id: int, treatment_id: int, updated_treatment: Treatment) -> Tuple[bool, str]:
        """Edit treatment in patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return False, "Error: Treatment ID must be a positive integer"
        if not isinstance(updated_treatment, Treatment):
            return False, "Error: Invalid treatment object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.update_treatment(treatment_id, updated_treatment)
    
    def delete_treatment(self, patient_id: int, treatment_id: int) -> Tuple[bool, str]:
        """Delete treatment from patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return False, "Error: Treatment ID must be a positive integer"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_treatment(treatment_id)
        
    def view_lab_results(self, patient_id: int) -> Optional[List[LabResult]]:
        """View laboratory results for a specific patient with validation."""
        if not isinstance(patient_id, int) or patient_id <= 0:
            return None
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return None
        return patient.get_lab_results()
    
    def add_medication(self, patient_id: int, medication: Medication) -> Tuple[bool, str]:
        """Add medication to a patient's record with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(medication, Medication):
            return False, "Error: Invalid medication object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Unable to find patient with specified id"
        return patient.add_medication(medication)
    
    def get_invalid_prescriptions(self) -> List[Prescription]:
        """Get a list of prescriptions that failed validation."""
        return self._invalid_prescriptions.copy()  # Return a copy to prevent external modification