from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from abc import ABC, abstractmethod

from polish_salary_calc.salary.salary_utilities import SalaryUtilities


@dataclass
class ContractSettngs(ABC):
    name: str | None = None
    current_month_gross_sum: Decimal = Decimal('0.0')
    social_security_base_sum: Decimal = Decimal('0.0')
    cost_fifty_sum: Decimal = Decimal('0.0')
    tax_base_sum: Decimal = Decimal('0.0')
    employee_ppk: Decimal = Decimal('0.0')
    employer_ppk: Decimal = Decimal('0.0')
    accident_insurance_rate: Decimal | None = None
    salary_deductions: Decimal = Decimal('0.0')

    def __str__(self) -> str:
        return SalaryUtilities.print_dict(self.to_dict())

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    def options_type(self):
        return self.__class__.__name__