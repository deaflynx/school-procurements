import pandas 
from parameters.filters_lists import *

def filter_dataframe(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'\b({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pandas.concat(filtered).drop_duplicates()
    print(f"{len(dataframe)} rows. After filtering: {len(df)}")
    return df

def filter_dataframe_strict(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'\b({})\b'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pandas.concat(filtered).drop_duplicates()
    print(f"{len(dataframe)} rows. After filtering: {len(df)}")
    return df

def filter_dataframe_drop(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[~dataframe[column].astype(str).str.contains(r'({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pandas.concat(filtered).drop_duplicates()
    print(f"Dropped rows: {len(dataframe)-len(df)}")
    return df

def filter_dataframe_inspect_before_drop(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pandas.concat(filtered).drop_duplicates()
    print(df.shape)
    return df

def step_check(given_df, column, number):
        given_df[column + '_step' + number + '_check'] = (given_df[column].str.contains(r'\b({})'.format('|'.join(filter_keywords)), case = False, na = False, regex = True)) | (given_df[column].str.contains(r'\b({})\b'.format('|'.join(filter_keywords_strict)), case = False, na = False, regex = True))
        return given_df

def separate_positives_and_negatives_ogranizator(df_step1, step_mark, action_mark):
        df_positives = df_step1.drop(df_step1[~(df_step1[f"Организатор_{step_mark}_{action_mark}"] == True)].index)
        df_negatives = df_step1.drop(df_step1[(df_step1[f"Организатор_{step_mark}_{action_mark}"] == True)].index)
        return df_positives, df_negatives

def separate_positives_and_negatives(df_step1, step_mark, action_mark):
        df_positives = df_step1.drop(df_step1[~((df_step1[f"Тендер_{step_mark}_{action_mark}"] == True) | (df_step1[f"Организатор_{step_mark}_{action_mark}"] == True) |
                                        (df_step1[f"ОписаниеТендера_{step_mark}_{action_mark}"] == True) | (df_step1[f"Лот_{step_mark}_{action_mark}"] == True))].index)
        df_negatives = df_step1.drop(df_step1[((df_step1[f"Тендер_{step_mark}_{action_mark}"] == True) | (df_step1[f"Организатор_{step_mark}_{action_mark}"] == True) |
                                        (df_step1[f"ОписаниеТендера_{step_mark}_{action_mark}"] == True) | (df_step1[f"Лот_{step_mark}_{action_mark}"] == True))].index)
        return df_positives, df_negatives

def clear_redundant_columns(given_df, step_mark, action_mark, column):
    given_df = given_df.drop(columns=column + '_' + step_mark + '_' + action_mark)
    return given_df