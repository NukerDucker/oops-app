from typing import List, Tuple, Optional, Dict
from .user import User
from .patient import Patient
from .appointment import Appointment
from .fee import Fee
from .supply import Supply

class Receptionist(User):
    """
    Represents a receptionist in the hospital system.
    
    Stores:
    - Name, username, password (inherited from User)
    - Reference to system service
    
    Does NOT store:
    - Patient information (stored in Patient class)
    - Appointment information (stored in Appointment class)
    - Supply inventory (stored in System class)
    - Fee details (stored in Fee class)
    """
    
    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        system_service
    ) -> None:
        """Initialize a new Receptionist with validation.
        
        Args:
            name: The receptionist's name
            username: The receptionist's username
            password: The receptionist's password
            system_service: Service for accessing system-wide operations
        """
        # Validate inputs
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
    
    # Appointment Management
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        """Add an appointment to the system with validation."""
        # Validate appointment
        if not isinstance(appointment, Appointment):
            return False, "Error: Invalid appointment object"
            
        return self._system_service.add_appointment(appointment)
    
    def edit_appointment(self, appointment_id: int, updated_appointment: Appointment) -> Tuple[bool, str]:
        """Edit an existing appointment with validation."""
        # Validate parameters
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
        if not isinstance(updated_appointment, Appointment):
            return False, "Error: Invalid appointment object"
            
        return self._system_service.update_appointment(appointment_id, updated_appointment)
    
    def delete_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        """Delete an appointment from the system with validation."""
        # Validate appointment_id
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
            
        return self._system_service.delete_appointment(appointment_id)
    
    # Financial Management
    def generate_financial_report(self, start_date: str, end_date: str) -> Tuple[bool, Dict]:
        """Generate financial report for a given period with validation."""
        # Validate date strings
        if not isinstance(start_date, str) or not start_date.strip():
            return False, {"error": "Start date must be a non-empty string"}
        if not isinstance(end_date, str) or not end_date.strip():
            return False, {"error": "End date must be a non-empty string"}
        
        # Basic date format validation (could be more sophisticated)
        date_format = True
        try:
            # Check if dates can be parsed - this is just validation, not conversion
            from datetime import datetime
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            date_format = False
            
        if not date_format:
            return False, {"error": "Dates must be in YYYY-MM-DD format"}
            
        return self._system_service.generate_financial_report(start_date, end_date)
    
    # Fee Management
    def add_fee(self, patient_id: int, fee: Fee) -> Tuple[bool, str]:
        """Add fee to patient's account with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(fee, Fee):
            return False, "Error: Invalid fee object"
            
        patient = self._system_service.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.add_fee(fee)
    
    def edit_fee(self, patient_id: int, fee_id: int, updated_fee: Fee) -> Tuple[bool, str]:
        """Edit fee in patient's account with validation."""
        # Validate parameters
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
        """Delete fee from patient's account with validation."""
        # Validate parameters
        if not isinstance(patient_id, int) or patient_id <= 0:
            return False, "Error: Patient ID must be a positive integer"
        if not isinstance(fee_id, int) or fee_id <= 0:
            return False, "Error: Fee ID must be a positive integer"
            
        patient = self._system_service.get_patient_from_id(patient_id)
        if patient is None:
            return False, "Error: Patient not found"
        return patient.remove_fee(fee_id)
    
    # Supply Management
    def add_supply(self, supply: Supply) -> Tuple[bool, str]:
        """Add supply to the inventory with validation."""
        # Validate supply
        if not isinstance(supply, Supply):
            return False, "Error: Invalid supply object"
            
        return self._system_service.add_supply(supply)
    
    def edit_supply(self, supply_id: int, updated_supply: Supply) -> Tuple[bool, str]:
        """Edit supply in the inventory with validation."""
        # Validate parameters
        if not isinstance(supply_id, int) or supply_id <= 0:
            return False, "Error: Supply ID must be a positive integer"
        if not isinstance(updated_supply, Supply):
            return False, "Error: Invalid supply object"
            
        return self._system_service.update_supply(supply_id, updated_supply)
    
    def delete_supply(self, supply_id: int) -> Tuple[bool, str]:
        """Delete supply from the inventory with validation."""
        # Validate supply_id
        if not isinstance(supply_id, int) or supply_id <= 0:
            return False, "Error: Supply ID must be a positive integer"
            
        return self._system_service.delete_supply(supply_id)
    
    def search_patients(self, search_term: str) -> List[Patient]:
        """Search for patients by name with validation."""
        # Validate search_term
        if not isinstance(search_term, str):
            return []
            
        return self._system_service.search_patients(search_term)
    
    def view_upcoming_appointments(self) -> List[Appointment]:
        """View upcoming appointments."""
        return self._system_service.get_upcoming_appointments()
    
    def mark_appointment_status(self, appointment_id: int, status: str) -> Tuple[bool, str]:
        """Update an appointment's status with validation."""
        # Validate parameters
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            return False, "Error: Appointment ID must be a positive integer"
        
        valid_statuses = ["scheduled", "completed", "cancelled", "no-show"]
        if not isinstance(status, str) or status not in valid_statuses:
            return False, f"Error: Status must be one of {valid_statuses}"
            
        return self._system_service.update_appointment_status(appointment_id, status)
