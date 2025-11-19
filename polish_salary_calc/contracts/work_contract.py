from decimal import Decimal
from typing import override
from polish_salary_calc.contract_settings.work_contract_settings import (
    WorkContractSettings,
    WorkContractType,
)
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contracts.base_contract import BaseContract
from polish_salary_calc.salary.salary_utilities import SalaryUtilities


class WorkContract(BaseContract[WorkContractSettings]):
    """Represents a Polish *umowa o dzieło* (work contract) salary calculation.

    This class implements all cost, tax, and insurance rules for "umowa o dzieło"
    contracts, depending on whether the work is performed for the same company
    or for a different one.

    Attributes:
        rates (Rates): The current tax and insurance rates used for calculations.
        contract_settings (WorkContractSettings): Configuration options including
            contract type, 50% cost flag, and lump-sum rules.
        salary_base (Decimal): Declared base income.
        salary_gross (Decimal): Calculated gross income.
        net_salary (Decimal): Calculated net income after all deductions.
    """

    def __init__(self, rates: Rates, contract_settings: WorkContractSettings) -> None:
        """Initializes the WorkContract instance.

        Args:
            rates (Rates): A Rates object containing tax and insurance rates.
            contract_settings (WorkContractSettings): Settings defining the contract type and parameters.
        """
        super().__init__(rates, contract_settings)

    @override
    def calculate_salary_base(self) -> Decimal:
        """Returns the input salary base.

        Returns:
            Decimal: The input salary base value.
        """
        return super().calculate_salary_base()

    @override
    def calculate_sick_pay(self) -> Decimal:
        """Work contracts do not include sick pay.

        Returns:
            Decimal: Always returns 0.0.
        """
        return Decimal("0.0")

    @override
    def calculate_salary_gross(self) -> Decimal:
        return super().calculate_salary_gross()

    @override
    def calculate_social_security_base(self) -> Decimal:
        """Calculates the social security base depending on the contract type.

        Rules:
            - COMMON: No social security contributions.
            - THE_SAME_COMPANY: Full base applies.

        Returns:
            Decimal: Calculated social security base.
        """
        match self.contract_settings.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal("0.0")
            case WorkContractType.THE_SAME_COMPANY:
                return super().calculate_social_security_base()
        return Decimal("0.0")

    @override
    def calculate_pension_insurance(self) -> Decimal:
        """Calculates pension insurance based on the contract type.

        Rules:
            - COMMON: No pension insurance.
            - THE_SAME_COMPANY: Standard pension insurance applies.

        Returns:
            Decimal: Pension insurance value.
        """
        match self.contract_settings.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal("0.0")
            case WorkContractType.THE_SAME_COMPANY:
                return super().calculate_pension_insurance()
        return Decimal("0.0")

    @override
    def calculate_disability_insurance(self) -> Decimal:
        """Calculates disability insurance based on the contract type.

        Returns:
            Decimal: Disability insurance amount or 0.0 for common contracts.
        """
        match self.contract_settings.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal("0.0")
            case WorkContractType.THE_SAME_COMPANY:
                return super().calculate_disability_insurance()
        return Decimal("0.0")

    @override
    def calculate_sickness_insurance(self) -> Decimal:
        """Calculates sickness insurance based on the contract type.

        Returns:
            Decimal: Sickness insurance amount or 0.0 for common contracts.
        """
        match self.contract_settings.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal("0.0")
            case WorkContractType.THE_SAME_COMPANY:
                return super().calculate_sickness_insurance()
        return Decimal("0.0")

    @override
    def calculate_cost(self) -> Decimal:
        return super().calculate_cost()

    @override
    def _calculate_regular_cost(self) -> Decimal:
        """Calculates standard (20%) cost deduction for work contracts.

        Rules:
            - Lump-sum contracts up to 200 PLN are exempt.
            - If `is_fifty` is False, applies standard 20% cost ratio.
            - The cost base depends on whether the contract is with the same company.

        Returns:
            Decimal: Regular cost value.
        """
        if self.contract_settings.is_a_lump_sum and self.salary_gross <= Decimal("200"):
            return Decimal("0.0")
        if not self.contract_settings.is_fifty:
            if (
                self.contract_settings.work_contract_type
                == WorkContractType.THE_SAME_COMPANY
            ):
                return (
                    self.health_insurance_base
                    * self.rates.income_tax_deduction_20_50[0]
                )
            else:
                return self.salary_gross * self.rates.income_tax_deduction_20_50[0]
        else:
            return Decimal("0.0")

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        """Calculates 50% author rights cost deduction if applicable.

        Rules:
            - Applies only when `is_fifty` is True.
            - Lump-sum contracts up to 200 PLN are excluded.
            - Base differs for same-company vs common contracts.

        Returns:
            Decimal: Author rights cost deduction.
        """
        if not self.contract_settings.is_fifty:
            return Decimal("0.0")
        if self.contract_settings.is_a_lump_sum and self.salary_gross <= Decimal("200"):
            return Decimal("0.0")
        if self.contract_settings.work_contract_type == WorkContractType.COMMON:
            cost_base = self.salary_gross
        else:
            cost_base = self.health_insurance_base
        return SalaryUtilities.calculate_author_rights_cost(
            Decimal("0"),
            self.rates.income_tax_deduction_20_50[1],
            cost_base,
            self.contract_settings.cost_fifty_sum,
            self.rates.cost_threshold,
        )

    @override
    def calculate_health_insurance_base(self) -> Decimal:
        """Calculates the health insurance base depending on contract type.

        Rules:
            - COMMON: No health insurance.
            - THE_SAME_COMPANY: Standard base applies.

        Returns:
            Decimal: Health insurance base amount.
        """
        match self.contract_settings.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal("0.0")
            case WorkContractType.THE_SAME_COMPANY:
                return super().calculate_health_insurance_base()
        return Decimal("0.0")

    @override
    def calculate_health_insurance(self) -> Decimal:
        return super().calculate_health_insurance()

    @override
    def calculate_tax_base(self) -> Decimal:
        return super().calculate_tax_base()

    @override
    def calculate_tax(self) -> Decimal:
        """Calculates income tax for the work contract.

        Rules:
            - Lump-sum contracts up to 200 PLN are taxed at 12%.
            - Otherwise, standard 12% tax applies to the calculated base.

        Returns:
            Decimal: Calculated tax value.
        """
        if (
            self.contract_settings.is_a_lump_sum
            and self.salary_gross <= Decimal("200")
            and self.contract_settings.work_contract_type
            != WorkContractType.THE_SAME_COMPANY
        ):
            return self.salary_gross * self.rates.income_tax[0]

        return self.tax_base * self.rates.income_tax[0]

    @override
    def calculate_ppk_tax(self) -> Decimal:
        """Calculates PPK-related tax for same-company work contracts.

        Returns:
            Decimal: PPK tax or 0.0 for common contracts.
        """
        if self.contract_settings.work_contract_type == WorkContractType.COMMON:
            return Decimal("0.0")
        return super().calculate_ppk_tax()

    @override
    def calculate_salary_deductions(self) -> Decimal:
        return super().calculate_salary_deductions()

    @override
    def calculate_employee_ppk_contribution(self) -> Decimal:
        """Calculates employee PPK contribution for same-company work contracts.

        Returns:
            Decimal: PPK contribution or 0.0 for common contracts.
        """
        if self.contract_settings.work_contract_type == WorkContractType.COMMON:
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
        return super().calculate_fp()

    @override
    def calculate_fgsp(self) -> Decimal:
        return super().calculate_fgsp()

    @override
    def calculate_employer_ppk_contribution(self) -> Decimal:
        """Calculates employer PPK contribution for same-company work contracts.

        Returns:
            Decimal: Employer PPK contribution or 0.0 for common contracts.
        """
        if self.contract_settings.work_contract_type == WorkContractType.COMMON:
            return Decimal("0.0")
        return super().calculate_employer_ppk_contribution()

    @override
    def calculate_total_employer_cost(self) -> Decimal:
        """Calculates total employer cost including all contributions.

        Returns:
            Decimal: Total employer cost value.
        """
        return super().calculate_total_employer_cost()
