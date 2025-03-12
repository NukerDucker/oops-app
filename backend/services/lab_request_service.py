class LabRequest:
    current_id = int(0)
    def __init__(self, patient_id, type, date, time):
        LabRequest.current_id += 1
        
        self.__patient_id = patient_id
        self.__type = type
        self.__date = date
        self.__time = time
        self.__id = LabRequest.current_id
        
    def get_id(self):
        return self.__id
    def get_patient_id(self):
        return self.__patient_id