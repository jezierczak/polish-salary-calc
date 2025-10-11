from decimal import Decimal

from opions.mandate_contract_options import MandateContractOptions, MandateContractType
from rates.rates import Rates
from opions.employment_contract_options import EmploymentContractOptions
from salary.abstract_salary import SalaryType
from contracts.employment_contract import EmploymentContract
from contracts.mandate_contract import MandateContract


def main() -> None:
    employment_options = (EmploymentContractOptions().builder().
                             is_increased_costs(True).
                             #set_cost_fifty_ratio(Decimal('0.15')).
                             is_active_business(False).
                             is_fp_fgsp(True).
                             #set_employee_ppk(Decimal('0.02')).
                             #set_employer_ppk(Decimal('0.015')).
                             is_under_26(True).
                             build())
    rates = Rates()
    salary = EmploymentContract(rates,employment_options)
    #salary.update_options(employment_options)
    salary.calculate(Decimal('10000'), SalaryType.NET)

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
    salary2.calculate(Decimal('10000'), SalaryType.NET)

    print(salary2.get_rates())
    print(salary2.get_options())
    for k, i in salary2.get_all_output().items():
        print(f'{k:20.20}: {i}')
    # print(salary.net_ratio)
    print(salary2.total_markups)
    print(salary2.total_markups_ratio)

if __name__ == '__main__':
    main()