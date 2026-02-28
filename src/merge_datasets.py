# merge_datasets.py
# Merges all preprocessed datasets into dyadic panel format
# Output: sender-recipient-year observations with all predictors
#
# USAGE: Run from project root directory:
#   cd /path/to/Violent-Offenders-GPV---CSSci-
#   python src/merge_datasets.py
#
# DATASETS USED:
#   - CPJ journalist killings (target variable)
#   - SIPRI arms transfers (military layer)
#   - OECD DAC2 bilateral ODA (economic layer)
#   - World Bank bilateral debt (economic layer)
#   - COLDAT colonial ties (colonial layer)
#
# NOTE: Run 06_oecd_dac2_oda_fixing.ipynb FIRST to resolve
#       Micronesia duplicates in the OECD DAC2 file.

import pandas as pd
import numpy as np
import os
import sys

# =============================================================================
# CONFIGURATION - Edit these paths if your folder structure differs
# =============================================================================

# Get the project root (assumes script is in src/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Data directories
INPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'merged')

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Add src to path so we can import country_utils_extended
sys.path.insert(0, SCRIPT_DIR)
from country_utils_extended import *

# Analysis window
YEAR_MIN = 1992
YEAR_MAX = 2024

# =============================================================================
# LOAD AND STANDARDIZE ALL DATASETS
# =============================================================================

print("="*60)
print("LOADING DATASETS")
print("="*60)
print(f"Input directory: {INPUT_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print(f"Analysis window: {YEAR_MIN}-{YEAR_MAX}\n")

# Target variable (CPJ journalist killings) - country-year format
cpj = pd.read_csv(os.path.join(INPUT_DIR, 'target_journalist_killings.csv'))
print(f"✓ CPJ: {len(cpj)} country-years, {cpj['journalist_killings'].sum()} total killings")

# Bilateral datasets
sipri = pd.read_csv(os.path.join(INPUT_DIR, 'sipri_trade_register.csv'))
print(f"✓ SIPRI: {len(sipri)} arms transfer records")

# OECD DAC2 bilateral ODA (must run 06_oecd_dac2_oda_fixing.ipynb first!)
dac2 = pd.read_csv(os.path.join(INPUT_DIR, 'oecd_dac2_oda.csv'))
# Safety check: resolve any remaining duplicates (Micronesia issue)
dac2 = dac2.groupby(['donor', 'recipient', 'year', 'a_iso3', 'b_iso3'], as_index=False)['oda_value'].sum()
print(f"✓ OECD DAC2: {len(dac2)} bilateral ODA records")

debt = pd.read_csv(os.path.join(INPUT_DIR, 'worldbank_bilateral_debt.csv'))
debt = standardize_debt(debt)
print(f"✓ Debt: {len(debt)} bilateral debt records")

# Static datasets
coldat = pd.read_csv(os.path.join(INPUT_DIR, 'coldat_colonial_ties.csv'))
coldat = standardize_coldat(coldat)
print(f"✓ COLDAT: {len(coldat)} colonial relationships")

# =============================================================================
# CREATE DYADIC PANEL STRUCTURE
# =============================================================================

print("\n" + "="*60)
print("CREATING DYADIC PANEL")
print("="*60)

# Get all unique countries that appear as recipients in any dataset
all_recipients = set()
all_recipients.update(cpj['iso3'].dropna().unique())
all_recipients.update(sipri['recipient_iso3'].dropna().unique())
all_recipients.update(dac2['b_iso3'].dropna().unique())
all_recipients.update(debt['debtor_iso3'].dropna().unique())

# Get all unique countries that appear as senders
all_senders = set()
all_senders.update(sipri['supplier_iso3'].dropna().unique())
all_senders.update(dac2['a_iso3'].dropna().unique())
all_senders.update(debt['creditor_iso3'].dropna().unique())
all_senders.update(coldat['colonizer_iso3'].dropna().unique())

print(f"\nUnique recipients: {len(all_recipients)}")
print(f"Unique senders: {len(all_senders)}")

# =============================================================================
# AGGREGATE BILATERAL DATA TO SENDER-RECIPIENT-YEAR
# =============================================================================

# SIPRI (arms transfers)
sipri_agg = sipri.groupby(['supplier_iso3', 'recipient_iso3', 'year']).agg({
    'tiv': 'sum'
}).reset_index()
sipri_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'arms_tiv']

# OECD DAC2 (bilateral ODA)
dac2_agg = dac2.groupby(['a_iso3', 'b_iso3', 'year']).agg({
    'oda_value': 'sum'
}).reset_index()
dac2_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'bilateral_oda']

# Debt (bilateral debt)
debt_agg = debt.groupby(['creditor_iso3', 'debtor_iso3', 'year']).agg({
    'debt_stock': 'sum'
}).reset_index()
debt_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'bilateral_debt']

# =============================================================================
# BUILD BASE PANEL FROM ALL OBSERVED DYADS
# =============================================================================

# Combine all dyadic observations to get the universe of sender-recipient-year
all_dyads = pd.concat([
    sipri_agg[['sender_iso3', 'recipient_iso3', 'year']],
    dac2_agg[['sender_iso3', 'recipient_iso3', 'year']],
    debt_agg[['sender_iso3', 'recipient_iso3', 'year']],
])

# Get unique dyads within analysis window
panel = all_dyads.drop_duplicates().copy()
panel = panel[(panel['year'] >= YEAR_MIN) & (panel['year'] <= YEAR_MAX)]

print(f"\nBase panel: {len(panel)} sender-recipient-year observations")

# =============================================================================
# MERGE IN EACH DATASET
# =============================================================================

# Bilateral variables (left join — missing = no relationship)
panel = panel.merge(sipri_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
panel = panel.merge(dac2_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
panel = panel.merge(debt_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')

# Fill SIPRI: missing = no arms transfer = 0
panel['arms_tiv'] = panel['arms_tiv'].fillna(0)

# Debt and ODA: keep as NaN (genuinely missing vs zero is meaningful)

# Add colonial ties (static — doesn't vary by year)
coldat_binary = coldat[['colony_iso3', 'colonizer_iso3']].drop_duplicates()
coldat_binary['colonial_tie'] = 1
coldat_binary.columns = ['recipient_iso3', 'sender_iso3', 'colonial_tie']

panel = panel.merge(coldat_binary, on=['sender_iso3', 'recipient_iso3'], how='left')
panel['colonial_tie'] = panel['colonial_tie'].fillna(0).astype(int)

# Add target variable (journalist killings in recipient country)
cpj_subset = cpj[['iso3', 'year', 'journalist_killings']].copy()
cpj_subset.columns = ['recipient_iso3', 'year', 'journalist_killings']

panel = panel.merge(cpj_subset, on=['recipient_iso3', 'year'], how='left')

# Fill missing journalist killings with 0 (absence from CPJ = no killings recorded)
panel['journalist_killings'] = panel['journalist_killings'].fillna(0)

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

print(f"\n{'='*60}")
print(f"PANEL SUMMARY (1992-2024)")
print(f"{'='*60}")
print(f"Total observations: {len(panel)}")
print(f"Unique senders: {panel['sender_iso3'].nunique()}")
print(f"Unique recipients: {panel['recipient_iso3'].nunique()}")
print(f"Year range: {panel['year'].min()} - {panel['year'].max()}")
print(f"\nColumn coverage (non-null %):")
for col in panel.columns:
    if col not in ['sender_iso3', 'recipient_iso3', 'year']:
        pct = 100 * panel[col].notna().sum() / len(panel)
        print(f"  {col}: {pct:.1f}%")

print(f"\nRecipients with journalist killings: {panel[panel['journalist_killings'] > 0]['recipient_iso3'].nunique()}")
print(f"Total journalist killings in panel: {panel['journalist_killings'].sum():.0f}")

# =============================================================================
# SAVE OUTPUT
# =============================================================================

output_path = os.path.join(OUTPUT_DIR, 'panel_dyadic_1992_2024.csv')
panel.to_csv(output_path, index=False)

print(f"\n{'='*60}")
print("OUTPUT SAVED")
print(f"{'='*60}")
print(f"✓ {output_path}")
print(f"  ({len(panel)} rows, {len(panel.columns)} columns)")
print(f"  Columns: {panel.columns.tolist()}")