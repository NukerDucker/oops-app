from datetime import date
from typing import Optional
from .base_entity import BaseEntity

class FinancialReport(BaseEntity):
    
    def __init__(
        self, 
        report_type: str, 
        amount: float, 
        description: str,
        report_date: date = None
    ) -> None:
        super().__init__()  
        self._report_type = report_type
        self._amount = amount
        self._description = description
        self._date = report_date or date.today()
    
    @property
    def report_id(self) -> int:
        return self.id
    
    @property
    def report_type(self) -> str:
        return self._report_type
    
    @property
    def date(self) -> date:
        return self._date
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def description(self) -> str:
        return self._description
    
    def update_amount(self, new_amount: float) -> None:
        self._amount = new_amount
