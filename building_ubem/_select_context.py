"""
Additional methods for the Building class.
Deals with the context selection of the context.
"""
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

    def prepare_face_for_context_new(self,is_target=False):
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
                face_list.append({"face_hb_obj": face, "area": face.geometry.area, "centroid": face.geometry.centroid,
                                  "lower_corner": {"left": face.geometry.lower_left_corner,
                                                   "right": face.geometry.lower_right_corner},"height":self.height})
        if is_target:
            face_list.sort(key=lambda x: x[1], reverse=False)  # sort the list according to the 2nd element = the area
            # from smaller to bigger for context building
            self.external_face_list_target=face_list
        else:
            face_list.sort(key=lambda x: x[1], reverse=True)  # sort the list according to the 2nd element = the area
            # from bigger to smaller for context building
            self.external_face_list_context=face_list



    def identify_context_building(self, context_building_obj):
        """
        # todo

        """
        # list_context_surface=deepcopy(context_building_obj.)



    def identify_context_surfaces_with_raytracing_second_pass(self):
        """
        todo
        :return:
        """



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
