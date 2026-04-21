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
notebooks/              # numbered sequential notebooks
outputs/                # model outputs, figures
## Notebook Naming Convention
Sequential numbered format: `07_trade_dependency_engineering.ipynb`
Next notebook should be `08_*`.
Always save outputs to `data/processed/` or `data/merged/` with clear names.
Use relative paths throughout for team portability.

## Current Dataset Stack (Final)

### Military Layer
- SIPRI Arms Transfers → `data/processed/sipri_trade_register.csv`
- UCDP Dyadic Dataset v25.1 → download pending

### Economic Layer
- OECD DAC2 bilateral ODA → `data/processed/oecd_dac2_oda.csv`
- IMF IMTS bilateral trade → `data/processed/v3_imf_trade.csv`
- ECI (Harvard Growth Lab) → `data/raw/economic/eci-rankings-raw.csv`
- ECI-based neo-colonial trade score → `data/processed/econ_neocol_score.csv`
- World Bank bilateral debt → DROPPED OR TO DROP (83.6% MNAR, South-South debt
  structurally invisible)

### Colonial Layer
- COLDAT → `data/processed/coldat_colonial_ties.csv`
- Used as interaction/moderator term only (3.8% dyads have colonial_tie=1)
- Never use as standalone predictor

### Outcome
- CPJ journalist killings + impunity → `data/processed/target_journalist_killings.csv`

### Controls (lean set of 4)
- GDP per capita log-transformed (WB)
- V-Dem v2x_polyarchy
- UCDP/PRIO Armed Conflict binary presence
- Population log-transformed (WB)
- All in: `data/processed/controls/controls_merged.csv`

### Rejected Variables — Do Not Reintroduce
- HDI (collinear with GDP + mediates economic pathway)
- Press freedom indices (too close to outcome + Western bias)
- State fragility indices (pre-2005 gap + mediator risk)
- World Bank bilateral debt (83.6% MNAR)
- p5_trade_engineering.csv (old income classification approach — replaced by ECI)

## Current Panel Files
- `data/merged/panel_with_controls_1992_2024.csv` — **single source of truth** (115,640 rows × 14 cols)
  - Columns: `sender_iso3`, `recipient_iso3`, `year`, `arms_tiv`, `bilateral_oda`,
    `econ_neocol_score`, `colonial_tie`, `journalist_killings`, `gdp_per_capita`,
    `gdp_per_capita_log`, `population`, `population_log`, `armed_conflict`, `conflict_intensity`
  - `bilateral_debt` not present (dropped — 83.6% MNAR)
  - `v2x_polyarchy` not present (dropped — 34.1% missing, not needed in lean control set)
- `panel_dyadic_1992_2024.csv` — **no longer exists**, superseded by the above
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
- bilateral_trade: sum of exports + imports per sender-receiver-year from IMF IMTS
- receiver_GDP: GDP column in `data/processed/controls/controls_merged.csv`

### Logic
- Flooring at 0 means only relationships where sender is MORE economically
  complex than receiver contribute positively
- North-North dyads auto-zero (no asymmetry)
- Angola-style petro-states score correctly low despite high GNI
- Coverage: 1995-2024 (ECI starts 1995 — document 1992-1994 gap as limitation)

### How it fits in the pipeline
- Dyadic variable: sender_iso3, recipient_iso3, year, econ_neocol_score
- Used as edge weight on economic network layer
- Collapsed to monadic for baseline: sum incoming scores per recipient-year

## Modelling Pipeline

### Target Variable Properties
- 83%+ zeros, variance/mean ratio ~11-16x
- Confirmed overdispersion → negative binomial appropriate
- Zero-inflation → hurdle model preferred over straight NegBin

### Two Models
1. **Baseline hurdle model** — logistic on zeros + NegBin on non-zeros
   - Predictors: collapsed monadic versions of all neo-colonial layers + controls
2. **Network-augmented hurdle model** — same + network centrality measures
   - Compare both models

### Network Layer Plan
- Build per-layer directed networks: arms / aid / economic (econ_neocol_score as edge weight) / colonial
- Extract node-level measures per country-year: weighted in-degree, eigenvector, PageRank
- Weighted in-degree on economic layer = sum of incoming econ_neocol_score = baseline econ variable
- Carry all as attributes into collapsed monadic panel

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
- `notebooks/07_trade_dependency_engineering_DEPRECATED.ipynb` — old income classification approach, replaced by ECI-based econ_neocol_score
- `data/processed/deprecated/` — dropped variables (worldbank_bilateral_debt.csv, wb_income_classification.csv, trade_dependency_engineering/p1–p5)