# Polish Salary Calculator

A Python library for calculating salaries in Poland across different contract types, including all mandatory contributions, taxes, cost deductions, and available configuration options. The library supports precise calculations using `Decimal` for all monetary values.

## Supported Contract Types
- Employment Contract (Umowa o pracę)
- Mandate Contract (Umowa zlecenie)
- Work Contract (Umowa o dzieło)
- Self-Employment (Samozatrudnienie) with multiple taxation models
- Yearly summaries and comparative analyses

## Installation

```bash
pip install polish-salary-calc
```

## Key Concepts

1. **Rates**
   The `Rates` object loads current legal contribution and tax rates (default covers Feb 2025 – Jan 2026).  
   You may override values manually:
   ```python
   rates['pension_insurance_rate'] = Decimal("0.0976")
   ```

2. **Contract Settings**
   Each contract type uses a configuration object built via a fluent builder:
   ```python
   EmploymentContractSettings().SettingsBuilder().is_increased_costs(True).build()
   ```

3. **Salary Calculation**
   Use:
   ```python
   contract.calculate(salary_value, SalaryType.GROSS or SalaryType.NET)
   ```

## Example Usage

```python
from decimal import Decimal
from polish_salary_calc.rates.rates import Rates
from polish_salary_calc.contract_settings.employment_contract_settings import EmploymentContractSettings
from polish_salary_calc.contract_settings.mandate_contract_settings import MandateContractSettings, MandateContractType
from polish_salary_calc.contract_settings.work_contract_settings import WorkContractSettings, WorkContractType
from polish_salary_calc.contract_settings.self_employment_settings import (
    SelfEmploymentSettings, SelfEmploymentType, TaxType, HealthBase
)
from polish_salary_calc.contracts.employment_contract import EmploymentContract
from polish_salary_calc.contracts.mandate_contract import MandateContract
from polish_salary_calc.contracts.work_contract import WorkContract
from polish_salary_calc.contracts.self_employment import SelfEmployment
from polish_salary_calc.contracts.base_contract import SalaryType
from polish_salary_calc.summary.contract_summary import YearContractSummary, Months

rates = Rates()

employment_settings = (
    EmploymentContractSettings().SettingsBuilder()
    .is_increased_costs(True)
    .is_active_business(False)
    .is_under_26(False)
    .is_fp_fgsp(True)
    .build()
)

mandate_settings = (
    MandateContractSettings().SettingsBuilder()
    .set_mandate_contract_type(MandateContractType.COMMON)
    .is_fifty(False)
    .is_fp(True)
    .is_fgsp(True)
    .build()
)

work_settings = (
    WorkContractSettings().SettingsBuilder()
    .is_a_lump_sum(False)
    .set_work_contract_type(WorkContractType.COMMON)
    .build()
)

self_employment_settings = (
    SelfEmploymentSettings().SettingsBuilder()
    .set_self_employment_type(SelfEmploymentType.COMMON)
    .set_sick_pay(True)
    .set_tax_type(TaxType.A_LUMP_SUM)
    .set_tax_lump_rate(Decimal('0.055'))
    .set_health_base(HealthBase.NONE)
    .set_costs(Decimal('0.0'))
    .set_tax_base_sum(Decimal('0.0'))
    .set_name("Self Employment")
    .build()
)

employment_contract = EmploymentContract(rates, employment_settings)
employment_contract.calculate(Decimal("7000"), SalaryType.GROSS)

mandate_contract = MandateContract(rates, mandate_settings)
mandate_contract.calculate(Decimal("7000"), SalaryType.GROSS)

work_contract = WorkContract(rates, work_settings)
work_contract.calculate(Decimal("7000"))

self_employment = SelfEmployment(rates, self_employment_settings)
self_employment.calculate(Decimal("7000"), SalaryType.NET)

print(self_employment)
```

## Year Summary and Comparisons

```python
year_employment_contract = YearContractSummary(rates, employment_settings, Decimal('8000'), SalaryType.NET)
#or initiate from contract
#year_employment_contract = YearContractSummary.from_contract(self_employment)
year_employment_contract.calculate()

year_employment_contract.modify_month_contracts([Months.MAR, Months.DEC], rates=rates, salary_base=Decimal('2100'))
year_employment_contract.modify_month_contracts([Months.APR, Months.AUG], enabled=False)
year_employment_contract.calculate()

print(year_employment_contract)

print(year_employment_contract["MAR"].compare_to(year_employment_contract["MAY"]))
print(self_employment.compare_to(year_employment_contract["MAY"]))
```

## Export Options

```python
year_employment_contract.to_excel("Output.xlsx")
df = year_employment_contract.get_data_frame()

self_employment.to_compared_excel("Comparison.xlsx")

rates.to_csv("rates.csv")
employment_settings.to_json("settings.json")
```

## Requirements
- Python 3.9+
- `decimal` (built-in)
- Optional: `pandas` (for DataFrame export)

## License
MIT
