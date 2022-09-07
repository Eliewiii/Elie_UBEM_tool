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

if __name__=="__main__":

    path_folder_csv = "D:\Elie\PhD\Simulation\Input_Data\Typology\list_constructionsets\configuration_to_test"
    name_csv = "IS_5280_ReferenceConstSet_A"

    constructionset_list_csv_to_json(path_folder_csv, name_csv)