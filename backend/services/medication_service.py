class Medication:
    current_medication_id = int(0)
    def __init__(self, symptoms:str, diagnosis:str, treatment:str, date:int, finished:bool):
        Medication.current_medication_id += 1
        self.__id = Medication.current_medication_id 
        self.__symptoms = symptoms
        self.__diagnosis = diagnosis
        self.__treatment = treatment
        self.__date = date
        self.__finished = finished
                
    def get_id(self):
        return self.__id
    def get_symptoms(self):
        return self.__symptoms
    
    def set_finished(self, state):
        self.__finished = state

    def get_treatment_as_string(self):
        if self.__has_lab_tests:
            return f"Treatment ID: {self.__id}\nSymptoms    :{self.__symptoms}\nDiagnosis   :{self.__diagnosis}\nTreatment   :{self.__treatment}\nDate        :{self.__date}"
        return f"Treatment ID: {self.__id}\nSymptoms    :{self.__symptoms}\nDiagnosis   :{self.__diagnosis}\nTreatment   :{self.__treatment}\nDate        :{self.__date}"