from Appointment import Appointment
from Patient import Patient
from LabRequest import LabRequest
from LabResult import LabResult
from Prescription import Prescription
from Medication import Medication

import globals

class Doctor:
    current_id = int(0)
    
    def __init__(self, name, surname, speciality, password, id = 0):
        Doctor.current_id += 1
        self.__id = Doctor.current_id
        self.__name = name
        self.__surname = surname
        self.__speciality = speciality
        self.__password = password
        self.__invalid_prescriptions: list[Prescription] = []
        
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_surname(self):
        return self.__surname
    def get_speciality(self):
        return self.__speciality
    
    def get_password(self):
        return self.__password
    
    def change_password(self, old_password, new_password) -> tuple[bool, str]:
        if old_password == self.__password:
            self.__password = new_password
            return True, "Success : Password changed"
        return False, "Error : Invalid password"
    
    def view_patient_record(self, patient_id) -> Patient:
        return globals.system.get_patient_from_id(patient_id)

    def schedule_appointment(self, appointment):
        appointment.set_doctor_id(self.__id)
        return globals.system.add_appointment(appointment)

    def prescribe_medicine(self, prescription: Prescription) -> tuple[bool, str]:
        return globals.system.verify_prescription(prescription)
    def add_disapproved_prescription(self, prescription: Prescription):
        self.__invalid_prescriptions.append(prescription)
        
    def add_admission(self, admission) -> tuple[bool, str]:
        return globals.system.add_admission(admission)
    def remove_admission(self, patient_id) -> tuple[bool, str]:
        return globals.system.removeAdmission(patient_id)
        
    def add_medication(self, patient_id, medication: Medication) -> tuple[bool, str]:
        patient: Patient = globals.system.get_patient_from_id(patient_id)
        if patient is None: return False, "Error : unable to find patient with specified id"
        patient.add_medication(medication)
        return True, "Success : added medication to patient"
        
    def order_lab_test(self, lab_request: LabRequest, lab_personnel_id) -> tuple[bool, str]:
        return globals.system.order_lab_test(lab_request=lab_request, lab_personnel_id=lab_personnel_id)
        
    def view_lab_results(self, patient_id) -> list[LabResult]:
        patient: Patient = globals.system.get_patient_from_id(patient_id)
        if patient is None: return None
        return patient.get_lab_results()