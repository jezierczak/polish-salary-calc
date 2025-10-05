from decimal import Decimal
from rates.rates import Rates
from opions.employment_contract_options import EmploymentContractOptions
from salary.abstract_salary import SalaryType
from contracts.employment_contract import EmploymentContract


def main() -> None:
    employment_options = (EmploymentContractOptions().builder().
                             is_increased_costs(True).
                             #set_cost_fifty_ratio(Decimal('0.15')).
                             is_active_business(False).
                             is_fp_fgsp(True).
                             #set_employee_ppk(Decimal('0.02')).
                             #set_employer_ppk(Decimal('0.015')).
                             #is_under_26(False).
                             build())
    rates = Rates()
    salary = EmploymentContract(rates,employment_options)
    #salary.update_options(employment_options)
    salary.calculate(Decimal('5000'), SalaryType.GROSS)

    print(salary.get_rates())
    print(salary.get_options())
    for k,i in salary.get_all_output().items():
        print(f'{k:20.20}: {i}')
    #print(salary.net_ratio)
    print(salary.total_markups)
    print(salary.total_markups_ratio)

if __name__ == '__main__':
    main()