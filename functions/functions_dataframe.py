import pandas as pd 
import numpy as np
import re
from parameters.filters_lists import *

def classification_by_type(df, columns, priority, names):
    given_df = df[:]
    checked_priority = priority[::-1]
    checked_names = names[::-1]
    given_df['Тип закладу'] = "Невідомо"

    for column in columns:
        given_df[column + "_check"] = ""

    for idx in range(len(checked_priority)):
        checked_filter = checked_priority[idx]
        for column in columns:
            given_df[column + "_check"] = given_df[column].astype(str).str.contains(r'\b({})'.format('|'.join(checked_filter)),
                case = False, na = False, regex = True)

        checked_name = checked_names[idx]
        given_df['Тип закладу'] = np.where(((given_df['Организатор_check'] == True) | (given_df['Тендер_check'] == True) | (given_df['ОписаниеТендера_check'] == True) | (given_df['Лот_check'] == True) | (given_df['Адрес поставки_check']) == True), checked_name, given_df['Тип закладу'])
    return given_df

# EXPERIMENTS WITH FUNCTION

def classification_by_type_one_column(df, columns, priority, names):
    given_df = df[:]
    checked_priority = priority[::-1]
    checked_names = names[::-1]
    given_df['Тип закладу'] = "Невідомо"

    for column in columns:
        given_df[column + "_check"] = ""

    for idx in range(len(checked_priority)):
        checked_filter = checked_priority[idx]
        for column in columns:
            given_df[column + "_check"] = given_df[column].astype(str).str.contains(r'\b({})'.format('|'.join(checked_filter)),
                case = False, na = False, regex = True)

        checked_name = checked_names[idx]
        given_df['Тип закладу'] = np.where(given_df['Организатор_check'] == True, checked_name, given_df['Тип закладу'])
    return given_df


def numeration_one_column(given_df, columns_to_numerate, regex):
    for column in columns_to_numerate:
        given_df['Номер'] = given_df[column].str.findall(f"{regex}", flags = re.IGNORECASE).apply(''.join)
    return given_df


def naming_one_column(given_df, columns_to_numerate, regex):
    for column in columns_to_numerate:
        given_df['Назва'] = given_df[column].str.findall(f"{regex}", flags = re.IGNORECASE).str[0].str[-1]
    return given_df






# ---- ----- ----- ------ ----- #



def filter_dataframe(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'\b({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pd.concat(filtered).drop_duplicates()
    print(f"{len(dataframe)} rows. filtered {len(df)}")
    return df

def filter_dataframe_strict(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'\b({})\b'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pd.concat(filtered).drop_duplicates()
    print(f"{len(dataframe)} rows, filtered: {len(df)}")
    return df

def filter_dataframe_drop(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[~dataframe[column].astype(str).str.contains(r'({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pd.concat(filtered).drop_duplicates()
    print(f"Dropped rows: {len(dataframe)-len(df)}")
    return df

def filter_dataframe_inspect_before_drop(dataframe, filter_keywords, columns_to_check):
    filtered = []
    for column in columns_to_check:
            filtered.append(dataframe[dataframe[column].astype(str).str.contains(r'({})'.format('|'.join(filter_keywords)), 
            case = False, na = False, regex = True)])
    df = pd.concat(filtered).drop_duplicates()
    print(df.shape)
    return df

def step_check(given_df, column, number):
    given_df[column + '_step' + number + '_check'] = (given_df[column].str.contains(r'\b({})'.format('|'.join(filter_keywords)), case = False, na = False, regex = True)) |(given_df[column].str.contains(r'\b({})\b'.format('|'.join(filter_keywords_strict)), case = False, na = False, regex = True))
    return given_df

def separate_positives_and_negatives_ogranizator(df_step1, step_mark, action_mark):
        df_positives = df_step1.drop(df_step1[~(df_step1[f"Организатор_{step_mark}_{action_mark}"] == True)].index)
        df_negatives = df_step1.drop(df_step1[(df_step1[f"Организатор_{step_mark}_{action_mark}"] == True)].index)
        return df_positives, df_negatives


def separate_positives_and_negatives(df_step1, step_mark, action_mark):
        df_positives = df_step1.drop(df_step1[~((df_step1[f"Тендер_{step_mark}_{action_mark}"] == True) | (df_step1[f"ОписаниеТендера_{step_mark}_{action_mark}"] == True) | (df_step1[f"Лот_{step_mark}_{action_mark}"] == True))].index)
        df_negatives = df_step1.drop(df_step1[((df_step1[f"Тендер_{step_mark}_{action_mark}"] == True) | (df_step1[f"ОписаниеТендера_{step_mark}_{action_mark}"] == True) | (df_step1[f"Лот_{step_mark}_{action_mark}"] == True))].index)
        return df_positives, df_negatives

def clear_redundant_columns(given_df, step_mark, action_mark, column):
    given_df = given_df.drop(columns=column + '_' + step_mark + '_' + action_mark)
    return given_df