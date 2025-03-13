import unittest
from unittest.mock import Mock

from backend.modules.patient import Patient
from backend.modules.lab_result import LabResult
from backend.modules.prescription import Prescription
from backend.modules.medication import Medication
from backend.modules.treatment import Treatment
from backend.modules.fee import Fee

class TestPatient(unittest.TestCase):
    """Test suite for the Patient class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.patient = Patient(
            name="Jane Doe",
            age=35,
            gender="Female",
            contact="555-1234"
        )
        
        # Create mock objects for testing
        self.mock_lab_result = Mock(spec=LabResult)
        self.mock_lab_result.id = 1
        
        self.mock_prescription = Mock(spec=Prescription)
        self.mock_prescription.id = 1
        
        self.mock_medication = Mock(spec=Medication)
        self.mock_medication.id = 1
        self.mock_medication.finished = False
        
        self.mock_treatment = Mock(spec=Treatment)
        self.mock_treatment.id = 1
        
        self.mock_fee = Mock(spec=Fee)
        self.mock_fee.id = 1
        self.mock_fee.amount = 100.0
    
    def test_patient_initialization(self):
        """Test patient initialization and property access."""
        self.assertEqual(self.patient.name, "Jane Doe")
        self.assertEqual(self.patient.age, 35)
        self.assertEqual(self.patient.gender, "Female")
        self.assertEqual(self.patient.contact, "555-1234")
        
        # Collections should be initialized empty
        self.assertEqual(len(self.patient.history), 0)
    
    def test_add_history_entry(self):
        """Test adding a history entry."""
        # Test valid entry
        result, message = self.patient.add_history_entry("Initial consultation")
        self.assertTrue(result)
        self.assertEqual(len(self.patient.history), 1)
        self.assertEqual(self.patient.history[0], "Initial consultation")
        
        # Test invalid entry
        result, message = self.patient.add_history_entry("")
        self.assertFalse(result)
        self.assertEqual(len(self.patient.history), 1)  # Should not change
    
    def test_lab_result_management(self):
        """Test lab result CRUD operations."""
        # Add lab result
        result, message = self.patient.add_lab_result(self.mock_lab_result)
        self.assertTrue(result)
        
        # Get lab results
        lab_results = self.patient.get_lab_results()
        self.assertEqual(len(lab_results), 1)
        self.assertEqual(lab_results[0], self.mock_lab_result)
        
        # Get specific lab result
        lab_result = self.patient.get_lab_result(1)
        self.assertEqual(lab_result, self.mock_lab_result)
        
        # Update lab result
        updated_mock = Mock(spec=LabResult)
        updated_mock.id = 1  # Same ID
        result, message = self.patient.update_lab_result(1, updated_mock)
        self.assertTrue(result)
        
        # Verify update
        lab_result = self.patient.get_lab_result(1)
        self.assertEqual(lab_result, updated_mock)
        
        # Delete lab result
        result, message = self.patient.remove_lab_result(1)
        self.assertTrue(result)
        
        # Verify deletion
        lab_results = self.patient.get_lab_results()
        self.assertEqual(len(lab_results), 0)
        
        # Try to get non-existent lab result
        lab_result = self.patient.get_lab_result(1)
        self.assertIsNone(lab_result)
    
    def test_prescription_management(self):
        """Test prescription CRUD operations."""
        # Add prescription
        result, message = self.patient.add_prescription(self.mock_prescription)
        self.assertTrue(result)
        
        # Get prescriptions
        prescriptions = self.patient.get_prescriptions()
        self.assertEqual(len(prescriptions), 1)
        self.assertEqual(prescriptions[0], self.mock_prescription)
        
        # Get specific prescription
        prescription = self.patient.get_prescription(1)
        self.assertEqual(prescription, self.mock_prescription)
        
        # Update prescription
        updated_mock = Mock(spec=Prescription)
        updated_mock.id = 1  # Same ID
        result, message = self.patient.update_prescription(1, updated_mock)
        self.assertTrue(result)
        
        # Verify update
        prescription = self.patient.get_prescription(1)
        self.assertEqual(prescription, updated_mock)
        
        # Delete prescription
        result, message = self.patient.remove_prescription(1)
        self.assertTrue(result)
        
        # Verify deletion
        prescriptions = self.patient.get_prescriptions()
        self.assertEqual(len(prescriptions), 0)
    
    def test_medication_management(self):
        """Test medication CRUD operations."""
        # Add medication
        result, message = self.patient.add_medication(self.mock_medication)
        self.assertTrue(result)
        
        # Get medications
        medications = self.patient.get_medications()
        self.assertEqual(len(medications), 1)
        self.assertEqual(medications[0], self.mock_medication)
        
        # Test current_medications property
        current_meds = self.patient.current_medications
        self.assertEqual(len(current_meds), 1)  # Should include our mock which is not finished
        
        # Test with a finished medication
        finished_med = Mock(spec=Medication)
        finished_med.id = 2
        finished_med.finished = True
        self.patient.add_medication(finished_med)
        
        # Should only return unfinished medications
        current_meds = self.patient.current_medications
        self.assertEqual(len(current_meds), 1)
    
    def test_fees_management(self):
        """Test fee CRUD operations."""
        # Add fee
        result, message = self.patient.add_fee(self.mock_fee)
        self.assertTrue(result)
        
        # Get fees
        fees = self.patient.get_fees()
        self.assertEqual(len(fees), 1)
        self.assertEqual(fees[0], self.mock_fee)
        
        # Test total fee calculation
        total = self.patient.calculate_total_fees()
        self.assertEqual(total, 100.0)
        
        # Add another fee
        another_fee = Mock(spec=Fee)
        another_fee.id = 2
        another_fee.amount = 50.0
        self.patient.add_fee(another_fee)
        
        # Test updated total
        total = self.patient.calculate_total_fees()
        self.assertEqual(total, 150.0)