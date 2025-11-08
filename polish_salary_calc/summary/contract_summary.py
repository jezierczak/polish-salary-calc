from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import TypedDict, override

import pandas as pd

from polish_salary_calc.console_printer.exporter import SalaryExporter
from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.contract_settings.self_employment_settings import SelfEmploymentSettings
from polish_salary_calc.contract_settings.work_contract_settings import WorkContractSettings
from polish_salary_calc.contract_settings.employment_contract_settings import EmploymentContractSettings
from polish_salary_calc.contract_settings.mandate_contract_settings import MandateContractSettings
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.salary import SalaryType, Salary



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

class ContractSettings(TypedDict):
    rates: Rates  | None
    contract_settings: EmploymentContractSettings | MandateContractSettings | SelfEmploymentSettings | WorkContractSettings | None
    salary_base: Decimal | None
    salary_type: SalaryType
    enabled: bool


class YearContractService(Salary):
    def __init__(self,
                 default_rates:Rates,
                 contract_settings: EmploymentContractSettings | MandateContractSettings | SelfEmploymentSettings | WorkContractSettings,
                 default_salary_base: Decimal,
                 default_salary_type: SalaryType= SalaryType.GROSS
                 ) -> None:
        super().__init__(default_rates, contract_settings)
        # self.contract_settings: EmploymentContractSettings | MandateContractSettings | SelfEmploymentSettings | WorkContractSettings = contract_settings
        # self.default_rates: Rates = default_rates
        self.default_salary_base: Decimal = default_salary_base
        self.default_salary_type: SalaryType = default_salary_type

        # self.is_calculated: bool = False

        self._monthly_contract_parameters: dict[Months, ContractSettings] = {}
        self._monthly_contract_calculated_data: dict[Months,Salary] = {}
        # self.summary:Salary = Salary(self.rates,self.contract_settings)

        self._set_empty_months_options_to_default()



    def calculate(self) -> None:
        social_security_base_sum: Decimal = self.contract_settings.social_security_base_sum
        cost_fifty_sum: Decimal = self.contract_settings.cost_fifty_sum
        tax_base_sum: Decimal = self.contract_settings.tax_base_sum

        for month in Months:
            mco = self._monthly_contract_parameters[month]
            if not mco["enabled"] or not mco["contract_settings"] or not mco["rates"] or not mco["salary_base"]:
                self._monthly_contract_calculated_data[month] = Salary(self.rates, self.contract_settings)
                continue

            mco["contract_settings"].social_security_base_sum = social_security_base_sum
            mco["contract_settings"].cost_fifty_sum = cost_fifty_sum
            mco["contract_settings"].tax_base_sum = tax_base_sum
            # contract: EmploymentContract | MandateContract | SelfEmployment | WorkContract | None = None
            if isinstance(mco["contract_settings"], EmploymentContractSettings):
                contract = EmploymentContract(mco["rates"],mco["contract_settings"])
            elif isinstance(mco["contract_settings"], MandateContractSettings):
                contract = MandateContract(mco["rates"],mco["contract_settings"])
            elif isinstance(mco["contract_settings"], SelfEmploymentSettings):
                contract = SelfEmployment(mco["rates"],mco["contract_settings"])
            elif isinstance(mco["contract_settings"], WorkContractSettings):
                contract = WorkContract(mco["rates"],mco["contract_settings"])
            else: raise NotImplementedError("Contract contract_settings not implemented")

            contract.calculate(mco["salary_base"],mco["salary_type"])
            contract.name = month.name
            self._monthly_contract_calculated_data[month] = contract

            social_security_base_sum = contract.social_security_base_total
            cost_fifty_sum = contract.cost_fifty_total
            tax_base_sum = contract.tax_base_total

            super().__iadd__(contract)

        # .is_calculated = True
        self.is_calculated = True

    def modify_month_contracts(self,
                               months: list[Months],
                               enabled: bool = True,
                               rates:Rates | None = None,
                               # options: EmploymentContractSettings | MandateContractSettings | SelfEmploymentSettings | WorkContractSettings | None = None,
                               salary_base: Decimal | None = None,
                               salary_type: SalaryType= SalaryType.GROSS
                               ) -> None:
        for month in months:
            self._monthly_contract_parameters[month]={"rates": rates or self.rates, "contract_settings":  self.contract_settings, "salary_base": salary_base or self.default_salary_base, "salary_type": salary_type or self.default_salary_type, "enabled":enabled}

    def _set_empty_months_options_to_default(self) -> None:
            self.modify_month_contracts(list(Months), True, self.rates, self.default_salary_base, self.default_salary_type)




    def all_to_dict_salary(self) ->  dict[str, Salary]:
        output = {k.value: v for k, v in self._monthly_contract_calculated_data.items()}
        output['SUMMARY'] = self

        return output

    # @override
    # def to_dict(self,row_name: str | None = None)-> dict[str,dict[str,str | Decimal | bool]]:
    #
    #     output = {}
    #     # if self.all_to_dict_salary().get("SOLO_SUMMARY"):
    #     # #     print("SOLO")
    #     #     output = super().to_dict(row_name)
    #     # else:
    #     for k,v in self.all_to_dict_salary().items():
    #         print(k,v)
    #         output = {k:vv for k, v in self.all_to_dict_salary().items() for vv in v.to_dict().values() }
    #         # output = super().to_dict(row_name)
    #     # output['SUMMARY'] = self.to_dict()
    #     return output


    def all_to_dict(self)-> dict[str,dict[str,str | Decimal | bool]]:
        output = {k:vv for k, v in self.all_to_dict_salary().items() for vv in v.to_dict().values() }
        return output

    def all_to_string(self) -> str:
        return SalaryExporter.to_string(self.all_to_dict())
        # return str(self.get_data_frame(columns=[
        #          "salary_gross", "social_insurance_sum", "cost", "health_insurance", "tax_advance_payment",
        #          "net_salary", "employer_pension_contribution", "employer_disability_contribution",
        #          "accident_insurance", "fp", "fgsp", "total_employer_cost"]))

    # def get_all_data_frame(self,rows: list[str] | None = None,columns: list[str] | None = None) -> pd.DataFrame:
    #     return SalaryExporter.get_data_frame(self.to_dict(), rows, columns)

    def get_all_data_frame(self,rows: list[str] | None = None,columns: list[str] | None = None) -> pd.DataFrame:
        return SalaryExporter.get_data_frame(self.all_to_dict(), rows, columns)

    def all_to_excel(self, path: Path):
        return SalaryExporter.to_excel(self.all_to_dict(), path)

    def all_to_json(self, path: Path):
        return SalaryExporter.to_json(self.all_to_dict(), path)

    def all_to_csv(self, path: Path):
        return SalaryExporter.to_csv(self.all_to_dict(), path)

    # def get_data_frame(self,rows: list[str] | None = None,columns: list[str] | None = None) -> pd.DataFrame:
    #     output = self.to_dict()
    #
    #     if rows is not None:
    #         output = {k:v for k,v in output.items() if k in rows}
    #
    #     return Salary._generate_data_frame(output, columns)

    def __getitem__(self, item: str) ->  Salary:
        return self.all_to_dict_salary()[item]

    # def print_all(self) ->str:
    #     return str(self.get_data_frame( columns = [
    #         "salary_gross", "social_insurance_sum", "cost", "health_insurance", "tax_advance_payment",
    #         "net_salary", "employer_pension_contribution", "employer_disability_contribution",
    #         "accident_insurance", "fp", "fgsp", "total_employer_cost"]))



    # @staticmethod
    # def _generate_data_frame(contract_simulator_data: dict[str, 'Salary'], columns: list | None = None
    #                         ) -> pd.DataFrame:
    #
    #     first_key = list(contract_simulator_data.keys())[0]
    #
    #     # if not isinstance(contract_simulator_data.get(first_key),Salary):
    #     #     if columns is None:
    #     #         columns = contract_simulator_data.keys()
    #     #     data=contract_simulator_data
    #     #     index = [contract_simulator_data.get('name')]
    #     # else:
    #     #     if columns is None:
    #     #         columns = list(contract_simulator_data.get(first_key).to_dict().keys())
    #     #     data = [salary.to_dict() for salary in contract_simulator_data.values()]
    #     #     index = list(contract_simulator_data.keys())
    #
    #     if columns is None:
    #         columns = list(contract_simulator_data.get(first_key).to_dict().keys())
    #     data = [salary.to_dict() for salary in contract_simulator_data.values()]
    #     index = list(contract_simulator_data.keys())
    #
    #     df = pd.DataFrame(data,
    #                     index=index,
    #                     columns=columns
    #                     )
    #     return df