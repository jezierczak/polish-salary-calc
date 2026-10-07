"""
Golden test case generator.

Runs the Python reference implementation over a deterministic grid of
rates / contract settings / salaries and stores the inputs together with the
calculated results in ``cases.json``. The file is the language-independent
specification of the calculator: ports (e.g. Kotlin) replay every case and must
reproduce the expected values to the grosz.

Regenerate with:  python -m tests.golden.generate
Verify with:      pytest tests/golden
"""

import dataclasses
import enum
import json
import types
import typing
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

from polish_salary_calc.contract_settings.contract_settings import ContractSettings
from polish_salary_calc.contract_settings.employment_contract_settings import (
    EmploymentContractSettings,
)
from polish_salary_calc.contract_settings.mandate_contract_settings import (
    MandateContractSettings,
    MandateContractType,
)
from polish_salary_calc.contract_settings.self_employment_settings import (
    HealthBase,
    SelfEmploymentSettings,
    SelfEmploymentType,
    TaxType,
)
from polish_salary_calc.contract_settings.work_contract_settings import (
    WorkContractSettings,
    WorkContractType,
)
from polish_salary_calc.contracts.base_contract import BaseContract
from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.salary import SalaryType

CASES_PATH = Path(__file__).with_name("cases.json")
FORMAT_VERSION = 1

CONTRACTS: dict[str, tuple[type[ContractSettings], type[BaseContract]]] = {
    "employment": (EmploymentContractSettings, EmploymentContract),
    "mandate": (MandateContractSettings, MandateContract),
    "work": (WorkContractSettings, WorkContract),
    "self_employment": (SelfEmploymentSettings, SelfEmployment),
}

# Result fields of Salary.to_dict() that carry no calculation result.
_SKIPPED_RESULT_FIELDS = {"name", "contract_type", "created_datetime"}
# Cumulative values kept on the contract but not part of to_dict().
_EXTRA_RESULT_FIELDS = (
    "social_security_base_total",
    "cost_fifty_total",
    "tax_base_total",
)
# Settings that are not calculation inputs.
_SKIPPED_SETTINGS_FIELDS = {"name"}

RATES_YEARS = (2025, 2026)

D = Decimal


# --------------------------------------------------------------------------- #
# (de)serialisation shared by the generator and the replaying test
# --------------------------------------------------------------------------- #


def _serialise(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, enum.Enum):
        return value.name
    return value


def _field_types(settings_cls: type[ContractSettings]) -> dict[str, Any]:
    return typing.get_type_hints(settings_cls)


def _deserialise(hint: Any, value: Any) -> Any:
    if value is None:
        return None
    if isinstance(hint, types.UnionType):  # e.g. Decimal | None
        hint = next(a for a in typing.get_args(hint) if a is not type(None))
    if isinstance(hint, type) and issubclass(hint, enum.Enum):
        return hint[value]
    if hint is Decimal:
        return Decimal(value)
    return value


def settings_to_dict(settings: ContractSettings) -> dict[str, Any]:
    return {
        f.name: _serialise(getattr(settings, f.name))
        for f in dataclasses.fields(settings)
        if f.name not in _SKIPPED_SETTINGS_FIELDS
    }


def settings_from_dict(
    settings_cls: type[ContractSettings], data: dict[str, Any]
) -> ContractSettings:
    hints = _field_types(settings_cls)
    return settings_cls(**{k: _deserialise(hints[k], v) for k, v in data.items()})


def rates_from_dict(data: dict[str, Any]) -> Rates:
    """Rebuild Rates from the yearly inputs stored in a case."""
    return Rates(
        description=data["description"],
        minimum_wage=D(data["minimum_wage"]),
        forecast_average_wage=D(data["forecast_average_wage"]),
        average_wage_q4=D(data["average_wage_q4"]),
    )


def rates_to_dict(rates: Rates) -> dict[str, Any]:
    """Inputs plus derived values; a port can check both."""
    return {
        "description": rates.description,
        "minimum_wage": str(rates.minimum_wage),
        "forecast_average_wage": str(rates.forecast_average_wage),
        "average_wage_q4": str(rates.average_wage_q4),
        "derived": {
            "standard_social_insurance_base": str(rates.standard_social_insurance_base),
            "reduced_social_insurance_base": str(rates.reduced_social_insurance_base),
            "social_insurance_cap": str(rates.social_insurance_cap),
            "health_insurance_base": str(rates.health_insurance_base),
            "unregistered_cap": str(rates.unregistered_cap),
            "health_insurance_lump_base": [
                str(x) for x in rates.health_insurance_lump_base
            ],
        },
    }


def calculate_case(
    case: dict[str, Any], rates_table: dict[str, dict[str, Any]]
) -> dict[str, str]:
    """Run the reference implementation for one case and return the results."""
    settings_cls, contract_cls = CONTRACTS[case["contract"]]
    rates = rates_from_dict(rates_table[case["rates"]])
    settings = settings_from_dict(settings_cls, case["settings"])
    contract = contract_cls(rates, settings)
    contract.calculate(D(case["salary"]), SalaryType[case["salary_type"]])

    result = {
        k: _serialise(v)
        for k, v in contract.to_dict().items()
        if k not in _SKIPPED_RESULT_FIELDS
    }
    for name in _EXTRA_RESULT_FIELDS:
        result[name] = _serialise(getattr(contract, name))
    return result


# --------------------------------------------------------------------------- #
# case grid
# --------------------------------------------------------------------------- #

Variant = tuple[str, Callable[[Rates], dict[str, Any]]]


def _v(label: str, **overrides: Any) -> Variant:
    return label, lambda _rates: dict(overrides)


def _employment_variants() -> list[Variant]:
    return [
        _v("default"),
        _v("increased_costs", increased_costs=True),
        _v("fifty", cost_fifty_ratio=D("0.5")),
        _v("fifty_near_cap", cost_fifty_ratio=D("0.5"), cost_fifty_sum=D("119500")),
        _v("fp_fgsp", fp_fgsp=True),
        _v("active_business", active_business=True),
        _v("under_26", under_26=True),
        _v("sick_pay", sick_pay=D("500")),
        _v("ppk_basic", employee_ppk=D("0.02"), employer_ppk=D("0.015")),
        _v("ppk_max", employee_ppk=D("0.04"), employer_ppk=D("0.04")),
        _v("ppk_reduced", employee_ppk=D("0.005"), employer_ppk=D("0.015")),
        _v("accident_rate", accident_insurance_rate=D("0.0067")),
        _v("deductions", salary_deductions=D("100")),
        (
            "social_near_cap",
            lambda r: {"social_security_base_sum": r.social_insurance_cap - D("3000")},
        ),
        (
            "social_over_cap",
            lambda r: {"social_security_base_sum": r.social_insurance_cap + D("1000")},
        ),
        _v("tax_near_threshold", tax_base_sum=D("118000")),
        _v("tax_over_threshold", tax_base_sum=D("125000")),
        _v(
            "combined",
            increased_costs=True,
            cost_fifty_ratio=D("0.5"),
            fp_fgsp=True,
            employee_ppk=D("0.02"),
            employer_ppk=D("0.015"),
            salary_deductions=D("50"),
        ),
    ]


def _mandate_variants() -> list[Variant]:
    variants: list[Variant] = []
    for ctype in MandateContractType:
        for is_fifty in (False, True):
            for lump in (False, True):
                for fp_fgsp in (False, True):
                    label = (
                        f"{ctype.name.lower()}"
                        f"{'_fifty' if is_fifty else ''}"
                        f"{'_lump' if lump else ''}"
                        f"{'_fpfgsp' if fp_fgsp else ''}"
                    )
                    variants.append(
                        _v(
                            label,
                            mandate_contract_type=ctype,
                            is_fifty=is_fifty,
                            is_a_lump_sum=lump,
                            fp=fp_fgsp,
                            fgsp=fp_fgsp,
                        )
                    )
    variants += [
        _v("ppk", employee_ppk=D("0.02"), employer_ppk=D("0.015")),
        (
            "social_near_cap",
            lambda r: {"social_security_base_sum": r.social_insurance_cap - D("3000")},
        ),
        _v("tax_over_threshold", tax_base_sum=D("125000")),
        _v("fifty_near_cap", is_fifty=True, cost_fifty_sum=D("119500")),
    ]
    return variants


def _work_variants() -> list[Variant]:
    variants: list[Variant] = []
    for ctype in WorkContractType:
        for is_fifty in (False, True):
            for lump in (False, True):
                label = (
                    f"{ctype.name.lower()}"
                    f"{'_fifty' if is_fifty else ''}"
                    f"{'_lump' if lump else ''}"
                )
                variants.append(
                    _v(
                        label,
                        work_contract_type=ctype,
                        is_fifty=is_fifty,
                        is_a_lump_sum=lump,
                    )
                )
    variants += [
        _v("tax_over_threshold", tax_base_sum=D("125000")),
        _v("fifty_near_cap", is_fifty=True, cost_fifty_sum=D("119500")),
    ]
    return variants


def _self_employment_variants() -> list[Variant]:
    variants: list[Variant] = []
    for stype in SelfEmploymentType:
        for tax in (TaxType.STANDARD, TaxType.LINE_TAX):
            variants.append(
                _v(
                    f"{stype.name.lower()}_{tax.name.lower()}",
                    self_employment_type=stype,
                    tax_type=tax,
                    health_base=HealthBase.NONE,
                )
            )
        for health in HealthBase:
            for rate in ("0.12", "0.055"):
                variants.append(
                    _v(
                        f"{stype.name.lower()}_lump_{rate}_health_{health.name.lower()}",
                        self_employment_type=stype,
                        tax_type=TaxType.A_LUMP_SUM,
                        tax_lump_rate=D(rate),
                        health_base=health,
                    )
                )
    base: dict[str, Any] = {
        "self_employment_type": SelfEmploymentType.COMMON,
        "tax_type": TaxType.STANDARD,
        "health_base": HealthBase.NONE,
    }
    variants += [
        _v("sick_pay", **base, is_sick_pay=True, sick_pay_days=5, month_days=30),
        _v("no_fp", **base, is_fp=False),
        _v("other_minimum_contract", **base, other_minimum_contract=True),
        _v("business_costs", **base, costs=D("1000")),
        _v("tax_over_threshold", **base, tax_base_sum=D("125000")),
        _v("line_tax_over_threshold", **{**base, "tax_type": TaxType.LINE_TAX}, tax_base_sum=D("125000")),
        (
            "social_near_cap",
            lambda r: {
                **base,
                "social_security_base_sum": r.social_insurance_cap - D("3000"),
            },
        ),
        _v("ppk_ignored_values", **base, employee_ppk=D("0.02"), employer_ppk=D("0.015")),
        _v(
            "lump_rate_not_allowed",
            **{**base, "tax_type": TaxType.A_LUMP_SUM},
            tax_lump_rate=D("0.13"),
        ),
    ]
    return variants


# (variants, gross salaries, net salaries)
GRID: dict[str, tuple[list[Variant], tuple[str, ...], tuple[str, ...]]] = {
    "employment": (
        _employment_variants(),
        ("1000", "3000", "6000", "15000"),
        ("5000",),
    ),
    "mandate": (
        _mandate_variants(),
        ("1000", "4806", "6000", "15000"),
        ("4000",),
    ),
    "work": (
        _work_variants(),
        ("1000", "4806", "6000", "15000"),
        ("4000",),
    ),
    "self_employment": (
        _self_employment_variants(),
        ("2000", "6000", "15000", "40000"),
        ("5000",),
    ),
}


def rates_table_for_years() -> dict[str, dict[str, Any]]:
    return {str(y): rates_to_dict(Rates.for_year(y)) for y in RATES_YEARS}


def generate_cases() -> list[dict[str, Any]]:
    """Return all cases; those that raise carry `expected_error` instead of `expected`."""
    cases: list[dict[str, Any]] = []
    rates_table = rates_table_for_years()
    for contract, (variants, gross, net) in GRID.items():
        settings_cls = CONTRACTS[contract][0]
        default_settings = settings_cls()
        for year in RATES_YEARS:
            rates = Rates.for_year(year)
            for label, make_overrides in variants:
                overrides = make_overrides(rates)
                settings = dataclasses.replace(default_settings, **overrides)
                salaries = [(s, "GROSS") for s in gross] + [(s, "NET") for s in net]
                for salary, salary_type in salaries:
                    case = {
                        "id": f"{contract}/{year}/{label}/{salary_type.lower()}-{salary}",
                        "contract": contract,
                        "rates": str(year),
                        "settings": settings_to_dict(settings),
                        "salary": salary,
                        "salary_type": salary_type,
                    }
                    try:
                        case["expected"] = calculate_case(case, rates_table)
                    except ValueError as exc:  # validation errors are part of the spec
                        case["expected_error"] = {
                            "type": type(exc).__name__,
                            "message": str(exc),
                        }
                    cases.append(case)
    return cases


INVALID_PPK = (
    ("employee_ppk", D("0.004")),
    ("employee_ppk", D("0.041")),
    ("employer_ppk", D("0.014")),
    ("employer_ppk", D("0.041")),
)


def generate_settings_validation() -> list[dict[str, Any]]:
    """Settings that must be rejected when they are created (before any calculation)."""
    cases: list[dict[str, Any]] = []
    for contract, (settings_cls, _) in CONTRACTS.items():
        for field, value in INVALID_PPK:
            settings = settings_to_dict(settings_cls())
            settings[field] = str(value)
            case: dict[str, Any] = {
                "id": f"{contract}/{field}-{value}",
                "contract": contract,
                "settings": settings,
            }
            try:
                settings_from_dict(settings_cls, settings)
            except ValueError as exc:
                case["expected_error"] = {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            else:  # pragma: no cover - the grid above must contain invalid values only
                raise AssertionError(f"{case['id']} was accepted")
            cases.append(case)
    return cases


def _dump(document: dict[str, Any]) -> str:
    """Compact JSON with one case per line, so git diffs stay readable."""

    def compact(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    head = {k: v for k, v in document.items() if k != "cases"}
    lines = [compact(head)[:-1] + ',"cases":[']
    cases = document["cases"]
    for i, case in enumerate(cases):
        lines.append(compact(case) + ("," if i < len(cases) - 1 else ""))
    lines.append("]}")
    return "\n".join(lines) + "\n"


def main() -> None:
    cases = generate_cases()
    document = {
        "format_version": FORMAT_VERSION,
        "description": (
            "Golden cases for polish-salary-calc. Decimals are strings; compare "
            "numerically. Enum values are given by name. A case has either "
            "`expected` (results) or `expected_error` (validation must fail)."
        ),
        "rates": rates_table_for_years(),
        "settings_validation": generate_settings_validation(),
        "cases": cases,
    }
    CASES_PATH.write_text(_dump(document), encoding="utf-8")
    errors = sum("expected_error" in c for c in cases)
    print(f"Wrote {len(cases)} cases ({errors} expecting an error) to {CASES_PATH}")


if __name__ == "__main__":
    main()
