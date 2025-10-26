import pytest
from decimal import Decimal

from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.opions.self_employment_options import SelfEmploymentOptions, SelfEmploymentType, TaxType, \
    HealthBase
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.abstract_salary import SalaryType


@pytest.mark.parametrize(
"salary_base,tax_base_sum,social_security_base,"
"pension,disability,sickness,"
"health_insurance,cost,"
"tax_advance,net,"
"accident,fp,total_gross",
[(Decimal('6000.00'),Decimal('1000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('314.96'),Decimal('1000'),
  Decimal('0'),Decimal('2911.08'),
  Decimal('86.90'),Decimal('127.49'),Decimal('6000')),
(Decimal('12000.00'),Decimal('25000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('830.34'),Decimal('1000'),
  Decimal('507'),Decimal('7888.70'),
  Decimal('86.90'),Decimal('127.49'),Decimal('12000')),
(Decimal('12000.00'),Decimal('35000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('830.34'),Decimal('1000'),
  Decimal('1107'),Decimal('7288.70'),
  Decimal('86.90'),Decimal('127.49'),Decimal('12000')),
(Decimal('12000.00'),Decimal('115000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('830.34'),Decimal('1000'),
  Decimal('1952'),Decimal('6443.70'),
  Decimal('86.90'),Decimal('127.49'),Decimal('12000')),
(Decimal('12000.00'),Decimal('125000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('830.34'),Decimal('1000'),
  Decimal('2952'),Decimal('5443.70'),
  Decimal('86.90'),Decimal('127.49'),Decimal('12000')),
])
def test_self_employment_common(
        salary_base:Decimal,tax_base_sum: Decimal,social_security_base:Decimal,
        pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        accident:Decimal,fp:Decimal,total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.COMMON).
                               set_sick_pay(True).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.social_security_base == social_security_base
    assert se.pension_insurance == pension
    assert se.disability_insurance == disability
    assert se.sickness_insurance == sickness
    assert se.social_insurance_sum == pension + disability + sickness +accident+fp
    assert se.health_insurance==health_insurance
    assert se.cost == cost
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.accident_insurance == accident
    assert se.fp == fp
    assert se.fgsp == Decimal('0')
    assert se.total_employer_cost ==total_gross

@pytest.mark.parametrize(
"salary_base,tax_base_sum,social_security_base,"
"pension,disability,sickness,"
"health_insurance,cost,"
"tax_advance,net,"
"accident,fp,total_gross",
[(Decimal('6000.00'),Decimal('1000'),Decimal('1399.80'),
  Decimal('273.24'),Decimal('111.98'),Decimal('34.30'),
  Decimal('410.14'),Decimal('1000'),
  Decimal('0'),Decimal('4146.96'),
  Decimal('23.38'),Decimal('0'),Decimal('6000')),
(Decimal('2000.00'),Decimal('1000'),Decimal('1399.80'),
  Decimal('273.24'),Decimal('111.98'),Decimal('34.30'),
  Decimal('314.96'),Decimal('1000'),
  Decimal('0'),Decimal('242.14'),
  Decimal('23.38'),Decimal('0'),Decimal('2000')),
])
def test_self_employment_preferred(
        salary_base:Decimal,tax_base_sum: Decimal,social_security_base:Decimal,
        pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        accident:Decimal,fp:Decimal,total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.PREFERRED).
                               set_sick_pay(True).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.social_security_base == social_security_base
    assert se.pension_insurance == pension
    assert se.disability_insurance == disability
    assert se.sickness_insurance == sickness
    assert se.social_insurance_sum == pension + disability + sickness +accident+fp
    assert se.health_insurance==health_insurance
    assert se.cost == cost
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.accident_insurance == accident
    assert se.fp == fp
    assert se.fgsp == Decimal('0')
    assert se.total_employer_cost ==total_gross

    #No sick pay
    se.update_options((SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.PREFERRED).
                               set_sick_pay(False).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build()))

    assert se.is_calculated == False

    se.calculate(salary_base)

    assert se.sickness_insurance == Decimal('0.0')
    assert se.social_insurance_sum == pension + disability +accident+fp
    assert se.net_salary > net

@pytest.mark.parametrize(
"salary_base,tax_base_sum,social_security_base,"
"pension,disability,sickness,"
"health_insurance,cost,"
"tax_advance,net,"
"accident,fp,total_gross",
[(Decimal('5000.00'),Decimal('1000'),Decimal('0'),
  Decimal('0'),Decimal('0'),Decimal('0'),
  Decimal('360'),Decimal('1000'),
  Decimal('0'),Decimal('3640'),
  Decimal('0'),Decimal('0'),Decimal('5000')),
])
def test_self_employment_startup_relief(
        salary_base:Decimal,tax_base_sum: Decimal,social_security_base:Decimal,
        pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        accident:Decimal,fp:Decimal,total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.STARTUP_RELIEF).
                               set_sick_pay(True).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.social_security_base == social_security_base
    assert se.pension_insurance == pension
    assert se.disability_insurance == disability
    assert se.sickness_insurance == sickness
    assert se.social_insurance_sum == pension + disability + sickness +accident+fp
    assert se.health_insurance==health_insurance
    assert se.cost == cost
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.accident_insurance == accident
    assert se.fp == fp
    assert se.fgsp == Decimal('0')
    assert se.total_employer_cost ==total_gross

@pytest.mark.parametrize(
"salary_base,tax_base_sum,social_security_base,"
"pension,disability,sickness,"
"health_insurance,cost,"
"tax_advance,net,"
"accident,fp,total_gross",
[(Decimal('3000.00'),Decimal('1000'),Decimal('0'),
  Decimal('0'),Decimal('0'),Decimal('0'),
  Decimal('0'),Decimal('1000'),
  Decimal('0'),Decimal('2000'),
  Decimal('0'),Decimal('0'),Decimal('3000')),
])
def test_self_employment_unregistered_business(
        salary_base:Decimal,tax_base_sum: Decimal,social_security_base:Decimal,
        pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        accident:Decimal,fp:Decimal,total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.UNREGISTERED_BUSINESS).
                               set_sick_pay(True).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.social_security_base == social_security_base
    assert se.pension_insurance == pension
    assert se.disability_insurance == disability
    assert se.sickness_insurance == sickness
    assert se.social_insurance_sum == pension + disability + sickness +accident+fp
    assert se.health_insurance==health_insurance
    assert se.cost == cost
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.accident_insurance == accident
    assert se.fp == fp
    assert se.fgsp == Decimal('0')
    assert se.total_employer_cost ==total_gross

def test_self_employment_unregistered_business_exceeded_income_cap() -> None:
    rates = Rates()
    se = SelfEmployment(rates, SelfEmploymentOptions().builder().set_self_employment_type(SelfEmploymentType.UNREGISTERED_BUSINESS).build())
    with pytest.raises(ValueError,match="Salary base for unregistered business exceeded unregistered business income cap") as e:
        se.calculate(Decimal('5000.0'))


@pytest.mark.parametrize(
"salary_base,tax_base_sum,social_security_base,"
"pension,disability,sickness,"
"health_insurance,cost,"
"tax_advance,net,"
"accident,fp,total_gross",
[(Decimal('6000.00'),Decimal('1000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('314.96'),Decimal('1000'),
  Decimal('613'),Decimal('2298.08'),
  Decimal('86.90'),Decimal('127.49'),Decimal('6000')),
(Decimal('12000.00'),Decimal('1000'),Decimal('5203.80'),
  Decimal('1015.78'),Decimal('416.30'),Decimal('127.49'),
  Decimal('452.08'),Decimal('1000'),
  Decimal('1753'),Decimal('7020.96'),
  Decimal('86.90'),Decimal('127.49'),Decimal('12000')),
])
def test_self_employment_common_with_linear_tax(
        salary_base:Decimal,tax_base_sum: Decimal,social_security_base:Decimal,
        pension:Decimal,disability: Decimal,sickness:Decimal,
        health_insurance:Decimal,cost:Decimal,
        tax_advance:Decimal,net:Decimal,
        accident:Decimal,fp:Decimal,total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.COMMON).
                               set_sick_pay(True).
                               set_tax_type(TaxType.LINE_TAX).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.social_security_base == social_security_base
    assert se.pension_insurance == pension
    assert se.disability_insurance == disability
    assert se.sickness_insurance == sickness
    assert se.social_insurance_sum == pension + disability + sickness +accident+fp
    assert se.health_insurance==health_insurance
    assert se.cost == cost
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.accident_insurance == accident
    assert se.fp == fp
    assert se.fgsp == Decimal('0')
    assert se.total_employer_cost ==total_gross

@pytest.mark.parametrize(
"salary_base,tax_base_sum,tax_lump_rate,"
"health_base,health_insurance,tax_base,"
"tax_advance,net,total_gross",
[(Decimal('12000.00'),
  Decimal('1000'),
  Decimal('0.17'),
  HealthBase.NONE,
  Decimal('769.43'),
  Decimal('12000'),
  Decimal('2040'),
  Decimal('6416.61'),
  Decimal('12000')),
(Decimal('2000.00'),
  Decimal('1000'),
  Decimal('0.10'),
  HealthBase.NONE,
  Decimal('461.63'),
  Decimal('2000'),
  Decimal('200'),
  Decimal('-1435.59'),
  Decimal('2000')),
(Decimal('30000.00'),
  Decimal('15000'),
  Decimal('0.055'),
  HealthBase.NONE,
  Decimal('1384.97'),
  Decimal('30000'),
  Decimal('1650'),
  Decimal('24191.07'),
  Decimal('30000')),
(Decimal('12000.00'),
  Decimal('1000'),
  Decimal('0.12'),
  HealthBase.LOW,
  Decimal('461.63'),
  Decimal('12000'),
  Decimal('1440'),
  Decimal('7324.41'),
  Decimal('12000')),
(Decimal('12000.00'),
  Decimal('1000'),
  Decimal('0.12'),
  HealthBase.MEDIUM,
  Decimal('769.43'),
  Decimal('12000'),
  Decimal('1440'),
  Decimal('7016.61'),
  Decimal('12000')),
(Decimal('12000.00'),
  Decimal('1000'),
  Decimal('0.12'),
  HealthBase.HIGH,
  Decimal('1384.97'),
  Decimal('12000'),
  Decimal('1440'),
  Decimal('6401.07'),
  Decimal('12000')),
])
def test_self_employment_common_with_a_lump(
        salary_base:Decimal,
        tax_base_sum:Decimal,
        tax_lump_rate:Decimal,
        health_base:HealthBase,
        health_insurance:Decimal,
        tax_base:Decimal,
        tax_advance:Decimal,
        net:Decimal,
        total_gross:Decimal
        )->None:
    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.COMMON).
                               set_sick_pay(True).
                               set_tax_type(TaxType.A_LUMP_SUM).
                               set_tax_lump_rate(tax_lump_rate).
                               set_health_base(health_base).
                               set_costs(Decimal('1000.0')).
                               set_tax_base_sum(tax_base_sum).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    se.calculate(Decimal(salary_base), SalaryType.GROSS)
    assert se.is_calculated == True
    assert se.salary_base == salary_base
    assert se.health_insurance==health_insurance
    assert se.tax_base==tax_base
    assert se.tax_advance_payment == tax_advance
    assert se.net_salary==net
    assert se.total_employer_cost ==total_gross


def test_self_employment_common_with_a_lump_raises_error_wrong_rate()->None:

    self_employment_options = (SelfEmploymentOptions().
                               builder().
                               set_self_employment_type(SelfEmploymentType.COMMON).
                               set_tax_type(TaxType.A_LUMP_SUM).
                               set_tax_lump_rate(Decimal('10')).
                               build())
    rates = Rates()
    se = SelfEmployment(rates, self_employment_options)
    with pytest.raises(ValueError, match="Lump rate not allowed"):
        se.calculate(Decimal("1000.00"), SalaryType.GROSS)