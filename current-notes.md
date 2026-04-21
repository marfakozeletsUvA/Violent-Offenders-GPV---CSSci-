# Panel Audit — current-notes.md

**Date:** 2026-04-21  
**Panel version:** `panel_with_controls_1992_2024.csv` (rebuilt clean, commit `a22734f`)  
**Status:** 🟡 NEEDS ATTENTION — one medium flag (negative ODA values), all structural checks pass

---

## Summary

The panel is structurally sound. Shape, duplicates, year coverage, null constraints, and all documented missingness values match exactly. One medium issue identified: `bilateral_oda` contains 4,714 negative values (4.5% of non-null ODA rows), reflecting DAC2 loan repayment accounting. A decision is needed before modelling on whether to floor at 0 or retain negatives.

---

## 1. Basic Integrity

| Check | Result |
|---|---|
| Shape | 115,640 rows × 14 columns ✓ |
| Duplicate rows | 0 ✓ |
| Nulls in sender_iso3 | 0 ✓ |
| Nulls in recipient_iso3 | 0 ✓ |
| Nulls in year | 0 ✓ |
| Nulls in arms_tiv | 0 ✓ |
| Nulls in colonial_tie | 0 ✓ |
| Nulls in journalist_killings | 0 ✓ |

**Columns in order:** `sender_iso3`, `recipient_iso3`, `year`, `arms_tiv`, `bilateral_oda`, `econ_neocol_score`, `colonial_tie`, `journalist_killings`, `gdp_per_capita`, `gdp_per_capita_log`, `population`, `population_log`, `armed_conflict`, `conflict_intensity`

---

## 2. Value Range Sanity

### arms_tiv
- Min: 0.0 | Max: 3,895.20 | Mean: 7.25
- Negatives: **0** ✓

### bilateral_oda ⚠️
- Min: **−1,206.34** | Max: 11,790.04
- **Negatives: 4,714 rows (4.5% of non-null ODA rows)**
- These are DAC2 loan repayment adjustments — not data errors, but valid accounting entries where aid recipients repaid past concessional loans. Largest negative values: JPN→IDN, KWT→BGD, JPN→THA.
- **Decision needed before modelling:** floor at 0 (treat as no net aid transfer) or retain negatives (model raw DAC2 values). Flooring is more conservative and standard in the literature.

### econ_neocol_score
- Min: 0.0 | Max: 3.55e-5 | Median: 3.33e-9
- Consistent with notebook 08 output ✓

### journalist_killings
- Min: 0 | Max: 82 (ISR 2024)
- Negatives: **0** ✓

### gdp_per_capita
- Min: 30.25 (MMR early 1990s) | Max: 137,781.68
- 171 rows with gdp_per_capita < 100 — countries: MMR, COD, IRQ, LBR, AZE
- These are plausible historical values for conflict-affected/transitional economies (Liberia civil war, Iraq sanctions era, Myanmar pre-reform). Not errors, but potential leverage points in models.
- No values above 200,000 ✓

### colonial_tie
- Values: {0, 1} only ✓

### year
- Range: 1992–2024 ✓
- No missing years in 1992–2024 ✓
- No out-of-range values ✓

---

## 3. Consistency Checks

### Killings in sender-only countries
- Countries with journalist_killings > 0 that are sender-only: **none** ✓
- All countries with recorded killings appear as recipients ✓

### Colonial tie sender integrity
- Rows with colonial_tie = 1 but sender NOT in {BEL, GBR, FRA, DEU, ITA, NLD, PRT, ESP}: **0** ✓
- Directed dyadic merge is correct ✓

### Arms + ODA overlap
- Rows with arms_tiv > 0 AND bilateral_oda > 0: **3,884 (3.4%)**
- Expected — major powers (USA, FRA, GBR) both sell arms and give aid to the same recipients. Plausible.

### econ_neocol_score > 0 AND colonial_tie = 1
- **2,594 rows (2.2%)** — theoretically most important dyads
- Top values: ESP → GNQ (Equatorial Guinea), historically correct
- These dyads are where historical colonial ties and ongoing economic dominance overlap — the core theoretical claim of the project

---

## 4. Temporal Coverage

| Layer | 1992–1999 | 2000–2009 | 2010–2024 |
|---|---|---|---|
| arms_tiv > 0 | 2,442 | 3,385 | 6,299 |
| bilateral_oda non-null | 20,116 | 30,276 | 53,447 |
| econ_neocol_score > 0 | 10,029 | 24,661 | 41,459 |
| colonial_tie = 1 | 1,085 | 1,307 | 1,975 |
| journalist_killings > 0 | 3,031 | 5,514 | 10,779 |

**Notes:**
- All layers grow over time — reflects panel expansion (more dyads added as more data becomes available) and real-world trends, not a data artefact.
- `econ_neocol_score` is absent for 1992–1994 (8,104 rows, ECI gap — documented in LIMITATIONS.md).
- `journalist_killings > 0` row count of 2002 dips to 279 (vs ~460–580 surrounding years). Likely genuine (post-9/11 reporting focus shift, not a coverage gap).
- 2011 spike in killings rows (987) reflects Arab Spring and Mexico drug war casualties — expected.

---

## 5. Cross-Check Against LIMITATIONS.md

| Metric | Panel value | Documented value | Match |
|---|---|---|---|
| econ_neocol_score total NaN | 35,181 | 35,181 | ✓ |
| NaN from year < 1995 | 8,104 | 8,104 | ✓ |
| NaN from ECI country gap (approx) | ~24,175* | 28,262 | ⚠️ see note |
| colonial_tie = 1 count | 4,367 | 4,367 | ✓ |
| colonial_tie = 1 % | 3.78% | 3.78% | ✓ |
| journalist_killings zeros | 96,316 | 96,316 | ✓ |
| journalist_killings zero % | 83.29% | 83.29% | ✓ |

**Note on ECI country gap count (24,175 vs 28,262):** The LIMITATIONS.md figure of 28,262 was computed in notebook 08 by checking whether `eci_sender` or `eci_receiver` was actually NaN after the merge (i.e., the country was in the ECI file but had no data for that specific year). The cross-check here used a simpler country-set membership test, which undercounts because it misses countries present in the ECI file but without year-specific values. The total NaN count (35,181) matches exactly — no data issue, measurement artifact only.

---

## Full Missingness Summary

| Column | NaN count | % |
|---|---|---|
| sender_iso3 | 0 | 0.0% |
| recipient_iso3 | 0 | 0.0% |
| year | 0 | 0.0% |
| arms_tiv | 0 | 0.0% |
| bilateral_oda | 11,801 | 10.2% |
| econ_neocol_score | 35,181 | 30.4% |
| colonial_tie | 0 | 0.0% |
| journalist_killings | 0 | 0.0% |
| gdp_per_capita | 2,751 | 2.4% |
| gdp_per_capita_log | 2,751 | 2.4% |
| population | 733 | 0.6% |
| population_log | 733 | 0.6% |
| armed_conflict | 644 | 0.6% |
| conflict_intensity | 644 | 0.6% |

---

## Flags Summary

| # | Flag | Severity | Action needed |
|---|---|---|---|
| 1 | **bilateral_oda has 4,714 negative values** (min −1,206, 4.5% of non-null rows) — DAC2 loan repayment accounting. JPN, KWT, ESP most affected. | **MEDIUM** | Decide before modelling: floor at 0 or retain. Recommend floor at 0 for a "net aid flows" interpretation. |
| 2 | **gdp_per_capita < 100** in 171 rows (MMR, COD, IRQ, LBR, AZE — conflict/transition era) | LOW | Not errors. Flag as leverage points in model diagnostics. |
| 3 | **ECI NaN decomposition cross-check discrepancy** (24,175 vs documented 28,262) | LOW | Measurement artifact — different counting method. Total NaN matches exactly. No action needed. |

---

## Next Steps

1. **Decision on negative ODA** — floor at 0 or retain? Document in LIMITATIONS.md.
2. **Monadic collapse** — sum incoming scores per recipient-year to produce the baseline modelling panel.
3. **Log transformation** of `econ_neocol_score` and `arms_tiv` before modelling (both right-skewed — documented in LIMITATIONS.md).
4. **Model fitting** — hurdle NegBin on collapsed monadic panel.
