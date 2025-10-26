
from polish_salary_calc.salary.abstract_salary_options import AbstractSalaryOptions
from typing import TypedDict,Self
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, IntEnum


class SelfEmploymentType(Enum):
    COMMON = 1
    PREFERRED = 2
    STARTUP_RELIEF = 3
    UNREGISTERED_BUSINESS = 4
    #SMALL_ZUS = 5

class TaxType(Enum):
    STANDARD = 1
    LINE_TAX = 2
    A_LUMP_SUM = 3

class HealthBase(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

LUMP_RATES_ALLOWED ={
    Decimal('0.02'),Decimal('0.03'),Decimal('0.055'),Decimal('0.085'),Decimal('0.10'),Decimal('0.12'),Decimal('0.14'),Decimal('0.15'),Decimal('0.17')
}

class SelfEmploymentOptionsDict(TypedDict):
    self_employment_type: SelfEmploymentType
    tax_type: TaxType
    tax_lump_rate: Decimal
    health_base: HealthBase
    employer_pension_contribution_rate: Decimal
    is_sick_pay: bool
    sick_pay_days: int
    month_days: int
    is_fp:bool
    other_minimum_contract:bool
    # average_social_income_previous_year:Decimal
    #is_a_lump_sum: bool
    costs: Decimal
    current_month_gross_sum: Decimal
    social_security_base_sum: Decimal
    #cost_fifty_sum: Decimal
    tax_base_sum: Decimal
    #employee_ppk: Decimal
    #employer_ppk: Decimal
    accident_insurance_rate: Decimal | None
    salary_deductions: Decimal

@dataclass
class SelfEmploymentOptions(AbstractSalaryOptions):

    self_employment_type: SelfEmploymentType = SelfEmploymentType.COMMON
    tax_type: TaxType = TaxType.STANDARD
    tax_lump_rate: Decimal = Decimal('0.17')
    health_base: HealthBase = HealthBase.NONE
    is_sick_pay: bool = False
    sick_pay_days: int = 0
    month_days: int = 0
    is_fp:bool = True
    other_minimum_contract:bool = False
    # average_social_income_previous_year:Decimal= Decimal('0.0')
    #is_a_lump_sum: bool = False
    costs: Decimal = Decimal('0.0')

    @classmethod
    def from_dict(cls, data: SelfEmploymentOptionsDict) -> Self:
        return cls(**data)

    @classmethod
    def builder(cls) -> 'Builder':
        return cls.Builder()

    class Builder:
        def __init__(self):
            self._options = SelfEmploymentOptions()

        def set_self_employment_type(self, self_employment_type: SelfEmploymentType) -> Self:
            self._options.self_employment_type = self_employment_type
            return self

        def set_tax_type(self, tax_type: TaxType) -> Self:
            self._options.tax_type = tax_type
            return self
        def set_tax_lump_rate(self, tax_lump_rate: Decimal) -> Self:
            self._options.tax_lump_rate = tax_lump_rate
            return self
        def set_health_base(self, health_base: HealthBase) -> Self:
            self._options.health_base = health_base
            return self

        def set_sick_pay(self,  is_sick_pay: bool, sick_pay_days: int = 0, month_days: int = 0) -> Self:
            self._options.is_sick_pay =  is_sick_pay
            self._options.sick_pay_days = sick_pay_days
            self._options.month_days = month_days
            return self

        def is_fp(self, is_fp: bool) -> Self:
            self._options.is_fp = is_fp
            return self

        def is_other_minimum_contract(self, other_minimum_contract: bool) -> Self:
            self._options.other_minimum_contract = other_minimum_contract
            return self

        # def set_average_social_income_previous_year(self, average_social_income_previous_year: Decimal) -> Self:
        #     self._options.average_social_income_previous_year = average_social_income_previous_year
        #     return self

        def set_costs(self, costs: Decimal) -> Self:
            self._options.costs = costs
            return self
        # def  is_a_lump_sum(self,  is_a_lump_sum: bool) -> Self:
        #     self._options. is_a_lump_sum =  is_a_lump_sum
        #     return self

        def set_current_month_gross_sum(self, current_month_gross_sum: Decimal) -> Self:
             self._options.current_month_gross_sum = current_month_gross_sum
             return self
        def set_social_security_base_sum(self, social_security_base_sum: Decimal) -> Self:
            self._options.social_security_base_sum = social_security_base_sum
            return self
        # def set_cost_fifty_sum(self, cost_fifty_sum: Decimal) -> Self:
        #     self._options.cost_fifty_sum = cost_fifty_sum
        #     return self
        def set_tax_base_sum(self, tax_base_sum: Decimal) -> Self:
            self._options.tax_base_sum = tax_base_sum
            return self

        def set_accident_insurance_rate(self, accident_insurance_rate: Decimal | None) -> Self:
             self._options.accident_insurance_rate = accident_insurance_rate
             return self
        def set_salary_deductions(self, salary_deductions: Decimal) -> Self:
            self._options.salary_deductions = salary_deductions
            return self
        def build(self) -> 'SelfEmploymentOptions':
            return self._options