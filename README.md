# Violence Against Journalists

> GPV: Unequal Machines Grand Challenge

## Research Question

Do neo-colonial ties—military dependency, economic relationships, and colonial history—predict violence against journalists? And does the structure of these relationships help explain patterns of impunity?

## Project Overview 

This project uses **network analysis** to examine how neo-colonial relationships create structural conditions for journalist violence. We construct a multiplex network where countries are nodes and neo-colonial ties (military, economic, colonial) are weighted edges. Network features are then used to predict journalist killings and imprisonments.

### Theoretical Framework

Drawing on neo-colonial theory (Nkrumah, dependency theory, world-systems analysis), we argue that former colonial powers maintain influence through indirect means. This creates two pathways to journalist violence:

1. **Destabilization pathway**: Military intervention and arms flows fuel conflict → journalists targeted in unstable environments
2. **Structural violence pathway**: Economic dependency creates elite capture → journalists targeted for exposing corruption

Both pathways converge on **impunity**: neo-colonial patrons don't pressure client states on press freedom because they benefit from maintaining these relationships.

### Two Phases

1. **Mindless Machine** — Build a predictive algorithm using network features from neo-colonial ties
2. **Auditor Phase** — Critical bias audit examining how the model may reproduce colonial categories

## Network Architecture

## Network Structure

We build a **multiplex network** with three layers:

### Layer 1: Military Ties
| Component | Data Source | Processed File | Measurement |
|-----------|-------------|----------------|-------------|
| Arms flows | SIPRI Arms Transfers | `sipri_arms_flows.csv` | TIV value (continuous, 1990–2024) |
| US interventions | MIP | `mip_us_interventions.csv` | Binary/count (1990–2019) |
| Global external support | UCDP ESD | `ucdp_external_support.csv` | Troops, weapons, training, funding (1990–2017) |

### Layer 2: Economic Ties
| Component | Data Source | Processed File | Measurement |
|-----------|-------------|----------------|-------------|
| Bilateral aid flows | AidData | `aiddata_bilateral_flows.csv` | USD commitments (1990–2013) |
| Total ODA received | World Bank | `oda_received_by_country.csv` | USD (control variable, 1990–2023) |

### Layer 3: Colonial History (Base Layer)
| Component | Data Source | Processed File | Measurement |
|-----------|-------------|----------------|-------------|
| Colonial relationship | COLDAT | `coldat_colonial_ties.csv` | Binary (colonized yes/no) |
| Colonial period | COLDAT | `coldat_colonial_ties.csv` | Start/end years |

### Outcome Variable
| Variable | Data Source | Processed File | Measurement |
|----------|-------------|----------------|-------------|
| Journalist killings | CPJ | `target_journalist_killings.csv` | Count per country-year (1992–2026) |

## Methodology

### Analysis Pipeline
```
Stage 1: Build Network     →  Merge datasets, assign edge weights per layer
Stage 2: Extract Features  →  Calculate tie strength, centrality per country-year
Stage 3: Run Models        →  Predict journalist violence from network features
```

### Model Strategy (Iterative)

| Model | Specification | Purpose |
|-------|---------------|---------|
| Model 1 | violence ~ composite_neocolonial_score | Baseline: does overall embeddedness predict violence? |
| Model 2 | violence ~ military + economic + colonial | Disaggregated: which dimension matters most? |
| Model 3 | Model 2 + controls (GDP, regime, conflict) | Full: is the effect robust? |

Models: Logistic regression (binary outcome) or negative binomial (count outcome), plus Random Forest for feature importance.

## Repository Structure
```
├── data/
│   ├── raw/                 # Original datasets (DO NOT EDIT)
│   ├── processed/           # Cleaned and merged data
│   └── README.md            # Data documentation
├── notebooks/               # Jupyter notebooks (analysis, exploration)
├── src/                     # Python scripts (reusable functions)
├── docs/
│   └── DATA_SOURCES.md      # Links to all datasets
├── outputs/                 # Figures, reports, exports
└── README.md
```

## Data Sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| CPJ Database | cpj.org/data | 1992–present |
| SIPRI Arms Transfers | armstransfers.sipri.org | 1950–2024 |
| MIP (US interventions) | Tufts CSS / Kaggle | 1776–2019 |
| MIPS (Major powers) | plsullivan.web.unc.edu | 1946–2003 |
| OECD DAC Aid | stats.oecd.org | 1960–present |
| World Bank IDS | data.worldbank.org | Varies |
| UN Comtrade | comtradeplus.un.org | 1962–present |
| COLDAT | Harvard Dataverse | Historical |
| ICOW Colonial History | paulhensel.org | Historical |

See [Data Sources](docs/DATA_SOURCES.md) for full documentation.

### Important rules

| Rule | Why |
|------|-----|
| **Never edit files in `data/raw/`** | Keep originals untouched. Save cleaned versions to `data/processed/` |
| **Pull before you work** | Always run `git pull` first to get latest changes |
| **Commit often with clear messages** | e.g. `git commit -m "Add EDA notebook for incident types"` |
| **Avoid merge conflicts** | Don't work on the same file simultaneously — communicate! |
| **Use relative paths in notebooks** | e.g. `pd.read_csv("../data/raw/mapmf_alerts_cleaned.csv")` |

### Typical workflow
```bash
git pull                     # Get latest changes
# ... do your work ...
git add .
git commit -m "Your message"
git push
```

### If you get merge conflicts
```bash
git pull                     # This will show conflict
# Open the conflicted file, fix it manually
git add .
git commit -m "Resolve merge conflict"
git push
```

## Team

- Marfa
- Kiavash
- Vanessa
- Julia
- Sophie

## Quick Links

- [Data Sources](docs/DATA_SOURCES.md)

---

*Last updated: February 2025*