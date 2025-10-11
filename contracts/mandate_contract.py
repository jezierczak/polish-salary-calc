from decimal import Decimal
from typing import override
from unittest import case

from rates.rates import Rates
from opions.mandate_contract_options import MandateContractOptions, MandateContractType
from salary.abstract_salary import AbstractSalary
from salary.salary_utilities import SalaryUtilities


class MandateContract(AbstractSalary[MandateContractOptions]):
    def __init__(self, rates: Rates, options: MandateContractOptions ) -> None:
        super().__init__(rates, options)

        if self.options.accident_insurance_rate is not None:
            self.rates.accident_insurance_rate = self.options.accident_insurance_rate

    @override
    def _calculate_salary_base(self) -> Decimal:
        return self.input_salary

    @override
    def _calculate_sick_pay(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_salary_gross(self) -> Decimal:
        return self.salary_base+self.salary_sick_pay

    @override
    def _calculate_social_security_base(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26:
                return Decimal('0.0')
            case MandateContractType.COMMON:
                return self.salary_base
            case MandateContractType.THE_SAME_COMPANY:
                return self.salary_base
            case MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case _: raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    @property
    def total_social_security_base_sum(self) -> Decimal:
        return self.options.social_security_base_sum + self.social_security_base

    @override
    def _calculate_pension_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return SalaryUtilities.calculate_pension_or_disability_insurance(
                    self.rates.pension_insurance_rate,
                    self.social_security_base,
                    self.options.social_security_base_sum,
                    self.rates.social_insurance_cap
                )
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    @override
    def _calculate_disability_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY:
                return Decimal('0.0')
            case MandateContractType.COMMON | MandateContractType.THE_SAME_COMPANY:
                return SalaryUtilities.calculate_pension_or_disability_insurance(
                    self.rates.disability_insurance_rate,
                    self.social_security_base,
                    self.options.social_security_base_sum,
                    self.rates.social_insurance_cap
                )
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)

    @override
    def _calculate_sickness_insurance(self) -> Decimal:
        match self.options.mandate_contract_type:
            case MandateContractType.UNDER_26 | MandateContractType.OTHER_COMPANY_MIN_SALARY | MandateContractType.COMMON:
                return Decimal('0.0')
            case  MandateContractType.THE_SAME_COMPANY:
                return self.social_security_base * self.rates.sickness_insurance_rate
            case _:
                raise NotImplementedError('Unknown mandate contract type: ' + self.options.mandate_contract_type.name)


    @override
    def _calculate_social_insurance_sum(self) -> Decimal:
        return self.pension_insurance + self.disability_insurance + self.sickness_insurance

    @override
    def _calculate_cost(self) -> Decimal:
        #if self.podst_podatek * (1 - self.options.cost_fifty_ratio) - self._calculate_koszt_norm() < 0:
        #    return self.koszt_fifty + self.podst_podatek * (1 - self.options.cost_fifty_ratio)
        #else:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26:
            return self.regular_cost
        else:
            return self.author_rights_cost + self.regular_cost

    @override
    def _calculate_regular_cost(self) -> Decimal:
        if self.options.is_a_lump_sum: return Decimal('0.0')

        if not self.options.is_fifty:
            return self.tax_base * self.rates.income_tax_deduction_20_50[0]
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

    @property
    def cost_fifty_sum(self) -> Decimal:
        return self.options.cost_fifty_sum + self.author_rights_cost

    @override
    def _calculate_health_insurance_base(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26:
            return Decimal('0.0')
        return self.salary_gross - self.social_insurance_sum

    @override
    def _calculate_health_insurance(self) -> Decimal:
        return self.health_insurance_base * self.rates.health_insurance_rate

    @override
    def _calculate_tax_base(self) -> Decimal:
        return self.salary_gross - self.social_insurance_sum - self.cost

    @property
    def tax_base_sum(self)  ->Decimal:
        return self.options.tax_base_sum + self.tax_base

    @override
    def _calculate_tax(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26: return Decimal('0.0')
        out = self.tax_base * self.rates.income_tax[0]
        out += self.ppk_tax
        if out<=0: self.ppk_podatek = Decimal('0.0')
        return out if out > 0 else Decimal('0.0')

    #@override
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @override
    def _calculate_ppk_tax(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
        return self.social_security_base * self.options.employer_ppk * self.rates.income_tax[0]

    @override
    def _calculate_tax_advance_payment(self) -> Decimal:
        return self.tax


    @override
    def _calculate_salary_deductions(self) -> Decimal:
        return Decimal('0')

    @override
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
        return self.social_security_base * self.options.employee_ppk

    @override
    def _calculate_net_salary(self) -> Decimal:
        return self.salary_gross - (
                self.social_insurance_sum + self.tax_advance_payment + self.employee_ppk_contribution + self.health_insurance) #self.salary_deductions

    @override
    def _calculate_pension_contribution(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.employer_pension_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @override
    def _calculate_disability_contribution(self)-> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.employer_disability_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )


    @override
    def _calculate_accident_insurance(self) -> Decimal:
        return self.social_security_base * self.rates.accident_insurance_rate


    @override
    def _calculate_fp(self) -> Decimal:
        if not self.options.fp:
            return Decimal('0')
        else:
            if self.options.current_month_gross_sum + self.salary_gross >= self.rates.minimum_wage:
                return self.social_security_base * self.rates.fp_rate
            else:
                return Decimal('0')



    @override
    def _calculate_fgsp(self) -> Decimal:
        if not self.options.fgsp:
            return Decimal('0')
        else:
            return self.social_security_base * self.rates.fgsp_rate

    @override
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        if self.options.mandate_contract_type == MandateContractType.UNDER_26 or MandateContractType.OTHER_COMPANY_MIN_SALARY:
            return Decimal('0.0')
        return self.social_security_base*self.options.employer_ppk

    @override
    def _calculate_total_employer_cost(self) -> Decimal:
        return self.salary_gross+self.employer_pension_contribution + self.employer_disability_contribution + self.accident_insurance+self.fp+self.fgsp+self.employer_ppk_contribution


