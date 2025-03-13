import unittest
from datetime import date, time
from unittest.mock import Mock, MagicMock

from backend.modules.receptionist import Receptionist
from backend.modules.appointment import Appointment
from backend.modules.fee import Fee
from backend.modules.supply import Supply

class TestReceptionist(unittest.TestCase):
    """Test suite for the Receptionist class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock system
        self.mock_system = Mock()
        
        # Create a receptionist instance for testing
        self.receptionist = Receptionist(
            name="Mary Johnson",
            username="mjohnson",
            password="secure123",
            system_service=self.mock_system
        )
        
        # Update the receptionist's system reference
        # In a real application, this would be injected through the constructor
        self.receptionist._system_service = self.mock_system
        
        # Create mock objects for testing
        self.mock_appointment = Mock(spec=Appointment)
        self.mock_appointment.id = 1
        
        self.mock_fee = Mock(spec=Fee)
        self.mock_fee.id = 1
        
        self.mock_supply = Mock(spec=Supply)
        self.mock_supply.id = 1
        
        # Create a mock patient
        self.mock_patient = Mock()
        self.mock_patient.id = 1
        
        # Configure mock system methods
        self.mock_system.get_patient_from_id.return_value = self.mock_patient
    
    def test_receptionist_initialization(self):
        """Test receptionist initialization and property access."""
        self.assertEqual(self.receptionist.name, "Mary Johnson")
        self.assertEqual(self.receptionist.username, "mjohnson")
        self.assertEqual(self.receptionist.user_type, "receptionist")
    
    def test_appointment_management(self):
        """Test appointment management functions."""
        # Configure mock system appointment methods
        self.mock_system.add_appointment.return_value = (True, "Success: Appointment added")
        self.mock_system.update_appointment.return_value = (True, "Success: Appointment updated")
        self.mock_system.delete_appointment.return_value = (True, "Success: Appointment deleted")
        
        # Test add appointment
        result, message = self.receptionist.add_appointment(self.mock_appointment)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Appointment added")
        self.mock_system.add_appointment.assert_called_with(self.mock_appointment)
        
        # Test edit appointment
        result, message = self.receptionist.edit_appointment(1, self.mock_appointment)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Appointment updated")
        self.mock_system.update_appointment.assert_called_with(1, self.mock_appointment)
        
        # Test delete appointment
        result, message = self.receptionist.delete_appointment(1)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Appointment deleted")
        self.mock_system.delete_appointment.assert_called_with(1)
    
    def test_financial_report_generation(self):
        """Test financial report generation."""
        # Configure mock system report method
        mock_report = {
            "period": "2025-01-01 to 2025-03-31",
            "total_income": 5000.0,
            "total_expenses": 3000.0,
            "net_profit": 2000.0,
            "details": {}
        }
        self.mock_system.generate_financial_report.return_value = (True, mock_report)
        
        # Test generate financial report
        result, report = self.receptionist.generate_financial_report("2025-01-01", "2025-03-31")
        self.assertTrue(result)
        self.assertEqual(report["net_profit"], 2000.0)
        self.mock_system.generate_financial_report.assert_called_with("2025-01-01", "2025-03-31")
    
    def test_fee_management(self):
        """Test fee management functions."""
        # Configure mock patient fee methods
        self.mock_patient.add_fee.return_value = (True, "Success: Fee added")
        self.mock_patient.update_fee.return_value = (True, "Success: Fee updated")
        self.mock_patient.remove_fee.return_value = (True, "Success: Fee removed")
        
        # Test add fee
        result, message = self.receptionist.add_fee(1, self.mock_fee)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Fee added")
        self.mock_patient.add_fee.assert_called_with(self.mock_fee)
        
        # Test edit fee
        result, message = self.receptionist.edit_fee(1, 1, self.mock_fee)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Fee updated")
        self.mock_patient.update_fee.assert_called_with(1, self.mock_fee)
        
        # Test delete fee
        result, message = self.receptionist.delete_fee(1, 1)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Fee removed")
        self.mock_patient.remove_fee.assert_called_with(1)
        
        # Test with invalid patient ID
        self.mock_system.get_patient_from_id.return_value = None
        result, message = self.receptionist.add_fee(999, self.mock_fee)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Patient not found")
    
    def test_supply_management(self):
        """Test supply management functions."""
        # Configure mock system supply methods
        self.mock_system.add_supply.return_value = (True, "Success: Supply added")
        self.mock_system.update_supply.return_value = (True, "Success: Supply updated")
        self.mock_system.delete_supply.return_value = (True, "Success: Supply deleted")
        
        # Test add supply
        result, message = self.receptionist.add_supply(self.mock_supply)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Supply added")
        self.mock_system.add_supply.assert_called_with(self.mock_supply)
        
        # Test edit supply
        result, message = self.receptionist.edit_supply(1, self.mock_supply)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Supply updated")
        self.mock_system.update_supply.assert_called_with(1, self.mock_supply)
        
        # Test delete supply
        result, message = self.receptionist.delete_supply(1)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Supply deleted")
        self.mock_system.delete_supply.assert_called_with(1)