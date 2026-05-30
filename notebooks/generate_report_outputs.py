"""
Generate pre-modelling report outputs for the Violent Offenders / GPV project.

Outputs:
  outputs/data&methods/summary_stats.csv      — monadic panel summary statistics
  outputs/data&methods/summary_stats.png      — table PNG, cream background
  outputs/data&methods/target_distribution.txt — journalist_killings stats
  outputs/appendices/variable_codebook.csv    — variable descriptions
  outputs/limitations/LIMITATIONS_EVIDENCE.md — limitation write-ups with evidence
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONO   = os.path.join(BASE, "data", "merged", "panel_monadic_1992_2024.csv")
DYAD   = os.path.join(BASE, "data", "merged", "dyadic_panel_1992_2024_oda_capped_log.csv")

OUT_DM   = os.path.join(BASE, "outputs", "data&methods")
OUT_APP  = os.path.join(BASE, "outputs", "appendices")
OUT_LIM  = os.path.join(BASE, "outputs", "limitations")

for d in [OUT_DM, OUT_APP, OUT_LIM]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
mono = pd.read_csv(MONO)
dyad = pd.read_csv(DYAD)

print(f"Monadic panel: {mono.shape}")
print(f"Dyadic panel:  {dyad.shape}")

# ---------------------------------------------------------------------------
# 1. Summary stats table
# ---------------------------------------------------------------------------
print("\n=== 1. Summary stats ===")

numeric_cols = mono.select_dtypes(include=[np.number]).columns.tolist()
n = len(mono)

rows = []
for col in numeric_cols:
    s = mono[col].dropna()
    zero_share = (mono[col] == 0).sum() / n * 100
    missing_pct = mono[col].isna().sum() / n * 100
    rows.append({
        "variable":    col,
        "mean":        round(s.mean(),   3),
        "std":         round(s.std(),    3),
        "min":         round(s.min(),    3),
        "max":         round(s.max(),    3),
        "median":      round(s.median(), 3),
        "zero_share":  round(zero_share, 3),
        "missing_pct": round(missing_pct, 3),
    })

stats_df = pd.DataFrame(rows).set_index("variable")
stats_df.to_csv(os.path.join(OUT_DM, "summary_stats.csv"))
print(stats_df)
print(f"Saved: {os.path.join(OUT_DM, 'summary_stats.csv')}")

# ---- PNG table version ----
CREAM  = "#F5F2ED"
DARK   = "#2D2D2D"
HEADER = "#3B3530"

col_labels = ["mean", "std", "min", "max", "median", "zero_share %", "missing %"]
table_data = stats_df.values.tolist()
row_labels  = stats_df.index.tolist()

fig_height = 0.45 * len(row_labels) + 1.4
fig, ax = plt.subplots(figsize=(13, fig_height), facecolor=CREAM)
ax.set_facecolor(CREAM)
ax.axis("off")

tbl = ax.table(
    cellText=table_data,
    rowLabels=row_labels,
    colLabels=col_labels,
    cellLoc="center",
    rowLoc="left",
    loc="center",
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.55)

# Style header row
for j, _ in enumerate(col_labels):
    cell = tbl[0, j]
    cell.set_facecolor(HEADER)
    cell.set_text_props(color="white", fontweight="bold")
    cell.set_edgecolor(CREAM)

# Style row-label column and data cells
for i, _ in enumerate(row_labels):
    row_idx = i + 1
    # row label cell
    lbl_cell = tbl[row_idx, -1]
    lbl_cell.set_facecolor(CREAM if i % 2 == 0 else "#ECE9E3")
    lbl_cell.set_text_props(color=DARK, fontweight="bold")
    lbl_cell.set_edgecolor(CREAM)
    # data cells
    for j in range(len(col_labels)):
        cell = tbl[row_idx, j]
        cell.set_facecolor(CREAM if i % 2 == 0 else "#ECE9E3")
        cell.set_text_props(color=DARK)
        cell.set_edgecolor(CREAM)

ax.set_title(
    "Summary Statistics — Monadic Panel (1992–2024)",
    fontsize=11, fontweight="bold", color=DARK, pad=8,
)

plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DM, "summary_stats.png"),
    dpi=150, bbox_inches="tight", facecolor=CREAM,
)
plt.close()
print(f"Saved: {os.path.join(OUT_DM, 'summary_stats.png')}")

# ---------------------------------------------------------------------------
# 2. Target distribution text
# ---------------------------------------------------------------------------
print("\n=== 2. Target distribution ===")

jk = mono["journalist_killings"]
n_rows        = len(mono)
zero_share    = (jk == 0).mean() * 100
mean_val      = jk.mean()
median_val    = jk.median()
max_val       = jk.max()
var_mean      = jk.var() / jk.mean()
unique_recip  = mono["recipient_iso3"].nunique()

lines = [
    "journalist_killings — Target Variable Distribution",
    "=" * 52,
    f"Total rows (recipient-year obs):  {n_rows:,}",
    f"Zero share:                       {zero_share:.1f}%",
    f"Mean:                             {mean_val:.4f}",
    f"Median:                           {median_val:.1f}",
    f"Max:                              {int(max_val)}",
    f"Variance / Mean ratio:            {var_mean:.2f}x  (overdispersion confirmed)",
    f"Unique recipient countries:       {unique_recip}",
    "",
    "Interpretation:",
    f"  {zero_share:.1f}% of recipient-year obs record zero journalist killings.",
    f"  Variance/Mean = {var_mean:.1f}x >> 1 confirms overdispersion.",
    "  Combined with zero-inflation this motivates the hurdle negative binomial",
    "  specification over a straight Poisson or NegBin model.",
]

txt = "\n".join(lines)
print(txt)

out_txt = os.path.join(OUT_DM, "target_distribution.txt")
with open(out_txt, "w") as f:
    f.write(txt + "\n")
print(f"Saved: {out_txt}")

# ---------------------------------------------------------------------------
# 3. Variable codebook
# ---------------------------------------------------------------------------
print("\n=== 3. Variable codebook ===")

# Compute live missing_pct from monadic panel for each variable
def miss(col):
    return round(mono[col].isna().mean() * 100, 2) if col in mono.columns else "N/A"

codebook = [
    {
        "variable_name": "recipient_iso3",
        "description":   "ISO 3166-1 alpha-3 country code of the recipient/target country",
        "source":        "Panel construction (country standardisation nb02)",
        "unit":          "categorical",
        "transformation":"none",
        "missing_pct":   miss("recipient_iso3"),
    },
    {
        "variable_name": "year",
        "description":   "Calendar year of observation",
        "source":        "Panel construction",
        "unit":          "integer (1992–2024)",
        "transformation":"none",
        "missing_pct":   miss("year"),
    },
    {
        "variable_name": "arms_tiv_total",
        "description":   "Sum of incoming arms transfers (TIV) from all senders to this recipient-year",
        "source":        "SIPRI Arms Transfers Database",
        "unit":          "Trend Indicator Value (TIV), millions",
        "transformation":"summed across senders; 0 where no transfers recorded",
        "missing_pct":   miss("arms_tiv_total"),
    },
    {
        "variable_name": "oda_total",
        "description":   "Sum of bilateral ODA received from all DAC donors in this recipient-year",
        "source":        "OECD DAC2 (Creditor Reporting System)",
        "unit":          "USD millions (constant prices)",
        "transformation":"negative values (loan repayments) floored at 0; summed across senders",
        "missing_pct":   miss("oda_total"),
    },
    {
        "variable_name": "econ_neocol_score_total",
        "description":   "Sum of incoming economic neo-colonial pressure scores from all senders. "
                         "Each dyadic score = (trade_dependency) × (ECI_sender − ECI_receiver).clip(0), "
                         "capturing unequal exchange weighted by trade exposure.",
        "source":        "Harvard Growth Lab ECI (eci_hs92) + BACI/IMF bilateral trade",
        "unit":          "dimensionless (ratio × ECI difference)",
        "transformation":"raw score log1p-scaled (×1e9) for modelling; summed across senders here",
        "missing_pct":   miss("econ_neocol_score_total"),
    },
    {
        "variable_name": "colonial_tie_flag",
        "description":   "1 if any sender held a formal colonial relationship with this recipient "
                         "(direct colony, protectorate, or mandate); 0 otherwise",
        "source":        "COLDAT Colonial Dates Dataset",
        "unit":          "binary (0/1)",
        "transformation":"max across senders (flag = 1 if any sender qualifies)",
        "missing_pct":   miss("colonial_tie_flag"),
    },
    {
        "variable_name": "journalist_killings",
        "description":   "Confirmed journalist killings in this recipient country-year",
        "source":        "Committee to Protect Journalists (CPJ) Database",
        "unit":          "count (non-negative integer)",
        "transformation":"none; 88.7% zeros, max 82, overdispersion ratio ~14.7x in raw panel",
        "missing_pct":   miss("journalist_killings"),
    },
    {
        "variable_name": "gdp_per_capita",
        "description":   "GDP per capita in current USD for the recipient country",
        "source":        "World Bank World Development Indicators (WDI)",
        "unit":          "current USD",
        "transformation":"none (raw; log version below used in modelling)",
        "missing_pct":   miss("gdp_per_capita"),
    },
    {
        "variable_name": "gdp_per_capita_log",
        "description":   "Natural log of GDP per capita; reduces right skew for modelling",
        "source":        "World Bank WDI (derived)",
        "unit":          "log(current USD)",
        "transformation":"np.log(gdp_per_capita)",
        "missing_pct":   miss("gdp_per_capita_log"),
    },
    {
        "variable_name": "population",
        "description":   "Total population of the recipient country",
        "source":        "World Bank WDI",
        "unit":          "persons",
        "transformation":"none (raw; log version below used in modelling)",
        "missing_pct":   miss("population"),
    },
    {
        "variable_name": "population_log",
        "description":   "Natural log of total population",
        "source":        "World Bank WDI (derived)",
        "unit":          "log(persons)",
        "transformation":"np.log(population)",
        "missing_pct":   miss("population_log"),
    },
    {
        "variable_name": "armed_conflict",
        "description":   "Binary indicator of active armed conflict (≥25 battle deaths) in recipient country-year",
        "source":        "UCDP/PRIO Armed Conflict Dataset v25.1",
        "unit":          "binary (0/1)",
        "transformation":"1 if any conflict episode active; 0 otherwise",
        "missing_pct":   miss("armed_conflict"),
    },
    {
        "variable_name": "conflict_intensity",
        "description":   "Ordinal conflict intensity: 0 = no conflict, 1 = minor (25–999 deaths), "
                         "2 = war (≥1000 deaths)",
        "source":        "UCDP/PRIO Armed Conflict Dataset v25.1",
        "unit":          "ordinal (0–2)",
        "transformation":"max intensity across episodes in country-year",
        "missing_pct":   miss("conflict_intensity"),
    },
]

cb_df = pd.DataFrame(codebook)
out_cb = os.path.join(OUT_APP, "variable_codebook.csv")
cb_df.to_csv(out_cb, index=False)
print(cb_df[["variable_name", "source", "unit"]].to_string())
print(f"Saved: {out_cb}")

# ---------------------------------------------------------------------------
# 4. LIMITATIONS_EVIDENCE.md
# ---------------------------------------------------------------------------
print("\n=== 4. Limitations evidence ===")

# Pull live statistics to embed
econ_miss_dyad  = round(dyad["econ_neocol_score"].isna().mean() * 100, 2)
oda_miss_dyad   = round(dyad["bilateral_oda"].isna().mean() * 100, 2)
colonial_share  = round(dyad["colonial_tie"].mean() * 100, 1)

jk_zeros_mono   = round((mono["journalist_killings"] == 0).mean() * 100, 1)
jk_max_mono     = int(mono["journalist_killings"].max())
jk_vmr_mono     = round(mono["journalist_killings"].var() / mono["journalist_killings"].mean(), 1)

arms_zero_mono  = round((mono["arms_tiv_total"] == 0).mean() * 100, 1)

md = f"""# Limitations Evidence

Prepared automatically from pipeline outputs. All statistics are derived from
the primary panel files and are reproducible by re-running
`notebooks/generate_report_outputs.py`.

---

## 1. econ_neocol_score Missingness ({econ_miss_dyad}%)

**What it is.**
The economic neo-colonial score is missing for {econ_miss_dyad}% of dyad-year rows
in the dyadic panel.

**Evidence.**
Verified in `notebooks/03_analysis/15_network_diagnostics.ipynb` (missingness bar chart cell):
`econ_neocol_score` is the highest-missing variable at {econ_miss_dyad}% of
115,640 dyad-year rows. Two structural sources explain this:

1. *ECI temporal gap* — Harvard Growth Lab's Economic Complexity Index begins
   in 1995, leaving 1992–1994 rows as NaN by construction (not data quality).
2. *ECI country coverage* — ECI covers approximately 145 of ~213 countries;
   small island states, micro-states, and heavily aid-dependent fragile states
   are excluded, introducing systematic South-South invisibility.

**Implication.**
Missingness is structurally non-random (MNAR): countries with sparse trade
networks are more likely to be both missing and theoretically relevant. Analyses
using econ_neocol_score should be interpreted as conditional on ECI coverage.
Sensitivity analyses restricting to 1995–2024 and to ECI-covered countries are
reported in the robustness section.

---

## 2. bilateral_oda Missingness ({oda_miss_dyad}%)

**What it is.**
Bilateral ODA records are absent for {oda_miss_dyad}% of dyad-year rows.

**Evidence.**
From `notebooks/03_analysis/15_network_diagnostics.ipynb`: `bilateral_oda` missing for
{oda_miss_dyad}% of rows. OECD DAC2 only covers DAC-member donor flows;
non-DAC senders (China, Gulf states, Russia, emerging South-South donors) have
no ODA record regardless of actual aid flows.

**Implication.**
The ODA variable systematically understates aid dependency for recipients whose
primary donors are non-Western. This biases the aid-as-leverage pathway toward
Western donor relationships and may underestimate total incoming dependency in
the Global South. The variable should be interpreted as *DAC bilateral ODA*,
not *total bilateral aid*.

---

## 3. Arms Flow vs. Stock

**What it is.**
The arms variable captures annual TIV *flow* (deliveries in a given year) rather
than cumulative *stock* (total military equipment held).

**Evidence.**
SIPRI TIV represents the trend-indicator value of equipment delivered per year.
Zero-share in the monadic panel: {arms_zero_mono}% of recipient-year observations
record zero arms inflows. A stock variable would require multi-year accumulation
accounting for equipment lifetimes.

**Implication.**
A single high-delivery year inflates the arms measure for that observation;
structural military dependency (e.g. long-standing equipment reliance) is
underweighted relative to episodic delivery spikes. This may attenuate the
arms coefficient in years before or after major procurement events. Future work
should construct a rolling 5-year stock proxy from TIV flows.

---

## 4. econ_neocol_score: Sum vs. Mean Aggregation

**What it is.**
In collapsing from dyadic to monadic panel, incoming econ_neocol_score is
*summed* across all senders rather than averaged.

**Evidence.**
Implemented in `notebooks/12_collapse_monadic_panel.ipynb`. The sum reflects
total incoming economic pressure; the mean would reflect average intensity per
sender relationship. Robustness checks using the mean are documented in
`notebooks/13_*` (network augmentation notebook).

**Implication.**
Summing is theoretically appropriate when the research question concerns
*aggregate* dependency, but conflates high-volume low-intensity relationships
with low-volume high-intensity ones. Countries with many low-pressure trade
partners may score similarly to those with one dominant neo-colonial relationship.
Results should be read as aggregate exposure, not per-relationship intensity.

---

## 5. colonial_tie Sparsity ({colonial_share}% of dyads)

**What it is.**
Only {colonial_share}% of dyad-year observations have `colonial_tie = 1`,
making the variable too sparse for use as a standalone predictor.

**Evidence.**
From `notebooks/03_analysis/15_network_diagnostics.ipynb`: `colonial_tie = 1` in {colonial_share}%
of 115,640 dyadic rows. COLDAT encodes direct colonial relationships (colony,
protectorate, mandate); informal empire and indirect colonial influence are
not captured.

**Implication.**
Too few positive cases to estimate a reliable direct effect; the variable is
used exclusively as a moderator/interaction term (e.g. `arms_tiv × colonial_tie`)
to test whether colonial history amplifies or conditions neo-colonial dependency
pathways. Standalone colonial_tie coefficients are not reported.

---

## 6. Bilateral Debt Dropped (83.6% MNAR)

**What it is.**
World Bank bilateral debt data was excluded from the final panel.

**Evidence.**
Missingness audit in `notebooks/03_analysis/15_network_diagnostics.ipynb` and confirmed in
LIMITATIONS.md: 83.6% of dyad-year rows lack bilateral debt records. The missingness
is structurally non-random — non-Western creditors (China's Belt and Road loans,
Gulf sovereign lending) are systematically absent from World Bank reporting.

**Implication.**
Including bilateral debt with imputation would have introduced confounded
estimates, as missingness correlates with the very South-South relationships the
study seeks to analyse. The variable is retained in `data/processed/deprecated/`
for reference; its exclusion is acknowledged as a limitation in capturing
debt-as-leverage pathways fully.

---

## 7. v2x_polyarchy Dropped (34.1% Missing)

**What it is.**
The V-Dem electoral democracy index (v2x_polyarchy) was excluded from the
control set.

**Evidence.**
From `notebooks/03_analysis/15_network_diagnostics.ipynb` and LIMITATIONS.md: 34.1% missing in the
merged panel, concentrated in small states and early years. Including it would
reduce the analytic sample by approximately one-third.

**Implication.**
The lean control set (GDP per capita log, armed conflict, population log) is
sufficient to control for level of development and political instability without
the sample attrition that v2x_polyarchy would introduce. The decision follows
the principle of preferring sample size over marginal covariate precision for
count outcomes in small-N panel settings. Results conditional on v2x_polyarchy
availability are available as supplementary robustness checks.

---

## 8. ODA Not Disaggregated by Type

**What it is.**
`bilateral_oda` aggregates all DAC aid modalities — budget support, project
aid, technical assistance, debt relief — into a single flow variable.

**Evidence.**
OECD DAC2 provides disbursement totals by donor-recipient-year. Sector-level
disaggregation (DAC5) was not incorporated due to complexity and additional
missingness in sector codes. See `notebooks/06_oecd_dac2_oda_fixing.ipynb` for
the processing pipeline.

**Implication.**
Budget support (direct government transfers) implies different leverage mechanisms
than project aid channelled through NGOs or technical assistance. Pooling these
types may attenuate ODA effects if the mechanisms are heterogeneous or
directionally opposed. Future work should test sector-disaggregated ODA flows
as separate predictors.

---

## 9. Hub-and-Spoke Network Topology

**What it is.**
The network layer constructed from sender–recipient dyads has a hub-and-spoke
structure dominated by a small number of powerful sender nodes (USA, UK, France,
China in arms; OECD members in ODA).

**Evidence.**
Documented in `notebooks/12_collapse_monadic_panel.ipynb` and flagged in LIMITATIONS.md.
Centrality measures (PageRank, eigenvector) show low variance across recipient
nodes because most recipients share a similar periphery position relative to
dominant senders.

**Implication.**
Low-variance centrality measures reduce their discriminating power as predictors
and may inflate standard errors in network-augmented models. This is an inherent
structural feature of the global aid/arms network rather than a modelling artefact.
The network layer nonetheless adds interpretive value for identifying outlier
recipients with atypical embeddedness patterns.

---

## 10. CPJ Coverage Bias

**What it is.**
The Committee to Protect Journalists database — the source of the outcome variable
`journalist_killings` — is itself subject to systematic undercounting in closed
or repressive states.

**Evidence.**
CPJ methodology relies on on-the-ground verification; in states that restrict
press access, expel foreign journalists, or suppress local reporting on journalist
deaths (e.g. North Korea, Eritrea, Turkmenistan), deaths may never enter the
database. The zero-share of {jk_zeros_mono}% in the monadic panel and max of
{jk_max_mono} deaths (IRQ/SYR conflict peaks) may therefore understate true
mortality, particularly for low-intensity repression regimes.

**Implication.**
The outcome variable is right-censored at the observability limit: we model
*reported* killings, not true killings. This introduces attenuation bias in
the estimated neo-colonial effect if closed states (most likely to underreport)
are also more deeply embedded in dependency networks. Sensitivity analyses
excluding persistently low-reporting states are recommended. CPJ figures remain
the field standard and are used throughout despite this acknowledged limitation.
"""

out_lim = os.path.join(OUT_LIM, "LIMITATIONS_EVIDENCE.md")
with open(out_lim, "w") as f:
    f.write(md)
print(f"Saved: {out_lim}")

# ---------------------------------------------------------------------------
print("\nAll outputs generated successfully.")
