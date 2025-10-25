import pytest
from decimal import Decimal

from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.opions.work_contract_options import WorkContractOptions, WorkContractType
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.abstract_salary import SalaryType


@pytest.mark.parametrize(
"salary_base,pension,disability,sickness,health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
[(Decimal('5000.00'),Decimal('0'),Decimal('0'),Decimal('0.0'),Decimal('0'),Decimal('1000'),
  Decimal('480'),Decimal('4520'),Decimal('0'),Decimal('0'),Decimal('0'),Decimal('0.0'),
  Decimal('0.0'),Decimal('5000')),
(Decimal('3000.00'),Decimal('0'),Decimal('0'),Decimal('0.0'),Decimal('0'),Decimal('600'),
  Decimal('288'),Decimal('2712'),Decimal('0'),Decimal('0'),Decimal('0'),Decimal('0.0'),
  Decimal('0.0'),Decimal('3000'))
 ])
def test_work_contract_common(
        salary_base:Decimal, pension:Decimal,disability,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        emp_pension:Decimal,emp_disability:Decimal,
        accident:Decimal,fp:Decimal,fgsp:Decimal,total_gross:Decimal
        )->None:
    work_contract_options = (WorkContractOptions().builder().
                       set_work_contract_type(WorkContractType.COMMON).
                       build())
    rates = Rates()
    wc = WorkContract(rates, work_contract_options)
    # salary.update_options(employment_options)
    wc.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert wc.is_calculated == True
    assert wc.salary_base == salary_base
    assert wc.pension_insurance == pension
    assert wc.disability_insurance == disability
    assert wc.sickness_insurance == sickness
    assert wc.social_insurance_sum == pension + disability + sickness
    assert wc.health_insurance==health_insurance
    assert wc.cost == cost
    assert wc.tax_advance_payment == tax_advance
    assert wc.net_salary==net
    assert wc.employer_pension_contribution==emp_pension
    assert wc.employer_disability_contribution==emp_disability
    assert wc.accident_insurance == accident
    assert wc.fp == fp
    assert wc.fgsp == fgsp
    assert wc.total_employer_cost ==total_gross

@pytest.mark.parametrize(
"salary_base,pension,disability,sickness,health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
[(Decimal('5000.00'),Decimal('488'),Decimal('75'),Decimal('122.50'),Decimal('388.3'),Decimal('2157'),
  Decimal('259'),Decimal('3667.20'),Decimal('488'),Decimal('325'),Decimal('83.5'),Decimal('122.50'),
  Decimal('5.0'),Decimal('6024')),
(Decimal('2000.00'),Decimal('195.2'),Decimal('30'),Decimal('49.0'),Decimal('155.32'),Decimal('863'),
  Decimal('104'),Decimal('1466.48'),Decimal('195.2'),Decimal('130'),Decimal('33.4'),Decimal('0.0'),
  Decimal('2.0'),Decimal('2360.6'))
 ])
def test_work_contract_the_same_company_with_50_costs(
        salary_base:Decimal, pension:Decimal,disability,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        emp_pension:Decimal,emp_disability:Decimal,
        accident:Decimal,fp:Decimal,fgsp:Decimal,total_gross:Decimal
        )->None:
    work_contract_options = (WorkContractOptions().builder().
                       set_work_contract_type(WorkContractType.THE_SAME_COMPANY).is_fifty(True).
                       build())
    rates = Rates()
    wc = WorkContract(rates, work_contract_options)
    # salary.update_options(employment_options)
    wc.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert wc.is_calculated == True
    assert wc.salary_base == salary_base
    assert wc.pension_insurance == pension
    assert wc.disability_insurance == disability
    assert wc.sickness_insurance == sickness
    assert wc.social_insurance_sum == pension + disability + sickness
    assert wc.health_insurance==health_insurance
    assert wc.cost == cost
    assert wc.tax_advance_payment == tax_advance
    assert wc.net_salary==net
    assert wc.employer_pension_contribution==emp_pension
    assert wc.employer_disability_contribution==emp_disability
    assert wc.accident_insurance == accident
    assert wc.fp == fp
    assert wc.fgsp == fgsp
    assert wc.total_employer_cost ==total_gross

    work_contract_options2 = (WorkContractOptions().builder().
                             set_work_contract_type(WorkContractType.THE_SAME_COMPANY).is_fifty(False).
                             build())

    wc2 = WorkContract(rates, work_contract_options2)
    wc2.calculate(Decimal('5000.00'))

    assert wc2.is_calculated == True
    assert wc2.salary_gross == Decimal('5000')
    assert wc2.health_insurance_base == Decimal('4314.50')
    assert wc2.cost == Decimal('863')
    assert wc2.net_salary == Decimal('3511.20')
    assert wc2.total_employer_cost == Decimal('6024')

    work_contract_options3 = (WorkContractOptions().builder().
                             set_work_contract_type(WorkContractType.THE_SAME_COMPANY).is_fifty(False).
                             set_employee_ppk(Decimal('0.02')).set_employer_ppk(Decimal('0.015')).
                             build())
    wc2.update_options(work_contract_options3)
    wc2.calculate(Decimal('5000.00'))

    assert wc2.is_calculated == True
    assert wc2.salary_gross == Decimal('5000')
    assert wc2.employee_ppk_contribution == Decimal('100')
    assert wc2.net_salary == Decimal('3402.20')
    assert wc2.employer_ppk_contribution == Decimal('75')
    assert wc2.total_employer_cost == Decimal('6099')


def test_work_contract_common_under_200_with_a_lump_sum() -> None:
    work_options = (WorkContractOptions().builder().
                           set_work_contract_type(WorkContractType.COMMON).
                           is_a_lump_sum(True).
                           build())
    r = Rates()
    wcc = WorkContract(r, work_options)
        # salary.update_options(employment_options)
    wcc.calculate(Decimal('200'), SalaryType.GROSS)
    assert wcc.is_calculated == True
    assert wcc.salary_base == Decimal('200')
    assert wcc.pension_insurance == Decimal('0')
    assert wcc.disability_insurance == Decimal('0')
    assert wcc.tax_advance_payment == Decimal('24')
    assert wcc.net_salary == Decimal('176')
    assert wcc.total_employer_cost == Decimal('200')