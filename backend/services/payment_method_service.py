
class PaymentMethod:
    def __init__(self, initial_balance: float):
        self.__balance = initial_balance
    
    def pay(self, amount) -> tuple[bool, str]:
        if(amount > self.__balance):
            return False, "Error : Not enough balance for payment"
        self.__balance -= amount
        return True, "Success : Payment successful"
    def refund(self, amount) -> None:
        self.__balance += amount