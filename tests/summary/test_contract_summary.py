from decimal import Decimal

import pytest

from polish_salary_calc.summary.contract_summary import YearContractSummary, Months


def test_year_contract_salary_employment_contract_first_init(
    rates_default, employment_settings_default, employment_contract_gross_6000
) -> None:
    ycs = YearContractSummary(
        rates_default, employment_settings_default, Decimal("6000")
    )

    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs.is_compared == False
    assert ycs.is_calculated == True
    assert ycs["JAN"] == ycs["MAR"]
    assert ycs.summary.net_salary == ycs["FEB"].net_salary * 12


def test_year_contract_salary_mandate_contract_init_from_contract(
    rates_default, mandate_settings_default, mandate_contract_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(mandate_contract_gross_6000)

    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs.is_compared == False
    assert ycs.is_calculated == True
    assert ycs["JAN"] == mandate_contract_gross_6000
    assert ycs.summary.net_salary == mandate_contract_gross_6000.net_salary * 12


def test_year_contract_salary_work_contract_compare_to(
    rates_default, work_settings_default, work_contract_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(work_contract_gross_6000)

    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs.is_compared == False
    assert ycs.is_calculated == True
    assert ycs["JAN"] == work_contract_gross_6000
    assert ycs.summary.net_salary == work_contract_gross_6000.net_salary * 12
    assert (
        ycs.compare_to(work_contract_gross_6000).salary_difference.net_salary
        == ycs.summary.net_salary - work_contract_gross_6000.net_salary
    )
    assert ycs.is_compared == True
    assert ycs.summary == ycs["SUMMARY"]
    assert ycs.salary_difference == ycs["DIFFERENCE"]


def test_year_contract_salary_self_employment_to_string(
    rates_default, self_employment_settings_default, self_employment_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(self_employment_gross_6000)

    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs.is_compared == False
    assert ycs.is_calculated == True
    assert ycs["JAN"] == self_employment_gross_6000
    assert (
        ycs.compare_to(self_employment_gross_6000).salary_difference.net_salary
        == ycs.summary.net_salary - self_employment_gross_6000.net_salary
    )
    assert ycs.is_compared == True
    assert ycs.summary == ycs["SUMMARY"]
    assert ycs.salary_difference == ycs["DIFFERENCE"]
    assert str("SUMMARY") in ycs.to_string()
    assert str("DIFFERENCE") in ycs.to_string()


def test_year_contract_salary_self_employment_to_exported_dict(
    rates_default, self_employment_settings_default, self_employment_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(self_employment_gross_6000)

    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs.to_exporter_dict()["JAN"] == ycs["JAN"].to_dict()
    assert ycs.to_exporter_dict()["SUMMARY"] == ycs["SUMMARY"].to_dict()


def test_year_contract_salary_employment_contract_modify_month(
    rates_default, employment_settings_default, employment_contract_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(employment_contract_gross_6000)

    ycs.modify_month_contracts([Months.APR, Months.MAY, Months.JAN], enabled=False)
    ycs.modify_month_contracts([Months.FEB], salary_base=Decimal("5000"))
    assert ycs.is_calculated == False
    assert ycs.is_calculated == False
    ycs.calculate()

    assert ycs["JAN"].net_salary == 0
    assert ycs["APR"].net_salary == 0
    assert ycs["MAY"].net_salary == 0
    assert ycs["FEB"].salary_gross == Decimal("5000")
    assert ycs[
        "SUMMARY"
    ].salary_gross == employment_contract_gross_6000.salary_gross * 9 - Decimal("1000")


def test_year_contract_salary_employment_contract_compared_raises(
    rates_default, employment_settings_default, employment_contract_gross_6000
) -> None:
    ycs = YearContractSummary.from_contract(employment_contract_gross_6000)

    with pytest.raises(RuntimeError) as e:
        ycs.compare_to(employment_contract_gross_6000)


def test_year_contract_salary_employment_contract_compared_to_other_ycs(
    rates_default,
    employment_settings_default,
    employment_contract_gross_6000,
    mandate_contract_gross_6000,
) -> None:
    ycs = YearContractSummary.from_contract(employment_contract_gross_6000)
    ycs.calculate()

    ycs2 = YearContractSummary.from_contract(mandate_contract_gross_6000)
    ycs.calculate()

    ycs.compare_to(ycs2)

    assert ycs.is_compared == True
    assert ycs.salary_difference == ycs.summary - ycs2.summary


# def test_year_contract_salary_export(employment_contract_gross_6000,tmp_path) -> None:
#     # ycs = YearContractSummary.from_contract(employment_contract_gross_6000)
#     ycs = MagicMock(YearContractSummary)
#     ycs.calculate()
#     ycs.to_excel(tmp_path/"exported.xlsx")
#
#     assert ycs.to_excel.called_once_with(tmp_path/"exported.xlsx")
