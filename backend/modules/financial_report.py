from datetime import date
from typing import Optional
from .base_entity import BaseEntity

class FinancialReport(BaseEntity):
    """Represents a financial report in the hospital system."""
    
    def __init__(
        self, 
        report_type: str, 
        amount: float, 
        description: str,
        report_date: date = None
    ) -> None:
        """Initialize a new financial report.
        
        Args:
            report_type: The type of financial report
            amount: The monetary amount associated with the report
            description: A description of the financial report
            report_date: The date of the report (defaults to None)
        """
        super().__init__()  # Generate the unique ID using the base class
        self._report_type = report_type
        self._amount = amount
        self._description = description
        self._date = report_date or date.today()
    
    @property
    def report_id(self) -> int:
        """Get the report's unique identifier."""
        return self.id
    
    @property
    def report_type(self) -> str:
        """Get the type of financial report."""
        return self._report_type
    
    @property
    def date(self) -> date:
        """Get the date of the financial report."""
        return self._date
    
    @property
    def amount(self) -> float:
        """Get the amount associated with the report."""
        return self._amount
    
    @property
    def description(self) -> str:
        """Get the description of the report."""
        return self._description
    
    def update_amount(self, new_amount: float) -> None:
        """Update the amount in the financial report.
        
        Args:
            new_amount: The new monetary amount
        """
        self._amount = new_amount