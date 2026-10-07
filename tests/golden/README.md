# Golden cases

`cases.json` is the language-independent specification of the calculator. It is
produced by the Python reference implementation and replayed by the tests in
this directory; ports (e.g. Kotlin) must reproduce every expected value.

Regenerate: `python -m tests.golden.generate` (deterministic - rerunning gives an
identical file, so a git diff shows exactly which results changed).
Verify: `pytest tests/golden`.

## Format

```
{ "format_version": 1,
  "rates": { "2025": {...}, "2026": {...} },   // yearly inputs + derived values
  "settings_validation": [ {...}, ... ],       // settings that must be rejected on creation
  "cases": [ {...}, ... ] }                    // one case per line
```

A case:

| field | meaning |
|---|---|
| `id` | `<contract>/<rates year>/<settings variant>/<gross\|net>-<salary>` |
| `contract` | `employment`, `mandate`, `work`, `self_employment` |
| `rates` | key into the top-level `rates` table |
| `settings` | every field of the contract settings (enums by name) |
| `salary`, `salary_type` | input amount and `GROSS` / `NET` |
| `expected` | all result fields (same names as `Salary.to_dict()` plus `social_security_base_total`, `cost_fifty_total`, `tax_base_total`) |
| `expected_error` | instead of `expected`: the calculation must fail with this validation error (`type`, `message`) |

`settings_validation` entries have `contract`, `settings` and `expected_error`: creating
the settings object must fail with exactly that message (PPK limits), before any
calculation happens.

Rates carry the three yearly inputs (`minimum_wage`, `forecast_average_wage`,
`average_wage_q4`); all other rates are the defaults of `Rates`. `derived`
holds the values calculated from them, so a port can check its own derivation.

## Replaying in a port

- Decimals are strings. Use `BigDecimal`, never floating point, and compare
  numerically (`compareTo`), because `"1000.00"` and `"1000"` are equal.
- Rounding: tax advance, tax base and costs are rounded half-up to full
  zlotys; every other amount is rounded half-up to 0.01 (`ROUND_HALF_UP` /
  `RoundingMode.HALF_UP`). Round at the same steps as the Python pipeline
  (each field is rounded when it is calculated, not only at the end).
- Enum values are given by name (`TaxType.LINE_TAX` -> `"LINE_TAX"`).
- `NET` cases search for the gross salary that gives the requested net.

Not covered yet: the yearly summary / month-by-month orchestration
(`YearContractSummary`) and the contract comparison - the cases test a single
month with explicit cumulative values (`*_sum` settings).
