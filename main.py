from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.abstract_salary import SalaryType

from polish_salary_calc.opions.employment_contract_options import EmploymentContractOptions
from polish_salary_calc.opions.mandate_contract_options import MandateContractOptions, MandateContractType
from polish_salary_calc.opions.work_contract_options import WorkContractOptions, WorkContractType
from polish_salary_calc.opions.self_employment_options import SelfEmploymentOptions, SelfEmploymentType

from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.contracts.self_employment import SelfEmployment

from decimal import Decimal


def main() -> None:
    # employment_options = (EmploymentContractOptions().builder().
    #                          is_increased_costs(True).
    #                          set_cost_fifty_ratio(Decimal('0.5')).
    #                          is_active_business(False).
    #                          is_fp_fgsp(False).
    #                          set_employee_ppk(Decimal('0.02')).
    #                          set_employer_ppk(Decimal('0.0')).
    #                          is_under_26(False).
    #                          set_accident_insurance_rate(Decimal('0.2')).
    #                          build())
    # employment_options = EmploymentContractOptions().from_dict({
    #     'sick_pay': Decimal('1000.00'),
    #     'current_month_gross_sum': Decimal('20000.00'),
    #     'social_security_base_sum': Decimal('20000.00'),
    #     'cost_fifty_sum': Decimal('20000.00'),
    #     'tax_base_sum': Decimal('20000.00'),
    #     'salary_deductions': Decimal('2000.00'),
    #     'increased_costs': False,
    #     'cost_fifty_ratio': Decimal('0.0'),
    #     'active_business': False,
    #     'fp_fgsp': False,
    #     'under_26': False,
    #     'accident_insurance_rate': None,
    #     'employer_ppk': Decimal('0.0'),
    #     'employee_ppk': Decimal('0.0')
    # })
    # rates = Rates()
    # salary = EmploymentContract(rates,employment_options)
    # #salary.update_options(employment_options)
    # salary.calculate(Decimal('6000'), SalaryType.GROSS)
    #
    # print(salary.get_rates())
    # print(salary.get_options())
    # for k,i in salary.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # #print(salary.net_ratio)
    # print(salary.total_markups)
    # print(salary.total_markups_ratio)

    print('--------------------Zlecenie----------------------------')

    # mandate_options = (MandateContractOptions().builder().
    #                    set_mandate_contract_type(MandateContractType.THE_SAME_COMPANY).
    #                    is_fifty(True).
    #                     is_fp(True).
    #                     is_fgsp(True).
    #                    build())
    rates = Rates()
    # salary2 = MandateContract(rates, mandate_options)
    # # salary.update_options(employment_options)
    # salary2.calculate(Decimal('2000'), SalaryType.GROSS)
    #
    # print(salary2.get_rates())
    # print(salary2.get_options())
    # for k, i in salary2.get_all_output().items():
    #     print(f'{k:20.20}: {i}')
    # # print(salary.net_ratio)
    # print(salary2.total_markups)
    # print(salary2.total_markups_ratio)
    # #
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
    # # print(salary.net_ratio)
    # print(salary3.total_markups)
    # print(salary3.total_markups_ratio)
    # #
    # print('--------------------Działalność----------------------------')

    self_employment_options = (SelfEmploymentOptions().builder().set_self_employment_type(SelfEmploymentType.COMMON).set_sick_pay(True).
                    build())
    salary4 = SelfEmployment(rates, self_employment_options)
    salary4.calculate(Decimal('6000'), SalaryType.GROSS)

    print(salary4.get_rates())
    print(salary4.get_options())
    for k, i in salary4.get_all_output().items():
        print(f'{k:20.20}: {i}')
    # print(salary.net_ratio)
    print(salary4.total_markups)
    print(salary4.total_markups_ratio)

if __name__ == '__main__':
    main()