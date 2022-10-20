"""
Additional methods for the Building class.
Deals with the context selection of the context.
"""
import copy

from math import sqrt, atan, pi, log

from ladybug_geometry.geometry3d import Vector3D
from copy import deepcopy


class Mixin:

    def prepare_face_for_context(self, reverse=False):
        """
        Returns a a list that will be used for the context selection.
        return a list as followed:
        [  [face_obj, area, centroid], [], .... ]
        order from the smallest area to the biggest
        if reverse==True, it is sorted reverse

        """
        face_list = []  # list to return
        z_vertices = [Vector3D(0, 0, 1), Vector3D(0, 0, -1)]  # vertical vertices
        for face in self.HB_room_envelop.faces:
            if face.normal not in z_vertices:  # do not keep the roof and ground
                face_list.append([face, face.geometry.area, face.geometry.centroid])

        face_list.sort(key=lambda x: x[1], reverse=reverse)  # sort the list according to the 2nd element = the area
        return face_list

    def prepare_face_for_context_new(self, is_target=False):
        """
        Returns a a list that will be used for the context selection.
        return a list as followed:
        [  [face_obj, area, centroid], [], .... ]
        order from the smallest area to the biggest
        if reverse==True, it is sorted reverse

        """
        face_list = []  # list to return
        z_vertices = [Vector3D(0, 0, 1), Vector3D(0, 0, -1)]  # vertical vertices
        for face in self.HB_room_envelop.faces:
            if face.normal not in z_vertices:  # do not keep the roof and ground
                face_list.append(
                    {"hb_face_obj": face, "area": face.geometry.area, "centroid_point3d": face.geometry.centroid,
                     "lower_corner_point3d": {"left": face.geometry.lower_left_corner,
                                              "right": face.geometry.lower_right_corner}, "height": self.height})
        if is_target:
            face_list.sort(key=lambda x: x[1], reverse=False)  # sort the list according to the 2nd element = the area
            # from smaller to bigger for context building
            self.external_face_list_target = face_list
        else:
            face_list.sort(key=lambda x: x[1], reverse=True)  # sort the list according to the 2nd element = the area
            # from bigger to smaller for context building
            self.external_face_list_context = face_list

    def shading_context_surfaces_selection(self, pre_processed_surface_list, mvfc=0.01, first_pass=True,
                                           second_pass=True):
        """
        Select the surfaces from all the context that shade noticeably on the building.
        The filtering has 2 passes:
        - the minimum view factor criterion
        - obstruction detection with LCA
        It can go through only one or none of the passes if needed

        Args:
            pre_processed_surface_list [list]: list containing all the surfaces to test. Each element, representing a
                surface, is a dictionary with the following properties {"hb_face_obj", "area", "centroid":(Point3D),
                 "lower_corner_point3d":{"left","right"},"height"}
            mvfc [float]: value for the minimum view factor criteria. Check the shading_context_first_pass function
               for the detailed explanation.
            first_pass [boolean]: True if we want to use the first pass, False if not.
            second_pass [boolean]: True if we want to use the second pass, False if not.
        """
        surface_to_test = copy.deepcopy(pre_processed_surface_list)

        ## first pass
        if mvfc_first_pass:
            for surface in context_building_obj.

            context_surface_first_pass = []
        if rt_second_pass:
            if mvfc_first_pass
                for surface in context_surface_first_pass

        ## second pass
        elif mvfc_first_pass:
            self.context_shading_HB_faces =

        return (first_pass_duration, second_pass_diration, shading_surface_list)

    def shading_context_first_pass(self, pre_processed_surface_list, mvfc=0.01, ):
        """
        First pass of the selection of shading the surfaces from the context.
        Use the minimum view factor criterion (mvfc).
        An upper bound of the view factor between each couple of target and context surfaces is computed. If this value
        is higher than the mvfc, the surface is kept as it has potential to shade significantly on the target building.
        If it is lower, the context surface is not keep for the second pass (and thus the energy simulation)
        Args:
            pre_processed_surface_list [list]: list containing all the surfaces to test. Each element, representing a
                surface, is a dictionary with the following properties {"hb_face_obj", "area", "centroid":(Point3D),
                 "lower_corner_point3d":{"left","right"},"height"}
            mvfc [float]: value for the minimum view factor criteria.
        """
        for test_face in pre_processed_surface_list:
            for target_face in self.external_face_list_target:
                if max_VF(centroid_1=target_face["centroid"], area_1=["centroid"], centroid_2=test_face["centroid"],
                          area_2=test_face["area"]) >= mvfc:
                    # self.building_dict[target_id].context_buildings_HB_faces.append(test_face[0])
                    break

    def shading_context_second_pass(self, mvfc=0.01, ):

    def identify_if_context_building(self, context_building_obj):
        """
        # todo

        """
        # for target_building_face_list in target_buildings_face_list:
        #     context_building_face_list_kept = []  # list with the id of the context buildings for this building_zon
        #     ## first check, just identify the buildings if one surface fits the requirement
        #     for test_context_building_face_list in all_building_face_list:
        #         # check if the buildings are not the same
        #         if target_building_face_list[0] != test_context_building_face_list[0]:
        #             if is_context_building(target_building_face_list[1], test_context_building_face_list[1],
        #                                    vf_criteria):
        #                 context_building_face_list_kept.append(test_context_building_face_list)
        #                 self.building_dict[target_building_face_list[0]].context_buildings_id.append(
        #                     test_context_building_face_list[0])
        #                 # self.building_dict[test_context_building_face_list[0]].is_simulated=True
        #             else:
        #                 None
        #         else:
        #             None

    def identify_context_surfaces_with_raytracing_second_pass(self):
        """
        todo
        :return:
        """
        # list_context_surface=deepcopy(context_building_obj.)

    # def prepare_face_for_context_pv(self, reverse=False):
    #     """
    #     Returns a a list that will be used for the context selection.
    #     return a list as followed:
    #     [  [face_obj, area, centroid], [], .... ]
    #     order from the smallest area to the biggest
    #     if reverse==True, it is sorted reverse
    #
    #     """
    #     vertex_list = self.footprint.reverse()  # the footprint look down
    #     nb_points_footprint = len(vertex_list)  # number of vertices in the footprint
    #     surface_dict_list = []
    #
    #     # for
    #     #     surface_dict_list.append({"pv_surface":,"pt_left","pt_right","pt_middle"})
    #     # for
    #     #
    #     #
    #     #
    #     # for
    #     #
    #     #     pt_left,pt_right,pt_middle=
    #     #
    #     # self.dict_surface_context_filtering={"id":self.id,"height":self.height,"surfaces"=surface_dict_list}
    #     #
    #     #
    #     #
    #     #


def distance_lb_geometry_point3d(pt_1, pt_2):
    """ Distance between 2 LB geometry Point3D """
    return sqrt((pt_1.x - pt_2.x) ** 2 + (pt_1.y - pt_2.y) ** 2 + (pt_1.z - pt_2.z) ** 2)


def max_VF(centroid_1, area_1, centroid_2, area_2):
    """
    Maximal view factor between the 2 surface, in the optimal configuration described in the context paper
    the faces are lists with following format :  [LB_face_obj,area, centroid]
    """
    ## distance between the centroids
    d = distance_lb_geometry_point3d(centroid_1, centroid_2)
    if d == 0:
        d = 0.01
    ## width of the optimal squares
    W_1 = sqrt(area_1)
    W_2 = sqrt(area_2)
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
    return 1 / (pi * w_1 ** 2) * (log(p / q) + s - t)
