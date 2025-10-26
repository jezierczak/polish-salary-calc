from polish_salary_calc.salary.abstract_salary_options import AbstractSalaryOptions
from decimal import Decimal, ROUND_UP
from abc import ABC, abstractmethod
from enum import Enum
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.salary.salary_utilities import SalaryUtilities


class SalaryType(Enum):
    GROSS = 1
    NET = 2

class AbstractSalary[T: AbstractSalaryOptions](ABC):
    def __init__(self, rates: Rates, options: T) -> None:
        self.rates: Rates = rates
        self.options: T  = options

        self.input_salary = Decimal('0')

        self.salary_base: Decimal = Decimal('0.0') #płaca podstawowa
        self.salary_sick_pay: Decimal = Decimal('0.0') #chorobowe
        #self.koszt_dzialalnosc: Decimal= Decimal('0.0')
        self.salary_gross: Decimal= Decimal('0.0')  #brutto
        self.social_security_base: Decimal= Decimal('0.0') #podst ub społ
        self.social_security_base_total: Decimal= Decimal('0.0')
        self.pension_insurance: Decimal= Decimal('0.0') #ub emeryt
        self.disability_insurance: Decimal= Decimal('0.0') #ub rent
        self.sickness_insurance: Decimal= Decimal('0.0') #chorobowe
        self.social_insurance_sum: Decimal= Decimal('0.0') #uma ub społ
        self.cost: Decimal= Decimal('0.0')
        self.cost_fifty_total: Decimal= Decimal('0.0')
        self.regular_cost: Decimal= Decimal('0.0')
        self.author_rights_cost: Decimal= Decimal('0.0') #koszt praw autorskich (50%)
        self.health_insurance_base: Decimal= Decimal('0.0') #podst zdrowotne
        self.tax_base: Decimal= Decimal('0.0') #podstawa podatku
        self.tax_base_total = Decimal('0.0')
        self.tax: Decimal= Decimal('0.0') # podatek
        self.health_insurance: Decimal= Decimal('0.0')
        #self.ub_zdr_odl: Decimal= Decimal('0.0')
        self.ppk_tax: Decimal= Decimal('0.0')
        self.tax_advance_payment: Decimal= Decimal('0.0') #zaliczka podatku
        self.salary_deductions: Decimal= Decimal('0.0') #potrącenia wypłaty
        self.employee_ppk_contribution: Decimal= Decimal('0.0')
        self.net_salary: Decimal= Decimal('0.0')
        self.employer_pension_contribution: Decimal= Decimal('0.0') #ub emeryt prac
        self.employer_disability_contribution: Decimal= Decimal('0.0') #ub rent prac
        self.accident_insurance: Decimal= Decimal('0.0') #ub wyp prac
        self.fp: Decimal= Decimal('0.0')
        self.fgsp: Decimal= Decimal('0.0')
        self.employer_ppk_contribution: Decimal= Decimal('0.0') #ppk pracodawca
        self.total_employer_cost: Decimal= Decimal('0.0') #brutto brutto

        self.is_calculated: bool = False

        # if self.options.accident_insurance_rate is None:
        #     self.options.accident_insurance_rate = self.rates.accident_insurance_rate

        if 0 < self.options.employer_ppk < Decimal('0.015') or 0 < self.options.employee_ppk < Decimal('0.02'):
            raise ValueError('Employer or employee PPK rate is too small')


    def update_rates(self, rates: Rates) -> None:
        self.rates = rates
        self.is_calculated = False

    def update_options(self, options: T) -> None:
        self.options = options
        if 0 < self.options.employer_ppk < Decimal('0.015') or 0 < self.options.employee_ppk < Decimal('0.02'):
            raise ValueError('Employer or employee PPK is too small')
        self.is_calculated = False

    @abstractmethod
    def _calculate_salary_base(self) -> Decimal:
        return self.input_salary

    @abstractmethod
    def _calculate_sick_pay(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_salary_gross(self) -> Decimal:
        return self.salary_base+self.salary_sick_pay

    @abstractmethod
    def _calculate_social_security_base(self) -> Decimal:
        return self.salary_base


    def _calculate_social_security_base_total(self) -> Decimal:
        return self.options.social_security_base_sum + self.social_security_base

    @abstractmethod
    def _calculate_pension_insurance(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.pension_insurance_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @abstractmethod
    def _calculate_disability_insurance(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.disability_insurance_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @abstractmethod
    def _calculate_sickness_insurance(self) -> Decimal:
        return self.social_security_base * self.rates.sickness_insurance_rate


    def _calculate_social_insurance_sum(self) -> Decimal:
        return self.pension_insurance + self.disability_insurance + self.sickness_insurance

    @abstractmethod
    def _calculate_cost(self) -> Decimal:
        return self.author_rights_cost + self.regular_cost

    @abstractmethod
    def _calculate_regular_cost(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_author_rights_cost(self) -> Decimal:
        pass

    def _calculate_cost_fifty_total(self) -> Decimal:
        return self.options.cost_fifty_sum + self.author_rights_cost

    @abstractmethod
    def _calculate_health_insurance_base(self) -> Decimal:
        return self.salary_gross - (self.pension_insurance + self.disability_insurance + self.sickness_insurance)

    @abstractmethod
    def _calculate_health_insurance(self) -> Decimal:
        return self.health_insurance_base * self.rates.health_insurance_rate

    @abstractmethod
    def _calculate_tax_base(self) -> Decimal:
        return self.salary_gross - self.social_insurance_sum - self.cost

    def _calculate_tax_base_total(self)  ->Decimal:
        return self.options.tax_base_sum + self.tax_base

    @abstractmethod
    def _calculate_tax(self) -> Decimal:
        pass

    def _add_ppk_tax_and_check_if_is_positive(self,input_tax: Decimal) -> Decimal:
        input_tax += self.ppk_tax
        if input_tax<=0: self.ppk_podatek = Decimal('0.0')
        return input_tax if input_tax > 0 else Decimal('0.0')

    #@abstractmethod
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @abstractmethod
    def _calculate_ppk_tax(self) -> Decimal:
        return self.social_security_base * self.options.employer_ppk * self.rates.income_tax[0]


    def _calculate_tax_advance_payment(self) -> Decimal:
        return self.tax

    @abstractmethod
    def _calculate_salary_deductions(self) -> Decimal:
        return self.options.salary_deductions

    @abstractmethod
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        # print(f'*******************************{self.social_security_base}')
        return self.social_security_base * self.options.employee_ppk

    @abstractmethod
    def _calculate_net_salary(self) -> Decimal:
        return self.salary_gross - (
                self.social_insurance_sum + self.tax_advance_payment + self.employee_ppk_contribution + self.health_insurance + self.salary_deductions)

    @abstractmethod
    def _calculate_pension_contribution(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.employer_pension_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @abstractmethod
    def _calculate_disability_contribution(self) -> Decimal:
        return SalaryUtilities.calculate_pension_or_disability_insurance(
            self.rates.employer_disability_contribution_rate,
            self.social_security_base,
            self.options.social_security_base_sum,
            self.rates.social_insurance_cap
        )

    @abstractmethod
    def _calculate_accident_insurance(self) -> Decimal:
        if self.options.accident_insurance_rate is None:
            return  self.social_security_base * self.rates.accident_insurance_rate
        return self.social_security_base * self.options.accident_insurance_rate

    @abstractmethod
    def _calculate_fp(self) -> Decimal:
        if self.options.current_month_gross_sum + self.salary_gross >= self.rates.minimum_wage:
            return self.social_security_base * self.rates.fp_rate
        else:
            return Decimal('0')

    @abstractmethod
    def _calculate_fgsp(self) -> Decimal:
        return self.social_security_base * self.rates.fgsp_rate

    @abstractmethod
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        return self.social_security_base*self.options.employer_ppk

    @abstractmethod
    def _calculate_total_employer_cost(self) -> Decimal:
        return self.salary_gross + self.employer_pension_contribution + self.employer_disability_contribution + self.accident_insurance + self.fp + self.fgsp + self.employer_ppk_contribution

    @property
    def total_markups(self) -> Decimal:
        return (self.total_employer_cost - self.net_salary).quantize(Decimal('0.01'))


    @property
    def brutto_ratio(self) -> Decimal:
        if self.total_employer_cost == 0: return Decimal('0.0')
        return ((self.salary_gross / self.total_employer_cost) * 100).quantize(Decimal('0.01'))

    @property
    def net_ratio(self)-> Decimal:
        if self.total_employer_cost == 0: return Decimal('0.0')
        return ((self.net_salary / self.total_employer_cost) * 100).quantize(Decimal('0.01'))


    @property
    def total_markups_ratio(self) -> Decimal:
        if self.total_employer_cost == 0: return Decimal('0.0')
        return ((self.total_markups / self.total_employer_cost) * 100).quantize(Decimal('0.01'))

    # @abstractmethod
    # def rodzaj_koszt(self) -> int:
    #     pass

    def calculate(self, salary_base: Decimal, salary_type: SalaryType = SalaryType.GROSS) -> None:
        if self.options is None:
            raise AttributeError('No options set to contract, use "update_options" before calculating')

        self.input_salary = salary_base
        if salary_type == SalaryType.GROSS:

            self._calculate_gross()
            self.is_calculated = True
        else:

            self._calculate_net()
            self.is_calculated = True


    def _calculate_gross(self) -> None:
        self.salary_base = self._calculate_salary_base().quantize(Decimal('0.01'))
        self.salary_sick_pay = self._calculate_sick_pay().quantize(Decimal('0.01'))
        self.salary_gross= self._calculate_salary_gross().quantize(Decimal('0.01'))
        self.social_security_base = self._calculate_social_security_base().quantize(Decimal('0.01'))
        self.social_security_base_total = self._calculate_social_security_base_total().quantize(Decimal('0.01'))
        self.pension_insurance = self._calculate_pension_insurance().quantize(Decimal('0.01'))
        self.disability_insurance = self._calculate_disability_insurance().quantize(Decimal('0.01'))
        self.sickness_insurance = self._calculate_sickness_insurance().quantize(Decimal('0.01'))
        self.social_insurance_sum = self._calculate_social_insurance_sum().quantize(Decimal('0.01'))
        self.health_insurance_base = self._calculate_health_insurance_base().quantize(Decimal('0.01'))
        self.regular_cost = self._calculate_regular_cost().quantize(Decimal('1'))
        self.author_rights_cost = self._calculate_author_rights_cost().quantize(Decimal('0.01'))
        self.cost = self._calculate_cost().quantize(Decimal('1'))
        self.cost_fifty_total = self._calculate_cost_fifty_total().quantize(Decimal('0.01'))
        self.tax_base = self._calculate_tax_base().quantize(Decimal('1'))
        self.tax_base_total = self._calculate_tax_base_total().quantize(Decimal('0.01'))
        self.ppk_tax = self._calculate_ppk_tax().quantize(Decimal('0.01'))
        self.tax = self._add_ppk_tax_and_check_if_is_positive(self._calculate_tax()).quantize(Decimal('0.01'))
        self.health_insurance = self._calculate_health_insurance().quantize(Decimal('0.01'))
        #self.ub_zdr_odl = self._calculate_ub_zdr_odl()
        self.salary_deductions = self._calculate_salary_deductions().quantize(Decimal('0.01'))
        self.tax_advance_payment = self._calculate_tax_advance_payment().quantize(Decimal('1'),rounding=ROUND_UP)
        self.employee_ppk_contribution = self._calculate_employee_ppk_contribution().quantize(Decimal('0.01'))
        self.employer_pension_contribution = self._calculate_pension_contribution().quantize(Decimal('0.01'))
        self.employer_disability_contribution = self._calculate_disability_contribution().quantize(Decimal('0.01'))
        self.accident_insurance = self._calculate_accident_insurance().quantize(Decimal('0.01'))
        self.fp = self._calculate_fp().quantize(Decimal('0.01'))
        self.fgsp = self._calculate_fgsp().quantize(Decimal('0.01'))
        self.employer_ppk_contribution = self._calculate_employer_ppk_contribution().quantize(Decimal('0.01'))

        self.net_salary = self._calculate_net_salary().quantize(Decimal('0.01'))
        self.total_employer_cost = self._calculate_total_employer_cost().quantize(Decimal('0.01'))


    def _calculate_net(self) -> None:
        wished_netto = self.input_salary #salary_base= brutto_estimate

        while self.net_salary.quantize(Decimal('0.01')) != wished_netto.quantize(Decimal('0.01')) :
            self.input_salary += wished_netto - self.net_salary
            self._calculate_gross()
            #print(self.salary_base, self.wynagrodzenie_netto)
        self.input_salary = wished_netto

    def __str__(self) -> str:
        return str(self.get_all_output())
    def get_all_output(self)-> dict:
        output = self.__dict__
        return {k:i for k,i in output.items() if k not in ["rates","options"]}

    def get_rates(self) -> Rates:
        return self.rates

    def get_options(self) -> dict:
        return self.__dict__['options']