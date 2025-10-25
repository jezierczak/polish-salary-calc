from decimal import Decimal
from typing import override
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.opions.self_employment_options import SelfEmploymentOptions,SelfEmploymentType
from polish_salary_calc.salary.abstract_salary import AbstractSalary
from polish_salary_calc.salary.salary_utilities import SalaryUtilities

class SelfEmployment(AbstractSalary[SelfEmploymentOptions]):
    def __init__(self, rates: Rates, options: SelfEmploymentOptions ) -> None:
        super().__init__(rates, options)

    @override
    def _calculate_salary_base(self) -> Decimal:
        return super()._calculate_salary_base()

    @override
    def _calculate_sick_pay(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_salary_gross(self) -> Decimal:
        return self.salary_base - self.options.costs

    @override
    def _calculate_social_security_base(self) -> Decimal:
        social_base = Decimal('0.0')
        match self.options.self_employment_type:
            case SelfEmploymentType.COMMON:
                if not self.options.other_minimum_contract:
                    social_base = self.rates.standard_social_insurance_base
            case SelfEmploymentType.PREFERRED:
                if not self.options.other_minimum_contract:
                    social_base = self.rates.reduced_social_insurance_base
            case SelfEmploymentType.STARTUP_RELIEF | SelfEmploymentType.UNREGISTERED_BUSINESS:
                    social_base = Decimal('0.0')
            #case SelfEmploymentType.SMALL_ZUS:
            case _:
                raise NotImplementedError('Unknown self employment type: ' + self.options.self_employment_type.name)

        if self.options.is_sick_pay and self.options.sick_pay_days > 0 and self.options.month_days > 0:
            social_base = social_base * (self.options.month_days - self.options.sick_pay_days) / self.options.month_days

        return social_base

    # @override
    # def _calculate_social_security_base_total(self) -> Decimal:
    #     return self.options.social_security_base_sum + self.social_security_base

    @override
    def _calculate_pension_insurance(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.pension_insurance_rate+self.rates.employer_pension_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )
        # if self.total_social_security_base_sum <= self.rates.social_insurance_cap:
        #     return self.social_security_base *self.rates.pension_insurance_rate
        # elif self.total_social_security_base_sum - self.social_security_base > self.rates.social_insurance_cap:
        #     return Decimal('0.0')
        # else:
        #     return (self.social_security_base - (self.total_social_security_base_sum - self.rates.social_insurance_cap))*self.rates.pension_insurance_rate

    @override
    def _calculate_disability_insurance(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.disability_insurance_rate+self.rates.employer_disability_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @override
    def _calculate_sickness_insurance(self) -> Decimal:
        if self.options.is_sick_pay:
            return super()._calculate_sickness_insurance()
        else:
            return Decimal('0.0')

    @override
    def _calculate_social_insurance_sum(self) -> Decimal:
        return self.pension_insurance + self.disability_insurance + self.sickness_insurance + self.accident_insurance+self.fp

    @override
    def _calculate_cost(self) -> Decimal:
        #if self.podst_podatek * (1 - self.options.cost_fifty_ratio) - self._calculate_koszt_norm() < 0:
        #    return self.koszt_fifty + self.podst_podatek * (1 - self.options.cost_fifty_ratio)
        #else:
        return super()._calculate_cost()

    @override
    def _calculate_regular_cost(self) -> Decimal:
        return self.options.costs

    @override
    def _calculate_author_rights_cost(self) -> Decimal:
        return Decimal('0.0')

    # @property
    # def cost_fifty_sum(self) -> Decimal:
    #     return self.options.cost_fifty_sum + self.author_rights_cost

    @override
    def _calculate_health_insurance_base(self) -> Decimal:
        min_base = self.rates.health_insurance_base

        return min_base
    #TODO podstawa zdrowotnego minimum to idzie ze stawek ale ona jest zależna od zysku a zysk jest liczony później i
    #TODO byćmoże nie da się tego tak obliczyć jak chcę

    @override
    def _calculate_health_insurance(self) -> Decimal:
        return super()._calculate_health_insurance()

    @override
    def _calculate_tax_base(self) -> Decimal:
        return self.salary_gross - self.social_insurance_sum

    # @property
    # def tax_base_sum(self)  ->Decimal:
    #     return self.options.tax_base_sum + self.tax_base

    @override
    def _calculate_tax(self) -> Decimal:
        out = SalaryUtilities.calculate_tax(
            self.rates.income_tax,
            self.tax_base,
            self.options.tax_base_sum,
            self.rates.tax_threshold
            )
        return out
        # out += self.ppk_tax
        # if out<=0: self.ppk_podatek = Decimal('0.0')
        # return out if out > 0 else Decimal('0.0')

    #@override
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @override
    def _calculate_ppk_tax(self) -> Decimal:
        return Decimal('0.0')

    # @override
    # def _calculate_tax_advance_payment(self) -> Decimal:
    #     return self.tax


    @override
    def _calculate_salary_deductions(self) -> Decimal:
        return super()._calculate_salary_deductions()

    @override
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_net_salary(self) -> Decimal:
        return super()._calculate_net_salary() - (self.employer_pension_contribution +
                                                  self.employer_disability_contribution +
                                                  self.accident_insurance+
                                                  self.fp+self.fgsp+
                                                  self.employer_ppk_contribution)

    @override
    def _calculate_pension_contribution(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_disability_contribution(self)-> Decimal:
        return Decimal('0.0')


    @override
    def _calculate_accident_insurance(self) -> Decimal:
        return super()._calculate_accident_insurance()


    @override
    def _calculate_fp(self) -> Decimal:
        if not self.options.is_fp:
            return Decimal('0')
        else:
            return super()._calculate_fp()



    @override
    def _calculate_fgsp(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        return Decimal('0.0')

    @override
    def _calculate_total_employer_cost(self) -> Decimal:
        return self.salary_gross

    @override
    def _calculate_gross(self) -> None:
        self.salary_base = self._calculate_salary_base().quantize(Decimal('0.01'))
        self.salary_sick_pay = self._calculate_sick_pay().quantize(Decimal('0.01'))
        self.salary_gross= self._calculate_salary_gross().quantize(Decimal('0.01'))
        self.social_security_base = self._calculate_social_security_base().quantize(Decimal('0.01'))
        self.social_security_base_total = self._calculate_social_security_base_total().quantize(Decimal('0.01'))
        self.pension_insurance = self._calculate_pension_insurance().quantize(Decimal('0.01'))
        self.disability_insurance = self._calculate_disability_insurance().quantize(Decimal('0.01'))
        self.sickness_insurance = self._calculate_sickness_insurance().quantize(Decimal('0.01'))

        self.health_insurance_base = self._calculate_health_insurance_base().quantize(Decimal('0.01'))
        self.regular_cost = self._calculate_regular_cost().quantize(Decimal('0.01'))
        self.author_rights_cost = self._calculate_author_rights_cost().quantize(Decimal('0.01'))
        self.cost = self._calculate_cost().quantize(Decimal('0.01'))
        self.cost_fifty_total = self._calculate_cost_fifty_total().quantize(Decimal('0.01'))
        self.tax_base = self._calculate_tax_base().quantize(Decimal('1'))
        self.tax_base_total = self._calculate_tax_base_total().quantize(Decimal('0.01'))
        self.ppk_tax = self._calculate_ppk_tax().quantize(Decimal('0.01'))
        self.tax = self._add_ppk_tax_and_check_if_is_positive(self._calculate_tax()).quantize(Decimal('0.01'))
        self.health_insurance = self._calculate_health_insurance().quantize(Decimal('0.01'))
        #self.ub_zdr_odl = self._calculate_ub_zdr_odl()
        self.salary_deductions = self._calculate_salary_deductions().quantize(Decimal('0.01'))
        self.tax_advance_payment = self._calculate_tax_advance_payment().quantize(Decimal('1'))
        self.employee_ppk_contribution = self._calculate_employee_ppk_contribution().quantize(Decimal('0.01'))
        self.employer_pension_contribution = self._calculate_pension_contribution().quantize(Decimal('0.01'))
        self.employer_disability_contribution = self._calculate_disability_contribution().quantize(Decimal('0.01'))
        self.accident_insurance = self._calculate_accident_insurance().quantize(Decimal('0.01'))
        self.social_insurance_sum = self._calculate_social_insurance_sum().quantize(Decimal('0.01'))
        self.fp = self._calculate_fp().quantize(Decimal('0.01'))
        self.fgsp = self._calculate_fgsp().quantize(Decimal('0.01'))
        self.employer_ppk_contribution = self._calculate_employer_ppk_contribution().quantize(Decimal('0.01'))

        self.net_salary = self._calculate_net_salary().quantize(Decimal('0.01'))
        self.total_employer_cost = self._calculate_total_employer_cost().quantize(Decimal('0.01'))


