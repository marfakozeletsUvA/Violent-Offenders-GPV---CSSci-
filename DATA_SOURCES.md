# Data Sources

> Links to datasets, documentation, and relevant papers for the Violence Against Journalists project.

---

## 📰 Core Datasets: Journalist Violence

### RSF Press Freedom Barometer
- **URL:** https://rsf.org/en/barometer
- **Coverage:** Global, 1995-present
- **Contains:** Journalists killed, detained, held hostage, missing
- **Variables:** Country, outcome type, gender, professional status, context
- **Notes:** 30 years of global data, good for our intervention-affected countries

### Mapping Media Freedom
- **URL:** https://www.mappingmediafreedom.org/
- **Coverage:** Europe-focused, 2014-present
- **Contains:** Incidents of media freedom violations
- **Variables:** Incident type (verbal/physical/legal/property), perpetrator type, context, journalist demographics
- **Notes:** 5,000+ incidents since 2020 — may be too Europe-focused for intervention analysis

### Committee to Protect Journalists (CPJ)
- **URL:** https://cpj.org/data/
- **Coverage:** Global
- **Contains:** Journalists killed database
- **Notes:** Alternative/supplement to RSF

---

## 🔫 Conflict & Intervention Datasets

### UCDP/PRIO Armed Conflict Dataset
- **URL:** https://ucdp.uu.se/downloads/index.html#armedconflict
- **Coverage:** 1946-2024
- **Contains:** Conflict-year data where at least one party is a state government
- **Format:** CSV, Excel, Stata, R
- **Citation:** Gleditsch et al. (2002); Davies et al. (2025)
- **Notes:** ⭐ Start here — cleanest country-year conflict data

### UCDP External Support Dataset
- **URL:** https://ucdp.uu.se/downloads/index.html (scroll to ESD)
- **Coverage:** 1975-2017
- **Contains:** External support to warring parties (who supports whom)
- **Format:** Excel, Stata
- **Citation:** Meier et al. (2022)
- **Notes:** ⭐ Gold for network construction — tracks triad relationships (supporter → recipient → opponent)

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

### Military Intervention Project (MIP)
- **URL:** https://sites.tufts.edu/css/?page_id=1582
- **Paper:** Kushi & Toft (2023) "Introducing the Military Intervention Project" *Journal of Conflict Resolution*
- **Coverage:** US interventions 1776-2019
- **Contains:** ~400 US military interventions with 200+ variables
- **Kaggle mirror:** https://www.kaggle.com/datasets/konradb/us-military-interventions
- **Notes:** US-only but very comprehensive; includes overt and covert interventions

---

## 🌍 Colonial & Trade Ties

### CEPII Colonial/Geographic Data
- **URL:** http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele.asp
- **Contains:** Colonial history ties, geographic distances, common language
- **Notes:** Standard source for gravity models; colonial ties well-documented

### SIPRI Arms Transfers Database
- **URL:** https://www.sipri.org/databases/armstransfers
- **Coverage:** 1950-present
- **Contains:** International arms trade flows
- **Notes:** Track military relationships between countries

---

## 📊 Country-Level Indicators

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

---

## 📚 Key Papers

### On Violence Against Journalists
- Relly & González de Bustamante (2017). "Global and Domestic Networks Advancing Prospects for Institutional and Social Change: The Collective Action Response to Violence Against Journalists." *Journalism & Communication Monographs* 19(2): 84-152.
  - **Notes:** Uses network framework qualitatively — we can operationalize quantitatively

### On Military Intervention Data
- Kushi, S. & Toft, M.D. (2023). "Introducing the Military Intervention Project: A New Dataset on US Military Interventions, 1776–2019." *Journal of Conflict Resolution* 67(4): 752-779.

### On UCDP Data
- Davies, S., Pettersson, T., Sollenberg, M., & Öberg, M. (2025). "Organized violence 1989–2024." *Journal of Peace Research* 62(4).

---

## 📝 To Do

- [ ] Download RSF Barometer data
- [ ] Get course CSV (Mapping Media Freedom?) from instructors
- [ ] Download UCDP/PRIO Armed Conflict Dataset
- [ ] Download UCDP External Support Dataset
- [ ] Explore MIP on Kaggle
- [ ] Find CEPII colonial ties data
- [ ] Check V-Dem for press freedom variables

---

*Last updated: February 2025*
