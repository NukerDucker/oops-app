from typing import Tuple
import time
from .base_entity import BaseEntity

class Supply(BaseEntity):
    
    def __init__(
        self,
        name: str,
        quantity: int,
        unit_price: float,
        category: str
    ) -> None:
        super().__init__()
        self._name = name
        self._quantity = quantity
        self._unit_price = unit_price
        self._category = category
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = max(0, value)
    
    @property
    def unit_price(self) -> float:
        return self._unit_price
    
    @unit_price.setter
    def unit_price(self, value: float) -> None:
        self._unit_price = max(0, value)
    
    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, value: str) -> None:
        self._category = value
    
    def total_value(self) -> float:
        return self._quantity * self._unit_price
