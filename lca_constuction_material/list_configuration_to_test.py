"""

"""

import json
import os

from copy import deepcopy

def configuation_to_test_csv_to_json(path_folder_csv, name_csv):
    """ """
    lines_csv = None
    # extract data csv
    with open(os.path.join(path_folder_csv, name_csv + ".csv"), "r") as csv_file:
        data = csv_file.read()
        lines_csv = data.split("\n")

    # create the dictionary to dump in json file
    dict_to_dump = {}

    element_line_const_set = lines_csv[0].split(",")
    element_line_surface_type = lines_csv[1].split(",")
    element_line_layer = lines_csv[2].split(",")

    n_row = len(element_line_const_set)  # number of row

    sub_dict_sample = {"construction_sets":{},"is_reference":False}
    const_set = None
    surface_type = None
    for i in range(2, n_row):
        if element_line_const_set[i] != "":
            const_set = element_line_const_set[i]
            sub_dict_sample["construction_sets"][const_set] = {"surface_types": {}}
        elif element_line_surface_type[i] != surface_type:
            surface_type = element_line_surface_type[i]
            sub_dict_sample["construction_sets"][const_set]["surface_types"][surface_type] = {}
            sub_dict_sample["construction_sets"][const_set]["surface_types"][surface_type][element_line_layer[i]] = None

    const_set = None
    for line in lines_csv[3:]:  # ignore the first one
        if line != "":
            sub_dict = deepcopy(sub_dict_sample)
            element_list = line.split(",")
            # check if this configuration is the reference one 9to compare the result later)

            # extract all the data in the line
            for i in range(2, n_row):
                # check if still in the same construction set
                if element_line_const_set[i] != "":
                    const_set = element_line_const_set[i]
                    sub_dict["construction_sets"][const_set]["new_const_set"] = element_list[i]
                else:
                    surface_type = element_line_surface_type[i]
                    layer = element_line_layer[i]
                    sub_dict["construction_sets"][const_set]["surface_types"][surface_type][layer] = int(element_list[i])
            if element_list[1] == "TRUE":
                sub_dict["is_reference"] = True
            dict_to_dump[element_list[0]] = sub_dict

    # write data in json
    with open(os.path.join(path_folder_csv, name_csv + ".json"), "w") as out_file:
        json.dump(dict_to_dump, out_file, indent=4)
    return(dict_to_dump)


if __name__ == "__main__":
    path_folder_csv = "D:\Elie\PhD\Simulation\Input_Data\Typology\list_constructionsets\\test"
    name_csv = "IS_5280_ReferenceConstSet_A"

    constructionset_list_csv_to_json_new(path_folder_csv, name_csv)
