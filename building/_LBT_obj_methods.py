"""
Additional methods for the Building class.
Deals with LBT obj attributes of the Building objects
"""
from ladybug_geometry.geometry3d import Point3D, Face3D


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

if __name__ == "__main__":
    None
