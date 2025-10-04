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


class Salary[T](ABC):
    def __init__(self, rates: Rates) -> None:
        self.rates = rates
        self.options: T

        self.salary_amount = Decimal('0')

        self.placa_podstawowa: Decimal = Decimal('0.0')
        self.placa_chorobowa: Decimal = Decimal('0.0')
        self.koszt_dzialalnosc: Decimal= Decimal('0.0')
        self.wynagrodzenie_brutto: Decimal= Decimal('0.0')
        self.podstawa_ub_spolecznych: Decimal= Decimal('0.0')
        self.ub_emeryt: Decimal= Decimal('0.0')
        self.ub_rent: Decimal= Decimal('0.0')
        self.ub_chor: Decimal= Decimal('0.0')
        self.ub_spol: Decimal= Decimal('0.0')
        self.koszt: Decimal= Decimal('0.0')
        self.koszt_norm: Decimal= Decimal('0.0')
        self.koszt_fifty: Decimal= Decimal('0.0')
        self.podst_zdrow: Decimal= Decimal('0.0')
        self.podst_podatek: Decimal= Decimal('0.0')
        self.podatek: Decimal= Decimal('0.0')
        self.ub_zdrowotne: Decimal= Decimal('0.0')
        self.ub_zdr_odl: Decimal= Decimal('0.0')
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
    def calculate_placa_podstawowa(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_placa_chorobowa(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_podstawa_ub_spolecznych(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_emeryt(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_rent(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_chor(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_spol(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_koszt(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_koszt_norm(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_koszt_fifty(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_podst_zdrow(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_podst_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_zdrowotne(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ub_zdr_odl(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ppk_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_zal_podatek(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_potraceniai_wyplaty(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ppk_pracownik(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_wynagrodzenie_netto(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_prac_ub_emeryt(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_prac_ub_rent(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_prac_ub_wyp(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_fp(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_fgsp(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_ppk_pracodawca(self) -> Decimal:
        pass

    @abstractmethod
    def calculate_brutto_brutto(self) -> Decimal:
        pass

    @property
    def suma_narzutow(self) -> Decimal:
        return self.brutto_brutto-self.wynagrodzenie_netto


    @property
    def brutto_ration(self) -> Decimal:
        return (self.wynagrodzenie_brutto / self.brutto_brutto)*100

    @property
    def netto_ratio(self)-> Decimal:
        return (self.wynagrodzenie_netto/ self.brutto_brutto)*100


    @property
    def suma_narzutow_ratio(self) -> Decimal:
        return (self.suma_narzutow/self.brutto_ration)*100


    @property
    def brutto_brutto_ratio(self) -> Decimal:
        return Decimal('100.00')

    # @abstractmethod
    # def rodzaj_koszt(self) -> int:
    #     pass

    def calculate(self, salary_amount: Decimal, salary_type: SalaryType) -> None:
        self.salary_amount = salary_amount
        if salary_type == SalaryType.Brutto:

            self._calculate_brutto()
            self.is_calculated = True
        else:

            self._calculate_netto()
            self.is_calculated = True


    def _calculate_brutto(self) -> None:
        self.placa_podstawowa = self.calculate_placa_podstawowa()
        self.placa_chorobowa = self.calculate_placa_chorobowa()
        self.podstawa_ub_spolecznych = self.calculate_podstawa_ub_spolecznych()
        self.ub_emeryt = self.calculate_ub_emeryt()
        self.ub_rent = self.calculate_ub_rent()
        self.ub_chor = self.calculate_ub_chor()
        self.ub_spol = self.calculate_ub_spol()
        self.podst_zdrow = self.calculate_podst_zdrow()
        self.koszt_norm = self.calculate_koszt_norm()
        self.koszt_fifty = self.calculate_koszt_fifty()
        self.koszt = self.calculate_koszt()
        self.podst_podatek = self.calculate_podst_podatek()
        self.podatek = self.calculate_podatek()
        self.ub_zdrowotne = self.calculate_ub_zdrowotne()
        self.ub_zdr_odl = self.calculate_ub_zdr_odl()
        self.ppk_podatek = self.calculate_ppk_podatek()
        self.zal_podatek = self.calculate_zal_podatek()
        self.ppk_pracownik = self.calculate_ppk_pracownik()
        self.wynagrodzenie_netto = self.calculate_wynagrodzenie_netto()
        self.prac_ub_emeryt = self.calculate_prac_ub_emeryt()
        self.prac_ub_rent = self.calculate_prac_ub_rent()
        self.prac_ub_wyp = self.calculate_prac_ub_wyp()
        self.fp = self.calculate_fp()
        self.fgsp = self.calculate_fgsp()
        self.ppk_pracodawca = self.calculate_ppk_pracodawca()
        self.brutto_brutto = self.calculate_brutto_brutto()



    def _calculate_netto(self) -> None:
        pass



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
    def Builder(cls) -> 'Builder':
        return cls.Builder()
    class Builder:
        def __init__(self):
            self.options = UmowaOPraceOptions()

        def is_podwyzszone_koszty(self, isPodwyzszoneKoszty: bool) -> Self:
            self.options.podwyzszoneKoszty = isPodwyzszoneKoszty
            return self
        def set_koszty_fifty_ratio(self, kosztyFiftyRatio: Decimal) -> Self:
            self.options.kosztyFiftyRatio = kosztyFiftyRatio
            return self
        def is_FPFGSP(self, isNotFPFGSP: bool) -> Self:
            self.options.FPFGSP = isNotFPFGSP
            return self
        def is_dzialanosc(self, isDzialanosc: bool) -> Self:
            self.options.dzialanosc = isDzialanosc
            return self
        def set_pChor(self, isPChor: Decimal) -> Self:
            self.options.pChor = isPChor
            return self
        def set_brutto_this_month(self, bruttoThisMonth: Decimal) -> Self:
            self.options.bruttoSumThisMonth = bruttoThisMonth
            return self
        def set_podst_ub_spol_sum(self, podstUbSpolSum: Decimal) -> Self:
            self.options.podstUbSpolSum = podstUbSpolSum
            return self
        def set_koszt_fifty_sum(self,kosztFiftySum: Decimal) -> Self:
            self.options.kosztFiftySum = kosztFiftySum
            return self
        def set_podst_podatek_sum(self, podstPodatekSum: Decimal) -> Self:
            self.options.podstPodatekSum = podstPodatekSum
            return self
        def set_ppk_pracownik(self, ppkPracownik: Decimal) -> Self:
            self.options.ppkPracownik = ppkPracownik
            return self
        def set_ppk_pracodawca(self, ppkPracodawca: Decimal) -> Self:
            self.options.ppkPracodawca = ppkPracodawca
            return self
        def build(self) -> 'UmowaOPraceOptions':
            return self.options


class UmowaOPrace[UmowaOPraceOptions](Salary):
    def __init__(self, rates: Rates):
        super().__init__(rates)
        self.options: UmowaOPraceOptions = UmowaOPraceOptions

    def set_options(self, options: UmowaOPraceOptions) -> None:
        self.options = options

    @override
    def calculate_placa_podstawowa(self) -> Decimal:
        return self.salary_amount

    @override
    def calculate_placa_chorobowa(self) -> Decimal:
        return self.options.pChor

    @override
    def calculate_podstawa_ub_spolecznych(self) -> Decimal:
        return self.salary_amount

    def sum_total_podst_ub_spol(self) -> Decimal:
        return self.options.podstUbSpolSum + self.podstawa_ub_spolecznych
    @override
    def calculate_ub_emeryt(self) -> Decimal:
        if self.sum_total_podst_ub_spol() <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych *self.rates.ub_emeryt
        elif self.sum_total_podst_ub_spol() - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0.0')
        else:
            return (self.podstawa_ub_spolecznych -(self.sum_total_podst_ub_spol() - self.rates.ograniczenie_zus))*self.rates.ub_emeryt

    @override
    def calculate_ub_rent(self) -> Decimal:
        if self.sum_total_podst_ub_spol() <= self.rates.ograniczenie_zus:
            return self.podstawa_ub_spolecznych * self.rates.ub_rent
        elif self.sum_total_podst_ub_spol() - self.podstawa_ub_spolecznych > self.rates.ograniczenie_zus:
            return Decimal('0.0')
        else:
            return (self.podstawa_ub_spolecznych - (
                        self.sum_total_podst_ub_spol() - self.rates.ograniczenie_zus)) * self.rates.ub_rent

    @override
    def calculate_ub_chor(self) -> Decimal:
        return self.podstawa_ub_spolecznych * self.rates.ub_chor

    @override
    def calculate_ub_spol(self) -> Decimal:
        return self.ub_emeryt + self.ub_rent + self.ub_chor

    @override
    def calculate_koszt(self) -> Decimal:
        pass

    @override
    def calculate_koszt_norm(self) -> Decimal:
        pass

    @override
    def calculate_koszt_fifty(self) -> Decimal:
        pass

    @override
    def calculate_podst_zdrow(self) -> Decimal:
        pass

    @override
    def calculate_podst_podatek(self) -> Decimal:
        pass

    @override
    def calculate_podatek(self) -> Decimal:
        pass

    @override
    def calculate_ub_zdrowotne(self) -> Decimal:
        pass

    @override
    def calculate_ub_zdr_odl(self) -> Decimal:
        pass

    @override
    def calculate_ppk_podatek(self) -> Decimal:
        pass

    @override
    def calculate_zal_podatek(self) -> Decimal:
        pass

    @override
    def calculate_potraceniai_wyplaty(self) -> Decimal:
        pass

    @override
    def calculate_ppk_pracownik(self) -> Decimal:
        pass

    @override
    def calculate_wynagrodzenie_netto(self) -> Decimal:
        pass

    @override
    def calculate_prac_ub_emeryt(self) -> Decimal:
        pass

    @override
    def calculate_prac_ub_rent(self)-> Decimal:
        pass


    @override
    def calculate_prac_ub_wyp(self) -> Decimal:
        pass


    @override
    def calculate_fp(self) -> Decimal:
        pass


    @override
    def calculate_fgsp(self) -> Decimal:
        pass


    @override
    def calculate_ppk_pracodawca(self) -> Decimal:
        pass


    @override
    def calculate_brutto_brutto(self) -> Decimal:
        pass


def main() -> None:
    umowa_o_prace_options = UmowaOPraceOptions().Builder().is_podwyzszone_koszty(True).set_koszty_fifty_ratio(Decimal('0.15')).is_dzialanosc(False).build()
    print(umowa_o_prace_options)
    rates_dict = {
        'description': 'Descritpion',
        'ub_emeryt': Decimal('9.00'),
        'ub_rent': Decimal('9.60')
    }
    rates = Rates().from_dict(rates_dict)
    rates.ograniczenie_zus = Decimal('0.33')
    rates.ub_chor = Decimal('0.12')

    wynagrodzenie = UmowaOPrace(rates)
    wynagrodzenie.set_options(umowa_o_prace_options)
    wynagrodzenie.calculate(Decimal('3000'), SalaryType.Brutto)
    print(wynagrodzenie.ub_emeryt)

if __name__ == '__main__':
    main()