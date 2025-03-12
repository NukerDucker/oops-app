class Appointment:
    current_id = int(0)
    
    def __init__(self, patient_id, doctor_id, date, time):
        Appointment.current_id += 1
        self.__appointment_id = Appointment.current_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__date = date
        self.__time = time
        
    def get_appointment_id(self):
        return self.__appointment_id
    def get_patient_id(self):
        return self.__patient_id
    def get_doctor_id(self):
        return self.__doctor_id
    def set_doctor_id(self, doc_id):
        self.__doctor_id = doc_id
    def get_date(self):
        return self.__date
    def get_time(self):
        return self.__time

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id
    def set_doctor_id(self, doctor_id):
        self.__doctor_id = doctor_id
    def set_date(self, date):
        self.__date = date
    def set_time(self, time):
        self.__time = time