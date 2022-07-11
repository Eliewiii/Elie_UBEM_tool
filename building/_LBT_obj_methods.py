"""
Additional methods for the Building class.

"""


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