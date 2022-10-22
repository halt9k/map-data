import pycountry

from Data.text_helpers import get_match_ids


def match_name_to_iso(fuzzy_name, valid_names, valid_iso):
    matches = get_match_ids(fuzzy_name, valid_names, cutoff=0.65)

    if len(matches) < 1:
        print('WARNING: region with unknown modern name: ' + fuzzy_name)
        return None

    iso = valid_iso[matches[0]]
    if len(matches) > 1:
        print('WARNING: ambigious iso for: ' + fuzzy_name + ': [ ' +
              valid_names[matches].to_string().replace('\n', ', ') + '] ->' + iso)

    return iso


def code_to_alpha_3_iso(column):
    # codes to Country names

    Codes = []
    for country_name in column:
        country = pycountry.countries.get(name=country_name)

        if country is None:
            try:
                match_list = pycountry.countries.search_fuzzy(country_name)
                if len(match_list) > 0:
                    country = match_list[0]
            except:
                country = None

        # .alpha_3 means 3-letter country code
        # .alpha_2 means 2-letter country code
        if country is None:
            Codes.append('UNK')
        else:
            Codes.append(country.alpha_3)

    return Codes


def filter_irregular_codes(df):
    # Remove combined world regions (Whole world, Africa, etc)

    valid_rows = ~df.Code.isnull() & (df.Code != 'OWID_WRL')
    print('Irregular countries removed: ' + str(df[~valid_rows]))
    return df[valid_rows]
