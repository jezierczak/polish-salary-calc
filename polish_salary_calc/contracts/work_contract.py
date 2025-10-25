from decimal import Decimal
from functools import cmp_to_key
from typing import override
from polish_salary_calc.opions.work_contract_options import WorkContractOptions, WorkContractType
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.abstract_salary import AbstractSalary
from polish_salary_calc.salary.salary_utilities import SalaryUtilities

class WorkContract(AbstractSalary[WorkContractOptions]):
    def __init__(self, rates: Rates, options: WorkContractOptions ) -> None:
        super().__init__(rates, options)

    @override
    def _calculate_salary_base(self) -> Decimal:
        return super()._calculate_salary_base()

    @override
    def _calculate_sick_pay(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_salary_gross(self) -> Decimal:
        return super()._calculate_salary_gross()

    @override
    def _calculate_social_security_base(self) -> Decimal:
        match self.options.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal('0.0')
            case WorkContractType.THE_SAME_COMPANY:
                return super()._calculate_social_security_base()

    # @override
    # def _calculate_social_security_base_total(self) -> Decimal:
    #     return self.options.social_security_base_sum + self.social_security_base

    @override
    def _calculate_pension_insurance(self) -> Decimal:
        match self.options.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal('0.0')
            case WorkContractType.THE_SAME_COMPANY:
                return super()._calculate_pension_insurance()

    @override
    def _calculate_disability_insurance(self) -> Decimal:
        match self.options.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal('0.0')
            case WorkContractType.THE_SAME_COMPANY:
                return super()._calculate_disability_insurance()

    @override
    def _calculate_sickness_insurance(self) -> Decimal:
        match self.options.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal('0.0')
            case WorkContractType.THE_SAME_COMPANY:
                return super()._calculate_sickness_insurance()

    # @override
    # def _calculate_social_insurance_sum(self) -> Decimal:
    #     return self.pension_insurance + self.disability_insurance + self.sickness_insurance

    @override
    def _calculate_cost(self) -> Decimal:
        return super()._calculate_cost()

    @override
    def _calculate_regular_cost(self) -> Decimal:
        if self.options.is_a_lump_sum and self.salary_gross <= Decimal('200'): return Decimal('0.0')

        if not self.options.is_fifty:
            if self.options.work_contract_type == WorkContractType.THE_SAME_COMPANY:
                return self.health_insurance_base * self.rates.income_tax_deduction_20_50[0]
            else: return self.salary_gross * self.rates.income_tax_deduction_20_50[0]
        else:
            return Decimal('0.0')

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        if not self.options.is_fifty: return Decimal('0.0')
        if self.options.is_a_lump_sum and self.salary_gross<=Decimal('200'): return Decimal('0.0')

        if self.options.work_contract_type == WorkContractType.COMMON:
            cost_base = self.salary_gross
        else:
            cost_base = self.health_insurance_base
        return SalaryUtilities.calculate_author_rights_cost(
                Decimal('0'),
                self.rates.income_tax_deduction_20_50[1],
                cost_base,#self.health_insurance_base if self.options.work_contract_type == WorkContractType.COMMON else self.salary_gross,
                self.options.cost_fifty_sum,
                self.rates.cost_threshold
                )

    @override
    def _calculate_health_insurance_base(self) -> Decimal:
        match self.options.work_contract_type:
            case WorkContractType.COMMON:
                return Decimal('0.0')
            case WorkContractType.THE_SAME_COMPANY:
                return super()._calculate_health_insurance_base()

    @override
    def _calculate_health_insurance(self) -> Decimal:
        return super()._calculate_health_insurance()

    @override
    def _calculate_tax_base(self) -> Decimal:
        return super()._calculate_tax_base()

    # @property
    # def tax_base_sum(self)  ->Decimal:
    #     return self.options.tax_base_sum + self.tax_base

    @override
    def _calculate_tax(self) -> Decimal:
        if (self.options.is_a_lump_sum
                and self.salary_gross <= Decimal('200')
                and self.options.work_contract_type != WorkContractType.THE_SAME_COMPANY):
            return self.salary_gross * self.rates.income_tax[0]

        return self.tax_base * self.rates.income_tax[0]

    @override
    def _calculate_ppk_tax(self) -> Decimal:
        if self.options.work_contract_type == WorkContractType.COMMON: return Decimal('0.0')
        return super()._calculate_ppk_tax()

    @override
    def _calculate_salary_deductions(self) -> Decimal:
        return super()._calculate_salary_deductions()

    @override
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        if self.options.work_contract_type == WorkContractType.COMMON: return Decimal('0.0')

        return super()._calculate_employee_ppk_contribution()

    @override
    def _calculate_net_salary(self) -> Decimal:
        return super()._calculate_net_salary()

    @override
    def _calculate_pension_contribution(self) -> Decimal:
        return super()._calculate_pension_contribution()

    @override
    def _calculate_disability_contribution(self)-> Decimal:
        return super()._calculate_disability_contribution()


    @override
    def _calculate_accident_insurance(self) -> Decimal:
        return super()._calculate_accident_insurance()


    @override
    def _calculate_fp(self) -> Decimal:
            return super()._calculate_fp()



    @override
    def _calculate_fgsp(self) -> Decimal:
            return super()._calculate_fgsp()

    @override
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        if self.options.work_contract_type == WorkContractType.COMMON: return Decimal('0.0')

        return super()._calculate_employer_ppk_contribution()

    @override
    def _calculate_total_employer_cost(self) -> Decimal:
        return super()._calculate_total_employer_cost()

