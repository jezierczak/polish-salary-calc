import warnings
from dataclasses import dataclass
from decimal import Decimal
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import override

from polish_salary_calc.salary.salaryexporter import SalaryExporter, SalaryExporterDict


# PPK contribution limits (Act on Employee Capital Plans, art. 26-27).
# The basic employee contribution is 2%; participants earning up to 120% of the
# minimum wage may declare a reduced one (min 0.5%). The library cannot verify
# that eligibility, because it depends on all of the person's remuneration.
MIN_EMPLOYEE_PPK = Decimal("0.005")
MAX_EMPLOYEE_PPK = Decimal("0.04")  # 2% basic + up to 2% additional
MIN_EMPLOYER_PPK = Decimal("0.015")
MAX_EMPLOYER_PPK = Decimal("0.04")  # 1.5% basic + up to 2.5% additional


@dataclass
class ContractSettings(SalaryExporter, ABC):
    """
    Abstract base class defining cumulative state and configuration shared between
    all contract types (Employment, Mandate, SelfEmployment, WorkContract).

    This class stores values that must be *propagated month-to-month* across yearly
    calculations, such as:
        - social insurance base accumulation (used to stop contributions above ZUS cap)
        - 50% cost limit usage (used until cost_threshold is reached)
        - taxable base progressive accumulation (for PIT tax threshold handling)
        - cumulative gross salary (optional reporting value)
        - PPK employee/employer contributions tracking
        - optional accident insurance rate (varies by employer industry risk class)

    It also acts as the configuration object passed into monthly contract calculation,
    where concrete subclasses define contract-specific calculation rules.
    """

    name: str | None = None
    current_month_gross_sum: Decimal = Decimal("0.0")
    social_security_base_sum: Decimal = Decimal("0.0")
    cost_fifty_sum: Decimal = Decimal("0.0")
    tax_base_sum: Decimal = Decimal("0.0")
    employee_ppk: Decimal = Decimal("0.0")
    employer_ppk: Decimal = Decimal("0.0")
    accident_insurance_rate: Decimal | None = None
    salary_deductions: Decimal = Decimal("0.0")

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """
        Check the settings against legal limits.

        Raises:
            ValueError: If a non-zero PPK contribution is outside the legal range
                (employee 0.5%-4%, employer 1.5%-4%).
        """
        if 0 < self.employer_ppk < MIN_EMPLOYER_PPK or (
            0 < self.employee_ppk < MIN_EMPLOYEE_PPK
        ):
            raise ValueError("Employer or employee PPK rate is too small")
        if self.employer_ppk > MAX_EMPLOYER_PPK or (
            self.employee_ppk > MAX_EMPLOYEE_PPK
        ):
            raise ValueError("Employer or employee PPK rate is too large")

    def __str__(self) -> str:
        """
        Return formatted string export of the configuration using SalaryExporter.
        """
        return self.to_string()

    @override
    def to_exporter_dict(self) -> SalaryExporterDict:
        """
        Convert internal configuration state to a dictionary structure suitable
        for export (JSON, Excel, CSV, Pandas DataFrame).

        Returns:
            SalaryExporterDict: A mapping where the key is the class name and the
            value is the internal attribute dictionary.
        """
        return {self.__class__.__name__: dict(self.__dict__)}

    @abstractmethod
    def to_dict(self) -> Mapping[str, object]:
        """
        Convert configuration to a simple dictionary representation that can be
        serialized or embedded inside salary summary objects.

        This method must be implemented by contract-specific subclasses to ensure
        that only relevant fields are exposed and formatted correctly.

        Returns:
            Mapping[str, object]: Serialisable contract settings data.
        """
        pass

    def options_type(self):
        """
        Get the user-friendly type name of the contract settings object.

        Returns:
            str: Name of the concrete class (e.g., 'EmploymentContractSettings').
        """
        return self.__class__.__name__


def __getattr__(name: str) -> type[ContractSettings]:
    # Backward compatibility for the former, misspelled class name.
    if name == "ContractSettngs":
        warnings.warn(
            "ContractSettngs is deprecated, use ContractSettings instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ContractSettings
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
