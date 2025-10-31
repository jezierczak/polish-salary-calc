from calendar import Month

from polish_salary_calc.console_printer.salary_console_printer import SalaryConsolePrinter
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.options.self_employment_options import SelfEmploymentOptions, SelfEmploymentType, TaxType, \
    HealthBase
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contracts.base_contract import SalaryType

from polish_salary_calc.options.employment_contract_options import EmploymentContractOptions

from polish_salary_calc.contracts.employment_contract import EmploymentContract

from decimal import Decimal

from polish_salary_calc.service.year_contract_simulator import YearContractService, Months


def main() -> None:
    rates = Rates()

    employment_options = (EmploymentContractOptions().builder().
                             is_increased_costs(True).
                             is_active_business(False).
                             is_under_26(False).
                                set_employee_ppk(Decimal("0.02")).
                                set_employer_ppk(Decimal("0.015")).
                                is_fp_fgsp(True).
                             build())
    # salary = EmploymentContract(rates,employment_options)
    # salary.calculate(Decimal('10000'), SalaryType.GROSS)

    # print(rates)
    # print(employment_options)
    # print(salary)

    # printer = ConsolePrinter(salary)
    # print(printer.print_rates())
    # print(printer.print_options())
    # print(printer.print_contract())

    # print(salary.get_rates())
    # print(salary.get_options())
    # for k,i in salary.to_dict().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary.net_ratio}')
    # print(f'Total markups: {salary.total_markups}')
    # print(f'Total markups ratio: {salary.total_markups_ratio}')

    # print('--------------------Zlecenie----------------------------')
    #
    # mandate_options = (MandateContractOptions().builder().
    #                    set_mandate_contract_type(MandateContractType.THE_SAME_COMPANY).
    #                    is_fifty(True).
    #                    is_fp(True).
    #                    is_fgsp(True).
    #                    build())
    #
    # salary2 = MandateContract(rates, mandate_options)
    # # salary.update_options(employment_options)
    # salary2.calculate(Decimal('2000'), SalaryType.GROSS)
    #
    # print(salary2.get_rates())
    # print(salary2.get_options())
    # for k, i in salary2.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary2.net_ratio}')
    # print(f'Total markups: {salary2.total_markups}')
    # print(f'Total markups ratio: {salary2.total_markups_ratio}')
    #
    # print('--------------------O dzieło----------------------------')
    #
    # work_options = (WorkContractOptions().builder().
    #                 is_a_lump_sum(True).
    #                 set_work_contract_type(WorkContractType.THE_SAME_COMPANY).
    #                 build())
    # salary3 = WorkContract(rates, work_options)
    # salary3.calculate(Decimal('200'), SalaryType.GROSS)
    #
    # print(salary3.get_rates())
    # print(salary3.get_options())
    # for k, i in salary3.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary3.net_ratio}')
    # print(f'Total markups: {salary3.total_markups}')
    # print(f'Total markups ratio: {salary34.total_markups_ratio}')
    # #
    print('--------------------Działalność----------------------------')
    #
    # self_employment_options = (SelfEmploymentOptions().
    #                             builder().
    #                             set_self_employment_type(SelfEmploymentType.COMMON).
    #                             set_sick_pay(True).
    #                             #set_tax_type(TaxType.A_LUMP_SUM).
    #                             #set_tax_lump_rate(Decimal('0.055')).
    #                             set_health_base(HealthBase.NONE).
    #                             set_costs(Decimal('1000.0')).
    #                             set_tax_base_sum(Decimal('1000.0')).
    #                             #set_name("Umowa nr 193").
    #                             build())
    # salary4 = SelfEmployment(rates, self_employment_options)
    # salary4.calculate(Decimal('10000'), SalaryType.GROSS)
    # print(salary4.to_dict())
    # print(salary4)
    #
    # # print(salary4.get_rates())
    # # print(salary4.get_options())
    # for k, i in salary4.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # print(f'Net ratio: {salary4.net_ratio}')
    # print(f'Total markups: {salary4.total_markups}')
    # print(f'Total markups ratio: {salary4.total_markups_ratio}')

    # contract_service = ContractServic(rates)
    # contract_service.add_contract(All,salary4)
    # contract_service.show()
    # contract_service.export(EXCCEL,"mojasymulacja.xcl", clean=True)

    yc = YearContractService(rates,employment_options,Decimal("8000"))
    yc.calculate()
    print(yc.monthly_contract_calculated_data[Months.JAN])
    print("------------------------")
    print(yc.summary)
if __name__ == '__main__':
    main()