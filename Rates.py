from typing import TypedDict, Unpack
from decimal import Decimal
from dataclasses import dataclass

class RatesDict(TypedDict):
    description: str
    ub_emeryt: Decimal
    ub_rent: Decimal
    ub_chor: Decimal
    koszt_uzysk_przych: Decimal
    koszt_uzysk_przych_20_50: Decimal
    pod_doch: Decimal
    kw_wol_od_pod: Decimal
    kw_wol_od: Decimal
    ub_zdr: Decimal
    ub_zdr_odl: Decimal
    prac_ub_emeryt: Decimal
    prac_ub_rent: Decimal
    prac_ub_wyp: Decimal
    fp: Decimal
    fgsp: Decimal
    placa_minimalna: Decimal
    prog_podatkowy: Decimal
    prog_kosztowy: Decimal
    podstawa_stand_spol: Decimal
    podstawa_pref_spol: Decimal
    podstawa_zdrowotne: Decimal
    ograniczenie_zus: Decimal

@dataclass
class Rates:

    description: str = None
    ub_emeryt: Decimal = None
    ub_rent: Decimal = None
    ub_chor: Decimal = None
    koszt_uzysk_przych: Decimal = None
    koszt_uzysk_przych_20_50: Decimal = None
    pod_doch: Decimal = None
    kw_wol_od_pod : Decimal = None
    kw_wol_od: Decimal = None
    ub_zdr: Decimal = None
    ub_zdr_odl: Decimal = None
    prac_ub_emeryt: Decimal = None
    prac_ub_rent: Decimal = None
    prac_ub_wyp: Decimal = None
    fp: Decimal = None
    fgsp: Decimal = None
    placa_minimalna: Decimal = None
    prog_podatkowy: Decimal = None
    prog_kosztowy: Decimal = None
    podstawa_stand_spol: Decimal = None
    podstawa_pref_spol: Decimal = None
    podstawa_zdrowotne: Decimal = None
    ograniczenie_zus: Decimal = None

    @property
    def podatek_wolny(self) -> Decimal:
        return self.pod_doch * self.kw_wol_od_pod
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

def main() -> None:
    rates_dict = {
                    'description':'Descritpion',
                    'ub_emeryt':Decimal('9.00'),
                    'ub_rent':Decimal('9.60')
                }
    rates = Rates().from_dict(rates_dict)
    print(rates.ub_emeryt)
    rates['pod_doch'] = Decimal('0.12')
    print(rates['ub_rent'])
    print(rates.pod_doch)



if __name__ == "__main__":
    main()


