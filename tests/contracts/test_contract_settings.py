from decimal import Decimal

import pytest

from polish_salary_calc.contract_settings import contract_settings
from polish_salary_calc.contract_settings.contract_settings import ContractSettings
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
from polish_salary_calc.rates.rates import Rates


def test_old_misspelled_name_is_deprecated_alias() -> None:
    with pytest.warns(DeprecationWarning):
        assert contract_settings.ContractSettngs is ContractSettings


def test_unknown_attribute_still_raises() -> None:
    with pytest.raises(AttributeError):
        contract_settings.NoSuchName


ALL_SETTINGS = [
    EmploymentContractSettings,
    MandateContractSettings,
    WorkContractSettings,
    SelfEmploymentSettings,
]


@pytest.mark.parametrize("settings_cls", ALL_SETTINGS)
@pytest.mark.parametrize(
    "employee,employer",
    [("0.004", "0.015"), ("0.02", "0.01"), ("0.0049", "0")],
)
def test_too_small_ppk_rejected_on_construction(
    settings_cls, employee: str, employer: str
) -> None:
    with pytest.raises(ValueError):
        settings_cls(employee_ppk=Decimal(employee), employer_ppk=Decimal(employer))


@pytest.mark.parametrize(
    "settings_cls",
    [EmploymentContractSettings, MandateContractSettings, WorkContractSettings],
)
def test_too_small_ppk_rejected_by_builder(settings_cls) -> None:
    builder = settings_cls.builder().set_employee_ppk(Decimal("0.004"))
    with pytest.raises(ValueError):
        builder.build()


@pytest.mark.parametrize("settings_cls", ALL_SETTINGS)
def test_valid_and_zero_ppk_accepted(settings_cls) -> None:
    settings_cls()
    settings_cls(employee_ppk=Decimal("0.02"), employer_ppk=Decimal("0.015"))
    # reduced employee contribution and both upper limits
    settings_cls(employee_ppk=Decimal("0.005"), employer_ppk=Decimal("0.04"))
    settings_cls(employee_ppk=Decimal("0.04"), employer_ppk=Decimal("0.015"))


@pytest.mark.parametrize("settings_cls", ALL_SETTINGS)
@pytest.mark.parametrize(
    "employee,employer",
    [("0.041", "0.015"), ("0.02", "0.041"), ("0.1", "0.015")],
)
def test_too_large_ppk_rejected(settings_cls, employee: str, employer: str) -> None:
    with pytest.raises(ValueError, match="too large"):
        settings_cls(employee_ppk=Decimal(employee), employer_ppk=Decimal(employer))


def test_contract_rejects_settings_mutated_to_invalid_ppk() -> None:
    settings = EmploymentContractSettings()
    settings.employee_ppk = Decimal("0.004")
    with pytest.raises(ValueError):
        EmploymentContract(Rates(), settings)


def test_update_options_rejects_invalid_ppk_and_keeps_old_settings() -> None:
    old = EmploymentContractSettings()
    contract = EmploymentContract(Rates(), old)
    bad = EmploymentContractSettings()
    bad.employer_ppk = Decimal("0.01")
    with pytest.raises(ValueError):
        contract.update_options(bad)
    assert contract.contract_settings is old
