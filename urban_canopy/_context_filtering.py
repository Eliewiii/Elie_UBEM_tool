"""
Additional methods for the Urban_canopy class.
Deals with the context filtering
"""

from math import sqrt, atan, pi, log

class Mixin:

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

def LB_distance_pt_3D(pt_1, pt_2):
    """
    Distance between 2 LB geometry Point3D
    """
    return (sqrt((pt_1.x - pt_2.x) ** 2 + (pt_1.y - pt_2.y) ** 2 + (pt_1.z - pt_2.z) ** 2))

def max_VF(target_face, test_face):
    """
    Maximal view factor between the 2 surface, in the optimal configuration described in the context paper
    the faces are lists with following format :
    [LB_face_obj,area, centroid]
    """
    ## distance between the centroids
    d = LB_distance_pt_3D(target_face[2], test_face[2])
    if d == 0:
        d = 0.01
    ## width of the optimal squares
    W_1 = sqrt(target_face[1])
    W_2 = sqrt(test_face[1])
    ## intermediary variable for the computation
    w_1 = W_1 / d
    w_2 = W_2 / d
    x = w_2 - w_1
    y = w_2 + w_1
    p = (w_1 ** 2 + w_2 ** 2 + 2) ** 2
    q = (x ** 2 + 2) * (y ** 2 + 2)
    u = sqrt(x ** 2 + 4)
    v = sqrt(y ** 2 + 4)
    s = u * (x * atan(x / u) - y * atan(y / u))
    t = v * (x * atan(x / v) - y * atan(y / v))
    return (1 / (pi * w_1 ** 2) * (log(p / q) + s - t))
