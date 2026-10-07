# Specyfikacja portu: kalkulator wynagrodzeń na Androida (Kotlin, offline)

Dokument opisuje, co i jak przenieść z biblioteki Python `polish-salary-calc`
(wersja 0.2.0) do aplikacji na Androida w Kotlinie. Jest napisany tak, żeby dało
się go przekazać komuś (lub modelowi) bez dostępu do kodu Pythona: zawiera
wszystkie wzory, kolejność obliczeń, zasady zaokrągleń i kryteria odbioru.

**Źródła prawdy, w tej kolejności:**
1. `tests/golden/cases.json` - 1130 przypadków z wynikami do grosza (kryterium odbioru).
2. `polish_salary_calc/rates/data/<rok>.json` - stawki roczne.
3. Ten dokument (opis reguł).
4. Kod Pythona (gdy dokument jest niejasny; pliki wskazane w tekście).

Jeśli dokument i golden się rozjeżdżają, **wygrywa golden**, a rozjazd należy zgłosić.

**Weryfikacja specyfikacji:** rozdziały 3-12 zostały sprawdzone przez niezależną
implementację napisaną wyłącznie z tego tekstu (bez zaglądania do kodu biblioteki).
Odtworzyła ona wszystkie 1130 przypadków z golden co do grosza (w tym 90 oczekiwanych
błędów). Rozdziały 13 (widok roczny) i 14 (uwagi) opisują kod, ale golden ich nie pokrywa.

---

## 1. Cel i zakres

- Aplikacja na Androida, **w pełni offline**, bez konta i serwera.
- Liczy wynagrodzenie dla: umowy o pracę, zlecenia, dzieła i samozatrudnienia
  (skala, liniowy, ryczałt) - brutto→netto i netto→brutto - oraz koszt pracodawcy.
- Widok roczny (12 miesięcy z narastającymi limitami) i porównanie dwóch wyników.
- Eksport/zapis scenariuszy lokalnie. Excel/CSV/pandas z wersji Pythona **nie** są
  w zakresie pierwszej wersji.
- Tylko Android. iOS jest odłożony (patrz 3.3).

## 2. Architektura

```
app/        Android, Jetpack Compose (UI, nawigacja, zapis scenariuszy)
core/       czysty Kotlin/JVM, BEZ zależności od Androida (cała logika)
core/src/test/resources/golden/cases.json    <- kopia z repo Pythona
core/src/main/resources/rates/2025.json, 2026.json
```

Zasada: **cała logika w `core`**, UI tylko wywołuje `core` i wyświetla wynik.
Dzięki temu `core` testuje się na JVM bez emulatora, a golden odpala się w sekundy.

Pakiety w `core` (odpowiadają modułom Pythona):

| Kotlin | Python |
|---|---|
| `rates/Rates`, `RatesLoader` | `rates/rates.py` |
| `settings/*` | `contract_settings/*` |
| `contracts/*` | `contracts/*` |
| `salary/SalaryResult`, `SalaryUtilities` | `salary/salary.py`, `salary_utilities.py` |
| `summary/YearSummary` | `summary/contract_summary.py` |

## 3. Zasady liczbowe (najważniejsze źródło błędów)

### 3.1 Typy
- Wszystkie kwoty i stawki: `java.math.BigDecimal`. **Nigdy** `Double`/`Float`.
- Tworzenie z napisów (`BigDecimal("0.0976")`), nie z `Double`.
- Porównania przez `compareTo`, nie `equals` (`"1000.00"` i `"1000"` są równe liczbowo).

### 3.2 Zaokrąglenia
Python zaokrągla przy każdym polu w chwili jego wyliczenia (nie tylko na końcu).
Port musi robić to samo, w tej samej kolejności.

| Pole | Zaokrąglenie |
|---|---|
| `tax_advance_payment`, `tax_base`, `cost`, `regular_cost` | do pełnych złotych, `HALF_UP` |
| wszystkie pozostałe kwoty | do 0,01, `HALF_UP` |
| `regular_cost`, `cost` w samozatrudnieniu | do 0,01 (nie do złotych) |

`HALF_UP` w Kotlinie: `setScale(0 lub 2, RoundingMode.HALF_UP)`. Podstawa prawna:
składki i podstawy - do pełnych groszy od 0,5 grosza w górę; podatek - do pełnych
złotych od 50 groszy w górę (art. 63 § 1 Ordynacji podatkowej).

### 3.3 Dzielenie
W Pythonie dzielenie używa kontekstu `Decimal` (precyzja 28 cyfr, `HALF_EVEN`).
W Kotlinie dzielenie `BigDecimal` **wymaga jawnego** `MathContext`. Użyj
`MathContext(28, RoundingMode.HALF_EVEN)` w tych trzech miejscach:
1. `Rates.monthTaxFree = taxFree / 12`
2. składka społeczna samozatrudnionego przy chorobowym: `ssb * (monthDays - sickDays) / monthDays`
3. wskaźniki procentowe: `x / totalEmployerCost * 100`

Mnożenia i dodawania są dokładne (bez `MathContext`).

> **Uwaga o przyszłym iOS:** `BigDecimal` jest tylko na JVM. Jeśli kiedyś pojawi się
> iOS (Kotlin Multiplatform), trzeba będzie podmienić go na bibliotekę
> multiplatformową (np. `bignum`). Żeby to ułatwić, w `core` użyj własnego aliasu
> typu (`typealias Money = BigDecimal`) i nie rozrzucaj `java.math` po kodzie.
> To jest zadanie na później i nie jest darmowe.

## 4. Stawki (`Rates`)

### 4.1 Wejścia roczne (z pliku JSON)
`minimum_wage`, `forecast_average_wage`, `average_wage_q4`, `description`.

| | 2025 | 2026 |
|---|---|---|
| minimum_wage | 4666 | 4806 |
| forecast_average_wage | 8673 | 9420 |
| average_wage_q4 | 8549.18 | 9228.64 |

### 4.2 Wartości pochodne (tylko do odczytu, liczone z wejść)
| Pole | Wzór | zaokr. |
|---|---|---|
| `standard_social_insurance_base` | 0,6 × forecast_average_wage | 0,01 HALF_UP |
| `reduced_social_insurance_base` | 0,3 × minimum_wage | 0,01 HALF_UP |
| `social_insurance_cap` | 30 × forecast_average_wage | brak |
| `health_insurance_base` = `unregistered_cap` | 0,75 × minimum_wage | 0,01 HALF_UP |
| `se_lump_health_insurance_cap` | (60 000; 300 000) | stała |
| `health_insurance_lump_base` | (0,6; 1; 1,8) × average_wage_q4 | każdy 0,01 HALF_UP |
| `tax_free` | `income_tax[0]` × `tax_free_base` | brak |
| `month_tax_free` | `tax_free / 12` (MathContext) | brak |

Wartości pochodne są zapisane w `cases.json` (`rates.<rok>.derived`) - test ma je
porównać z własnymi.

### 4.3 Stałe (domyślne, nie zależą od roku w obecnej wersji)
```
pension_insurance_rate 0.0976            disability_insurance_rate 0.015
sickness_insurance_rate 0.0245           health_insurance_rate 0.09
health_insurance_rate_line_tax 0.049     line_tax_rate 0.19
income_tax (0.12, 0.32)                  tax_threshold 120000
tax_free_base 30000                      cost_threshold 120000
income_tax_deduction (250, 300)          # koszty uzyskania: zwykłe, podwyższone
income_tax_deduction_20_50 (0.2, 0.5)    # koszty 20% i 50%
employer_pension_contribution_rate 0.0976   employer_disability_contribution_rate 0.065
accident_insurance_rate 0.0167           fp_rate 0.0245       fgsp_rate 0.001
```
Stawki mają być wczytywane z JSON-a (lub z listy w kodzie ładowanej tak samo),
tak by nowy rok = nowy plik, bez zmiany logiki.

## 5. Ustawienia umów

Wspólne pola (wszystkie typy), wszystkie `BigDecimal` jeśli nie napisano inaczej:
`current_month_gross_sum=0`, `social_security_base_sum=0`, `cost_fifty_sum=0`,
`tax_base_sum=0`, `employee_ppk=0`, `employer_ppk=0`, `accident_insurance_rate=null`
(nullable; gdy `null` - używa się `rates.accident_insurance_rate`), `salary_deductions=0`.

Pola `*_sum` to **narastające sumy z poprzednich miesięcy** (limit 30-krotności,
limit kosztów 50%, próg podatkowy). Dla pojedynczego miesiąca zostają 0.

| Typ | Dodatkowe pola (domyślnie) |
|---|---|
| Employment | `increased_costs=false`, `cost_fifty_ratio=0`, `fp_fgsp=false`, `active_business=false`, `under_26=false`, `sick_pay=0` |
| Mandate | `mandate_contract_type=COMMON` {COMMON, THE_SAME_COMPANY, OTHER_COMPANY_MIN_SALARY, UNDER_26_AND_STUDENT}, `is_fifty=false`, `fp=false`, `fgsp=false`, `is_a_lump_sum=false` |
| Work | `work_contract_type=COMMON` {COMMON, THE_SAME_COMPANY}, `is_fifty=false`, `is_a_lump_sum=false` |
| SelfEmployment | `self_employment_type=COMMON` {COMMON, PREFERRED, STARTUP_RELIEF, UNREGISTERED_BUSINESS}, `tax_type=STANDARD` {STANDARD, LINE_TAX, A_LUMP_SUM}, `tax_lump_rate=0.17`, `health_base=NONE` {NONE=0, LOW=1, MEDIUM=2, HIGH=3}, `is_sick_pay=false`, `sick_pay_days=0` (int), `month_days=0` (int), `is_fp=true`, `other_minimum_contract=false`, `costs=0` |

Dozwolone stawki ryczałtu: `0.02, 0.03, 0.055, 0.085, 0.10, 0.12, 0.14, 0.15, 0.17`.

### 5.1 Walidacja (musi rzucać błąd o tej samej treści co w golden)
Ustawienia są walidowane **przy tworzeniu** (nie dopiero przy liczeniu):
- PPK pracownika: 0 lub w zakresie **0,005–0,04**; PPK pracodawcy: 0 lub **0,015–0,04**.
  Za mało: `Employer or employee PPK rate is too small`; za dużo: `... is too large`.
  (Sprawdzenie „za mało” ma pierwszeństwo przed „za dużo”.)
- Stawka ryczałtu spoza zbioru: `Lump rate not allowed` (przy obliczaniu, tylko dla `A_LUMP_SUM`).
- Działalność nieewidencjonowana: gdy `salary_base > unregistered_cap`:
  `Salary base for unregistered business exceeded unregistered business income cap`
  (sprawdzane po policzeniu wszystkich pól).

W aplikacji walidację należy zrobić też w UI (pole czerwone, zanim użytkownik kliknie „Policz”),
ale **błędy z `core` muszą mieć te same komunikaty i być typu `IllegalArgumentException`**.

Limitu PPK 0,5% (obniżona wpłata) biblioteka **nie weryfikuje**: nie zna łącznych
zarobków osoby (próg 120% płacy minimalnej). UI może to zasygnalizować podpowiedzią.

## 6. Funkcje pomocnicze (`SalaryUtilities`)

```
roundZl(x)    = x.setScale(0, HALF_UP)
round2(x)     = x.setScale(2, HALF_UP)

capped(rate, base, sum, cap):                  // emerytalna / rentowa (limit 30x)
  total = sum + base
  if total <= cap          -> base * rate
  elif total - base > cap  -> 0
  else                     -> (base - (total - cap)) * rate

authorCost(deduction, ratio, base, sum, threshold):     // koszty 50%
  fifty = if base > deduction then (base - deduction) * ratio else 0
  total = sum + fifty
  if total <= threshold         -> fifty
  elif total - fifty < threshold-> threshold - (total - fifty)
  else                          -> 0

progressiveTax(rates, base, sum, threshold, monthTaxFree = 0):   // skala miesięczna
  total = sum + base
  if total <= threshold:
      out = base * r0 - monthTaxFree
  elif total - base <= threshold:
      out = (threshold - (total - base)) * r0 - monthTaxFree + (total - threshold) * r1
  else:
      out = base * r1
  return max(out, 0)
```
`r0`=`income_tax[0]` (0,12), `r1`=`income_tax[1]` (0,32), `threshold`=`tax_threshold`.

## 7. Potok obliczeń brutto→wynik

`calculate(salary, GROSS)` wykonuje `calculateGross()`. Pola liczy się **w tej kolejności**,
każde zaokrągla się w chwili obliczenia (3.2). Poniżej wersja bazowa
(umowa o pracę); odchyłki per typ umowy w rozdziałach 8-11.

```
 1 salary_base            = input_salary
 2 salary_sick_pay        = 0                      (Employment: settings.sick_pay)
 3 salary_gross           = salary_base + salary_sick_pay
 4 social_security_base   = salary_base            (uwaga: bez chorobowego)
 5 social_security_base_total = settings.social_security_base_sum + social_security_base
 6 pension_insurance      = capped(pension_insurance_rate,   ssb, ss_sum, cap)
 7 disability_insurance   = capped(disability_insurance_rate, ssb, ss_sum, cap)
 8 sickness_insurance     = ssb * sickness_insurance_rate
 9 social_insurance_sum   = pension + disability + sickness
10 health_insurance_base  = salary_gross - (pension + disability + sickness)
11 regular_cost           = roundZl(koszty zwykłe, zależne od umowy)
12 author_rights_cost     = round2(koszty 50%, zależne od umowy)
13 cost                   = roundZl(author_rights_cost + regular_cost)
14 cost_fifty_total       = settings.cost_fifty_sum + author_rights_cost
15 tax_base               = roundZl(salary_gross - social_insurance_sum - cost)
16 tax_base_total         = settings.tax_base_sum + tax_base
17 ppk_tax                = ssb * employer_ppk * income_tax[0]
18 tax                    = clampPositive( podatek_umowy + ppk_tax )   // <=0 -> 0
19 health_insurance       = health_insurance_base * health_insurance_rate
20 salary_deductions      = settings.salary_deductions
21 tax_advance_payment    = roundZl(tax)
22 employee_ppk_contribution = ssb * employee_ppk
23 employer_pension_contribution    = capped(employer_pension_contribution_rate, ...)
24 employer_disability_contribution = capped(employer_disability_contribution_rate, ...)
25 accident_insurance     = ssb * (settings.accident_insurance_rate ?: rates.accident_insurance_rate)
26 fp                     = if (settings.current_month_gross_sum + salary_gross >= minimum_wage)
                              ssb * fp_rate else 0
27 fgsp                   = ssb * fgsp_rate
28 employer_ppk_contribution = ssb * employer_ppk
29 net_salary             = salary_gross - (social_insurance_sum + tax_advance_payment
                              + employee_ppk_contribution + health_insurance + salary_deductions)
30 total_employer_cost    = salary_gross + employer_pension_contribution
                              + employer_disability_contribution + accident_insurance
                              + fp + fgsp + employer_ppk_contribution
```

Pola wyliczane po fakcie (nie zaokrąglane w potoku, tylko przy odczycie, `round2`):
```
total_markups       = round2(total_employer_cost - net_salary)
net_ratio           = total_employer_cost == 0 ? 0 : round2(net_salary / total_employer_cost * 100)
total_markups_ratio = total_employer_cost == 0 ? 0 : round2(total_markups / total_employer_cost * 100)
```
(`gross_ratio` istnieje w Pythonie, ale nie jest eksportowany ani w golden.)

## 8. Umowa o pracę (`EmploymentContract`)

- `salary_sick_pay = settings.sick_pay`.
- `regular_cost`: `increased_costs ? income_tax_deduction[1] : income_tax_deduction[0]` (300 / 250).
- `author_rights_cost = authorCost(regular_cost, cost_fifty_ratio, health_insurance_base, cost_fifty_sum, cost_threshold)`.
  Uwaga: `deduction` to **już zaokrąglone** `regular_cost`.
- Podatek (krok 18, przed dodaniem `ppk_tax`):
  - `under_26` → 0 (i `ppk_tax` = 0),
  - w przeciwnym razie `progressiveTax(income_tax, tax_base, tax_base_sum, tax_threshold, monthTaxFree)`,
    gdzie `monthTaxFree` jest stosowane tylko gdy `active_business == false`
    (czyli „zerowy PIT” z kwoty wolnej 300 zł/mies. tylko dla pracownika bez działalności).
- `fp` i `fgsp`: jeśli `fp_fgsp == false` → 0; inaczej wzory bazowe (26, 27).

## 9. Zlecenie (`MandateContract`)

| Typ | ssb | emerytalna/rentowa | chorobowa | koszty | podatek |
|---|---|---|---|---|---|
| COMMON | salary_base | tak | **0** | 20% lub 50% | skala |
| THE_SAME_COMPANY | salary_base | tak | tak | jw. | skala |
| OTHER_COMPANY_MIN_SALARY | **0** | 0 | 0 | jw. | skala |
| UNDER_26_AND_STUDENT | **0** | 0 | 0 | **cost=0**, `health_insurance_base=0` | **0** |

- `salary_sick_pay = 0`.
- `regular_cost`: jeśli `is_a_lump_sum && salary_gross <= 200` → 0; jeśli `!is_fifty` →
  `health_insurance_base * income_tax_deduction_20_50[0]` (20%); inaczej 0.
- `author_rights_cost`: jeśli `!is_fifty` → 0; jeśli `is_a_lump_sum && salary_gross <= 200` → 0;
  inaczej `authorCost(0, income_tax_deduction_20_50[1] /*0.5*/, health_insurance_base, cost_fifty_sum, cost_threshold)`.
- Podatek: `UNDER_26_AND_STUDENT` → 0. Jeśli `is_a_lump_sum && salary_gross <= 200 && type != THE_SAME_COMPANY`
  → `salary_gross * r0`. W pozostałych przypadkach `max(tax_base * r0 - monthTaxFree, 0)`.
  **Zlecenie nie używa drugiego progu (32%) ani `tax_base_sum`** - zob. 14.
- `fp` = 0 gdy `settings.fp == false`; `fgsp` = 0 gdy `settings.fgsp == false`; inaczej wzory bazowe.
- PPK pracownika/pracodawcy i `ppk_tax`: 0 dla `UNDER_26_AND_STUDENT`; dla
  `OTHER_COMPANY_MIN_SALARY` wartość wychodzi 0 i tak (bo ssb = 0). Zob. 14, pkt 1.

## 10. Dzieło (`WorkContract`)

| Typ | ssb | składki społeczne | `health_insurance_base` | PPK |
|---|---|---|---|---|
| COMMON | **0** | 0 | **0** | 0 |
| THE_SAME_COMPANY | salary_base | jak zlecenie THE_SAME_COMPANY (z chorobową) | bazowo | bazowo |

- `salary_sick_pay = 0`.
- `regular_cost`: `is_a_lump_sum && salary_gross <= 200` → 0; `!is_fifty` →
  (THE_SAME_COMPANY: `health_insurance_base * 0.2`, COMMON: `salary_gross * 0.2`); `is_fifty` → 0.
- `author_rights_cost`: `!is_fifty` lub (`is_a_lump_sum && salary_gross <= 200`) → 0; inaczej
  `authorCost(0, 0.5, base, cost_fifty_sum, cost_threshold)` gdzie `base = salary_gross` (COMMON)
  lub `health_insurance_base` (THE_SAME_COMPANY).
- Podatek: jeśli `is_a_lump_sum && salary_gross <= 200 && type != THE_SAME_COMPANY` → `salary_gross * r0`;
  w pozostałych `tax_base * r0` (**bez kwoty wolnej i bez progów**; ujemne wartości wycina krok 18).
- `fp`, `fgsp`: bez flag - wzory bazowe (dla COMMON i tak 0, bo ssb = 0).

## 11. Samozatrudnienie (`SelfEmployment`)

Potok **ma inną kolejność** niż bazowy (`accident`, `fp`, `fgsp` liczone przed
`social_insurance_sum`). Kolejność:

```
salary_base, salary_sick_pay(=0), salary_gross = salary_base - costs,
social_security_base, social_security_base_total,
pension_insurance, disability_insurance, sickness_insurance,
regular_cost = round2(costs), author_rights_cost = 0, cost = round2(...), cost_fifty_total,
employee_ppk_contribution(=0), employer_pension_contribution(=0), employer_disability_contribution(=0),
accident_insurance, fp, fgsp(=0),
social_insurance_sum, tax_base = roundZl(...), tax_base_total, ppk_tax(=0), tax,
health_insurance_base, health_insurance, salary_deductions, tax_advance_payment,
employer_ppk_contribution(=0), net_salary, total_employer_cost = salary_base
```

- **ssb:** `other_minimum_contract` → 0. W przeciwnym razie wg typu: COMMON → `standard_social_insurance_base`;
  PREFERRED → `reduced_social_insurance_base`; STARTUP_RELIEF i UNREGISTERED_BUSINESS → 0.
  Jeśli `is_sick_pay && sick_pay_days > 0 && month_days > 0`: `ssb * (month_days - sick_pay_days) / month_days` (MathContext).
- **pension / disability:** `capped(rate_pracownika + rate_pracodawcy, ssb, ss_sum, cap)` (obie części w jednej składce).
- **sickness:** `is_sick_pay ? ssb * sickness_insurance_rate : 0`.
- **accident:** wzór bazowy. **fp:** `is_fp && ssb > minimum_wage ? ssb * fp_rate : 0` (uwaga: **ostra** nierówność `>`).
- **social_insurance_sum** = pension + disability + sickness + accident + fp + fgsp.
- **tax_base:** `A_LUMP_SUM` → `salary_base`; inaczej `salary_gross - social_insurance_sum`; potem `roundZl`.
- **tax:** (potem krok 18: dodanie `ppk_tax`=0 i obcięcie do ≥ 0)
  - `STANDARD`: `present = tax_base + tax_base_sum`:
    - `present <= tax_free_base` → 0
    - `present <= tax_threshold`: jeśli `tax_base_sum <= tax_free_base` → `(present - tax_free_base) * r0`, inaczej `tax_base * r0`
    - `present > tax_threshold`: jeśli `tax_base_sum <= tax_threshold` → `(present - tax_threshold) * r1 + (tax_threshold - tax_base_sum) * r0`, inaczej `tax_base * r1`
  - `LINE_TAX`: `tax_base * line_tax_rate`
  - `A_LUMP_SUM`: walidacja stawki, `tax_base * tax_lump_rate`
- **health_insurance_base:**
  - `UNREGISTERED_BUSINESS` → 0
  - `A_LUMP_SUM`: gdy `health_base == NONE`: `rocznie = 12 * salary_base`; `<= 60000` → `lump[0]`; `<= 300000` → `lump[1]`; inaczej `lump[2]`.
    Gdy `LOW/MEDIUM/HIGH` → `lump[0/1/2]`.
  - inaczej `max(rates.health_insurance_base, salary_gross - social_insurance_sum)`
- **health_insurance:** `LINE_TAX`: `max(rates.health_insurance_base * health_insurance_rate, health_insurance_base * health_insurance_rate_line_tax)`;
  inaczej `health_insurance_base * health_insurance_rate`.
- **net_salary** = `salary_gross - social_insurance_sum - tax_advance_payment - health_insurance`
  (bez `salary_deductions` i PPK).
- **total_employer_cost** = `salary_base`.
- Na końcu: walidacja nieewidencjonowanej (5.1).

## 12. Netto→brutto (`calculate(salary, NET)`)

Algorytm iteracyjny, **dokładnie**:
```
wished = salary
input_salary = wished
net_salary = 0                       // świeży obiekt
while round2(net_salary) != round2(wished):
    input_salary += wished - net_salary
    calculateGross()                 // używa input_salary jako salary_base
input_salary = wished                // przywracane po zakończeniu
```
Wynik końcowy to pola z ostatniego `calculateGross()` (czyli `salary_base`/`salary_gross`
to znalezione brutto).

Uwagi do portu:
- Obiekt musi startować z `net_salary = 0` (w Pythonie każdy obiekt jest świeży).
- **Dodaj limit iteracji** (np. 100) i po jego przekroczeniu rzuć czytelny błąd. Oryginał
  go nie ma. Empirycznie na 600 losowych kwotach (umowa o pracę i zlecenie, 2026)
  pętla kończyła się w ≤ 17 iteracjach, więc limit jest tylko zabezpieczeniem.
- Walidacja nieewidencjonowanej w trakcie iteracji może rzucić błąd w środku pętli - to oczekiwane.

## 13. Widok roczny i porównanie

### 13.1 `YearSummary` (`summary/contract_summary.py`)
Wejście: stawki, ustawienia, kwota, typ kwoty (GROSS/NET). Dla każdego z 12 miesięcy:
1. Jeśli miesiąc **wyłączony** lub kwota = 0 (falsy) → wynik pusty (same zera), bez wkładu do sum.
2. Ustaw w ustawieniach miesiąca: `social_security_base_sum`, `cost_fifty_sum`, `tax_base_sum`
   = narastające sumy z poprzednich miesięcy (start: wartości z ustawień wejściowych).
3. Utwórz umowę właściwego typu i `calculate(kwota, typ)`.
4. Narastające sumy dla następnego miesiąca = `social_security_base_total`, `cost_fifty_total`, `tax_base_total`
   bieżącego miesiąca.
5. Wynik dołóż do podsumowania (`SUMMARY`) jako **sumę po polach** (każde pole kwotowe zsumowane).

W Kotlinie **ustawienia traktuj jako niemutowalne** (`copy(...)` na miesiąc). Python mutuje
jeden współdzielony obiekt, co jest szczegółem implementacji, nie zachowaniem.

`modify_month_contracts(miesiące, enabled, rates, salary_base, salary_type)`: nadpisuje parametry
wybranych miesięcy (stawki, kwota, wyłączenie). Zob. 14, pkt 2.

Pola `*_total` w `SUMMARY` są wewnętrzne i **nie są pokryte golden**; nie eksponuj ich w UI.

### 13.2 Porównanie (`compare_to`)
`różnica = A - B` pole po polu (`A.pole - B.pole` dla wszystkich kwot z listy w 15), nazwa
„DIFFERENCE”. Wskaźniki (`net_ratio`, `total_markups_ratio`) liczone są z pól różnicy
(wzory z 7). Porównywać można dowolne dwa wyniki, także miesiąc z rocznym.

## 14. Do rozstrzygnięcia przed/w trakcie portu

To są miejsca, w których Python robi coś, co wygląda na niezamierzone albo ograniczone.
Port **odtwarza obecne zachowanie** (bo to definiuje golden), dopóki nie podejmiesz decyzji.

1. **`MandateContract`: `type == (A or B)`.** W `calculate_ppk_tax`, `calculate_employee_ppk_contribution`
   i `calculate_employer_ppk_contribution` warunek `== (UNDER_26_AND_STUDENT or OTHER_COMPANY_MIN_SALARY)`
   w Pythonie sprowadza się do porównania tylko z pierwszym. Skutek liczbowy zerowy (dla drugiego typu
   ssb = 0, więc PPK = 0). Można bezpiecznie poprawić w Pythonie (golden się nie zmieni); w Kotlinie
   zaimplementuj intencję (oba typy).
2. **`modify_month_contracts`: `salary_type` domyślnie `GROSS`.** Wywołanie bez `salary_type`
   zmienia kwotę nadpisanych miesięcy na brutto, nawet gdy domyślny typ był netto. Prawdopodobnie błąd;
   w porcie proponuję: brak parametru = typ domyślny podsumowania.
3. **Zlecenie i dzieło nie mają progów podatkowych.** Zlecenie liczy zawsze 12% (minus kwota wolna),
   dzieło zawsze 12%, nawet gdy narastająca podstawa przekracza 120 000 zł. Dla rocznych zarobków
   powyżej progu wynik jest niższy niż w rzeczywistości. Decyzja: udokumentować jako ograniczenie
   w UI albo dodać progi (zmiana w Pythonie + golden + port).
4. **`current_month_gross_sum` nigdy nie jest uzupełniane przez podsumowanie roczne.** Wpływa tylko
   na regułę FP (`>= minimum_wage`) przy kilku umowach u jednego pracodawcy w miesiącu.
5. **FP: `>=` dla pracownika, `>` dla samozatrudnionego.** Wygląda na niespójność; spójne z golden.
6. **Domyślny rok `Rates()` to 2025.** W aplikacji zawsze wybieraj rok jawnie (domyślnie 2026).

## 15. Model wyniku (`SalaryResult`)

Pola dokładnie jak w `expected` w golden (kolejność jak w Pythonie), wszystkie `BigDecimal`:

```
salary_base, salary_sick_pay, salary_gross, social_security_base, pension_insurance,
disability_insurance, sickness_insurance, social_insurance_sum, cost, regular_cost,
author_rights_cost, health_insurance_base, tax_base, tax, health_insurance, ppk_tax,
tax_advance_payment, salary_deductions, employee_ppk_contribution, net_salary,
employer_pension_contribution, employer_disability_contribution, accident_insurance,
fp, fgsp, employer_ppk_contribution, total_employer_cost, total_markups, net_ratio,
total_markups_ratio, social_security_base_total, cost_fifty_total, tax_base_total
```
Nazwy w Kotlinie: camelCase (`salaryBase`, ...). Mapowanie na snake_case tylko w teście golden.

## 16. Strategia testów (kryterium odbioru)

1. Skopiuj `tests/golden/cases.json` do `core/src/test/resources/golden/`.
2. Parser: `kotlinx.serialization` (lub Moshi/Gson) - kwoty to **napisy**; parsuj do `BigDecimal`.
3. Test parametryczny: dla każdego `case` zbuduj stawki (`rates` → `Rates` z 3 wejść), ustawienia
   (`settings`, enumy po nazwie), uruchom `calculate`, porównaj **każde** pole `expected`
   przez `compareTo == 0`. Przypadki z `expected_error` muszą rzucić błąd o tym samym `message`.
4. Test `settings_validation`: tworzenie ustawień z `settings` musi rzucić błąd z `expected_error.message`.
5. Test stawek: wartości pochodne z `rates.<rok>.derived` muszą zgadzać się z własnymi wyliczeniami.
6. Zgłaszaj **pierwsze 20 niezgodności z `id` przypadku**, nie tylko liczbę - `id` ma postać
   `<umowa>/<rok>/<wariant>/<gross|net>-<kwota>`, więc wskazuje, którą regułę zepsuto.

**Kryterium ukończenia `core`:** 1130 przypadków + 16 walidacji zielone, bez wyjątków i bez tolerancji.

Golden **nie pokrywa**: widoku rocznego (13.1) i porównania (13.2). Dla nich napisz własne testy
na przykładach policzonych w Pythonie (`python main.py` wypisuje kilka pełnych scenariuszy) albo
rozszerz generator (`tests/golden/generate.py`) o przypadki roczne - to jest zalecany następny krok
po ukończeniu `core`.

## 17. Aplikacja (Android)

Minimalny zakres pierwszej wersji:
1. **Ekran „Policz”**: wybór umowy, rok stawek, kwota, brutto/netto, opcje (zależne od umowy),
   przycisk „Policz” → wynik (netto, brutto, podatek, składki, koszt pracodawcy).
2. **Szczegóły**: pełna lista pól wyniku.
3. **Porównanie**: dwa scenariusze obok siebie + różnica (13.2).
4. **Rok**: tabela 12 miesięcy z wyłączaniem miesięcy i zmianą kwoty (13.1).
5. **Zapis scenariuszy lokalnie** (Room lub DataStore). Brak sieci, brak telemetrii.

Zasady UI: język polski; kwoty formatowane z separatorem tysięcy i dwoma miejscami (tylko w
warstwie widoku; `core` nie formatuje); pola liczbowe parsowane do `BigDecimal` z przecinka i kropki;
błędy z `core` pokazywane użytkownikowi czytelnie (mapowanie komunikatów na polskie teksty w `app`).

## 18. Plan prac

| Etap | Zakres | Gotowe, gdy |
|---|---|---|
| 0 | Projekt w Android Studio, moduł `core` (Kotlin/JVM), JUnit, zasoby (`cases.json`, stawki) | `./gradlew :core:test` uruchamia pusty test |
| 1 | `Rates`, `RatesLoader`, `SalaryUtilities`, parser golden | testy stawek i pomocnicze zielone |
| 2 | Umowa o pracę (brutto→netto) | wszystkie `employment/*/gross-*` zielone |
| 3 | Netto→brutto | wszystkie `*/net-*` dla umowy o pracę zielone |
| 4 | Zlecenie, dzieło | `mandate/*`, `work/*` zielone |
| 5 | Samozatrudnienie | `self_employment/*` zielone |
| 6 | Walidacje | `settings_validation` i `expected_error` zielone |
| 7 | Widok roczny i porównanie + własne testy | testy roczne zielone |
| 8 | UI (Compose), zapis scenariuszy | ręczny przegląd na emulatorze |

Etapy 1-7 nie wymagają emulatora ani Androida - sam `core`.

### Android Studio - wskazówki startowe
- Nowy projekt „Empty Activity” (Compose), potem **File → New → Module → Kotlin/Java Library** dla `core`.
- Wersje Kotlina, Gradle i bibliotek: użyj aktualnych stabilnych, które proponuje Android Studio
  (version catalog `libs.versions.toml`); w tym dokumencie celowo nie ma numerów wersji.
- Zależności `core`: `kotlinx-serialization-json` (tylko do testów golden), JUnit. **Nic z Androida.**
- Moduł `app` zależy od `core` (`implementation(project(":core"))`).

## 19. Pierwsze polecenie do wykonania w nowym projekcie

> Przeczytaj `docs/kotlin-port-spec.md` i `core/src/test/resources/golden/cases.json`.
> Zrealizuj etapy 0-2 z rozdziału 18: moduł `core`, `Rates` z JSON-a, `SalaryUtilities`
> oraz `EmploymentContract` brutto→netto, aż wszystkie przypadki `employment/*/gross-*`
> z golden przejdą. Nie zmieniaj reguł zaokrągleń z rozdziału 3. Raportuj pierwsze
> niezgodności z `id` przypadku.
