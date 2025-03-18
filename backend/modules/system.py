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
        self._lab_requests: Dict[int, LabRequest] = {}

    
    def add_user(self, user: User) -> Tuple[bool, str]:
        if user.id in self._users:
            return False, "Error: User ID already exists"
        self._users[user.id] = user
        return True, f"Success: Added {user.user_type} to system"
    
    def edit_user(self, user_id: int, updated_user: User) -> Tuple[bool, str]:
        if user_id not in self._users:
            return False, "Error: User not found"
        if user_id != updated_user.id:
            return False, "Error: Cannot change user ID"
        self._users[user_id] = updated_user
        return True, "Success: User updated"
    
    def remove_user(self, user_id: int) -> Tuple[bool, str]:
        if user_id not in self._users:
            return False, "Error: User not found"
        del self._users[user_id]
        return True, "Success: User removed"
    
    def change_user_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        if user_id not in self._users:
            return False, "Error: User not found"
        return self._users[user_id].change_password(old_password, new_password)
    
    
    def add_patient(self, patient: Patient) -> Tuple[bool, str]:
        if patient.id in self._patients:
            return False, "Error: Patient ID already exists"
        self._patients[patient.id] = patient
        return True, "Success: Patient added"
    
    def get_patient_from_id(self, patient_id: int) -> Optional[Patient]:
        return self._patients.get(patient_id)
    
    
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        if appointment.id in self._appointments:
            return False, "Error: Appointment ID already exists"
        self._appointments[appointment.id] = appointment
        return True, "Success: Appointment added"
    
    def update_appointment(self, appointment_id: int, updated_appointment: Appointment) -> Tuple[bool, str]:
        if appointment_id not in self._appointments:
            return False, "Error: Appointment not found"
        if appointment_id != updated_appointment.id:
            return False, "Error: Cannot change appointment ID"
        self._appointments[appointment_id] = updated_appointment
        return True, "Success: Appointment updated"
    
    def delete_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        if appointment_id not in self._appointments:
            return False, "Error: Appointment not found"
        del self._appointments[appointment_id]
        return True, "Success: Appointment deleted"
    
    
    def verify_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        
        patient = self.get_patient_from_id(prescription.patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        patient.add_prescription(prescription)
        return True, "Success: Prescription verified and added"
    
    
    def add_supply(self, supply: Supply) -> Tuple[bool, str]:
        if supply.id in self._supplies:
            return False, "Error: Supply ID already exists"
        self._supplies[supply.id] = supply
        return True, "Success: Supply added"
    
    def update_supply(self, supply_id: int, updated_supply: Supply) -> Tuple[bool, str]:
        if supply_id not in self._supplies:
            return False, "Error: Supply not found"
        if supply_id != updated_supply.id:
            return False, "Error: Cannot change supply ID"
        self._supplies[supply_id] = updated_supply
        return True, "Success: Supply updated"
    
    def delete_supply(self, supply_id: int) -> Tuple[bool, str]:
        if supply_id not in self._supplies:
            return False, "Error: Supply not found"
        del self._supplies[supply_id]
        return True, "Success: Supply deleted"
    
    
    def generate_financial_report(self, start_date: str, end_date: str) -> Tuple[bool, Dict[str, Any]]:
        report = {
            "period": f"{start_date} to {end_date}",
            "total_income": 0,
            "total_expenses": 0,
            "net_profit": 0,
            "details": {
                "doctor_fees": 0,
                "medication_fees": 0,
                "lab_fees": 0,
                "other_income": 0,
                "supply_expenses": 0,
                "salary_expenses": 0,
                "other_expenses": 0
            }
        }
        
        
        
        report["total_income"] = sum([
            report["details"]["doctor_fees"], 
            report["details"]["medication_fees"], 
            report["details"]["lab_fees"], 
            report["details"]["other_income"]
        ])
        
        report["total_expenses"] = sum([
            report["details"]["supply_expenses"], 
            report["details"]["salary_expenses"], 
            report["details"]["other_expenses"]
        ])
        
        report["net_profit"] = report["total_income"] - report["total_expenses"]
        
        return True, report
