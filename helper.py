import math

def distance_between_coords(coord1, coord2):
    # Using Haversine's distance formula

    la1, lo1 = coord1
    la2, lo2 = coord2
    
    la1 = la1 * math.pi / 180
    lo1 = lo1 * math.pi / 180
    la2 = la2 * math.pi / 180
    lo2 = lo2 * math.pi / 180
    
    deltalat = la2 - la1
    deltalon = lo2 - lo1
    
    radius = 6371
    
    a = math.sin(deltalat/2)**2 + math.cos(la1) * math.cos(la2) * math.sin(deltalon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    
    return distance

country_dict = {
    "AF": ["Afghanistan"],
    "AX": ["Åland Islands", "Åland"],
    "AL": ["Albania"],
    "AD": ["Andorra"],
    "AQ": ["Antarctica"],
    "AR": ["Argentina"],
    "AW": ["Aruba"],
    "AU": ["Australia"],
    "AT": ["Austria"],
    "BD": ["Bangladesh"],
    "BY": ["Belarus"],
    "BZ": ["Belize"],
    "BE": ["Belgium"],
    "BT": ["Bhutan"],
    "BO": ["Bolivia"],
    "BW": ["Botswana"],
    "BR": ["Brazil"],
    "BG": ["Bulgaria"],
    "KH": ["Cambodia"],
    "CA": ["Canada"],
    "CL": ["Chile"],
    "CN": ["China"],
    "CO": ["Colombia"],
    "CR": ["Costa Rica"],
    "HR": ["Croatia"],
    "CZ": ["Czech Republic"],
    "DK": ["Denmark"],
    "DO": ["Dominican Republic"],
    "EC": ["Ecuador"],
    "EG": ["Egypt"],
    "EE": ["Estonia"],
    "SZ": ["Eswatini", "Swaziland"],
    "FO": ["Faroe Islands"],
    "FI": ["Finland"],
    "FR": ["France"],
    "DE": ["Germany"],
    "GH": ["Ghana"],
    "GR": ["Greece"],
    "GL": ["Greenland"],
    "GT": ["Guatemala"],
    "HU": ["Hungary"],
    "IS": ["Iceland"],
    "IN": ["India"],
    "ID": ["Indonesia"],
    "IQ": ["Iraq"],
    "IE": ["Ireland"],
    "IL": ["Israel"],
    "IT": ["Italy"],
    "JP": ["Japan"],
    "JO": ["Jordan"],
    "KZ": ["Kazakhstan"],
    "KE": ["Kenya"],
    "KG": ["Kyrgyzstan"],
    "LA": ["Laos"],
    "LV": ["Latvia"],
    "LB": ["Lebanon"],
    "LS": ["Lesotho"],
    "LT": ["Lithuania"],
    "LU": ["Luxembourg"],
    "MO": ["Macau"],
    "MG": ["Madagascar"],
    "MY": ["Malaysia"],
    "MV": ["Maldives"],
    "MT": ["Malta"],
    "MX": ["Mexico"],
    "MC": ["Monaco"],
    "MN": ["Mongolia"],
    "ME": ["Montenegro"],
    "NP": ["Nepal"],
    "NL": ["Netherlands"],
    "NZ": ["New Zealand"],
    "NG": ["Nigeria"],
    "MK": ["North Macedonia"],
    "NO": ["Norway"],
    "PK": ["Pakistan"],
    "PS": ["Palestine"],
    "PA": ["Panama"],
    "PH": ["Philippines"],
    "PL": ["Poland"],
    "PT": ["Portugal"],
    "PR": ["Puerto Rico"],
    "QA": ["Qatar"],
    "RE": ["Réunion"],
    "RO": ["Romania"],
    "RU": ["Russia"],
    "RW": ["Rwanda"],
    "SM": ["San Marino"],
    "SN": ["Senegal"],
    "RS": ["Serbia"],
    "SG": ["Singapore"],
    "SK": ["Slovakia"],
    "SB": ["Solomon Islands"],
    "ZA": ["South Africa"],
    "KR": ["South Korea"],
    "ES": ["Spain"],
    "LK": ["Sri Lanka"],
    "SJ": ["Svalbard"],
    "SE": ["Sweden"],
    "CH": ["Switzerland"],
    "TW": ["Taiwan"],
    "TZ": ["Tanzania"],
    "TH": ["Thailand"],
    "BS": ["The Bahamas", "Bahamas"],
    "TN": ["Tunisia"],
    "TR": ["Turkey"],
    "UG": ["Uganda"],
    "UA": ["Ukraine"],
    "AE": ["United Arab Emirates"],
    "GB": ["United Kingdom", "UK"],
    "US": ["United States", "USA"],
    "UY": ["Uruguay"],
    "VU": ["Vanuatu"],
    "VN": ["Vietnam"],
}
