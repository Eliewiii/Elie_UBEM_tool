"""

"""


def dict_assign_if_key_exist(dict_para, key):
    """ Return the value if the key exist, otherwise return None"""
    try:
        dict_para[key]
    except:
        return None
    else:
        return dict_para[key]
