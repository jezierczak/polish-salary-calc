import pytest
from unittest.mock import MagicMock
from decimal import Decimal

from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contract_settings.employment_contract_settings import (
    EmploymentContractSettings,
)
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contracts.base_contract import SalaryType


@pytest.fixture
def employment_contract_mock_6000_gross() -> MagicMock:
    employment_contract = MagicMock(spec=EmploymentContract)
    employment_contract.rates = Rates()
    employment_contract.options = (
        EmploymentContractSettings()
        .builder()
        .is_increased_costs(True)
        .
        # set_cost_fifty_ratio(Decimal('0.15')).
        is_active_business(True)
        .is_fp_fgsp(True)
        .
        # set_employee_ppk(Decimal('0.02')).
        # set_employer_ppk(Decimal('0.015')).
        is_under_26(False)
        .build()
    )

    employment_contract.input_salary = Decimal("6000")

    employment_contract.salary_base = Decimal("6000.00")  # płaca podstawowa
    employment_contract.salary_sick_pay = Decimal("0.00")  # chorobowe
    employment_contract.salary_gross = Decimal("6000.00")  # brutto
    employment_contract.social_security_base = Decimal("6000.0")  # podst ub społ
    employment_contract.social_security_base_total = Decimal("6000.0")
    employment_contract.pension_insurance = Decimal("585.60")  # ub emeryt
    employment_contract.disability_insurance = Decimal("90.00")  # ub rent
    employment_contract.sickness_insurance = Decimal("147.00")  # chorobowe
    employment_contract.social_insurance_sum = Decimal("822.60")  # uma ub społ
    employment_contract.cost = Decimal("300.00")
    employment_contract.cost_fifty_total = Decimal("0.00")
    employment_contract.regular_cost = Decimal("300.00")
    employment_contract.author_rights_cost = Decimal(
        "0.00"
    )  # koszt praw autorskich (50%)
    employment_contract.health_insurance_base = Decimal("5177.00")  # podst zdrowotne
    employment_contract.tax_base = Decimal("4877.40")  # podstawa podatku
    employment_contract.tax_base_total = Decimal("4877.40")
    employment_contract.tax = Decimal("585.29")  # podatek
    employment_contract.health_insurance = Decimal("465.97")
    # self.ub_zdr_odl: Decimal= Decimal('0.0')
    employment_contract.ppk_tax = Decimal("0.00")
    employment_contract.tax_advance_payment = Decimal("585")  # zaliczka podatku
    employment_contract.salary_deductions = Decimal("0.00")  # potrącenia wypłaty
    employment_contract.employee_ppk_contribution = Decimal("0.00")
    employment_contract.net_salary = Decimal("4125.43")
    employment_contract.employer_pension_contribution = Decimal(
        "585.60"
    )  # ub emeryt prac
    employment_contract.employer_disability_contribution = Decimal(
        "390.00"
    )  # ub rent prac
    employment_contract.accident_insurance = Decimal("100.20")  # ub wyp prac
    employment_contract.fp = Decimal("147.00")
    employment_contract.fgsp = Decimal("6.00")
    employment_contract.employer_ppk_contribution = Decimal("0.0")  # ppk pracodawca
    employment_contract.total_employer_cost = Decimal("7228.00")  # brutto brutto

    employment_contract.is_calculated = True
    return employment_contract


def test_employment_contract_6000_gross(employment_contract_mock_6000_gross) -> None:
    rates = Rates()
    options = (
        EmploymentContractSettings()
        .SettingsBuilder()
        .is_increased_costs(True)
        .
        # set_cost_fifty_ratio(Decimal('0.15')).
        is_active_business(True)
        .is_fp_fgsp(False)
        .
        # set_employee_ppk(Decimal('0.02')).
        # set_employer_ppk(Decimal('0.015')).
        is_under_26(False)
        .build()
    )
    ec = EmploymentContract(rates, options)
    ec.calculate(Decimal("6000"), SalaryType.GROSS)
    assert ec.salary_gross == employment_contract_mock_6000_gross.salary_gross
    assert ec.net_salary == employment_contract_mock_6000_gross.net_salary

    options2 = (
        EmploymentContractSettings()
        .SettingsBuilder()
        .is_increased_costs(True)
        .set_cost_fifty_ratio(Decimal("0.5"))
        .is_active_business(False)
        .is_fp_fgsp(False)
        .set_employee_ppk(Decimal("0.02"))
        .set_employer_ppk(Decimal("0.015"))
        .is_under_26(False)
        .set_accident_insurance_rate(Decimal("0.2"))
        .build()
    )

    ec.update_options(options2)
    ec.calculate(Decimal("6000"), SalaryType.GROSS)
    assert ec.is_calculated == True
    assert ec.get_settings() == options2
    assert ec.author_rights_cost == Decimal("2438.70")
    assert ec.employee_ppk_contribution == Decimal("120.00")
    assert ec.employer_ppk_contribution == Decimal("90.00")

    options_3 = EmploymentContractSettings().from_dict(
        {
            "name": "",
            "sick_pay": Decimal("1000.00"),
            "current_month_gross_sum": Decimal("20000.00"),
            "social_security_base_sum": Decimal("20000.00"),
            "cost_fifty_sum": Decimal("20000.00"),
            "tax_base_sum": Decimal("20000.00"),
            "salary_deductions": Decimal("1000.00"),
            "increased_costs": False,
            "cost_fifty_ratio": Decimal("0.0"),
            "active_business": False,
            "fp_fgsp": False,
            "under_26": False,
            "accident_insurance_rate": None,
            "employer_ppk": Decimal("0.0"),
            "employee_ppk": Decimal("0.0"),
        }
    )
    ec.update_options(options_3)
    ec.update_rates(rates)
    ec.calculate(Decimal("6000"), SalaryType.GROSS)

    assert ec.social_security_base_total == Decimal("26000.00")
    assert ec.tax_base_total == options_3.tax_base_sum + ec.tax_base
    assert (
        ec.accident_insurance == rates.accident_insurance_rate * ec.social_security_base
    )
    assert ec.net_salary == Decimal("4209.43")
    assert ec.cost_fifty_total == options_3.cost_fifty_sum
    assert ec.total_markups == Decimal("3866.37")
    assert ec.total_markups_ratio == (
        ec.total_markups / ec.total_employer_cost * 100
    ).quantize(Decimal("0.01"))
    assert ec.gross_ratio == (ec.salary_gross / ec.total_employer_cost * 100).quantize(
        Decimal("0.01")
    )
    assert ec.net_ratio == (ec.net_salary / ec.total_employer_cost * 100).quantize(
        Decimal("0.01")
    )


def test_employment_contract_6000_gross_wrong_ppk() -> None:
    rates = Rates()
    options = (
        EmploymentContractSettings()
        .SettingsBuilder()
        .set_employee_ppk(Decimal("0.1"))
        .set_employer_ppk(Decimal("0.01"))
        .build()
    )
    with pytest.raises(ValueError, match="Employer or employee PPK rate is too small"):
        ec = EmploymentContract(rates, options)
        ec.calculate(Decimal("6000"), SalaryType.GROSS)


@pytest.mark.parametrize(
    "salary_base,pension,disability,sickness,"
    "health_insurance,cost,tax_advance,net,emp_pension,emp_disability,accident,fp,fgsp,total_gross",
    [
        (
            Decimal("6000.00"),
            Decimal("585.60"),
            Decimal("90.0"),
            Decimal("147.0"),
            Decimal("465.97"),
            Decimal("250.0"),
            Decimal("292"),
            Decimal("4419.43"),
            Decimal("585.60"),
            Decimal("390.0"),
            Decimal("100.20"),
            Decimal("147.0"),
            Decimal("6.0"),
            Decimal("7228.80"),
        ),
        (
            Decimal("15000.00"),
            Decimal("1464.00"),
            Decimal("225.0"),
            Decimal("367.50"),
            Decimal("1164.92"),
            Decimal("250.0"),
            Decimal("1224"),
            Decimal("10554.58"),
            Decimal("1464.00"),
            Decimal("975.0"),
            Decimal("250.50"),
            Decimal("367.50"),
            Decimal("15.0"),
            Decimal("18072.00"),
        ),
        (
            Decimal("2000.00"),
            Decimal("195.20"),
            Decimal("30.0"),
            Decimal("49.00"),
            Decimal("155.32"),
            Decimal("250.0"),
            Decimal("0"),
            Decimal("1570.48"),
            Decimal("195.20"),
            Decimal("130.0"),
            Decimal("33.40"),
            Decimal("0"),
            Decimal("2.0"),
            Decimal("2360.60"),
        ),
    ],
)
def test_employment_contract_small_cost_no_fgsp_no_ppk(
    salary_base: Decimal,
    pension: Decimal,
    disability,
    sickness: Decimal,
    health_insurance: Decimal,
    cost: Decimal,
    tax_advance: Decimal,
    net: Decimal,
    emp_pension: Decimal,
    emp_disability: Decimal,
    accident: Decimal,
    fp: Decimal,
    fgsp: Decimal,
    total_gross: Decimal,
) -> None:
    rates = Rates()
    options = (
        EmploymentContractSettings()
        .SettingsBuilder()
        .is_increased_costs(False)
        .is_active_business(False)
        .is_fp_fgsp(True)
        .set_name("NAME SET")
        .is_under_26(False)
        .build()
    )
    ec = EmploymentContract(rates, options)
    ec.calculate(salary_base, SalaryType.GROSS)
    assert ec.is_calculated == True
    assert ec.salary_base == salary_base
    assert ec.pension_insurance == pension
    assert ec.disability_insurance == disability
    assert ec.sickness_insurance == sickness
    assert ec.social_insurance_sum == pension + disability + sickness
    assert ec.health_insurance == health_insurance
    assert ec.cost == cost
    assert ec.tax_advance_payment == tax_advance
    assert ec.net_salary == net
    assert ec.employer_pension_contribution == emp_pension
    assert ec.employer_disability_contribution == emp_disability
    assert ec.accident_insurance == accident
    assert ec.fp == fp
    assert ec.fgsp == fgsp
    assert ec.total_employer_cost == total_gross
    assert ec.name == "NAME SET"
    assert ec.get_rates() == rates
    assert ec.get_settings() == options

    ec2 = EmploymentContract(rates, options)
    ec2.calculate(ec.net_salary, SalaryType.NET)
    assert ec2.is_calculated == True
    assert ec2.salary_gross == ec.salary_gross


def test_employment_contract_comparing_to(
    employment_contract_gross_6000, mandate_contract_gross_6000
) -> None:
    assert employment_contract_gross_6000.is_compared == False
    assert len(employment_contract_gross_6000.to_compared_dict()) == 1
    employment_contract_gross_6000.compare_to(mandate_contract_gross_6000)
    assert employment_contract_gross_6000.is_calculated == True
    assert employment_contract_gross_6000.is_compared == True
    assert len(employment_contract_gross_6000.to_compared_dict()) == 3
    assert list(employment_contract_gross_6000.to_compared_dict().keys())[-2:] == [
        "COMPARED",
        "DIFFERANCE",
    ]
    assert (
        employment_contract_gross_6000.salary_compared_contract
        == mandate_contract_gross_6000
    )


def test_employment_contract_add_to_other(
    employment_contract_gross_6000, self_employment_gross_6000
) -> None:
    sum_contract = employment_contract_gross_6000 + self_employment_gross_6000

    assert (
        sum_contract.net_salary
        == employment_contract_gross_6000.net_salary
        + self_employment_gross_6000.net_salary
    )


def test_employment_contract_isub(
    employment_contract_gross_6000, self_employment_gross_6000
) -> None:
    net_salary = employment_contract_gross_6000.net_salary
    employment_contract_gross_6000 -= self_employment_gross_6000

    assert (
        employment_contract_gross_6000.net_salary
        == net_salary - self_employment_gross_6000.net_salary
    )


def test_employment_to_str(employment_contract_gross_6000) -> None:
    assert len(employment_contract_gross_6000.to_string().split("\n")) == 34
    assert (
        employment_contract_gross_6000.to_string().split("\n")[1].startswith("NAME..")
    )
    assert (
        employment_contract_gross_6000.to_string()
        == employment_contract_gross_6000.__str__()
    )
