from decimal import Decimal
from typing import override

from rates.rates import Rates
from opions.mandate_contract_options import MandateContractOptions, MandateContractType
from salary.abstract_salary import AbstractSalary
from salary.salary_utilities import SalaryUtilities


class MandateContract(AbstractSalary[MandateContractOptions]):
    def __init__(self, rates: Rates, options: MandateContractOptions ) -> None:
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
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super()._calculate_social_security_base()
            case _: raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    # @override
    # def _calculate_social_security_base_total(self) -> Decimal:
    #     return self.options.social_security_base_sum + self.social_security_base

    @override
    def _calculate_pension_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super()._calculate_pension_insurance()
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    @override
    def _calculate_disability_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return super()._calculate_disability_insurance()
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    @override
    def _calculate_sickness_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY | MandateContractType.COMMON:
                return Decimal('0.0')
            case  MandateContractType.THE_SAME_COMPANY:
                return super()._calculate_sickness_insurance()
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)


    # @override
    # def _calculate_social_insurance_sum(self) -> Decimal:
    #     return self.pension_insurance + self.disability_insurance + self.sickness_insurance

    @override
    def _calculate_cost(self) -> Decimal:
        #if self.podst_podatek * (1 - self.options.cost_fifty_ratio) - self._calculate_koszt_norm() < 0:
        #    return self.koszt_fifty + self.podst_podatek * (1 - self.options.cost_fifty_ratio)
        #else:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26:
            return self.regular_cost
        else:
            return super()._calculate_cost()

    @override
    def _calculate_regular_cost(self) -> Decimal:
        if self.options.is_a_lump_sum: return Decimal('0.0')

        if not self.options.is_fifty:
            return self.health_insurance_base * self.rates.income_tax_deduction_20_50[0]
        else:
            return Decimal('0.0')

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        if not self.options.is_fifty: return Decimal('0.0')
        return SalaryUtilities.calculate_author_rights_cost(
                self.rates.income_tax_deduction_20_50[1],
                Decimal('1.0'),
                self.health_insurance_base,
                self.options.cost_fifty_sum,
                self.rates.cost_threshold
                )

    # @property
    # def cost_fifty_sum(self) -> Decimal:
    #     return self.options.cost_fifty_sum + self.author_rights_cost

    @override
    def _calculate_health_insurance_base(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26:
            return Decimal('0.0')
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
        if self.options.mandate_contract_type == MandateContractType.UNDER_26: return Decimal('0.0')
        out = self.tax_base * self.rates.income_tax[0]

        return out

    #@override
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @override
    def _calculate_ppk_tax(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
        return super()._calculate_ppk_tax()

    # @override
    # def _calculate_tax_advance_payment(self) -> Decimal:
    #     return self.tax


    @override
    def _calculate_salary_deductions(self) -> Decimal:
        return super()._calculate_salary_deductions()

    @override
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
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
        if not self.options.fp:
            return Decimal('0')
        else:
            return super()._calculate_fp()



    @override
    def _calculate_fgsp(self) -> Decimal:
        if not self.options.fgsp:
            return Decimal('0')
        else:
            return super()._calculate_fgsp()

    @override
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
        return super()._calculate_employer_ppk_contribution()

    @override
    def _calculate_total_employer_cost(self) -> Decimal:
        return super()._calculate_total_employer_cost()
