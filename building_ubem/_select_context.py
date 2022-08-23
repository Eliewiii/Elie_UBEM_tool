"""
Additional methods for the Building class.
Deals with the context selection of the context.
"""
from ladybug_geometry.geometry3d import Vector3D


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



    def prepare_face_for_context_pv(self, reverse=False):
        """
        Returns a a list that will be used for the context selection.
        return a list as followed:
        [  [face_obj, area, centroid], [], .... ]
        order from the smallest area to the biggest
        if reverse==True, it is sorted reverse

        """
        vertex_list= self.footprint.reverse() #the footprint look down
        nb_points_footprint = len(vertex_list) # number of vertices in the footprint
        surface_dict_list=[]

        # for
        #     surface_dict_list.append({"pv_surface":,"pt_left","pt_right","pt_middle"})
        # for
        #
        #
        #
        # for
        #
        #     pt_left,pt_right,pt_middle=
        #
        # self.dict_surface_context_filtering={"id":self.id,"height":self.height,"surfaces"=surface_dict_list}
        #
        #
        #
        #



























