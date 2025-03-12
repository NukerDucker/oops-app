from typing import List, Tuple, Optional, Callable
from .base_entity import BaseEntity
from .prescription import Prescription
from .doctor import Doctor
from .system_registry import get_system
from . import utils


class Pharmacist(BaseEntity):
    def __init__(
        self, 
        name: str, 
        surname: str, 
        password: str
    ) -> None:
        super().__init__()
        self._name = name
        self._surname = surname
        self._password = password
        self._pending_prescriptions: List[Prescription] = []
    
    @property
    def pharmacist_id(self) -> int:
        return self.id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def surname(self) -> str:
        return self._surname
    
    @property
    def pending_prescriptions(self) -> List[Prescription]:
        return self._pending_prescriptions
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        if old_password == self._password:
            self._password = new_password
            return True, "Success: Password changed"
        return False, "Error: Original password is incorrect"

    def add_prescription_for_verification(self, prescription: Prescription) -> None:
        self._pending_prescriptions.append(prescription)
        
    def view_patient_record(self, patient_id: int) -> Optional['Patient']:
        system = get_system()
        if system:
            return system.get_patient_from_id(patient_id)
        return None
        
    def send_prescription_with_feedback(self, prescription_id: int) -> Tuple[bool, str]:
        prescription_index = utils.get_object_index_in_container(
            container=self._pending_prescriptions,
            target_id=prescription_id,
            get_id=lambda obj: obj.id
        )
        
        if prescription_index == -1:
            return False, "Error: Approved prescription not in your list"
            
        prescription = self._pending_prescriptions[prescription_index]
        
        system = get_system()
        if not system:
            return False, "Error: System not available"
            
        doctor = system.get_doctor_from_id(prescription.doctor_id)
        if doctor is None:
            return False, "Error: Could not find the doctor issuing the prescription"
            
        doctor.add_disapproved_prescription(prescription)
        del self._pending_prescriptions[prescription_index]
        return True, "Success: Sent prescription feedback"
        
    def queue_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
            
        return system.queue_prescription(prescription)

    def dispense_medication(self, prescription_id: int) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
            
        return True, f"Success: Medication dispensed for prescription #{prescription_id}"