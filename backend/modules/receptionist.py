from typing import List, Tuple, Optional, Dict
from .user import User
from .patient import Patient
from .appointment import Appointment
from .fee import Fee
from .supply import Supply

class Receptionist(User):
    
    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        system_service
    ) -> None:
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password must be a non-empty string")
        if system_service is None:
            raise ValueError("System service cannot be None")
            
        super().__init__(name, username, password, "receptionist")
        self._system_service = system_service
    
    
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        
        if not isinstance(appointment, Appointment):
            return False, "Error: Invalid appointment object"
            
        return self._system_service.add_appointment(appointment)
    
    def edit_appointment(self, appointment_id: int, updated_appointment: Appointment) -> Tuple[bool, str]:
        
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
        if not isinstance(updated_appointment, Appointment):
            return False, "Error: Invalid appointment object"
            
        return self._system_service.update_appointment(appointment_id, updated_appointment)
    
    def delete_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
            
        return self._system_service.delete_appointment(appointment_id)
    
    
    def generate_financial_report(self, start_date: str, end_date: str) -> Tuple[bool, Dict]:
        
        if not isinstance(start_date, str) or not start_date.strip():
            return False, {"error": "Start date must be a non-empty string"}
        if not isinstance(end_date, str) or not end_date.strip():
            return False, {"error": "End date must be a non-empty string"}
        
        
        date_format = True
        try:
            
            from datetime import datetime
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            date_format = False
            
        if not date_format:
            return False, {"error": "Dates must be in YYYY-MM-DD format"}
            
        return self._system_service.generate_financial_report(start_date, end_date)
    
    
    def add_fee(self, patient_id: int, fee: Fee) -> Tuple[bool, str]:
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(fee, Fee):
            return False, "Error: Invalid fee object"
            
        patient = self._system_service.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.add_fee(fee)
    
    def edit_fee(self, patient_id: int, fee_id: int, updated_fee: Fee) -> Tuple[bool, str]:
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(fee_id, int) or fee_id <= 0:
            return False, "Error: Fee ID must be a positive integer"
        if not isinstance(updated_fee, Fee):
            return False, "Error: Invalid fee object"
            
        patient = self._system_service.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.update_fee(fee_id, updated_fee)
    
    def delete_fee(self, patient_id: int, fee_id: int) -> Tuple[bool, str]:
        
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(fee_id, int) or fee_id <= 0:
            return False, "Error: Fee ID must be a positive integer"
            
        patient = self._system_service.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_fee(fee_id)
    
    
    def add_supply(self, supply: Supply) -> Tuple[bool, str]:
        
        if not isinstance(supply, Supply):
            return False, "Error: Invalid supply object"
            
        return self._system_service.add_supply(supply)
    
    def edit_supply(self, supply_id: int, updated_supply: Supply) -> Tuple[bool, str]:
        
        if not isinstance(supply_id, int) or supply_id <= 0:
            return False, "Error: Supply ID must be a positive integer"
        if not isinstance(updated_supply, Supply):
            return False, "Error: Invalid supply object"
            
        return self._system_service.update_supply(supply_id, updated_supply)
    
    def delete_supply(self, supply_id: int) -> Tuple[bool, str]:
        
        if not isinstance(supply_id, int) or supply_id <= 0:
            return False, "Error: Supply ID must be a positive integer"
            
        return self._system_service.delete_supply(supply_id)
    
    def search_patients(self, search_term: str) -> List[Patient]:
        
        if not isinstance(search_term, str):
            return []
            
        return self._system_service.search_patients(search_term)
    
    def view_upcoming_appointments(self) -> List[Appointment]:
        return self._system_service.get_upcoming_appointments()
    
    def mark_appointment_status(self, appointment_id: int, status: str) -> Tuple[bool, str]:
        
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
        
        valid_statuses = ["scheduled", "completed", "cancelled", "no-show"]
        if not isinstance(status, str) or status not in valid_statuses:
            return False, f"Error: Status must be one of {valid_statuses}"
            
        return self._system_service.update_appointment_status(appointment_id, status)
