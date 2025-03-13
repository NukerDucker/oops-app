from typing import Tuple
import time
from .base_entity import BaseEntity

class Supply(BaseEntity):
    """Represents a medical supply in the inventory."""
    
    def __init__(
        self,
        name: str,
        quantity: int,
        unit_price: float,
        category: str
    ) -> None:
        """Initialize a new Supply."""
        super().__init__()
        self._name = name
        self._quantity = quantity
        self._unit_price = unit_price
        self._category = category
    
    @property
    def name(self) -> str:
        """Get the supply name."""
        return self._name
    
    @property
    def quantity(self) -> int:
        """Get the supply quantity."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set the supply quantity."""
        self._quantity = max(0, value)
    
    @property
    def unit_price(self) -> float:
        """Get the unit price."""
        return self._unit_price
    
    @unit_price.setter
    def unit_price(self, value: float) -> None:
        """Set the unit price."""
        self._unit_price = max(0, value)
    
    @property
    def category(self) -> str:
        """Get the supply category."""
        return self._category
    
    def total_value(self) -> float:
        """Calculate the total value of the supply."""
        return self._quantity * self._unit_price