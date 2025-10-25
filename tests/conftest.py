import pytest
from polish_salary_calc.rates.rates import Rates, RatesDict


@pytest.fixture
def rates_default()->Rates:
    return Rates()

@pytest.fixture
def rates_dict(rates_default: Rates) -> RatesDict:
    return rates_default.to_dict()