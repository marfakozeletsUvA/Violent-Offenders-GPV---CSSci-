# Data Sources

This document contains all datasets used in the Neo-Colonial Networks and Journalist Violence project.

---

## Target Variable (Outcome)

### Committee to Protect Journalists (CPJ)
- **What**: Journalist killings
- **Coverage**: Global, 1992–2026
- **Unit**: Incident-level (aggregated to country-year)
- **Access**: Download
- **Processed file**: `target_journalist_killings.csv`
- **Links**:
  - Database: https://cpj.org/data/ -> downloaded

---

## Military Ties Layer

### SIPRI Arms Transfers Database
- **What**: International transfers of major conventional weapons
- **Coverage**: Global, 1990–2024 (filtered)
- **Unit**: Supplier-recipient-year (TIV values)
- **Access**: Download
- **Processed file**: `sipri_arms_flows.csv`
- **Links**:
  - Transfer Register: https://armstransfers.sipri.org/ArmsTransfer/TransferRegister -> downloaded

### Military Intervention Project (MIP)
- **What**: US military interventions
- **Coverage**: US only, 1990–2019 (filtered)
- **Unit**: Intervention-level
- **Access**: Download
- **Processed file**: `mip_us_interventions.csv`
- **Links**:
  - Tufts CSS: https://sites.tufts.edu/css/?page_id=682 -> downloaded

### UCDP External Support Dataset (ESD)
- **What**: External support (troops, weapons, training, funding) to conflict parties from state and non-state actors
- **Coverage**: Global, 1990–2017 (filtered)
- **Unit**: Triad-year (supporter–recipient–opponent–year)
- **Access**: Download
- **Processed file**: `ucdp_external_support.csv`
- **Links**:
  - Data: https://ucdp.uu.se/downloads/ -> downloaded
  - Codebook: https://ucdp.uu.se/downloads/extsup/ESD/ucdp-esd-181.pdf

---

## Economic Ties Layer

### AidData Core Research Release
- **What**: Bilateral aid flows from 96 donors
- **Coverage**: Global, 1990–2013 (filtered)
- **Unit**: Donor-recipient-year
- **Access**: Download
- **Processed file**: `aiddata_bilateral_flows.csv`
- **Links**:
  - Datasets: https://www.aiddata.org/data/aiddata-core-research-release-level-1-3-1 -> downloaded

### World Bank Net Bilateral ODA
- **What**: Total net bilateral ODA received per country (control variable, not dyadic)
- **Coverage**: Global, 1990–2023
- **Unit**: Recipient-country-year
- **Access**: Download
- **Processed file**: `oda_received_by_country.csv`
- **Links**:
  - Data: https://data.worldbank.org/indicator/DC.DAC.TOTL.CD -> downloaded

---

## Colonial History Layer

### COLDAT (Colonial Dates Dataset)
- **What**: Colonial relationships between colonizers and colonies
- **Coverage**: Historical (European colonial empires)
- **Unit**: Colony-colonizer dyad
- **Access**: Download
- **Processed file**: `coldat_colonial_ties.csv`
- **Links**:
  - Harvard Dataverse: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T9SDEW -> downloaded

---

## Processed Data Summary

| File | Source | Structure | Rows | Coverage |
|------|--------|-----------|------|----------|
| `target_journalist_killings.csv` | CPJ | country-year | ~1,200 | 1992–2026 |
| `sipri_arms_flows.csv` | SIPRI | supplier-recipient-year | ~28,000 | 1990–2024 |
| `mip_us_interventions.csv` | MIP | intervention-level | 146 | 1990–2019 |
| `ucdp_external_support.csv` | UCDP ESD | supporter-target-year | 6,899 | 1990–2017 |
| `aiddata_bilateral_flows.csv` | AidData | donor-recipient-year | 82,112 | 1990–2013 |
| `oda_received_by_country.csv` | World Bank | recipient-year | 6,679 | 1990–2023 |
| `coldat_colonial_ties.csv` | COLDAT | colony-colonizer | ~160 | Historical |

---

## Not Used (Documented for Reference)

### MIPS (Military Intervention by Powerful States)
- **Status**: Could not locate accessible download
- **Alternative**: UCDP ESD provides similar global coverage

### OECD DAC (Bilateral ODA)
- **Status**: Download too large 
- **Alternative**: AidData provides dyadic aid flows

### World Bank IDS (Debt Statistics)
- **Status**: Not downloaded (time constraints)
- **Potential use**: Future refinement of economic dependency measure

### UN Comtrade (Trade Flows)
- **Status**: Not downloaded (time constraints)
- **Potential use**: Future refinement of economic dependency measure

---

*Last updated: February 2025*