# merge_datasets.py
# Merges all preprocessed datasets into dyadic panel format
# Output: sender-recipient-year observations with all predictors
#
# USAGE: Run from project root directory:
#   cd /path/to/Violent-Offenders-GPV---CSSci-
#   python src/merge_datasets.py

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

# =============================================================================
# LOAD AND STANDARDIZE ALL DATASETS
# =============================================================================

print("="*60)
print("LOADING DATASETS")
print("="*60)
print(f"Input directory: {INPUT_DIR}")
print(f"Output directory: {OUTPUT_DIR}\n")

# Target variable (CPJ journalist killings) - country-year format
cpj = pd.read_csv(os.path.join(INPUT_DIR, 'target_journalist_killings.csv'))
print(f"✓ CPJ: {len(cpj)} country-years, {cpj['journalist_killings'].sum()} total killings")

# Bilateral datasets
sipri = pd.read_csv(os.path.join(INPUT_DIR, 'sipri_trade_register.csv'))
print(f"✓ SIPRI: {len(sipri)} arms transfer records")

aid = pd.read_csv(os.path.join(INPUT_DIR, 'aiddata_bilateral_flows.csv'))
aid = standardize_aiddata(aid)
print(f"✓ AidData: {len(aid)} aid flow records ({aid['is_intl_org'].sum()} from intl orgs)")

debt = pd.read_csv(os.path.join(INPUT_DIR, 'worldbank_bilateral_debt.csv'))
debt = standardize_debt(debt)
print(f"✓ Debt: {len(debt)} bilateral debt records")

ucdp = pd.read_csv(os.path.join(INPUT_DIR, 'ucdp_esd_ty.csv'))
ucdp = standardize_ucdp(ucdp)
print(f"✓ UCDP: {len(ucdp)} external support records ({ucdp['is_state_supporter'].sum()} from states)")

# Static datasets
coldat = pd.read_csv(os.path.join(INPUT_DIR, 'coldat_colonial_ties.csv'))
coldat = standardize_coldat(coldat)
print(f"✓ COLDAT: {len(coldat)} colonial relationships")

# Control variable (ODA) - country-year format
oda = pd.read_csv(os.path.join(INPUT_DIR, 'oda_received_by_country.csv'))
print(f"✓ ODA: {len(oda)} country-years")

# MIP (US interventions only) - country-year format
mip = pd.read_csv(os.path.join(INPUT_DIR, 'mip_us_interventions.csv'))
print(f"✓ MIP: {len(mip)} US intervention records")

# =============================================================================
# CREATE DYADIC PANEL STRUCTURE
# =============================================================================

print("\n" + "="*60)
print("CREATING DYADIC PANEL")
print("="*60)

# Define time windows
WINDOW_FULL = (1992, 2013)  # All datasets overlap
WINDOW_EXTENDED = (1992, 2024)  # Without AidData

# Get all unique countries that appear as recipients in any dataset
all_recipients = set()
all_recipients.update(cpj['iso3'].dropna().unique())
all_recipients.update(sipri['recipient_iso3'].dropna().unique())
all_recipients.update(aid['recipient_iso3'].dropna().unique())
all_recipients.update(debt['debtor_iso3'].dropna().unique())
all_recipients.update(ucdp['target_iso3'].dropna().unique())

# Get all unique countries that appear as senders (Global North focus)
all_senders = set()
all_senders.update(sipri['supplier_iso3'].dropna().unique())
all_senders.update(aid[~aid['is_intl_org']]['donor_iso3'].dropna().unique())
all_senders.update(debt['creditor_iso3'].dropna().unique())
all_senders.update(ucdp[ucdp['is_state_supporter']]['supporter_iso3'].dropna().unique())
all_senders.update(coldat['colonizer_iso3'].dropna().unique())

print(f"\nUnique recipients: {len(all_recipients)}")
print(f"Unique senders: {len(all_senders)}")

# =============================================================================
# AGGREGATE BILATERAL DATA TO SENDER-RECIPIENT-YEAR
# =============================================================================

def create_dyadic_panel(year_min, year_max, include_aiddata=True):
    """Create dyadic panel for specified time window"""
    
    years = range(year_min, year_max + 1)
    
    # Start with SIPRI (arms transfers)
    sipri_agg = sipri.groupby(['supplier_iso3', 'recipient_iso3', 'year']).agg({
        'tiv': 'sum'
    }).reset_index()
    sipri_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'arms_tiv']
    
    # AidData (bilateral aid from countries only)
    if include_aiddata:
        aid_countries = aid[~aid['is_intl_org']].copy()
        aid_agg = aid_countries.groupby(['donor_iso3', 'recipient_iso3', 'year']).agg({
            'aid_amount': 'sum'
        }).reset_index()
        aid_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'bilateral_aid']
    
    # Debt (bilateral debt)
    debt_agg = debt.groupby(['creditor_iso3', 'debtor_iso3', 'year']).agg({
        'debt_stock': 'sum'
    }).reset_index()
    debt_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 'bilateral_debt']
    
    # UCDP (external support from state actors)
    ucdp_states = ucdp[ucdp['is_state_supporter']].copy()
    ucdp_agg = ucdp_states.groupby(['supporter_iso3', 'target_iso3', 'year']).agg({
        'troops': 'max',  # binary indicators, take max
        'weapons': 'max',
        'training': 'max',
        'funding': 'max'
    }).reset_index()
    ucdp_agg.columns = ['sender_iso3', 'recipient_iso3', 'year', 
                        'ucdp_troops', 'ucdp_weapons', 'ucdp_training', 'ucdp_funding']
    
    # Create base panel: all sender-recipient-year combinations from observed data
    # (We don't want to create all possible combinations - too sparse)
    
    # Combine all dyadic observations
    all_dyads = pd.concat([
        sipri_agg[['sender_iso3', 'recipient_iso3', 'year']],
        debt_agg[['sender_iso3', 'recipient_iso3', 'year']],
        ucdp_agg[['sender_iso3', 'recipient_iso3', 'year']],
    ])
    
    if include_aiddata:
        all_dyads = pd.concat([all_dyads, aid_agg[['sender_iso3', 'recipient_iso3', 'year']]])
    
    # Get unique dyads
    panel = all_dyads.drop_duplicates().copy()
    panel = panel[(panel['year'] >= year_min) & (panel['year'] <= year_max)]
    
    print(f"\nBase panel: {len(panel)} sender-recipient-year observations")
    
    # Merge in each dataset
    panel = panel.merge(sipri_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
    panel = panel.merge(debt_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
    panel = panel.merge(ucdp_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
    
    if include_aiddata:
        panel = panel.merge(aid_agg, on=['sender_iso3', 'recipient_iso3', 'year'], how='left')
    
    # Fill missing values
    # SIPRI: missing = no arms transfer = 0
    panel['arms_tiv'] = panel['arms_tiv'].fillna(0)
    
    # UCDP: missing = no support = 0
    for col in ['ucdp_troops', 'ucdp_weapons', 'ucdp_training', 'ucdp_funding']:
        panel[col] = panel[col].fillna(0).astype(int)
    
    # Debt and Aid: keep as NaN (genuinely missing vs zero is meaningful)
    
    # Add colonial ties (static - doesn't vary by year)
    coldat_binary = coldat[['colony_iso3', 'colonizer_iso3']].drop_duplicates()
    coldat_binary['colonial_tie'] = 1
    coldat_binary.columns = ['recipient_iso3', 'sender_iso3', 'colonial_tie']
    
    panel = panel.merge(coldat_binary, on=['sender_iso3', 'recipient_iso3'], how='left')
    panel['colonial_tie'] = panel['colonial_tie'].fillna(0).astype(int)
    
    # Add target variable (journalist killings in recipient country)
    cpj_subset = cpj[['iso3', 'year', 'journalist_killings']].copy()
    cpj_subset.columns = ['recipient_iso3', 'year', 'journalist_killings']
    
    panel = panel.merge(cpj_subset, on=['recipient_iso3', 'year'], how='left')
    
    # Add control variable (ODA received by recipient)
    oda_subset = oda[['iso3', 'year', 'oda_received']].copy()
    oda_subset.columns = ['recipient_iso3', 'year', 'oda_received']
    
    panel = panel.merge(oda_subset, on=['recipient_iso3', 'year'], how='left')
    
    # Add MIP (US intervention in recipient country)
    # Create binary indicator for US intervention by year
    mip_binary = mip.copy()
    mip_binary['us_intervention'] = 1
    mip_expanded = []
    for _, row in mip_binary.iterrows():
        start = int(row['start_year'])
        end = int(row['end_year']) if pd.notna(row['end_year']) else start
        for y in range(start, end + 1):
            mip_expanded.append({'recipient_iso3': row['iso3'], 'year': y, 'us_intervention': 1})
    
    mip_df = pd.DataFrame(mip_expanded).drop_duplicates()
    panel = panel.merge(mip_df, on=['recipient_iso3', 'year'], how='left')
    panel['us_intervention'] = panel['us_intervention'].fillna(0).astype(int)
    
    return panel

# =============================================================================
# CREATE BOTH PANELS
# =============================================================================

print("\n" + "="*60)
print("PANEL 1: FULL DATA (1992-2013)")
print("="*60)
panel_full = create_dyadic_panel(1992, 2013, include_aiddata=True)

print("\n" + "="*60)
print("PANEL 2: EXTENDED (1992-2024, no AidData)")
print("="*60)
panel_extended = create_dyadic_panel(1992, 2024, include_aiddata=False)

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

def summarize_panel(panel, name):
    print(f"\n{'='*60}")
    print(f"SUMMARY: {name}")
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

summarize_panel(panel_full, "FULL DATA (1992-2013)")
summarize_panel(panel_extended, "EXTENDED (1992-2024)")

# =============================================================================
# FILL MISSING VALUES
# =============================================================================

# Fill missing journalist killings with 0 (absence from CPJ = no killings recorded)
panel_full['journalist_killings'] = panel_full['journalist_killings'].fillna(0)
panel_extended['journalist_killings'] = panel_extended['journalist_killings'].fillna(0)

# =============================================================================
# SAVE OUTPUTS
# =============================================================================

output_full = os.path.join(OUTPUT_DIR, 'panel_dyadic_1992_2013.csv')
output_extended = os.path.join(OUTPUT_DIR, 'panel_dyadic_1992_2024.csv')

panel_full.to_csv(output_full, index=False)
panel_extended.to_csv(output_extended, index=False)

print(f"\n{'='*60}")
print("OUTPUTS SAVED")
print(f"{'='*60}")
print(f"✓ {output_full}")
print(f"  ({len(panel_full)} rows)")
print(f"✓ {output_extended}")
print(f"  ({len(panel_extended)} rows)")
