from typing import TypedDict, Unpack
from decimal import Decimal
from dataclasses import dataclass

class RatesDict(TypedDict):
    description: str
    ub_emeryt: Decimal
    ub_rent: Decimal
    ub_chor: Decimal
    koszt_uzysk_przych: tuple[Decimal, Decimal]
    kw_wol_od_pod: Decimal
    koszt_uzysk_przych_20_50: tuple[Decimal, Decimal]
    pod_doch: tuple[Decimal, Decimal]

    ub_zdr: Decimal
    #ub_zdr_odl: Decimal
    prac_ub_emeryt: Decimal
    prac_ub_rent: Decimal
    prac_ub_wyp: Decimal
    fp: Decimal
    fgsp: Decimal
    placa_minimalna: Decimal
    prog_podatkowy: Decimal
    #prog_kosztowy: Decimal
    podstawa_stand_spol: Decimal
    podstawa_pref_spol: Decimal
    podstawa_zdrowotne: Decimal
    ograniczenie_zus: Decimal

@dataclass
class Rates:

    description: str = 'Default Rates (2025 year second half)'
    ub_emeryt: Decimal = Decimal('0.0976')
    ub_rent: Decimal = Decimal('0.015')
    ub_chor: Decimal = Decimal('0.0245')
    koszt_uzysk_przych = (Decimal('250'),Decimal('300'))
    koszt_uzysk_przych_20_50 = (Decimal('0.2'),Decimal('0.5'))
    pod_doch = (Decimal('0.12'),Decimal('0.32'))
    kw_wol_od_pod : Decimal = Decimal('30000')
    ub_zdr: Decimal = Decimal('0.09')
    #ub_zdr_odl: Decimal = None
    prac_ub_emeryt: Decimal = Decimal('0.0976')
    prac_ub_rent: Decimal = Decimal('0.0650')
    prac_ub_wyp: Decimal = Decimal('0.0167')
    fp: Decimal = Decimal('0.0245')
    fgsp: Decimal = Decimal('0.001')
    placa_minimalna: Decimal = Decimal('4666')
    prog_podatkowy: Decimal = Decimal('120000')
    #prog_kosztowy: Decimal = None
    podstawa_stand_spol: Decimal = Decimal('5203.80')
    podstawa_pref_spol: Decimal = Decimal('1399.80 ')
    podstawa_zdrowotne: Decimal = Decimal('3499.50')
    ograniczenie_zus: Decimal = Decimal('260190')

    @property
    def podatek_wolny(self) -> Decimal:
        return self.pod_doch[0] * self.kw_wol_od_pod
    @property
    def podatek_wony_mies(self) -> Decimal:
        return self.podatek_wolny/12
    @classmethod
    def from_dict(cls,data: Unpack[RatesDict]) -> "Rates":
        return cls(**data)

    def __getitem__(self, item: str) -> Decimal | str:
        return getattr(self, item)

    def __setitem__(self, key: str, value: Decimal | str) -> None:
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f'Attribute {key} not found.')

    def get_all(self) -> dict:
        return self.__dict__

def main() -> None:
    #rates_dict = {
    #                'description':'Descritpion',
    #                'ub_emeryt':Decimal('9.00'),
    #                'ub_rent':Decimal('9.60')
    #            }
    #rates = Rates().from_dict(rates_dict)
    #print(rates.ub_emeryt)
    #rates['pod_doch'] = Decimal('0.12')
    #print(rates['ub_rent'])
    #print(rates.pod_doch)

    rates = Rates()
    for n,rate in rates.get_all().items():
        print(f'{n:20.20} : {rate}')



if __name__ == "__main__":
    main()


