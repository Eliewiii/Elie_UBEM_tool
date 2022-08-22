"""
Additional methods for the Building class.
Used for extracting results from CSV
"""
import numpy as np

import pyvista as pv

import pyviewfactor as pvf


def find_extreme_base_point(building_facade):
    None




def face_each_other(polydata_1,polydata_2):
    """
    Check if 2 polydata (can be made of multiple faces, but they must have the same orientation and be coplanar)
    face each other, which means that, assuming there is no obstruction, their
    """










if __name__=="__main__":

    vertices_1 = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]])
    vertices_2 = np.array([[0., 0., -1.], [1., 0., -1.], [0., 1., -1.]])

    faces_1 = np.array([[3, 0, 1, 2]])
    faces_2 = np.array([[3, 2, 1, 0]])

    surf_1 = pv.PolyData(vertices_1, faces_1)
    surf_2 = pv.PolyData(vertices_2, faces_2)

    pointa = [1., 0., 1.]
    pointb = [1., 1., 1.]
    pointc = [0., 1., 1.]
    pointd = [0., 0., 1.]
    rectangle_up = pv.Rectangle([pointd, pointc, pointb, pointa])

    print(pvf.get_visibility(surf_1, surf_2))
    print(pvf.get_visibility(surf_1, rectangle_up))