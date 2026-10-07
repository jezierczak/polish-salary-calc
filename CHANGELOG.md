# Changelog

## 0.2.1

### Fixed (behaviour)
- Mandate (`umowa zlecenie`) and work (`umowa o dzieło`) contracts now use the
  progressive scale: 32% is applied to the part of the cumulative tax base above
  the 120 000 PLN threshold (`tax_base_sum` is taken into account). Previously
  they always used 12%, which understated the tax for high yearly incomes.
- `YearContractSummary.modify_month_contracts()` without `salary_type` keeps the
  summary's default type instead of silently switching the month to GROSS.
- `MandateContract`: PPK contributions and PPK tax are excluded for both
  `UNDER_26_AND_STUDENT` and `OTHER_COMPANY_MIN_SALARY` (the comparison
  previously covered only the first type; no numeric impact, as the base is 0).

## 0.2.0

### Added
- `Rates.for_year(2025 | 2026)`; rates of a year are defined by three inputs
  (`minimum_wage`, `forecast_average_wage`, `average_wage_q4`) stored in
  `polish_salary_calc/rates/data/<year>.json`.
- PPK limits: employee 0.5%-4%, employer 1.5%-4%. Contribution rates are validated
  when settings are created or built, when a contract is created and in `update_options()`.
- `SalaryUtilities.round_to_full_zloty()`.
- Golden test cases (`tests/golden/`) - a language-independent specification of the calculator.

### Changed (behaviour)
- Tax advance, tax base and costs are rounded half-up to full zlotys (the advance
  used to be rounded up, so it was up to 1 PLN too high).
- Amounts in groszy are rounded half-up (previously half-even), e.g. health insurance
  4314.50 * 9% = 388.305 is now 388.31.
- Lump-sum health insurance base for revenue up to 60 000 PLN in 2025: 5129.51
  (was 5129.18, a typo), so the contribution is 461.66 instead of 461.63.
- `update_options()` validates the new settings before replacing the old ones.

### Changed (API)
- `Rates`: `standard_social_insurance_base`, `reduced_social_insurance_base`,
  `social_insurance_cap`, `health_insurance_base`, `unregistered_cap`,
  `se_lump_health_insurance_cap` and `health_insurance_lump_base` are read-only
  properties derived from the yearly inputs and can no longer be assigned or passed
  to the constructor. New fields: `forecast_average_wage`, `average_wage_q4`.
- `RatesDict` now matches the `Rates` fields (`tax_free_base`, ...); `Rates.to_dict()`
  and the settings' `to_dict()` return copies instead of the live `__dict__`.
- `ContractSettngs` was renamed to `ContractSettings`; the old name still works
  but emits a `DeprecationWarning`.
- `SalaryDict` describes what `Salary.to_dict()` really returns.
- The architecture image and diagram moved from the package to `docs/`.
- License metadata is `MIT`.

### Removed
- Pass-through method overrides in contract classes (no behaviour change).
