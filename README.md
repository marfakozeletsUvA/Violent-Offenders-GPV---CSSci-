# Violence Against Journalists

> GPV: Unequal Machines Grand Challenge

## Potential RQ

## Project Overview 

### Two Phases
1. **Mindless Machine** — Build a predictive algorithm optimizing for performance (using SNA)
2. **Auditor Phase** — Critical bias audit using postcolonial theory (post-colonialism ties nicely)

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

- Marfa
- Kiavash
- Vanessa
- Julia
- Sophie


## Quick Links

- [Data Sources](docs/DATA_SOURCES.md)

---

*Last updated: February 2025*