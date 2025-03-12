class Nurse:
    def __init__(self, id, name, surname, password):
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__password = password
        self.__is_assisting_lab_test = False
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_surname(self):
        return self.__surname
    
    def get_is_assisting_lab_test(self):
        return self.__is_assisting_lab_test
    
    def change_password(self, old_password, new_password):
        if old_password == self.__password:
            self.__password = new_password
            return "Success : Password changed"
        return "Error : Invalid password"
    
    def chg_is_assisting_lab_test(self, status : bool):
        try:
            self.__is_assisting_lab_test = status
            return "Success : is_assisting_lab_test changed"
        except:
            return "Error : Nurse.chg_is_assisting_lab_test() error"
    
    def administer_treatment(self, patient_id, medicine):
        pass

    def assist_lab_test(self, test):
        pass