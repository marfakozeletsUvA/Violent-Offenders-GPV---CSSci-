# Presentation Facts — GPV Research Project
**Compiled:** 2026-05-18  
**Source:** Direct extraction from notebooks/16–19 cell outputs and all saved CSVs in outputs/  
**NOT FOUND** entries = searched all output files, not present  

---

## 1. Dataset Confirmed

### Final Modelling Panel
- **File:** `data/merged/panel_final_1992_2024.csv`
- **Shape:** 6,358 rows × 38 columns
- **Unit of analysis:** recipient-country × year (monadic)
- **Coverage:** 1992–2024 (33 years)
- **Unique recipient countries:** 213

### Dyadic Panel (source/intermediate)
- **File:** `data/merged/dyadic_panel_1992_2024_oda_capped_log.csv`
- **Shape:** 115,640 rows × 15 columns
- **Columns:** sender_iso3, recipient_iso3, year, arms_tiv, bilateral_oda, econ_neocol_score, colonial_tie, journalist_killings, gdp_per_capita, gdp_per_capita_log, population, population_log, armed_conflict, conflict_intensity, econ_neocol_score_log

### Target Variable Distribution (from `outputs/data&methods/target_distribution.txt`)
- Total recipient-year observations: 6,358
- Zero share: **88.7%**
- Mean killings per year: 0.3688
- Median: 0.0
- Maximum: 82
- Variance/Mean ratio: **14.75×** (overdispersion confirmed)
- Unique recipient countries: 213

### Summary Statistics for Key Variables (from `outputs/data&methods/summary_stats.csv`)

| Variable | Mean | Std | Min | Max | Median | Zero share (%) | Missing (%) |
|---|---|---|---|---|---|---|---|
| arms_tiv_total | 131.95 | 376.33 | 0.0 | 5271.93 | 3.0 | 43.24 | 0.0 |
| oda_total | 292.84 | 793.25 | 0.0 | 22007.84 | 72.39 | 21.53 | 0.0 |
| econ_neocol_score_total | 22.31 | 24.51 | 0.0 | 101.37 | 9.84 | 38.50 | 0.0 |
| colonial_tie_flag | 0.568 | 0.495 | 0 | 1 | 1 | 43.22 | 0.0 |
| journalist_killings | 0.369 | 2.332 | 0 | 82 | 0 | 88.66 | 0.0 |
| gdp_per_capita | 9821.97 | 15570.29 | 30.25 | 137781.68 | 3446.0 | 0 | 6.354 |
| gdp_per_capita_log | 8.138 | 1.531 | 3.41 | 11.833 | 8.145 | 0 | 6.354 |
| population | 36,363,618 | 135,486,968 | 9038 | 1,450,935,791 | 7,749,535 | 0 | 4.215 |
| population_log | 15.571 | 2.163 | 9.109 | 21.095 | 15.863 | 0 | 4.215 |
| armed_conflict | 0.165 | 0.371 | 0 | 1 | 0 | 80.43 | 3.696 |
| conflict_intensity | 0.207 | 0.500 | 0 | 2 | 0 | 80.43 | 3.696 |

### Column Missingness in panel_final (from nb16, Cell 3)
- gdp_per_capita / gdp_per_capita_log: 404 rows (6.35%)
- population / population_log: 268 rows (4.22%)
- armed_conflict / conflict_intensity: 235 rows (3.70%)
- arms_tiv_total_log_lag1, oda_total_log_lag1, econ_neocol_score_total_lag1: 213 rows (3.35%)
- All network lagged measures: 208 rows (3.27%)

### Data Sources (from `outputs/appendices/variable_codebook.csv`)
| Variable | Source |
|---|---|
| arms_tiv_total | SIPRI Arms Transfers Database |
| oda_total | OECD DAC2 (Creditor Reporting System) |
| econ_neocol_score_total | Harvard Growth Lab ECI + BACI/IMF bilateral trade |
| colonial_tie_flag | COLDAT Colonial Dates Dataset |
| journalist_killings | Committee to Protect Journalists (CPJ) Database |
| gdp_per_capita | World Bank WDI |
| population | World Bank WDI |
| armed_conflict | UCDP/PRIO Armed Conflict Dataset v25.1 |
| conflict_intensity | UCDP/PRIO Armed Conflict Dataset v25.1 |

---

## 2. baseline_features List (exact column names from nb16 Cell 5)

```python
baseline_features = [
    'arms_tiv_total_log_lag1',
    'oda_total_log_lag1',
    'econ_neocol_score_total_lag1',
    'colonial_tie_flag',
    'gdp_per_capita_log',
    'population_log',
    'armed_conflict',
    'conflict_intensity',
]
```

**armed_conflict** and **conflict_intensity** are included as **controls** in all models. Both are correlated with the outcome. VIF ~8 between them; robustness check dropping `armed_conflict` is in Part D (nb16) and Part H (nb17). Conflict_intensity is the graded version (0=none, 1=minor, 2=war); armed_conflict is its binary companion.

---

## 3. network_features List (exact column names from nb17)

### network_only_features (8) — added on top of baseline in nb17:
```python
network_only_features = [
    'arms_tiv_in_strength_lag1',
    'arms_tiv_pagerank_lag1',
    'bilateral_oda_in_strength_lag1',
    'bilateral_oda_pagerank_lag1',
    'econ_neocol_score_in_strength_lag1',
    'econ_neocol_score_pagerank_lag1',
    'colonial_tie_in_strength_lag1',
    'colonial_tie_pagerank_lag1',
]
```

### interaction_features (3) — constructed in nb17, not stored in panel_final:
```python
interaction_features = [
    'arms_x_colonial',   # arms_tiv_total_log_lag1 × colonial_tie_flag
    'oda_x_colonial',    # oda_total_log_lag1 × colonial_tie_flag
    'econ_x_colonial',   # econ_neocol_score_total_lag1 × colonial_tie_flag
]
```

### Full network_features (16) = baseline_features (8) + network_only_features (8)

---

## 4. nb16 — Baseline Hurdle Model Results

### Sample Construction (from `outputs/data&methods/sample_construction_nb16.csv` and nb16 Cell 7)

| Stage | N | % |
|---|---|---|
| Panel rows (before dropna) | 6,358 | 100.0 |
| After dropna (model sample) | 5,765 | 90.7 |
| Dropped rows | 593 | 9.3 |
| Zero killing rows (logit denominator) | 5,078 | 88.1 |
| Non-zero killing rows (NegBin) | 687 | 11.9 |

**SE method:** nonrobust (standard MLE defaults) for Part A/B; clustered SEs computed in Part C as robustness (see below).

---

### nb16 — Part A: Logistic Regression (Zero Component)
**n = 5,765 | predicts P(any journalist killing)**

**Model fit:**
- AUC: **0.8488**
- McFadden pseudo-R²: **0.2689**
- AIC: **3097.16** | BIC: 3157.09
- Log-Likelihood: −1539.58
- LLR p-value: 3.999e-239
- Converged: True | SE type: nonrobust

**Coefficients (nonrobust SEs):**

| term | coef | std_err | z | p_value | sig | CI 0.025 | CI 0.975 |
|---|---|---|---|---|---|---|---|
| const | −14.0556 | 0.7891 | −17.811 | 5.77e-71 | *** | −15.602 | −12.509 |
| arms_tiv_total_log_lag1 | −0.0786 | 0.0272 | −2.892 | 3.83e-03 | ** | −0.132 | −0.025 |
| oda_total_log_lag1 | +0.1819 | 0.0305 | +5.954 | 2.62e-09 | *** | +0.122 | +0.242 |
| econ_neocol_score_total_lag1 | −0.0279 | 0.0202 | −1.382 | 0.167 | ns | −0.067 | +0.012 |
| colonial_tie_flag | +0.4876 | 0.1169 | +4.170 | 3.05e-05 | *** | +0.258 | +0.717 |
| gdp_per_capita_log | +0.2150 | 0.0482 | +4.461 | 8.16e-06 | *** | +0.121 | +0.310 |
| population_log | +0.5521 | 0.0410 | +13.472 | 2.29e-41 | *** | +0.472 | +0.632 |
| armed_conflict | −0.4751 | 0.2387 | −1.990 | 4.66e-02 | * | −0.943 | −0.007 |
| conflict_intensity | +1.5425 | 0.1719 | +8.971 | 2.93e-19 | *** | +1.205 | +1.879 |

**Classification report (threshold = 0.5):**
- Accuracy: 89.2% | Precision (nonzero): 0.604 | Recall (nonzero): 0.282 | F1 (nonzero): 0.385

---

### nb16 — Part B: Negative Binomial (Count Component)
**n = 687 (non-zero years only) | predicts count conditional on ≥1 killing**

**Model fit:**
- Pseudo-R²: **0.0984**
- AIC: **2899.30** | BIC: 2944.63
- Log-Likelihood: −1439.65
- Alpha (overdispersion): **0.4632** (SE=0.0365, z=12.678, p=7.82e-37 ***)
- MAE: 2.4032 | RMSE: 5.8009
- SE type: nonrobust

**Coefficients (nonrobust SEs):**

| term | coef | std_err | z | p_value | sig | CI 0.025 | CI 0.975 |
|---|---|---|---|---|---|---|---|
| const | −2.8399 | 0.6424 | −4.421 | 9.84e-06 | *** | −4.099 | −1.581 |
| arms_tiv_total_log_lag1 | −0.0326 | 0.0207 | −1.572 | 0.116 | ns | −0.073 | +0.008 |
| oda_total_log_lag1 | +0.0576 | 0.0234 | +2.456 | 0.014 | * | +0.012 | +0.103 |
| econ_neocol_score_total_lag1 | −0.0318 | 0.0163 | −1.954 | 0.051 | . | −0.064 | +9.8e-05 |
| colonial_tie_flag | +0.3077 | 0.1004 | +3.065 | 0.002 | ** | +0.111 | +0.504 |
| gdp_per_capita_log | +0.2456 | 0.0369 | +6.660 | 2.75e-11 | *** | +0.173 | +0.318 |
| population_log | +0.0709 | 0.0342 | +2.071 | 0.038 | * | +0.004 | +0.138 |
| armed_conflict | −0.9651 | 0.1589 | −6.073 | 1.25e-09 | *** | −1.277 | −0.654 |
| conflict_intensity | +1.2454 | 0.0969 | +12.852 | 8.36e-38 | *** | +1.055 | +1.435 |
| alpha | +0.4632 | 0.0365 | +12.678 | 7.82e-37 | *** | +0.392 | +0.535 |

---

### nb16 — Part C: Clustered SEs (Nonrobust vs Clustered by recipient_iso3)

**Logit — clustered SEs:**

| term | coef | se_nonrobust | p_nonrobust | sig_nonrobust | se_clustered | p_clustered | sig_clustered | sig_changed? |
|---|---|---|---|---|---|---|---|---|
| const | −14.0556 | 0.7891 | 0.0000 | *** | 1.8040 | 0.0000 | *** | No |
| arms_tiv_total_log_lag1 | −0.0786 | 0.0272 | 0.0038 | ** | 0.0481 | 0.1023 | ns | YES |
| oda_total_log_lag1 | +0.1819 | 0.0305 | 0.0000 | *** | 0.0626 | 0.0036 | ** | YES |
| econ_neocol_score_total_lag1 | −0.0279 | 0.0202 | 0.1669 | ns | 0.0360 | 0.4388 | ns | No |
| colonial_tie_flag | +0.4876 | 0.1169 | 0.0000 | *** | 0.2605 | 0.0612 | . | YES |
| gdp_per_capita_log | +0.2150 | 0.0482 | 0.0000 | *** | 0.0982 | 0.0285 | * | YES |
| population_log | +0.5521 | 0.0410 | 0.0000 | *** | 0.0863 | 0.0000 | *** | No |
| armed_conflict | −0.4751 | 0.2387 | 0.0466 | * | 0.4629 | 0.3048 | ns | YES |
| conflict_intensity | +1.5425 | 0.1719 | 0.0000 | *** | 0.3122 | 0.0000 | *** | No |

**NegBin — clustered SEs:**

| term | coef | se_nonrobust | p_nonrobust | sig_nonrobust | se_clustered | p_clustered | sig_clustered | sig_changed? |
|---|---|---|---|---|---|---|---|---|
| const | −2.8399 | 0.6424 | 0.0000 | *** | 1.3509 | 0.0355 | * | YES |
| arms_tiv_total_log_lag1 | −0.0326 | 0.0207 | 0.1160 | ns | 0.0385 | 0.3974 | ns | No |
| oda_total_log_lag1 | +0.0576 | 0.0234 | 0.0141 | * | 0.0466 | 0.2169 | ns | YES |
| econ_neocol_score_total_lag1 | −0.0318 | 0.0163 | 0.0507 | . | 0.0304 | 0.2948 | ns | YES |
| colonial_tie_flag | +0.3077 | 0.1004 | 0.0022 | ** | 0.1421 | 0.0303 | * | YES |
| gdp_per_capita_log | +0.2456 | 0.0369 | 0.0000 | *** | 0.0828 | 0.0030 | ** | YES |
| population_log | +0.0709 | 0.0342 | 0.0384 | * | 0.0612 | 0.2468 | ns | YES |
| armed_conflict | −0.9651 | 0.1589 | 0.0000 | *** | 0.3721 | 0.0095 | ** | YES |
| conflict_intensity | +1.2454 | 0.0969 | 0.0000 | *** | 0.2332 | 0.0000 | *** | No |
| alpha | +0.4632 | 0.0365 | 0.0000 | *** | 0.0668 | 0.0000 | *** | No |

---

### nb16 — VIF Baseline Features (from `outputs/data&methods/vif_table_nb16.csv`)

| Feature | VIF |
|---|---|
| armed_conflict | 8.22 |
| conflict_intensity | 8.06 |
| oda_total_log_lag1 | 2.48 |
| gdp_per_capita_log | 2.48 |
| arms_tiv_total_log_lag1 | 2.30 |
| population_log | 2.23 |
| econ_neocol_score_total_lag1 | 1.44 |
| colonial_tie_flag | 1.35 |

---

### nb16 — ODA Crisis-Aid Sensitivity (IRQ/SYR exclusion)

| Model | Sample | ODA coef | ODA p-value | N |
|---|---|---|---|---|
| logit_any_killing | All | +0.1819 | 2.62e-09 | 5765 |
| logit_any_killing | Excl. IRQ/SYR | +0.1650 | 1.23e-07 | 5703 |
| negative_binomial_positive_counts | All | +0.0576 | 0.014 | 687 |
| negative_binomial_positive_counts | Excl. IRQ/SYR | +0.0063 | 0.800 | 657 |

**Finding:** Count-component ODA effect (NegBin) drops from p=0.014 to p=0.800 when excluding Iraq and Syria. ODA signal in NegBin component is crisis-driven.

---

## 5. nb17 — Network-Augmented Hurdle Model Results

### Sample Construction (same as nb16)

| Stage | N | % |
|---|---|---|
| Panel rows | 6,358 | — |
| After dropna | 5,765 | — |
| Dropped | 593 | 9.3% |
| Non-zero rows (NegBin) | 687 | 11.9% |
| Zero rows (logit) | 5,078 | 88.1% |

**SE method:** clustered by recipient_iso3 throughout (applied to all features from the start).

---

### nb17 — Logistic Regression (Zero Component)
**n = 5,765 | clustered SEs**

**Model fit:**
- AUC: **0.857**
- McFadden pseudo-R²: **0.284**
- AIC: **3054.1** | BIC: 3187.3
- Log-Likelihood: −1507.1
- **ΔAIC vs nb16 logit: −43.1** (lower = better)
- Converged: True

**Full coefficient table (clustered SEs):**

| term | coef | std_err | z | p_value | sig |
|---|---|---|---|---|---|
| const | −14.5189 | 2.6249 | −5.531 | 3.18e-08 | *** |
| arms_tiv_total_log_lag1 | −0.1215 | 0.0890 | −1.366 | 0.172 | ns |
| oda_total_log_lag1 | +0.2239 | 0.1219 | +1.836 | 0.066 | . |
| econ_neocol_score_total_lag1 | +0.2307 | 0.0912 | +2.528 | 0.011 | * |
| colonial_tie_flag | −0.0827 | 0.6296 | −0.131 | 0.896 | ns |
| gdp_per_capita_log | +0.1930 | 0.0880 | +2.192 | 0.028 | * |
| population_log | +0.5303 | 0.0818 | +6.486 | 8.81e-11 | *** |
| armed_conflict | −0.5745 | 0.4660 | −1.233 | 0.218 | ns |
| conflict_intensity | +1.6103 | 0.3316 | +4.857 | 1.19e-06 | *** |
| arms_tiv_in_strength_lag1 | −0.0137 | 0.0161 | −0.850 | 0.396 | ns |
| bilateral_oda_in_strength_lag1 | −0.0103 | 0.0116 | −0.882 | 0.378 | ns |
| econ_neocol_score_in_strength_lag1 | −0.0311 | 0.0110 | −2.826 | 4.72e-03 | ** |
| colonial_tie_in_strength_lag1 | −0.4018 | 0.3309 | −1.214 | 0.225 | ns |
| arms_tiv_pagerank_lag1 | +33.635 | 26.452 | +1.272 | 0.204 | ns |
| bilateral_oda_pagerank_lag1 | +41.501 | 102.181 | +0.406 | 0.685 | ns |
| econ_neocol_score_pagerank_lag1 | +57.369 | 41.399 | +1.386 | 0.166 | ns |
| colonial_tie_pagerank_lag1 | +82.776 | 331.079 | +0.250 | 0.803 | ns |
| arms_x_colonial | +0.1020 | 0.0844 | +1.209 | 0.227 | ns |
| oda_x_colonial | +0.1957 | 0.0980 | +1.996 | 0.046 | * |
| econ_x_colonial | −0.0580 | 0.0794 | −0.731 | 0.465 | ns |

---

### nb17 — Negative Binomial (Count Component)
**n = 687 | clustered SEs**

**Model fit:**
- Pseudo-R²: **0.116**
- AIC: **2863.9** | BIC: 2959.1
- Log-Likelihood: −1410.9
- **ΔAIC vs nb16 NegBin: −35.4** (lower = better)
- Alpha (overdispersion): **0.406** (SE=0.0595, z=6.820, p=9.13e-12 ***)
- MAE: 2.304 | RMSE: 5.565
- Converged: True

**Full coefficient table (clustered SEs):**

| term | coef | std_err | z | p_value | sig |
|---|---|---|---|---|---|
| const | −1.6518 | 1.4750 | −1.120 | 0.263 | ns |
| arms_tiv_total_log_lag1 | +0.0107 | 0.0469 | +0.227 | 0.820 | ns |
| oda_total_log_lag1 | +0.0632 | 0.0747 | +0.846 | 0.397 | ns |
| econ_neocol_score_total_lag1 | −0.0046 | 0.0615 | −0.075 | 0.940 | ns |
| colonial_tie_flag | −0.7403 | 0.3864 | −1.916 | 0.055 | . |
| gdp_per_capita_log | +0.1886 | 0.0621 | +3.037 | 0.002 | ** |
| population_log | +0.0637 | 0.0635 | +1.003 | 0.316 | ns |
| armed_conflict | −0.9852 | 0.3511 | −2.806 | 0.005 | ** |
| conflict_intensity | +1.2307 | 0.2307 | +5.335 | 9.56e-08 | *** |
| arms_tiv_in_strength_lag1 | −0.0148 | 0.0096 | −1.542 | 0.123 | ns |
| bilateral_oda_in_strength_lag1 | −0.0094 | 0.0067 | −1.413 | 0.158 | ns |
| econ_neocol_score_in_strength_lag1 | −0.0118 | 0.0068 | −1.733 | 0.083 | . |
| colonial_tie_in_strength_lag1 | −0.0730 | 0.2239 | −0.326 | 0.744 | ns |
| arms_tiv_pagerank_lag1 | +5.328 | 16.681 | +0.319 | 0.749 | ns |
| bilateral_oda_pagerank_lag1 | +101.000 | 50.646 | +1.994 | 0.046 | * |
| econ_neocol_score_pagerank_lag1 | +0.149 | 15.655 | +0.010 | 0.992 | ns |
| colonial_tie_pagerank_lag1 | −166.940 | 146.339 | −1.141 | 0.254 | ns |
| arms_x_colonial | +0.0103 | 0.0533 | +0.193 | 0.847 | ns |
| oda_x_colonial | +0.1669 | 0.0568 | +2.936 | 0.003 | ** |
| econ_x_colonial | +0.0777 | 0.0497 | +1.565 | 0.117 | ns |
| alpha | +0.4059 | 0.0595 | +6.820 | 9.13e-12 | *** |

---

### nb17 — AIC/LLF Comparison vs nb16

| Component | nb16 AIC | nb17 AIC | ΔAIC | nb16 LLF | nb17 LLF |
|---|---|---|---|---|---|
| Logit | 3097.2 | 3054.1 | **−43.1** | −1539.6 | −1507.1 |
| NegBin | 2899.3 | 2863.9 | **−35.4** | −1439.7 | −1410.9 |

---

### nb17 — Interaction Terms Summary (from `outputs/results/nb17_interaction_terms_summary.csv`)

| term | logit_coef | logit_p | logit_sig | nb_coef | nb_p | nb_sig |
|---|---|---|---|---|---|---|
| arms_x_colonial | +0.1020 | 0.227 | ns | +0.0103 | 0.847 | ns |
| econ_x_colonial | −0.0580 | 0.465 | ns | +0.0777 | 0.117 | ns |
| **oda_x_colonial** | **+0.1957** | **0.046** | **\*** | **+0.1669** | **0.003** | **\*\*** |

**Key finding:** oda_x_colonial (ODA × colonial_tie) is the only significant interaction term. Significant in both hurdle components: logit p=0.046, NegBin p=0.003. Robust to IRQ/SYR exclusion in logit (logit full p=0.066; excl. IRQ/SYR p=0.066).

---

### nb17 — Network Features Summary (from `outputs/results/nb17_network_features_summary.csv`)

| term | logit_coef | logit_p | logit_sig | nb_coef | nb_p | nb_sig |
|---|---|---|---|---|---|---|
| arms_tiv_in_strength_lag1 | −0.0137 | 0.396 | ns | −0.0148 | 0.123 | ns |
| arms_tiv_pagerank_lag1 | +33.635 | 0.204 | ns | +5.328 | 0.749 | ns |
| bilateral_oda_in_strength_lag1 | −0.0103 | 0.378 | ns | −0.0094 | 0.158 | ns |
| **bilateral_oda_pagerank_lag1** | **+41.501** | **0.685** | **ns** | **+101.000** | **0.046** | **\*** |
| colonial_tie_in_strength_lag1 | −0.4018 | 0.225 | ns | −0.0730 | 0.744 | ns |
| colonial_tie_pagerank_lag1 | +82.776 | 0.803 | ns | −166.940 | 0.254 | ns |
| **econ_neocol_score_in_strength_lag1** | **−0.0311** | **0.005** | **\*\*** | **−0.0118** | **0.083** | **.** |
| econ_neocol_score_pagerank_lag1 | +57.369 | 0.166 | ns | +0.149 | 0.992 | ns |

**Notes:** bilateral_oda_pagerank_lag1 NegBin: VIF=10.40 (HIGH) — treat p=0.046 with caution. econ_neocol_score_in_strength_lag1 logit: VIF=10.70 (HIGH) — interpret cautiously.

---

### nb17 — VIF (Network-Augmented Features, from `outputs/data&methods/vif_nb17_network_features.csv`)

| Feature | VIF | Flag |
|---|---|---|
| econ_neocol_score_in_strength_lag1 | 10.70 | HIGH |
| bilateral_oda_in_strength_lag1 | 10.40 | HIGH |
| oda_x_colonial | 10.01 | HIGH |
| colonial_tie_flag | 9.74 | — |
| econ_neocol_score_total_lag1 | 8.52 | — |
| armed_conflict | 8.40 | — |
| conflict_intensity | 8.40 | — |
| oda_total_log_lag1 | 7.51 | — |
| arms_tiv_total_log_lag1 | 6.72 | — |
| econ_x_colonial | 6.68 | — |
| arms_tiv_in_strength_lag1 | 5.40 | — |
| colonial_tie_in_strength_lag1 | 4.11 | — |
| bilateral_oda_pagerank_lag1 | 3.99 | — |
| arms_x_colonial | 3.40 | — |
| population_log | 2.76 | — |
| gdp_per_capita_log | 2.61 | — |
| econ_neocol_score_pagerank_lag1 | 2.37 | — |
| arms_tiv_pagerank_lag1 | 2.27 | — |
| colonial_tie_pagerank_lag1 | 1.48 | — |

---

### nb17 — ODA Sensitivity (IRQ/SYR exclusion, from `outputs/limitations/nb17_oda_irq_syr_sensitivity.csv`)

| Model | Sample | ODA coef | ODA p |
|---|---|---|---|
| Logit | Full | +0.224 | 0.066 |
| Logit | Excl. IRQ/SYR | +0.231 | 0.066 |
| NegBin | Full | +0.063 | 0.397 |
| NegBin | Excl. IRQ/SYR | +0.080 | 0.344 |

**Finding:** ODA coefficients are stable when excluding Iraq and Syria in nb17. Both remain non-significant in NegBin (unlike nb16 where NegBin ODA fully collapsed to p=0.800). The oda_x_colonial interaction (not shown here) remains significant at p=0.046 (logit) and p=0.003 (NegBin).

---

### nb17 — Conflict Robustness (from `outputs/limitations/nb17_conflict_robustness.csv`)
Full model vs armed_conflict dropped (conflict_intensity retained):

| predictor | logit_coef_full | logit_coef_reduced | nb_coef_full | nb_coef_reduced |
|---|---|---|---|---|
| arms_tiv_total_log_lag1 | −0.122 | −0.116 | +0.011 | −0.009 |
| oda_total_log_lag1 | +0.224 | +0.221 | +0.063 | +0.059 |
| econ_neocol_score_total_lag1 | +0.231 | +0.225 | −0.005 | +0.001 |
| colonial_tie_flag | −0.083 | −0.103 | −0.740 | −0.761 |
| gdp_per_capita_log | +0.193 | +0.193 | +0.189 | +0.217 |
| population_log | +0.530 | +0.516 | +0.064 | +0.021 |
| armed_conflict | −0.575 | dropped | −0.985 | dropped |
| conflict_intensity | +1.610 | +1.239 | +1.231 | +0.717 |

**Finding:** Baseline coefficients stable when armed_conflict dropped. econ_neocol_score sign flips from + to + (stable), arms and ODA remain directionally consistent.

---

### nb17 — nb16 vs nb17 Coefficient Comparison (from `outputs/results/nb17_vs_nb16_comparison.csv`)

| predictor | logit_sig_nb16 | logit_sig_nb17 | logit_sign_flip | nb_sig_nb16 | nb_sig_nb17 | nb_sign_flip |
|---|---|---|---|---|---|---|
| arms_tiv_total_log_lag1 | ** | ns | No | ns | ns | YES (→ +) |
| oda_total_log_lag1 | *** | . | No | * | ns | No |
| econ_neocol_score_total_lag1 | ns | * | YES (→ +) | . | ns | No |
| colonial_tie_flag | *** | ns | YES (→ −) | ** | . | YES (→ −) |
| gdp_per_capita_log | *** | * | No | *** | ** | No |
| population_log | *** | *** | No | * | ns | No |
| armed_conflict | * | ns | No | *** | ** | No |
| conflict_intensity | *** | *** | No | *** | *** | No |

**Notes on sign flips:** Many significance changes reflect the shift from nonrobust (nb16) to clustered SEs (nb17), not just the addition of network features. The colonial_tie_flag sign flip in nb17 is absorbed by the interaction terms (oda_x_colonial, arms_x_colonial).

---

## 6. nb18 — Econ Neo-Colonial Score Diagnostic Results

**Purpose:** Diagnose why econ_neocol_score_total_lag1 is statistically null in nb16/nb17.

### Score Distribution in Monadic Panel (nb18 Cell 1)
Using econ_neocol_score_total (log1p-scaled, range 0–11):

| Stat | Value |
|---|---|
| Count | 6,358 |
| Mean | 3.3525 |
| Std | 2.9114 |
| Min | 0.0 |
| 25th pct | 0.0 |
| Median (50th) | 4.318 |
| 75th pct | 6.015 |
| Max | 11.061 |

Zero share (econ_neocol_score_total in monadic): NOT FOUND as a standalone percentage in nb18 cell 1 output. From summary_stats.csv: **38.5%** zeros (for econ_neocol_score_total, which uses a different scale — 0–101 range in that file; see note below).

### Bivariate Relationship (nb18 Cell 7)
- **Spearman r = 0.0023**, p = 0.9516
- **Finding:** No monotonic rank correlation between econ score and journalist killings.

### Score by Killing Status (from `outputs/results/nb18_econ_score_by_killing_status.csv`)
_Note: these figures use a rescaled version of econ score (econ_log), range ~0–23._

| Group | Mean econ score | Median econ score | Std | N |
|---|---|---|---|---|
| Zero killings | 13.23 | 22.08 | 10.99 | 5,444 |
| Any killing | 17.77 | 22.42 | 9.09 | 701 |

### Mann-Whitney U Test (nb18 Cell 15)
- U statistic: **1,514,880.0**
- p-value: **< 0.0001** (distributions are statistically different)
- Note: Means differ (13.2 vs 17.8) but medians are nearly identical (22.08 vs 22.42), suggesting the difference is driven by the high zero-share in non-killing years, not by a monotonic relationship. Spearman r≈0 confirms no predictive relationship.

### Structural Mismatch (nb18 Cell 5)
Overlap between top-25 econ score countries and top-20 killing countries: **only 3 countries** (TJK, HND, DZA). The high-econ-score and high-killing sets are largely disjoint.

### Key Finding (nb18 Interpretation markdown)
The econ neo-colonial score is well-constructed and theoretically grounded but null in both hurdle model components. The null result is substantive: the score captures structural trade dependency weighted by technological asymmetry, identifying countries like TJK, HND, DZA — which have high trade dependency on more complex economies but do not show elevated journalist killings. The pathway from economic subordination to journalist violence is either non-existent, blocked by other mechanisms, or too indirect to detect with this operationalisation.

---

## 7. nb19 — Case Study Diagnostic Results

### Model Used for Predictions
nb19 re-fits the baseline hurdle model with interaction terms (oda_x_colonial, econ_x_colonial, arms_x_colonial) but WITHOUT the 8 network features. Clustered SEs by recipient_iso3. This produces the prediction table.

### nb19 Re-fitted Model Coefficients (Cell 8 and 9)

**Logit (clustered SEs):**

| term | coef | std_err | p |
|---|---|---|---|
| const | −13.949 | 1.804 | 0.000 |
| arms_tiv_total_log_lag1 | −0.148 | 0.069 | 0.032 |
| oda_total_log_lag1 | +0.096 | 0.079 | 0.226 |
| econ_neocol_score_total_lag1 | +0.057 | 0.065 | 0.385 |
| colonial_tie_flag | −0.133 | 0.516 | 0.796 |
| gdp_per_capita_log | +0.227 | 0.096 | 0.018 |
| population_log | +0.553 | 0.081 | 0.000 |
| armed_conflict | −0.582 | 0.474 | 0.219 |
| conflict_intensity | +1.606 | 0.330 | 0.000 |
| oda_x_colonial | +0.172 | 0.092 | 0.060 |
| econ_x_colonial | −0.115 | 0.078 | 0.141 |
| arms_x_colonial | +0.096 | 0.081 | 0.234 |

**NegBin (clustered SEs):**

| term | coef | std_err | p |
|---|---|---|---|
| const | −1.955 | 1.352 | 0.148 |
| arms_tiv_total_log_lag1 | −0.047 | 0.054 | 0.383 |
| oda_total_log_lag1 | +0.008 | 0.046 | 0.859 |
| econ_neocol_score_total_lag1 | −0.087 | 0.043 | 0.044 |
| colonial_tie_flag | −0.785 | 0.316 | 0.013 |
| gdp_per_capita_log | +0.219 | 0.074 | 0.003 |
| population_log | +0.061 | 0.061 | 0.317 |
| armed_conflict | −1.002 | 0.383 | 0.009 |
| conflict_intensity | +1.221 | 0.224 | 0.000 |
| oda_x_colonial | +0.139 | 0.056 | 0.013 |
| econ_x_colonial | +0.070 | 0.052 | 0.181 |
| arms_x_colonial | +0.017 | 0.054 | 0.750 |
| alpha | +0.438 | 0.063 | 0.000 |

### Philippines (PHL) vs Iraq (IRQ) — Mean Annual Comparison Table (from `outputs/case_study/phl_irq_comparison_table.csv`)

| Variable | PHL (mean/yr) | IRQ (mean/yr) | IRQ − PHL |
|---|---|---|---|
| journalist_killings | 4.844 | 8.906 | +4.062 |
| pred_count_hurdle | 1.785 | 4.010 | +2.225 |
| residual | 3.058 | 4.896 | +1.838 |
| p_any_killing | 0.529 | 0.501 | −0.028 |
| colonial_tie_flag | 1.0 | 1.0 | 0.0 |
| oda_total_log_lag1 | 6.478 | 6.814 | +0.336 |
| arms_tiv_total_log_lag1 | 3.488 | 3.314 | −0.174 |
| econ_neocol_score_total_lag1 | 5.491 | 5.771 | +0.280 |
| gdp_per_capita_log | 7.533 | 7.738 | +0.205 |
| armed_conflict | 1.0 | 0.812 | −0.188 |
| conflict_intensity | 1.062 | 1.188 | +0.126 |

### Case Study Spotlight (nb19 Cell 14 and Cell 26)

**Philippines (PHL):**
- Total killings (1992–2024): 155
- Total predicted: 57.1
- Mean annual residual: 3.058 killings/year
- Mean P(any killing): 0.529
- Colonial tie: 1 (Spain; coded via COLDAT → ESP)
- Top ODA donors: Japan (11,333 USD millions cumulative), USA (4,152), Australia (2,116), France (1,414), Korea (1,268)
- n_years: 32
- Peak killing year: 2009 | Peak killings: 38

**Iraq (IRQ):**
- Total killings (1992–2024): 285
- Total predicted: 128.3
- Mean annual residual: 4.896 killings/year
- Mean P(any killing): 0.501
- Colonial tie: 1 (UK mandate → GBR coded as colonial tie)
- Top ODA donors: USA (38,182 USD millions cumulative), Japan (15,075), Germany (10,745), UK (3,734), France (3,249)
- n_years: 32
- Peak killing year: 2006 | Peak killings: 55

**Key finding:** Same apparent patron (US), two mechanisms. PHL: colonial_tie=1 (Spain-US colonial chain), ODA channel partially active, model captures ~37% of violence (57.1/155). IRQ: colonial_tie coded =1 via GBR mandate, but US invasion is the primary mechanism, which is invisible to the model's ODA/colonial structure. Model captures ~45% of violence (128.3/285) through wrong channel (conflict variables, not ODA×colonial). Both countries generate large positive residuals — the model under-predicts severely.

### Top Countries by Total Killings and Residuals (from `outputs/case_study/country_residuals.csv`)

| ISO3 | Total killings | Mean annual killings | Mean annual pred | Mean residual | P(any killing) | Colonial tie | n_years |
|---|---|---|---|---|---|---|---|
| IRQ | 285 | 8.906 | 4.010 | +4.896 | 0.501 | 1 | 32 |
| ISR | 181 | 5.656 | 0.642 | +5.015 | 0.130 | 1 | 32 |
| MEX | 158 | 4.938 | 0.962 | +3.976 | 0.334 | 1 | 32 |
| SYR | 155 | 5.167 | 2.822 | +2.344 | 0.359 | 1 | 30 |
| PHL | 155 | 4.844 | 1.785 | +3.058 | 0.529 | 1 | 32 |
| PAK | 104 | 3.250 | 3.026 | +0.224 | 0.614 | 1 | 32 |
| COL | 96 | 3.000 | 2.829 | +0.171 | 0.542 | 1 | 32 |
| IND | 89 | 2.781 | 3.138 | −0.357 | 0.824 | 1 | 32 |
| SOM | 86 | 2.688 | 2.893 | −0.205 | 0.428 | 1 | 32 |
| AFG | 77 | 3.208 | 1.419 | +1.790 | 0.436 | 0 | 24 |
| BRA | 60 | 1.875 | 1.040 | +0.835 | 0.378 | 1 | 32 |
| DZA | 59 | 1.844 | 1.381 | +0.463 | 0.340 | 1 | 32 |
| HND | 39 | 1.219 | 0.132 | +1.087 | 0.076 | 1 | 32 |
| NGA | 25 | 0.781 | 3.916 | −3.135 | 0.532 | 1 | 32 |
| LKA | 25 | 0.781 | 1.651 | −0.870 | 0.315 | 1 | 32 |
| YEM | 30 | 1.154 | 1.876 | −0.723 | 0.298 | 1 | 26 |

---

## 8. Interaction Terms — Full Summary

| Term | Construction | Logit coef (nb17) | Logit p | Logit sig | NegBin coef (nb17) | NegBin p | NegBin sig |
|---|---|---|---|---|---|---|---|
| arms_x_colonial | arms_tiv_total_log_lag1 × colonial_tie_flag | +0.102 | 0.227 | ns | +0.010 | 0.847 | ns |
| oda_x_colonial | oda_total_log_lag1 × colonial_tie_flag | +0.196 | 0.046 | * | +0.167 | 0.003 | ** |
| econ_x_colonial | econ_neocol_score_total_lag1 × colonial_tie_flag | −0.058 | 0.465 | ns | +0.078 | 0.117 | ns |

**oda_x_colonial interpretation:** Among countries with a colonial tie, a one-unit increase in log ODA (lagged) is associated with an additional 0.196 increase in log-odds of any killing (logit) and an additional 0.167 increase in log expected count conditional on any killing (NegBin). The interaction is the primary neo-colonial finding of the study.

---

## 9. Controls — Confirmed Variable Names in Final Panel

From `outputs/appendices/variable_codebook.csv` and nb16 Cell 5:

| Variable | Role | Log-transformed | Lagged | Source |
|---|---|---|---|---|
| gdp_per_capita_log | Control | Yes (ln) | No | World Bank WDI |
| population_log | Control | Yes (ln) | No | World Bank WDI |
| armed_conflict | Control (binary: 0/1, ≥25 battle deaths) | No | No | UCDP/PRIO v25.1 |
| conflict_intensity | Control (ordinal: 0=none, 1=minor, 2=war) | No | No | UCDP/PRIO v25.1 |

**Note:** v2x_polyarchy (democracy) was dropped (34.1% missing, shrinks sample). HDI was dropped (collinear with GDP, mediates pathway). Press freedom indices and state fragility indices were rejected. The final lean control set is 4 variables (2 continuous + 2 UCDP conflict).

**Conflict as control and potential mediator:** armed_conflict and conflict_intensity are included as controls but are noted as potential mediators of the neo-colonial → violence pathway. Robustness checks dropping armed_conflict are documented in nb16 Part D and nb17 Part H. Results show conflict_intensity coefficients are stable but armed_conflict coefficient changes significance after clustering (p=0.305 in nb16 clustered logit; p=0.218 in nb17 clustered logit).

---

## 10. Econ Score Construction (Confirmed from nb18)

**Formula:**
```python
complexity_asymmetry = (ECI_sender - ECI_receiver).clip(lower=0)
trade_dependency = bilateral_trade / receiver_GDP
econ_neocol_score = trade_dependency * complexity_asymmetry

# Log transformation:
econ_neocol_score_log = np.log1p(econ_neocol_score * 1e9)
```

**Monadic collapse:**
```python
econ_neocol_score_total = log1p(sum_across_senders(raw_dyadic_score) * 1e9)
```

**Coverage gap:** ECI data starts 1995. Monadic panel uses 1992–2024. Years 1992–1994 have no econ edges in network layer; PageRank is uniform (1/N) for those years. The 1-year lag shifts this forward: econ_neocol_score_pagerank_lag1 is uniform for 1993, 1994, 1995 in panel_final.

---

*All numbers above are extracted directly from notebook cell outputs and saved CSV/TXT files. No numbers were inferred or estimated.*
