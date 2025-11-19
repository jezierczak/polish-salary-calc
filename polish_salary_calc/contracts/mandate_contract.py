from decimal import Decimal
from typing import override

from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contract_settings.mandate_contract_settings import (
    MandateContractSettings,
    MandateContractType,
)
from polish_salary_calc.contracts.base_contract import BaseContract
from polish_salary_calc.salary.salary_utilities import SalaryUtilities


class MandateContract(BaseContract[MandateContractSettings]):
    """Represents a Polish *umowa zlecenie* (mandate contract) salary calculation.

    This class implements all mandate contract–specific rules for insurance, costs, and taxation.
    It inherits base logic from `BaseContract` and customizes behavior depending on the
    contract type (`MandateContractType`), e.g. student under 26, same company, or common contract.

    Attributes:
        rates (Rates): The set of financial and tax rates used in calculations.
        contract_settings (MandateContractSettings): Configuration options for the contract,
            including type, 50% costs, lump-sum options, etc.
        input_salary (Decimal): The input base amount used for calculation (gross or net).
        salary_gross (Decimal): The calculated gross salary.
        net_salary (Decimal): The calculated net salary after taxes and contributions.
    """

    def __init__(
        self, rates: Rates, contract_settings: MandateContractSettings
    ) -> None:
        """Initializes the MandateContract instance.

        Args:
            rates (Rates): Rates object containing tax and contribution rates.
            contract_settings (MandateContractSettings): Contract configuration with mandate-specific options.
        """
        super().__init__(rates, contract_settings)

    @override
    def calculate_salary_base(self) -> Decimal:
        """Returns the salary base value.

        Returns:
            Decimal: The input salary base value.
        """
        return super().calculate_salary_base()

    @override
    def calculate_sick_pay(self) -> Decimal:
        """Mandate contracts do not include sick pay by default.

        Returns:
            Decimal: Always returns 0.0.
        """
        return Decimal("0.0")

    @override
    def calculate_salary_gross(self) -> Decimal:
        return super().calculate_salary_gross()

    @override
    def calculate_social_security_base(self) -> Decimal:
        """Calculates the base amount for social security contributions.

        The method varies by contract type:
        - For students under 26 and contracts with another employer meeting minimum wage: 0.
        - For common and same-company contracts: full salary base applies.

        Returns:
            Decimal: The social security base amount.
        Raises:
            NotImplementedError: If contract type is unknown.
        """
        match self.contract_settings.mandate_contract_type:
            case (
                MandateContractType.UNDER_26_AND_STUDENT
                | MandateContractType.OTHER_COMPANY_MIN_SALARY
            ):
                return Decimal("0.0")
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super().calculate_social_security_base()
            case _:
                raise NotImplementedError(
                    f"Unknown mandate contract type:  {self.contract_settings.mandate_contract_type}"
                )

    @override
    def calculate_pension_insurance(self) -> Decimal:
        """Calculates employee pension insurance contribution.

        Skips pension for student and other-company minimum salary contracts.

        Returns:
            Decimal: Pension insurance amount.
        """
        match self.contract_settings.mandate_contract_type:
            case (
                MandateContractType.UNDER_26_AND_STUDENT
                | MandateContractType.OTHER_COMPANY_MIN_SALARY
            ):
                return Decimal("0.0")
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super().calculate_pension_insurance()
            case _:
                raise NotImplementedError(
                    f"Unknown mandate contract type:  {self.contract_settings.mandate_contract_type}"
                )

    @override
    def calculate_disability_insurance(self) -> Decimal:
        match self.contract_settings.mandate_contract_type:
            case (
                MandateContractType.UNDER_26_AND_STUDENT
                | MandateContractType.OTHER_COMPANY_MIN_SALARY
            ):
                return Decimal("0.0")
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super().calculate_disability_insurance()
            case _:
                raise NotImplementedError(
                    f"Unknown mandate contract type:  {self.contract_settings.mandate_contract_type}"
                )

    @override
    def calculate_sickness_insurance(self) -> Decimal:
        match self.contract_settings.mandate_contract_type:
            case (
                MandateContractType.UNDER_26_AND_STUDENT
                | MandateContractType.OTHER_COMPANY_MIN_SALARY
                | MandateContractType.COMMON
            ):
                return Decimal("0.0")
            case MandateContractType.THE_SAME_COMPANY:
                return super().calculate_sickness_insurance()
            case _:
                raise NotImplementedError(
                    f"Unknown mandate contract type:  {self.contract_settings.mandate_contract_type}"
                )

    @override
    def calculate_cost(self) -> Decimal:
        if (
            self.contract_settings.mandate_contract_type
            == MandateContractType.UNDER_26_AND_STUDENT
        ):
            return Decimal("0")
        else:
            return super().calculate_cost()

    @override
    def _calculate_regular_cost(self) -> Decimal:
        """Calculates standard (20%) cost deduction for mandate contract.

        Rules:
            - For lump-sum contracts up to 200 PLN, no cost applies.
            - If `is_fifty` is False, use 20% cost.
            - Otherwise, returns 0.

        Returns:
            Decimal: The calculated cost value.
        """
        if self.contract_settings.is_a_lump_sum and self.salary_gross <= Decimal("200"):
            return Decimal("0.0")
        if not self.contract_settings.is_fifty:
            return self.health_insurance_base * self.rates.income_tax_deduction_20_50[0]
        else:
            return Decimal("0.0")

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        """Calculates 50% author rights cost deduction for mandate contracts.

        Only applies when `is_fifty` is True and not lump-sum below 200 PLN.

        Returns:
            Decimal: Author rights cost.
        """
        if not self.contract_settings.is_fifty:
            return Decimal("0.0")
        if self.contract_settings.is_a_lump_sum and self.salary_gross <= Decimal("200"):
            return Decimal("0.0")
        return SalaryUtilities.calculate_author_rights_cost(
            Decimal("0"),
            self.rates.income_tax_deduction_20_50[1],
            self.health_insurance_base,
            self.contract_settings.cost_fifty_sum,
            self.rates.cost_threshold,
        )

    @override
    def calculate_health_insurance_base(self) -> Decimal:
        if (
            self.contract_settings.mandate_contract_type
            == MandateContractType.UNDER_26_AND_STUDENT
        ):
            return Decimal("0.0")
        return super().calculate_health_insurance_base()

    @override
    def calculate_health_insurance(self) -> Decimal:
        return super().calculate_health_insurance()

    @override
    def calculate_tax_base(self) -> Decimal:
        return super().calculate_tax_base()

    @override
    def calculate_tax(self) -> Decimal:
        """Calculates income tax for the mandate contract.

        Tax rules:
            - Students under 26 are tax-exempt.
            - Lump-sum contracts up to 200 PLN are taxed at 12%.
            - Otherwise, uses standard tax base with free amount applied.

        Returns:
            Decimal: Calculated income tax.
        """
        if (
            self.contract_settings.mandate_contract_type
            == MandateContractType.UNDER_26_AND_STUDENT
        ):
            return Decimal("0.0")

        if (
            self.contract_settings.is_a_lump_sum
            and self.salary_gross <= Decimal("200")
            and self.contract_settings.mandate_contract_type
            != MandateContractType.THE_SAME_COMPANY
        ):
            return self.salary_gross * self.rates.income_tax[0]

        out = self.tax_base * self.rates.income_tax[0] - self.rates.month_tax_free
        return out if out > Decimal("0.0") else Decimal("0.0")

    @override
    def calculate_ppk_tax(self) -> Decimal:
        if self.contract_settings.mandate_contract_type == (
            MandateContractType.UNDER_26_AND_STUDENT
            or MandateContractType.OTHER_COMPANY_MIN_SALARY
        ):
            return Decimal("0.0")
        return super().calculate_ppk_tax()

    @override
    def calculate_salary_deductions(self) -> Decimal:
        return super().calculate_salary_deductions()

    @override
    def calculate_employee_ppk_contribution(self) -> Decimal:
        if self.contract_settings.mandate_contract_type == (
            MandateContractType.UNDER_26_AND_STUDENT
            or MandateContractType.OTHER_COMPANY_MIN_SALARY
        ):
            return Decimal("0.0")
        return super().calculate_employee_ppk_contribution()

    @override
    def calculate_net_salary(self) -> Decimal:
        return super().calculate_net_salary()

    @override
    def calculate_pension_contribution(self) -> Decimal:
        return super().calculate_pension_contribution()

    @override
    def calculate_disability_contribution(self) -> Decimal:
        return super().calculate_disability_contribution()

    @override
    def calculate_accident_insurance(self) -> Decimal:
        return super().calculate_accident_insurance()

    @override
    def calculate_fp(self) -> Decimal:
        """Calculates the Labor Fund contribution.

        Returns zero if `fp` flag is disabled.

        Returns:
            Decimal: FP contribution or 0.
        """
        if not self.contract_settings.fp:
            return Decimal("0")
        else:
            return super().calculate_fp()

    @override
    def calculate_fgsp(self) -> Decimal:
        """Calculates FGŚP (Guaranteed Employee Benefits Fund) contribution.

        Returns zero if `fgsp` flag is disabled.

        Returns:
            Decimal: FGŚP contribution or 0.
        """
        if not self.contract_settings.fgsp:
            return Decimal("0")
        else:
            return super().calculate_fgsp()

    @override
    def calculate_employer_ppk_contribution(self) -> Decimal:
        if self.contract_settings.mandate_contract_type == (
            MandateContractType.UNDER_26_AND_STUDENT
            or MandateContractType.OTHER_COMPANY_MIN_SALARY
        ):
            return Decimal("0.0")
        return super().calculate_employer_ppk_contribution()

    @override
    def calculate_total_employer_cost(self) -> Decimal:
        return super().calculate_total_employer_cost()
