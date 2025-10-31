from dataclasses import dataclass

from polish_salary_calc.console_printer.abstract_salary_console_printer import AbstractSalaryConsolePrinter
from polish_salary_calc.salary.salary_utilities import SalaryUtilities


@dataclass
class SalaryConsolePrinter(AbstractSalaryConsolePrinter):

    def print_rates(self) -> str:
        rates_dict = self.contract.get_rates().to_dict()
        print(f"\nRates ")

        return SalaryUtilities.print_dict(rates_dict)
        # return self._print_pandas_dict(rates_dict).to_string()

    def print_options(self) -> str:
        print(f"\n{self.contract.get_options().options_type()}")
        options_dict = self.contract.get_options().to_dict()
        return SalaryUtilities.print_dict(options_dict)

        # return self._print_pandas_dict(options_dict).to_string()

    def print_contract(self) -> str:
        print(f"\n{self.contract.get_contract_type()}: {self.contract.name} ... created time: {self.contract.created_datetime}")
        contract_dict = self.contract.to_dict()
        del contract_dict['created_datetime']
        del contract_dict['name']
        return SalaryUtilities.print_dict(contract_dict)
        # return self._print_pandas_dict(contract_dict).to_string()

    def print_all(self) -> str:
        return self.print_rates() +"\n"+ self.print_options() +"\n"+ self.print_contract()


    # @staticmethod
    # def _print_pandas_dict(input_dict: dict) -> pd.DataFrame:
    #     pd.set_option('display.max_columns', 5)
    #     return pd.DataFrame.from_dict(input_dict, orient='index')


    # @staticmethod
    # def _print_dict(input_dict: dict, max_items_row: int = 5) -> str:
    #     min_len=8
    #     key_len = []
    #     output_keys = []
    #     output_values = []
    #     i = 0
    #     for key, value in input_dict.items():
    #         if isinstance(input_dict[key], tuple):
    #             for v in value:
    #                 if value is None: value = "None"
    #                 key_len.append(max(len(key),min_len))
    #                 key_len[i] = max(len(str(v)), key_len[i])
    #                 output_keys.append(f"{key:^{key_len[i]}}")
    #                 output_values.append(f"{v:>{key_len[i]}}")
    #
    #                 i += 1
    #         else:
    #             if value is None: value = "None"
    #             key_len.append(max(len(key), min_len))
    #             key_len[i] = max(len(str(value)), key_len[i])
    #             output_keys.append(f"{key:^{key_len[i]}}")
    #             output_values.append(f"{value:>{key_len[i]}}")
    #
    #             i += 1
    #
    #     return (" | ".join(output_keys)) + "\n" + (" | ".join(output_values))


# def main() -> None:
#
#     rates = Rates()
#
#     employment_options = (EmploymentContractOptions().builder().
#                              is_increased_costs(True).
#                              is_active_business(False).
#                              is_under_26(False).
#                              build())
#     salary = EmploymentContract(rates,employment_options)
#     salary.calculate(Decimal('6000'), SalaryType.GROSS)
#
#     # print(salary)
#
#     console_printer = ConsolePrinter(salary)
#     print(console_printer.print_rates())
#     print(console_printer.print_options())
#     print(console_printer.print_contract())
#
#
# if __name__ == '__main__':
#     main()
