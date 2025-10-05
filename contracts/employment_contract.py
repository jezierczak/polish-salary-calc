from decimal import Decimal
from typing import override
from rates.rates import Rates
from opions.employment_contract_options import EmploymentContractOptions
from salary.abstract_salary import AbstractSalary

class EmploymentContract(AbstractSalary[EmploymentContractOptions]):
    def __init__(self, rates: Rates, options: EmploymentContractOptions ) -> None:
        super().__init__(rates, options)

    @override
    def _calculate_salary_base(self) -> Decimal:
        return self.input_salary

    @override
    def _calculate_sick_pay(self) -> Decimal:
        return self.options.sick_pay

    @override
    def _calculate_salary_gross(self) -> Decimal:
        return self.salary_base+self.salary_sick_pay

    @override
    def _calculate_social_security_base(self) -> Decimal:
        return self.input_salary

    def sum_total_podst_ub_spol(self) -> Decimal:
        return self.options.social_security_base_sum + self.social_security_base

    @override
    def _calculate_pension_insurance(self) -> Decimal:

        if self.sum_total_podst_ub_spol() <= self.rates.social_insurance_cap:
            return self.social_security_base *self.rates.pension_insurance_rate
        elif self.sum_total_podst_ub_spol() - self.social_security_base > self.rates.social_insurance_cap:
            return Decimal('0.0')
        else:
            return (self.social_security_base - (self.sum_total_podst_ub_spol() - self.rates.social_insurance_cap))*self.rates.pension_insurance_rate

    @override
    def _calculate_disability_insurance(self) -> Decimal:
        if self.sum_total_podst_ub_spol() <= self.rates.social_insurance_cap:
            return self.social_security_base * self.rates.disability_insurance_rate
        elif self.sum_total_podst_ub_spol() - self.social_security_base > self.rates.social_insurance_cap:
            return Decimal('0.0')
        else:
            return (self.social_security_base - (
                        self.sum_total_podst_ub_spol() - self.rates.social_insurance_cap)) * self.rates.disability_insurance_rate

    @override
    def _calculate_sickness_insurance(self) -> Decimal:
        return self.social_security_base * self.rates.sickness_insurance_rate

    @override
    def _calculate_social_insurance_sum(self) -> Decimal:
        return self.pension_insurance + self.disability_insurance + self.sickness_insurance

    @override
    def _calculate_cost(self) -> Decimal:
        #if self.podst_podatek * (1 - self.options.cost_fifty_ratio) - self._calculate_koszt_norm() < 0:
        #    return self.koszt_fifty + self.podst_podatek * (1 - self.options.cost_fifty_ratio)
        #else:
        return self.author_rights_cost + self.regular_cost

    @override
    def _calculate_regular_cost(self) -> Decimal:
        if self.options.increased_costs:
            return self.rates.income_tax_deduction[1]
        else:
            return self.rates.income_tax_deduction[0]

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        if self.options.cost_fifty_ratio>0:
            cost_fifty = self.rates.income_tax_deduction_20_50[1] * self.health_insurance_base * self.options.cost_fifty_ratio
            cost_fifty_sum  = self.options.cost_fifty_sum +  cost_fifty
            print('log')
            print(cost_fifty_sum, self.health_insurance_base, self.options.cost_fifty_ratio)
            if cost_fifty_sum <= self.rates.cost_threshold:
                return cost_fifty
            elif cost_fifty_sum - cost_fifty <= self.rates.cost_threshold:
                return self.rates.cost_threshold - cost_fifty_sum -  cost_fifty
            else:
                return Decimal('0.0')

        else: return Decimal('0.0')

    @override
    def _calculate_health_insurance_base(self) -> Decimal:
        return self.salary_gross - self.social_insurance_sum

    @override
    def _calculate_health_insurance(self) -> Decimal:
        return self.health_insurance_base * self.rates.health_insurance_rate

    @override
    def _calculate_tax_base(self) -> Decimal:
        return self.salary_gross - self.social_insurance_sum - self.cost

    @override
    def _calculate_tax(self) -> Decimal:
        if self.options.under_26: return Decimal('0.0')
        suma_podst_podatek = self.options.tax_base_sum + self.tax_base
        if not self.options.active_business:
            if suma_podst_podatek <= self.rates.tax_threshold:
                out = self.tax_base * self.rates.income_tax[0] - self.rates.month_tax_free
            elif suma_podst_podatek-self.tax_base <= self.rates.tax_threshold:
                pod_1= (self.rates.tax_threshold - (suma_podst_podatek - self.tax_base)) * self.rates.income_tax[0] - self.rates.month_tax_free
                pod_2= (suma_podst_podatek - self.rates.tax_threshold) * self.rates.income_tax[1]
                out= pod_1+pod_2
            else:
                out= self.tax_base * self.rates.income_tax[1]
        else:
            if suma_podst_podatek <= self.rates.tax_threshold:
                out= self.tax_base * self.rates.income_tax[0]
            elif suma_podst_podatek-self.tax_base <=  self.rates.tax_threshold:
                pod_1= (self.rates.tax_threshold - self.tax_base) * self.rates.income_tax[0]
                pod_2= (suma_podst_podatek - self.rates.tax_threshold) * self.rates.income_tax[1]
                out=pod_1+pod_2
            else:
                out= self.tax_base * self.rates.income_tax[1]

        out += self.ppk_tax
        if out<=0: self.ppk_podatek = Decimal('0.0')
        return out if out > 0 else Decimal('0.0')

    #@override
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @override
    def _calculate_ppk_tax(self) -> Decimal:
        if self.options.under_26: return Decimal('0.0')
        return self.social_security_base * self.options.employer_ppk * self.rates.income_tax[0]

    @override
    def _calculate_tax_advance_payment(self) -> Decimal:
        return self.tax


    @override
    def _calculate_potracenia_wyplaty(self) -> Decimal:
        return Decimal('0')

    @override
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        return self.social_security_base * self.options.employee_ppk

    @override
    def _calculate_net_salary(self) -> Decimal:
        return self.salary_gross - (
                self.social_insurance_sum + self.tax_advance_payment + self.employee_ppk_contribution + self.health_insurance) #self.salary_deductions

    @override
    def _calculate_pension_contribution(self) -> Decimal:
        suma_podst_spol= self.options.tax_base_sum + self.tax_base

        if suma_podst_spol  <= self.rates.social_insurance_cap:
            return self.social_security_base * self.rates.employer_pension_contribution_rate

        elif suma_podst_spol - self.social_security_base > self.rates.social_insurance_cap:
            return Decimal('0')

        else:
            return self.social_security_base - (
                suma_podst_spol - self.rates.social_insurance_cap) * self.rates.employer_pension_contribution_rate

    @override
    def _calculate_disability_contribution(self)-> Decimal:
        suma_podst_spol = self.options.tax_base_sum + self.tax_base
        if suma_podst_spol <= self.rates.social_insurance_cap:
            return self.social_security_base * self.rates.employer_disability_contribution_rate
        elif suma_podst_spol - self.social_security_base > self.rates.social_insurance_cap:
            return Decimal('0')
        else:
            return self.social_security_base - (
                    suma_podst_spol - self.rates.social_insurance_cap) * self.rates.employer_disability_contribution_rate


    @override
    def _calculate_accident_insurance(self) -> Decimal:
        return self.social_security_base * self.rates.accident_insurance_rate


    @override
    def _calculate_fp(self) -> Decimal:
        if not self.options.fp_fgsp:
            return Decimal('0')
        else:
            if self.options.current_month_gross_sum + self.salary_gross >= self.rates.minimum_wage:
                return self.social_security_base * self.rates.fp_rate
            else:
                return Decimal('0')



    @override
    def _calculate_fgsp(self) -> Decimal:
        if not self.options.fp_fgsp:
            return Decimal('0')
        else:
            return self.social_security_base * self.rates.fgsp_rate

    @override
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        return self.social_security_base*self.options.employer_ppk

    @override
    def _calculate_total_employer_cost(self) -> Decimal:
        return self.salary_gross+self.employer_pension_contribution + self.employer_disability_contribution + self.accident_insurance+self.fp+self.fgsp+self.employer_ppk_contribution


