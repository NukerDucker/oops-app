from typing import Dict, List, Tuple, Optional, Any
from .user import User
from .doctor import Doctor
from .receptionist import Receptionist
from .patient import Patient
from .appointment import Appointment
from .prescription import Prescription
from .supply import Supply

class System:
    """Central management system for the clinic."""
    
    def __init__(self):
        """Initialize the system with empty collections."""
        self._users: Dict[int, User] = {}  # All system users
        self._patients: Dict[int, Patient] = {}
        self._appointments: Dict[int, Appointment] = {}
        self._supplies: Dict[int, Supply] = {}
        self._lab_requests: Dict[int, LabRequest] = {}

    # User Management
    def add_user(self, user: User) -> Tuple[bool, str]:
        """Add a new user to the system."""
        if user.id in self._users:
            return False, "Error: User ID already exists"
        self._users[user.id] = user
        return True, f"Success: Added {user.user_type} to system"
    
    def edit_user(self, user_id: int, updated_user: User) -> Tuple[bool, str]:
        """Edit a user in the system."""
        if user_id not in self._users:
            return False, "Error: User not found"
        if user_id != updated_user.id:
            return False, "Error: Cannot change user ID"
        self._users[user_id] = updated_user
        return True, "Success: User updated"
    
    def remove_user(self, user_id: int) -> Tuple[bool, str]:
        """Remove a user from the system."""
        if user_id not in self._users:
            return False, "Error: User not found"
        del self._users[user_id]
        return True, "Success: User removed"
    
    def change_user_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change a user's password."""
        if user_id not in self._users:
            return False, "Error: User not found"
        return self._users[user_id].change_password(old_password, new_password)
    
    # Patient Management
    def add_patient(self, patient: Patient) -> Tuple[bool, str]:
        """Add a new patient to the system."""
        if patient.id in self._patients:
            return False, "Error: Patient ID already exists"
        self._patients[patient.id] = patient
        return True, "Success: Patient added"
    
    def get_patient_from_id(self, patient_id: int) -> Optional[Patient]:
        """Get a patient by ID."""
        return self._patients.get(patient_id)
    
    # Appointment Management
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        """Add an appointment to the system."""
        if appointment.id in self._appointments:
            return False, "Error: Appointment ID already exists"
        self._appointments[appointment.id] = appointment
        return True, "Success: Appointment added"
    
    def update_appointment(self, appointment_id: int, updated_appointment: Appointment) -> Tuple[bool, str]:
        """Update an existing appointment."""
        if appointment_id not in self._appointments:
            return False, "Error: Appointment not found"
        if appointment_id != updated_appointment.id:
            return False, "Error: Cannot change appointment ID"
        self._appointments[appointment_id] = updated_appointment
        return True, "Success: Appointment updated"
    
    def delete_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        """Delete an appointment from the system."""
        if appointment_id not in self._appointments:
            return False, "Error: Appointment not found"
        del self._appointments[appointment_id]
        return True, "Success: Appointment deleted"
    
    # Prescription Management
    def verify_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        """Verify a prescription."""
        # In a real system, this would have more verification logic
        patient = self.get_patient_from_id(prescription.patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        patient.add_prescription(prescription)
        return True, "Success: Prescription verified and added"
    
    # Supply Management
    def add_supply(self, supply: Supply) -> Tuple[bool, str]:
        """Add supply to the inventory."""
        if supply.id in self._supplies:
            return False, "Error: Supply ID already exists"
        self._supplies[supply.id] = supply
        return True, "Success: Supply added"
    
    def update_supply(self, supply_id: int, updated_supply: Supply) -> Tuple[bool, str]:
        """Update supply in the inventory."""
        if supply_id not in self._supplies:
            return False, "Error: Supply not found"
        if supply_id != updated_supply.id:
            return False, "Error: Cannot change supply ID"
        self._supplies[supply_id] = updated_supply
        return True, "Success: Supply updated"
    
    def delete_supply(self, supply_id: int) -> Tuple[bool, str]:
        """Delete supply from the inventory."""
        if supply_id not in self._supplies:
            return False, "Error: Supply not found"
        del self._supplies[supply_id]
        return True, "Success: Supply deleted"
    
    # Financial Reporting
    def generate_financial_report(self, start_date: str, end_date: str) -> Tuple[bool, Dict[str, Any]]:
        """Generate financial report for a period."""
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
        
        # In a real system, you would collect and calculate real data here
        
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