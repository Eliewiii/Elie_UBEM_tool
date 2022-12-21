import os
import shutil
class Library:
    """
    Loads the construction, construction set, material, schedule and program libraries

    """
    @staticmethod
    def load_HBjson_sets(path_construction_and_load_library_folder,path_LBT_user_defined):
        """
        Load the user defined libraries of constructions, schedules and programs
        """
        ## materials and constructions
        construction_folder = os.path.join(path_construction_and_load_library_folder,"constructions")
        for construction_file in os.listdir(construction_folder):
            try:
                source= os.path.join(construction_folder,construction_file)
                destination = os.path.join(path_LBT_user_defined,"constructions")
                shutil.copy(source, destination)
            # If there is any permission issue
            except PermissionError:
                print("Permission typology load denied.")
        ## sets of constructions
        constructions_sets_folder = os.path.join(path_construction_and_load_library_folder,"constructionsets")
        for constructions_sets_file in os.listdir(constructions_sets_folder):
            try:
                source= os.path.join(constructions_sets_folder,constructions_sets_file)
                destination = os.path.join(path_LBT_user_defined,"constructionsets")
                shutil.copy(source, destination)
            # If there is any permission issue
            except PermissionError:
                print("Permission typology load denied.")
        ## Program types
        program_types_folder = os.path.join(path_construction_and_load_library_folder,"programtypes")
        for program_types_file in os.listdir(program_types_folder):
            try:
                source= os.path.join(program_types_folder,program_types_file)
                destination = os.path.join(path_LBT_user_defined,"programtypes")
                shutil.copy(source, destination)
            # If there is any permission issue
            except PermissionError:
                print("Permission typology load denied.")
        ## Schedules
        schedules_folder = os.path.join(path_construction_and_load_library_folder,"schedules")
        for schedules_file in os.listdir(schedules_folder):
            try:
                source= os.path.join(schedules_folder,schedules_file)
                destination = os.path.join(path_LBT_user_defined,"schedules")
                shutil.copy(source, destination)
            # If there is any permission issue
            except PermissionError:
                print("Permission typology load denied.")


