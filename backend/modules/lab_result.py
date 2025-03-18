from typing import Any
from .base_entity import BaseEntity

class LabResult(BaseEntity):
    
    def __init__(self, result: Any) -> None:
        super().__init__()  
        self._result = result
    
    @property
    def lab_id(self) -> int:
        return self.id
    
    @property
    def result(self) -> Any:
        return self._result
    
    @result.setter
    def result(self, value: Any) -> None:
        self._result = value
