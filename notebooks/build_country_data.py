"""
build_country_data.py
Run from anywhere:
  python build_country_data.py

Reads:  data/merged/panel_final_1992_2024.csv  (monadic panel)
Writes: country_stats.json  (in the same directory as this script)

Then copy country_stats.json to:
  marfakozeletsUvA.github.io/neo-colonial-networks/data/
"""

import json, sys
from pathlib import Path
import pandas as pd

COUNTRY_NAMES = {
    "AFG":"Afghanistan","ALB":"Albania","DZA":"Algeria","AGO":"Angola","ARG":"Argentina",
    "ARM":"Armenia","AUS":"Australia","AUT":"Austria","AZE":"Azerbaijan","BGD":"Bangladesh",
    "BLR":"Belarus","BEL":"Belgium","BLZ":"Belize","BEN":"Benin","BTN":"Bhutan","BOL":"Bolivia",
    "BIH":"Bosnia & Herz.","BWA":"Botswana","BRA":"Brazil","BRN":"Brunei","BGR":"Bulgaria",
    "BFA":"Burkina Faso","BDI":"Burundi","KHM":"Cambodia","CMR":"Cameroon","CAN":"Canada",
    "CAF":"C. African Rep.","TCD":"Chad","CHL":"Chile","CHN":"China","COL":"Colombia",
    "COM":"Comoros","COD":"DR Congo","COG":"Congo","CRI":"Costa Rica","CIV":"Côte d'Ivoire",
    "HRV":"Croatia","CUB":"Cuba","CZE":"Czech Rep.","DNK":"Denmark","DJI":"Djibouti",
    "DOM":"Dominican Rep.","ECU":"Ecuador","EGY":"Egypt","SLV":"El Salvador","ERI":"Eritrea",
    "EST":"Estonia","ETH":"Ethiopia","FJI":"Fiji","FIN":"Finland","FRA":"France","GAB":"Gabon",
    "GMB":"Gambia","GEO":"Georgia","DEU":"Germany","GHA":"Ghana","GRC":"Greece",
    "GTM":"Guatemala","GIN":"Guinea","GNB":"Guinea-Bissau","GUY":"Guyana","HTI":"Haiti",
    "HND":"Honduras","HUN":"Hungary","IND":"India","IDN":"Indonesia","IRN":"Iran","IRQ":"Iraq",
    "IRL":"Ireland","ISR":"Israel","ITA":"Italy","JAM":"Jamaica","JPN":"Japan","JOR":"Jordan",
    "KAZ":"Kazakhstan","KEN":"Kenya","PRK":"North Korea","KOR":"South Korea","KWT":"Kuwait",
    "KGZ":"Kyrgyzstan","LAO":"Laos","LVA":"Latvia","LBN":"Lebanon","LSO":"Lesotho",
    "LBR":"Liberia","LBY":"Libya","LTU":"Lithuania","LUX":"Luxembourg","MDG":"Madagascar",
    "MWI":"Malawi","MYS":"Malaysia","MDV":"Maldives","MLI":"Mali","MLT":"Malta",
    "MRT":"Mauritania","MUS":"Mauritius","MEX":"Mexico","MDA":"Moldova","MNG":"Mongolia",
    "MNE":"Montenegro","MAR":"Morocco","MOZ":"Mozambique","MMR":"Myanmar","NAM":"Namibia",
    "NPL":"Nepal","NLD":"Netherlands","NZL":"New Zealand","NIC":"Nicaragua","NER":"Niger",
    "NGA":"Nigeria","MKD":"N. Macedonia","NOR":"Norway","OMN":"Oman","PAK":"Pakistan",
    "PAN":"Panama","PNG":"Papua New Guinea","PRY":"Paraguay","PER":"Peru","PHL":"Philippines",
    "POL":"Poland","PRT":"Portugal","QAT":"Qatar","ROU":"Romania","RUS":"Russia",
    "RWA":"Rwanda","SAU":"Saudi Arabia","SEN":"Senegal","SRB":"Serbia","SLE":"Sierra Leone",
    "SGP":"Singapore","SVK":"Slovakia","SVN":"Slovenia","SOM":"Somalia","ZAF":"South Africa",
    "SSD":"South Sudan","ESP":"Spain","LKA":"Sri Lanka","SDN":"Sudan","SWE":"Sweden",
    "CHE":"Switzerland","SYR":"Syria","TJK":"Tajikistan","TZA":"Tanzania","THA":"Thailand",
    "TLS":"Timor-Leste","TGO":"Togo","TTO":"Trinidad & Tobago","TUN":"Tunisia","TUR":"Turkey",
    "TKM":"Turkmenistan","UGA":"Uganda","UKR":"Ukraine","ARE":"UAE","GBR":"United Kingdom",
    "USA":"United States","URY":"Uruguay","UZB":"Uzbekistan","VEN":"Venezuela","VNM":"Vietnam",
    "YEM":"Yemen","ZMB":"Zambia","ZWE":"Zimbabwe","PSE":"Palestine","SUR":"Suriname","TWN":"Taiwan",
}

# ── locate panel ──────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
candidates = [
    ROOT / "data" / "merged" / "panel_final_1992_2024.csv",
    ROOT / "data" / "merged" / "panel_with_controls_1992_2024.csv",
]
panel_path = next((p for p in candidates if p.exists()), None)
if panel_path is None:
    print("ERROR: could not find panel CSV. Tried:", [str(c) for c in candidates])
    sys.exit(1)

print(f"Reading {panel_path} ...")
df = pd.read_csv(panel_path, low_memory=False)
print(f"  {len(df):,} rows × {len(df.columns)} cols")

# ── map actual column names ───────────────────────────────────
# This is a monadic panel — one row per recipient-year, no sender column
cols = list(df.columns)
print("  cols:", cols)

# Find recipient col
recip_col = next((c for c in cols if 'recipient' in c.lower() and 'iso' in c.lower()), None)
if recip_col is None:
    # fallback: maybe it's just called 'iso3' or 'country'
    recip_col = next((c for c in cols if c.lower() in ('iso3','country','recipient')), None)
if recip_col is None:
    print("ERROR: cannot find recipient ISO3 column. Cols:", cols)
    sys.exit(1)

# Find year col
year_col = next((c for c in cols if c.lower() == 'year'), None)

# Find killings col
kill_col = next((c for c in cols if 'journalist' in c.lower() and 'kill' in c.lower()), None)

# Find arms col  — prefer total, then log, then anything with arms+tiv
arms_col = next((c for c in cols if 'arms' in c.lower() and 'total' in c.lower() and 'log' not in c.lower()), None)
if arms_col is None:
    arms_col = next((c for c in cols if 'arms' in c.lower() and 'tiv' in c.lower() and 'log' not in c.lower()), None)

# Find ODA col — prefer total non-log
oda_col = next((c for c in cols if 'oda' in c.lower() and 'total' in c.lower() and 'log' not in c.lower()), None)
if oda_col is None:
    oda_col = next((c for c in cols if 'oda' in c.lower() and 'log' not in c.lower()), None)

# Find econ col — prefer total non-log, non-lag
econ_col = next((c for c in cols if 'econ' in c.lower() and 'total' in c.lower() and 'log' not in c.lower() and 'lag' not in c.lower()), None)
if econ_col is None:
    econ_col = next((c for c in cols if 'econ' in c.lower() and 'log' not in c.lower() and 'lag' not in c.lower()), None)

# Find colonial col
col_col = next((c for c in cols if 'colonial' in c.lower() and 'flag' in c.lower()), None)
if col_col is None:
    col_col = next((c for c in cols if 'colonial' in c.lower()), None)

print(f"\n  Mapped columns:")
print(f"    recipient : {recip_col}")
print(f"    year      : {year_col}")
print(f"    killings  : {kill_col}")
print(f"    arms      : {arms_col}")
print(f"    oda       : {oda_col}")
print(f"    econ      : {econ_col}")
print(f"    colonial  : {col_col}")

# ── clean ─────────────────────────────────────────────────────
df = df.rename(columns={recip_col: 'recipient', year_col: 'year'})
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df.dropna(subset=['recipient', 'year'])
df['year'] = df['year'].astype(int)

for col, name in [(kill_col,'kills'),(arms_col,'arms'),(oda_col,'oda'),(econ_col,'econ'),(col_col,'colonial')]:
    if col:
        df[name] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[name] = 0

years = list(range(1992, 2025))
out = {}

recipients = df['recipient'].unique()
print(f"\n  {len(recipients)} recipient countries found")

for iso3 in recipients:
    sub = df[df['recipient'] == iso3].copy()

    kills_by_year = {}
    total_kills = 0
    for yr in years:
        k = int(sub[sub['year'] == yr]['kills'].sum())
        kills_by_year[str(yr)] = k
        total_kills += k

    arms_by_year = {str(yr): round(float(sub[sub['year']==yr]['arms'].sum()), 2) for yr in years}
    oda_by_year  = {str(yr): round(float(sub[sub['year']==yr]['oda'].sum()),  2) for yr in years}
    econ_by_year = {str(yr): round(float(sub[sub['year']==yr]['econ'].sum()), 4) for yr in years}

    colonial = 1 if sub['colonial'].max() >= 1 else 0

    out[iso3] = {
        "name":          COUNTRY_NAMES.get(iso3, iso3),
        "total_kills":   total_kills,
        "kills_by_year": kills_by_year,
        "arms_by_year":  arms_by_year,
        "oda_by_year":   oda_by_year,
        "econ_by_year":  econ_by_year,
        "colonial":      colonial,
        # monadic panel has no sender info — top senders come from dyadic edge CSV in the browser
        "top_arms_sender": "",
        "top_oda_sender":  "",
    }

# ── write next to this script ─────────────────────────────────
out_path = Path(__file__).parent / "country_stats.json"
with open(out_path, "w") as f:
    json.dump(out, f, separators=(",", ":"))

print(f"\nWrote {len(out)} countries → {out_path}")
print(f"\nNow copy to your website repo:")
print(f"  cp {out_path} /Users/mac/marfakozeletsUvA.github.io/neo-colonial-networks/data/country_stats.json")
