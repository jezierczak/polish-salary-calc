import json
from decimal import Decimal

import pytest

from polish_salary_calc.rates.rates import Rates
from tests.golden.generate import (
    CASES_PATH,
    calculate_case,
    rates_from_dict,
    rates_to_dict,
)

DOCUMENT = json.loads(CASES_PATH.read_text(encoding="utf-8"))
CASES = DOCUMENT["cases"]
RATES = DOCUMENT["rates"]


def test_golden_file_is_not_empty() -> None:
    assert DOCUMENT["format_version"] == 1
    assert len(CASES) > 100
    assert any("expected_error" in c for c in CASES)
    assert len({c["id"] for c in CASES}) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_golden_case(case: dict) -> None:
    if "expected_error" in case:
        with pytest.raises(ValueError) as error:
            calculate_case(case, RATES)
        assert str(error.value) == case["expected_error"]["message"]
        return
    result = calculate_case(case, RATES)
    assert result.keys() == case["expected"].keys()
    for key, expected in case["expected"].items():
        assert Decimal(result[key]) == Decimal(expected), key


@pytest.mark.parametrize("year", sorted(RATES))
def test_golden_rates_derived_values(year: str) -> None:
    rates = rates_from_dict(RATES[year])
    assert rates_to_dict(rates) == RATES[year]
    assert rates_to_dict(Rates.for_year(int(year))) == RATES[year]


def test_every_case_references_known_rates() -> None:
    assert {c["rates"] for c in CASES} <= set(RATES)
