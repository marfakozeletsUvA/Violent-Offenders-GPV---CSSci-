# Audit Report — GPV: Violent Offenders
**Date:** 2026-05-29  
**Auditor:** Claude Code (automated audit)  
**Scope:** Full repository, notebooks nb02–nb22, all data files, all outputs  

---

## 1. Repo Inventory

### 1.1 Notebooks

| Notebook | Status | Notes |
|---|---|---|
| `02_country_standardization.ipynb` | Active | ISO3 standardisation; stale file paths (see §2.1) |
| `03_eda.ipynb` | Active | EDA on raw data; reads from deprecated paths |
| `04_eda_merged.ipynb` | Active | EDA on merged dyadic panel |
| `05_controls_preprocessing.ipynb` | Active | Builds `controls_merged.csv`; v2x_polyarchy included |
| `06_oecd_dac2_oda_fixing.ipynb` | Active | ODA duplicate fix |
| `07_trade_dependency_engineering_DEPRECATED.ipynb` | **Deprecated** | Replaced by ECI-based score |
| `08_econ_neocol_score.ipynb` | Active | Builds `econ_neocol_score.csv` |
| `09_transform_oda_values.ipynb` | **STALE PATHS** | Reads `panel_with_controls_1992_2024.csv` (renamed) |
| `10_final_panel_eda.ipynb` | Active | Panel EDA |
| `11_network_construction.ipynb` | Active | Builds `network_measures_1992_2024.csv` with pre-lagged centrality |
| `12_collapse_monadic_panel.ipynb` | Active | Dyadic → monadic collapse; also does file renames |
| `13_robustness_variants.ipynb` | Active | 5-yr arms stock + econ score mean variants |
| `14_final_panel_merge.ipynb` | Active | Final merge → `panel_final_1992_2024.csv`; adds lags |
| `15_network_diagnostics.ipynb` | Active | Pre-modelling diagnostics |
| `16_baseline_hurdle_model.ipynb` | Active | Hurdle model, non-robust SEs for main results |
| `17_network_augmented_hurdle_model.ipynb` | Active | Hurdle model, clustered SEs |
| `18_econ_neocol_score_diagnostic.ipynb` | Active | **Not in CLAUDE.md table** |
| `19_case_study_diagnostic.ipynb` | Active | PHL vs IRQ case study |
| `20_gephi_export.ipynb` | Active | **Not in CLAUDE.md table** |
| `21_econ_neocol_score_variance_audit.ipynb` | Active | **Not in CLAUDE.md table** |
| `22_temporal_train_test_validation.ipynb` | Active | Temporal split; baseline model only (not nb17) |

**Missing from numbered sequence:** No `nb01`. The notebook that builds the initial dyadic panel (`panel_with_controls_1992_2024.csv`) from raw SIPRI / ODA / ECI / COLDAT / controls sources is **absent from the repo**. See §6 (Reproducibility, Critical).

**Notebooks absent from CLAUDE.md table:** nb18, nb20, nb21, nb22.

**Raw exploration notebooks** (in `notebooks/raw-data-exploration/`): active v2/v3 IMF trade explorations; 5 deprecated in subdirectory. These are exploratory only, not pipeline.

**Helper scripts:**
- `notebooks/build_country_data.py` — generates `country_stats.json`
- `notebooks/generate_final_report_figures.py` — figure generation
- `notebooks/generate_report_outputs.py` — output generation

---

### 1.2 Data files

| Path | Role | Status |
|---|---|---|
| `data/raw/` | Original unmodified sources | OK |
| `data/processed/sipri_trade_register.csv` | Pipeline input | OK |
| `data/processed/oecd_dac2_oda.csv` | Pipeline input | OK |
| `data/processed/econ_neocol_score.csv` | Pipeline intermediate | OK (115,640 × 10) |
| `data/processed/coldat_colonial_ties.csv` | Pipeline input | OK; no `colonizer_iso3` column (see §2.4) |
| `data/processed/controls/controls_merged.csv` | Pipeline input | OK; v2x_polyarchy present (34.1% missing) but not carried into final panel |
| `data/processed/target_journalist_killings.csv` | Pipeline input | OK (763 × 4) |
| `data/processed/v3_imf_trade.csv` | **Misplaced** | Should be in `data/processed/ignore/` per current structure |
| `data/processed/ignore/` | Dropped sources | OK |
| `data/processed/deprecated/` | Deprecated outputs | OK |
| `data/merged/dyadic_panel_1992_2024_oda_capped_log.csv` | **Primary dyadic panel** | OK (115,640 × 15) |
| `data/merged/dyadic_panel_1992_2024_oda_capped.csv` | Intermediate | OK |
| `data/merged/dyadic_panel_1992_2024_pre_oda_floor.csv` | Pre-floor snapshot | OK |
| `data/merged/panel_monadic_1992_2024.csv` | Collapsed panel | OK (6,358 × 13) |
| `data/merged/panel_monadic_enriched_1992_2024.csv` | Robustness side-branch | OK (6,358 × 15) |
| `data/merged/network_measures_1992_2024.csv` | Network centrality | OK (6,526 × 22) — 168 extra rows (see §2.2) |
| `data/merged/panel_final_1992_2024.csv` | **Primary modelling input** | OK (6,358 × 38) |

---

### 1.3 Outputs

| Path | Contents | Status |
|---|---|---|
| `outputs/final_report/01_data_and_methods/` | fig01–fig03 | 3 PNG present |
| `outputs/final_report/02_results_main_findings/` | fig04–fig07 | 4 PNG present |
| `outputs/final_report/03_results_econ_score/` | fig08–fig09 | 2 PNG present |
| `outputs/final_report/04_appendix/` | figa01–figa07 + 7 audit figures | 14 PNG present |
| `outputs/final_report/05_tables/` | table01–table05 | 5 PNG present |
| `outputs/final_report/06_case_study/` | 4 figures + 2 CSVs | OK |
| `outputs/gephi/inputs/` | 9 CSV input files | OK; arms animation has wrong column (see §5) |
| `outputs/gephi/outputs/` | 3 PNG + 3 SVG renders | OK |
| `outputs/gephi/gephi_projects/` | 4 .gephi files | OK |
| `outputs/models/` | 4 PKL files (nb16+nb17) | OK |
| `outputs/results/` | nb16/nb17 coefficient CSVs, metrics, nb22 validation | OK |
| `outputs/limitations/` | sensitivity figures | OK |
| **`gpv_presentation.html`** | **NOT FOUND** | Absent from repo (see §5) |

**No `requirements.txt` or `environment.yml` found anywhere in the repo.**

---

## 2. Data Pipeline Audit

### 2.1 Merge Keys

**ISO3 identifiers are used consistently throughout the pipeline.** The nb02 country standardisation uses `pycountry` with a manual mapping dictionary to convert all source-specific country names (including COLDAT lowercase colonizer names: `britain`, `belgium`, etc.) to ISO3. Kosovo is handled via special code `XKX`.

**Flag — STALE PATHS (MODERATE):**  
`nb02` reads from paths like `PROCESSED / "military" / "sipri_trade_register.csv"`, `PROCESSED / "target" / "target_journalist_killings.csv"`, etc. These subdirectory structures no longer exist. Current files are at `data/processed/sipri_trade_register.csv` etc. **nb02 cannot be re-run as-is.**

**Flag — STALE PATHS (CRITICAL):**  
`nb09` reads from `../data/merged/panel_with_controls_1992_2024.csv` (pre-ODA-floor version) and `../data/merged/panel_with_controls_1992_2024-ODACAPPED.csv`. Both were renamed in nb12 to `dyadic_panel_1992_2024_pre_oda_floor.csv` and `dyadic_panel_1992_2024_oda_capped.csv`. **nb09 cannot be re-run as-is.**

### 2.2 Row Counts

| Step | Rows | Notes |
|---|---|---|
| Raw dyadic panel (primary) | 115,640 | 15 cols |
| Network measures | 6,526 | 22 cols; 168 more rows than monadic |
| Monadic panel | 6,358 | 13 cols; nb12 inner join collapses recipient-year |
| Final panel (after nb14 inner join) | 6,358 | 38 cols; assertion in place |
| Model analytical sample (after dropna) | 5,765 | 593 dropped (9.3%) |
| Count component (NB, non-zero) | 687 | 11.9% of model sample |

**The 168 extra country-years in `network_measures_1992_2024.csv`** are countries that appear as senders/network nodes but have no recipient-role rows in the monadic panel (e.g., ISL, LUX, IRL, BGR, CHE). The inner join in nb14 correctly excludes these. The discrepancy is expected but should be documented.

**Row count is stable across all joins.** Assertions in nb12 and nb14 would catch unexpected row loss on re-run. No unexpected drops observed.

**Years in model sample:** 1993–2024 (first year 1992 lost due to 1-year lag). This is correct behaviour.

### 2.3 Leakage Risk

**No leakage detected.** All right-hand-side predictors are lagged by 1 year:

- **Flow variables** (`arms_tiv_total_log_lag1`, `oda_total_log_lag1`, `econ_neocol_score_total_lag1`): lagged in nb14 via `groupby('recipient_iso3')[col].shift(1)` after `sort_values(['recipient_iso3', 'year'])`. Correct.
- **Network measures**: lagged in nb11 via `groupby('country')[col].shift(1)` after `sort_values(['country', 'year'])`. Correct. All network columns in the final panel carry the `_lag1` suffix.
- **`colonial_tie_flag`**: time-invariant binary, no lag needed or possible.
- **Controls** (`gdp_per_capita_log`, `population_log`, `armed_conflict`, `conflict_intensity`): **contemporaneous** with DV. This is a deliberate modelling choice (GDP and conflict level in year t controls for country wealth/stability in that year). Theoretical justification should be stated explicitly in the paper — contemporaneous controls do not create leakage in political science panel models but reviewers may flag it.
- **`econ_neocol_score_total_lag1`**: lagged version of the already-log-transformed monadic total. The naming is slightly confusing (see §2.9) but construction is correct.

### 2.4 COLDAT — Colonial Network Variable

**Structure:** 160 unique colonizer–colony pairs across 8 colonizers (belgium→BEL, britain→GBR, france→FRA, germany→DEU, netherlands→NLD, portugal→PRT, spain→ESP, italy→ITA).

**Binary variable:** `colonial_tie` = 1 fires on 4,367 dyad-years (3.8% of 115,640), matching 160 unique sender-recipient pairs × available years. Aggregated to `colonial_tie_flag` = 1 if any sender was a colonial power for that recipient.

**Flag — NO `colonizer_iso3` IN PROCESSED FILE (MINOR):**  
`data/processed/coldat_colonial_ties.csv` contains only `colony_iso3`, not `colonizer_iso3`. The colonizer → ISO3 mapping is implicit in nb02's `get_iso3()` function. The ISO3 mapping works correctly (verified: 4,367 colonial dyad-years ÷ 160 pairs is consistent with available panel years). However, the processed file should store `colonizer_iso3` explicitly for audit transparency.

**`oda_x_colonial` construction:** `oda_total_log_lag1 × colonial_tie_flag` — constructed in nb17 at fit time, not stored in `panel_final`. Construction is correct (standard multiplicative interaction). No clipping applied (correct — ODA is log-transformed and colonial_tie is binary 0/1).

**Iraq COLDAT note:** `colonial_tie_flag=1` for Iraq because GBR (British Mandate 1920–32) is in COLDAT. USA is not a COLDAT colonizer of Iraq, so the ODA×colonial interaction captures UK influence, not the 2003 US invasion. This is a structural limitation, not a data error (correctly documented in nb19/CLAUDE.md).

### 2.5 econ_neocol_score Construction

**Formula verified:** `econ_neocol_score = trade_dependency × complexity_asymmetry`, where `complexity_asymmetry = (ECI_sender − ECI_receiver).clip(lower=0)`.

- **No negative values** in `econ_neocol_score`: confirmed (0 negative values).
- **Complexity asymmetry clipped correctly**: 0 negative values confirmed; range 0–5.47.
- **Non-zero for non-colonial dyads (73,555 cases):** correct — econ score is independent of colonial tie. North-North dyads auto-zero only when sender ECI ≤ receiver ECI.
- **Log transformation:** `log1p(econ_neocol_score × 1e9)` applied; range 0–11, 38.5% zeros. Correct.

### 2.6 SIPRI Arms — Aggregation Check

- `arms_tiv_total` = sum of incoming TIV across all senders per recipient-year.
- 43.2% zeros (no incoming arms that year). This is expected — most countries receive no arms transfers in most years.
- Log transform: `arms_tiv_total_log = log1p(arms_tiv_total)`. Then lagged.
- **Model variable:** `arms_tiv_total_log_lag1` — confirmed correct in baseline_features list.

### 2.7 Missing Data in Final Panel

All missing percentages are within acceptable range (<15%) for modelling:

| Column | Missing % | Flag |
|---|---|---|
| `gdp_per_capita` / `_log` | **6.35%** | Acceptable; highest of controls |
| `population` / `_log` | 4.22% | OK |
| `armed_conflict` / `conflict_intensity` | 3.70% | OK |
| All `_lag1` columns | 3.27–3.35% | Expected (first year per country) |
| All other columns | 0% | OK |

**Forbidden variables confirmed absent from final panel:** `v2x_polyarchy`, `bilateral_debt`, `hdi`, `press_freedom` — all confirmed not present.

**`v2x_polyarchy` in `controls_merged.csv` (34.1% missing):** Present in the intermediate controls file but correctly excluded from all downstream merges and modelling. Not a data error but may confuse readers inspecting intermediate files.

### 2.8 ODA Floor

**Confirmed:** No negative `bilateral_oda` values in dyadic panel (verified). ODA floor applied correctly in nb09.

### 2.9 Naming Ambiguity (MINOR)

`econ_neocol_score_total` in the monadic/final panel is the **log-transformed** version (`log1p(sum_raw × 1e9)`), not the raw total. The `_total` suffix implies aggregation but not transformation. Readers may expect a raw total and a separate `_log` column (as exists for arms and ODA). The CLAUDE.md documents this correctly but the column name in the dataset is potentially misleading.

---

## 3. Modelling Audit (nb16–nb17)

### 3a. Specification

**nb16 — Baseline hurdle model:**
- 8 baseline features (3 neo-colonial lags + colonial_tie_flag + 4 controls)
- Logit (any killing) + NegBin (count | killing > 0) — correctly separated
- SEs: **non-robust (standard MLE)** in main results; clustered SE comparison computed in cell 11 but not used as headline
- No country fixed effects; no year fixed effects — pooled specification

**nb17 — Network-augmented hurdle model:**
- 8 baseline + 8 network centrality + 3 interaction features (16 predictors + 3 interactions)
- Interaction terms constructed at fit time: `oda_x_colonial = oda_total_log_lag1 × colonial_tie_flag` etc.
- SEs: **clustered by `recipient_iso3`** throughout — correct for T=33 panel
- No country fixed effects; no year fixed effects — pooled

**Flag — NO FIXED EFFECTS (MODERATE):**  
Both models are pooled GLMs without country or year fixed effects. Country FE would control for time-invariant unobserved heterogeneity (e.g., press culture, political system type) but would also sweep out the time-invariant `colonial_tie_flag`. Year FE would control for global trends. The pooled specification is a deliberate design choice but must be explicitly justified in the write-up. A reviewer is likely to raise this; prepare a response.

**Note:** Country FE would eliminate `colonial_tie_flag` (perfectly collinear with country in a balanced panel), so the FE choice and the colonial_tie identification strategy are in tension — using a within-country estimator is not possible for this specific variable.

### 3b. Train-Test Split

**Flag — IN-SAMPLE AUC NOT LABELLED (MODERATE):**  
AUC 0.857 reported in nb16 and nb17 is **in-sample** (computed on the same 5,765 rows used to fit the model). Both notebooks compute:  
```python
logit_probs = logit_result.predict(X_logit)  # X_logit is the training data
logit_auc = roc_auc_score(y_logit, logit_probs)
```
This is not a bug given that `nb22` exists and performs temporal validation, but the AUC as reported in model summaries and figures (fig07, nb17_roc_curve.png) is in-sample. It should be clearly labelled.

**nb22 temporal validation results (baseline model only):**

| Metric | Value |
|---|---|
| In-sample AUC (nb16 full model, 1992–2024) | 0.8570 |
| Train AUC (1992–2015) | 0.8503 |
| OOS AUC (2016–2024) | **0.8576** |
| AUC degradation | −0.0073 (negative = OOS slightly *higher*) |
| NegBin OOS Spearman r | 0.425 |
| Sign flips (logit coefs) | 0 |

The temporal validation result is reassuring — no overfitting detected, no sign flips. **However, nb22 only validates the baseline 8-feature model.** The network-augmented model (nb17, 19 predictors) has no out-of-sample evaluation. Given the high VIFs and 3 significant covariates out of 19, this gap should be addressed or acknowledged.

**Train/test split choice:** 1992–2015 train / 2016–2024 test. This is a reasonable temporal split. Countries in test but not train (cold-start) are flagged in nb22 cell 2.

### 3c. Consistency Checks

**Verified key findings:**

| Claim | Verified | Notes |
|---|---|---|
| `oda_x_colonial` logit p=0.046 | ✓ | p=0.0459 (p<0.05) |
| `oda_x_colonial` NegBin p=0.003 | ✓ | p=0.0033 |
| `econ_neocol_score` NegBin null | ✓ | coef=−0.005, p=0.940 |
| Arms negative in logit | Partial | coef=−0.122 (nb17 logit), p=0.172 — negative direction but not significant |
| AUC 0.857 | ✓ | Confirmed from saved metrics |

**Flag — SIGN FLIPS BETWEEN SPECIFICATIONS (CRITICAL DOCUMENTATION):**

The comparison table (`outputs/results/nb17_vs_nb16_comparison.csv`) shows:

| Feature | nb16 logit | nb17 logit | Flip? | nb16 NB | nb17 NB | Flip? |
|---|---|---|---|---|---|---|
| `econ_neocol_score_total_lag1` | −0.028 (ns) | **+0.231 (p=0.011\*)** | ✓ YES | −0.032 (p=0.051) | −0.005 (ns) | No |
| `colonial_tie_flag` | +0.488 (p<0.001) | −0.083 (ns) | ✓ YES | +0.308 (p=0.002) | −0.740 (p=0.055) | ✓ YES |
| `arms_tiv_total_log_lag1` | −0.033 (ns) | | No | | +0.011 (ns) | ✓ YES |

**Most serious:** `econ_neocol_score_total_lag1` reverses from null-negative in nb16 to **significant-positive** in the nb17 logit. CLAUDE.md attributes this to collinearity (VIF=8.52 for econ score; VIF=10.7 for its correlated in-strength counterpart). The table in `outputs/results` flagging this sign flip exists, but the results narrative must address it. As written, CLAUDE.md states "econ_neocol_score null across all specifications" — this is incorrect for the nb17 logit component (p=0.011). The econ score is null only in the NegBin count component.

**`colonial_tie_flag` sign flip (expected):** When interaction terms absorb the main effect, the sign of the main effect can flip (the coefficient now represents the effect at ODA=0). This is standard interaction term behaviour and does not indicate a problem, but should be explained.

**`bilateral_oda_pagerank_lag1` significance in NB:** coef=101.0, p=0.046* (VIF=10.4). This result is driven by near-uniform PageRank values producing extreme coefficient scaling. The result is treated correctly with caution in CLAUDE.md. It should not appear as a substantive finding.

### 3d. Overdispersion and Zero-Inflation

| Statistic | Full panel | Model sample (n=5,765) | CLAUDE.md claim | Match? |
|---|---|---|---|---|
| Zero proportion | 88.7% | 88.1% | "83%+" | **No — 83% is stale** |
| Mean | 0.369 | 0.393 | — | — |
| Var/mean ratio | 14.7x | 15.1x | "~11–16x" | ✓ |
| Max | 82 | 82 | 82 | ✓ |

**Flag — INCORRECT ZERO PROPORTION IN CLAUDE.md (MINOR):**  
CLAUDE.md modelling pipeline section says "83%+ zeros". The actual figure is **88.7%** (full panel) / **88.1%** (model sample). This is an internally inconsistent documentation error. Correct the CLAUDE.md and any paper text that quotes the 83% figure.

**Hurdle vs ZINB justification:** The hurdle model is chosen over ZINB on the theoretical grounds that zeros are structural (countries where journalist killings simply did not occur, not countries where they could occur but didn't). This is a valid theoretical distinction. No formal Vuong test comparing hurdle to ZINB is in the notebooks. Consider adding a brief note in limitations that the Vuong test was not computed, or add it as a robustness check (low priority).

### 3e. Standard Errors

- **nb17:** Clustered by `recipient_iso3` in both components — correct for a panel with T=33 and N≈196.
- **nb16:** Non-robust SEs in the headline results. Clustered SE comparison is computed (cell 11) and saved to `outputs/results/nb16_logit_clustered_se_comparison.csv`, but the main figures and tables use non-robust SEs. **This creates a SE method inconsistency between nb16 (non-robust) and nb17 (clustered)** — the two models cannot be directly compared on significance thresholds. The nb16 results will show artificially tight confidence intervals relative to nb17.
- **Recommended:** Either (a) promote nb16's clustered SE results as the headline, or (b) clearly label in the paper that nb16 uses non-robust SEs and nb17 uses clustered SEs.

---

## 4. Case Study Notebook (nb19)

### 4a. Residual Computation

Residuals are computed as:
```python
model_df['pred_count_hurdle']  = model_df['p_any_killing'] * model_df['pred_count_nonzero']
model_df['residual']           = model_df['journalist_killings'] - model_df['pred_count_hurdle']
```
This is the **hurdle-combined prediction** (probability × NegBin mean), not the NegBin component alone. The residual is thus the difference between observed kills and the hurdle model's joint expected value.

**Note:** The prediction in nb19 is generated by re-fitting the model within nb19 itself (not by loading the nb17 pickled model). The feature set used matches nb17 (baseline + interactions). Since nb19 re-fits on the full sample, the residuals are **in-sample residuals** — the same qualification applies here as for nb17's AUC.

### 4b. Residual Verification

| Country | Total killings | Total predicted | Mean annual residual | Years |
|---|---|---|---|---|
| Philippines (PHL) | 155 | 57.1 | **3.06/yr** | 32 |
| Iraq (IRQ) | 285 | 128.3 | **4.90/yr** | 32 |

- Mean annual residuals confirmed correct (averaged over all available years, not a single-year artefact). ✓
- Residuals are from the hurdle combined prediction. ✓

### 4c. Maguindanao 2009 Spike

Philippines 2009 killings = **38** — confirmed as a clearly visible spike (next highest year is 2004 with 11). The spike is the Maguindanao massacre. The model does not predict close to 38 for 2009 (predicted is structural, ~3–4), confirming the audit note that this event-driven spike is not captured by the structural model.

---

## 5. Output Integrity

### 5.1 Figures

**final_report/ subdirectories:** All numbered figures present (fig01–fig09, figa01–figa07, table01–table05, case study figures).

**`gpv_presentation.html`: FILE NOT FOUND.**  
No HTML presentation file exists anywhere in the repository. If such a file was referenced in the audit prompt or should exist for submission, it needs to be created or added to the repo.

### 5.2 Gephi Files

**Gephi project files (4 present):** `arms_2007.gephi`, `arms_animation.gephi`, `colonial_structure_snapshot.gephi`, `oda_2010.gephi`. ✓

**Gephi input CSVs (9 present):** Confirmed:
- `edges_arms_2007.csv`, `edges_arms_allyears.csv`, `edges_colonial_static.csv`
- `edges_oda_2010.csv`, `edges_oda_allyears.csv`
- `nodes_2007_arms.csv`, `nodes_2010_oda.csv`, `nodes_attributes.csv`, `nodes_colonial.csv`

**Gephi renders (PNG/SVG, 3+3 present):** arms_2007, oda_2010, colonial_structure — all present. ✓

**Flag — ARMS ANIMATION COLUMN MISMATCH (MINOR):**  
`edges_arms_allyears.csv` has columns `['Source', 'Target', 'Year', 'Weight', 'Type', 'Layer']`.  
Gephi's timeline/dynamic graph feature requires **`Start`** and **`End`** columns (interval format), not a single `Year` column. `arms_animation.gephi` was built from this file. The animation timeline will not work in Gephi unless the edge file is converted to Start/End format. Same issue applies to `edges_oda_allyears.csv`. The static snapshot files (`edges_arms_2007.csv`, `edges_oda_2010.csv`) are unaffected. **Do not fix without instruction** — noted here for review.

### 5.3 Colour Palette

The project palette is `#BF3A27` (red) / `#C7922A` (gold).

**Consistent use found in:** nb19, nb21, nb22, `generate_final_report_figures.py`.

**Flag — MAIN MODEL NOTEBOOKS MISSING PROJECT COLOURS (MINOR):**  
`nb16` and `nb17` use their own colour schemes (`steelblue`, `salmon`, `#2e7d32`) rather than the project palette. This means the main results figures (fig04_nb16_forest.png, fig05_nb17_forest.png, fig06_comparison_forest.png, fig07_roc_curves.png) do not use the project colours. For a unified submission this should be standardised.

---

## 6. Reproducibility

### 6.1 Correct Execution Order

```
05 → 06 → 08 → [MISSING: initial dyadic panel build] → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21 → 22
```

nb02 (country standardisation) and nb03/nb04 (EDA) can run at any point after their input files exist.

### 6.2 Critical Reproducibility Gaps

**Flag — MISSING PIPELINE NOTEBOOK (CRITICAL):**  
No notebook in the repo constructs the initial dyadic panel (`panel_with_controls_1992_2024.csv` / `dyadic_panel_1992_2024_pre_oda_floor.csv`) from raw sources. This notebook would need to:
1. Read SIPRI, OECD ODA, econ_neocol_score, COLDAT, controls, CPJ
2. Create the sender-recipient-year dyadic frame
3. Join all sources on ISO3 + year
4. Produce the initial 115,640-row dyadic panel

The output file exists on disk so existing analysis can proceed, but the pipeline **cannot be rebuilt from raw data**.

**Flag — nb09 STALE FILE PATHS (CRITICAL):**  
`nb09` reads `panel_with_controls_1992_2024.csv` and `panel_with_controls_1992_2024-ODACAPPED.csv`. Both were renamed in nb12 cell 8. nb09 will fail with `FileNotFoundError` if re-run.

**Flag — nb02 STALE FILE PATHS (MODERATE):**  
`nb02` reads from `data/processed/military/sipri_trade_register.csv`, `data/processed/colonial/coldat_colonial_ties.csv`, etc. Current structure has these at `data/processed/sipri_trade_register.csv`, `data/processed/coldat_colonial_ties.csv`. nb02 will fail if re-run.

### 6.3 Overwrite Risk

**nb09** saves back to the **same path** it reads from (`panel_with_controls_1992_2024.csv`). If re-run, it would overwrite the input with the ODA-floored version, making the pre-floor snapshot inaccessible. (Currently moot because the source file was renamed, but the code pattern is unsafe.)

**nb12 cell 8** performs file renames. If re-run after the renames were already done, the cell prints "SKIP (already renamed)" — this is safe.

### 6.4 Environment

**No `requirements.txt` or `environment.yml` found.**

Key packages inferred from notebook imports:

| Package | Used in |
|---|---|
| pandas | All notebooks |
| numpy | All notebooks |
| statsmodels | nb16, nb17, nb22 (Logit, NegativeBinomial) |
| sklearn | nb16, nb17, nb22 (roc_auc_score, roc_curve) |
| networkx | nb11 |
| scipy | nb22 (spearmanr, pearsonr) |
| matplotlib | nb15–nb22 |
| pycountry | nb02 |
| pickle | nb16, nb17, nb22 |

The conda environment `basecamp` contains these; it should be exported as `environment.yml` before submission.

### 6.5 Random Seeds

No random seeds are set in any notebook. The statsmodels MLE optimiser is deterministic given starting values, so results are reproducible. No bootstrap confidence intervals or sampling is performed. This is acceptable, but should be noted if any bootstrap-based sensitivity checks are added later.

---

## 7. Prioritised Fix List

### Must Fix Before Submission

| # | Issue | Severity | Action |
|---|---|---|---|
| F1 | **Missing initial dyadic panel build notebook** | CRITICAL | Reconstruct or document the build steps; at minimum add a `DATA_BUILD.md` explaining which raw files were joined and how, so a reviewer can audit the construction even if they can't re-run it |
| F2 | **nb09 stale paths** | CRITICAL | Update read/write paths in nb09 to use current file names (`dyadic_panel_1992_2024_pre_oda_floor.csv`, `dyadic_panel_1992_2024_oda_capped.csv`) |
| F3 | **econ_neocol_score sign flip undocumented in results** | CRITICAL | The logit coefficient flips from null-negative (nb16) to significant-positive (nb17 p=0.011). CLAUDE.md's claim "null across all specifications" is wrong for the logit. Either correct the narrative or add a paragraph explaining the collinearity mechanism in the results section |
| F4 | **In-sample AUC labelling** | MODERATE | Label AUC 0.857 as "in-sample" wherever reported (figure captions, paper text). Add nb22's OOS AUC 0.858 as the confirmed temporal validation result. Note that nb17 network model OOS performance is not validated |
| F5 | **nb16 vs nb17 SE method inconsistency** | MODERATE | Either (a) promote nb16 clustered SEs as headline (already computed in cell 11), or (b) clearly note in the paper that nb16 SEs are non-robust and nb17 SEs are clustered, so p-values are not directly comparable |
| F6 | **No environment file** | CRITICAL | Run `conda env export -n basecamp > environment.yml` and commit it |
| F7 | **No fixed effects justification in write-up** | MODERATE | Add a paragraph explaining why pooled specification is chosen and why country FE is not feasible (would eliminate time-invariant colonial_tie_flag) |
| F8 | **CLAUDE.md "83%+ zeros" is wrong** | MINOR | Correct to 88.7% (full panel) / 88.1% (model sample) in CLAUDE.md and any paper text |

### Fix Before Final Submission (Cosmetic/Documentation)

| # | Issue | Severity | Action |
|---|---|---|---|
| F9 | **nb02 stale paths** | MODERATE | Update read paths if nb02 will be re-run; otherwise mark as "historical, do not re-run" |
| F10 | **Gephi arms animation column format** | MINOR | Convert `Year` column to `Start`/`End` (e.g., `Start = Year`, `End = Year + 1`) in `edges_arms_allyears.csv` and `edges_oda_allyears.csv` for timeline functionality |
| F11 | **Colour palette in nb16/nb17** | MINOR | Replace `steelblue`/`salmon`/`#2e7d32` with `#BF3A27`/`#C7922A` for consistency with case study and appendix figures |
| F12 | **CLAUDE.md notebook table incomplete** | MINOR | Add nb18, nb20, nb21, nb22 with descriptions |
| F13 | **`v3_imf_trade.csv` misplaced** | MINOR | Move from `data/processed/` to `data/processed/ignore/` |
| F14 | **`colonizer_iso3` not stored in COLDAT** | MINOR | Add a `colonizer_iso3` column to `coldat_colonial_ties.csv` for audit transparency |
| F15 | **nb17 network OOS validation missing** | MODERATE | Run nb22 variant with `full_features` (nb17) to get OOS AUC for the network-augmented model. Expected to perform similarly given coefficient stability, but unverified |
| F16 | **`bilateral_oda_pagerank_lag1` p=0.046 in NB** | MODERATE | Add explicit caution note in results: this coefficient (value=101.0) is an artefact of near-uniform PageRank scaling, not substantively interpretable |
| F17 | **Presentation HTML missing** | MODERATE | Create or add `gpv_presentation.html` if this is required for submission |

---

## 8. Summary Assessment

The pipeline is **substantially sound** for the count model and key result (`oda_x_colonial` significant in both components). The target variable, feature engineering, and lag structure are correctly implemented. The temporal validation (nb22) confirms the in-sample AUC is not inflated by overfitting. The case study residuals are computed correctly.

**The three issues that most need attention before submission:**
1. The missing dyadic panel construction notebook (F1) — any reviewer who wants to independently reproduce from raw data cannot.
2. The econ_neocol_score logit sign flip between specifications (F3) — as written, the paper's claim of "consistent null" is factually incorrect for the logit component.
3. No environment file (F6) — reproduction is not possible without knowing exact package versions.

Everything else is either cosmetic, already mitigated (temporal validation via nb22), or a well-documented limitation (no FE, in-sample AUC labelling).
