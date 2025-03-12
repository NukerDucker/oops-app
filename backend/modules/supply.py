from typing import Tuple
import time
from .base_entity import BaseEntity

class Supply(BaseEntity):
    def __init__(
        self, 
        name: str, 
        count: int, 
        best_before: int = None, 
        price: float = 0, 
        unit: str = 'piece(s)', 
        restriction: str = 'No restrictions', 
        notes: str = 'No notes'
    ):
        super().__init__()
        self._name = name
        self._count = count
        self._unit = unit
        self._best_before = best_before if best_before is not None else 'Not specified'
        self._price = price
        self._restriction = restriction
        self._notes = notes
        
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def count(self) -> int:
        return self._count
    
    @property
    def unit(self) -> str:
        return self._unit
    
    @property
    def best_before(self) -> int:
        return self._best_before
    
    @property
    def price(self) -> float:
        return self._price
    
    @property
    def restriction(self) -> str:
        return self._restriction
    
    @property
    def notes(self) -> str:
        return self._notes
    
    def add_count(self, count: int) -> Tuple[bool, str]:
        if count < 0:
            return False, "Error: Invalid count"
        self._count += count
        return True, "Success: Count added"
    
    def remove_count(self, count: int) -> Tuple[bool, str]:
        if count < 0:
            return False, "Error: Invalid count"
        if self._count - count < 0:
            return False, "Error: Not enough supply"
        self._count -= count
        return True, "Success: Count removed"
        
    def update_count(self, count: int) -> Tuple[bool, str]:
        if count < 0:
            return False, "Error: Invalid count"
        self._count = count
        return True, "Success: Count updated"
        
    def update_unit(self, unit: str) -> Tuple[bool, str]:
        valid_units = ["kg", "g", "mg", "l", "ml", "unit", "piece(s)"]
        if unit not in valid_units:
            return False, "Error: Invalid unit"
        self._unit = unit
        return True, "Success: Unit updated"
        
    def update_best_before(self, best_before: int) -> Tuple[bool, str]:
        if best_before <= time.time():
            return False, "Error: Invalid best before date"
        self._best_before = best_before
        return True, "Success: Best before date updated"
        
    def update_price(self, price: float) -> Tuple[bool, str]:
        if price < 0:
            return False, "Error: Invalid price"
        self._price = price
        return True, "Success: Price updated"
        
    def update_restriction(self, restriction: str) -> Tuple[bool, str]:
        self._restriction = restriction
        return True, "Success: Restriction updated"
        
    def update_notes(self, notes: str) -> Tuple[bool, str]:
        self._notes = notes
        return True, "Success: Notes updated"