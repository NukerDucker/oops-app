from Prescription import Prescription
from Doctor import Doctor
import globals
import utils

class Pharmacist:
    current_id = int(0)
    
    def __init__(self, name, surname, password):
        Pharmacist.current_id += 1
        self.__id = Pharmacist.current_id
        self.__name = name
        self.__surname = surname
        self.__password = password
        self.__pending_prescriptions_for_verification: list[Prescription] = []

    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_surname(self):
        return self.__surname
    def get_pending_prescriptions(self) -> list[Prescription]:
        return self.__pending_prescriptions_for_verification
    
    def change_password(self, old_password, new_password) -> tuple[bool, str]:
        if old_password == self.__password:
            self.__password = new_password
            return True, "Success : changed password"
        else: return False, "Error : original password is incorrect"

    def add_prescription_for_verification(self, prescription: Prescription):
        self.__pending_prescriptions_for_verification.append(prescription)
        
    def view_patient_record(self, patient_id: int):
        return globals.get_patient_from_patient_id(patient_id)
        
    def send_prescription_with_feedback(self, prescription_id: int) -> tuple[bool, str]:
        prescription_index: int = get_object_index_in_container_id(container=self.__pending_prescriptions_for_verification, \
                                                                    id=prescription_id, get_id=lambda obj:obj.get_id())
        if prescription_index == -1:
            return False, "Error : approved prescription not in your list"
        prescription: Prescription = self.__pending_prescriptions_for_verification[prescription_index]
        doctor: Doctor = globals.system.get_doctor_from_id(prescription.get_doctor_id())
        if doctor is None:
            return False, "Error : could not find the doctor issuing the prescription"
        doctor.add_disapproved_prescription(prescription)
        del self.__pending_prescriptions_for_verification[prescription_index]
        return True, "Sent prescription feedback"
        
    def add_dispense_pending_prescription(self, prescription: Prescription) -> tuple[bool, str]:
        return globals.system.queue_prescription(prescription)

    def dispense_med(self, ):
        pass