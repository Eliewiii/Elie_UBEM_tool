# import urban_canopy_44

from ladybug_geometry.geometry3d import Point3D, Face3D, Polyface3D, Vector3D

import dragonfly as df
import dragonfly.building
from dragonfly.room2d import Room2D
from dragonfly.story import Story

import honeybee
from honeybee.room import Room
from honeybee.face import Face
from honeybee.model import Model
from honeybee import orientation

# import honeybee_energy
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.lib.programtypes import program_type_by_identifier
from honeybee_energy.writer import model_to_idf
from math import sqrt
from honeybee_energy.internalmass import InternalMass
from honeybee_energy.lib.constructions import opaque_construction_by_identifier

from honeybee.model import Model
from honeybee.face import Face
from honeybee.shade import Shade

from building_ubem import _select_context, _attribute_setter, _shp_files, _LBT_obj_methods, \
    _footprin_and_envelop_manipulation, _extract_result_csv, _uwg, _generate_sample, _lca, _ber


class Building(_select_context.Mixin, _attribute_setter.Mixin, _shp_files.Mixin, _LBT_obj_methods.Mixin,
               _footprin_and_envelop_manipulation.Mixin, _extract_result_csv.Mixin, _uwg.Mixin,
               _generate_sample.Mixin, _lca.Mixin, _ber.Mixin):
    """
    description ............


    Properties:
        * urban_canopy_44 [Urban_Canopy object] : urban canopy the building_zon belongs
        * id [int] : id of the building_zon in the urban canopy
        * footprint [list of lists] : list of the points of the footprint ((x,y),(x,y)...)
        * holes [list of lists of lists] : list of the points of the holes [((x,y),(... ] (optional)
        * name [str] : name of the building_zon (optional in the shape file, but it will get a name automatically anyway)
        * group [str] : name of the group the building_zon belongs if it has one (optional)
        * age [int] : year of construction of the building_zon (optional)
        * typo [str] : typology the building_zon belongs to (optional, but will be assigned one anyway)
        * height [float] : height of the building_zon in meter
        * num_floor [int] : number of floors

    Ladybug:
        * LB_face_footprint [int] : number of floors

    Dragonfly:
        * zob
        *

    Honeybee:
        *
        *


    """

    def __init__(self, urban_canopy, id, footprint, holes_footprint=None, name=None, group=None, age=None, typo=None,
                 height=None, num_floor=None, building_id_shp=None, elevation=0., dimension=2):
        """Initialize a building obj"""
        ## add building_zon to urban canopy dictionary
        urban_canopy.add_building(id, self)
        self.urban_canopy = urban_canopy
        # # # # # # # properties # # # # # # #
        self.id = id
        self.footprint = footprint  # will be oriented down as the ground floor "look" down
        self.holes = holes_footprint
        self.name = name
        self.group = group
        self.age = age
        self.typology = typo
        self.num_floor = None
        self.height = None
        # todo : add the elevation, especially to the buuilding envelop
        self.elevation = elevation
        self.dimension = dimension
        self.shp_id = building_id_shp  # id in the shp file, can be useful to see which is the building_zon if a problem is spotted
        self.floor_height = None
        self.int_mass_ratio = None
        self.is_target = False
        self.is_simulated = False
        # # Context filtering
        self.bounding_box_face_list = None
        self.external_face_list_target = None
        self.external_face_list_context = None
        self.context_buildings_id_list = []
        self.context_shading_HB_faces = []
        self.context_hb_kept_first_pass = []
        self.all_context_hb_faces = []
        self.all_context_oriented_bb = []
        self.context_buildings_HB_faces = [] # todo : delete it later, useless

        # # Ladybug #
        self.LB_face_footprint = None  # EVENTUALLY ANOTHER VERSION FOR THE FIRST FLOOR IF DIFFERENT
        self.LB_face_centroid = None
        self.LB_apartments = None
        self.LB_cores = None
        self.LB_balconies = None
        self.LB_extruded_building = None
        # # Honeybee # #
        self.HB_room_envelop = None
        self.hb_oriented_bounding_box = None
        self.HB_model = None
        self.HB_model_dict =None
        # # DragonFly # #
        self.DF_story = None
        self.DF_building = None
        # # View factor # #

        # # additional characteristics
        self.cores_per_floor = None  # number of cores per floor
        self.use = None  # use of the building_zon, given by the GIS por the typology: ["residential", "residential with 1st floor commercial", "office"]
        # # EnergyPlus
        self.idf_path = None
        # # Result extraction
        self.path_csv = None
        self.apartment_dict = {}
        self.apartment_json = {}
        self.apartment_area = 0.
        self.energy_consumption = {"total_w_cop": 0., "total_BER_light": 0., "total_BER_no_light": 0., "total_h_cop": 0.,
                                   "total_c_cop": 0., "total_BER_compared_to_ref": 0, "total_c_cop_compared_to_ref": 0,
                                   "total_h_cop_compared_to_ref": 0}
        self.cop_h = None
        self.cop_c = None
        self.climate_zone = "A"
        self.rating = None
        self.grade_value = 0
        # # df building for UWG   # to extract either form the typology or the construction sets
        self.df_building_uwg = None
        self.df_model_uwg = None
        self.uwg_program = "MidriseApartment"
        self.vintage = "New"
        self.fract_heat_to_canyon = 0.5
        self.shgc = 0.7
        self.wall_albedo = 0.2  #
        self.roof_albedo = 0.7
        self.roof_veg_fraction = 0
        # # LCA
        self.is_reference = None
        self.carbon_footprint = {"mini": 0, "maxi": 0, "standard": 0}  # total
        self.carbon_footprint_kwh_per_m2_eq_per_year= {"mini": 0, "maxi": 0, "standard": 0}
        self.carbon_footprint_kwh_per_m2_eq_compared_to_ref = {"mini": 0, "maxi": 0}
        self.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref = {"mini": 0, "maxi": 0}

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                   Class methods             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @classmethod
    def from_shp_2D(cls, id, point_list_footprints, urban_canopy, shape_file, building_id_shp, unit):
        """  create a building_zon object from geometry in a shapefile """

        ## create the building_zon object from POLYGON fron shp file
        building_obj = cls(urban_canopy, id, footprint=point_list_footprints[0],
                           holes_footprint=point_list_footprints[1], building_id_shp=building_id_shp, dimension=2)
        ## convert footprint and holes to lists
        building_obj.point_tuples_to_list()
        ## convert to the correct unit (meter instead of degrees if necessary)
        building_obj.scale_unit(unit)
        ## Delete the points that are too close to each other in the footprint and holes
        building_obj.check_point_proximity()
        ## affect the properties from  the shp file
        building_obj.affect_properties_shp(shape_file, building_id_shp)
        ## check if the properties given are sufficient to run building_zon simulation
        building_obj.check_property()



    # # # # # # # # # # # # # # #                  force rotation                 # # # # # # # # # # # # # # # # # # # # #

    def HB_model_force_rotation(self, angle):
        """
        Rotate the model around its centroid
        """
        z_vect = Vector3D(0, 0, 1)
        self.HB_model.rotate(axis=z_vect, angle=angle, origin=self.LB_face_centroid)

    # # # # # # # # # # # # # # # #                  Internal mass                # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # # # # # # # #                Create Windows              # # # # # # # # # # # # # # # # # # # # #
    def HB_building_window_generation_floor_area_ratio(self):
        """
        Generate windows on a building_zon according to floor area % per direction
        """
        ratio_per_direction = [self.typology.window_floor_area_ratio_per_direction['north'],
                               self.typology.window_floor_area_ratio_per_direction['east'],
                               self.typology.window_floor_area_ratio_per_direction['south'],
                               self.typology.window_floor_area_ratio_per_direction['west']]

        min_length_wall_for_window = 2.  # minimum length of external wall to put a window on, should be extracted from the typology though

        (rooms_per_floor, floor_elevation) = Room.group_by_floor_height(self.HB_model.rooms)  # group rooms per floors

        # print(self.id,self.height,self.num_floor,self.floor_height,floor_elevation)
        floor_elevation.append(self.height)  # add the height of the building_zon to the list to make the floor height
        # calculation below

        orientation_angles = orientation.angles_from_num_orient()  # orientation subdivisions for the orientation identification

        floor_heights = [floor_elevation[i + 1] - floor_elevation[i] for i in
                         range(len(floor_elevation) - 1)]  # floor height of all the floors

        for i in range(len(rooms_per_floor)):  # do the generation for each floor individually
            self.HB_floor_window_generation_floor_area_ratio(rooms_per_floor[i], floor_heights[i], ratio_per_direction,
                                                             min_length_wall_for_window, orientation_angles)

    def HB_floor_window_generation_floor_area_ratio(self, rooms, floor_height, ratio_per_direction,
                                                    min_length_wall_for_window, orientation_angles):
        """
        Generate windows on a floor according to floor area % per direction.
        Called by the function for the whole building_zon.
        """
        floor_area = sum([room.floor_area for room in rooms])  # copute the floor area
        # list with the faces for all directions
        north_faces = []
        east_faces = []
        south_faces = []
        west_faces = []

        for room in rooms:
            # use only conditioned rooms
            if room.properties.energy.is_conditioned == True:
                for face in room.faces:
                    # outdoor faces only
                    if isinstance(face.boundary_condition, honeybee.boundarycondition.Outdoors):
                        # faces with sufficient length according to the min_length_wall_for_window criteria
                        if face.area / floor_height > min_length_wall_for_window:
                            face_orientation = orientation.face_orient_index(face, orientation_angles)
                            # add to the proper orientation list
                            if face_orientation == 0:  # North
                                north_faces.append(face)
                            elif face_orientation == 1:  # East
                                east_faces.append(face)
                            elif face_orientation == 2:  # South
                                south_faces.append(face)
                            elif face_orientation == 3:  # West
                                west_faces.append(face)
        # North
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(north_faces, floor_area,
                                                                         ratio_per_direction[0])
        # East
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(east_faces, floor_area, ratio_per_direction[1])
        # South
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(south_faces, floor_area,
                                                                         ratio_per_direction[2])
        # West
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(west_faces, floor_area, ratio_per_direction[3])

    def HB_floor_window_generation_floor_area_ratio_per_orientation(self, face_list, floor_area, floor_ratio):
        """
        Generate windows on one direction for a floor according to floor area % per direction.
        Called by the function for the whole floor called by the function for the whole building_zon.
        """
        if floor_ratio > 0:
            facade_area = sum([face.area for face in face_list])  # compute façade area
            window_ratio = floor_area * floor_ratio / facade_area  # compute the % window ratio on the façade
            # Tests to ensure correct windows
            if window_ratio < 0.01:
                window_ratio = 0.01
            elif window_ratio > 0.95:
                window_ratio = 0.95
            # Create window for all faces
            for face in face_list:
                face.apertures_by_ratio(window_ratio)

    # # # # # # # # # # # # # # # #                   Blinds                   # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # # # # # # # #                 Construction               # # # # # # # # # # # # # # # # # # # # #
    def HB_assign_conditioned_zone(self):
        """
        Assign an ideal hvac system for every apartment types rooms, turning them into conditioned zones
        """
        for room in self.HB_model.rooms:  # loop on all rooms
            if "core" not in room.identifier:  # if not a core, add ideal air Hvac system, making it a conditioned zone
                room.properties.energy.add_default_ideal_air()

    def HB_apply_buildings_characteristics(self):
        """
        Force construction set and program on rooms depending on if they are conditioned or not
        """
        for room in self.HB_model.rooms:
            zob = construction_set_by_identifier("2004::ClimateZone1::SteelFramed")
            ## assign construction set
            room.properties.energy.construction_set = construction_set_by_identifier(self.typology.constructions_set_id)
            ## assign program
            if room.properties.energy.is_conditioned:
                room.properties.energy.program_type = program_type_by_identifier(
                    self.typology.program_type_apartment_id)  # if conditioned => apartment
            else:
                room.properties.energy.program_type = program_type_by_identifier(self.typology.program_type_core_id)

    def hb_change_construction_set(self, new_constructionset_id):
        """

        """
        for room in self.HB_model.rooms:
            ## assign construction set
            room.properties.energy.construction_set = construction_set_by_identifier(new_constructionset_id)

    def replace_hb_constr_set(self, initial_constr_set_id, new_constr_set_id):
        """

        """
        ## Loop over all the rooms in the hb_model
        for room in self.HB_model.rooms:
            ## check if the room has the
            if room.properties.energy.construction_set.identifier == initial_constr_set_id:
                ## assign construction set
                room.properties.energy.construction_set = construction_set_by_identifier(new_constr_set_id)

    def HB_assign_ideal_hvac_system(self, ideal_hvac_system):
        """ Assign an ideal HVAC_system to the conditioned zones"""
        for room in self.HB_model.rooms:
            if room.properties.energy.is_conditioned:
                room.properties.energy.hvac = ideal_hvac_system

    # # # # # # # # # # # # # # # #                     IDF                    # # # # # # # # # # # # # # # # # # # # #

    def generate_IDF_from_HB_model(self, simulation_parameters_idf_str, path_folder_idf):
        """ create an IDF from the HB model """
        idf_str = '\n\n'.join((simulation_parameters_idf_str, model_to_idf(self.HB_model)))
        self.idf_path = path_folder_idf + "in.idf"
        with open(self.idf_path, "w") as idf_file:
            idf_file.write(idf_str)

    def GIS_context_to_hbjson(self, path_folder_context_hbjson):
        """
        Generate a hbjson file to plot the context in Rhinoceros
        The hbjson is a HB model.
        Each room of the model represent one building_zon.
        Rooms are generated with the building_zon envelop = LB polyface3D
        """

        room_list = []  # list of the rooms

        for id in range(self.urban_canopy.num_of_buildings):
            # plot only the buildings that are not simulated/modeled = the rest of the GIS for now
            if id != self.id:
                room_list.append(self.urban_canopy.building_dict[id].HB_room_envelop)

        model = Model(identifier=("GIS_context_{}").format(self.name), rooms=room_list)
        # generate model
        model.to_hbjson(name="GIS_context", folder=path_folder_context_hbjson)



    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #            Dragonfly modeling for UWG       # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # def DF_buildings_for_not_simulated_buildings :


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #          Additional useful functions        # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def distance(pt_1, pt_2):
    """
    :param pt_1: list for the point 1 
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return (sqrt((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2))


def surface_txt_to_LB_surfaces(path_file):
    """
    description
    input :
             * path_file
    output :
             * LB_surfaces
    """

    LB_surfaces = []  # initialization of the output

    with open(path_file, "r") as txt_file:
        data = txt_file.read()  # read the file
        data = data.split("\n")  # separate

        for surface in data:
            point_list = []
            if len(surface) > 0:
                surface = surface.split(";")
                for point in surface:
                    [x, y] = point[1:-1].split(",")
                    point = [float(x), float(y)]
                    point_list.append(Point3D(point[0], point[1], 0))
                LB_surfaces.append(Face3D(point_list, enforce_right_hand=False))

    if LB_surfaces == []:
        LB_surfaces = None

    return (LB_surfaces)
