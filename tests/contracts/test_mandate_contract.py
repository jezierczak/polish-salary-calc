import pytest
from decimal import Decimal

from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.opions.mandate_contract_options import MandateContractOptions, MandateContractType
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.abstract_salary import SalaryType

@pytest.mark.parametrize(
"salary_base,pension,disability,sickness,health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
[(Decimal('6000.00'),Decimal('585.60'),Decimal('90.0'),Decimal('0.0'),Decimal('479.20'),Decimal('1065'),
  Decimal('212'),Decimal('4633.20'),Decimal('585.60'),Decimal('390.0'),Decimal('100.20'),Decimal('0.0'),
  Decimal('0.0'),Decimal('7075.80')),
(Decimal('3000.00'),Decimal('292.80'),Decimal('45.0'),Decimal('0.0'),Decimal('239.60'),Decimal('532'),
  Decimal('0'),Decimal('2422.60'),Decimal('292.80'),Decimal('195.00'),Decimal('50.10'),Decimal('0.0'),
  Decimal('0.0'),Decimal('3537.90'))
])
def test_mandate_contract_common_with_and_without_fp_fgsp_ppk(
        salary_base:Decimal, pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        emp_pension:Decimal,emp_disability:Decimal,
        accident:Decimal,fp:Decimal,fgsp:Decimal,total_gross:Decimal
        )->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.COMMON).
                       is_fifty(False).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    mc.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert mc.is_calculated == True
    assert mc.salary_base == salary_base
    assert mc.pension_insurance == pension
    assert mc.disability_insurance == disability
    assert mc.sickness_insurance == sickness
    assert mc.social_insurance_sum == pension + disability + sickness
    assert mc.health_insurance==health_insurance
    assert mc.cost == cost
    assert mc.tax_advance_payment == tax_advance
    assert mc.net_salary==net
    assert mc.employer_pension_contribution==emp_pension
    assert mc.employer_disability_contribution==emp_disability
    assert mc.accident_insurance == accident
    assert mc.fp == fp
    assert mc.fgsp == fgsp
    assert mc.total_employer_cost ==total_gross

    mandate_options2 = (MandateContractOptions().builder().
                        set_mandate_contract_type(MandateContractType.COMMON).
                        is_fp(True).
                        is_fgsp(True).
                        build())
    mc.update_options(mandate_options2)
    mc.calculate(salary_base)
    assert mc.is_calculated == True
    assert mc.fp == salary_base * rates.fp_rate if salary_base>rates.minimum_wage else mc.fp == Decimal('0')
    assert mc.fgsp == salary_base * rates.fgsp_rate
    assert mc.total_employer_cost ==total_gross+mc.fp + mc.fgsp

    mandate_options3 = (MandateContractOptions().builder().
                        set_mandate_contract_type(MandateContractType.COMMON).
                        is_fp(False).
                        is_fgsp(False).
                        set_employee_ppk(Decimal('0.02')).
                        set_employer_ppk(Decimal('0.015')).
                        build())
    mc.update_options(mandate_options3)
    mc.calculate(Decimal('6000'))

    assert mc.is_calculated == True
    assert mc.fp == Decimal('0.0')
    assert mc.fgsp == Decimal('0.0')
    assert mc.employee_ppk_contribution == Decimal('6000') * mc.options.employee_ppk
    assert mc.employer_ppk_contribution == Decimal('6000') * mc.options.employer_ppk
    assert mc.net_salary == Decimal('4503.20')
    assert mc.total_employer_cost == Decimal('7165.80')

@pytest.mark.parametrize(
"salary_base,pension,disability,sickness,health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
[(Decimal('6000.00'),Decimal('585.60'),Decimal('90.0'),Decimal('147.0'),Decimal('465.97'),Decimal('1035'),
  Decimal('198'),Decimal('4513.43'),Decimal('585.60'),Decimal('390.0'),Decimal('100.20'),Decimal('147.0'),
  Decimal('6.0'),Decimal('7228.80')),
(Decimal('2000.00'),Decimal('195.20'),Decimal('30.0'),Decimal('49.0'),Decimal('155.32'),Decimal('345'),
  Decimal('0'),Decimal('1570.48'),Decimal('195.20'),Decimal('130.00'),Decimal('33.40'),Decimal('0.0'),
  Decimal('2.0'),Decimal('2360.60'))
])
def test_mandate_contract_the_same_company_with_20_and_50_costs(
        salary_base:Decimal, pension:Decimal,disability,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        emp_pension:Decimal,emp_disability:Decimal,
        accident:Decimal,fp:Decimal,fgsp:Decimal,total_gross:Decimal
        )->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.THE_SAME_COMPANY).
                       is_fifty(False).
                       is_fp(True).
                       is_fgsp(True).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    mc.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert mc.is_calculated == True
    assert mc.salary_base == salary_base
    assert mc.pension_insurance == pension
    assert mc.disability_insurance == disability
    assert mc.sickness_insurance == sickness
    assert mc.social_insurance_sum == pension + disability + sickness
    assert mc.health_insurance==health_insurance
    assert mc.cost == cost
    assert mc.tax_advance_payment == tax_advance
    assert mc.net_salary==net
    assert mc.employer_pension_contribution==emp_pension
    assert mc.employer_disability_contribution==emp_disability
    assert mc.accident_insurance == accident
    assert mc.fp == fp
    assert mc.fgsp == fgsp
    assert mc.total_employer_cost ==total_gross

    mc2 = MandateContract(rates, mandate_options)
    mc2.calculate(mc.net_salary, SalaryType.NET)
    assert mc2.net_salary == mc.net_salary
    assert mc2.salary_gross == mc.salary_gross

    mandate_options2 = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.THE_SAME_COMPANY).
                       is_fifty(True).
                       is_fp(True).
                       is_fgsp(True).
                       build())
    mc.update_options(mandate_options2)
    rates['description'] ="new description"
    mc.update_rates(rates)
    mc.calculate(Decimal('6000'))

    assert mc.net_salary == Decimal('4700.43')
    assert mc.cost == Decimal('2589.00')
    assert mc.get_rates().description == rates['description'] == "new description"


@pytest.mark.parametrize(
"salary_base,pension,disability,sickness,health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
[(Decimal('8000.00'),Decimal('0'),Decimal('0'),Decimal('0'),Decimal('720'),Decimal('1600'),
  Decimal('468'),Decimal('6812'),Decimal('0'),Decimal('0'),Decimal('0'),Decimal('0'),
  Decimal('0'),Decimal('8000'))

])
def test_mandate_contract_the_same_company_with_20_costs(
        salary_base:Decimal, pension:Decimal,disability,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        emp_pension:Decimal,emp_disability:Decimal,
        accident:Decimal,fp:Decimal,fgsp:Decimal,total_gross:Decimal
        )->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.OTHER_COMPANY_MIN_SALARY).
                       is_fifty(False).
                       is_fp(False).
                       is_fgsp(False).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    mc.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert mc.is_calculated == True
    assert mc.salary_base == salary_base
    assert mc.pension_insurance == pension
    assert mc.disability_insurance == disability
    assert mc.sickness_insurance == sickness
    assert mc.social_insurance_sum == pension + disability + sickness
    assert mc.health_insurance==health_insurance
    assert mc.cost == cost
    assert mc.tax_advance_payment == tax_advance
    assert mc.net_salary==net
    assert mc.employer_pension_contribution==emp_pension
    assert mc.employer_disability_contribution==emp_disability
    assert mc.accident_insurance == accident
    assert mc.fp == fp
    assert mc.fgsp == fgsp
    assert mc.total_employer_cost ==total_gross


def test_mandate_contract_under_26()->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.UNDER_26_AND_STUDENT).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    mc.calculate(Decimal('4000'), SalaryType.GROSS)
    assert mc.is_calculated == True
    assert mc.salary_base == Decimal('4000')
    assert mc.pension_insurance == Decimal('0')

    assert mc.tax_advance_payment == Decimal('0')
    assert mc.net_salary==Decimal('4000')
    assert mc.total_employer_cost ==Decimal('4000')


def test_mandate_contract_common_under_200_with_a_lump_sum()->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(MandateContractType.COMMON).
                        is_a_lump_sum(True).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    # salary.update_options(employment_options)
    mc.calculate(Decimal('200'), SalaryType.GROSS)
    assert mc.is_calculated == True
    assert mc.salary_base == Decimal('200')
    assert mc.pension_insurance == Decimal('19.52')
    assert mc.disability_insurance == Decimal('3')
    assert mc.tax_advance_payment == Decimal('24')
    assert mc.net_salary==Decimal('137.51')
    assert mc.total_employer_cost ==Decimal('235.86')


def test_mandate_contract_unknown_contract_type()->None:
    mandate_options = (MandateContractOptions().builder().
                       set_mandate_contract_type(5).
                       build())
    rates = Rates()
    mc = MandateContract(rates, mandate_options)
    with pytest.raises(NotImplementedError):
      mc.calculate(Decimal("4000"))