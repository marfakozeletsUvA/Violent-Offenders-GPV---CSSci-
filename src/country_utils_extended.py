# Extended country standardization for all datasets
# Handles: AidData donors, Debt creditors, UCDP supporters

import pandas as pd
import pycountry

# =============================================================================
# MANUAL MAPPINGS
# =============================================================================

# Base manual mapping (from your original script)
manual_map = {
    # Debt dataset variants
    "Germany, Fed. Rep. of": "Germany",
    "Korea, Republic of": "South Korea",
    
    # COLDAT lowercase
    "britain": "United Kingdom",
    "belgium": "Belgium",
    "france": "France",
    "germany": "Germany",
    "netherlands": "Netherlands",
    "portugal": "Portugal",
    "spain": "Spain",
    "italy": "Italy",
    
    # Congo variants
    "Congo - Kinshasa": "Congo, The Democratic Republic of the",
    "Congo, Dem. Rep.": "Congo, The Democratic Republic of the",
    "Congo, Democratic Republic of": "Congo, The Democratic Republic of the",
    "DR Congo": "Congo, The Democratic Republic of the",
    "DRC": "Congo, The Democratic Republic of the",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "DR Congo (Zaire)": "Congo, The Democratic Republic of the",
    "Congo - Brazzaville": "Congo",
    "Congo, Rep.": "Congo",
    "Congo, Republic of": "Congo",
    "Republic of Congo": "Congo",
    
    # Russia variants
    "Russia": "Russian Federation",
    "Soviet Union": "Russian Federation",
    "Russia (Soviet Union)": "Russian Federation",
    
    # UCDP historical variants
    "Cambodia (Kampuchea)": "Cambodia",
    "East Germany": "Germany",
    "Serbia (Yugoslavia)": "Serbia",
    "Vietnam (North Vietnam)": "Viet Nam",
    "Yemen (North Yemen)": "Yemen",
    "Zimbabwe (Rhodesia)": "Zimbabwe",
    
    # Korea variants
    "Korea": "South Korea",
    "Korea, Rep.": "South Korea",
    "Korea, Dem. People's Rep.": "North Korea",
    "Korea, Democratic Republic of": "North Korea",
    
    # Common variants
    "United States of America": "United States",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Cote d`Ivoire": "Côte d'Ivoire",
    "Ivory Coast": "Côte d'Ivoire",
    "Turkey": "Türkiye",
    "Turkiye": "Türkiye",
    "Myanmar (Burma)": "Myanmar",
    "East Timor": "Timor-Leste",
    "ETM": "Timor-Leste",
    "Brunei": "Brunei Darussalam",
    "Laos": "Lao People's Democratic Republic",
    "Lao PDR": "Lao People's Democratic Republic",
    "Iran, Islamic Rep.": "Iran",
    "Egypt, Arab Rep.": "Egypt",
    "Yemen, Rep.": "Yemen",
    "Venezuela, RB": "Venezuela",
    "Bahamas, The": "Bahamas",
    "Gambia, The": "Gambia",
    "Cape Verde": "Cabo Verde",
    "Swaziland": "Eswatini",
    "Macedonia, FYR": "North Macedonia",
    "Micronesia, Fed. Sts.": "Micronesia, Federated States of",
    "Micronesia (Federated States of)": "Micronesia, Federated States of",
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Bosnia": "Bosnia and Herzegovina",
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates",
    "Antigua & Barbuda": "Antigua and Barbuda",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "St. Kitts & Nevis": "Saint Kitts and Nevis",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Lucia": "Saint Lucia",
    "St. Vincent & Grenadines": "Saint Vincent and the Grenadines",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "St.Vincent & Grenadines": "Saint Vincent and the Grenadines",
    "Sao Tome & Principe": "Sao Tome and Principe",
    "São Tomé & Príncipe": "Sao Tome and Principe",
    "Hong Kong, China": "Hong Kong",
    "Hong Kong SAR, China": "Hong Kong",
    "Macao SAR, China": "Macao",
    "Palestine": "Palestine, State of",
    "West Bank and Gaza": "Palestine, State of",
    "Palestinian Adm. Areas": "Palestine, State of",
    "Somalia, Fed. Rep.": "Somalia",
    "Serbia and Montenegro": "Serbia",
    "Yugoslavia": "Serbia",
    "Czechoslovakia": "Czechia",
    "Czech Republic": "Czechia",
    "East Germany (GDR)": "Germany",
    "Netherlands Antilles": "Netherlands",
    "Israel and the Occupied Palestinian Territory": "Israel",
    "Falkland Islands": "Falkland Islands (Malvinas)",
    "Reunion": "Réunion",
    "Northern Marianas": "Northern Mariana Islands",
    "Virgin Islands (UK)": "Virgin Islands, British",
    "Wallis & Futuna": "Wallis and Futuna",
    "St. Helena": "Saint Helena, Ascension and Tristan da Cunha",
    "Northern Cyprus": "Cyprus",
    "Slovak Republic": "Slovakia",
    
    # MIP COW codes
    "CUB": "Cuba",
    "IRQ": "Iraq",
    "KUW": "Kuwait",
    "LBR": "Liberia",
    "SAU": "Saudi Arabia",
    "CAN": "Canada",
    "IRN": "Iran",
    "SOM": "Somalia",
    "PER": "Peru",
    "HAI": "Haiti",
    "HON": "Honduras",
    "LEB": "Lebanon",
    "LIB": "Libya",
    "NIR": "Niger",
    "PHI": "Philippines",
    "SUD": "Sudan",
    "THI": "Thailand",
    "URU": "Uruguay",
    "YUG": "Serbia",
    "BOS": "Bosnia and Herzegovina",
    "CAM": "Cameroon",
    "CAO": "Central African Republic",
    "CEN": "Central African Republic",
    "CDI": "Côte d'Ivoire",
    "GUA": "Guatemala",
    "SIE": "Sierra Leone",
    "INS": "Indonesia",
    "ICE": "Iceland",
}

# Special cases without official ISO codes
special_codes = {
    "Kosovo": "XKX",
    "Taiwan": "TWN",
}

# =============================================================================
# INTERNATIONAL ORGANIZATIONS (non-state actors in AidData)
# =============================================================================

international_orgs = {
    # Multilateral Development Banks
    "African Capacity Building Foundation (ACBF)",
    "African Development Bank (AFDB)",
    "African Development Fund (AFDF)",
    "Andean Development Corporation (CAF)",
    "Arab Bank for Economic Development in Africa (BADEA)",
    "Arab Fund for Economic & Social Development (AFESD)",
    "Asian Development Bank (ASDB)",
    "Asian Development Bank (AsDB Special Funds)",
    "Asian Development Fund (ASDF)",
    "Caribbean Development Bank (CDB)",
    "European Bank for Reconstruction & Development (EBRD)",
    "Inter-American Development Bank (IADB)",
    "Islamic Development Bank (ISDB)",
    "Nigerian Trust Fund (NTF)",
    "Nordic Development Fund (NDF)",
    "North American Development Bank (NADB)",
    "OPEC Fund for International Development (OFID)",
    
    # UN Agencies
    "United Nations Children`s Fund (UNICEF)",
    "United Nations Democracy Fund (UNDEF)",
    "United Nations Development Programme (UNDP)",
    "United Nations Economic Commission for Europe (UNECE)",
    "United Nations Economic and Social Commission for Asia and the Pacific (UNESCAP)",
    "United Nations High Commissioner for Refugees (UNHCR)",
    "United Nations Peacebuilding Fund (UNPBF)",
    "United Nations Population Fund (UNFPA)",
    "United Nations Relief and Works Agency for Palestine Refugees in the Near East (UNRWA)",
    "Joint United Nations Programme on HIV/AIDS (UNAIDS)",
    "World Health Organization (WHO)",
    "World Trade Organization (WTO)",
    
    # World Bank Group
    "World Bank - Carbon Finance Unit",
    "World Bank - Debt Reduction Facility",
    "World Bank - International Bank for Reconstruction and Development (IBRD)",
    "World Bank - International Development Association (IDA)",
    "World Bank - International Finance Corporation (IFC)",
    "World Bank - Managed Trust Funds",
    "International Fund for Agricultural Development (IFAD)",
    "International Monetary Fund (IMF)",
    
    # Other multilaterals
    "European Communities (EC)",
    "Organization for Security and Co-operation in Europe (OSCE)",
    "Global Alliance for Vaccines & Immunization (GAVI)",
    "Global Environment Facility (GEF)",
    "Global Fund to Fight Aids, Tuberculosis and Malaria (GFATM)",
    "Global Green Growth Institute (GGGI)",
    "Global Partnership for Education",
    "Multilateral Fund for the Implementation of the Montreal Protocol",
    "Congo Basin Forest Fund (CBFF)",
    
    # Private foundations
    "Bill & Melinda Gates Foundation",
}

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def clean_country_name(name):
    """Clean country name before pycountry lookup"""
    if pd.isna(name):
        return None
    
    name = str(name).strip()
    
    # Strip "Government of" prefix (UCDP)
    if name.startswith("Government of "):
        name = name.replace("Government of ", "")
    
    # Apply manual mapping
    if name in manual_map:
        name = manual_map[name]
    
    return name


def get_iso3(country_name):
    """Get ISO3 code for a country name"""
    cleaned = clean_country_name(country_name)
    if cleaned is None:
        return None
    
    # Check special cases first
    if cleaned in special_codes:
        return special_codes[cleaned]
    
    try:
        return pycountry.countries.lookup(cleaned).alpha_3
    except LookupError:
        return None


def is_international_org(name):
    """Check if a donor/supporter is an international organization"""
    if pd.isna(name):
        return False
    return str(name).strip() in international_orgs


def is_state_actor(name):
    """Check if a UCDP supporter is a state actor (government)"""
    if pd.isna(name):
        return False
    return str(name).strip().startswith("Government of ")


def standardize_supporter(name):
    """Standardize UCDP supporter name and get ISO3 if state actor"""
    if pd.isna(name):
        return None, None, False
    
    name = str(name).strip()
    is_state = name.startswith("Government of ")
    
    if is_state:
        country = name.replace("Government of ", "")
        iso3 = get_iso3(country)
        return country, iso3, True
    else:
        # Non-state actor (rebel group, terrorist org, etc.)
        return name, None, False


# =============================================================================
# DATASET-SPECIFIC STANDARDIZATION FUNCTIONS
# =============================================================================

def standardize_aiddata(df):
    """Add donor_iso3 column to AidData, mark international orgs"""
    df = df.copy()
    df['is_intl_org'] = df['donor'].apply(is_international_org)
    df['donor_iso3'] = df['donor'].apply(lambda x: None if is_international_org(x) else get_iso3(x))
    return df


def standardize_debt(df):
    """Add creditor_iso3 column to Debt data"""
    df = df.copy()
    df['creditor_iso3'] = df['creditor'].apply(get_iso3)
    return df


def standardize_ucdp(df):
    """Standardize UCDP supporter column"""
    df = df.copy()
    
    results = df['supporter'].apply(standardize_supporter)
    df['supporter_clean'] = results.apply(lambda x: x[0])
    df['supporter_iso3'] = results.apply(lambda x: x[1])
    df['is_state_supporter'] = results.apply(lambda x: x[2])
    
    return df


def standardize_coldat(df):
    """Add colonizer_iso3 column to COLDAT"""
    df = df.copy()
    df['colonizer_iso3'] = df['colonizer'].apply(get_iso3)
    return df


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def check_coverage(df, iso3_col, name_col, dataset_name):
    """Check standardization coverage for a dataset"""
    total = len(df[name_col].dropna())
    matched = df[iso3_col].notna().sum()
    unmatched = df[df[iso3_col].isna()][name_col].dropna().unique()
    
    print(f"\n=== {dataset_name} ===")
    print(f"Total rows with {name_col}: {total}")
    print(f"Matched to ISO3: {matched} ({100*matched/total:.1f}%)")
    print(f"Unmatched unique values: {len(unmatched)}")
    
    if len(unmatched) > 0 and len(unmatched) <= 20:
        print("Unmatched values:")
        for v in sorted(unmatched):
            print(f"  - {v}")
    elif len(unmatched) > 20:
        print(f"First 20 unmatched values:")
        for v in sorted(unmatched)[:20]:
            print(f"  - {v}")
    
    return unmatched
