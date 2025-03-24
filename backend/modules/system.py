from typing import Dict, List, Tuple, Optional, Any
from .user import User
from .doctor import Doctor
from .receptionist import Receptionist
from .patient import Patient
from .appointment import Appointment
from .prescription import Prescription
from .supply import Supply

class System:
    
    def __init__(self):
        self._users: Dict[int, User] = {}  
        self._patients: Dict[int, Patient] = {}
        self._appointments: Dict[int, Appointment] = {}
        self._supplies: Dict[int, Supply] = {}
        
    def get_user_from_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def add_user(self, user: User) -> Tuple[bool, str]:
        if user.id in self._users:
            return False, "User ID already exists"
        self._users[user.id] = user
        return True, "User added successfully"
    
    def edit_user(self, user_id: int, updated_user: User) -> Tuple[bool, str]:
        if user_id not in self._users:
            return False, "User not found"
        if user_id != updated_user.id:
            return False, "Cannot change user ID"
        self._users[user_id] = updated_user
        return True, "User updated successfully"
    
    def remove_user(self, user_id: int) -> Tuple[bool, str]:
        if user_id not in self._users:
            return False, "User not found"
        del self._users[user_id]
        return True, "User removed successfully"
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def add_patient(self, patient: Patient) -> Tuple[bool, str]:
        if patient.id in self._patients:
            return False, "Patient ID already exists"
        self._patients[patient.id] = patient
        return True, "Patient added successfully"
    
    def update_patient(self, patient_id: int, updated_patient: Patient) -> Tuple[bool, str]:
        if patient_id not in self._patients:
            return False, "Patient not found"
        if patient_id != updated_patient.id:
            return False, "Cannot change patient ID"
        self._patients[patient_id] = updated_patient
        return True, "Patient updated successfully"
    
    def get_patient_from_id(self, patient_id: int) -> Optional[Patient]:
        return self._patients.get(patient_id)
    
    def get_appointments(self, user: User) -> List[Appointment]:
        if user.user_type == "doctor":
            return [a for a in self._appointments.values() if a.doctor_id == user.id]
        return []
    
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        if appointment.id in self._appointments:
            return False, "Appointment ID already exists"
        self._appointments[appointment.id] = appointment
        return True, "Appointment added successfully"
    
    def update_appointment(self, appointment_id: int, updated_appointment: Appointment) -> Tuple[bool, str]:
        if appointment_id not in self._appointments:
            return False, "Appointment not found"
        if appointment_id != updated_appointment.id:
            return False, "Cannot change appointment ID"
        self._appointments[appointment_id] = updated_appointment
        return True, "Appointment updated successfully"
    
    def delete_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        if appointment_id not in self._appointments:
            return False, "Appointment not found"
        del self._appointments[appointment_id]
        return True, "Appointment deleted successfully"
    
    def verify_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        # Implementation based on business rules
        return True, "Prescription verified"
    
    def add_supply(self, supply: Supply) -> Tuple[bool, str]:
        if supply.id in self._supplies:
            return False, "Supply ID already exists"
        self._supplies[supply.id] = supply
        return True, "Supply added successfully"
    
    def update_supply(self, supply_id: int, updated_supply: Supply) -> Tuple[bool, str]:
        if supply_id not in self._supplies:
            return False, "Supply not found"
        if supply_id != updated_supply.id:
            return False, "Cannot change supply ID"
        self._supplies[supply_id] = updated_supply
        return True, "Supply updated successfully"
    
    def delete_supply(self, supply_id: int) -> Tuple[bool, str]:
        if supply_id not in self._supplies:
            return False, "Supply not found"
        del self._supplies[supply_id]
        return True, "Supply deleted successfully"