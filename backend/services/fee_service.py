class Fee:
    current_id = int(0)
    def __init__(self, amount, date, patient_id):
        Fee.current_id += 1
        self.__id = Fee.current_id
        self.__amount = amount
        self.__date = date
        self.__patient_id = patient_id
        
    def get_id(self):
        return self.__id
    def get_amount(self):
        return self.__amount
    def get_date(self):
        return self.__date
    def get_patient_id(self):
        return self.__patient_id