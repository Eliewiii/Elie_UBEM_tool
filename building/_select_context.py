"""
Additional methods for the Building class.

"""
from ladybug_geometry.geometry3d import Vector3D

class Mixin:

    def prepare_face_for_context(self, reverse=False):
        """
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
        return (face_list)
