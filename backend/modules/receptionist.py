from typing import Tuple, Optional
from .base_entity import BaseEntity
from .patient import Patient
from .appointment import Appointment
from .admission import Admission
from .fee import Fee
from .payment_method import PaymentMethod
from .system_registry import get_system

class Receptionist(BaseEntity):
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

    @property
    def receptionist_id(self) -> int:
        return self.id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def surname(self) -> str:
        return self._surname
        
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        if self._password == old_password:
            self._password = new_password
            return True, "Success: Password changed"
        return False, "Error: Incorrect old password" 
    
    def register_patient(self, patient: Patient) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.add_patient(patient)
        
    def update_patient_record(
        self, 
        patient_to_edit: Patient, 
        updated_patient: Patient
    ) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.edit_patient(patient_to_edit_to=patient_to_edit, overwrite_as=updated_patient)
        
    def delete_patient(self, patient_id: int) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.deletePatient(patient_id)
        
    def search_for_patient_info(self, search_term: str) -> Optional[Patient]:
        system = get_system()
        if not system:
            return None
        return system.search_patients(search_term)

    def schedule_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.add_appointment(appointment)

    def cancel_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.removeAppointment(appointment_id)
    
    def admit_patient(self, admission: Admission) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.add_admission(admission)

    def discharge_patient(self, patient_id: int) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.removeAdmission(patient_id)
    
    def handle_patient_fee_payment(
        self, 
        fee: Fee, 
        payment_method: PaymentMethod
    ) -> Tuple[bool, str]:
        system = get_system()
        if not system:
            return False, "Error: System not available"
        return system.pay_fee(fee=fee, payment_method=payment_method)
