    
class FinancialReport:
    def __init__(self, type: str, amount: float, description: str):
        self.__type = type
        self.__amount = amount
        self.__description = description
        
    def get_date(self):
        return self.__date
    
    def get_amount(self):
        return self.__amount
    
    def get_description(self):
        return self.__description