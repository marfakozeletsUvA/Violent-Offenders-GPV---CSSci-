# Limitations Evidence

Prepared automatically from pipeline outputs. All statistics are derived from
the primary panel files and are reproducible by re-running
`notebooks/generate_report_outputs.py`.

---

## 1. econ_neocol_score Missingness (30.42%)

**What it is.**
The economic neo-colonial score is missing for 30.42% of dyad-year rows
in the dyadic panel.

**Evidence.**
Verified in `notebooks/03_analysis/15_network_diagnostics.ipynb` (missingness bar chart cell):
`econ_neocol_score` is the highest-missing variable at 30.42% of
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

## 2. bilateral_oda Missingness (10.2%)

**What it is.**
Bilateral ODA records are absent for 10.2% of dyad-year rows.

**Evidence.**
From `notebooks/03_analysis/15_network_diagnostics.ipynb`: `bilateral_oda` missing for
10.2% of rows. OECD DAC2 only covers DAC-member donor flows;
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
Zero-share in the monadic panel: 43.2% of recipient-year observations
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
Implemented in `notebooks/02_pipeline/12_collapse_monadic_panel.ipynb`. The sum reflects
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

## 5. colonial_tie Sparsity (3.8% of dyads)

**What it is.**
Only 3.8% of dyad-year observations have `colonial_tie = 1`,
making the variable too sparse for use as a standalone predictor.

**Evidence.**
From `notebooks/03_analysis/15_network_diagnostics.ipynb`: `colonial_tie = 1` in 3.8%
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
missingness in sector codes. See `notebooks/01_preprocessing/06_oecd_dac2_oda_fixing.ipynb` for
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
Documented in `notebooks/02_pipeline/12_collapse_monadic_panel.ipynb` and flagged in LIMITATIONS.md.
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
database. The zero-share of 88.7% in the monadic panel and max of
82 deaths (IRQ/SYR conflict peaks) may therefore understate true
mortality, particularly for low-intensity repression regimes.

**Implication.**
The outcome variable is right-censored at the observability limit: we model
*reported* killings, not true killings. This introduces attenuation bias in
the estimated neo-colonial effect if closed states (most likely to underreport)
are also more deeply embedded in dependency networks. Sensitivity analyses
excluding persistently low-reporting states are recommended. CPJ figures remain
the field standard and are used throughout despite this acknowledged limitation.
