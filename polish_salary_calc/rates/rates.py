import json
from dataclasses import asdict, dataclass
from decimal import ROUND_HALF_UP, Decimal
from importlib import resources
from typing import Self, TypedDict, cast, override

from polish_salary_calc.salary.salaryexporter import SalaryExporter

# Statutory coefficients; the yearly inputs live in `Rates` / `data/<year>.json`.
STANDARD_SOCIAL_BASE_RATIO = Decimal("0.6")
REDUCED_SOCIAL_BASE_RATIO = Decimal("0.3")
SOCIAL_INSURANCE_CAP_MULTIPLIER = Decimal("30")
HEALTH_BASE_RATIO = Decimal("0.75")
LUMP_HEALTH_REVENUE_CAPS = (Decimal("60000"), Decimal("300000"))
LUMP_HEALTH_BASE_RATIOS = (Decimal("0.6"), Decimal("1"), Decimal("1.8"))

# Read-only values calculated from `minimum_wage`, `forecast_average_wage`
# and `average_wage_q4`.
_DERIVED_FIELDS = (
    "standard_social_insurance_base",
    "reduced_social_insurance_base",
    "social_insurance_cap",
    "health_insurance_base",
    "unregistered_cap",
    "se_lump_health_insurance_cap",
    "health_insurance_lump_base",
)


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class RatesDict(TypedDict):
    """
    Typed dictionary structure defining expected fields for Rates configuration.

    Attributes:
        description (str): Opis zestawu stawek (np. okres obowiązywania).
        pension_insurance_rate (Decimal): Stawka składki emerytalnej (ubezpieczenie społeczne).
        disability_insurance_rate (Decimal): Stawka składki rentowej.
        sickness_insurance_rate (Decimal): Stawka składki chorobowej.
        income_tax_deduction (tuple[Decimal, Decimal]): Kwoty zmniejszające podatek dla dwóch progów.
        tax_free_base (Decimal): Kwota wolna od podatku.
        income_tax_deduction_20_50 (tuple[Decimal, Decimal]): Koszty autorskie 20%/50%.
        income_tax (tuple[Decimal, Decimal]): Stawki podatku PIT (pierwszy próg, drugi próg).
        line_tax_rate (Decimal): Stawka podatku liniowego.
        health_insurance_rate (Decimal): Stawka składki zdrowotnej dla zasad ogólnych.
        health_insurance_rate_line_tax (Decimal): Stawka składki zdrowotnej dla podatku liniowego.
        employer_pension_contribution_rate (Decimal): Składka pracodawcy na ZUS emerytalne.
        employer_disability_contribution_rate (Decimal): Składka pracodawcy na ZUS rentowe.
        accident_insurance_rate (Decimal): Składka wypadkowa.
        fp_rate (Decimal): Składka na Fundusz Pracy.
        fgsp_rate (Decimal): Składka na FGŚP.
        minimum_wage (Decimal): Aktualna płaca minimalna brutto.
        forecast_average_wage (Decimal): Prognozowane przeciętne wynagrodzenie (ustawa budżetowa).
        average_wage_q4 (Decimal): Przeciętne wynagrodzenie z IV kwartału roku poprzedniego (GUS).
        tax_threshold (Decimal): Próg podatkowy PIT.
        cost_threshold (Decimal): Próg kosztowy.
    """

    description: str
    pension_insurance_rate: Decimal
    disability_insurance_rate: Decimal
    sickness_insurance_rate: Decimal
    income_tax_deduction: tuple[Decimal, Decimal]
    tax_free_base: Decimal
    income_tax_deduction_20_50: tuple[Decimal, Decimal]
    income_tax: tuple[Decimal, Decimal]
    line_tax_rate: Decimal
    health_insurance_rate: Decimal
    health_insurance_rate_line_tax: Decimal
    employer_pension_contribution_rate: Decimal
    employer_disability_contribution_rate: Decimal
    accident_insurance_rate: Decimal
    fp_rate: Decimal
    fgsp_rate: Decimal
    minimum_wage: Decimal
    forecast_average_wage: Decimal
    average_wage_q4: Decimal
    tax_threshold: Decimal  # próg podatkowy
    cost_threshold: Decimal


@dataclass
class Rates(SalaryExporter):
    """
    Container for tax and insurance rate values used in salary calculations.
    Represents a parameter set for a specific legal period or tax configuration.

    This class is intended to be used by salary calculators and exporters.
    Each field corresponds to a fixed statutory rate or threshold.

    Attributes:
        description: Opis zestawu stawek (np. rok / półrocze).
        pension_insurance_rate: Stawka składki emerytalnej.
        disability_insurance_rate: Stawka składki rentowej.
        sickness_insurance_rate: Stawka składki chorobowej.
        income_tax_deduction: Koszty uzyskania przychodu (standardowe, podwyższone).
        income_tax_deduction_20_50: Koszty uzyskania przychodu 20% / 50%.
        income_tax: Stawki podatku PIT (próg pierwszy, prog drugi).
        line_tax_rate: Stawka podatku liniowego 19%.
        tax_free_base: Kwota wolna od podatku.
        health_insurance_rate: Składka zdrowotna dla zasad ogólnych (pracownik).
        health_insurance_rate_line_tax: Składka zdrowotna dla podatku liniowego.
        employer_pension_contribution_rate: Składka emerytalna pracodawcy.
        employer_disability_contribution_rate: Składka rentowa pracodawcy.
        accident_insurance_rate: Składka wypadkowa.
        fp_rate: Składka na Fundusz Pracy.
        fgsp_rate: Składka na Fundusz Gwarantowanych Świadczeń Pracowniczych.
        minimum_wage: Płaca minimalna brutto.
        forecast_average_wage: Prognozowane przeciętne wynagrodzenie (ustawa budżetowa).
        average_wage_q4: Przeciętne wynagrodzenie z IV kwartału roku poprzedniego (GUS).
        tax_threshold: Próg podatkowy PIT.
        cost_threshold: Próg kosztowy.

    Wartości zależne od trzech wejść rocznych (`minimum_wage`, `forecast_average_wage`,
    `average_wage_q4`) są właściwościami tylko do odczytu:
        standard_social_insurance_base: 60% prognozowanego przeciętnego wynagrodzenia.
        reduced_social_insurance_base: 30% płacy minimalnej (mały ZUS).
        social_insurance_cap: 30-krotność prognozowanego przeciętnego wynagrodzenia.
        health_insurance_base: 75% płacy minimalnej.
        unregistered_cap: Limit przychodu działalności nieewidencjonowanej.
        se_lump_health_insurance_cap: Progi przychodu dla ryczałtowej składki zdrowotnej.
        health_insurance_lump_base: 60% / 100% / 180% wynagrodzenia z IV kwartału.
    """

    description: str = "Default Rates (2025 year second half)"
    pension_insurance_rate: Decimal = Decimal("0.0976")
    disability_insurance_rate: Decimal = Decimal("0.015")
    sickness_insurance_rate: Decimal = Decimal("0.0245")
    income_tax_deduction: tuple[Decimal, Decimal] = (Decimal("250"), Decimal("300"))
    income_tax_deduction_20_50: tuple[Decimal, Decimal] = (
        Decimal("0.2"),
        Decimal("0.5"),
    )
    income_tax: tuple[Decimal, Decimal] = (Decimal("0.12"), Decimal("0.32"))
    line_tax_rate: Decimal = Decimal("0.19")
    tax_free_base: Decimal = Decimal("30000")
    health_insurance_rate: Decimal = Decimal("0.09")
    health_insurance_rate_line_tax: Decimal = Decimal("0.049")
    employer_pension_contribution_rate: Decimal = Decimal("0.0976")
    employer_disability_contribution_rate: Decimal = Decimal("0.0650")
    accident_insurance_rate: Decimal = Decimal("0.0167")
    fp_rate: Decimal = Decimal("0.0245")
    fgsp_rate: Decimal = Decimal("0.001")
    minimum_wage: Decimal = Decimal("4666")
    forecast_average_wage: Decimal = Decimal("8673")
    average_wage_q4: Decimal = Decimal("8549.18")
    tax_threshold: Decimal = Decimal("120000")
    cost_threshold: Decimal = Decimal("120000")

    @property
    def standard_social_insurance_base(self) -> Decimal:
        """60% of the forecast average wage (full ZUS base)."""
        return _money(self.forecast_average_wage * STANDARD_SOCIAL_BASE_RATIO)

    @property
    def reduced_social_insurance_base(self) -> Decimal:
        """30% of the minimum wage (reduced ZUS base)."""
        return _money(self.minimum_wage * REDUCED_SOCIAL_BASE_RATIO)

    @property
    def social_insurance_cap(self) -> Decimal:
        """Annual pension/disability contribution cap (30x forecast average wage)."""
        return self.forecast_average_wage * SOCIAL_INSURANCE_CAP_MULTIPLIER

    @property
    def health_insurance_base(self) -> Decimal:
        """75% of the minimum wage."""
        return _money(self.minimum_wage * HEALTH_BASE_RATIO)

    @property
    def unregistered_cap(self) -> Decimal:
        """Revenue limit of an unregistered business activity."""
        return self.health_insurance_base

    @property
    def se_lump_health_insurance_cap(self) -> tuple[Decimal, Decimal]:
        """Revenue thresholds (60k / 300k) for the lump-sum health insurance base."""
        return LUMP_HEALTH_REVENUE_CAPS

    @property
    def health_insurance_lump_base(self) -> tuple[Decimal, Decimal, Decimal]:
        """Lump-sum health insurance bases: 60% / 100% / 180% of the Q4 average wage."""
        low, mid, high = LUMP_HEALTH_BASE_RATIOS
        return (
            _money(self.average_wage_q4 * low),
            _money(self.average_wage_q4 * mid),
            _money(self.average_wage_q4 * high),
        )

    @property
    def tax_free(self) -> Decimal:
        """
        Returns:
            Decimal: Annual tax-free deduction expressed as (low tax rate * tax_free_base).
        """
        return self.income_tax[0] * self.tax_free_base

    @property
    def month_tax_free(self) -> Decimal:
        """
        Returns:
            Decimal: Monthly portion of the tax-free amount.
        """
        return self.tax_free / 12

    @classmethod
    def for_year(cls, year: int) -> Self:
        """
        Load the yearly rate inputs (minimum wage, forecast and Q4 average wage)
        from the bundled `data/<year>.json`; all other rates keep their defaults.

        Args:
            year (int): Calendar year, e.g. 2026.

        Returns:
            Rates: Rates for the given year.

        Raises:
            ValueError: If there is no bundled data for the given year.
        """
        path = resources.files(__package__).joinpath("data", f"{year}.json")
        if not path.is_file():
            raise ValueError(f"No rates data for year {year}.")
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            description=raw["description"],
            minimum_wage=Decimal(raw["minimum_wage"]),
            forecast_average_wage=Decimal(raw["forecast_average_wage"]),
            average_wage_q4=Decimal(raw["average_wage_q4"]),
        )

    @classmethod
    def from_dict(cls, data: RatesDict) -> Self:
        """
        Instantiates a Rates object from a dictionary matching RatesDict schema.

        Args:
            data (RatesDict): Source data dictionary.

        Returns:
            Rates: A new Rates instance.
        """
        return cls(**data)

    def to_dict(self) -> RatesDict:
        """
        Converts the Rates instance into a dictionary matching RatesDict.

        Returns:
            RatesDict: Independent copy of the instance's fields; modifying it
            does not affect this Rates object. Derived values are not included.
        """
        return cast(RatesDict, asdict(self))

    @override
    def to_exporter_dict(self) -> dict[str, dict[str, str | Decimal | bool]]:
        """
        Prepares the object for standardized export (fields plus derived values).

        Returns:
            dict: Export-structured dictionary payload.
        """
        data = cast(dict[str, str | Decimal | bool], self.to_dict())
        for name in _DERIVED_FIELDS:
            data[name] = getattr(self, name)
        return {self.__class__.__name__: data}

    def __getitem__(self, item: str) -> Decimal | str:
        """
        Allows retrieving attribute values via dictionary-like access.

        Args:
            item (str): Attribute name.

        Returns:
            Decimal | str: Value of requested attribute.
        """
        return getattr(self, item)

    def __setitem__(self, key: str, value: Decimal | str) -> None:
        """
        Allows mutation of attributes via dictionary-like access.

        Args:
            key (str): Attribute name.
            value (Decimal | str): Value to assign.

        Raises:
            AttributeError: If the attribute is derived (read-only).
            KeyError: If attribute does not exist.
        """
        if key in _DERIVED_FIELDS:
            raise AttributeError(
                f"Attribute {key} is derived and read-only; change "
                "minimum_wage, forecast_average_wage or average_wage_q4 instead."
            )
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute {key} not found.")

    def __str__(self) -> str:
        """
        Returns:
            str: Human-readable string representation suitable for logs or console output.
        """
        return self.to_string()
