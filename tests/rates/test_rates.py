import pytest
from polish_salary_calc.rates.rates import Rates,RatesDict

def test_rates_default(rates_default: Rates) -> None:
    assert isinstance(rates_default, Rates)
    assert rates_default.description == 'Default Rates (2025 year second half)'

def test_rates_dict(rates_default: Rates,rates_dict: RatesDict) -> None:
    assert isinstance(rates_dict, dict)
    assert Rates.from_dict(rates_dict) == rates_default
    assert rates_default.to_dict() == rates_dict

def test_rates_change_one_character(rates_default:Rates) -> None:
    new_rates = rates_default
    new_rates.__setitem__("description", "Change Description")
    assert new_rates.description == "Change Description"
    assert new_rates.__getitem__("description")== "Change Description"
    assert new_rates.__getitem__("income_tax")== rates_default.income_tax

def test_rates_tax_to_mont_year(rates_default:Rates) -> None:
    assert rates_default.tax_free == rates_default.income_tax[0]*rates_default.tax_free_amount
    assert rates_default.month_tax_free == rates_default.tax_free/12

def test_wrong_key_set(rates_default:Rates) -> None:
    with pytest.raises(KeyError) as e:
        rates_default.__setitem__("wrong_key","1")

    assert 'Attribute wrong_key not found.' in str(e.value)

def test_wrong_key_get(rates_default:Rates) -> None:
    with pytest.raises(AttributeError):
        rates_default.__getitem__("wrong_key")

