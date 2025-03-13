import unittest
from datetime import date, time
from unittest.mock import Mock, MagicMock

from backend.modules.doctor import Doctor
from backend.modules.patient import Patient
from backend.modules.prescription import Prescription
from backend.modules.treatment import Treatment
from backend.modules.lab_result import LabResult
from backend.modules.medication import Medication

class TestDoctor(unittest.TestCase):
    """Test suite for the Doctor class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock system service
        self.mock_system_service = Mock()
        
        # Create a doctor instance for testing
        self.doctor = Doctor(
            name="Dr. John Smith",
            username="jsmith",
            password="password123",
            speciality="Cardiology",
            system_service=self.mock_system_service
        )
        
        # Create a mock patient
        self.mock_patient = Mock(spec=Patient)
        self.mock_patient.id = 1
        self.mock_patient.name = "Jane Doe"
        
        # Configure the mock system service to return our mock patient
        self.mock_system_service.get_patient_from_id.return_value = self.mock_patient
    
    def test_doctor_initialization(self):
        """Test doctor initialization and property access."""
        self.assertEqual(self.doctor.name, "Dr. John Smith")
        self.assertEqual(self.doctor.username, "jsmith")
        self.assertEqual(self.doctor.speciality, "Cardiology")
        self.assertEqual(self.doctor.user_type, "doctor")
    
    def test_doctor_speciality_update(self):
        """Test updating doctor speciality."""
        # Test valid update
        result, message = self.doctor.update_speciality("Neurology")
        self.assertTrue(result)
        self.assertEqual(self.doctor.speciality, "Neurology")
        
        # Test invalid update
        result, message = self.doctor.update_speciality("")
        self.assertFalse(result)
        self.assertEqual(self.doctor.speciality, "Neurology")  # Should not change
    
    def test_view_patient_record(self):
        """Test viewing a patient's record."""
        # Test valid patient ID
        patient = self.doctor.view_patient_record(1)
        self.assertIsNotNone(patient)
        self.mock_system_service.get_patient_from_id.assert_called_with(1)
        
        # Test invalid patient ID
        patient = self.doctor.view_patient_record(-1)
        self.assertIsNone(patient)
        # System service should not be called with invalid ID
        self.mock_system_service.get_patient_from_id.assert_called_once()
    
    def test_add_lab_result(self):
        """Test adding a lab result to a patient."""
        # Create a mock lab result
        mock_lab_result = Mock(spec=LabResult)
        mock_lab_result.id = 1
        
        # Configure mock patient's add_lab_result method
        self.mock_patient.add_lab_result.return_value = (True, "Success: Lab result added")
        
        # Test adding lab result
        result, message = self.doctor.add_lab_result(1, mock_lab_result)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Lab result added")
        self.mock_patient.add_lab_result.assert_called_with(mock_lab_result)
        
        # Test invalid patient ID
        result, message = self.doctor.add_lab_result(-1, mock_lab_result)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Patient ID must be a positive integer")
        
        # Test invalid lab result object
        result, message = self.doctor.add_lab_result(1, "Not a lab result")
        self.assertFalse(result)
        self.assertEqual(message, "Error: Invalid lab result object")
    
    def test_edit_lab_result(self):
        """Test editing a lab result."""
        # Create a mock lab result
        mock_lab_result = Mock(spec=LabResult)
        mock_lab_result.id = 1
        
        # Configure mock patient's update_lab_result method
        self.mock_patient.update_lab_result.return_value = (True, "Success: Lab result updated")
        
        # Test editing lab result
        result, message = self.doctor.edit_lab_result(1, 1, mock_lab_result)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Lab result updated")
        self.mock_patient.update_lab_result.assert_called_with(1, mock_lab_result)
        
        # Test invalid patient ID
        result, message = self.doctor.edit_lab_result(-1, 1, mock_lab_result)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Patient ID must be a positive integer")
        
        # Test invalid lab result ID
        result, message = self.doctor.edit_lab_result(1, -1, mock_lab_result)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Lab result ID must be a positive integer")
    
    def test_add_prescription(self):
        """Test adding a prescription."""
        # Create a mock prescription
        mock_prescription = Mock(spec=Prescription)
        mock_prescription.id = 1
        
        # Configure mock system service verify_prescription method
        self.mock_system_service.verify_prescription.return_value = (True, "Success: Prescription verified")
        
        # Test adding prescription
        result, message = self.doctor.add_prescription(mock_prescription)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Prescription verified")
        self.mock_system_service.verify_prescription.assert_called_with(mock_prescription)
        
        # Test failed verification
        self.mock_system_service.verify_prescription.return_value = (False, "Error: Invalid prescription")
        result, message = self.doctor.add_prescription(mock_prescription)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Invalid prescription")
        
        # Check if invalid prescription was added to the list
        invalid_prescriptions = self.doctor.get_invalid_prescriptions()
        self.assertEqual(len(invalid_prescriptions), 1)
        self.assertEqual(invalid_prescriptions[0], mock_prescription)
    
    def test_add_treatment(self):
        """Test adding a treatment to a patient."""
        # Create a mock treatment
        mock_treatment = Mock(spec=Treatment)
        mock_treatment.id = 1
        
        # Configure mock patient's add_treatment method
        self.mock_patient.add_treatment.return_value = (True, "Success: Treatment added")
        
        # Test adding treatment
        result, message = self.doctor.add_treatment(1, mock_treatment)
        self.assertTrue(result)
        self.assertEqual(message, "Success: Treatment added")
        self.mock_patient.add_treatment.assert_called_with(mock_treatment)
        
        # Test invalid patient ID
        result, message = self.doctor.add_treatment(-1, mock_treatment)
        self.assertFalse(result)
        self.assertEqual(message, "Error: Patient ID must be a positive integer")
        
        # Test invalid treatment object
        result, message = self.doctor.add_treatment(1, "Not a treatment")
        self.assertFalse(result)
        self.assertEqual(message, "Error: Invalid treatment object")
