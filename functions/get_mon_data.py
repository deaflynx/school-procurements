import pandas
import importlib
from parameters.route import path_positive_edrpou, path_negative_edrpou
from functions.functions_shared  import list_convert_el_to_str

def positive_edrpous():
    edropu_manual_list = pandas.read_csv(path_positive_edrpou)
    edrpous = edropu_manual_list.edrpou.tolist()
    edrpous_str = list_convert_el_to_str(edrpous)
    return edrpous_str

def negative_edrpou():
    edropu_manual_list = pandas.read_csv(path_negative_edrpou)
    edrpous = edropu_manual_list.edrpou.tolist()
    edrpous_str = list_convert_el_to_str(edrpous)
    return edrpous_str

def get_mon_data():
    edropu_manual_list = pandas.read_csv(path_positive_edrpou)
    edrpous = edropu_manual_list.edrpou.tolist()
    edrpous_str = list_convert_el_to_str(edrpous)
    return edrpous_str