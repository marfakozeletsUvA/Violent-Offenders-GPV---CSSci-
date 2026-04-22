# Data Sources

This document contains all datasets used in the Neo-Colonial Networks and Journalist Violence project.

**Analysis window:** 1992–2024

---

## Target Variable

### Committee to Protect Journalists (CPJ)
- **What**: Journalist killings worldwide
- **Coverage**: Global, 1992–present
- **Unit**: Incident-level (aggregated to country-year)
- **Access**: Download
- **Processed file**: `target_journalist_killings.csv`
- **Links**:
  - Database: https://cpj.org/data/
- **APA 7 citation**:
  > Committee to Protect Journalists. (2025). *CPJ's database of attacks on the press* [Data set]. https://cpj.org/data/

---

## Military Ties Layer

### SIPRI Arms Transfers Database
- **What**: International transfers of major conventional weapons (trend-indicator values, TIV)
- **Coverage**: Global, 1950–2024
- **Unit**: Supplier-recipient-year
- **Role**: Time-varying dyadic measure of military dependency
- **Access**: Download
- **Processed file**: `sipri_arms_flows.csv`
- **Links**:
  - Transfer Register: https://armstransfers.sipri.org/ArmsTransfer/TransferRegister
  - Sources and methods: https://www.sipri.org/databases/armstransfers/sources-and-methods
- **APA 7 citation**:
  > Stockholm International Peace Research Institute. (2025). *SIPRI Arms Transfers Database* [Data set]. https://www.sipri.org/databases/armstransfers


---

## Economic Ties Layer

### OECD DAC Bilateral ODA (DAC2A)
- **What**: Bilateral Official Development Assistance disbursements from DAC donor countries to recipient countries
- **Coverage**: Global, 1960–present
- **Unit**: Donor-recipient-year
- **Role**: Time-varying dyadic measure of economic dependency (aid flows)
- **Note**: Negative values (loan repayment entries, 4.1% of rows) floored at 0 — not meaningful under donor leverage framework
- **Access**: Download via OECD Data Explorer
- **Processed file**: *to be created*
- **Links**:
  - Data Explorer: https://data-explorer.oecd.org/
  - Dataset: Aid (ODA) disbursements to countries and regions [DAC2a]
  - Methodology: https://one.oecd.org/document/DCD/DAC/STAT(2020)44/FINAL/en/pdf
- **APA 7 citation**:
  > Organisation for Economic Co-operation and Development. (2025). *Aid (ODA) disbursements to countries and regions [DAC2a]* [Data set]. OECD Data Explorer. https://data-explorer.oecd.org/

### ECI (Harvard Growth Lab — Atlas of Economic Complexity)
- **What**: Economic Complexity Index rankings by country-year, measuring the knowledge intensity of a country's export basket
- **Coverage**: 145 countries, 1995–2024
- **Unit**: Country-year
- **Role**: Used to compute complexity asymmetry component of econ_neocol_score (ECI_sender − ECI_receiver, floored at 0)
- **Raw file**: `data/raw/economic/eci-rankings-raw.csv`, column `eci_hs92`
- **Merge key**: iso3 + year
- **Links**:
  - https://atlas.cid.harvard.edu/
- **APA 7 citation**:
  > The Growth Lab at Harvard University. (2019). *International Trade Data (HS, 92)* [Data set]. Harvard Dataverse. https://doi.org/10.7910/DVN/T4CHWJ

---

## Colonial History Layer

### COLDAT (Colonial Dates Dataset)
- **What**: Colonial relationships between European colonizers and colonies, including start/end dates of colonial rule
- **Coverage**: Historical (European colonial empires, all currently independent states)
- **Unit**: Colony-colonizer dyad
- **Role**: Static binary layer used to weight military and economic ties (identifies neo-colonial patron-client channels)
- **Access**: Download
- **Processed file**: `coldat_colonial_ties.csv`
- **Links**:
  - Harvard Dataverse: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T9SDEW
  - Author page: https://www.beckerbastian.net/data
- **APA 7 citation**:
  > Becker, B. (2020). Introducing COLDAT: The Colonial Dates Dataset. *SOCIUM/SFB1342 Working Paper Series*, 02/2019. https://doi.org/10.7910/DVN/T9SDEW

---

## Control Variables

### V-Dem (Varieties of Democracy)
- **Status**: Dropped from model — 34.1% missingness shrinks analytical sample significantly; lean control set (GDP, population, conflict) is more defensible; see Removed Datasets table below
- **APA 7 citation** (retained for reference):
  > Coppedge, M., Gerring, J., Knutsen, C. H., Lindberg, S. I., Teorell, J., Altman, D., Bernhard, M., Cornell, A., Fish, M. S., Gastaldi, L., Gjerløw, H., Glynn, A., God, A. G., Grahn, S., Hicken, A., Kinzelbach, K., Krusell, J., Marquardt, K. L., McMann, K., … Ziblatt, D. (2025). *V-Dem dataset v15* [Data set]. Varieties of Democracy (V-Dem) Project. https://doi.org/10.23696/vdemds25

### World Bank World Development Indicators (WDI)
- **What**: GDP per capita (constant USD) and total population
- **Coverage**: Global, 1960–present
- **Unit**: Country-year
- **Role**: Control variables — economic development and population as exposure control
- **Access**: Download
- **Processed file**: *to be created*
- **Links**:
  - GDP per capita: https://data.worldbank.org/indicator/NY.GDP.PCAP.KD
  - Population: https://data.worldbank.org/indicator/SP.POP.TOTL
- **APA 7 citation**:
  > World Bank. (2025). *World Development Indicators* [Data set]. https://data.worldbank.org/

  ### UCDP Dyadic Dataset v25.1
- **What**: Dyad-year data on armed conflicts where at least one party is a state government; records opposing actors, conflict location, intensity level, and type
- **Coverage**: Global, 1946–2024
- **Unit**: Dyad-year (government vs. opposition actor)
- **Role**: Cumulative/windowed conflict presence indicator (military layer predictor)
- **Access**: Download
- **Processed file**: *to be created*
- **Links**:
  - Download: https://ucdp.uu.se/downloads/
  - Codebook: https://ucdp.uu.se/downloads/dyadic/ucdp-dyadic-251.pdf
- **APA 7 citations** (cite both):
  > Davies, S., Pettersson, T., Sollenberg, M., & Öberg, M. (2025). Organized violence 1989–2024, and the challenges of identifying civilian victims. *Journal of Peace Research*, *62*(4).
  >
  > Harbom, L., Melander, E., & Wallensteen, P. (2008). Dyadic dimensions of armed conflict, 1946–2007. *Journal of Peace Research*, *45*(5), 697–710. https://doi.org/10.1177/0022343308094331

---

## Final Dataset Summary

| Layer | Dataset | Structure | Coverage | Role |
|-------|---------|-----------|----------|------|
| Target | CPJ | Country-year | 1992–present | Journalist killings (DV) |
| Military | SIPRI | Supplier-recipient-year | 1950–2024 | Arms transfers (time-varying, dyadic) |
| Military | UCDP Dyadic v25.1 | Dyad-year | 1946–2024 | Armed conflict presence (cumulative) |
| Economic | OECD DAC (DAC2A) | Donor-recipient-year | 1960–present | Bilateral aid flows (time-varying, dyadic) |
| Economic | ECI (Harvard Growth Lab) | Country-year | 1995–2024 | Complexity asymmetry in econ_neocol_score |
| Colonial | COLDAT | Colony-colonizer | Historical | Colonial relationship (static, binary) |
| Control | World Bank WDI | Country-year | 1960–present | GDP per capita, population |

---

## Datasets Removed from Earlier Versions (Documented for Reference)

| Dataset | Reason for removal |
|---------|-------------------|
| Military Intervention Project (MIP) | US-only coverage; ends 2019; replaced by UCDP Dyadic |
| UCDP External Support Dataset (ESD) | Ends 2017; replaced by UCDP Dyadic for conflict presence |
| AidData Core Research Release | Ends 2013 (binding constraint on analysis window); replaced by OECD DAC |
| World Bank Bilateral Debt (IDS) | 83.6% MNAR; South-South debt structurally invisible; dropped |
| V-Dem (v2x_polyarchy) | 34.1% missing; shrinks analytical sample; lean control set preferred |
| World Bank Net Bilateral ODA | Aggregate (not dyadic); no longer needed as control since OECD DAC covers aid |
| UN Comtrade | Trade flows don't cleanly capture asymmetric dependency |

---

*Last updated: April 2026*