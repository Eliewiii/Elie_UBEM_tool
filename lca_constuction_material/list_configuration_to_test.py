"""

"""

import json
import os


def constructionset_list_csv_to_json(path_folder_csv,name_csv):
    """ """
    lines_csv = None
    # extract data csv
    with open(os.path.join(path_folder_csv,name_csv +".csv"), "r") as csv_file:
        data = csv_file.read()
        lines_csv = data.split("\n")

    # create the dictionary to dump in json file
    dict_to_dump = {}

    element_first_line = lines_csv[0].split(",")
    n_row = len(element_first_line)  # number of row


    for line in lines_csv[1:]:  # ignore the first one
        if line!="":
            sub_dict = {}
            element_list = line.split(",")
            for i in range(1,n_row):
                print(i)
                sub_dict[element_first_line[i]] = int(element_list[i])
            dict_to_dump[element_list[0]] = sub_dict

    # write data in json
    with open(os.path.join(path_folder_csv,name_csv+".json"),"w") as out_file:
        json.dump(dict_to_dump, out_file, indent=4)

def constructionset_list_csv_to_json_new(path_folder_csv,name_csv):
    """ """
    lines_csv = None
    # extract data csv
    with open(os.path.join(path_folder_csv,name_csv +".csv"), "r") as csv_file:
        data = csv_file.read()
        lines_csv = data.split("\n")

    # create the dictionary to dump in json file
    dict_to_dump = {}

    element_line_const_set = lines_csv[0].split(",")
    element_line_surface_type = lines_csv[1].split(",")
    element_line_layer = lines_csv[2].split(",")

    n_row = len(element_line_const_set)  # number of row

    sub_dict_sample={}
    const_set= None
    surface_type=None
    for i in range(1, n_row):
        if element_line_const_set[i] != "":
            const_set = element_line_const_set[i]
            sub_dict_sample[const_set]={}
        if element_line_surface_type[i] != surface_type:
            surface_type = element_line_surface_type[i]
            sub_dict_sample[const_set][surface_type] = {}
        sub_dict_sample[const_set][surface_type][element_line_layer[i]]=None

    const_set= None
    for line in lines_csv[3:]:  # ignore the first one
        if line!="":
            sub_dict = dict(sub_dict_sample)
            element_list = line.split(",")
            for i in range(1,n_row):
                if element_line_const_set[i]!="":
                    const_set=element_line_const_set[i]
                surface_type=element_line_surface_type[i]
                layer=element_line_layer[i]
                sub_dict[const_set][surface_type][layer] = int(element_list[i])
            dict_to_dump[element_list[0]] = dict(sub_dict)

    # write data in json
    with open(os.path.join(path_folder_csv,name_csv+".json"),"w") as out_file:
        json.dump(dict_to_dump, out_file, indent=4)





if __name__=="__main__":

    path_folder_csv = "D:\Elie\PhD\Simulation\Input_Data\Typology\list_constructionsets\\test"
    name_csv = "IS_5280_ReferenceConstSet_A"

    constructionset_list_csv_to_json_new(path_folder_csv, name_csv)