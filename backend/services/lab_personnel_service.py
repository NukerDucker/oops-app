from LabRequest import LabRequest
from LabResult import LabResult
from Patient import Patient
import globals

class LabPersonnel:
    current_id = int(0)
    
    def __init__(self, name, surname, password):
        LabPersonnel.current_id += 1 
        self.__id = LabPersonnel.current_id
        self.__name = name
        self.__surname = surname
        self.__password = password
        self.__pending_labs: list[LabRequest] = list()

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id
    def get_name(self):
        return self.__name
    def get_surname(self):
        return self.__surname
    def get_pending_labs(self):
        return self.__pending_labs

    def change_password(self, old_password, new_password):
        if old_password == self.__password:
            self.__password = new_password
            return "Success : Password changed"
        return "Error : Invalid password"
        
    def assign_lab_test(self, lab_request: LabRequest):
        self.__pending_labs.append(lab_request)
        
    def return_lab_result_to_patient(self, lab_request_id, lab_result: LabResult) -> tuple[bool, str]:
        delete_at_index = int(-1)
        for i, pending_lab in enumerate(self.__pending_labs):
            if pending_lab.get_id() == lab_request_id:
                delete_at_index = i
                break
        if delete_at_index == -1:
            return False, "Error : Unable to find the pending lab request"
        
        patient: Patient = globals.system.get_patient_from_id(self.__pending_labs[delete_at_index].get_patient_id())
        if patient is None:
            return False, "Error : Unable to find patient of the lab request"
        del self.__pending_labs[delete_at_index]
        patient.add_lab_result(lab_result)
        return True, "Success : Added lab result to patient"