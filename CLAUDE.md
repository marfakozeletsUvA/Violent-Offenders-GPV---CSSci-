# CLAUDE.md — GPV: Unequal Machines / Violent Offenders

## Project Overview
Computational Social Science graduate research project examining whether
Global South states' embeddedness in neo-colonial networks predicts
journalist killings and impunity.

Research question: To what extent do economic subordination, military dependency, and historical colonial relationships predict journalist killings in countries? (general direction phrasing might be changing)

## Conda Environment Rules
### Available Environments
- **basecamp** — default for this project (pandas, sklearn, statsmodels, networkx)
- **everest-ml** — heavy ML only (torch, transformers)
- **k2-geo** — geospatial only (geopandas, rasterio)
- **kilimanjaro** — blank/experimental, do not use unless explicitly told to

### Rules
- This project uses: basecamp (default for all data pipeline and modelling work)
- Run Python via: `conda run -n basecamp python`
- Never default to `base` or `kilimanjaro`
- Never install packages without explicit permission
- If a required library is missing, ask before installing

## Repo Structure
data/
raw/                  # original unmodified source files
processed/            # cleaned single-source files
trade_dependency_engineering/  # old approach, do not use
merged/               # joined multi-source panels
src/                    # reusable modules
notebooks/              # numbered sequential notebooks (see subfolders below)
  01_preprocessing/   # raw data cleaning and transformation
  02_pipeline/        # panel construction and merging
  03_analysis/        # modelling, diagnostics, and validation
  *.py                # report generation scripts (remain in notebooks/ root)
outputs/                # model outputs, figures

## Notebook Naming Convention
Sequential numbered format: `11_network_construction.ipynb`

### Notebook Folder Structure
- `notebooks/01_preprocessing/` — raw data cleaning and transformation
- `notebooks/02_pipeline/`      — panel construction and merging
- `notebooks/03_analysis/`      — modelling, diagnostics, and validation
- `.py` scripts remain in `notebooks/` root (path-resolution depends on their location)

### Pipeline Sequence — All Completed

| Notebook | Folder | Status | Description |
|----------|--------|--------|-------------|
| `02_country_standardization.ipynb` | 01_preprocessing | Active | Cross-dataset country name standardisation to ISO3 |
| `05_controls_preprocessing.ipynb` | 01_preprocessing | Active | Control variables preprocessing (GDP, population, UCDP conflict) |
| `06_oecd_dac2_oda_fixing.ipynb` | 01_preprocessing | Active | OECD DAC2 ODA duplicate fix and FSM correction |
| `09_transform_oda_values.ipynb` | 01_preprocessing | Active | ODA negative values floor (loan repayment entries → 0) |
| `11_network_construction.ipynb` | 02_pipeline | Active | Network construction — 4 layers (arms, ODA, econ, colonial); pre-lagged centrality measures |
| `12_collapse_monadic_panel.ipynb` | 02_pipeline | Active | Dyadic → monadic panel collapse (recipient-year aggregation) |
| `14_final_panel_merge.ipynb` | 02_pipeline | Active | Final panel merge: monadic + network measures + lag transforms |
| `13_robustness_variants.ipynb` | 03_analysis | Active | Robustness operationalisations: 5-yr arms stock, econ score mean aggregation |
| `15_network_diagnostics.ipynb` | 03_analysis | Active | Network diagnostics and visualisation (pre-modelling checks) |
| `16_baseline_hurdle_model.ipynb` | 03_analysis | Active | Baseline hurdle model (logit + NegBin, non-robust SEs) |
| `17_network_augmented_hurdle_model.ipynb` | 03_analysis | Active | Network-augmented hurdle model (+ network features, interaction terms, clustered SEs) |
| `18_econ_neocol_score_diagnostic.ipynb` | 03_analysis | Active | Econ neo-colonial score diagnostic (variance, structural mismatch, top recipients) |
| `19_case_study_diagnostic.ipynb` | 03_analysis | Active | Philippines vs Iraq case study. PHL: colonial_tie=1 (ESP/USA), model predicts ~37% of killings, misses 2009 Maguindanao massacre (32 killed, event-driven). IRQ: colonial_tie=0 for USA (GBR mandate fires), model predicts ~45% through wrong channel (conflict not ODA×colonial). Shared audit finding: model sees violence not power structures. Outputs in `outputs/final_report/06_case_study/` |
| `20_gephi_export.ipynb` | 03_analysis | Active | Gephi-compatible edge/node export for network visualisation |
| `21_econ_neocol_score_variance_audit.ipynb` | 03_analysis | Active | ECI distribution, clip-loss, and econ score temporal variance audit |
| `22_temporal_train_test_validation.ipynb` | 03_analysis | Active | Temporal train/test split validation; AUC stability across time windows |
| `nb23_oos_validation.ipynb` | 03_analysis | Active | OOS temporal validation, bootstrapped AUC CIs, four-cell AUC summary table |
| `24_econ_neocol_score_audit.ipynb` | 03_analysis | Active | econ_neocol_score measurement audit (1995 artifact, variance, clip-induced zeros); outputs in `outputs/final_report/04_appendix/` |

Always save outputs to `data/processed/` or `data/merged/` with clear names.
Use relative paths throughout for team portability.

## Current Dataset Stack (Final)

### Military Layer
- SIPRI Arms Transfers → `data/processed/sipri_trade_register.csv`
- UCDP Dyadic Dataset v25.1 → `data/raw/controls/ucdp-control-raw.csv` (merged into `data/processed/controls/controls_merged.csv`)

### Economic Layer
- OECD DAC2 bilateral ODA → `data/processed/oecd_dac2_oda.csv` (negative values floored at 0)
- ECI (Harvard Growth Lab) → `data/raw/economic/eci-rankings-raw.csv`
- ECI-based neo-colonial trade score → `data/processed/econ_neocol_score.csv`
- World Bank bilateral debt → DROPPED (83.6% MNAR, South-South debt structurally invisible)

### Colonial Layer
- COLDAT → `data/processed/coldat_colonial_ties.csv`
- Used as interaction/moderator term only (3.8% dyads have colonial_tie=1)
- Never use as standalone predictor

### Outcome
- CPJ journalist killings + impunity → `data/processed/target_journalist_killings.csv`

### Controls (lean set of 3)
- GDP per capita log-transformed (WB)
- UCDP/PRIO Armed Conflict binary presence
- Population log-transformed (WB)
- All in: `data/processed/controls/controls_merged.csv`
- v2x_polyarchy dropped (34.1% missing, shrinks sample — see LIMITATIONS.md)

### Rejected Variables — Do Not Reintroduce
- HDI (collinear with GDP + mediates economic pathway)
- Press freedom indices (too close to outcome + Western bias)
- State fragility indices (pre-2005 gap + mediator risk)
- World Bank bilateral debt (83.6% MNAR)
- p5_trade_engineering.csv (old income classification approach — replaced by ECI)

## Current Panel Files

### Dyadic panel (sender–recipient–year)
- `data/merged/dyadic_panel_1992_2024_oda_capped_log.csv` — **primary dyadic source of truth** (115,640 rows × 15 cols)
  - Columns: `sender_iso3`, `recipient_iso3`, `year`, `arms_tiv`, `bilateral_oda`,
    `econ_neocol_score`, `econ_neocol_score_log`, `colonial_tie`, `journalist_killings`, `gdp_per_capita`,
    `gdp_per_capita_log`, `population`, `population_log`, `armed_conflict`, `conflict_intensity`
  - `bilateral_oda` floored at 0 (negative values = DAC2 loan repayment entries, no theoretical meaning)
  - `bilateral_debt` not present (dropped — 83.6% MNAR)
  - `v2x_polyarchy` not present (dropped — 34.1% missing, not needed in lean control set)
- `data/merged/dyadic_panel_1992_2024_oda_capped.csv` — same panel without log transforms (intermediate)
- `data/merged/dyadic_panel_1992_2024_pre_oda_floor.csv` — pre-floor snapshot (negative ODA values retained)

### Monadic panel (recipient–year) — use for modelling
- `data/merged/panel_monadic_1992_2024.csv` — **collapsed for baseline modelling** (6,358 rows × 13 cols)
  - Built by `notebooks/02_pipeline/12_collapse_monadic_panel.ipynb`
  - Columns: `recipient_iso3`, `year`, `arms_tiv_total`, `oda_total`, `econ_neocol_score_total`,
    `colonial_tie_flag`, `journalist_killings`, `gdp_per_capita`, `gdp_per_capita_log`,
    `population`, `population_log`, `armed_conflict`, `conflict_intensity`
  - `arms_tiv_total` = sum of incoming TIV across all senders per recipient-year
  - `oda_total` = sum of incoming ODA (USD millions) across all senders per recipient-year
  - `econ_neocol_score_total` = log1p(sum of raw dyadic econ_neocol_score × 1e9) — raw scores
    summed first, then scaled and log-transformed (matches dyadic `econ_neocol_score_log` convention;
    range 0–11; 38.5% zeros reflect ECI gap 1992–1994 and non-ECI countries)
  - `colonial_tie_flag` = 1 if any sender held a colonial relationship with this recipient
  - journalist_killings: 88.7% zeros, max 82, var/mean ratio 14.7x → confirms overdispersion

- `data/merged/panel_monadic_enriched_1992_2024.csv` — **robustness side-branch only** (6,358 rows × 15 cols)
  - Built by `notebooks/03_analysis/13_robustness_variants.ipynb`
  - Adds `arms_tiv_stock_5yr` (5-year rolling sum) and `econ_neocol_score_mean` (mean across senders)
  - NOT used in `panel_final_1992_2024.csv` — for robustness model comparison only

### Final modelling panel
- `data/merged/panel_final_1992_2024.csv` — **primary modelling input** (6,358 rows × 38 cols)
  - Built by `notebooks/02_pipeline/14_final_panel_merge.ipynb` (inner join of monadic + network measures)
  - Contains all baseline features, network centrality measures (pre-lagged), and additional lags

  **baseline_features (8):**
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

  **network_only_features (8):** added on top of baseline_features in nb17:
  ```python
  network_only_features = [
      'arms_tiv_in_strength_lag1',          'arms_tiv_pagerank_lag1',
      'bilateral_oda_in_strength_lag1',     'bilateral_oda_pagerank_lag1',
      'econ_neocol_score_in_strength_lag1', 'econ_neocol_score_pagerank_lag1',
      'colonial_tie_in_strength_lag1',      'colonial_tie_pagerank_lag1',
  ]
  ```
  `network_features` = `baseline_features` + `network_only_features` (16 total)

  **interaction_features (3, constructed in nb17 — not stored in panel_final):**
  ```python
  interaction_features = [
      'arms_x_colonial',   # arms_tiv_total_log_lag1 × colonial_tie_flag
      'oda_x_colonial',    # oda_total_log_lag1 × colonial_tie_flag
      'econ_x_colonial',   # econ_neocol_score_total_lag1 × colonial_tie_flag
  ]
  ```
  These terms are computed during model fitting in nb17 and are not stored in
  `panel_final_1992_2024.csv`.

- Analysis window: 1992–2024 (CPJ is left binding constraint)
- Future additions might limit time window (always warn)

## Variable Being Constructed: econ_neocol_score

### Formula
```python
complexity_asymmetry = (ECI_sender - ECI_receiver).clip(lower=0)
trade_dependency = bilateral_trade / receiver_GDP
econ_neocol_score = trade_dependency * complexity_asymmetry
```

### Data Sources
- ECI: `data/raw/economic/eci-rankings-raw.csv`, column `eci_hs92`, merge on iso3 + year
- bilateral_trade: sum of exports + imports per sender-receiver-year (derived from IMF IMTS; v3_imf_trade.csv no longer used directly)
- receiver_GDP: GDP column in `data/processed/controls/controls_merged.csv`

### Logic
- Flooring at 0 means only relationships where sender is MORE economically
  complex than receiver contribute positively
- North-North dyads auto-zero (no asymmetry)
- Angola-style petro-states score correctly low despite high GNI
- Coverage: 1995-2024 (ECI starts 1995 — document 1992-1994 gap as limitation)

### Log transformation
```python
econ_neocol_score_log = np.log1p(econ_neocol_score * 1e9)
```
Raw `econ_neocol_score` retained in panel. Log version added as `econ_neocol_score_log` to handle extreme right skew before modelling.

### How it fits in the pipeline
- Dyadic variable: sender_iso3, recipient_iso3, year, econ_neocol_score
- Used as log-transformed edge weight on economic network layer (`econ_neocol_score_log`);
  NaN → 0 before edge construction (no edge = no measurable asymmetry, not a zero relationship)
- Collapsed to monadic for baseline: raw scores summed per recipient-year, then log1p(sum × 1e9)
- **Econ network 1992–1994 caveat:** ECI gap means no econ edges for those years;
  PageRank distributes uniformly at 1/N. 1-year lag shifts this forward — `econ_neocol_score_pagerank_lag1`
  is uniform for years 1993, 1994, 1995 in the final panel (not just 1992–1994).

## Modelling Pipeline

### Target Variable Properties
- 83%+ zeros, variance/mean ratio ~11-16x
- Confirmed overdispersion → negative binomial appropriate
- Zero-inflation → hurdle model preferred over straight NegBin

### Two Models (Both Completed)
1. **Baseline hurdle model** (nb16) — logistic on zeros + NegBin on non-zeros
   - Predictors: collapsed monadic versions of all neo-colonial layers + controls
   - SE method: non-robust (standard MLE defaults)
2. **Network-augmented hurdle model** (nb17) — baseline + network centrality + interaction terms
   - SE method: clustered by `recipient_iso3` throughout
   - Compare both models via AIC and coefficient stability

### Network Layer (Completed in nb11)
- Built per-layer directed networks: arms / ODA / economic (econ_neocol_score_log as edge weight) / colonial
- Extracted node-level measures per country-year: weighted in-strength, out-strength, PageRank, dependency balance, in-concentration
- All network measures pre-lagged by 1 year in nb11 (`_lag1` suffix in `network_measures_1992_2024.csv`)
- Network in-strength for econ layer ≠ econ_neocol_score_total: in-strength uses log edge weights;
  total uses log1p(sum_raw × 1e9). Both are valid but measure different things.
- Carried into final panel via inner join in nb14

### Model Results Summary

**nb16 — Baseline Hurdle Model**
- Analytical sample: 5,765 obs (593 dropped, 9.3% — lag NaNs + missing GDP/population/conflict)
- Logit (any killing): AUC 0.848, McFadden R² = 0.269, AIC = 3097.2
- NegBin (count | killing > 0): pseudo-R² = 0.098, AIC = 2899.3, n = 687
- SE method: non-robust

**nb17 — Network-Augmented Hurdle Model**
- Same analytical sample as nb16
- Logit: AUC 0.857, McFadden R² = 0.284, AIC = 3054.1 (Δ = −43.1 vs nb16)
- NegBin: AIC = 2863.9 (Δ = −35.4 vs nb16), overdispersion alpha = 0.41
- SE method: clustered by `recipient_iso3`

**Key findings**
- `oda_x_colonial` significant in both components (logit p = 0.046, NegBin p = 0.003); robust to IRQ/SYR exclusion
- `econ_neocol_score` null across all specifications (NegBin p = 0.94 in nb17; sign flip in nb17 logit is collinearity artifact — VIF 10.7 on in-strength)
- Arms: negative coefficient in logit (stable-allies effect); near-zero in NegBin
- Network features add AIC fit (Δ = −43 logit, −35 NegBin) but no standalone interpretable signal
- `bilateral_oda_pagerank_lag1` shows marginal significance in NegBin (p = 0.046) — treat with caution given VIF = 10.4

### COLDAT as Moderator
- Use only as interaction term: arms_effect × colonial_tie, aid_effect × colonial_tie
- Never as standalone predictor

### Compute Constraints
- PyMC/Bayesian deferred — M1 Air C compilation fails under macOS Tahoe
- Use Google Colab or university HPC for any sampling-heavy work
- nutpie installed but insufficient on local machine

## Key Methodological Decisions (Do Not Revisit Without Discussion)
- Hurdle model chosen over straight NegBin
- Bilateral debt dropped (MNAR not random)
- Conflict variable is both control AND potential mediator — run with/without
  as robustness check
- Over-controlling risk: HDI, press freedom, fragility all block causal pathways
- Hub-and-spoke network limitation acknowledged — address in limitations section
- ECI replaces income classification for asymmetry weighting

## Team
- Marfa: technical lead
- Kiavash: network visualization
- Sophie: postcolonial theory
- Vanessa: social science
- Julia: bias analysis

## Deadlines
- June 2-3 2026: predictive algorithm demo, bias audit report, code/data submission

## Code Style
- Relative paths throughout (team portability)
- Save all intermediate outputs with clear versioned names
- Document all missingness decisions inline
- Pause and show shape + head after each major transformation step
- Never proceed past a step without confirming output looks correct

## Deprecated
The following files are kept for reference only. Do not use in analysis or modelling.
- `data/processed/deprecated/` — dropped variables (worldbank_bilateral_debt.csv, wb_income_classification.csv, trade_dependency_engineering/p1–p5)
- `data/processed/trade_dependency_engineering/` — old income classification approach, replaced by ECI-based econ_neocol_score