import unittest
from datetime import date, time
import sys
import os
from unittest.mock import Mock, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.modules.receptionist import Receptionist
from backend.modules.appointment import Appointment
from backend.modules.patient import Patient
from backend.modules.fee import Fee
from backend.modules.supply import Supply

class TestReceptionist(unittest.TestCase):
    """Test cases for the Receptionist class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock system service
        self.mock_system = MagicMock()
        
        # Create a receptionist with the mock service
        self.receptionist = Receptionist(
            "Jane Doe",
            "janedoe",
            "password123",
            self.mock_system
        )
        
        # Create test data
        self.today = date.today()
        
        # Mock patient
        self.patient = MagicMock(spec=Patient)
        self.patient.id = 1
        self.patient.name = "John Smith"
        
        # Mock appointment
        self.appointment = MagicMock(spec=Appointment)
        self.appointment.id = 1
        self.appointment.patient_id = self.patient.id
        self.appointment.date = self.today
        self.appointment.time = time(10, 0)
        
        # Mock fee
        self.fee = MagicMock(spec=Fee)
        self.fee.id = 1
        self.fee.patient_id = self.patient.id
        self.fee.amount = 100.00
        self.fee.fee_type = "doctor"
        
        # Mock supply
        self.supply = MagicMock(spec=Supply)
        self.supply.id = 1
        self.supply.name = "Surgical Gloves"
        self.supply.quantity = 100
        
        # Configure the mock system
        self.mock_system.get_patient_from_id.return_value = self.patient
        self.patient.add_fee.return_value = (True, "Success: Fee added")
        self.patient.update_fee.return_value = (True, "Success: Fee updated")
        self.patient.remove_fee.return_value = (True, "Success: Fee removed")
    
    def test_constructor_validation(self):
        """Test constructor validation."""
        # Test with invalid name
        with self.assertRaises(ValueError):
            Receptionist("", "username", "password", self.mock_system)
        
        # Test with invalid username
        with self.assertRaises(ValueError):
            Receptionist("Name", "", "password", self.mock_system)
        
        # Test with invalid password
        with self.assertRaises(ValueError):
            Receptionist("Name", "username", "", self.mock_system)
        
        # Test with None system_service
        with self.assertRaises(ValueError):
            Receptionist("Name", "username", "password", None)
    
    def test_add_appointment(self):
        """Test adding an appointment."""
        # Configure mock
        self.mock_system.add_appointment.return_value = (True, "Success: Appointment added")
        
        # Test with valid appointment
        result, message = self.receptionist.add_appointment(self.appointment)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.add_appointment.assert_called_once_with(self.appointment)
        
        # Test with invalid appointment
        result, message = self.receptionist.add_appointment("not an appointment")
        self.assertFalse(result)
        self.assertIn("Error", message)
        # Mock should still have been called only once
        self.mock_system.add_appointment.assert_called_once()
    
    def test_edit_appointment(self):
        """Test editing an appointment."""
        # Configure mock
        self.mock_system.update_appointment.return_value = (True, "Success: Appointment updated")
        
        # Test with valid parameters
        result, message = self.receptionist.edit_appointment(1, self.appointment)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.update_appointment.assert_called_once_with(1, self.appointment)
        
        # Reset mock
        self.mock_system.update_appointment.reset_mock()
        
        # Test with invalid appointment ID
        result, message = self.receptionist.edit_appointment(0, self.appointment)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_appointment.assert_not_called()
        
        # Test with invalid appointment object
        result, message = self.receptionist.edit_appointment(1, "not an appointment")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_appointment.assert_not_called()
    
    def test_delete_appointment(self):
        """Test deleting an appointment."""
        # Configure mock
        self.mock_system.delete_appointment.return_value = (True, "Success: Appointment deleted")
        
        # Test with valid ID
        result, message = self.receptionist.delete_appointment(1)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.delete_appointment.assert_called_once_with(1)
        
        # Reset mock
        self.mock_system.delete_appointment.reset_mock()
        
        # Test with invalid ID
        result, message = self.receptionist.delete_appointment(0)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.delete_appointment.assert_not_called()
    
    def test_generate_financial_report(self):
        """Test generating a financial report."""
        mock_report = {"total_income": 1000, "total_expenses": 500, "net_profit": 500}
        self.mock_system.generate_financial_report.return_value = (True, mock_report)
        
        # Test with valid dates
        result, report = self.receptionist.generate_financial_report("2024-01-01", "2024-01-31")
        self.assertTrue(result)
        self.assertEqual(report, mock_report)
        self.mock_system.generate_financial_report.assert_called_once_with("2024-01-01", "2024-01-31")
        
        # Reset mock
        self.mock_system.generate_financial_report.reset_mock()
        
        # Test with invalid start date
        result, report = self.receptionist.generate_financial_report("", "2024-01-31")
        self.assertFalse(result)
        self.assertIn("error", report)
        self.mock_system.generate_financial_report.assert_not_called()
        
        # Test with invalid end date
        result, report = self.receptionist.generate_financial_report("2024-01-01", "")
        self.assertFalse(result)
        self.assertIn("error", report)
        self.mock_system.generate_financial_report.assert_not_called()
        
        # Test with invalid date format
        result, report = self.receptionist.generate_financial_report("01/01/2024", "31/01/2024")
        self.assertFalse(result)
        self.assertIn("error", report)
        self.mock_system.generate_financial_report.assert_not_called()
    
    def test_add_fee(self):
        """Test adding a fee to a patient."""
        # Test with valid parameters
        result, message = self.receptionist.add_fee(1, self.fee)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(1)
        self.patient.add_fee.assert_called_once_with(self.fee)
        
        # Reset mocks
        self.mock_system.get_patient_from_id.reset_mock()
        self.patient.add_fee.reset_mock()
        
        # Test with invalid patient ID
        result, message = self.receptionist.add_fee(0, self.fee)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.add_fee.assert_not_called()
        
        # Test with invalid fee object
        result, message = self.receptionist.add_fee(1, "not a fee")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.add_fee.assert_not_called()
        
        # Test with non-existent patient
        self.mock_system.get_patient_from_id.return_value = None
        result, message = self.receptionist.add_fee(999, self.fee)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(999)
        self.patient.add_fee.assert_not_called()
    
    def test_edit_fee(self):
        """Test editing a fee."""
        # Test with valid parameters
        result, message = self.receptionist.edit_fee(1, 1, self.fee)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(1)
        self.patient.update_fee.assert_called_once_with(1, self.fee)
        
        # Reset mocks
        self.mock_system.get_patient_from_id.reset_mock()
        self.patient.update_fee.reset_mock()
        
        # Test with invalid patient ID
        result, message = self.receptionist.edit_fee(0, 1, self.fee)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.update_fee.assert_not_called()
        
        # Test with invalid fee ID
        result, message = self.receptionist.edit_fee(1, 0, self.fee)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.update_fee.assert_not_called()
        
        # Test with invalid fee object
        result, message = self.receptionist.edit_fee(1, 1, "not a fee")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.update_fee.assert_not_called()
        
        # Test with non-existent patient
        self.mock_system.get_patient_from_id.return_value = None
        result, message = self.receptionist.edit_fee(999, 1, self.fee)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(999)
        self.patient.update_fee.assert_not_called()
    
    def test_delete_fee(self):
        """Test deleting a fee."""
        # Test with valid parameters
        result, message = self.receptionist.delete_fee(1, 1)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(1)
        self.patient.remove_fee.assert_called_once_with(1)
        
        # Reset mocks
        self.mock_system.get_patient_from_id.reset_mock()
        self.patient.remove_fee.reset_mock()
        
        # Test with invalid patient ID
        result, message = self.receptionist.delete_fee(0, 1)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.remove_fee.assert_not_called()
        
        # Test with invalid fee ID
        result, message = self.receptionist.delete_fee(1, 0)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_not_called()
        self.patient.remove_fee.assert_not_called()
        
        # Test with non-existent patient
        self.mock_system.get_patient_from_id.return_value = None
        result, message = self.receptionist.delete_fee(999, 1)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.get_patient_from_id.assert_called_once_with(999)
        self.patient.remove_fee.assert_not_called()
    
    def test_add_supply(self):
        """Test adding a supply to inventory."""
        # Configure mock
        self.mock_system.add_supply.return_value = (True, "Success: Supply added")
        
        # Test with valid supply
        result, message = self.receptionist.add_supply(self.supply)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.add_supply.assert_called_once_with(self.supply)
        
        # Reset mock
        self.mock_system.add_supply.reset_mock()
        
        # Test with invalid supply
        result, message = self.receptionist.add_supply("not a supply")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.add_supply.assert_not_called()
    
    def test_edit_supply(self):
        """Test editing a supply."""
        # Configure mock
        self.mock_system.update_supply.return_value = (True, "Success: Supply updated")
        
        # Test with valid parameters
        result, message = self.receptionist.edit_supply(1, self.supply)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.update_supply.assert_called_once_with(1, self.supply)
        
        # Reset mock
        self.mock_system.update_supply.reset_mock()
        
        # Test with invalid supply ID
        result, message = self.receptionist.edit_supply(0, self.supply)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_supply.assert_not_called()
        
        # Test with invalid supply object
        result, message = self.receptionist.edit_supply(1, "not a supply")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_supply.assert_not_called()
    
    def test_delete_supply(self):
        """Test deleting a supply."""
        # Configure mock
        self.mock_system.delete_supply.return_value = (True, "Success: Supply deleted")
        
        # Test with valid ID
        result, message = self.receptionist.delete_supply(1)
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.delete_supply.assert_called_once_with(1)
        
        # Reset mock
        self.mock_system.delete_supply.reset_mock()
        
        # Test with invalid ID
        result, message = self.receptionist.delete_supply(0)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.delete_supply.assert_not_called()
    
    def test_search_patients(self):
        """Test searching for patients."""
        # Create mock patient list
        mock_patients = [self.patient]
        self.mock_system.search_patients.return_value = mock_patients
        
        # Test with valid search term
        result = self.receptionist.search_patients("Smith")
        self.assertEqual(result, mock_patients)
        self.mock_system.search_patients.assert_called_once_with("Smith")
        
        # Reset mock
        self.mock_system.search_patients.reset_mock()
        
        # Test with invalid search term
        result = self.receptionist.search_patients(123)
        self.assertEqual(result, [])
        self.mock_system.search_patients.assert_not_called()
    
    def test_view_upcoming_appointments(self):
        """Test viewing upcoming appointments."""
        # Create mock appointment list
        mock_appointments = [self.appointment]
        self.mock_system.get_upcoming_appointments.return_value = mock_appointments
        
        # Test method
        result = self.receptionist.view_upcoming_appointments()
        self.assertEqual(result, mock_appointments)
        self.mock_system.get_upcoming_appointments.assert_called_once()
    
    def test_mark_appointment_status(self):
        """Test marking appointment status."""
        # Configure mock
        self.mock_system.update_appointment_status.return_value = (True, "Success: Status updated")
        
        # Test with valid parameters
        result, message = self.receptionist.mark_appointment_status(1, "completed")
        self.assertTrue(result)
        self.assertIn("Success", message)
        self.mock_system.update_appointment_status.assert_called_once_with(1, "completed")
        
        # Reset mock
        self.mock_system.update_appointment_status.reset_mock()
        
        # Test with invalid appointment ID
        result, message = self.receptionist.mark_appointment_status(0, "completed")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_appointment_status.assert_not_called()
        
        # Test with invalid status
        result, message = self.receptionist.mark_appointment_status(1, "invalid_status")
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_appointment_status.assert_not_called()

if __name__ == "__main__":
    unittest.main()