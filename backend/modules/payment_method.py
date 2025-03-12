from abc import ABC
from typing import Tuple

class PaymentMethod(ABC):
    """Base class for all payment methods in the hospital system."""
    
    def __init__(self, initial_balance: float) -> None:
        """Initialize a new payment method.
        
        Args:
            initial_balance: The starting balance amount
        
        Raises:
            ValueError: If the initial balance is negative
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Get the current balance.
        
        Returns:
            The current balance amount
        """
        return self._balance
    
    def pay(self, amount: float) -> Tuple[bool, str]:
        """Process a payment from this payment method.
        
        Args:
            amount: The amount to pay
            
        Returns:
            A tuple of (success, message)
        """
        if amount <= 0:
            return False, "Error: Payment amount must be positive"
            
        if amount > self._balance:
            return False, "Error: Not enough balance for payment"
            
        self._balance -= amount
        return True, "Success: Payment successful"
    
    def refund(self, amount: float) -> Tuple[bool, str]:
        """Process a refund to this payment method.
        
        Args:
            amount: The amount to refund
            
        Returns:
            A tuple of (success, message)
        """
        if amount <= 0:
            return False, "Error: Refund amount must be positive"
            
        self._balance += amount
        return True, "Success: Refund processed"