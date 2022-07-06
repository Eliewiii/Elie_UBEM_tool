""" Class containing all the urban canopy (buildings, surfaces etc...) """

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
import json
import shutil

from math import sqrt,atan,pi,log

from ladybug.epw import EPW

from honeybee.room import Room
from honeybee.model import Model

from honeybee.model import Model
from honeybee_energy.simulation.output import SimulationOutput
from honeybee_energy.simulation.sizing import SizingParameter
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.parameter import SimulationParameter

from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.lib.programtypes import program_type_by_identifier

from honeybee_energy import run
from honeybee_energy.config import folders
from ladybug.futil import write_to_file, preparedir


from typology import Typology
from building import Building

class Urban_canopy:
    """
    Urban canopy recreated from a GIS file.

    Args:
        name [str] : Name of the urban canopy (just to initialize it)

    Properties:
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
        self.simulation_parameters = None # Simulation parameters, extracted from json files
        self.simulation_parameters_idf_str = None

    def __str__(self):
        """ what you see when you print the urban canopy object """
        return(f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings" )
    def __repr__(self):
        """ what you see when you type the urban canopy variable in the console """
        return(f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings" )

    # # # # # # # # # # # # # # # #                Load Typology               # # # # # # # # # # # # # # # # # # # # #

    def load_typologies(self,typo_folder_path):
        ### listdir of all typo in the typo folder (and maybe create all the typo directly ?)
        typo_folders = os.listdir(typo_folder_path)
        ### for all typo, copy the constructions, loads etc... in the LBT folder
        for typo in typo_folders:

            ### create the typo object
            typo_obj = Typology.from_json(typo_folder_path+"//"+typo)
            self.typology_dict[typo_obj.identifier]=typo_obj

    # # # # # # # # # # # # # # # #                   Extraction               # # # # # # # # # # # # # # # # # # # # #

    def extract_gis_2D(self, path,unit):
        """ exctract the data from a shp file and create the associated buildings objects"""
        ## read GIS
        shape_file = gpd.read_file(path)
        # shape_file.plot()
        # plt.show()
        ## number of buildings##
        # in the shp file (not necessarily the real number of buildings, a building can be made of several elements)
        number_of_building_shp = len(shape_file['geometry'])

        ## loop to create a building for each foot print in the shp file
        for building_number_shp in range(0,number_of_building_shp):
        # for building_number_shp in range(0, 5):  # few buildings
        # for building_number_shp in range(3,8): # few buildings
            footprint = shape_file['geometry'][building_number_shp]
            if isinstance(footprint, shapely.geometry.polygon.Polygon) : # if the building is made of 1 footprint (isinstance check if the type is correct)
                self.polygon_to_building(footprint, shape_file, building_number_shp,unit)
            elif isinstance(footprint, shapely.geometry.multipolygon.MultiPolygon): # if the building is made of multiple footprints
                self.multipolygon_to_building(footprint, shape_file, building_number_shp, unit)
            else :
                print(("geometry {} in shp file is not a POLYGON").format(building_number_shp))


    def polygon_to_building(self,footprint,shape_file,building_number_shp,unit):
        """ Convert a Polygon to a Building object """
        point_list_footprints = polygon_to_points(footprint)  # convert the POLYGON into a list of points
        id_building = self.num_of_buildings  # id of the building for the urban canopy object
        # create a building object (automatically added to the urban_canopy)
        Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)

    def multipolygon_to_building(self,footprint,shape_file,building_number_shp,unit):
        """ Convert a MultiPolygon to a Building object """
        for polygon in footprint.geoms:
            point_list_footprints = polygon_to_points(polygon)
            id_building = self.num_of_buildings  # id of the building for the urban canopy object
            # create a building object (automatically added to the urban_canopy)
            Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)





    # # # # # # # # # # # # # # # #          Create Building and Geometry      # # # # # # # # # # # # # # # # # # # # #

    def add_building(self,id,building_object):
        """ add a building object to the urban canopy """
        self.building_dict[id]=building_object
        self.num_of_buildings += 1



    def select_target_building(self,id_list):
        """
        Set the target buildings that will need to be simulate
        Args:
            * id_list : list of the ids (from the shapefile ! not the local ids here, the shp_id property of buildings)
                        of the building to simulate
        """
        for id in self.building_dict:
            if self.building_dict[id].shp_id in id_list:
                self.building_dict[id].is_target = True


    def add_context_simulated_building(self,building_id):
        """
        Add a simulated context building to the Urban Canopy
        """
        self.building_to_simulate.append(self.building_dict[building_id])
        self.building_dict[building_id].is_simulated = True


    # # # # # # # # # # # # # # # #          Create Building and Geometry      # # # # # # # # # # # # # # # # # # # # #

    def create_building_LB_geometry_footprint(self):
        """
        goes from list of points to Ladybug footprints for all the building in the GIS, not only th simulated one
        """
        for i,id in enumerate(self.building_dict):
            self.building_dict[id].footprint_to_LB_face()

    def create_building_HB_room_envelop(self):
        """ goes from list of points to Ladybug geometry objects """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].LB_face_to_HB_room_envelop()

    def create_DF_building(self):
        """ goes from list of points to Ladybug geometry objects """
        for id in self.building_to_simulate:
            self.building_dict[id].LB_face_to_DF_building()

    def convert_DF_building_to_HB_models(self):
        """ goes from list of points to Ladybug geometry objects """
        for id in self.building_to_simulate:
            self.building_dict[id].DF_building_to_HB_model()



    # def create_envelop_json(self,path) :
    #
    #     HB_room_list=[]
    #     for i in self.building_to_simulate:
    #         HB_room_list.append(self.building_dict[i].HB_room_envelop)
    #     hb_model=Model.from_objects("UC",HB_room_list)
    #     print(hb_model.rooms)
    #     hb_model.to_hbjson("uc_envelop",path)

    # # # # # # # # # # # # # # # #         Extract building typology        # # # # # # # # # # # # # # # # # # # # #

    def load_characteristics_typo(self):
        """
        After assigning typologies to buildings, load the constructions, constructions sets, loads etc...
        of the typology of the building
        """
        None

    def assign_conditioned_zone(self):
        """
        Assign an ideal hvac system for every apartment types rooms, turning them into conditioned zones for all buildings.
        """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_assign_conditioned_zone()

    # # # # # # # # # # # # # # # #        Extract Simulation parameters       # # # # # # # # # # # # # # # # # # # # #

    def simulation_parameters_for_idf(self,idf):
        """
        Extract simulation parameter from an idf file
        """
        idf_string = None # idf in a single string to crete Simulationparameter object with HB_energy
        with open(idf,"r") as idf_file :
            idf_string = idf_file.read() # convert idf file in string
        simulation_parameter = parameter.SimulationParameter.from_idf(idf_string) # create the Simulationparameter object
        return(simulation_parameter)

    def simulation_parameters_from_json(self,simulation_parameter_folder) :
        """
        
        """
        output = None
        run_period = None
        simulation_control = None
        shadow_calculation = None
        sizing_parameter = None
        # default
        timestep = 6 # By default here, but might be changed
        north_angle = 0
        terrain_type = 'Urban' # By default here, but might be changed
        # Extract the parameters from json files
        with open(os.path.join(simulation_parameter_folder,"SimulationOutput.json"), 'r') as f:
            json_dict = json.load(f)
            output = SimulationOutput.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder,"RunPeriod.json"), 'r') as f:
            json_dict = json.load(f)
            run_period = RunPeriod.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder , "SimulationControl.json"), 'r') as f:
            json_dict = json.load(f)
            simulation_control = SimulationControl.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder , "ShadowCalculation.json"), 'r') as f:
            json_dict = json.load(f)
            shadow_calculation = ShadowCalculation.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder , "SizingParameter.json"), 'r') as f:
            json_dict = json.load(f)
            sizing_parameter = SizingParameter.from_dict(json_dict)

        self.simulation_parameters= SimulationParameter(output=output, run_period=run_period, timestep=timestep,
                 simulation_control=simulation_control, shadow_calculation=shadow_calculation, sizing_parameter=sizing_parameter,
                 north_angle=north_angle, terrain_type=terrain_type)


    # # # # # # # # # # # # # #       Force characteristics on building      # # # # # # # # # # # # # # # # # # # # #

    def apply_buildings_characteristics(self):
        """
        After assigning typologies to buildings, load the constructions, constructions sets, loads etc...
        of the typology of the building
        """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_apply_buildings_characteristics()

    # # # # # # # # # # # # # # # #       force floor typology   # # # # # # # # # # # # # # # # # # # # #

    def force_typology(self,typo_identifier):
        """ apply the layout of a given typology without adaption to the building specificities, just for the tests """
        for id in self.building_to_simulate:
            if self.building_dict[id].typology==None :
                self.building_dict[id].typology=self.typology_dict[typo_identifier]

    # # # # # # # # # # # # # # # #       force floor layout on buildings    # # # # # # # # # # # # # # # # # # # # #

    def Apply_floor_layout(self):
        """ apply the layout of a given typology without adaption to the building specificities, just for the tests """
        for id in self.building_to_simulate:
            self.building_dict[id].extract_face_typo()

    def LB_layout_to_DF_building(self):
        """ goes from list of points to Ladybug geometry objects """
        for id in self.building_to_simulate:
            self.building_dict[id].LB_layout_to_DF_building()

    def LB_layout_to_DF_story(self):
        """ goes from layout in Ladybug 3Dface format to DF stories for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].LB_layout_to_DF_story()

    def DF_story_to_DF_building(self):
        """ goes from DF stories to DF Buildings for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].DF_story_to_DF_building()


    def create_DF_building_according_to_typology(self,):
        """ create DF buildings from a forced typology layout for all the buildings"""
        self.Apply_floor_layout()
        self.LB_layout_to_DF_story()
        self.DF_story_to_DF_building()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #               Honeybee modeling             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    # # # # # # # # # # # # # # # #       Honeybee solve adjacencies           # # # # # # # # # # # # # # # # # # # # #
    def HB_solve_adjacencies(self):
        """ Solve the adjacencies for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_solve_adjacencies()
            # self.building_dict[id].HB_model.to_hbjson("test", "D://Elie//PhD//Programming//")

    # # # # # # # # # # # # # # # #        Honeybee windows generation         # # # # # # # # # # # # # # # # # # # # #
    def HB_building_window_generation_floor_area_ratio(self):
        """ Generate windows on buildings according to a floor area % ratio on façade per direction  """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_building_window_generation_floor_area_ratio()

    def add_thermal_mass_int_wall(self):
        """
        Add thermal mass to buildings
        """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_add_thermalmass_int_wall()





    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #          Context filter algorithm           # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def filter_context(self,VF_criteria):
        """
        1- identify the buildings that are close to the target buildings and that should be simulated
        2- identify the buildings that are close to the simulated context buildings and that should be part of their context
        3- Select the context surfaces
        """

        target_buildings_face_list = []
        all_building_face_list = []
        context_simulated_building_face_list = []

        ## prepare target building surfaces
        for id in self.target_buildings:
            target_buildings_face_list.append([id,self.building_dict[id].prepare_face_for_context(reverse=False)])
        ## prepare all building surfaces
        for not_used,(id,building_obj) in enumerate(self.building_dict.items()):
            all_building_face_list.append([id,building_obj.prepare_face_for_context(reverse=True)])

        for target_building_face_list in target_buildings_face_list :
            context_building_face_list_kept = [] # list with the id of the context buildings for this building
            ## first check, just identify the buildings if one surface fits the requirement
            for test_context_building_face_list  in all_building_face_list :
                if target_building_face_list[0]!=test_context_building_face_list[0]: # check if the buildings are not the same
                    if is_context_building(target_building_face_list[1],test_context_building_face_list[1],VF_criteria)==True:
                        context_building_face_list_kept.append(test_context_building_face_list)
                        self.building_dict[target_building_face_list[0]].context_buildings_id.append(test_context_building_face_list[0])
                        # self.building_dict[test_context_building_face_list[0]].is_simulated=True
                    else:
                        None
                else:
                    None
            for test_context_building_face_list in context_building_face_list_kept :
                self.filter_context_surfaces(target_building_face_list[1],test_context_building_face_list[1],
                                        target_id=target_building_face_list[0],
                                        VF_criteria=VF_criteria)


            ## second check, check every surfaces in the selected context buildings

        ## prepare the simulated buildings that are not targets

    def filter_context_surfaces(self, target_building_face_list, test_context_building_face_list, target_id,
                                VF_criteria):
        """
        Check if the  test_context_building is part of the context
        """
        ## first pass
        for test_face in test_context_building_face_list:
            for target_face in target_building_face_list:
                if max_VF(target_face, test_face) >= VF_criteria:
                    self.building_dict[target_id].context_buildings_HB_faces.append(test_face[0])
                    break
        ## second pass

        # to be continued...

    def add_context_surfaces_to_HB_model(self):
        """
        """
        for id in self.building_to_simulate:
            self.building_dict[id].add_context_surfaces_to_HB_model()




    # # # # # # # # # # # # # # # #    Detect Typology and assign the layout   # # # # # # # # # # # # # # # # # # # # #

    def detect_typology(self):
        """ detect the typology of building, their orientation and width/length ratio according to their shape"""

    # # Use recognition algorithm to get the shape type # #


    # # Guess the final typology with the shape type and the other properties of the buildings # #

        None


    def Apply_layout(self):
        """ Apply the layout of the data base to the buildings """

    # # add all the faces to the building foot print, distinguishing cores and apartments # #



    # # convert the surfaces to Ladybug faces # #

        None




    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                Generate IDF                 # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




    def add_design_days_to_simulation_parameters(self,path_simulation_parameter,path_file_epw,terrain_type_in="City",timestep_in=6):
        # sim_parameter_obj = None
        with open(path_simulation_parameter, 'r') as f:
            json_dic = json.load(f)
            sim_parameter_obj = SimulationParameter.from_dict(json_dic)
        epw_obj = EPW(path_file_epw)
        des_days = [epw_obj.approximate_design_day('WinterDesignDay'),
                    epw_obj.approximate_design_day('SummerDesignDay')]
        sim_parameter_obj.sizing_parameter.design_days = des_days

        sim_parameter_obj.terrain_type = terrain_type_in
        sim_parameter_obj.timestep = timestep_in
        # replace the simulatio_paramter.json by the updated one
        sim_parameter_dic = SimulationParameter.to_dict(sim_parameter_obj)
        with open(path_simulation_parameter, "w") as json_file:
            json.dump(sim_parameter_dic, json_file)

    def generate_HB_model(self,path_folder_building_simulation):   # can be done in parallel
        """

        """
        ## Generate models ##
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            ## Convert HB model to hbjson file ##
            for room in self.building_dict[building_id].HB_model.rooms:
                room.remove_colinear_vertices_envelope(0.1)
            self.building_dict[building_id].HB_model.to_hbjson("in", path_dir_building + "//model_json")
            # run.measure_compatible_model_json(path_dir_building + "//model_json//in.hbjson")
            ## Prepare simulation for OpenStudio ##





            # osw=run.to_openstudio_osw(osw_directory=path_dir_building + "//osw",
            #                       model_json_path=model_json_path,
            #                       sim_par_json_path=path_simulation_parameter,
            #                       epw_file=path_epw)
            # ## Run simulation in OpenStudio to generate IDF ##
            # (osm,idf)=run.run_osw(osw,measures_only=True,silent=True)
            # # print(idf)
            # # ## Move the idf to the idf folder
            # # shutil.copy(idf, path_dir_building + "//idf//in.idf")
            # # shutil.copy(osm, path_dir_building + "//idf//in.osm")
            # # zob = run.run_idf(path_dir_building + "//idf//in.idf", epw_file_path=path_epw)
            # #
            # # path_epw = "D://Elie//PhD//Programming//EPW//ISR_Tel_Aviv_1999.epw"
            #
            # zob = run.run_idf(idf, epw_file_path=path_epw)


    def simulate_idf(self,path_folder_building_simulation,path_simulation_parameter,path_file_epw,path_energyplus_exe):
        """
        """
        ## Create simulation folders ##
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            ## Convert HB model to hbjson file ##
            model_json_path = os.path.join(path_dir_building,"model_json","in.hbjson")
            ## Prepare simulation for OpenStudio ##
            osw=run.to_openstudio_osw(osw_directory=path_dir_building + "//osw",
                                  model_json_path=model_json_path,
                                  sim_par_json_path=path_simulation_parameter,
                                  epw_file=path_file_epw)
            ## Run simulation in OpenStudio to generate IDF ##
            (osm,idf)=run.run_osw(osw,measures_only=True,silent=False)
            # zob = run.run_idf(idf, epw_file_path=path_file_epw,silent=False)
            zob= run_idf_windows_modified(idf_file_path=idf, epw_file_path=path_file_epw, expand_objects=True,silent=False,path_energyplus_exe=path_energyplus_exe)




    def create_folder_simulation(self,path_folder_simulation,path_folder_context_hbjson,path_folder_building_simulation):
        """
        Create/clean the simulation folder
        """
        ## Clean folder Simulation ##
        clean_folder(path_folder_simulation)
        ## Clean folder Simulation/Context ##
        clean_folder(path_folder_context_hbjson)
        ## Clean folder Simulation/Buildings ##
        clean_folder(path_folder_building_simulation)
        ## Create simulation folders for each building ##
        for building_id in self.building_to_simulate:
            path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
            if not os.path.exists(path_dir_building):
                os.mkdir(path_dir_building)
                os.mkdir(os.path.join(path_dir_building, "osw"))
                os.mkdir(os.path.join(path_dir_building, "osm"))
                os.mkdir(os.path.join(path_dir_building, "idf"))
                os.mkdir(os.path.join(path_dir_building, "model_json"))
                os.mkdir(os.path.join(path_dir_building, "context_surfaces_json"))
                os.mkdir(os.path.join(path_dir_building, "GIS_context_json"))




    # def create_folder_context_hbjson(self,path_folder_context_hbjson):
    #     """
    #     Create/clean the folder for the context json (everything beside the target/simulated buildings
    #     """
    #     ## Clean folders ##
    #     if os.path.exists(path_folder_context_hbjson) :
    #         shutil.rmtree(path_folder_context_hbjson)
    #     os.mkdir(path_folder_context_hbjson)
    #
    #
    # def create_folder_building_simulation(self,path_folder_building_simulation):
    #     """
    #     Create  the folder and sub folder each simulated building
    #     """
    #     ## Clean folders ##
    #     if os.path.exists(path_folder_building_simulation) :
    #         shutil.rmtree(path_folder_building_simulation)
    #     os.mkdir(path_folder_building_simulation)
    #     ## Create simulation folders ##
    #     for building_id in self.building_to_simulate:
    #         path_dir_building = os.path.join(path_folder_building_simulation, self.building_dict[building_id].name)
    #         if not os.path.exists(path_dir_building):
    #             os.mkdir(path_dir_building)
    #             os.mkdir(os.path.join(path_dir_building, "osw"))
    #             os.mkdir(os.path.join(path_dir_building, "osm"))
    #             os.mkdir(os.path.join(path_dir_building, "idf"))
    #             os.mkdir(os.path.join(path_dir_building, "model_json"))
    #             os.mkdir(os.path.join(path_dir_building, "context_surfaces_json"))
    #             os.mkdir(os.path.join(path_dir_building, "GIS_context_json"))


    def load_simulation_parameter(self,path_folder_simulation_parameter,path_simulation_parameter):
        """
        convert properly the simulation parameters for HB
        """
        self.simulation_parameters_from_json(path_folder_simulation_parameter)
        HB_simulation_parameter_dic = SimulationParameter.to_dict(self.simulation_parameters)
        with open(path_simulation_parameter, "w") as json_file:
            json.dump(HB_simulation_parameter_dic, json_file)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                Context                      # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def context_to_hbjson(self, path_folder_context_hbjson):
        """
        Generate a hbjson file to plot the context in Rhinoceros
        The hbjson is a HB model.
        Each room of the model represent one building.
        Rooms are generated with the building envelop = LB polyface3D
        """

        room_list = [] # list of the rooms

        for id in range(self.num_of_buildings) :
            # plot only the buildings that are not simulated/modeled = the rest of the GIS for now
            if id not in self.building_to_simulate:
                room_list.append(self.building_dict[id].HB_room_envelop)

        model = Model(identifier="context",rooms=room_list)

        # generate model
        model.to_hbjson(name="context",folder=path_folder_context_hbjson)

    def context_surfaces_to_hbjson(self, path_folder_simulation):
        """
        Write the context surfaces of each building in a hbjson file in the building directory
        """
        for building_id in self.building_to_simulate:
            path_dir_building_context = os.path.join(path_folder_simulation, self.building_dict[building_id].name,"context_surfaces_json")
            self.building_dict[building_id].context_surfaces_to_hbjson(path_dir_building_context)


    def GIS_context_individual_to_hbjson(self, path_folder_simulation):
        """
        Write the context surfaces of each building in a hbjson file in the building directory
        """
        for building_id in self.building_to_simulate:
            path_dir_building_context = os.path.join(path_folder_simulation, self.building_dict[building_id].name,"GIS_context_json")
            self.building_dict[building_id].GIS_context_to_hbjson(path_dir_building_context)





########################## additional functions for GIS/shp extraction##############
def polygon_to_points(polygon):
    """      """
    ## ADD COMMENTS


    exterior_footprint = polygon.exterior.__geo_interface__['coordinates']
    # eventually check that the footprint is well oriented
    interior_holes=None
    try:
        polygon.interiors
    except:
        None
    else:
        interior_holes = []
        for hole in polygon.interiors:
            if hole.__geo_interface__['coordinates']!=None :
                interior_holes.append(hole.__geo_interface__['coordinates'])

    return([exterior_footprint,interior_holes])


def is_context_building(target_building_face_list, test_context_building_face_list,VF_criteria):
    """
    Check if the  test_context_building is part of the context
    """
    for target_face in target_building_face_list :
        for test_face in test_context_building_face_list:
            if max_VF(target_face,test_face)>=VF_criteria:
                return(True)
    return(False)



def max_VF(target_face,test_face):
    """
    Maximal view factor between the 2 surface, in the optimal configuration described in the context paper
    the faces are lists with following format :
    [LB_face_obj,area, centroid]
    """
    ## distance between the centroids
    d   = LB_distance_pt_3D(target_face[2],test_face[2])
    if d==0:
        d=0.01
    ## width of the optimal squares
    W_1 = sqrt(target_face[1])
    W_2 = sqrt(test_face[1])
    ## intermediary variable for the computation
    w_1 = W_1/d
    w_2 = W_2/d
    x   = w_2 - w_1
    y   = w_2 + w_1
    p   = (w_1**2+w_2**2+2)**2
    q   = (x**2+2)*(y**2+2)
    u   = sqrt(x**2+4)
    v   = sqrt(y**2+4)
    s   = u * (x * atan(x/u) - y * atan(y/u))
    t   = v * (x * atan(x/v) - y * atan(y/v))
    return( 1/(pi*w_1**2) * (log(p/q) + s - t) )

def LB_distance_pt_3D(pt_1,pt_2):
    """
    Distance between 2 LB geometry Point3D
    """
    return(sqrt((pt_1.x-pt_2.x)**2+(pt_1.y-pt_2.y)**2+(pt_1.z-pt_2.z)**2))


def clean_folder(path):
    """
    Clean a folder by deleting it and recreating it
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

# # # # # # # # # unused # # # # # # # # #

    # def Convert_to_HB_model(self):
    #     """ goes from list of points to Ladybug geometry objects """
    #     for id in range(self.num_of_buildings):
    #         self.building_dict[id].LB_face_to_HB_room_envelop()

def run_idf_windows_modified(idf_file_path, epw_file_path=None, expand_objects=True,
                     silent=False,path_energyplus_exe=None):
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
        cmds = [folders.energyplus_exe, '-i ', folders.energyplus_idd_path,'-r ',idf_file_path ]
        if epw_file_path is not None:
            cmds.append('-w')
            cmds.append(os.path.abspath(epw_file_path))
        if expand_objects:
            cmds.append('-x')
        process = subprocess.Popen(
            cmds, cwd=directory, stdout=subprocess.PIPE, shell=True)
        process.communicate()  # prevents the script from running before command is done

    return directory