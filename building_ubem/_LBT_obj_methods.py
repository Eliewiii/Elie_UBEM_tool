"""
Additional methods for the Building class.
Deals with LBT obj attributes of the Building objects
"""
from ladybug_geometry.geometry3d import Point3D, Face3D
from honeybee.room import Room
from honeybee import boundarycondition
from honeybee_energy.internalmass import InternalMass
from honeybee_energy.lib.constructions import opaque_construction_by_identifier


class Mixin:
    def footprint_to_LB_face(self):
        """ Convert the footprints into Ladybug Face3D geometry object, the elevation will be 0,  """

        footprint_point_list = []  # list containing the Ladybug Point3D of the external contour of the footprint
        ## External footprint
        for point in self.footprint:
            footprint_point_list.append(Point3D(point[0], point[1], 0))
        ## internal holes
        if self.holes != [] and self.holes != None:
            holes_list = []  # list of list of points of holes
            for hole in self.holes:
                holes_point_list = []  # list of points for a hole
                for point in hole:
                    holes_point_list.append(Point3D(point[0], point[1], 0))
                holes_list.append(holes_point_list)
        else:
            holes_list = None
        ## Create the Ladybug face for the footprint
        self.LB_face_footprint = Face3D(footprint_point_list, holes=holes_list, enforce_right_hand=True)
        self.LB_face_centroid = self.LB_face_footprint.centroid

    def add_hvac_system(self, LBT_hvac_system_obj):
        """ Add the HVAC system to the conditionned zone in the building"""
        for room in self.HB_model.rooms:  # loop on all rooms
            if room.is_conditioned:  # if not a core, add ideal air Hvac system, making it a conditioned zone
                room.properties.energy.hvac = LBT_hvac_system_obj

    def add_infiltration_air_exchange(self, air_exchange_rate : (float,int) = 1.):
        """
        Add air infiltration exchange with a rate in volume per hour
        :param air_exchange_rate: float : air flow exchange rate with the exterior due to infiltration [vol/h]
        :return:
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
            if room.properties.energy.is_conditioned:
                int_mass_area = room.floor_area * self.int_mass_ratio
                construction_internal_wall = opaque_construction_by_identifier(
                    self.typology.construction_int_wall_int_mass)
                mass = InternalMass(identifier="int_mass" + room.identifier, construction=construction_internal_wall,
                                    area=int_mass_area)
                room.properties.energy.add_internal_mass(mass)

if __name__ == "__main__":
    None
