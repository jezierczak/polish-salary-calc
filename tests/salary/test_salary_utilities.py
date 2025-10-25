from decimal import Decimal

from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.salary_utilities import SalaryUtilities
import pytest

@pytest.mark.parametrize("tax_base,tax_base_sum,out",[
    (Decimal('0.0'), Decimal('0.0'), Decimal('0.0')),
    (Decimal('10000.0'), Decimal('0.0'), Decimal('900.0')), #10000*0.12 -300 = 900
    (Decimal('20000.0'), Decimal('25000.0'), Decimal('2100.0')), #10000*0.12 -300 = 900
    (Decimal('130000.0'), Decimal('0.0'), Decimal('17300.0')), #12000*0.12 - 300 = 14100+3200 = 17300
    (Decimal('20000.0'), Decimal('110000.0'), Decimal('4100.0')), #10000*0.12 - 300 = 900+3200 = 4100
    (Decimal('20000.0'), Decimal('120000.0'), Decimal('6100.0')),  # -300 = 20000*0,32 = 6100
    (Decimal('20000.0'), Decimal('170000.0'), Decimal('6400.0')),  # 20000*0,32 = 6400
])
def test_salary_utilities_calculate_tax(tax_base: Decimal, tax_base_sum: Decimal, out: Decimal) -> None:
    output = SalaryUtilities.calculate_tax(
        income_tax = Rates().income_tax,
        tax_base = tax_base,
        tax_base_sum = tax_base_sum,
        tax_threshold = Rates().tax_threshold,
        month_tax_free = Rates().month_tax_free)

    assert output == out


@pytest.mark.parametrize("cost_ratio,base,cost_fifty_sum,out",[
    (Decimal('0.5'),Decimal('0.0'), Decimal('0.0'),Decimal('0.0')),
    (Decimal('0.5'), Decimal('5250'), Decimal('0.0'),Decimal('2500')),
    (Decimal('0.5'), Decimal('5250'), Decimal('10000.0'),Decimal('2500')),
    (Decimal('0.5'), Decimal('5250'), Decimal('115000.0'), Decimal('2500')),
    (Decimal('0.5'), Decimal('5250'), Decimal('118000.0'), Decimal('2000')),
    (Decimal('0.5'), Decimal('5250'), Decimal('120000.0'), Decimal('0.0')),
    (Decimal('0.5'), Decimal('5250'), Decimal('130000.0'), Decimal('0.0')),
])
def test_salary_utilities_calculate_author_right_cost(cost_ratio: Decimal,base: Decimal, cost_fifty_sum: Decimal, out:Decimal) -> None:
    output = SalaryUtilities.calculate_author_rights_cost(
        income_tax_deduction = Rates.income_tax_deduction[0],
        cost_ratio = cost_ratio,
        base = base,
        cost_fifty_sum = cost_fifty_sum,
        cost_threshold = Rates.cost_threshold
    )
    assert output == out

@pytest.mark.parametrize("social_security_base,social_security_base_sum,out",[
        (Decimal('0.0'), Decimal('0.0'), Decimal('0.0')),
        (Decimal('10000.0'), Decimal('0.0'), Decimal('976.0')),
        (Decimal('10000.0'), Decimal('250190.0'), Decimal('976.0')), # insurance cap = 260190, insurance rate = 9.76%
        (Decimal('10000.0'), Decimal('255190.0'), Decimal('488.0')),  # insurance cap = 260190, insurance rate = 9.76%
        (Decimal('10000.0'), Decimal('260190.0'), Decimal('0.0')),  # insurance cap = 260190, insurance rate = 9.76%
        (Decimal('10000.0'), Decimal('270190.0'), Decimal('0.0')),  # insurance cap = 260190, insurance rate = 9.76%
     ])
def test_salary_utilities_calculate_pension_or_disability_insurance(social_security_base: Decimal, social_security_base_sum: Decimal, out: Decimal) -> None:
    output = SalaryUtilities.calculate_pension_or_disability_insurance(
        pension_or_disability_insurance_rate=Rates.pension_insurance_rate,
        social_security_base = social_security_base,
        social_security_base_sum=social_security_base_sum,
        social_insurance_cap=Rates().social_insurance_cap
    )
    assert output == out

        # total_social_security_base_sum = social_security_base_sum + social_security_base
        # if total_social_security_base_sum <= social_insurance_cap:
        #     return social_security_base *pension_or_disability_insurance_rate
        # elif total_social_security_base_sum - social_security_base > social_insurance_cap:
        #     return Decimal('0.0')
        # else:
        #     return (social_security_base - (total_social_security_base_sum - social_insurance_cap))*pension_or_disability_insurance_rate
