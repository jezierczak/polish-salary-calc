from decimal import Decimal
from enum import Enum
from typing import TypedDict

from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.options.self_employment_options import SelfEmploymentOptions
from polish_salary_calc.options.work_contract_options import WorkContractOptions
from polish_salary_calc.options.employment_contract_options import EmploymentContractOptions
from polish_salary_calc.options.mandate_contract_options import MandateContractOptions
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.salary import SalaryType, Salary,SalaryDict


class Months(Enum):
    JAN = "JAN"
    FEB = "FEB"
    MAR = "MAR"
    APR = "APR"
    MAY = "MAY"
    JUN = "JUN"
    JUL = "JUL"
    AUG = "AUG"
    SEP = "SEP"
    OCT = "OCT"
    NOV = "NOV"
    DEC = "DEC"

class ContractOptions(TypedDict):
    rates: Rates  | None
    options: EmploymentContractOptions | MandateContractOptions | SelfEmploymentOptions | WorkContractOptions | None
    salary_base: Decimal | None
    salary_type: SalaryType
    enabled: bool


class YearContractService:
    def __init__(self,
                 default_rates:Rates | None = None,
                 default_options: EmploymentContractOptions | MandateContractOptions | SelfEmploymentOptions | WorkContractOptions | None = None,
                 default_salary_base: Decimal | None = None,
                 default_salary_type: SalaryType= SalaryType.GROSS
                 ) -> None:

        self.default_rates: Rates | None = default_rates
        self.default_options: EmploymentContractOptions | MandateContractOptions | SelfEmploymentOptions | WorkContractOptions | None = default_options
        self.default_salary_base: Decimal | None = default_salary_base
        self.default_salary_type: SalaryType = default_salary_type

        self.is_calculated: bool = False

        self.monthly_contract_options: dict[Months, ContractOptions] = {}
        self.monthly_contract_calculated_data: dict[Months,Salary] = {}
        self.summary:Salary = Salary()

    def calculate(self) -> None:
        social_security_base_sum: Decimal = Decimal('0.0')
        cost_fifty_sum: Decimal = Decimal('0.0')
        tax_base_sum: Decimal = Decimal('0.0')

        self._set_empty_months_options_to_default()

        for month in Months:
            mco = self.monthly_contract_options[month]
            if not mco["enabled"] or not mco["options"] or not mco["rates"] or not mco["salary_base"]:
                self.monthly_contract_calculated_data[month] = Salary()
                continue

            mco["options"].social_security_base_sum = social_security_base_sum
            mco["options"].cost_fifty_sum = cost_fifty_sum
            mco["options"].tax_base_sum = tax_base_sum

            if isinstance(mco["options"],EmploymentContractOptions):
                contract = EmploymentContract(mco["rates"],mco["options"])
            elif isinstance(mco["options"],MandateContractOptions):
                contract = MandateContract(mco["rates"],mco["options"])
            elif isinstance(mco["options"],SelfEmploymentOptions):
                contract = SelfEmployment(mco["rates"],mco["options"])
            elif isinstance(mco["options"],WorkContractOptions):
                contract = WorkContract(mco["rates"],mco["options"])
            else: raise NotImplementedError("Contract options not implemented")

            contract.calculate(mco["salary_base"],mco["salary_type"])
            self.monthly_contract_calculated_data[month] = contract

            social_security_base_sum = contract.social_security_base_total
            cost_fifty_sum = contract.cost_fifty_total
            tax_base_sum = contract.tax_base_total

            self.summary += contract

        self.is_calculated = True


    def set_month_contract(self,
                            month: Months,
                            rates:Rates | None = None,
                            options: EmploymentContractOptions | MandateContractOptions | SelfEmploymentOptions | WorkContractOptions | None = None,
                            salary_base: Decimal | None = None,
                            salary_type: SalaryType= SalaryType.GROSS
                            ) -> None:
        enabled=True
        if rates is None:
            rates = self.default_rates
        if options is None:
            options = self.default_options
        if salary_base is None:
            salary_base = self.default_salary_base
            if salary_base is None:
                enabled=False
            else: enabled=True
        self.monthly_contract_options[month]={"rates": rates,"options": options,"salary_base": salary_base,"salary_type": salary_type,"enabled":enabled}

    def _set_empty_months_options_to_default(self) -> None:
        for month in Months:
            if self.monthly_contract_options.get(month) is None:
                self.set_month_contract(month)
