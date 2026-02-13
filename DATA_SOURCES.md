# Data Sources

This document contains all datasets used in the Neo-Colonial Networks and Journalist Violence project.

---

## Target Variable (Outcome)

### Committee to Protect Journalists (CPJ)
- **What**: Journalist killings, imprisonments, and missing persons
- **Coverage**: Global, 1992–present
- **Unit**: Incident-level (aggregate to country-year)
- **Access**: API + download
- **Links**:
  - Database: https://cpj.org/data/
  - API documentation: https://cpj.org/data-api/
  - Methodology: https://cpj.org/data-methodology/

---

## Military Ties Layer

### SIPRI Arms Transfers Database
- **What**: International transfers of major conventional weapons
- **Coverage**: Global, 1950–2024
- **Unit**: Supplier-recipient-year (USD TIV values)
- **Access**: Download
- **Links**:
  - Database: https://armstransfers.sipri.org/
  - Overview: https://www.sipri.org/databases/armstransfers
  - Also via World Bank: https://data.worldbank.org/indicator/MS.MIL.XPRT.KD

### Military Intervention Project (MIP)
- **What**: US military interventions
- **Coverage**: US only, 1776–2019
- **Unit**: Intervention-level (200+ variables)
- **Access**: Download
- **Links**:
  - Tufts CSS: https://sites.tufts.edu/css/?page_id=682
  - Kaggle mirror: https://www.kaggle.com/datasets/konradb/us-military-interventions
  - Paper: https://journals.sagepub.com/doi/10.1177/00220027221117546

### Military Intervention by Powerful States (MIPS)
- **What**: Interventions by US, UK, France, China, Russia
- **Coverage**: Major powers, 1946–2003
- **Unit**: Intervention-level
- **Access**: Download
- **Links**:
  - Data: https://plsullivan.web.unc.edu/data/

---

## Economic Ties Layer

### OECD DAC Aid Flows
- **What**: Bilateral Official Development Assistance (ODA)
- **Coverage**: DAC donors to recipients, 1960–present
- **Unit**: Donor-recipient-year
- **Access**: API + bulk download
- **Links**:
  - Data explorer: https://data-explorer.oecd.org/
  - Overview: https://www.oecd.org/dac/financing-sustainable-development/development-finance-data/
  - Also via World Bank: https://data.worldbank.org/indicator/DC.DAC.TOTL.CD

### AidData
- **What**: Aid flows including China (often missing from OECD)
- **Coverage**: Global, varies by dataset
- **Unit**: Project-level
- **Access**: Download
- **Links**:
  - Datasets: https://www.aiddata.org/datasets

### World Bank International Debt Statistics (IDS)
- **What**: Bilateral debt relationships
- **Coverage**: Global, varies
- **Unit**: Creditor-debtor-year
- **Access**: Download
- **Links**:
  - Data: https://data.worldbank.org/products/ids
  - DataBank: https://databank.worldbank.org/source/international-debt-statistics

### UN Comtrade
- **What**: Bilateral trade flows
- **Coverage**: Global, 1962–present
- **Unit**: Reporter-partner-year-commodity
- **Access**: API
- **Links**:
  - Database: https://comtradeplus.un.org/

---

## Colonial History Layer

### COLDAT (Colonial Dates Dataset)
- **What**: Aggregated colonial relationships from multiple sources
- **Coverage**: Historical (European colonial empires)
- **Unit**: Colony-colonizer
- **Access**: Download
- **Links**:
  - Harvard Dataverse: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T9SDEW

### ICOW Colonial History Data
- **What**: Primary colonial ruler for each state
- **Coverage**: COW system states, 1816–2018
- **Unit**: State-level
- **Access**: Download
- **Links**:
  - Data: http://www.paulhensel.org/icowcol.html
  - Also on Harvard Dataverse: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/5EMETG

---

## Potential Control Variables

### V-Dem (Varieties of Democracy)
- **What**: Democracy and governance indicators
- **Coverage**: Global, 1789–present
- **Links**: https://www.v-dem.net/

### World Bank Development Indicators
- **What**: GDP, population, economic indicators
- **Coverage**: Global
- **Links**: https://data.worldbank.org/

### UCDP (Uppsala Conflict Data Program)
- **What**: Armed conflict data
- **Coverage**: Global, 1946–present
- **Links**: https://ucdp.uu.se/

---

## Data Layer Summary

| Layer | Dataset | Key Variable | Temporal Coverage |
|-------|---------|--------------|-------------------|
| Target | CPJ | Killings, imprisonments | 1992–present |
| Military | SIPRI | Arms transfers (USD) | 1950–2024 |
| Military | MIP | US interventions (count) | 1776–2019 |
| Military | MIPS | Major power interventions | 1946–2003 |
| Economic | OECD DAC | Aid (% of GDP) | 1960–present |
| Economic | World Bank IDS | Bilateral debt | Varies |
| Economic | UN Comtrade | Trade flows | 1962–present |
| Colonial | COLDAT | Colonial relationship | Historical |
| Colonial | ICOW | Colonial ruler | Historical |

---

*Last updated: February 2025*
