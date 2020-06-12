
# coding: utf-8

# In[2]:

import pandas
import importlib
from route import path_positive_edrpou, path_negative_edrpou
from functions_shared import list_convert_el_to_str

def get_mon_data():
    edropu_manual_list = pandas.read_csv(path_positive_edrpou)
    edrpous = edropu_manual_list.edrpou.tolist()
    edrpous_str = list_convert_el_to_str(edrpous)
    return edrpous_str

