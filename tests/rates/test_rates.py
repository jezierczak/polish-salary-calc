import dataclasses
from decimal import Decimal
from typing import get_type_hints

import pytest
from polish_salary_calc.rates.rates import Rates, RatesDict


def test_rates_default(rates_default: Rates) -> None:
    assert isinstance(rates_default, Rates)
    assert rates_default.description == "Default Rates (2025 year second half)"


def test_rates_dict(rates_default: Rates, rates_dict: RatesDict) -> None:
    assert isinstance(rates_dict, dict)
    assert Rates.from_dict(rates_dict) == rates_default
    assert rates_default.to_dict() == rates_dict


def test_rates_change_one_character(rates_default: Rates) -> None:
    new_rates = rates_default
    new_rates.__setitem__("description", "Change Description")
    assert new_rates.description == "Change Description"
    assert new_rates.__getitem__("description") == "Change Description"
    assert new_rates.__getitem__("income_tax") == rates_default.income_tax


def test_rates_tax_to_mont_year(rates_default: Rates) -> None:
    assert (
        rates_default.tax_free
        == rates_default.income_tax[0] * rates_default.tax_free_base
    )
    assert rates_default.month_tax_free == rates_default.tax_free / 12


def test_wrong_key_set(rates_default: Rates) -> None:
    with pytest.raises(KeyError) as e:
        rates_default.__setitem__("wrong_key", "1")

    assert "Attribute wrong_key not found." in str(e.value)


def test_wrong_key_get(rates_default: Rates) -> None:
    with pytest.raises(AttributeError):
        rates_default.__getitem__("wrong_key")


def test_rates_dict_keys_match_dataclass_fields() -> None:
    assert set(get_type_hints(RatesDict)) == {
        f.name for f in dataclasses.fields(Rates)
    }


def test_rates_to_dict_returns_independent_copy(rates_default: Rates) -> None:
    data = rates_default.to_dict()
    data["minimum_wage"] = Decimal("1")
    assert rates_default.minimum_wage != Decimal("1")


def test_rates_derived_values_2025(rates_default: Rates) -> None:
    assert rates_default.standard_social_insurance_base == Decimal("5203.80")
    assert rates_default.reduced_social_insurance_base == Decimal("1399.80")
    assert rates_default.social_insurance_cap == Decimal("260190")
    assert rates_default.health_insurance_base == Decimal("3499.50")
    assert rates_default.unregistered_cap == Decimal("3499.50")
    assert rates_default.health_insurance_lump_base == (
        Decimal("5129.51"),
        Decimal("8549.18"),
        Decimal("15388.52"),
    )


def test_rates_for_year_2025_equals_default(rates_default: Rates) -> None:
    rates = Rates.for_year(2025)
    assert rates.description == "Rates 2025"
    assert rates.to_dict() | {"description": ""} == rates_default.to_dict() | {
        "description": ""
    }


def test_rates_for_year_2026() -> None:
    rates = Rates.for_year(2026)
    assert rates.minimum_wage == Decimal("4806")
    assert rates.standard_social_insurance_base == Decimal("5652.00")
    assert rates.reduced_social_insurance_base == Decimal("1441.80")
    assert rates.social_insurance_cap == Decimal("282600")
    assert rates.health_insurance_base == Decimal("3604.50")
    assert rates.health_insurance_lump_base == (
        Decimal("5537.18"),
        Decimal("9228.64"),
        Decimal("16611.55"),
    )


def test_rates_for_unknown_year() -> None:
    with pytest.raises(ValueError):
        Rates.for_year(1999)


def test_rates_derived_follow_inputs(rates_default: Rates) -> None:
    rates_default["minimum_wage"] = Decimal("5000")
    assert rates_default.health_insurance_base == Decimal("3750.00")
    assert rates_default.reduced_social_insurance_base == Decimal("1500.00")


def test_rates_derived_are_read_only(rates_default: Rates) -> None:
    with pytest.raises(AttributeError):
        rates_default["social_insurance_cap"] = Decimal("1")


def test_rates_exporter_contains_derived(rates_default: Rates) -> None:
    exported = rates_default.to_exporter_dict()["Rates"]
    assert exported["social_insurance_cap"] == Decimal("260190")
    assert exported["minimum_wage"] == Decimal("4666")
