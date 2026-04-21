# Limitations & Methodological Notes
Running log for final report writeup. Append as issues are identified.

---

## Data Coverage

**ECI 1992–1994 gap**
ECI data starts 1995; panel starts 1992. econ_neocol_score is NaN for all
dyads in 1992–1994. These rows are excluded from the economic network layer.
Documented as limitation, no imputation applied. 8,104 affected rows
confirmed via decomposition of econ_neocol_score NaNs.

**ECI country coverage (68 missing recipients)**
ECI covers 145 countries. 68 recipient countries (mostly small island states
and fragile states: ABW, BDI, CAF, COM, BRB, BTN etc.) have no ECI scores.
econ_neocol_score is NaN for all dyads where these are the receiver.
Treated as NaN by design — imputing would introduce false precision.

**Bilateral debt dropped**
World Bank IDS bilateral debt excluded (83.6% MNAR). Missingness is not
random — only major creditor nations tracked, making South-South debt
structurally invisible. Including it would bias the model.

**econ_neocol_score missingness (30.4% NaN)**
Decomposed: 8,104 rows year <1995 (ECI gap), 28,262 rows country not in ECI
(68 recipients, mostly small island and fragile states), 1,749 rows no
recorded trade, 1,883 rows missing GDP. Analytical sample for economic layer
is 141 countries, not 213. NaN by design, no imputation applied.

**v2x_polyarchy 34.1% missing**
Affects 90 countries entirely (mostly regional aggregates and micro-states,
none present in CPJ data). Including this control materially reduces
modelling sample. Decision: drop from model. 34.1% missingness shrinks analytical sample
significantly, framework does not require a democracy measure, and lean
control set (GDP, population, conflict) is more defensible. Removing
reduces over-control risk.

**PRK and TWN — no GDP data**
North Korea and Taiwan appear in the panel but have no GDP data in
controls_merged.csv. Silently excluded from any model using controls.
Neither appears in CPJ data so no effect on outcome coverage.

---

## Panel Structure

**Sender constraint (112 senders, 213 recipients)**
Panel built from SIPRI arms transfers and bilateral aid flows, which are
inherently asymmetric. Global South countries (Mali, Chad, Niger etc.)
appear only as recipients. This is a structural feature of the data that
aligns with the theoretical framework — the panel captures directional
neo-colonial dependency relationships, not symmetric bilateral ties.

**Fully-covered analytical sample is 81 countries**
Only 81 of 213 panel recipients appear in all 5 layers simultaneously (arms,
ODA, econ_neocol_score, controls, CPJ). 132 recipients are partial or absent
across at least one layer. Core modelling sample will be substantially
smaller than the full panel.

**98 recipients have zero CPJ killings on record**
True structural zeros in the outcome, not missing data. These countries
receive arms and/or aid but have no journalist killings recorded by CPJ.

**35 recipients absent from both SIPRI and ODA**
Extremely small or isolated states with no recorded arms or aid flows.
Present in panel as recipients of colonial ties or trade only.

**China as sender**
China appears among top 20 senders despite Global South
self-identification. Retained — it is a major arms and aid exporter to
the Global South, which the neo-colonial framework is designed to capture.

**Israel as sender**
ISR appears as a sender primarily through arms exports. Theoretically
ambiguous in the neo-colonial framing. Flag in discussion section.

---

## Variable Construction

**econ_neocol_score directionality**
Score is directional (sender → receiver). Bilateral trade values are
symmetric (sum of both flows) but directionality comes from which country
is assigned as receiver for ECI and GDP. Monadic collapse sums incoming
scores per recipient-year — correct direction for predicting journalist
killings in the recipient country.

**GDP denominator**
Total GDP derived as gdp_per_capita × population (no total GDP column
in controls). Standard trade-to-GDP ratio approach.

**COLDAT sparsity**
Only 3.8% of dyads have colonial_tie=1. Used exclusively as
interaction/moderator term — never as standalone predictor.

**econ_neocol_score extreme right skew**
Max 3.5e-5 vs median 3.9e-9 — four orders of magnitude. Japan→Liberia 1995
spike driven by near-zero GDP (~$135M) during civil war amplifying the
trade-to-GDP ratio. Log transformation to be applied before modelling.
Winsorisation as alternative robustness check.

**Colonial layer — no coloniser ISO3**
COLDAT stores colonisers as lowercase strings (britain, france, etc.), not
ISO3 codes. Cannot be used as a directed sender-keyed edge in the ISO3
framework without a manual name→ISO3 mapping. Used as binary
recipient-level flag only.

**bilateral_oda 10.2% NaN in panel**
Structural NaNs for non-donor senders (China, arms exporters with no ODA
records). Not random missingness — reflects the donor/non-donor split
in the sender set.

---

## Military Layer

**SIPRI TIV right-skewed**
Max TIV 3,895 (Russia→India 2012) vs median 13.2. Russia→India 2012/2013
and USA→Saudi Arabia 2017 are extreme values. Log transformation to be
considered alongside econ_neocol_score before modelling.

**arms_tiv structural sparsity**
Only 10.5% of dyad-rows have arms_tiv > 0. Expected given most country-pairs
have no arms transfers. Zero treated as genuine observed zero, not missing.

---

## Modelling

**Conflict as control and potential mediator**
Armed conflict variable is both a control and a potential mediator of
the military pathway. Run models with and without as robustness check.

**Hub-and-spoke network topology**
Colonial networks produce hub-and-spoke structure where weighted
in-degree centrality risks replicating raw bilateral variables.
Acknowledged limitation — addressed in limitations section rather
than causing methodology change.

**Bayesian layer deferred**
PyMC/Bayesian hierarchical model deprioritized — M1 Air C compilation
fails under macOS Tahoe. Considered future extension only.

---

## Outcome Variable

**CPJ coverage bias**
CPJ data starts 1992 (left binding constraint for panel). CPJ reporting
may undercount killings in countries with limited press access —
structural underreporting in the most repressive states.

**CPJ zero construction**
CPJ encodes positive killings only — zeros are structural absences filled
via left join onto the base panel. Merge confirmed correct (0 NaNs in
journalist_killings, 83.29% genuine zeros). Zero-inflation is an empirical
property of the outcome, not a data quality issue. Hurdle model chosen
specifically to handle this two-process structure (zero vs non-zero, then
count intensity).

**ISR 2023–2025 extreme outliers**
Israel 2023–2025 killings (74, 82, 53) driven by Gaza conflict dominate the
top of the distribution. Will have outsized leverage in regression.
Robustness check: run full model on complete sample, then re-run
excluding ISR 2023–2025 rows, compare coefficients and effect sizes.
If results hold direction and significance, robustness confirmed.
Report both sets of results in appendix.
Flag as known leverage point in modelling section.