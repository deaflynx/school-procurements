
# coding: utf-8

# In[ ]:


import pandas
import numpy as np
from filters_lists import *

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

def printHello():
    print('hello')
