from decimal import Decimal
from typing import TypedDict
from dataclasses import dataclass
from typing import Self, Unpack, override
from abc import ABC, abstractmethod
from enum import Enum

from Rates import Rates


class SalaryType(Enum):
    Brutto = 1
    Netto = 2


class Salary(ABC):
    def __init__(self, rates: Rates) -> None:
        self.rates = rates

        self.salary_base = Decimal('0')

        self.placa_podstawowa: Decimal = Decimal('0.0')
        self.placa_chorobowa: Decimal = Decimal('0.0')
        #self.koszt_dzialalnosc: Decimal= Decimal('0.0')
        self.wynagrodzenie_brutto: Decimal= Decimal('0.0')
        self.podstawa_ub_spolecznych: Decimal= Decimal('0.0')
        self.ub_emeryt: Decimal= Decimal('0.0')
        self.ub_rent: Decimal= Decimal('0.0')
        self.ub_chor: Decimal= Decimal('0.0')
        self.ub_spol: Decimal= Decimal('0.0')
        self.koszt: Decimal= Decimal('0.0')
        #self.koszt_norm: Decimal= Decimal('0.0')
        #self.koszt_fifty: Decimal= Decimal('0.0')
        self.podst_zdrow: Decimal= Decimal('0.0')
        self.podst_podatek: Decimal= Decimal('0.0')
        self.podatek: Decimal= Decimal('0.0')
        self.ub_zdrowotne: Decimal= Decimal('0.0')
        #self.ub_zdr_odl: Decimal= Decimal('0.0')
        self.ppk_podatek: Decimal= Decimal('0.0')
        self.zal_podatek: Decimal= Decimal('0.0')
        self.potracenia_wyplaty: Decimal= Decimal('0.0')
        self.ppk_pracownik: Decimal= Decimal('0.0')
        self.wynagrodzenie_netto: Decimal= Decimal('0.0')
        self.prac_ub_emeryt: Decimal= Decimal('0.0')
        self.prac_ub_rent: Decimal= Decimal('0.0')
        self.prac_ub_wyp: Decimal= Decimal('0.0')
        self.fp: Decimal= Decimal('0.0')
        self.fgsp: Decimal= Decimal('0.0')
        self.ppk_pracodawca: Decimal= Decimal('0.0')
        self.brutto_brutto: Decimal= Decimal('0.0')

        self.is_calculated: bool = False

    @abstractmethod
    def _calculate_placa_podstawowa(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_placa_chorobowa(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_wynagrodzenie_brutto(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_podstawa_ub_spolecznych(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ub_emeryt(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ub_rent(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ub_chor(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ub_spol(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_koszt(self) -> Decimal:
        pass

    #@abstractmethod
    #def _calculate_koszt_norm(self) -> Decimal:
    #    pass

    #@abstractmethod
    #def _calculate_koszt_fifty(self) -> Decimal:
    #    pass

    @abstractmethod
    def _calculate_podst_zdrow(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_podst_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ub_zdrowotne(self) -> Decimal:
        pass

    #@abstractmethod
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @abstractmethod
    def _calculate_ppk_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_zal_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_potracenia_wyplaty(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ppk_pracownik(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_wynagrodzenie_netto(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_prac_ub_emeryt(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_prac_ub_rent(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_prac_ub_wyp(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_fp(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_fgsp(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_ppk_pracodawca(self) -> Decimal:
        pass

    @abstractmethod
    def _calculate_brutto_brutto(self) -> Decimal:
        pass

    @property
    def suma_narzutow(self) -> Decimal:
        return (self.brutto_brutto-self.wynagrodzenie_netto).quantize(Decimal('0.01'))


    @property
    def brutto_ration(self) -> Decimal:
        return ((self.wynagrodzenie_brutto / self.brutto_brutto)*100).quantize(Decimal('0.01'))

    @property
    def netto_ratio(self)-> Decimal:
        return ((self.wynagrodzenie_netto/ self.brutto_brutto)*100).quantize(Decimal('0.01'))


    @property
    def suma_narzutow_ratio(self) -> Decimal:
        return ((self.suma_narzutow/self.brutto_brutto)*100).quantize(Decimal('0.01'))


    @property
    def brutto_brutto_ratio(self) -> Decimal:
        return Decimal('100.00')

    # @abstractmethod
    # def rodzaj_koszt(self) -> int:
    #     pass

    def calculate(self, salary_base: Decimal, salary_type: SalaryType) -> None:
        self.salary_base = salary_base
        if salary_type == SalaryType.Brutto:

            self._calculate_brutto()
            self.is_calculated = True
        else:

            self._calculate_netto()
            self.is_calculated = True


    def _calculate_brutto(self) -> None:
        self.placa_podstawowa = self._calculate_placa_podstawowa().quantize(Decimal('0.01'))
        self.placa_chorobowa = self._calculate_placa_chorobowa().quantize(Decimal('0.01'))
        self.wynagrodzenie_brutto= self._calculate_wynagrodzenie_brutto().quantize(Decimal('0.01'))
        self.podstawa_ub_spolecznych = self._calculate_podstawa_ub_spolecznych().quantize(Decimal('0.01'))
        self.ub_emeryt = self._calculate_ub_emeryt().quantize(Decimal('0.01'))
        self.ub_rent = self._calculate_ub_rent().quantize(Decimal('0.01'))
        self.ub_chor = self._calculate_ub_chor().quantize(Decimal('0.01'))
        self.ub_spol = self._calculate_ub_spol().quantize(Decimal('0.01'))
        self.podst_zdrow = self._calculate_podst_zdrow().quantize(Decimal('0.01'))
        #self.koszt_norm = self._calculate_koszt_norm()
        #self.koszt_fifty = self._calculate_koszt_fifty()
        self.koszt = self._calculate_koszt().quantize(Decimal('0.01'))
        self.podst_podatek = self._calculate_podst_podatek().quantize(Decimal('0.01'))
        self.podatek = self._calculate_podatek().quantize(Decimal('0.01'))
        self.ub_zdrowotne = self._calculate_ub_zdrowotne().quantize(Decimal('0.01'))
        #self.ub_zdr_odl = self._calculate_ub_zdr_odl()
        self.ppk_podatek = self._calculate_ppk_podatek().quantize(Decimal('0.01'))
        self.zal_podatek = self._calculate_zal_podatek().quantize(Decimal('0.01'))
        self.ppk_pracownik = self._calculate_ppk_pracownik().quantize(Decimal('0.01'))
        self.wynagrodzenie_netto = self._calculate_wynagrodzenie_netto().quantize(Decimal('0.01'))
        self.prac_ub_emeryt = self._calculate_prac_ub_emeryt().quantize(Decimal('0.01'))
        self.prac_ub_rent = self._calculate_prac_ub_rent().quantize(Decimal('0.01'))
        self.prac_ub_wyp = self._calculate_prac_ub_wyp().quantize(Decimal('0.01'))
        self.fp = self._calculate_fp().quantize(Decimal('0.01'))
        self.fgsp = self._calculate_fgsp().quantize(Decimal('0.01'))
        self.ppk_pracodawca = self._calculate_ppk_pracodawca().quantize(Decimal('0.01'))
        self.brutto_brutto = self._calculate_brutto_brutto().quantize(Decimal('0.01'))


    def _calculate_netto(self) -> None:
        wished_netto = self.salary_base #salary_base= brutto_estimate


        while self.wynagrodzenie_netto.quantize(Decimal('0.1')) != wished_netto.quantize(Decimal('0.1')) :

            self.salary_base += wished_netto- self.wynagrodzenie_netto
            self._calculate_brutto()
            #print(self.salary_base, self.wynagrodzenie_netto)

        self.salary_base = wished_netto

    def __str__(self) -> str:

        return str(self.get_all_output())

    def get_all_output(self)-> dict:
        output = self.__dict__
        return {k:i for k,i in output.items() if k not in ["rates","options"]}

    def get_rates(self) -> Rates:
        return self.rates

    def get_options(self) -> dict:
        return self.__dict__['options']


class UmowaOPraceDict(TypedDict):
    podwyzszoneKoszty: bool
    kosztyFiftyRatio: Decimal
    FPFGSP: bool
    dzialanosc: bool
    pChor: Decimal
    bruttoSumThisMonth: Decimal
    podstUbSpolSum: Decimal
    kosztFiftySum: Decimal
    podstPodatekSum: Decimal
    ppkPracownik: Decimal
    ppkPracodawca: Decimal

@dataclass
class UmowaOPraceOptions:
    podwyzszoneKoszty: bool = False
    kosztyFiftyRatio: Decimal = Decimal('0.0')
    FPFGSP: bool = False
    dzialanosc: bool = False
    pChor: Decimal = Decimal('0.0')
    bruttoSumThisMonth: Decimal = Decimal('0.0')
    podstUbSpolSum: Decimal = Decimal('0.0')
    kosztFiftySum: Decimal = Decimal('0.0')
    podstPodatekSum: Decimal = Decimal('0.0')
    ppkPracownik: Decimal = Decimal('0.0')
    ppkPracodawca: Decimal = Decimal('0.0')

    @classmethod
    def from_dict(cls, data: Unpack[UmowaOPraceDict]) -> Self:
        return cls(**data)

    @classmethod
    def builder(cls) -> 'Builder':
        return cls.Builder()

    class Builder:
        def __init__(self):

            self._options = UmowaOPraceOptions()

        def is_podwyzszone_koszty(self, isPodwyzszoneKoszty: bool) -> Self:
            self._options.podwyzszoneKoszty = isPodwyzszoneKoszty
            return self
        def set_koszty_fifty_ratio(self, kosztyFiftyRatio: Decimal) -> Self:
            self._options.kosztyFiftyRatio = kosztyFiftyRatio
            return self
        def is_FPFGSP(self, isNotFPFGSP: bool) -> Self:
            self._options.FPFGSP = isNotFPFGSP
            return self
        def is_dzialanosc(self, isDzialanosc: bool) -> Self:
            self._options.dzialanosc = isDzialanosc
            return self
        def set_pChor(self, isPChor: Decimal) -> Self:
            self._options.pChor = isPChor
            return self
        def set_brutto_this_month(self, bruttoThisMonth: Decimal) -> Self:
            self._options.bruttoSumThisMonth = bruttoThisMonth
            return self
        def set_podst_ub_spol_sum(self, podstUbSpolSum: Decimal) -> Self:
            self._options.podstUbSpolSum = podstUbSpolSum
            return self
        def set_koszt_fifty_sum(self,kosztFiftySum: Decimal) -> Self:
            self._options.kosztFiftySum = kosztFiftySum
            return self
        def set_podst_podatek_sum(self, podstPodatekSum: Decimal) -> Self:
            self._options.podstPodatekSum = podstPodatekSum
            return self
        def set_ppk_pracownik(self, ppkPracownik: Decimal) -> Self:
            self._options.ppkPracownik = ppkPracownik
            return self
        def set_ppk_pracodawca(self, ppkPracodawca: Decimal) -> Self:
            self._options.ppkPracodawca = ppkPracodawca
            return self
        def build(self) -> 'UmowaOPraceOptions':
            return self._options


class UmowaOPrace(Salary):
    def __init__(self, rates: Rates):
        super().__init__(rates)
        self.options: UmowaOPraceOptions = UmowaOPraceOptions()

    def set_options(self, options: UmowaOPraceOptions) -> None:
        self.options = options

    @override
    def _calculate_placa_podstawowa(self) -> Decimal:
        return self.salary_base

    @override
    def _calculate_placa_chorobowa(self) -> Decimal:
        return self.options.pChor

    @override
    def _calculate_wynagrodzenie_brutto(self) -> Decimal:
        return self.placa_podstawowa+self.placa_chorobowa

    @override
    def _calculate_podstawa_ub_spolecznych(self) -> Decimal:
        return self.salary_base

    def sum_total_podst_ub_spol(self) -> Decimal:
        return self.options.podstUbSpolSum + self.podstawa_ub_spolecznych

    @override
    def _calculate_ub_emeryt(self) -> Decimal:

        if self.sum_total_podst_ub_spol() <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych *self.rates.ub_emeryt
        elif self.sum_total_podst_ub_spol() - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0.0')
        else:
            return (self.podstawa_ub_spolecznych -(self.sum_total_podst_ub_spol() - self.rates.ograniczenie_zus))*self.rates.ub_emeryt

    @override
    def _calculate_ub_rent(self) -> Decimal:
        if self.sum_total_podst_ub_spol() <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych * self.rates.ub_rent
        elif self.sum_total_podst_ub_spol() - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0.0')
        else:
            return (self.podstawa_ub_spolecznych - (
                        self.sum_total_podst_ub_spol() - self.rates.ograniczenie_zus)) * self.rates.ub_rent

    @override
    def _calculate_ub_chor(self) -> Decimal:
        return self.podstawa_ub_spolecznych * self.rates.ub_chor

    @override
    def _calculate_ub_spol(self) -> Decimal:
        return self.ub_emeryt + self.ub_rent + self.ub_chor

    @override
    def _calculate_koszt(self) -> Decimal:
        if self.options.podwyzszoneKoszty:
            return self.rates.koszt_uzysk_przych[1]
        else: return self.rates.koszt_uzysk_przych[0]

   # @override
   # def _calculate_koszt_norm(self) -> Decimal:
   #    pass

   # @override
   # def _calculate_koszt_fifty(self) -> Decimal:
   #     pass

    @override
    def _calculate_podst_zdrow(self) -> Decimal:
        return self.wynagrodzenie_brutto - self.ub_spol

    @override
    def _calculate_ub_zdrowotne(self) -> Decimal:
        return self.podst_zdrow * self.rates.ub_zdr

    @override
    def _calculate_podst_podatek(self) -> Decimal:
        return self.wynagrodzenie_brutto - self.ub_spol - self.koszt

    @override
    def _calculate_podatek(self) -> Decimal:
        out = Decimal('0.0')
        suma_podst_podatek = self.options.podstPodatekSum + self.podst_podatek
        if not self.options.dzialanosc:
            if suma_podst_podatek <= self.rates.prog_podatkowy:
                out = self.podst_podatek * self.rates.pod_doch[0] - self.rates.podatek_wony_mies
            elif suma_podst_podatek-self.podst_podatek <= self.rates.prog_podatkowy:
                pod_1=(self.rates.prog_podatkowy-(suma_podst_podatek-self.podst_podatek)) *self.rates.pod_doch[0]- self.rates.podatek_wony_mies
                pod_2=(suma_podst_podatek-self.rates.prog_podatkowy) * self.rates.pod_doch[1]
                out= pod_1+pod_2
            else:
                out=  self.podst_podatek * self.rates.pod_doch[1]
        else:
            if suma_podst_podatek <= self.rates.prog_podatkowy:
                out= self.podst_podatek * self.rates.pod_doch[0]

            elif suma_podst_podatek-self.podst_podatek <=  self.rates.prog_podatkowy:
                pod_1=(self.rates.prog_podatkowy-self.podst_podatek) * self.rates.pod_doch[0]
                pod_2=(suma_podst_podatek-self.rates.prog_podatkowy) * self.rates.pod_doch[1]

                out=pod_1+pod_2

            else:
                out= self.podst_podatek  * self.rates.pod_doch[1]


        return out if out > 0 else Decimal('0.0')



    #@override
    #def _calculate_ub_zdr_odl(self) -> Decimal:
    #    pass

    @override
    def _calculate_ppk_podatek(self) -> Decimal:
        return self.podstawa_ub_spolecznych * self.options.ppkPracodawca * self.rates.pod_doch[0]

    @override
    def _calculate_zal_podatek(self) -> Decimal:
        return self.podatek + self.ppk_podatek


    @override
    def _calculate_potracenia_wyplaty(self) -> Decimal:
        return Decimal('0')

    @override
    def _calculate_ppk_pracownik(self) -> Decimal:
        return self.podstawa_ub_spolecznych * self.options.ppkPracownik

    @override
    def _calculate_wynagrodzenie_netto(self) -> Decimal:
        return self.wynagrodzenie_brutto - (
                    self.ub_spol + self.zal_podatek + self.potracenia_wyplaty + self.ppk_pracownik+self.ub_zdrowotne)

    @override
    def _calculate_prac_ub_emeryt(self) -> Decimal:
        suma_podst_spol= self.options.podstPodatekSum + self.podst_podatek

        if suma_podst_spol  <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych * self.rates.prac_ub_emeryt

        elif suma_podst_spol - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0')

        else:
            return self.podstawa_ub_spolecznych - (
                suma_podst_spol - self.rates.ograniczenie_zus) * self.rates.prac_ub_emeryt

    @override
    def _calculate_prac_ub_rent(self)-> Decimal:
        suma_podst_spol = self.options.podstPodatekSum + self.podst_podatek
        if suma_podst_spol <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych * self.rates.prac_ub_rent
        elif suma_podst_spol - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0')
        else:
            return self.podstawa_ub_spolecznych - (
                    suma_podst_spol - self.rates.ograniczenie_zus) * self.rates.prac_ub_rent


    @override
    def _calculate_prac_ub_wyp(self) -> Decimal:
        return self.podstawa_ub_spolecznych * self.rates.prac_ub_wyp


    @override
    def _calculate_fp(self) -> Decimal:
        if not self.options.FPFGSP:
            return Decimal('0')
        else:
            if self.options.bruttoSumThisMonth + self.wynagrodzenie_brutto >= self.rates.placa_minimalna:
                return self.podstawa_ub_spolecznych * self.rates.fp
            else:
                return Decimal('0')



    @override
    def _calculate_fgsp(self) -> Decimal:
        if not self.options.FPFGSP:
            return Decimal('0')
        else:
            return self.podstawa_ub_spolecznych * self.rates.fgsp

    @override
    def _calculate_ppk_pracodawca(self) -> Decimal:
        return self.podstawa_ub_spolecznych*self.options.ppkPracodawca

    @override
    def _calculate_brutto_brutto(self) -> Decimal:
        return self.wynagrodzenie_brutto+self.prac_ub_emeryt + self.prac_ub_rent + self.prac_ub_wyp+self.fp+self.fgsp



def main() -> None:
    umowa_o_prace_options = (UmowaOPraceOptions().builder().
                             is_podwyzszone_koszty(True).
                             set_koszty_fifty_ratio(Decimal('0.15')).
                             is_dzialanosc(False).
                             is_FPFGSP(True).
                             build())

    rates = Rates()

    wynagrodzenie = UmowaOPrace(rates)
    wynagrodzenie.set_options(umowa_o_prace_options)
    wynagrodzenie.calculate(Decimal('4426.146'), SalaryType.Netto)

    print(wynagrodzenie.get_rates())
    print(wynagrodzenie.get_options())
    for k,i in wynagrodzenie.get_all_output().items():
        print(f'{k:20.20}: {i}')
    print(wynagrodzenie.netto_ratio)
    print(wynagrodzenie.suma_narzutow)
    print(wynagrodzenie.suma_narzutow_ratio)
if __name__ == '__main__':
    main()