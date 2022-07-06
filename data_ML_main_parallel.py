"""

"""
from data_ML import *
import os

building_type_folder_path = "D://Elie//PhD//Programming//GIS//Building_type//North_Tel_Aviv//Training_data"
# building_type_folder_path = "D://Elie//PhD//Programming//GIS//Building_type//North_Tel_Aviv//Verification"

is_deg = True # if the GIS is in degree and not meters

ML_path = "D://Elie//PhD//Programming//Machine_Learning_Identifier"

output_folder_name = "Training_data"
# output_folder_name = "Test_data"


ML_output_folder_path = os.path.join(ML_path, output_folder_name)


nb_sample_noise = 300

## Clean output folder ##
clean_directory(ML_output_folder_path)

# go to the folder with the sample
building_type_folders = os.listdir(building_type_folder_path)



# loop on all the building shape
for building_type in building_type_folders :
    type_path = os.path.join(building_type_folder_path, building_type) # path directory with all the samples
    ## create a folder to store the generated images
    output_building_type_path = os.path.join(ML_output_folder_path, building_type)
    os.mkdir(output_building_type_path)
    ## Loop on all the samples
    index = 0
    sample_list = os.listdir(type_path)
    for sample in sample_list :
        for gis_file in os.listdir(os.path.join(type_path, sample)):
            if gis_file.endswith(".shp"):
                print("zob")
                path_file_shp = os.path.join(type_path, sample, gis_file )
                index = generate_data_base_from_sample_parallel(path_file_shp,index,output_building_type_path,nb_sample_noise,is_deg)



# delete than create one folder to put all the new images

# loop on all the sample

# create an image for each sample

# generate artificial new samples



















