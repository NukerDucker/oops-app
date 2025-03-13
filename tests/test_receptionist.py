import unittest        # Create test data        self.today = date.today()                # Mock patient
from datetime import date, time        self.patient = MagicMock(spec=Patient)
import sys        self.patient.id = 1
import os        self.patient.name = "John Smith"        
from unittest.mock import Mock, MagicMock

# Add the parent directory to the path so we can import the modules        # Mock appointment        self.appointment = MagicMock(spec=Appointment)        self.appointment.id = 1
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.modules.receptionist import Receptionist        self.appointment.patient_id = self.patient.id        self.appointment.date = self.today
from backend.modules.appointment import Appointment
from backend.modules.patient import Patient
from backend.modules.fee import Fee        self.appointment.time = time(10, 0)                # Mock fee
from backend.modules.supply import Supply

class TestReceptionist(unittest.TestCase):
    """Test cases for the Receptionist class."""
            self.fee = MagicMock(spec=Fee)        self.fee.id = 1        self.fee.patient_id = self.patient.id
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock system service        self.fee.amount = 100.00        self.fee.fee_type = "doctor"        
        self.mock_system = MagicMock()
        
        # Create a receptionist with the mock service
        self.receptionist = Receptionist(        # Mock supply        self.supply = MagicMock(spec=Supply)        self.supply.id = 1
            "Jane Doe",
            "janedoe",
            "password123",
            self.mock_system
        )
                self.supply.name = "Surgical Gloves"        self.supply.quantity = 100                # Configure the mock system
        # Create test data
        self.today = date.today()
        
        # Mock patient        self.mock_system.get_patient_from_id.return_value = self.patient
        self.patient = MagicMock(spec=Patient)
        self.patient.id = 1
        self.patient.name = "John Smith"
                self.patient.add_fee.return_value = (True, "Success: Fee added")        self.patient.update_fee.return_value = (True, "Success: Fee updated")
        # Mock appointment
        self.appointment = MagicMock(spec=Appointment)
        self.appointment.id = 1        self.patient.remove_fee.return_value = (True, "Success: Fee removed")    
        self.appointment.patient_id = self.patient.id
        self.appointment.date = self.today    def test_constructor_validation(self):        """Test constructor validation."""        # Test with invalid name        with self.assertRaises(ValueError):
        self.appointment.time = time(10, 0)
        
        # Mock fee            Receptionist("", "username", "password", self.mock_system)                # Test with invalid username
        self.fee = MagicMock(spec=Fee)
        self.fee.id = 1
        self.fee.patient_id = self.patient.id        with self.assertRaises(ValueError):            Receptionist("Name", "", "password", self.mock_system)        
        self.fee.amount = 100.00
        self.fee.fee_type = "doctor"
                # Test with invalid password        with self.assertRaises(ValueError):
        # Mock supply
        self.supply = MagicMock(spec=Supply)
        self.supply.id = 1            Receptionist("Name", "username", "", self.mock_system)                # Test with None system_service        with self.assertRaises(ValueError):
        self.supply.name = "Surgical Gloves"
        self.supply.quantity = 100
        
        # Configure the mock system            Receptionist("Name", "username", "password", None)        def test_add_appointment(self):        """Test adding an appointment."""
        self.mock_system.get_patient_from_id.return_value = self.patient        # Configure mock
        self.patient.add_fee.return_value = (True, "Success: Fee added")
        self.patient.update_fee.return_value = (True, "Success: Fee updated")        self.mock_system.add_appointment.return_value = (True, "Success: Appointment added")                # Test with valid appointment
        self.patient.remove_fee.return_value = (True, "Success: Fee removed")
            result, message = self.receptionist.add_appointment(self.appointment)        self.assertTrue(result)        self.assertIn("Success", message)
    def test_constructor_validation(self):
        """Test constructor validation."""
        # Test with invalid name
        with self.assertRaises(ValueError):        self.mock_system.add_appointment.assert_called_once_with(self.appointment)                # Test with invalid appointment
            Receptionist("", "username", "password", self.mock_system)
        
        # Test with invalid username        result, message = self.receptionist.add_appointment("not an appointment")        self.assertFalse(result)        self.assertIn("Error", message)
        with self.assertRaises(ValueError):
            Receptionist("Name", "", "password", self.mock_system)
                # Mock should still have been called only once        self.mock_system.add_appointment.assert_called_once()    
        # Test with invalid password
        with self.assertRaises(ValueError):    def test_edit_appointment(self):        """Test editing an appointment."""        # Configure mock
            Receptionist("Name", "username", "", self.mock_system)
        
        # Test with None system_service
        with self.assertRaises(ValueError):        self.mock_system.update_appointment.return_value = (True, "Success: Appointment updated")                # Test with valid parameters
            Receptionist("Name", "username", "password", None)
    
    def test_add_appointment(self):
        """Test adding an appointment."""        result, message = self.receptionist.edit_appointment(1, self.appointment)        self.assertTrue(result)
        # Configure mock        self.assertIn("Success", message)
        self.mock_system.add_appointment.return_value = (True, "Success: Appointment added")        self.mock_system.update_appointment.assert_called_once_with(1, self.appointment)
                
        # Test with valid appointment        # Reset mock
        result, message = self.receptionist.add_appointment(self.appointment)        self.mock_system.update_appointment.reset_mock()
        self.assertTrue(result)        
        self.assertIn("Success", message)        # Test with invalid appointment ID
        self.mock_system.add_appointment.assert_called_once_with(self.appointment)        result, message = self.receptionist.edit_appointment(0, self.appointment)
                self.assertFalse(result)
        # Test with invalid appointment        self.assertIn("Error", message)
        result, message = self.receptionist.add_appointment("not an appointment")        self.mock_system.update_appointment.assert_not_called()
        self.assertFalse(result)        
        self.assertIn("Error", message)        # Test with invalid appointment object
        # Mock should still have been called only once
        self.mock_system.add_appointment.assert_called_once()
            result, message = self.receptionist.edit_appointment(1, "not an appointment")        self.assertFalse(result)        self.assertIn("Error", message)
    def test_edit_appointment(self):
        """Test editing an appointment."""
        # Configure mock        self.mock_system.update_appointment.assert_not_called()        def test_delete_appointment(self):        """Test deleting an appointment."""
        self.mock_system.update_appointment.return_value = (True, "Success: Appointment updated")
        
        # Test with valid parameters        # Configure mock        self.mock_system.delete_appointment.return_value = (True, "Success: Appointment deleted")        
        result, message = self.receptionist.edit_appointment(1, self.appointment)
        self.assertTrue(result)        # Test with valid ID        result, message = self.receptionist.delete_appointment(1)
        self.assertIn("Success", message)        self.assertTrue(result)        self.assertIn("Success", message)
        self.mock_system.update_appointment.assert_called_once_with(1, self.appointment)
        
        # Reset mock
        self.mock_system.update_appointment.reset_mock()
                self.mock_system.delete_appointment.assert_called_once_with(1)                # Reset mock        self.mock_system.delete_appointment.reset_mock()        
        # Test with invalid appointment ID
        result, message = self.receptionist.edit_appointment(0, self.appointment)        # Test with invalid ID        result, message = self.receptionist.delete_appointment(0)        self.assertFalse(result)
        self.assertFalse(result)
        self.assertIn("Error", message)
        self.mock_system.update_appointment.assert_not_called()        self.assertIn("Error", message)        self.mock_system.delete_appointment.assert_not_called()    
        
        # Test with invalid appointment object    def test_generate_financial_report(self):        """Test generating a financial report."""
        result, message = self.receptionist.edit_appointment(1, "not an appointment")
        self.assertFalse(result)
        self.assertIn("Error", message)


































































































































































































































































































    unittest.main()if __name__ == "__main__":        self.mock_system.update_appointment_status.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.mark_appointment_status(1, "invalid_status")        # Test with invalid status                self.mock_system.update_appointment_status.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.mark_appointment_status(0, "completed")        # Test with invalid appointment ID                self.mock_system.update_appointment_status.reset_mock()        # Reset mock                self.mock_system.update_appointment_status.assert_called_once_with(1, "completed")        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.mark_appointment_status(1, "completed")        # Test with valid parameters                self.mock_system.update_appointment_status.return_value = (True, "Success: Status updated")        # Configure mock        """Test marking appointment status."""    def test_mark_appointment_status(self):            self.mock_system.get_upcoming_appointments.assert_called_once()        self.assertEqual(result, mock_appointments)        result = self.receptionist.view_upcoming_appointments()        # Test method                self.mock_system.get_upcoming_appointments.return_value = mock_appointments        mock_appointments = [self.appointment]        # Create mock appointment list        """Test viewing upcoming appointments."""    def test_view_upcoming_appointments(self):            self.mock_system.search_patients.assert_not_called()        self.assertEqual(result, [])        result = self.receptionist.search_patients(123)        # Test with invalid search term                self.mock_system.search_patients.reset_mock()        # Reset mock                self.mock_system.search_patients.assert_called_once_with("Smith")        self.assertEqual(result, mock_patients)        result = self.receptionist.search_patients("Smith")        # Test with valid search term                self.mock_system.search_patients.return_value = mock_patients        mock_patients = [self.patient]        # Create mock patient list        """Test searching for patients."""    def test_search_patients(self):            self.mock_system.delete_supply.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_supply(0)        # Test with invalid ID                self.mock_system.delete_supply.reset_mock()        # Reset mock                self.mock_system.delete_supply.assert_called_once_with(1)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.delete_supply(1)        # Test with valid ID                self.mock_system.delete_supply.return_value = (True, "Success: Supply deleted")        # Configure mock        """Test deleting a supply."""    def test_delete_supply(self):            self.mock_system.update_supply.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_supply(1, "not a supply")        # Test with invalid supply object                self.mock_system.update_supply.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_supply(0, self.supply)        # Test with invalid supply ID                self.mock_system.update_supply.reset_mock()        # Reset mock                self.mock_system.update_supply.assert_called_once_with(1, self.supply)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.edit_supply(1, self.supply)        # Test with valid parameters                self.mock_system.update_supply.return_value = (True, "Success: Supply updated")        # Configure mock        """Test editing a supply."""    def test_edit_supply(self):            self.mock_system.add_supply.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.add_supply("not a supply")        # Test with invalid supply                self.mock_system.add_supply.reset_mock()        # Reset mock                self.mock_system.add_supply.assert_called_once_with(self.supply)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.add_supply(self.supply)        # Test with valid supply                self.mock_system.add_supply.return_value = (True, "Success: Supply added")        # Configure mock        """Test adding a supply to inventory."""    def test_add_supply(self):            self.patient.remove_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_called_once_with(999)        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_fee(999, 1)        self.mock_system.get_patient_from_id.return_value = None        # Test with non-existent patient                self.patient.remove_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_fee(1, 0)        # Test with invalid fee ID                self.patient.remove_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_fee(0, 1)        # Test with invalid patient ID                self.patient.remove_fee.reset_mock()        self.mock_system.get_patient_from_id.reset_mock()        # Reset mocks                self.patient.remove_fee.assert_called_once_with(1)        self.mock_system.get_patient_from_id.assert_called_once_with(1)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.delete_fee(1, 1)        # Test with valid parameters        """Test deleting a fee."""    def test_delete_fee(self):            self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_called_once_with(999)        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(999, 1, self.fee)        self.mock_system.get_patient_from_id.return_value = None        # Test with non-existent patient                self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(1, 1, "not a fee")        # Test with invalid fee object                self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(1, 0, self.fee)        # Test with invalid fee ID                self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(0, 1, self.fee)        # Test with invalid patient ID                self.patient.update_fee.reset_mock()        self.mock_system.get_patient_from_id.reset_mock()        # Reset mocks                self.patient.update_fee.assert_called_once_with(1, self.fee)        self.mock_system.get_patient_from_id.assert_called_once_with(1)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.edit_fee(1, 1, self.fee)        # Test with valid parameters        """Test editing a fee."""    def test_edit_fee(self):            self.patient.add_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_called_once_with(999)        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.add_fee(999, self.fee)        self.mock_system.get_patient_from_id.return_value = None        # Test with non-existent patient                self.patient.add_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.add_fee(1, "not a fee")        # Test with invalid fee object                self.patient.add_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.add_fee(0, self.fee)        # Test with invalid patient ID                self.patient.add_fee.reset_mock()        self.mock_system.get_patient_from_id.reset_mock()        # Reset mocks                self.patient.add_fee.assert_called_once_with(self.fee)        self.mock_system.get_patient_from_id.assert_called_once_with(1)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.add_fee(1, self.fee)        # Test with valid parameters        """Test adding a fee to a patient."""    def test_add_fee(self):            self.mock_system.generate_financial_report.assert_not_called()        self.assertIn("error", report)        self.assertFalse(result)        result, report = self.receptionist.generate_financial_report("01/01/2024", "31/01/2024")        # Test with invalid date format                self.mock_system.generate_financial_report.assert_not_called()        self.assertIn("error", report)        self.assertFalse(result)        result, report = self.receptionist.generate_financial_report("2024-01-01", "")        # Test with invalid end date                self.mock_system.generate_financial_report.assert_not_called()        self.assertIn("error", report)        self.assertFalse(result)        result, report = self.receptionist.generate_financial_report("", "2024-01-31")        # Test with invalid start date                self.mock_system.generate_financial_report.reset_mock()        # Reset mock                self.mock_system.generate_financial_report.assert_called_once_with("2024-01-01", "2024-01-31")        self.assertEqual(report, mock_report)        self.assertTrue(result)        result, report = self.receptionist.generate_financial_report("2024-01-01", "2024-01-31")        # Test with valid dates                self.mock_system.generate_financial_report.return_value = (True, mock_report)        mock_report = {"total_income": 1000, "total_expenses": 500, "net_profit": 500}        """Test generating a financial report."""    def test_generate_financial_report(self):            self.mock_system.delete_appointment.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_appointment(0)        # Test with invalid ID                self.mock_system.delete_appointment.reset_mock()        # Reset mock                self.mock_system.delete_appointment.assert_called_once_with(1)        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.delete_appointment(1)        # Test with valid ID                self.mock_system.delete_appointment.return_value = (True, "Success: Appointment deleted")        # Configure mock        """Test deleting an appointment."""    def test_delete_appointment(self):            self.mock_system.update_appointment.assert_not_called()        mock_report = {"total_income": 1000, "total_expenses": 500, "net_profit": 500}
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
        







    unittest.main()if __name__ == "__main__":

        self.mock_system.update_appointment_status.assert_not_called()        self.assertIn("Error", message)


        self.assertFalse(result)        result, message = self.receptionist.mark_appointment_status(1, "invalid_status")

        # Test with invalid status                self.mock_system.update_appointment_status.assert_not_called()        self.assertIn("Error", message)


        self.assertFalse(result)        result, message = self.receptionist.mark_appointment_status(0, "completed")


        # Test with invalid appointment ID                self.mock_system.update_appointment_status.reset_mock()


        # Reset mock                self.mock_system.update_appointment_status.assert_called_once_with(1, "completed")


        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.mark_appointment_status(1, "completed")




        # Test with valid parameters                self.mock_system.update_appointment_status.return_value = (True, "Success: Status updated")

        # Configure mock        """Test marking appointment status."""


    def test_mark_appointment_status(self):            self.mock_system.get_upcoming_appointments.assert_called_once()

        self.assertEqual(result, mock_appointments)        result = self.receptionist.view_upcoming_appointments()



        # Test method                self.mock_system.get_upcoming_appointments.return_value = mock_appointments


        mock_appointments = [self.appointment]        # Create mock appointment list        """Test viewing upcoming appointments."""


    def test_view_upcoming_appointments(self):            self.mock_system.search_patients.assert_not_called()



        self.assertEqual(result, [])        result = self.receptionist.search_patients(123)        # Test with invalid search term

                self.mock_system.search_patients.reset_mock()        # Reset mock                self.mock_system.search_patients.assert_called_once_with("Smith")


        self.assertEqual(result, mock_patients)        result = self.receptionist.search_patients("Smith")




        # Test with valid search term                self.mock_system.search_patients.return_value = mock_patients


        mock_patients = [self.patient]        # Create mock patient list
        """Test searching for patients."""    def test_search_patients(self):            self.mock_system.delete_supply.assert_not_called()



        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_supply(0)

        # Test with invalid ID                self.mock_system.delete_supply.reset_mock()




        # Reset mock                self.mock_system.delete_supply.assert_called_once_with(1)        self.assertIn("Success", message)
        self.assertTrue(result)        result, message = self.receptionist.delete_supply(1)

        # Test with valid ID                self.mock_system.delete_supply.return_value = (True, "Success: Supply deleted")


        # Configure mock        """Test deleting a supply."""    def test_delete_supply(self):            self.mock_system.update_supply.assert_not_called()




        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_supply(1, "not a supply")


        # Test with invalid supply object


                self.mock_system.update_supply.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)


        result, message = self.receptionist.edit_supply(0, self.supply)        # Test with invalid supply ID


                self.mock_system.update_supply.reset_mock()        # Reset mock                self.mock_system.update_supply.assert_called_once_with(1, self.supply)


        self.assertIn("Success", message)

        self.assertTrue(result)        result, message = self.receptionist.edit_supply(1, self.supply)






        # Test with valid parameters
        
        self.mock_system.update_supply.return_value = (True, "Success: Supply updated")
        # Configure mock
        """Test editing a supply."""
    def test_edit_supply(self):
    
        self.mock_system.add_supply.assert_not_called()
        self.assertIn("Error", message)
        self.assertFalse(result)
        result, message = self.receptionist.add_supply("not a supply")
        # Test with invalid supply
        
        self.mock_system.add_supply.reset_mock()
        # Reset mock
        
        self.mock_system.add_supply.assert_called_once_with(self.supply)
        self.assertIn("Success", message)
        self.assertTrue(result)
        result, message = self.receptionist.add_supply(self.supply)
        # Test with valid supply
        
        self.mock_system.add_supply.return_value = (True, "Success: Supply added")
        # Configure mock
        """Test adding a supply to inventory."""
    def test_add_supply(self):
    
        self.patient.remove_fee.assert_not_called()
        self.mock_system.get_patient_from_id.assert_called_once_with(999)



        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_fee(999, 1)        self.mock_system.get_patient_from_id.return_value = None        # Test with non-existent patient                self.patient.remove_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.delete_fee(1, 0)        # Test with invalid fee ID                self.patient.remove_fee.assert_not_called()
        self.mock_system.get_patient_from_id.assert_not_called()
        self.assertIn("Error", message)
        self.assertFalse(result)
        result, message = self.receptionist.delete_fee(0, 1)


        # Test with invalid patient ID                self.patient.remove_fee.reset_mock()


        self.mock_system.get_patient_from_id.reset_mock()        # Reset mocks                self.patient.remove_fee.assert_called_once_with(1)
        self.mock_system.get_patient_from_id.assert_called_once_with(1)



        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.delete_fee(1, 1)

        # Test with valid parameters        """Test deleting a fee."""    def test_delete_fee(self):

            self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_called_once_with(999)


        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(999, 1, self.fee)


        self.mock_system.get_patient_from_id.return_value = None

        # Test with non-existent patient                self.patient.update_fee.assert_not_called()


        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)


        result, message = self.receptionist.edit_fee(1, 1, "not a fee")


        # Test with invalid fee object                self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()
        self.assertIn("Error", message)        self.assertFalse(result)



        result, message = self.receptionist.edit_fee(1, 0, self.fee)        # Test with invalid fee ID

                self.patient.update_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()

        self.assertIn("Error", message)        self.assertFalse(result)        result, message = self.receptionist.edit_fee(0, 1, self.fee)

        # Test with invalid patient ID        



        self.patient.update_fee.reset_mock()        self.mock_system.get_patient_from_id.reset_mock()        # Reset mocks

                self.patient.update_fee.assert_called_once_with(1, self.fee)        self.mock_system.get_patient_from_id.assert_called_once_with(1)


        self.assertIn("Success", message)        self.assertTrue(result)        result, message = self.receptionist.edit_fee(1, 1, self.fee)



        # Test with valid parameters
        """Test editing a fee."""    def test_edit_fee(self):            self.patient.add_fee.assert_not_called()


        self.mock_system.get_patient_from_id.assert_called_once_with(999)        self.assertIn("Error", message)



        self.assertFalse(result)        result, message = self.receptionist.add_fee(999, self.fee)

        self.mock_system.get_patient_from_id.return_value = None        # Test with non-existent patient

                self.patient.add_fee.assert_not_called()        self.mock_system.get_patient_from_id.assert_not_called()
        self.assertIn("Error", message)

        self.assertFalse(result)        result, message = self.receptionist.add_fee(1, "not a fee")


        # Test with invalid fee object                self.patient.add_fee.assert_not_called()
        self.mock_system.get_patient_from_id.assert_not_called()        self.assertIn("Error", message)        self.assertFalse(result)


        result, message = self.receptionist.add_fee(0, self.fee)        # Test with invalid patient ID


                self.patient.add_fee.reset_mock()        self.mock_system.get_patient_from_id.reset_mock()
        # Reset mocks                self.patient.add_fee.assert_called_once_with(self.fee)        self.mock_system.get_patient_from_id.assert_called_once_with(1)


        self.assertIn("Success", message)
        self.assertTrue(result)

        result, message = self.receptionist.add_fee(1, self.fee)
        # Test with valid parameters
        """Test adding a fee to a patient."""    def test_add_fee(self):    


        self.mock_system.generate_financial_report.assert_not_called()
        self.assertIn("error", report)
        self.assertFalse(result)
        result, report = self.receptionist.generate_financial_report("01/01/2024", "31/01/2024")
        # Test with invalid date format
        
        self.mock_system.generate_financial_report.assert_not_called()        self.assertIn("error", report)        self.assertFalse(result)        result, report = self.receptionist.generate_financial_report("2024-01-01", "")        # Test with invalid end date