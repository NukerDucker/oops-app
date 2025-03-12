from Fee import Fee
from LabResult import LabResult
from Medication import Medication
from Prescription import Prescription
import utils

class Patient:
    current_id = int(0)
    
    def __init__(self, name, age, gender, increment_id: bool = True):
        if increment_id: Patient.current_id += 1
        self.__id = Patient.current_id
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__history = []
        self.__medications: list[Medication] = []
        self.__fees: list[Fee] = []
        self.__lab_results: list[LabResult] = []
        self.__prescription_history: list[Prescription] = []

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id
    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_gender(self):
        return self.__gender
    def get_history(self):
        self.__history.append()
    def get_current_medication(self):
        self.__current_medication.append()
    def gen_report(self):
        pass

    def add_fee(self, fee: Fee):
        self.__fees.append(fee)

    def remove_fee(self, fee: Fee) -> tuple[bool, str]:
        delete_at_index = utils.get_object_index_in_container(self.__fees, fee, lambda obj: obj.get_id())
        if delete_at_index == -1:
            return False, "Error : could not find fee in patient's list"
        del self.__fees[delete_at_index]
        return True, "Success : removed fee from patient"
    
    def get_all_fees(self) -> list[Fee]:
        return self.__fees
        
    def add_lab_result(self, lab_result):
        self.__lab_results.append(lab_result)
    def get_lab_results(self) -> list[LabResult]:
        return self.__lab_results
        
    def add_medication(self, medication: Medication):
        self.__medications.append(medication)
    def get_all_medications(self) -> list[Medication]:
        return self.__medications
        
    #addFinancialIncome
    #addFinancialspending
    #calculateFee