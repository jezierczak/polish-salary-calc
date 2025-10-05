from decimal import Decimal
from abc import ABC, abstractmethod
from enum import Enum
from rates.rates import Rates

class SalaryType(Enum):
    GROSS = 1
    NET = 2

class AbstractSalary[T](ABC):
    def __init__(self, rates: Rates, options: T) -> None:
        self.rates: Rates = rates
        self.options: T  = options

        self.input_salary = Decimal('0')

        self.salary_base: Decimal = Decimal('0.0') #płaca podstawowa
        self.salary_sick_pay: Decimal = Decimal('0.0') #chorobowe
        #self.koszt_dzialalnosc: Decimal= Decimal('0.0')
        self.salary_gross: Decimal= Decimal('0.0')  #brutto
        self.social_security_base: Decimal= Decimal('0.0') #podst ub społ
        self.pension_insurance: Decimal= Decimal('0.0') #ub emeryt
        self.disability_insurance: Decimal= Decimal('0.0') #ub rent
        self.sickness_insurance: Decimal= Decimal('0.0') #chorobowe
        self.social_insurance_sum: Decimal= Decimal('0.0') #uma ub społ
        self.cost: Decimal= Decimal('0.0')
        self.regular_cost: Decimal= Decimal('0.0')
        self.author_rights_cost: Decimal= Decimal('0.0') #koszt praw autorskich (50%)
        self.health_insurance_base: Decimal= Decimal('0.0') #podst zdrowotne
        self.tax_base: Decimal= Decimal('0.0') #podstawa podatku
        self.tax: Decimal= Decimal('0.0') # podatek
        self.health_insurance: Decimal= Decimal('0.0')
        #self.ub_zdr_odl: Decimal= Decimal('0.0')
        self.ppk_tax: Decimal= Decimal('0.0')
        self.tax_advance_payment: Decimal= Decimal('0.0') #zaliczka podatku
        #self.salary_deductions: Decimal= Decimal('0.0') #potrącenia wypłaty
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

    def update_rates(self, rates: Rates) -> None:
        self.rates = rates

    def update_options(self, options: T) -> None:
        self.options = options

    @abstractmethod
    def _calculate_salary_base(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_sick_pay(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_salary_gross(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_social_security_base(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_pension_insurance(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_disability_insurance(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_sickness_insurance(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_social_insurance_sum(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_cost(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_regular_cost(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_author_rights_cost(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_health_insurance_base(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_tax_base(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_tax(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_health_insurance(self) -> Decimal:
        pass

    #@abstractmethod
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @abstractmethod
    def _calculate_ppk_tax(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_tax_advance_payment(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_potracenia_wyplaty(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_employee_ppk_contribution(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_net_salary(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_pension_contribution(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_disability_contribution(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_accident_insurance(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_fp(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_fgsp(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_employer_ppk_contribution(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_total_employer_cost(self) -> Decimal:
        pass

    @property
    def total_markups(self) -> Decimal:
        return (self.total_employer_cost - self.net_salary).quantize(Decimal('0.01'))


    @property
    def brutto_ration(self) -> Decimal:
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


    @property
    def brutto_brutto_ratio(self) -> Decimal:
        return Decimal('100.00')

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
        self.pension_insurance = self._calculate_pension_insurance().quantize(Decimal('0.01'))
        self.disability_insurance = self._calculate_disability_insurance().quantize(Decimal('0.01'))
        self.sickness_insurance = self._calculate_sickness_insurance().quantize(Decimal('0.01'))
        self.social_insurance_sum = self._calculate_social_insurance_sum().quantize(Decimal('0.01'))
        self.health_insurance_base = self._calculate_health_insurance_base().quantize(Decimal('0.01'))
        self.regular_cost = self._calculate_regular_cost().quantize(Decimal('0.01'))
        self.author_rights_cost = self._calculate_author_rights_cost().quantize(Decimal('0.01'))
        self.cost = self._calculate_cost().quantize(Decimal('0.01'))
        self.tax_base = self._calculate_tax_base().quantize(Decimal('0.01'))
        self.ppk_tax = self._calculate_ppk_tax().quantize(Decimal('0.01'))
        self.tax = self._calculate_tax().quantize(Decimal('0.01'))
        self.health_insurance = self._calculate_health_insurance().quantize(Decimal('0.01'))
        #self.ub_zdr_odl = self._calculate_ub_zdr_odl()

        self.tax_advance_payment = self._calculate_tax_advance_payment().quantize(Decimal('1'))
        self.employee_ppk_contribution = self._calculate_employee_ppk_contribution().quantize(Decimal('0.01'))
        self.net_salary = self._calculate_net_salary().quantize(Decimal('0.01'))
        self.employer_pension_contribution = self._calculate_pension_contribution().quantize(Decimal('0.01'))
        self.employer_disability_contribution = self._calculate_disability_contribution().quantize(Decimal('0.01'))
        self.accident_insurance = self._calculate_accident_insurance().quantize(Decimal('0.01'))
        self.fp = self._calculate_fp().quantize(Decimal('0.01'))
        self.fgsp = self._calculate_fgsp().quantize(Decimal('0.01'))
        self.employer_ppk_contribution = self._calculate_employer_ppk_contribution().quantize(Decimal('0.01'))
        self.total_employer_cost = self._calculate_total_employer_cost().quantize(Decimal('0.01'))


    def _calculate_net(self) -> None:
        wished_netto = self.input_salary #salary_base= brutto_estimate

        while self.net_salary.quantize(Decimal('0.1')) != wished_netto.quantize(Decimal('0.1')) :
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