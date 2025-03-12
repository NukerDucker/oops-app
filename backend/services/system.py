# Task: Implement the classes and methods in the class descriptions below
# Note: You can add additional methods to the classes if you need
# Note: You can add additional classes if you need
# Note: You can add additional attributes to the classes if you need
# text in bracket is name in class diagram
# / means started
# // means done
# System /
# Receptionist  /
# Pharmacist  /
# Doctor /
# Nurse /
# LabPersonel  /
# Patient /
# Prescription /
# Treatment /
# LabResult /
# Supply (Medicine and Supply) /
# Appointment /
# Admission /
# Fee //
# Note: You can add additional classes if you need

#Question
# How is class Fee different from class Invoice?
# Answer:
# How is class Treatment different from class MedicalCondition?  I think medical condition is a part of treatment so, I coded it as a part of treatment.
# Answer:

from Patient import Patient
from Appointment import Appointment
from Receptionist import Receptionist
from Admission import Admission
from Fee import Fee
from PaymentMethod import PaymentMethod
from LabRequest import LabRequest
from LabResult import LabResult
from LabPersonnel import LabPersonnel
from Prescription import Prescription
from Pharmacist import Pharmacist
from Doctor import Doctor
import utils

import time
import random

class System:
    def __init__(self):
        self.__supplies = []
        #self.__medicines = []  # I think medicines are a part of supplies so, I coded it as a part of supplies.
        self.__financial_spendings = []
        self.__financial_incomes = []
        self.__lab_personels = []
        self.__doctor_personels = [Doctor]
        self.__nurse_personels = []
        self.__receptionist_personels = []
        self.__pharmacist_personels = []
        self.__appointments = []
        self.__patients: list[Patient] = []
        self.__pending_prescriptions = []
        self.__admissions = []
    
    def get_supplies(self):
        return self.__supplies
    
    # def get_medicines(self):
    #     return self.__medicines
    
    def get_financial_spendings(self):
        return self.__financial_spendings
    
    def get_financial_incomes(self):
        return self.__financial_incomes
    
    def get_personels(self, type):
        try:
            if type == "lab":
                return self.__lab_personels
            elif type == "doctor":
                return self.__doctor_personels
            elif type == "nurse":
                return self.__nurse_personels
            elif type == "receptionist":
                return self.__receptionist_personels
            elif type == "pharmacist":
                return self.__pharmacist_personels
            else:
                return "Error : Invalid type"
        except:
            return "Error : System.get_personels() error"
    
    def get_appointments(self) -> list[Appointment]:
        return self.__appointments
    
    def get_patients(self) -> list[Patient]:
        return self.__patients
    
    def get_pending_prescriptions(self):
        return self.__pending_prescriptions
    
    def get_admissions(self) -> list[Admission]:
        return self.__admissions

    def get_current_number_of_personel(self, type):
        try:
            if type == "lab":
                return len(self.__lab_personels)
            elif type == "doctor":
                return len(self.__doctor_personels)
            elif type == "nurse":
                return len(self.__nurse_personels)
            elif type == "receptionist":
                return len(self.__receptionist_personels)
            elif type == "pharmacist":
                return len(self.__pharmacist_personels)
            else:
                return "Error : Invalid type"
        except:
            return "Error : System.get_current_number_of_personel() error"


    def add_supply(self, name, count, unit, best_before, price, restriction, notes):
        # Add supplies to system's supplies in the form of instance_of_supply
        # Example : [instance_of_supply1, instance_of_supply2, ...]
        # To be able to pass supplies to supply list, they must satisfy following condition
        # 1. count > 0
        # 2. unit is one of the following : "kg", "g", "mg", "l", "ml", "unit", "piece"
        # 3. best before date is in the future, best before date is in seconds counted since epoch
        # If any of the conditions are not satisfied, return "Error : Invalid input"
        try:
            if not count > 0:
                return "Error : Invalid count"
            if not unit in ["kg", "g", "mg", "l", "ml", "unit", "piece"]:
                return "Error : System.add_supply() error, Invalid unit"
            if not best_before > time.time():
                return "Error : System.add_supply() error, Invalid best before date"
            for supplies in self.__supplies:
                if supplies.get_name() == name:
                    supplies.add_count(count)
                    return "Success : Supply count added"
            self.__supplies.append(Supply(name= name, count= count, unit= unit, best_before= best_before, price= price, restriction= restriction, notes= notes))
            return "Success : New supply added"
        except:
            return "Error : System.add_supply() error, Invalid input"

    def add_personel(self, personnel: any) -> tuple[bool, str]:
        if isinstance(personnel, LabPersonnel):
            self.__lab_personels.append(personnel)
        elif isinstance(personnel, Doctor):
            self.__doctor_personels.append(personnel)            
        #elif isinstance(personnel, Nurse):
        elif isinstance(personnel, Receptionist):
            self.__receptionist_personels.append(personnel)     
        elif isinstance(personnel, Pharmacist):
            self.__pharmacist_personels.append(personnel)     
        else:
            return False, f"Error : System.add_personnel(): invalid type for personnel {type(personnel)}"
            
        return True, "Success : Added personnel"

    def add_patient(self, patient: Patient) -> tuple[bool, str]:
        try:
            self.__patients.append(patient)
            return True, "Success : added patient to record"
        except Exception as excp:
            return False, f"Error : {str(excp)}"
            
    def edit_patient(self, patient_to_edit_to: Patient, overwrite_as: Patient):
        index_to_overwrite_to = utils.get_object_index_in_container(container=self.__patients, object=patient_to_edit_to, get_identifier=lambda obj:obj.get_id())
        if index_to_overwrite_to == -1:
            return False, "Error : Cannot find patient"
        overwrite_as.set_id(self.__patients[index_to_overwrite_to].get_id())
        self.__patients[index_to_overwrite_to] = overwrite_as
        return True, "Success : edited patient data"
        
    def deletePatient(self, patient_id) -> tuple[bool, str]:
        index_to_delete_at = utils.get_object_index_in_container_id(container=self.__patients, id=patient_id, get_id=lambda obj:obj.get_id())
        if index_to_delete_at == -1:
            return False, "Error : Could not find patient"
        del self.__patients[index_to_delete_at]
        return True, "Success : deleted patient"
        
    def get_all_patients(self) -> list[Patient]:
        return self.__patients
    def get_all_lab_personnel(self) -> list[LabPersonnel]:
        return self.__lab_personels

    def add_appointment(self, appointment: Appointment) -> tuple[bool, str]:
        try:
            self.__appointments.append(appointment)
            return True, "Success : Appointment added"
        except Exception as excp:
            return False, f"Error : {str(excp)}"
            
    def chg_appointment(self, id, patient_id, doctor_id, date, time):
        try:
            for appointment in self.__appointments:
                if appointment.get_appointment_id() == id:
                    appointment.set_patient_id(patient_id)
                    appointment.set_doctor_id(doctor_id)
                    appointment.set_date(date)
                    appointment.set_time(time)
                    return "Success : Appointment changed"
            return "Error : Appointment not found"
        except:
            return "Error : System.chg_appointment() error"
            
    def removeAppointment(self, appointment_id) -> tuple[bool, str]:
        index_to_delete_at = utils.get_object_index_in_container_id(container=self.__appointments, id=appointment_id, get_id=lambda obj:obj.get_appointment_id())
        if index_to_delete_at == -1:
            return False, "Error : Could not find appointment"
        del self.__appointments[index_to_delete_at]
        return True, "Success : removed appointment"
            
    def get_all_appointments(self) -> list[Appointment]:
        return self.__appointments
            
    def add_admission(self, admisssion):
        try:
            self.__admissions.append(admisssion)
            return True, "Success : Admission added"
        except Exception as excp:
            return False, f"Error : {str(e)}"
            
    def removeAdmission(self, patient_id) -> tuple[bool, str]:
        index_to_delete_at = utils.get_object_index_in_container_id(container=self.__admissions, id=patient_id, get_id=lambda obj:obj.get_patient_id())
        if index_to_delete_at == -1:
            return False, "Error : Could not find appointment"
        del self.__admissions[index_to_delete_at]
        return True, "Success : deleted appointment"        

    def get_all_admissions(self) -> list[Admission]:
        return self.__admissions

    def get_patient_from_id(self, patient_id):
        for patient in self.__patients:
            if patient.get_id() == patient_id:
                return patient
        return None

    def pay_fee(self, fee: Fee, payment_method: PaymentMethod) -> tuple[bool, str]:
        payment_status: tuple[bool, str] = payment_method.pay(fee.get_amount())
        if not payment_status[0]: return payment_status

        fee_owner = self.get_patient_from_id(fee.get_patient_id())
        if fee_owner is None: return False, "Error : unable to find patient with id specified in the fee"
        
        fee_removal_status: tuple[bool, str] = fee_owner.remove_fee(fee)
        if not fee_removal_status[0]:
            payment_method.refund(fee.get_amount())
            return False, "Error : Unable to find the fee in patient. Refunded payment."
        return True, "Success : fee is paid"
        
    def order_lab_test(self, lab_request: LabRequest, lab_personnel_id):
        for lab_personnel in self.__lab_personels:
            if lab_personnel.get_id() == lab_personnel_id:
                lab_personnel.assign_lab_test(lab_request)
                return True, "Success : Ordered lab test"
        return False, "Error : No lab personnel found with specified id"
        
    def verify_prescription(self, prescription: Prescription):
        total_pharmacists: int = len(self.__pharmacist_personels)
        if total_pharmacists == 0: return False, "Error : no pharmacists employed, how is this hospital even working"
        random_pharmacist_index: int = random.randint(0, total_pharmacists)
        self.__pharmacist_personels[random_pharmacist_index].add_prescription_for_verification(prescription)
        return True, "Success : sent prescription for verification with pharmacist"
        
    def queue_prescription(self, prescription: Prescription) -> tuple[bool, str]:
        self.__pending_prescriptions.append(prescription)
        return True, "Success : prescription in queue"
        
    def get_doctor_from_id(self, doctor_id: int) -> Doctor:
        doctor_index: int = utils.get_object_index_in_container_id(container=self.__doctor_personels, id=doctor_id, \
                                                                    get_id=lambda obj:obj.get_id())
        if doctor_index == -1:
            return None
        return self.__doctor_personels[doctor_index]