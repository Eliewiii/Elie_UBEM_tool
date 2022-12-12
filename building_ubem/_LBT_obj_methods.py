"""
Additional methods for the Building class.
Deals with LBT obj attributes of the Building objects
"""
import logging

from ladybug_geometry.geometry3d import Point3D, Face3D, Vector3D
from honeybee.room import Room
from honeybee import boundarycondition
from honeybee_energy.internalmass import InternalMass
from honeybee_energy.lib.constructions import opaque_construction_by_identifier

import dragonfly


class Mixin:

    def footprint_to_LB_face(self, tolerance_collinear_vertices=0.01):
        """ Convert the footprints into Ladybug Face3D geometry object, the elevation will be 0,  """

        footprint_point_list = []  # list containing the Ladybug Point3D of the external contour of the footprint
        ## External footprint
        for point in self.footprint:
            footprint_point_list.append(Point3D(point[0], point[1], 0))
        ## internal holes
        holes_list=None
        if self.holes != [] and self.holes != None:
            holes_list = []  # list of list of points of holes
            for hole in self.holes:
                holes_point_list = []  # list of points for a hole
                for point in hole:
                    holes_point_list.append(Point3D(point[0], point[1], 0))
                holes_list.append(holes_point_list)

        ## Create the Ladybug face for the footprint
        self.LB_face_footprint = Face3D(footprint_point_list, holes=holes_list, enforce_right_hand=True)
        # Remove collinear vertices
        self.LB_face_footprint=self.LB_face_footprint.remove_colinear_vertices(tolerance=tolerance_collinear_vertices)
        # Centroid of the footprint
        self.LB_face_centroid = self.LB_face_footprint.centroid

    def lb_footprint_to_df_building(self, core_area_ratio=0.15, tol=0.005):
        """ generate a Dragonfly building out of the footprint, generating a core in the center """

        footprint_area = self.LB_face_footprint.area
        # target area of the core and the acceptable range
        target_core_area = footprint_area * core_area_ratio
        max_core_area = target_core_area * (1 + tol)
        min_core_area = target_core_area * (1 - tol)
        # list with the floor height between each floor
        floor_to_floor_heights = [self.floor_height for i in range(self.num_floor)]
        # initialization of the dichotomy
        perimeter_offset_boundary_up = 20
        perimeter_offset_boundary_down = 1
        perimeter_offset = perimeter_offset_boundary_down
        first_try_df_building = dragonfly.building.Building.from_footprint(identifier="Building_" + str(self.id),
                                                                           footprint=[self.LB_face_footprint],
                                                                           floor_to_floor_heights=[3.],
                                                                           perimeter_offset=perimeter_offset)
        # number of rooms including the core when subdivided by the Dragonfly algorithm
        nb_rooms_per_stories = len(first_try_df_building.unique_stories[0].room_2ds)
        # core_area = first_try_df_building.unique_stories[0].room_2ds[-1].floor_area()

        max_iteration = 30
        converged = False
        for i in range(max_iteration):
            # print("it {}".format(i),footprint_area,target_core_area)
            perimeter_offset = (perimeter_offset_boundary_up + perimeter_offset_boundary_down) / 2.

            df_building = dragonfly.building.Building.from_footprint(identifier="Building_" + str(self.id),
                                                                     footprint=[self.LB_face_footprint],
                                                                     floor_to_floor_heights=[3.],
                                                                     perimeter_offset=perimeter_offset)
            # print("it {}".format(i))
            if len(df_building.unique_stories[0].room_2ds) >= nb_rooms_per_stories:
                nb_cores=len(df_building.unique_stories[0].room_2ds)-nb_rooms_per_stories+1
                core_area = sum([df_building.unique_stories[0].room_2ds[-i-1].floor_area for i in range(nb_cores)])
                if max_core_area < core_area:
                    perimeter_offset_boundary_down = perimeter_offset
                elif min_core_area > core_area:
                    perimeter_offset_boundary_up = perimeter_offset
                else :
                    converged= True
                    break
            else:
                # print("wrong number of room")
                perimeter_offset_boundary_up = perimeter_offset

        if converged:
            self.DF_building = dragonfly.building.Building.from_footprint(identifier="Building_" + str(self.id),
                                                                          footprint=[self.LB_face_footprint],
                                                                          floor_to_floor_heights=floor_to_floor_heights,
                                                                          perimeter_offset=perimeter_offset)
            # Rename the room to know what are the apartments and cores
            for id_story in range (len(self.DF_building.unique_stories)):
                for room_id in range(nb_rooms_per_stories-1):
                    self.DF_building.unique_stories[0].room_2ds[room_id].identifier= "apartment_" + str(room_id)
                # last room is the core
                for i in range(len(self.DF_building.unique_stories[0].room_2ds)-nb_rooms_per_stories + 1):
                    self.DF_building.unique_stories[0].room_2ds[-i-1].identifier = "core_" + str(i)



        else:
            logging.warning(f" building_{self.id} : the automatic subdivision in rooms and cores failed")
            self.DF_building = dragonfly.building.Building.from_footprint(identifier="Building_" + str(self.id),
                                                                          footprint=[self.LB_face_footprint],
                                                                          floor_to_floor_heights=floor_to_floor_heights)
            # rename only the main room
            for id_story in range (len(self.DF_building.unique_stories)):
                    self.DF_building.unique_stories[0].room_2ds[0].identifier= "apartment_" + str(0)

    def extract_face_typo(self):
        """
        Extract the typology faces from txt file

        input:
        * path_file :

        outputs:
        * apartments :
        * core :
        """
        path_file = self.typology.path_file_layout
        ## Apartments
        self.LB_apartments = surface_txt_to_LB_surfaces(path_file + "//apartment.txt")
        self.LB_cores = surface_txt_to_LB_surfaces(path_file + "//core.txt")
        self.LB_balconies = surface_txt_to_LB_surfaces(path_file + "//balcony.txt")
        ## Move the elements to be a the position of building_zon
        [x, y, z] = [self.LB_face_centroid.x, self.LB_face_centroid.y, self.LB_face_centroid.z]
        mov_vector = Vector3D(x, y, z)
        if self.LB_apartments:
            for i, apartment in enumerate(self.LB_apartments):
                self.LB_apartments[i] = apartment.move(mov_vector)
        if self.LB_cores:
            for i, core in enumerate(self.LB_cores):
                self.LB_cores[i] = core.move(mov_vector)
        if self.LB_balconies:
            for i, balcony in enumerate(self.LB_balconies):
                self.LB_balconies[i] = balcony.move(mov_vector)

    def LB_layout_to_DF_story(self):
        """
        Convert the LB layout to a DF story

        The difference between the first floor and the other floor might have to be made in the future
        """
        DF_room2Dlist = []  # list with all the Room2D objects for the story

        # Create DF Room2D for each apartment (originally a Ladybug 3Dface)
        for i, room in enumerate(self.LB_apartments):
            DF_room2Dlist.append(
                dragonfly.room2d.Room2D("apartment_" + str(i), floor_geometry=room, floor_to_ceiling_height=self.floor_height))
        # Create DF Room2D for each core
        if self.LB_cores:
            for i, room in enumerate(self.LB_cores):
                DF_room2Dlist.append(
                    dragonfly.room2d.Room2D("core_" + str(i), floor_geometry=room, floor_to_ceiling_height=self.floor_height))

        # Create the story
        self.DF_story = dragonfly.story.Story(identifier="floor", room_2ds=DF_room2Dlist, multiplier=self.num_floor)
        # Solve adjacency and boundary conditions for all the Rooms/Faces
        self.DF_story.intersect_room_2d_adjacency()  # prevent some issues with non identified interior walls.
        self.DF_story.solve_room_2d_adjacency()

    def DF_story_to_DF_building(self):
        """
        Convert DF story to DF building_zon.

        Will need to be modified to consider different stories for the same building_zon, especially a first floor.
        """

        self.DF_building = dragonfly.building.Building(identifier="Building_" + str(self.id), unique_stories=[self.DF_story])

    def DF_building_to_HB_model(self):
        """ Create an extruded DF building_zon from LB geometry footprint """

        self.HB_model = self.DF_building.to_honeybee(use_multiplier=False)
        # print(self.id,self.LB_face_centroid)

    def add_hvac_system(self, LBT_hvac_system_obj):
        """ Add the HVAC system to the conditionned zone in the building"""
        for room in self.HB_model.rooms:  # loop on all rooms
            if room.is_conditioned:  # if not a core, add ideal air Hvac system, making it a conditioned zone
                room.properties.energy.hvac = LBT_hvac_system_obj

    def add_infiltration_air_exchange(self, air_exchange_rate: (float, int) = 1.):
        """
        Add air infiltration exchange with a rate in volume per hour
        :param air_exchange_rate: float : air flow exchange rate with the exterior due to infiltration [vol/h]
        """

        for room in self.HB_model.rooms:  # loop on all rooms
            room.properties.energy.abolute_infiltration_ach(air_exchange_rate)

    def HB_solve_adjacencies(self):
        """
        Solve the adjacency ...
        Correct the boundary conditions, here especially for the floor/ceiling and the ground floor and roof.
        In addition to the one from Dragonfly, but
        """

        Room.solve_adjacency(self.HB_model.rooms)
        # correct the adiabatic surfaces on the ground and on roof (need to check why it happens)
        for room in self.HB_model.rooms:  # loop on rooms (could be just do the ground floor and last floor but whatever)
            for face in room.faces:  # loop on the faces
                if isinstance(face.boundary_condition, boundarycondition.Adiabatic):
                    if room.average_floor_height == 0:  # if can be ground => it's ground floor
                        face.boundary_condition = boundarycondition.boundary_conditions.ground
                    else:  # if it's not ground and it's adiabatic it's roof a priori, but need to investigate deeper.
                        face.boundary_condition = boundarycondition.boundary_conditions.outdoors

    def HB_add_thermalmass_int_wall(self):
        """
        Add the internal mass due the non-load-bearing internal walls
        Israeli Standards suggests 1.5m2 of intwall per floor m2 for a 3m height floor
        Can be generalize to 0.5m2*height
        The intwall is only half an int wall here, the surface counts both sides of the walls
        The default value for self.int_wall_ratio is 1.5
        """
        for room in self.HB_model.rooms:
            # add internal mass only in conditioned zones
            if room.properties.energy.is_conditioned:
                int_mass_area = room.floor_area * self.int_mass_ratio
                # find the construction
                construction_internal_wall = opaque_construction_by_identifier(
                    self.typology.construction_int_wall_int_mass)
                # create the internal mass
                mass = InternalMass(identifier="int_mass" + room.identifier, construction=construction_internal_wall,
                                    area=int_mass_area)
                # assign the internal mass
                room.properties.energy.add_internal_mass(mass)

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

if __name__ == "__main__":
    None
