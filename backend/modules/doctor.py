from typing import List, Tuple, Optional
from .base_entity import BaseEntity
from .appointment import Appointment
from .patient import Patient
from .lab_request import LabRequest
from .lab_result import LabResult
from .prescription import Prescription
from .medication import Medication

# Import the global system, but ideally this should be dependency injected
import globals

class Doctor(BaseEntity):
    """Represents a doctor in the hospital system."""
    
    def __init__(
        self, 
        name: str, 
        surname: str, 
        speciality: str, 
        password: str
    ) -> None:
        """Initialize a new Doctor.
        
        Args:
            name: The doctor's first name
            surname: The doctor's last name
            speciality: The doctor's medical speciality
            password: The doctor's password for system access
        """
        super().__init__()  # Generate the unique ID using the base class
        self._name = name
        self._surname = surname
        self._speciality = speciality
        self._password = password
        self._invalid_prescriptions: List[Prescription] = []
    
    @property
    def doctor_id(self) -> int:
        """Get the doctor's unique identifier."""
        return self.id
    
    @property
    def name(self) -> str:
        """Get the doctor's first name."""
        return self._name
    
    @property
    def surname(self) -> str:
        """Get the doctor's last name."""
        return self._surname
    
    @property
    def speciality(self) -> str:
        """Get the doctor's medical speciality."""
        return self._speciality
    
    @property
    def password(self) -> str:
        """Get the doctor's password (should only be used for authentication)."""
        return self._password
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change the doctor's password.
        
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
    
    def view_patient_record(self, patient_id: int) -> Optional[Patient]:
        """Retrieve a patient's record.
        
        Args:
            patient_id: The ID of the patient
            
        Returns:
            The Patient object if found, None otherwise
        """
        return globals.system.get_patient_from_id(patient_id)

    def schedule_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        """Schedule a new appointment.
        
        Args:
            appointment: The appointment to schedule
            
        Returns:
            A tuple of (success, message)
        """
        appointment.doctor_id = self.id
        return globals.system.add_appointment(appointment)

    def prescribe_medicine(self, prescription: Prescription) -> Tuple[bool, str]:
        """Prescribe medicine to a patient.
        
        Args:
            prescription: The prescription details
            
        Returns:
            A tuple of (success, message)
        """
        return globals.system.verify_prescription(prescription)
    
    def add_disapproved_prescription(self, prescription: Prescription) -> None:
        """Add a prescription to the disapproved list.
        
        Args:
            prescription: The rejected prescription
        """
        self._invalid_prescriptions.append(prescription)
        
    def add_admission(self, admission) -> Tuple[bool, str]:
        """Add a patient admission record.
        
        Args:
            admission: The admission record to add
            
        Returns:
            A tuple of (success, message)
        """
        return globals.system.add_admission(admission)
    
    def remove_admission(self, patient_id: int) -> Tuple[bool, str]:
        """Remove a patient's admission record.
        
        Args:
            patient_id: The ID of the patient
            
        Returns:
            A tuple of (success, message)
        """
        return globals.system.removeAdmission(patient_id)
        
    def add_medication(self, patient_id: int, medication: Medication) -> Tuple[bool, str]:
        """Add medication to a patient's record.
        
        Args:
            patient_id: The ID of the patient
            medication: The medication to add
            
        Returns:
            A tuple of (success, message)
        """
        patient: Optional[Patient] = globals.system.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Unable to find patient with specified id"
        patient.add_medication(medication)
        return True, "Success: Added medication to patient"
        
    def order_lab_test(self, lab_request: LabRequest, lab_personnel_id: int) -> Tuple[bool, str]:
        """Order a laboratory test for a patient.
        
        Args:
            lab_request: The laboratory request details
            lab_personnel_id: The ID of the lab personnel assigned
            
        Returns:
            A tuple of (success, message)
        """
        return globals.system.order_lab_test(lab_request=lab_request, lab_personnel_id=lab_personnel_id)
        
    def view_lab_results(self, patient_id: int) -> Optional[List[LabResult]]:
        """View laboratory results for a specific patient.
        
        Args:
            patient_id: The ID of the patient
            
        Returns:
            A list of lab results for the patient, or None if patient not found
        """
        patient: Optional[Patient] = globals.system.get_patient_from_id(patient_id)
        if patient is None:
            return None
        return patient.get_lab_results()