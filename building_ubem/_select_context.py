"""
Additional methods for the Building class.
Deals with the context selection of the context.
"""
import copy
import time
import numpy as np

import pyvista as pv

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
                face_list.sort(key=lambda x: x[1],
                               reverse=False)  # sort the list according to the 2nd element = the area
                # from smaller to bigger for context building
                self.external_face_list_target = face_list
            else:
                face_list.sort(key=lambda x: x[1],
                               reverse=True)  # sort the list according to the 2nd element = the area
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
                   for the detailed explanation. default value 0.01
                first_pass [boolean]: True if we want to use the first pass, False if not.
                second_pass [boolean]: True if we want to use the second pass, False if not.
            """
            surface_to_test = copy.deepcopy(pre_processed_surface_list)

            ## Initialization
            first_pass_duration = 0
            second_pass_duration = 0
            kept_surfaces_dict_list = []

            ## first pass
            if first_pass:
                first_pass_duration = time.time()
                kept_surfaces_dict_list = self.shading_context_first_pass(surface_to_test, mvfc)
                first_pass_duration = time.time() - first_pass_duration
                ## second pass
                if second_pass:
                    second_pass_duration = time.time()
                    kept_surfaces_dict_list = self.shading_context_second_pass(kept_surfaces_dict_list)
                    second_pass_duration = time.time() - second_pass_duration

                first_pass_duration = time.time() - first_pass_duration


            ## second pass only
            elif second_pass:
                second_pass_duration = time.time()
                kept_surfaces_dict_list = self.shading_context_second_pass(surface_to_test)
                second_pass_duration = time.time() - second_pass_duration

            surface_dict_to_hb_faces(kept_surfaces_dict_list)

            self.context_shading_HB_faces = kept_surfaces_dict_list

            return (kept_surfaces_dict_list, first_pass_duration, second_pass_duration)

        def shading_context_first_pass(self, pre_processed_surface_list, mvfc):
            """
            First pass of the selection of the shading surfaces from the context.
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
            kept_surfaces = []  # surfaces to keep after the first pass
            for test_face in pre_processed_surface_list:  # loop over all the context surfaces
                for target_face in self.external_face_list_target:  # loop over all the surfaces of the target building
                    if max_VF(centroid_1=target_face["centroid"], area_1=target_face["area"],
                              centroid_2=test_face["centroid"], area_2=test_face["area"]) >= mvfc:  # mvf criterion
                        kept_surfaces.append(test_face)  # if criteria valid, add the surface to the kept surface
                        break  # if a surface is context for one of the target surface, it is kept and thus stop the loop

            return kept_surfaces

        def shading_context_second_pass(self, pre_processed_surface_list):
            """
            + Second pass of the selection of the shading surfaces from the context.
            + Use raytracing to identify the obstructions among the context surfaces.
            + The context surfaces to test are generally pre-filtered by the first pass.
            + Rays are sent from the left, right and middle of each target building facade to the left, right and middle of
              target building facade.
            + The z coordinate of the receiver/context building vertices is the height of the context building.
            + The z coordinate of the sender/target building vertices is the minimum between the height of the target and
              the context building
            Args:
                pre_processed_surface_list [list]: list containing all the surfaces to test, usually pre filtered
                    by the first pass. Each element, representing a surface, is a dictionary with the following properties
                     {"hb_face_obj", "area", "centroid":(Point3D), "lower_corner_point3d":{"left","right"},"height"}

            """
            # Initialization
            kept_surfaces = []  # surfaces to keep after the first pass
            # Preparation of the context in pyvista format
            list_hb_face_context = pre_processed_surface_list_to_hb_face_list(pre_processed_surface_list)
            context_mesh_pv = hb_face_to_pv_polydata(list_hb_face_context)

            for test_face in pre_processed_surface_list:  # loop over all the context surfaces
                for target_face in self.external_face_list_context:  # loop over all the surfaces of the target building
                    # we use the _list_context as the surfaces are sorted from bigger to smaller and it is faster
                    if is_obstructed(emitter=target_face, receiver=test_face, context=context_mesh_pv) == False:
                        kept_surfaces.append(test_face)  # if criteria valid, add the surface to the kept surface
                        break  # if a surface is context for one of the target surface, it is kept and thus stop the loop

            return kept_surfaces

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


def surface_dict_to_hb_faces(surface_dict_list):
    """ convert the list of dictionary surfaces to hb faces"""
    hb_surface_list = []  # if no surface return empty list
    if surface_dict_list != []:
        for surface_dict in surface_dict_list:
            hb_surface_list.append(surface_dict["hb_face_obj"])  # take the hb face from the dict
    return hb_surface_list


def is_obstructed(emitter, receiver, context):
    """
    Check if the surfaces
    """
    ## preprocess the vectors to check
    ray_list = []
    ray_0 = None
    ray_1 = None
    ray_2 = None
    ray_3 = None
    ray_4 = None
    ray_5 = None
    ray_6 = None

    ## loop over the context
    for ray in ray_list:
        # WARNING : the ray tracing work only if the surfaces are oriented
        context.ray_trace(origine=ray[0], end_point=ray[1], first_point=False)

        break
    if obstructed == False:
        return False


# if all the ray were obstructed at least once, receiver context surface should not be included in the computation
return True


def pre_processed_surface_list_to_hb_face_list(pre_processed_surface_list):
    """ convert the preprocessed surface list into hb face list """
    return ([face["hb_face_obj"] for face in pre_processed_surface_list])


def hb_face_to_pv_polydata(hb_face):
    """ convert the context hb face to a polydata Pyvista mesh  """

    # vertices
    vertices = []  # initialize the list of vertices
    lb_vertex_list = hb_face.vertices  # extract LB geometry vertices
    # face [number of vertices, index vertex 1, index vertex 2 ...] <=> [n, 0,1,2...]
    face = [len(lb_vertex_list)]
    # extraction
    for index, vertex in lb_vertex_list:
        vertices.append([vertex.x, vertex.y, vertex.z])  # add the coordinates of the vertices
        face.append(index)
    vertices = np.array(vertices)  # convert into numpy array ( makes it faster to process for later

    return pv.PolyData(vertices, face)


def hb_face_list_to_pv_polydata(hb_face_list):
    """ convert the context hb face to a polydata Pyvista mesh  """

    # Initialize mesh
    mesh_list = []

    for hb_face in hb_face_list:
        mesh_list.append(hb_face_to_pv_polydata(hb_face))

    mesh = sum(mesh_list)  # merge all the sub_meshes/hb faces/facades of all the context building

    return mesh


def are_hb_faces_facing(hb_face_1, centroid_1, hb_face_2, centroid_2):
    """ check with the normals if the surfaces are facing each other (and thus they can shade on each other) """

    # normal vectors
    normal_1 = hb_face_1.normal
    normal_2 = hb_face_2.normal
    # vectors from centroid_2 to centroid_1
    vector_21 = centroid_1 - centroid_2  # operation possible with LB Point3D
    # dot product
    dot_product_sup = normal_2.dot(vector_21)
    dot_product_inf = normal_1.dot(vector_21)
    # vivibility/facing criteria  (same as PyviewFactor)
    if dot_product_sup > 0 and dot_product_inf < 0:
        return True
    else:
        return False
