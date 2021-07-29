# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
def fill_strange_vals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace('<15',value = 14)
    df['agas_code'] = df['agas_code'].fillna('999.0')  # random statistical area
    return df


# %%
def cols_to_int(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        'agas_code',
        'accumulated_cases',
        'accumulated_recoveries',
        'accumulated_deaths',
        'accumulated_hospitalized',
        'accumulated_vaccination_first_dose',
        'accumulated_vaccination_second_dose',
        'accumulated_diagnostic_tests'
    ]
    for h in columns:
        try:
            df[h]= df[h].astype('int')
        except:
            df[h]= df[h].astype('float')
    return df


# %%
def bin_to_int(df: pd.DataFrame):
    return df.replace({False: 0, True: 1}, inplace=True)


# %%
def drop_cols(df: pd.DataFrame):
    columns = [
        'town',
        # 'new_cases_on_date',
        # 'new_recoveries_on_date',
        # 'new_hospitalized_on_date',
        # 'new_deaths_on_date',
        # 'new_diagnostic_tests_on_date',
        'new_vacc_first_dose_on_date',
        'new_vacc_second_dose_on_date',
        'accumulated_vaccination_first_dose',
        'accumulated_vaccination_second_dose'
    ]
    return df.drop(columns, axis=1)


# %%
def calc_changes(df: pd.DataFrame):
    df = df.sort_values(by=["agas_code","date"])
    df = df.assign(new_cases = ( df['accumulated_cases'] - df['accumulated_recoveries'] - df['accumulated_deaths']) )
    df["new_cases_percent"] = df.groupby("agas_code")["new_cases"].pct_change()

    df["new_deaths"] = df.groupby("agas_code")["accumulated_deaths"].diff()
    df["new_recoveries"] = df.groupby("agas_code")["accumulated_recoveries"].diff()

    # some na's might have been created
    df["new_deaths"] =df["new_deaths"].fillna(0)
    df["new_recoveries"] =df["new_recoveries"].fillna(0)
    df["new_cases_percent"] = df["new_cases_percent"].fillna(0)
    df = df.replace(np.inf, 100)
    df = df.replace(-np.inf, -100)
    return df


# %%
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = fill_strange_vals(df)
    df = cols_to_int(df)
    bin_to_int(df)
    df = calc_changes(df)
    df = drop_cols(df)
    return df


