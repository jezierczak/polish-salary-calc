from decimal import Decimal

import pytest

from polish_salary_calc.contract_settings.employment_contract_settings import (
    EmploymentContractSettings,
)
from polish_salary_calc.contract_settings.mandate_contract_settings import (
    MandateContractSettings,
)
from polish_salary_calc.contract_settings.self_employment_settings import (
    SelfEmploymentSettings,
)
from polish_salary_calc.contract_settings.work_contract_settings import (
    WorkContractSettings,
)
from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.rates.rates import Rates, RatesDict


@pytest.fixture
def rates_default() -> Rates:
    return Rates()


@pytest.fixture
def rates_dict(rates_default: Rates) -> RatesDict:
    return rates_default.to_dict()


@pytest.fixture
def employment_settings_default() -> EmploymentContractSettings:
    return EmploymentContractSettings()


@pytest.fixture
def mandate_settings_default() -> MandateContractSettings:
    return MandateContractSettings()


@pytest.fixture
def work_settings_default() -> WorkContractSettings:
    return WorkContractSettings()


@pytest.fixture
def self_employment_settings_default() -> SelfEmploymentSettings:
    return SelfEmploymentSettings()


@pytest.fixture
def employment_contract_gross_6000(
    rates_default, employment_settings_default
) -> EmploymentContract:
    ec = EmploymentContract(rates_default, employment_settings_default)
    ec.calculate(Decimal("6000"))
    return ec


@pytest.fixture
def mandate_contract_gross_6000(
    rates_default, mandate_settings_default
) -> MandateContract:
    mc = MandateContract(rates_default, mandate_settings_default)
    mc.calculate(Decimal("6000"))
    return mc


@pytest.fixture
def work_contract_gross_6000(rates_default, work_settings_default) -> WorkContract:
    wc = WorkContract(rates_default, work_settings_default)
    wc.calculate(Decimal("6000"))
    return wc


@pytest.fixture
def self_employment_gross_6000(
    rates_default, self_employment_settings_default
) -> SelfEmployment:
    se = SelfEmployment(rates_default, self_employment_settings_default)
    se.calculate(Decimal("6000"))
    return se
