from typing import TypedDict, Unpack
from decimal import Decimal
from dataclasses import dataclass

class RatesDict(TypedDict):
    description: str
    pension_insurance_rate: Decimal
    disability_insurance_rate: Decimal
    sickness_insurance_rate: Decimal
    income_tax_deduction: tuple[Decimal, Decimal]
    tax_free_amount: Decimal
    income_tax_deduction_20_50: tuple[Decimal, Decimal]
    income_tax: tuple[Decimal, Decimal]
    health_insurance_rate: Decimal
    #ub_zdr_odl: Decimal
    employer_pension_contribution_rate: Decimal
    employer_disability_contribution_rate: Decimal
    accident_insurance_rate: Decimal
    fp_rate: Decimal
    fgsp_rate: Decimal
    minimum_wage: Decimal
    tax_threshold: Decimal #próg podatkowy
    cost_threshold: Decimal
    standard_social_insurance_base: Decimal
    reduced_social_insurance_base: Decimal
    health_insurance_base: Decimal
    social_insurance_cap: Decimal

@dataclass
class Rates:

    description: str = 'Default Rates (2025 year second half)'
    pension_insurance_rate: Decimal = Decimal('0.0976')
    disability_insurance_rate: Decimal = Decimal('0.015')
    sickness_insurance_rate: Decimal = Decimal('0.0245')
    income_tax_deduction = (Decimal('250'), Decimal('300'))
    income_tax_deduction_20_50 = (Decimal('0.2'), Decimal('0.5'))
    income_tax = (Decimal('0.12'), Decimal('0.32'))
    tax_free_amount : Decimal = Decimal('30000')
    health_insurance_rate: Decimal = Decimal('0.09')
    #ub_zdr_odl: Decimal = None
    employer_pension_contribution_rate: Decimal = Decimal('0.0976')
    employer_disability_contribution_rate: Decimal = Decimal('0.0650')
    accident_insurance_rate: Decimal = Decimal('0.0167')
    fp_rate: Decimal = Decimal('0.0245')
    fgsp_rate: Decimal = Decimal('0.001')
    minimum_wage: Decimal = Decimal('4666')
    tax_threshold: Decimal = Decimal('120000')
    cost_threshold: Decimal = Decimal('120000')
    standard_social_insurance_base: Decimal = Decimal('5203.80')
    reduced_social_insurance_base: Decimal = Decimal('1399.80 ')
    health_insurance_base: Decimal = Decimal('3499.50')
    social_insurance_cap: Decimal = Decimal('260190')

    @property
    def tax_free(self) -> Decimal:
        return self.income_tax[0] * self.tax_free_amount
    @property
    def month_tax_free(self) -> Decimal:
        return self.tax_free/12
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


