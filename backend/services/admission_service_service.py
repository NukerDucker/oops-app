class Admission:
    current_id = int(0)
    
    def __init__(self, patient_id, doctor_id, date, time):
        Admission.current_id += 1
        self.__id = Admission.current_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__time = time

    def get_id(self):
        return self.__id
    def get_patient_id(self):
        return self.__patient_id
    def get_doctor_id(self):
        return self.__doctor_id
    def get_date(self):
        return self.__date
    def get_time(self):
        return self.__time