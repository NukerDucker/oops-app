from typing import List, Tuple, Optional, Any, Union
from patient import Patient
from appointment import Appointment
from receptionist import Receptionist
from admission import Admission
from fee import Fee
from payment_method import PaymentMethod
from lab_request import LabRequest
from lab_result import LabResult
from lab_personnel import LabPersonnel
from prescription import Prescription
from pharmacist import Pharmacist
from doctor import Doctor
from supply import Supply
import utils
import time
import random


class System:
    def __init__(self):
        self.__supplies: List[Supply] = []
        self.__financial_spendings: List[Any] = []
        self.__financial_incomes: List[Any] = []
        self.__lab_personnel: List[LabPersonnel] = []
        self.__doctor_personnel: List[Doctor] = []
        self.__nurse_personnel: List[Any] = []
        self.__receptionist_personnel: List[Receptionist] = []
        self.__pharmacist_personnel: List[Pharmacist] = []
        self.__appointments: List[Appointment] = []
        self.__patients: List[Patient] = []
        self.__pending_prescriptions: List[Prescription] = []
        self.__admissions: List[Admission] = []
    
    @property
    def supplies(self) -> List[Supply]:
        return self.__supplies
    
    @property
    def financial_spendings(self) -> List[Any]:
        return self.__financial_spendings
    
    @property
    def financial_incomes(self) -> List[Any]:
        return self.__financial_incomes
    
    @property
    def appointments(self) -> List[Appointment]:
        return self.__appointments
    
    @property
    def patients(self) -> List[Patient]:
        return self.__patients
    
    @property
    def pending_prescriptions(self) -> List[Prescription]:
        return self.__pending_prescriptions
    
    @property
    def admissions(self) -> List[Admission]:
        return self.__admissions

    def get_personnel(self, personnel_type: str) -> Union[List[Any], str]:
        personnel_map = {
            "lab": self.__lab_personnel,
            "doctor": self.__doctor_personnel,
            "nurse": self.__nurse_personnel,
            "receptionist": self.__receptionist_personnel,
            "pharmacist": self.__pharmacist_personnel
        }
        
        if personnel_type in personnel_map:
            return personnel_map[personnel_type]
        return "Error: Invalid type"
    
    def get_personnel_count(self, personnel_type: str) -> Union[int, str]:
        personnel = self.get_personnel(personnel_type)
        if isinstance(personnel, list):
            return len(personnel)
        return personnel  # Return the error message

    def add_supply(self, name: str, count: int, unit: str, best_before: int, 
                  price: float, restriction: str, notes: str) -> str:
        try:
            if count <= 0:
                return "Error: Invalid count"
                
            valid_units = ["kg", "g", "mg", "l", "ml", "unit", "piece"]
            if unit not in valid_units:
                return "Error: Invalid unit"
                
            if best_before <= time.time():
                return "Error: Invalid best before date"
                
            for supply in self.__supplies:
                if supply.name == name:
                    supply.add_count(count)
                    return "Success: Supply count added"
                    
            self.__supplies.append(Supply(
                name=name, count=count, unit=unit, best_before=best_before, 
                price=price, restriction=restriction, notes=notes
            ))
            return "Success: New supply added"
        except:
            return "Error: Invalid input"

    def add_personnel(self, personnel: Any) -> Tuple[bool, str]:
        personnel_map = {
            LabPersonnel: self.__lab_personnel,
            Doctor: self.__doctor_personnel,
            # Nurse: self.__nurse_personnel,  # Uncomment when Nurse class is implemented
            Receptionist: self.__receptionist_personnel,
            Pharmacist: self.__pharmacist_personnel
        }
        
        for cls, personnel_list in personnel_map.items():
            if isinstance(personnel, cls):
                personnel_list.append(personnel)
                return True, "Success: Added personnel"
                
        return False, f"Error: Invalid type for personnel {type(personnel)}"

    def add_patient(self, patient: Patient) -> Tuple[bool, str]:
        try:
            self.__patients.append(patient)
            return True, "Success: Added patient to record"
        except Exception as exc:
            return False, f"Error: {str(exc)}"
            
    def edit_patient(self, patient_to_edit: Patient, updated_patient: Patient) -> Tuple[bool, str]:
        index = utils.get_object_index_in_container(
            container=self.__patients, 
            object=patient_to_edit, 
            get_identifier=lambda obj: obj.id
        )
        
        if index == -1:
            return False, "Error: Cannot find patient"
            
        updated_patient.id = self.__patients[index].id
        self.__patients[index] = updated_patient
        return True, "Success: Edited patient data"
        
    def delete_patient(self, patient_id: int) -> Tuple[bool, str]:
        index = utils.get_object_index_in_container_id(
            container=self.__patients, 
            id=patient_id, 
            get_id=lambda obj: obj.id
        )
        
        if index == -1:
            return False, "Error: Could not find patient"
            
        del self.__patients[index]
        return True, "Success: Deleted patient"
        
    def add_appointment(self, appointment: Appointment) -> Tuple[bool, str]:
        try:
            self.__appointments.append(appointment)
            return True, "Success: Appointment added"
        except Exception as exc:
            return False, f"Error: {str(exc)}"
            
    def change_appointment(self, appointment_id: int, patient_id: int, doctor_id: int, 
                          date: str, time: str) -> str:
        try:
            for appointment in self.__appointments:
                if appointment.appointment_id == appointment_id:
                    appointment.patient_id = patient_id
                    appointment.doctor_id = doctor_id
                    appointment.date = date
                    appointment.time = time
                    return "Success: Appointment changed"
            return "Error: Appointment not found"
        except:
            return "Error: Failed to change appointment"
            
    def remove_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        index = utils.get_object_index_in_container_id(
            container=self.__appointments, 
            id=appointment_id, 
            get_id=lambda obj: obj.appointment_id
        )
        
        if index == -1:
            return False, "Error: Could not find appointment"
            
        del self.__appointments[index]
        return True, "Success: Removed appointment"
            
    def add_admission(self, admission: Admission) -> Tuple[bool, str]:
        try:
            self.__admissions.append(admission)
            return True, "Success: Admission added"
        except Exception as exc:
            return False, f"Error: {str(exc)}"
            
    def remove_admission(self, patient_id: int) -> Tuple[bool, str]:
        index = utils.get_object_index_in_container_id(
            container=self.__admissions, 
            id=patient_id, 
            get_id=lambda obj: obj.patient_id
        )
        
        if index == -1:
            return False, "Error: Could not find admission"
            
        del self.__admissions[index]
        return True, "Success: Deleted admission"

    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        for patient in self.__patients:
            if patient.id == patient_id:
                return patient
        return None

    def pay_fee(self, fee: Fee, payment_method: PaymentMethod) -> Tuple[bool, str]:
        payment_status = payment_method.pay(fee.amount)
        if not payment_status[0]: 
            return payment_status

        fee_owner = self.get_patient_by_id(fee.patient_id)
        if fee_owner is None: 
            return False, "Error: Unable to find patient with ID specified in the fee"
        
        fee_removal_status = fee_owner.remove_fee(fee)
        if not fee_removal_status[0]:
            payment_method.refund(fee.amount)
            return False, "Error: Unable to find the fee in patient. Refunded payment."
            
        return True, "Success: Fee is paid"
        
    def order_lab_test(self, lab_request: LabRequest, lab_personnel_id: int) -> Tuple[bool, str]:
        for personnel in self.__lab_personnel:
            if personnel.id == lab_personnel_id:
                personnel.assign_lab_test(lab_request)
                return True, "Success: Ordered lab test"
                
        return False, "Error: No lab personnel found with specified ID"
        
    def verify_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        total_pharmacists = len(self.__pharmacist_personnel)
        
        if total_pharmacists == 0: 
            return False, "Error: No pharmacists employed"
            
        random_pharmacist_index = random.randint(0, total_pharmacists - 1)
        self.__pharmacist_personnel[random_pharmacist_index].add_prescription_for_verification(prescription)
        return True, "Success: Sent prescription for verification with pharmacist"
        
    def queue_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        self.__pending_prescriptions.append(prescription)
        return True, "Success: Prescription in queue"
        
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Doctor]:
        doctor_index = utils.get_object_index_in_container_id(
            container=self.__doctor_personnel, 
            id=doctor_id, 
            get_id=lambda obj: obj.id
        )
        
        if doctor_index == -1:
            return None
            
        return self.__doctor_personnel[doctor_index]