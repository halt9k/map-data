import pandas as pd
from i18n import t

from data.geo_helpers import match_name_to_iso


def prepare_fuzzy_matching(df_column):
    # NOT 'Oblast':'' due to moscow vs moscow oblast
    repl = {'region': 'r',
            'area': 'a',
            'Oblast': 'o',
            'Republic': 'r',
            'of': '',
            '  ': ' ',
            'Krai': 'k',
            'territory': 't'}

    return df_column.replace(repl, regex=True).str.strip()


def get_df_population_change_ru(year_from, year_to):
    df = pd.read_csv("data\\ru\\ru_2002_2022.csv")
    # print(df)

    assert (str(year_from + 2) in str(df.columns))
    assert (str(year_to + 2) in str(df.columns))

    # original region names messed, rename goals from this file
    correct_names = pd.read_csv("data\\ru\\ru_2022_correct_names.csv", encoding='utf-8')

    df.Region = prepare_fuzzy_matching(df.Region)
    correct_names['cleaned_iso_names'] = prepare_fuzzy_matching(correct_names.iso_name)

    def get_best_guess(name):
        return match_name_to_iso(name, correct_names.cleaned_iso_names, correct_names.iso_name)

    df['iso_name'] = df.Region.apply(lambda x: get_best_guess(x))

    print('Replaced: \n' + str(df.Region + ' -> ' + df.iso_name))
    df['Growth'] = df.p_2022.div(df.p_2002).mul(100)

    desc = t('NOTE_RU')

    return df, desc
