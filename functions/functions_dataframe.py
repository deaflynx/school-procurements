import pandas as pd 
import numpy as np
import re
from parameters.filters_lists import *

from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter

#---------- Фукнції для визначення координат ----------# 
# get_coordinates()
    # Використовується для визначення координат закладів за їх назвою.
    
def get_coordinates(df, target_column, new_column):
    API = "AIzaSyBVrzpUWXjQTdE3ugrd6Iaon0QNQNCmPh4"
    PATH_SC = "data/mon_data/expdata_sc.csv"
    geolocator = GoogleV3(api_key=API)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df[new_column] = df[target_column].apply(geocode)
    df["Longitude"] = df[new_column].apply(lambda loc: loc.longitude if loc else "ERROR")
    df["Latitude"] = df[new_column].apply(lambda loc: loc.latitude if loc else "ERROR")
    return df
    


#---------- Фукнції для визначення типу закладу ----------# 

# classification_by_type_one_column()
    # Використовується у Step 3 для класифікації навчальних закладів, які є замовниками і присвоєння типу.
    # Детальніше про типи див. у 'parameters/filter_lists.py'  
def classification_by_type_one_column(df, columns, priority, names, new_column):
    given_df = df[:]
    checked_priority = priority[::-1]
    checked_names = names[::-1]
    given_df[new_column] = "Невідомо"

    for column in columns:
        given_df[column + "_check"] = ""

    for idx in range(len(checked_priority)):
        checked_filter = checked_priority[idx]
        for column in columns:
            given_df[column + "_check"] = given_df[column].astype(str).str.contains(r'({})'.format('|'.join(checked_filter)),
                case = False, na = False, regex = True)

        checked_name = checked_names[idx]
        given_df[new_column] = np.where(given_df[column + '_check'] == True, checked_name, given_df[new_column])
    return given_df

def classification_by_type_city(df, columns, priority, names, new_column):
    given_df = df[:]
    checked_priority = priority[::-1]
    checked_names = names[::-1]
    given_df[new_column] = "Невідомо"
    for column in columns:
        given_df[column + "_check"] = ""
        for idx in range(len(checked_priority)):
            checked_filter = checked_priority[idx]
            for column in columns:
                given_df[column + "_check"] = (given_df[column].astype(str) == checked_filter)
                checked_name = checked_names[idx]
            given_df[new_column] = np.where(given_df[column + '_check'] == True, checked_name, given_df[new_column])
    return given_df


# classification_by_type_three_cols()
    # Використовується у Step 6 для класифікації навчальних закладів, які є не замовниками і присвоєння типу.
    # Детальніше про типи див. у 'parameters/filter_lists.py'  
def classification_by_type_three_cols(df, columns, priority, names):
    given_df = df[:]
    checked_priority = priority[::-1]
    checked_names = names[::-1]
    given_df['Тип закладу'] = "Невідомо"

    for column in columns:
        given_df[column + "_check"] = ""

    for idx in range(len(checked_priority)):
        checked_filter = checked_priority[idx]
        for column in columns:
            given_df[column + "_check"] = given_df[column].astype(str).str.contains(r'({})'.format('|'.join(checked_filter)),
                case = False, na = False, regex = True)

        checked_name = checked_names[idx]
        given_df['Тип закладу'] = np.where((given_df['Тендер_check'] == True) | (given_df['ОписаниеТендера_check'] == True) | (given_df['Лот_check'] == True), checked_name, given_df['Тип закладу'])
    return given_df


#---------- Фукнції для визначення номеру навчальних закладів ----------#

# numeration_one_column()
    # Використовується у Step 4 для визначення номеру закладу.
    # Визначається наявністья символу № в колонкці 'Организатор'. 
def numeration_one_column(given_df, columns_to_numerate, regex):
    for column in columns_to_numerate:
        given_df['Номер'] = given_df[column].str.findall(f"{regex}", flags = re.IGNORECASE).apply(''.join)
    return given_df

# long_numeration()
    # Використовується у Step 7
def long_numeration(df_step7, reg_number):
    df_step7['ОписаниеТендера'] = df_step7['ОписаниеТендера'].fillna('')
    # df_step7_numerated - результат фільтрування numeration()
    df_step7_numerated = numeration(df_step7, ['Тендер', 'Лот', 'ОписаниеТендера'], reg_number, 'numeration')
    df_step7_numerated['Номер'] = np.where(((df_step7_numerated['Тендер_numeration_count'] == 1) | (df_step7_numerated['Лот_numeration_count'] == 1)) & (df_step7_numerated['Лот_numeration_count'] == df_step7_numerated['Тендер_numeration_count']), df_step7_numerated['Лот_numeration'], 'Невідомо')
    # df_step7_numerated_lot_tender - датафрейм, де в колонці Лот і Тендер знайдено один і однаковий паттерн
    # df_step7_numerated_undefined_2 - решта неідентифікованих закупівель 
    df_step7_numerated_lot_tender = df_step7_numerated[df_step7_numerated['Номер'] != 'Невідомо']
    df_step7_numerated_undefined = df_step7_numerated[df_step7_numerated['Номер'] == 'Невідомо']
    # df_step7_numerated_lot - датафрейм, де в колонці Лот знайдений один паттерн
    # df_step7_numerated_undefined_2 - решта неідентифікованих закупівель 
    df_step7_numerated_lot = df_step7_numerated_undefined.copy()
    df_step7_numerated_lot['Номер'] = np.where(df_step7_numerated_lot['Лот_numeration_count'] == 1, df_step7_numerated_lot['Лот_numeration'], 'Невідомо')
    df_step7_numerated_undefined_2 = df_step7_numerated_lot[df_step7_numerated_lot['Номер'] == 'Невідомо']
    df_step7_numerated_lot = df_step7_numerated_lot[df_step7_numerated_lot['Номер'] != 'Невідомо']
    # df_step7_numerated_opystendera - датафрейм, де в колонці Описаниетендера знайдений один паттерн
    # df_step7_numerated_undefined_3 - решта неідентифікованих закупівель 
    df_step7_numerated_opystendera = df_step7_numerated_undefined_2.copy()
    df_step7_numerated_opystendera['Номер'] = np.where(df_step7_numerated_opystendera['ОписаниеТендера_numeration_count'] == 1, 
                                                     df_step7_numerated_opystendera['ОписаниеТендера_numeration'], 'Невідомо')
    df_step7_numerated_undefined_3 = df_step7_numerated_opystendera[df_step7_numerated_opystendera['Номер'] == 'Невідомо']
    df_step7_numerated_opystendera = df_step7_numerated_opystendera[df_step7_numerated_opystendera['Номер'] != 'Невідомо']
    # df_step7_numerated_opystendera - датафрейм, де в колонці  Тендер знайдений один паттерн
    # df_step7_numerated_undefined_4 - решта неідентифікованих закупівель 
    df_step7_numerated_tender = df_step7_numerated_undefined_3.copy()
    df_step7_numerated_tender['Номер'] = np.where(df_step7_numerated_tender['Тендер_numeration_count'] == 1, 
                                                     df_step7_numerated_tender['Тендер_numeration'], 'Невідомо')
    df_step7_numerated_undefined_4 = df_step7_numerated_tender[df_step7_numerated_tender['Номер'] == 'Невідомо']
    df_step7_numerated_tender = df_step7_numerated_tender[df_step7_numerated_tender['Номер'] != 'Невідомо']
    # df_tenders_not_by_schools_numerated - об'єднаний датафрейм шкіл-не-замовників з номерами.
    frames = [df_step7_numerated_lot_tender, df_step7_numerated_lot, df_step7_numerated_opystendera, df_step7_numerated_tender]
    df_tenders_not_by_schools_numerated = pd.concat(frames)
    return df_tenders_not_by_schools_numerated, df_step7_numerated_undefined_4

# numeration()
    # Використовується у Step 7 у функції long_numeration для визначення номеру закладу.
    # Логіка функції:
        # Визначається наявністья символу № в колонках 'Тендер', 'Лот', 'ОписаниеТендера'.
        # Регулярний вираз знаходить всі паттерни і джойнить через кому.
        # Паралельно створюється колонка, де рахується кількість знайдених паттернів.
def numeration(given_df, columns_to_numerate, regex, action_mark):
    for column in columns_to_numerate:
        given_df[column + action_mark] = given_df[column].str.findall(f"{regex}", flags = re.IGNORECASE)
        given_df[column + '_' + action_mark] = [','.join(map(str, l)) for l in given_df[column + action_mark]]
        given_df = given_df.drop([column + action_mark], axis=1)
        given_df[column + '_' + action_mark + '_count'] = given_df[column + '_' + action_mark].str.count('№')
    return given_df

#----------- Фукнції для визначення назви навчальних закладів ----------# 

# long_naming()
    # Використовується у Step 8
    # Фільтрування дафафрейму df_named ключовими словами з бази МОН school_names.
    # Паттерн '^({})$' - шукає повне співпадіння.
    # Ключові слова шукаються в колонках у такому порядку:
    #         Тендер_naming_first
    #         Лот_naming_first
    #         ОписаниеТендера_naming_first
    #         Тендер_naming_last
    #         Лот_naming_last
    #         ОписаниеТендера_naming_last
    # Якщо є співпадення - рядок вважається назвою закладу. Інші отримують статус "Невідомо".
    # Для кожної колонки створюється свій датафрейм тільки з тими рядками, де були знайдені ключові слова. 
def long_naming(df_step8, reg_double_quotes, school_names):
    # Визначення у датафреймі df_step8 власних назв функцією naming()
    df_named = naming(df_step8, ['Тендер', 'Лот', 'ОписаниеТендера'], reg_double_quotes, 'naming')  
    # Тендер_naming_first
    df_named['Назва'] = np.where(df_named['Тендер_naming_first'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named['Тендер_naming_first'], "Невідомо")
    df_named_tender = df_named[df_named['Назва'] != 'Невідомо']
    df_named_undefined_1 = df_named[df_named['Назва'] == 'Невідомо']
    # Лот_naming_first
    df_named_undefined_1['Назва'] = np.where(df_named_undefined_1['Лот_naming_first'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named_undefined_1['Лот_naming_first'], "Невідомо")
    df_named_lot = df_named_undefined_1[df_named_undefined_1['Назва'] != 'Невідомо']
    df_named_undefined_2 = df_named_undefined_1[df_named_undefined_1['Назва'] == 'Невідомо']
    # ОписаниеТендера_naming_first
    df_named_undefined_2['Назва'] = np.where(df_named_undefined_2['ОписаниеТендера_naming_first'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named_undefined_2['ОписаниеТендера_naming_first'], "Невідомо")
    df_named_opystendera = df_named_undefined_2[df_named_undefined_2['Назва'] != 'Невідомо']
    df_named_undefined_3 = df_named_undefined_2[df_named_undefined_2['Назва'] == 'Невідомо']
    # Тендер_naming_last
    df_named_undefined_3['Назва'] = np.where(df_named_undefined_3['Тендер_naming_last'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named_undefined_3['Тендер_naming_last'], "Невідомо")
    df_named_tender_last = df_named_undefined_3[df_named_undefined_3['Назва'] != 'Невідомо']
    df_named_undefined_4 = df_named_undefined_3[df_named_undefined_3['Назва'] == 'Невідомо']
    # Лот_naming_last
    df_named_undefined_4['Назва'] = np.where(df_named_undefined_4['Лот_naming_last'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named_undefined_4['Лот_naming_last'], "Невідомо")
    df_named_lot_last = df_named_undefined_4[df_named_undefined_4['Назва'] != 'Невідомо']
    df_named_undefined_5 = df_named_undefined_4[df_named_undefined_4['Назва'] == 'Невідомо']
    # ОписаниеТендера_naming_last
    df_named_undefined_5['Назва'] = np.where(df_named_undefined_5['ОписаниеТендера_naming_last'].astype(str).str.contains(r'^({})$'.format('|'.join(school_names)), case = False, na = False, regex = True), df_named_undefined_5['ОписаниеТендера_naming_last'], "Невідомо")
    df_named_opystendera_last = df_named_undefined_5[df_named_undefined_5['Назва'] != 'Невідомо'] 
    # df_tender_not_by_schools_unidentified - датафрейм шкіл-не-замовників, де не визначився ані номер, ані назва 
    df_tender_not_by_schools_unidentified = df_named_undefined_5[df_named_undefined_5['Назва'] == 'Невідомо']
    # df_tenders_not_by_schools_named - об'єднаний датафрейм шкіл-не-замовників з номерами
    # Видалення "технічних" колонок, створених функціями.
    frames = [ df_named_tender, df_named_lot, df_named_opystendera, df_named_tender_last, df_named_lot_last, df_named_opystendera_last]
    df_tenders_not_by_schools_named = pd.concat(frames)
    return df_tenders_not_by_schools_named, df_tender_not_by_schools_unidentified

# naming()
    # Використовується у Step 8 у функції long_naming для визначення назви закладу.
    # у колонках columns_to_name шукає всі паттерни (у подвійних лапках) і створює для них дві нові колонки з суфіксами: 
    #    "_first" (відбирається перше зі зі знайденого масиву)
    #    "_last" (відбирається останнє зі зі знайденого масиву)
    # Знайдені значення форматуються: видаляються символи "«»()
    # Пусті клітинки перетворюються у NaN і перейменовуються у "Невідомо".
def naming(given_df, columns_to_name, reg_double_quotes, action_mark):
    for column in columns_to_name:
        given_df[column + '_' + action_mark + "_first"] = given_df[column].str.findall(f"{reg_double_quotes}", flags = re.IGNORECASE).str[0].str[0]
        given_df[column + '_' + action_mark + "_first"] = given_df[column + '_' + action_mark + "_first"].str.replace('"|«|»', '')
        given_df[column + '_' + action_mark + "_first"] = given_df[column + '_' + action_mark + "_first"].str.replace('(', '')
        given_df[column + '_' + action_mark + "_first"] = given_df[column + '_' + action_mark + "_first"].str.replace(')', '')
        given_df[column + '_' + action_mark + "_first"] = given_df[column + '_' + action_mark + "_first"].replace(r'^\s*$', np.nan, regex=True)
        given_df[column + '_' + action_mark + "_first"] = given_df[column + '_' + action_mark + "_first"].fillna('Невідомо')
        given_df[column + '_' + action_mark + "_last"] = given_df[column].str.findall(f"{reg_double_quotes}", flags = re.IGNORECASE).str[0].str[-1]
        given_df[column + '_' + action_mark + "_last"] = given_df[column + '_' + action_mark + "_last"].str.replace('"|«|»', '')
        given_df[column + '_' + action_mark + "_last"] = given_df[column + '_' + action_mark + "_last"].str.replace('(', '')
        given_df[column + '_' + action_mark + "_last"] = given_df[column + '_' + action_mark + "_last"].str.replace(')', '')
        given_df[column + '_' + action_mark + "_last"] = given_df[column + '_' + action_mark + "_last"].replace(r'^\s*$', np.nan, regex=True)
        given_df[column + '_' + action_mark + "_last"] = given_df[column + '_' + action_mark + "_last"].fillna('Невідомо')
    return given_df

# naming_one_column()
    # Використовується в 'filter MON data'
def naming_one_column(given_df, columns_to_numerate, regex):
    for column in columns_to_numerate:
        given_df['Назва'] = given_df[column].str.findall(f"{regex}", flags = re.IGNORECASE).str[0].str[-1]
    return given_df    