from rates.rates import Rates
from salary.abstract_salary import SalaryType

from opions.employment_contract_options import EmploymentContractOptions
from opions.mandate_contract_options import MandateContractOptions, MandateContractType
from opions.work_contract_options import WorkContractOptions
from opions.self_employment_options import SelfEmploymentOptions, SelfEmploymentType

from contracts.employment_contract import EmploymentContract
from contracts.mandate_contract import MandateContract
from contracts.work_contract import WorkContract
from contracts.self_employment import SelfEmployment

from decimal import Decimal


def main() -> None:
    employment_options = (EmploymentContractOptions().builder().
                             is_increased_costs(True).
                             #set_cost_fifty_ratio(Decimal('0.15')).
                             is_active_business(True).
                             is_fp_fgsp(True).
                             #set_employee_ppk(Decimal('0.02')).
                             #set_employer_ppk(Decimal('0.015')).
                             is_under_26(False).
                             build())
    rates = Rates()
    salary = EmploymentContract(rates,employment_options)
    #salary.update_options(employment_options)
    salary.calculate(Decimal('6000'), SalaryType.GROSS)

    print(salary.get_rates())
    print(salary.get_options())
    for k,i in salary.get_all_output().items():
        print(f'{k:20.20}: {i}')
    #print(salary.net_ratio)
    print(salary.total_markups)
    print(salary.total_markups_ratio)

    print('--------------------Zlecenie----------------------------')

    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.THE_SAME_COMPANY).
                       is_fifty(False).
                       build())
    salary2 = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    salary2.calculate(Decimal('6000'), SalaryType.GROSS)

    print(salary2.get_rates())
    print(salary2.get_options())
    for k, i in salary2.get_all_output().items():
        print(f'{k:20.20}: {i}')
    # print(salary.net_ratio)
    print(salary2.total_markups)
    print(salary2.total_markups_ratio)

    print('--------------------O dzieło----------------------------')

    work_options = (WorkContractOptions().builder().is_fifty(False).
                       build())
    salary3 = WorkContract(rates, work_options)
    salary3.calculate(Decimal('6000'), SalaryType.GROSS)

    print(salary3.get_rates())
    print(salary3.get_options())
    for k, i in salary3.get_all_output().items():
        print(f'{k:20.20}: {i}')
    # print(salary.net_ratio)
    print(salary3.total_markups)
    print(salary3.total_markups_ratio)

    print('--------------------Działalność----------------------------')

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