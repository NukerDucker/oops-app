from typing import List, Tuple, Optional
from .user import User
from .patient import Patient
from .appointment import Appointment
from .prescription import Prescription
from .medication import Medication
from .treatment import Treatment

class Doctor(User):
    
    def __init__(
        self, 
        name: str,
        username: str,
        password: str,
        system_service
    ) -> None:
        super().__init__(name, username, password, "doctor")
        self._system_service = system_service
    
    @property
    def doctor_id(self) -> int:
        return self.id
    
    def view_patient_record(self, patient_id: int) -> Optional[Patient]:
        if not isinstance(patient_id, int) or patient_id <= 0:
            return None
        return self._system_service.get_patient_from_id(patient_id)
    
    def add_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        if not isinstance(prescription, Prescription):
            return False, "Error: Invalid prescription object"
            
        result = self._system_service.verify_prescription(prescription)
        if not result[0]:
            self._invalid_prescriptions.append(prescription)
        return result
    
    def edit_prescription(self, patient_id: int, prescription_id: int, updated_prescription: Prescription) -> Tuple[bool, str]:
        
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
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return False, "Error: Prescription ID must be a positive integer"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_prescription(prescription_id)
        
    
    def add_treatment(self, patient_id: int, treatment: Treatment) -> Tuple[bool, str]:
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(treatment, Treatment):
            return False, "Error: Invalid treatment object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.add_treatment(treatment)
    
    def edit_treatment(self, patient_id: int, treatment_id: int, updated_treatment: Treatment) -> Tuple[bool, str]:
        
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
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return False, "Error: Treatment ID must be a positive integer"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_treatment(treatment_id)
    
    def add_medication(self, patient_id: int, medication: Medication) -> Tuple[bool, str]:
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(medication, Medication):
            return False, "Error: Invalid medication object"
            
        patient = self.view_patient_record(patient_id)
        if patient is None:
            return False, "Error: Unable to find patient with specified id"
        return patient.add_medication(medication)
    
