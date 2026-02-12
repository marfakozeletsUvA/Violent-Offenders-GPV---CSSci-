# Violence Against Journalists: Network Prediction Project

> GPV: Unequal Machines Grand Challenge

## Research Question

Does Global North military intervention destabilize countries in ways that increase violence against journalists—and does the international community then treat that violence as "expected", leading to systematic impunity?

## Project Overview

This project uses **network analysis** combined with **machine learning** to predict impunity outcomes for violence against journalists. We construct networks capturing military intervention ties, colonial history, and conflict spillover to examine how a country's position in global power structures affects whether perpetrators face justice.

### Two Phases
1. **Mindless Machine** — Build a predictive algorithm optimizing for performance
2. **Auditor Phase** — Critical bias audit using postcolonial theory

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

## For Teammates: Getting Started

### Clone the repo
```bash
git clone https://github.com/marfakozeletsUvA/Violent-Offenders-GPV---CSSci-.git
cd Violent-Offenders-GPV---CSSci-
```
You'll get everything including the data automatically.

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

- [Team member names here]

## Timeline

| Week | Goal |
|------|------|
| 1-2  | Data exploration, research question formulation |
| 3    | Literature review (status quo theory) |
| 4-5  | Method exploration, synthesis |
| 6-8  | Critical theory application, bias audit |

**Final deadline:** June 2, 2025

## Quick Links

- [Data Sources](docs/DATA_SOURCES.md)

---

*Last updated: February 2025*