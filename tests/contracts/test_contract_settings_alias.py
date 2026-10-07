import pytest

from polish_salary_calc.contract_settings import contract_settings
from polish_salary_calc.contract_settings.contract_settings import ContractSettings


def test_old_misspelled_name_is_deprecated_alias() -> None:
    with pytest.warns(DeprecationWarning):
        assert contract_settings.ContractSettngs is ContractSettings


def test_unknown_attribute_still_raises() -> None:
    with pytest.raises(AttributeError):
        contract_settings.NoSuchName
