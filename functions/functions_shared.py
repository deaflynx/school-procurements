def list_convert_el_to_str(ls):
    new_list = []
    for i in range(0, len(ls)):
        try:
            new_list.append(str(ls[i]))
        except ValueError:
            new_list.append('1')
    return new_list

def list_convert_el_to_number(ls):
    new_list = []
    for i in range(0, len(ls)):
        try:
            new_list.append(int(ls[i]))
        except ValueError:
            new_list.append('1')
    return new_list

def filter_by_len(words, size):
    return [word for word in words if len(word) == size]

def extend_lists(list_names):
    new = []
    for i in range(len(list_names)-1):
        new.extend(list_names[i])
    return [i for n, i in enumerate(new) if i not in new[:n]] 