class Prescription:
    current_id = int(0)
    
    def __init__(self, patient_id, amount):
        Prescription.current_id += 1
        self.__patient_id = patient_id
        self.__amount = []
        self.__feedback: tuple[bool, str] = ()
        self.__id = Prescription.current_id
        
    def set_feedback(self, feedback: tuple[bool, str]):
        self.__feedback = feedback
    def get_feedback(self) -> tuple[bool, str]:
        return self.__feedback