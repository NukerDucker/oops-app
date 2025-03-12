import globals
from Patient import Patient
from Appointment import Appointment
from Admission import Admission
from Fee import Fee
from PaymentMethod import PaymentMethod

class Receptionist:
    def __init__(self, name, surname, password):
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__password = password

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_surname(self):
        return self.__surname

    #bro just let me use friend like c++ ffs i hate python :sob:
    def get_password(self):
        return self.__password
        
    def change_password(self, old_password, new_password) -> tuple[bool, str]:
        if self.__password == old_password:
            self.__password = new_password
            return True, "Successfully changed password"
        return False, "Error: Incorrect old password" 
    
    def reg_patient(self, patient: Patient) -> tuple[bool, str]:
        return globals.system.add_patient(patient)
        
    def updatePatientRecord(self, patient_to_edit_to: Patient, overwrite_as: Patient) -> tuple[bool, str]:
        return globals.system.edit_patient(patient_to_edit_to=patient_to_edit_to, overwrite_as=overwrite_as)
        
    def deletePatient(self, patient_id) -> tuple[bool, str]:
        return globals.system.deletePatient(patient_id)
        
    #how would this work - just return the entire patient info or use the edit screen or smth
    def searchForPatientInfo(self):
        pass

    def scheduleAppointment(self, appointment: Appointment) -> tuple[bool, str]:
        return globals.system.add_appointment(appointment)

    def cancelAppointment(self, appointment_id) -> tuple[bool, str]:
        return globals.system.removeAppointment(appointment_id)
    
    def admitPatient(self, admisssion: Admission) -> tuple[bool, str]:
        return globals.system.add_admission(admisssion)

    def dischargePatient(self, patient_id) -> tuple[bool, str]:
        return globals.system.removeAdmission(patient_id)
    
    def handlePatientFeePayment(self, fee: Fee, payment_method: PaymentMethod) -> tuple[bool, str]:
        return globals.system.pay_fee(fee=fee, payment_method=payment_method)
        