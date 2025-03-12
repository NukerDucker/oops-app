class LabResult:
    current_id = int(0)
# Class "LabResult" is used to store the lab test results of a patient
# Lab test results include the test ID, test result
# Lab test results can be accessed by get_result() method

    def __init__(self, result):
        LabResult.current_id += 1
        self.__id = LabResult.current_id 
        self.__result = result       
        
    def get_id(self):
        return self.__id
    def get_result(self):
        return self.__result