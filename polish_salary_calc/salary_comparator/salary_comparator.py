from typing import override, Literal

from polish_salary_calc.salary.salaryexporter import SalaryExporter, SalaryExporterDict
from polish_salary_calc.salary.salary import Salary

COMPARATOR_ITEMS: Literal[
    'BASE',
    'COMPARED',
    'DIFFERENCE',]

class SalaryComparator(SalaryExporter):
    def __init__(self, salary_base_contract: Salary) -> None:
        self.salary_base_contract = salary_base_contract
        self.salary_compare_contract : Salary | None = None
        self.salary_difference: Salary | None = None
        self.is_compared: bool = False

    def compare_to(self,salary_compare_contract: Salary) -> None:
        self.salary_compare_contract = salary_compare_contract
        self.salary_difference = self.salary_base_contract - self.salary_compare_contract
        self.is_compared = True

    def __getitem__(self, item: COMPARATOR_ITEMS) -> Salary:
        if not self.is_compared:
            raise RuntimeError("Salary comparison not computed, use compare_to() method")
        output_name_dict = {
            'BASE': 'salary_base_contract',
            'COMPARED': 'salary_compare_contract',
            'DIFFERENCE': 'salary_difference'
        }
        return getattr(self, output_name_dict[item])

    def to_dict_salary(self) ->  dict[str, Salary]:
        output = {'BASE': self.salary_base_contract,
                  'COMPARED': self.salary_compare_contract,
                  'DIFFERENCE': self.salary_difference}
        return output

    @override
    def to_exporter_dict(self) -> SalaryExporterDict:
        output = {k: vv for k, v in self.to_dict_salary().items() for vv in v.to_exporter_dict().values()}
        return output




