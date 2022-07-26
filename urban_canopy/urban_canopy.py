""" Class containing all the urban canopy (buildings, surfaces etc...) """

import os
import geopandas as gpd
import shapely
import shutil

from honeybee_energy import run
from honeybee_energy.config import folders
from ladybug.futil import write_to_file

from typology import Typology
from tools._folder_manipulation import make_sub_folders

# additional methods for the Urban_canopy class

from urban_canopy import _EP_simulation, _context_filtering, _extract_data, _outputs_for_GH_visualization, \
    _geometry_and_HB


class Urban_canopy(_context_filtering.Mixin, _EP_simulation.Mixin, _extract_data.Mixin, _geometry_and_HB.Mixin,
                   _outputs_for_GH_visualization.Mixin):
    """
    Urban canopy recreated from a GIS file.

    Args:
        name [str] : Name of the urban canopy (just to initialize it)

    Attributes:
        * name
        * building_id_list
        * building_dict
        * target_building
        * building_to_simulate
        * many more
    """

    def __init__(self, name):
        """Initialize the Urban Canopy"""
        # process the boundary and plane inputs
        self.name = name
        self.num_of_buildings = 0
        self.building_dict = {}
        self.target_buildings = []
        self.building_to_simulate = []
        self.typology_dict = {}
        self.simulation_parameters = None  # Simulation parameters, extracted from json files
        self.simulation_parameters_idf_str = None
        self.hvac_system = None

    def __str__(self):
        """ what you see when you print the urban canopy object """
        return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")

    def __repr__(self):
        """ what you see when you type the urban canopy variable in the console """
        return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")

    # # # # # # # # # # # # # # # #                Load Typology               # # # # # # # # # # # # # # # # # # # # #

    def load_typologies(self, typo_folder_path):
        ### listdir of all typo in the typo folder (and maybe create all the typo directly ?)
        typo_folders = os.listdir(typo_folder_path)
        ### for all typo, copy the constructions, loads etc... in the LBT folder
        for typo in typo_folders:
            ### create the typo object
            typo_obj = Typology.from_json(typo_folder_path + "//" + typo)
            self.typology_dict[typo_obj.identifier] = typo_obj

    # # # # # # # # # # # # # # # #                   Extraction               # # # # # # # # # # # # # # # # # # # # #

    def extract_gis_2D(self, path, unit):
        """ exctract the data from a shp file and create the associated buildings objects"""
        ## read GIS
        shape_file = gpd.read_file(path)
        # shape_file.plot()
        # plt.show()
        ## number of buildings##
        # in the shp file (not necessarily the real number of buildings, a building_zon can be made of several elements)
        number_of_building_shp = len(shape_file['geometry'])

        ## loop to create a building_zon for each foot print in the shp file
        for building_number_shp in range(0, number_of_building_shp):
            # for building_number_shp in range(0, 5):  # few buildings
            # for building_number_shp in range(3,8): # few buildings
            footprint = shape_file['geometry'][building_number_shp]
            if isinstance(footprint,
                          shapely.geometry.polygon.Polygon):  # if the building_zon is made of 1 footprint (isinstance check if the type is correct)
                self.polygon_to_building(footprint, shape_file, building_number_shp, unit)
            elif isinstance(footprint,
                            shapely.geometry.multipolygon.MultiPolygon):  # if the building_zon is made of multiple footprints
                self.multipolygon_to_building(footprint, shape_file, building_number_shp, unit)
            else:
                print(("geometry {} in shp file is not a POLYGON").format(building_number_shp))

    # # # # # # # # # # # # # # # #          Create Building and Geometry      # # # # # # # # # # # # # # # # # # # # #

    def add_building(self, id, building_object):
        """ add a building_zon object to the urban canopy """
        self.building_dict[id] = building_object
        self.num_of_buildings += 1

    def select_target_building(self, id_list):
        """
        Set the target buildings that will need to be simulate
        Args:
            * id_list : list of the ids (from the shapefile ! not the local ids here, the shp_id property of buildings)
                        of the building_zon to simulate
        """
        for id in self.building_dict:
            if self.building_dict[id].shp_id in id_list:
                self.building_dict[id].is_target = True

    def add_context_simulated_building(self, building_id):
        """
        Add a simulated context building_zon to the Urban Canopy
        """
        self.building_to_simulate.append(self.building_dict[building_id])
        self.building_dict[building_id].is_simulated = True

    # # # # # # # # # # # # # #       Force characteristics on building_zon      # # # # # # # # # # # # # # # # # # # # #

    def apply_buildings_characteristics(self):
        """
        After assigning typologies to buildings, load the constructions, constructions sets, loads etc...
        of the typology of the building_zon
        """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_apply_buildings_characteristics()

    # # # # # # # # # # # # # # # #       force floor typology   # # # # # # # # # # # # # # # # # # # # #

    def force_typology(self, typo_identifier):
        """ apply the layout of a given typology without adaption to the building_zon specificities, just for the tests """
        for id in self.building_to_simulate:
            if self.building_dict[id].typology == None:
                self.building_dict[id].typology = self.typology_dict[typo_identifier]

    # # # # # # # # # # # # # # # #       force floor layout on buildings    # # # # # # # # # # # # # # # # # # # # #

    def create_DF_building_according_to_typology(self):
        """ create DF buildings from a forced typology layout for all the buildings"""
        self.Apply_floor_layout()
        self.LB_layout_to_DF_story()
        self.DF_story_to_DF_building()

        # todo : make it complete and add the typology

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #               Honeybee modeling             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # todo: reorganize
    def generate_HB_model(self):
        self.DF_to_HB()

    # def add_hvac_system_to_building(self, paramater_set="default"):
    #     """
    #
    #     Need to be set after conditioning the zones
    #     """
    #     self.configure_ideal_hvac_system(paramater_set="default")  # set the self.hvac_system
    #     for id in self.building_to_simulate:
    #         self.building_dict[id].add_hvac_system(self.hvac_system)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #          Context filter algorithm           # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # def filter_context(self, VF_criteria):
    #     """
    #     1- identify the buildings that are close to the target buildings and that should be simulated
    #     2- identify the buildings that are close to the simulated context buildings and that should be part of their context
    #     3- Select the context surfaces
    #     """
    #     target_buildings_face_list = []
    #     all_building_face_list = []
    #     context_simulated_building_face_list = []
    #
    #     ## prepare target building_zon surfaces
    #     for id in self.target_buildings:
    #         target_buildings_face_list.append([id, self.building_dict[id].prepare_face_for_context(reverse=False)])
    #     ## prepare all building_zon surfaces
    #     for not_used, (id, building_obj) in enumerate(self.building_dict.items()):
    #         all_building_face_list.append([id, building_obj.prepare_face_for_context(reverse=True)])
    #
    #     for target_building_face_list in target_buildings_face_list:
    #         context_building_face_list_kept = []  # list with the id of the context buildings for this building_zon
    #         ## first check, just identify the buildings if one surface fits the requirement
    #         for test_context_building_face_list in all_building_face_list:
    #             if target_building_face_list[0] != test_context_building_face_list[
    #                 0]:  # check if the buildings are not the same
    #                 if is_context_building(target_building_face_list[1], test_context_building_face_list[1],
    #                                        VF_criteria) == True:
    #                     context_building_face_list_kept.append(test_context_building_face_list)
    #                     self.building_dict[target_building_face_list[0]].context_buildings_id.append(
    #                         test_context_building_face_list[0])
    #                     # self.building_dict[test_context_building_face_list[0]].is_simulated=True
    #                 else:
    #                     None
    #             else:
    #                 None
    #         for test_context_building_face_list in context_building_face_list_kept:
    #             self.filter_context_surfaces(target_building_face_list[1], test_context_building_face_list[1],
    #                                          target_id=target_building_face_list[0],
    #                                          VF_criteria=VF_criteria)
    #
    #         ## second check, check every surfaces in the selected context buildings
    #
    #     ## prepare the simulated buildings that are not targets

    def add_context_surfaces_to_HB_model(self):
        """
        """
        for id in self.building_to_simulate:
            self.building_dict[id].add_context_surfaces_to_HB_model()

    # # # # # # # # # # # # # # # #    Detect Typology and assign the layout   # # # # # # # # # # # # # # # # # # # # #

    def detect_typology(self):
        """ detect the typology of building_zon, their orientation and width/length ratio according to their shape"""

        # # Use recognition algorithm to get the shape type # #

        # # Guess the final typology with the shape type and the other properties of the buildings # #

        None

    def Apply_layout(self):
        """ Apply the layout of the data base to the buildings """

        # # add all the faces to the building_zon foot print, distinguishing cores and apartments # #

        # # convert the surfaces to Ladybug faces # #

        None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                Generate IDF                 # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def model_to_HBjson(self, path_folder_building_simulation):  # can be done in parallel
        """

        """
        ## Generate models ##
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            ## Convert HB model to hbjson file ##
            for room in self.building_dict[building_id].HB_model.rooms:
                room.remove_colinear_vertices_envelope(0.1)
            self.building_dict[building_id].HB_model.to_hbjson("in", os.path.join(path_dir_building, "HBjson_model"))
            # run.measure_compatible_model_json(path_dir_building + "//model_json//in.hbjson")

    def simulate_idf(self, path_folder_building_simulation, path_simulation_parameter, path_file_epw,
                     path_energyplus_exe):
        """
        """
        ## Create simulation folders ##
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            ## Convert HB model to hbjson file ##
            model_json_path = os.path.join(path_dir_building, "HBjson_model", "in.hbjson")
            ## Prepare simulation for OpenStudio ##
            osw = run.to_openstudio_osw(osw_directory=os.path.join(path_dir_building, "EnergyPlus_simulation"),
                                        model_json_path=model_json_path,
                                        sim_par_json_path=path_simulation_parameter,
                                        epw_file=path_file_epw)
            ## Run simulation in OpenStudio to generate IDF ##
            (osm, idf) = run.run_osw(osw, measures_only=True, silent=False)
            # zob = run.run_idf(idf, epw_file_path=path_file_epw,silent=False)
            zob = run_idf_windows_modified(idf_file_path=idf, epw_file_path=path_file_epw, expand_objects=True,
                                           silent=False, path_energyplus_exe=path_energyplus_exe)

    def create_simulation_folder_buildings(self, path_folder_building_simulation):
        """ Generate the output simulation folder and the sub-folder of each simulated building_zon """
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            make_sub_folders(path_dir_building,
                             ["Building_object", "Context_surfaces_json", "EnergyPlus_simulation", "HBjson_model",
                              "Results"])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                Context                      # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


########################## additional functions for GIS/shp extraction##############
def polygon_to_points(polygon):
    """      """
    ## ADD COMMENTS

    exterior_footprint = polygon.exterior.__geo_interface__['coordinates']
    # eventually check that the footprint is well oriented
    interior_holes = None
    try:
        polygon.interiors
    except:
        None
    else:
        interior_holes = []
        for hole in polygon.interiors:
            if hole.__geo_interface__['coordinates'] != None:
                interior_holes.append(hole.__geo_interface__['coordinates'])

    return ([exterior_footprint, interior_holes])


# def is_context_building(target_building_face_list, test_context_building_face_list, VF_criteria):
#     """
#     Check if the  test_context_building is part of the context
#     """
#     for target_face in target_building_face_list:
#         for test_face in test_context_building_face_list:
#             if max_VF(target_face, test_face) >= VF_criteria:
#                 return (True)
#     return (False)
#


def clean_folder(path):
    """
    Clean a folder by deleting it and recreating it
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def run_idf_windows_modified(idf_file_path, epw_file_path=None, expand_objects=True,
                             silent=False, path_energyplus_exe=None):
    """Run an IDF file through energyplus on a Windows-based operating system.

    A batch file will be used to run the simulation.
    BATCH FILE MODIFIED FROM THE ORIGINAL VERSION
    I ADD OME MORE OPTION TO GET CSV FILE AS OUTPUTS AAS WELL

    Args:
        idf_file_path: The full path to an IDF file.
        epw_file_path: The full path to an EPW file. Note that inputting None here
            is only appropriate when the simulation is just for design days and has
            no weather file run period. (Default: None).
        expand_objects: If True, the IDF run will include the expansion of any
            HVAC Template objects in the file before beginning the simulation.
            This is a necessary step whenever there are HVAC Template objects in
            the IDF but it is unnecessary extra time when they are not
            present. (Default: True).
        silent: Boolean to note whether the simulation should be run silently
            (without the batch window). If so, the simulation will be run using
            subprocess with shell set to True. (Default: False).

    Returns:
        Path to the folder out of which the simulation was run.
    """
    # check and prepare the input files
    directory = run.prepare_idf_for_simulation(idf_file_path, epw_file_path)

    if not silent:  # run the simulations using a batch file
        # generate various arguments to pass to the energyplus command
        epw_str = '-w "{}"'.format(os.path.abspath(epw_file_path)) \
            if epw_file_path is not None else ''
        # idd_str = '-i "{}"'.format(folders.energyplus_idd_path)
        idf_str = '-r {}'.format("in.idf")
        working_drive = directory[:2]
        # write the batch file
        batch = '{}\ncd "{}"\n"{}" {} {}'.format(
            working_drive, directory, path_energyplus_exe, epw_str,
            idf_str)
        batch_file = os.path.join(directory, 'in.bat')
        write_to_file(batch_file, batch, True)
        os.system('"{}"'.format(batch_file))  # run the batch file
    else:  # run the simulation using subprocess
        cmds = [folders.energyplus_exe, '-i ', folders.energyplus_idd_path, '-r ', idf_file_path]
        if epw_file_path is not None:
            cmds.append('-w')
            cmds.append(os.path.abspath(epw_file_path))
        if expand_objects:
            cmds.append('-x')
        process = subprocess.Popen(
            cmds, cwd=directory, stdout=subprocess.PIPE, shell=True)
        process.communicate()  # prevents the script from running before command is done

    return directory


# todo: make proper name=name with proper mixin classes
if __name__ == '__main__':
    a = Urban_canopy("yo")
