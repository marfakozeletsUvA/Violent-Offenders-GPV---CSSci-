# Data Sources

> Links to datasets, documentation, and relevant papers for the Violence Against Journalists project.

---

## Core Datasets: Journalist Violence

### Committee to Protect Journalists (CPJ)
- **URL:** https://cpj.org/data/
- **Coverage:** Global
- **Contains:** Journalists killed database
- **Notes:** Alternative/supplement to RSF


---

## Colonial layer

### COLDAT
- **URL:** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/T9SDEW
- **Contains:** Historical colonial ties, start and end of colonisation
- **Notes:** Base layer

---

## Military layer

### SIPRI Arms Transfers Database
- **URL:** https://www.sipri.org/databases/armstransfers
- **Coverage:** 1950-present
- **Contains:** International arms trade flows
- **Notes:** Track military relationships between countries

### UCDP External Support Dataset
- **URL:** https://ucdp.uu.se/downloads/index.html (scroll to ESD)
- **Coverage:** 1975-2017
- **Contains:** External support to warring parties (who supports whom)
- **Format:** Excel, Stata
- **Citation:** Meier et al. (2022)
- **Notes:** Gold for network construction — tracks triad relationships (supporter → recipient → opponent)

### Military Intervention Project (MIP)
- **URL:** https://sites.tufts.edu/css/?page_id=1582
- **Paper:** Kushi & Toft (2023) "Introducing the Military Intervention Project" *Journal of Conflict Resolution*
- **Coverage:** US interventions 1776-2019
- **Contains:** ~400 US military interventions with 200+ variables
- **Kaggle mirror:** https://www.kaggle.com/datasets/konradb/us-military-interventions
- **Notes:** US-only but very comprehensive; includes overt and covert interventions

---

### Economic layer

### AidData
- **URL:** https://www.aiddata.org/datasets
- **Coverage:** 1990-2013, annual
- **Contains:** Bilateral aid flows
- **Notes:** Dependency on financial aid from other countries

### World Bank Group - Debt
- **URL:** https://www.worldbank.org/en/programs/debt-statistics/ids
- **Coverage:** ~1970-2024, annual
- **Contains:** Country debt-creditor relationship and debt owned
- **Notes:** Financial dependency by loans etc.

### IMF International Trade in Goods (IMTS)
- **URL:** https://data.imf.org/en/datasets/IMF.STA:IMTS
- **Coverage:** 1940/50-2025, annual
- **Contains:** International trade flows in goods and merchandise
- **Notes:** Contains military goods as well (!)

### WTO-OECD Balanced Trade in Services Dataset (BaTiS) — BPM6
- **URL:** https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm
- **Coverage:** 2005-2024, annual
- **Contains:** International trade flows in services (intangible products)
- **Notes:** Includes 200+ reporters and partners, covers 26 EBOPS 2010 categories + total services

---

## Control Variables

### Fragile States Index
- **URL:** https://fragilestatesindex.org/excel/
- **Coverage:** 2006-present, annual
- **Contains:** Composite fragility scores across 12 indicators
- **Notes:** Good proxy for destabilization outcomes

### V-Dem (Varieties of Democracy)
- **URL:** https://www.v-dem.net/data/
- **Contains:** Democracy indices, press freedom measures, rule of law
- **Notes:** Very granular — could use their media freedom variables

### World Bank Governance Indicators
- **URL:** https://info.worldbank.org/governance/wgi/
- **Contains:** Rule of law, control of corruption, government effectiveness
- **Notes:** Standard country-level controls

### Freedom House Press Freedom
- **URL:** https://freedomhouse.org/report/freedom-press
- **Contains:** Annual press freedom scores
- **Notes:** Binary (free/partly free/not free) + detailed scores

### UCDP One-sided Violence Dataset
- **URL:** https://ucdp.uu.se/downloads/index.html#onesided
- **Coverage:** 1989-2024
- **Contains:** Intentional attacks on civilians by governments and armed groups
- **Notes:** Could be useful for context on state violence patterns

### UCDP Georeferenced Event Dataset (GED)
- **URL:** https://ucdp.uu.se/downloads/index.html#ged_global
- **Coverage:** 1989-2024, event-level
- **Contains:** Individual events of organized violence, geocoded
- **Notes:** Most granular — use if we need event-level analysis

### UCDP/PRIO Armed Conflict Dataset
- **URL:** https://ucdp.uu.se/downloads/index.html#armedconflict
- **Coverage:** 1946-2024
- **Contains:** Conflict-year data where at least one party is a state government
- **Format:** CSV, Excel, Stata, R
- **Citation:** Gleditsch et al. (2002); Davies et al. (2025)
- **Notes:** Start here — cleanest country-year conflict data

### OECD ODA
- **URL:** https://www.aiddata.org/datasets
- **Coverage:** 1960-present, annual
- **Contains:** Development assistance received
- **Notes:** Useful to control for which countries receive aid in general

---

## Key Papers

### On Violence Against Journalists
- Relly & González de Bustamante (2017). "Global and Domestic Networks Advancing Prospects for Institutional and Social Change: The Collective Action Response to Violence Against Journalists." *Journalism & Communication Monographs* 19(2): 84-152.
  - **Notes:** Uses network framework qualitatively — we can operationalize quantitatively

### On Military Intervention Data
- Kushi, S. & Toft, M.D. (2023). "Introducing the Military Intervention Project: A New Dataset on US Military Interventions, 1776–2019." *Journal of Conflict Resolution* 67(4): 752-779.

### On UCDP Data
- Davies, S., Pettersson, T., Sollenberg, M., & Öberg, M. (2025). "Organized violence 1989–2024." *Journal of Peace Research* 62(4).

---

*Last updated: February 2025*
