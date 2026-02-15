# Save this as: src/country_utils.py

import pandas as pd
import pycountry

# Manual mapping for country name variants
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
    "Congo - Brazzaville": "Congo",
    "Congo, Rep.": "Congo",
    "Congo, Republic of": "Congo",
    "Republic of Congo": "Congo",
    
    # Russia variants
    "Russia": "Russian Federation",
    "Soviet Union": "Russian Federation",
    
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
}


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