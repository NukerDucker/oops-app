from typing import List, Optional, Tuple
from .base_entity import BaseEntity
from .lab_result import LabResult
from .prescription import Prescription
from .medication import Medication
from .fee import Fee
from .treatment import Treatment

class Patient(BaseEntity):
    
    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        contact: str
    ) -> None:
        super().__init__()
        
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Patient name must be a non-empty string")
        self._name = name
        
        
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Patient age must be a positive integer")
        self._age = age
        
        
        if not isinstance(gender, str) or not gender.strip():
            raise ValueError("Patient gender must be a non-empty string")
        self._gender = gender
        
        
        if not isinstance(contact, str) or not contact.strip():
            raise ValueError("Patient contact must be a non-empty string")
        self._contact = contact
        
        
        self._history: List[str] = []
        self._lab_results: List[LabResult] = []
        self._prescriptions: List[Prescription] = []
        self._medications: List[Medication] = []
        self._fees: List[Fee] = []
        self._treatments: List[Treatment] = []
    
    @property
    def patient_id(self) -> int:
        return self.id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def age(self) -> int:
        return self._age
    
    @property
    def gender(self) -> str:
        return self._gender
    
    @property
    def contact(self) -> str:
        return self._contact
    
    @property
    def history(self) -> List[str]:
        return self._history.copy()  
    
    def add_history_entry(self, entry: str) -> Tuple[bool, str]:
        
        if not isinstance(entry, str) or not entry.strip():
            return False, "Error: History entry must be a non-empty string"
        
        self._history.append(entry)
        return True, "Success: History entry added"
    
    @property
    def current_medications(self) -> List[Medication]:
        return [med for med in self._medications if not med.finished]
    
    def get_report_data(self) -> dict:
        current_meds = self.current_medications
        
        return {
            "id": self.id,
            "name": self._name,
            "age": self._age,
            "gender": self._gender,
            "contact": self._contact,
            "history": self._history.copy(),
            "current_medications": current_meds,
            "lab_results": self._lab_results.copy(),
            "total_fees": sum(fee.amount for fee in self._fees)
        }
    
    
    def add_lab_result(self, lab_result: LabResult) -> Tuple[bool, str]:
        
        if not isinstance(lab_result, LabResult):
            return False, "Error: Invalid lab result object"
        
        self._lab_results.append(lab_result)
        return True, "Success: Lab result added"
    
    def get_lab_results(self) -> List[LabResult]:
        return self._lab_results.copy()  
    
    def get_lab_result(self, lab_result_id: int) -> Optional[LabResult]:
        
        if not isinstance(lab_result_id, int) or lab_result_id <= 0:
            return None
            
        for result in self._lab_results:
            if result.id == lab_result_id:
                return result
        return None
    
    def update_lab_result(self, lab_result_id: int, updated_result: LabResult) -> Tuple[bool, str]:
        
        if not isinstance(lab_result_id, int) or lab_result_id <= 0:
            return False, "Error: Invalid lab result ID"
        if not isinstance(updated_result, LabResult):
            return False, "Error: Invalid lab result object"
        
        for i, result in enumerate(self._lab_results):
            if result.id == lab_result_id:
                if lab_result_id != updated_result.id:
                    return False, "Error: Cannot change lab result ID"
                self._lab_results[i] = updated_result
                return True, "Success: Lab result updated"
        return False, "Error: Lab result not found"
    
    def remove_lab_result(self, lab_result_id: int) -> Tuple[bool, str]:
        
        if not isinstance(lab_result_id, int) or lab_result_id <= 0:
            return False, "Error: Invalid lab result ID"
            
        for i, result in enumerate(self._lab_results):
            if result.id == lab_result_id:
                self._lab_results.pop(i)
                return True, "Success: Lab result removed"
        return False, "Error: Lab result not found"
    
    
    def add_prescription(self, prescription: Prescription) -> Tuple[bool, str]:
        
        if not isinstance(prescription, Prescription):
            return False, "Error: Invalid prescription object"
            
        self._prescriptions.append(prescription)
        return True, "Success: Prescription added"
    
    def get_prescriptions(self) -> List[Prescription]:
        return self._prescriptions.copy()  
    
    def get_prescription(self, prescription_id: int) -> Optional[Prescription]:
        
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return None
            
        for prescription in self._prescriptions:
            if prescription.id == prescription_id:
                return prescription
        return None
    
    def update_prescription(self, prescription_id: int, updated_prescription: Prescription) -> Tuple[bool, str]:
        
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return False, "Error: Invalid prescription ID"
        if not isinstance(updated_prescription, Prescription):
            return False, "Error: Invalid prescription object"
            
        for i, prescription in enumerate(self._prescriptions):
            if prescription.id == prescription_id:
                if prescription_id != updated_prescription.id:
                    return False, "Error: Cannot change prescription ID"
                self._prescriptions[i] = updated_prescription
                return True, "Success: Prescription updated"
        return False, "Error: Prescription not found"
    
    def remove_prescription(self, prescription_id: int) -> Tuple[bool, str]:
        
        if not isinstance(prescription_id, int) or prescription_id <= 0:
            return False, "Error: Invalid prescription ID"
            
        for i, prescription in enumerate(self._prescriptions):
            if prescription.id == prescription_id:
                self._prescriptions.pop(i)
                return True, "Success: Prescription removed"
        return False, "Error: Prescription not found"
    
    
    def add_medication(self, medication: Medication) -> Tuple[bool, str]:
        
        if not isinstance(medication, Medication):
            return False, "Error: Invalid medication object"
            
        self._medications.append(medication)
        return True, "Success: Medication added"
    
    def get_medications(self) -> List[Medication]:
        return self._medications.copy()  
    
    def get_medication(self, medication_id: int) -> Optional[Medication]:
        if not isinstance(medication_id, int) or medication_id <= 0:
            return None
            
        for medication in self._medications:
            if medication.id == medication_id:
                return medication
        return None
    
    def update_medication(self, medication_id: int, updated_medication: Medication) -> Tuple[bool, str]:
        
        if not isinstance(medication_id, int) or medication_id <= 0:
            return False, "Error: Invalid medication ID"
        if not isinstance(updated_medication, Medication):
            return False, "Error: Invalid medication object"
            
        for i, medication in enumerate(self._medications):
            if medication.id == medication_id:
                if medication_id != updated_medication.id:
                    return False, "Error: Cannot change medication ID"
                self._medications[i] = updated_medication
                return True, "Success: Medication updated"
        return False, "Error: Medication not found"
    
    def remove_medication(self, medication_id: int) -> Tuple[bool, str]:
        
        if not isinstance(medication_id, int) or medication_id <= 0:
            return False, "Error: Invalid medication ID"
            
        for i, medication in enumerate(self._medications):
            if medication.id == medication_id:
                self._medications.pop(i)
                return True, "Success: Medication removed"
        return False, "Error: Medication not found"
    
    
    def add_treatment(self, treatment: Treatment) -> Tuple[bool, str]:
        
        if not isinstance(treatment, Treatment):
            return False, "Error: Invalid treatment object"
            
        self._treatments.append(treatment)
        return True, "Success: Treatment added"
    
    def get_treatments(self) -> List[Treatment]:
        return self._treatments.copy()  
    
    def get_treatment(self, treatment_id: int) -> Optional[Treatment]:
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return None
            
        for treatment in self._treatments:
            if treatment.id == treatment_id:
                return treatment
        return None
    
    def update_treatment(self, treatment_id: int, updated_treatment: Treatment) -> Tuple[bool, str]:
        
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return False, "Error: Invalid treatment ID"
        if not isinstance(updated_treatment, Treatment):
            return False, "Error: Invalid treatment object"
            
        for i, treatment in enumerate(self._treatments):
            if treatment.id == treatment_id:
                if treatment_id != updated_treatment.id:
                    return False, "Error: Cannot change treatment ID"
                self._treatments[i] = updated_treatment
                return True, "Success: Treatment updated"
        return False, "Error: Treatment not found"
    
    def remove_treatment(self, treatment_id: int) -> Tuple[bool, str]:
        
        if not isinstance(treatment_id, int) or treatment_id <= 0:
            return False, "Error: Invalid treatment ID"
            
        for i, treatment in enumerate(self._treatments):
            if treatment.id == treatment_id:
                self._treatments.pop(i)
                return True, "Success: Treatment removed"
        return False, "Error: Treatment not found"
    
    
    def add_fee(self, fee: Fee) -> Tuple[bool, str]:
        
        if not isinstance(fee, Fee):
            return False, "Error: Invalid fee object"
            
        self._fees.append(fee)
        return True, "Success: Fee added"
    
    def get_fees(self) -> List[Fee]:
        return self._fees.copy()  
    
    def get_fee(self, fee_id: int) -> Optional[Fee]:
        
        if not isinstance(fee_id, int) or fee_id <= 0:
            return None
            
        for fee in self._fees:
            if fee.id == fee_id:
                return fee
        return None
    
    def update_fee(self, fee_id: int, updated_fee: Fee) -> Tuple[bool, str]:
        
        if not isinstance(fee_id, int) or fee_id <= 0:
            return False, "Error: Invalid fee ID"
        if not isinstance(updated_fee, Fee):
            return False, "Error: Invalid fee object"
            
        for i, fee in enumerate(self._fees):
            if fee.id == fee_id:
                if fee_id != updated_fee.id:
                    return False, "Error: Cannot change fee ID"
                self._fees[i] = updated_fee
                return True, "Success: Fee updated"
        return False, "Error: Fee not found"
    
    def remove_fee(self, fee_id: int) -> Tuple[bool, str]:
        
        if not isinstance(fee_id, int) or fee_id <= 0:
            return False, "Error: Invalid fee ID"
            
        for i, fee in enumerate(self._fees):
            if fee.id == fee_id:
                self._fees.pop(i)
                return True, "Success: Fee removed"
        return False, "Error: Fee not found"
    
    def calculate_total_fees(self) -> float:
        return sum(fee.amount for fee in self._fees)
