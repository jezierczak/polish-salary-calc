from dataclasses import dataclass
from decimal import Decimal

@dataclass
class AbstractSalaryOptions:
    current_month_gross_sum: Decimal = Decimal('0.0')
    social_security_base_sum: Decimal = Decimal('0.0')
    cost_fifty_sum: Decimal = Decimal('0.0')
    tax_base_sum: Decimal = Decimal('0.0')
    employee_ppk: Decimal = Decimal('0.0')
    employer_ppk: Decimal = Decimal('0.0')
    accident_insurance_rate: Decimal | None = None
    salary_deductions: Decimal = Decimal('0.0')