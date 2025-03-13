import unittest
from datetime import date, time

from backend.modules.appointment import Appointment

class TestAppointment(unittest.TestCase):
    """Test suite for the Appointment class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.today = date.today()
        self.appointment_time = time(14, 30)  # 2:30 PM
        
        self.appointment = Appointment(
            patient_id=1,
            doctor_id=2,
            appointment_date=self.today,
            appointment_time=self.appointment_time
        )
    
    def test_appointment_initialization(self):
        """Test appointment initialization and property access."""
        self.assertEqual(self.appointment.patient_id, 1)
        self.assertEqual(self.appointment.doctor_id, 2)
        self.assertEqual(self.appointment.date, self.today)
        self.assertEqual(self.appointment.time, self.appointment_time)
        self.assertEqual(self.appointment.status, "scheduled")
    
    def test_update_patient_id(self):
        """Test updating patient ID."""
        # Test valid update
        result, message = self.appointment.update_patient_id(3)
        self.assertTrue(result)
        self.assertEqual(self.appointment.patient_id, 3)
        
        # Test invalid update
        result, message = self.appointment.update_patient_id(-1)
        self.assertFalse(result)
        self.assertEqual(self.appointment.patient_id, 3)  # Should not change
    
    def test_update_doctor_id(self):
        """Test updating doctor ID."""
        # Test valid update
        result, message = self.appointment.update_doctor_id(5)
        self.assertTrue(result)
        self.assertEqual(self.appointment.doctor_id, 5)
        
        # Test invalid update
        result, message = self.appointment.update_doctor_id(0)
        self.assertFalse(result)
        self.assertEqual(self.appointment.doctor_id, 5)  # Should not change
    
    def test_update_date(self):
        """Test updating appointment date."""
        # Test valid update
        tomorrow = date(2025, 3, 14)
        result, message = self.appointment.update_date(tomorrow)
        self.assertTrue(result)
        self.assertEqual(self.appointment.date, tomorrow)
        
        # Test invalid update
        result, message = self.appointment.update_date("not a date")
        self.assertFalse(result)
        self.assertEqual(self.appointment.date, tomorrow)  # Should not change
    
    def test_update_time(self):
        """Test updating appointment time."""
        # Test valid update
        new_time = time(15, 45)  # 3:45 PM
        result, message = self.appointment.update_time(new_time)
        self.assertTrue(result)
        self.assertEqual(self.appointment.time, new_time)
        
        # Test invalid update
        result, message = self.appointment.update_time("not a time")
        self.assertFalse(result)
        self.assertEqual(self.appointment.time, new_time)  # Should not change
    
    def test_status_transitions(self):
        """Test appointment status transitions."""
        # Initial status is "scheduled"
        self.assertEqual(self.appointment.status, "scheduled")
        self.assertTrue(self.appointment.is_active())
        self.assertFalse(self.appointment.is_completed())
        
        # Mark as completed
        result, message = self.appointment.mark_completed()
        self.assertTrue(result)
        self.assertEqual(self.appointment.status, "completed")
        self.assertTrue(self.appointment.is_completed())
        self.assertFalse(self.appointment.is_active())
        
        # Try to cancel (should fail as completed)
        result, message = self.appointment.cancel()
        self.assertFalse(result)
        self.assertEqual(self.appointment.status, "completed")  # Should not change
        
        # Create a new appointment for testing other transitions
        new_appointment = Appointment(
            patient_id=1,
            doctor_id=2,
            appointment_date=self.today,
            appointment_time=self.appointment_time
        )
        
        # Cancel appointment
        result, message = new_appointment.cancel()
        self.assertTrue(result)
        self.assertEqual(new_appointment.status, "cancelled")
        self.assertFalse(new_appointment.is_active())
        
        # Try to mark cancelled as completed (should fail)
        result, message = new_appointment.mark_completed()
        self.assertFalse(result)
        self.assertEqual(new_appointment.status, "cancelled")  # Should not change
    
    def test_mark_no_show(self):
        """Test marking an appointment as no-show."""
        # Only scheduled appointments can be marked as no-show
        result, message = self.appointment.mark_no_show()
        self.assertTrue(result)
        self.assertEqual(self.appointment.status, "no-show")
        
        # Create an appointment and cancel it
        new_appointment = Appointment(
            patient_id=1,
            doctor_id=2,
            appointment_date=self.today,
            appointment_time=self.appointment_time
        )
        new_appointment.cancel()
        
        # Try to mark cancelled as no-show (should fail)
        result, message = new_appointment.mark_no_show()
        self.assertFalse(result)
        self.assertEqual(new_appointment.status, "cancelled")  # Should not change