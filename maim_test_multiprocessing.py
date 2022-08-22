import pyvista as pv
# from pyviewfactor import compute_viewfactor
# from multiprocessing import Pool
from test_multyprocessing._fuc_for_multi_proc import many_VF_cal
from test_multyprocessing._fuc_2 import zob

from time import time

# Initialization #

# rectangle


if __name__ == '__main__':

    point_a = [1., 0., 0.]
    point_b = [1., 1., 0.]
    point_c = [0., 1., 0.]
    point_d = [0., 0., 0.]
    rectangle_1 = pv.Rectangle([point_a, point_b, point_c, point_d])

    rectangle_2 = rectangle_1.copy()
    rectangle_2.translate([0, 0, 1], inplace=True)

    dt=zob(rectangle_1,rectangle_2,1000)
    print(dt)
    dt=many_VF_cal(rectangle_1,rectangle_2,1000)
    print(dt)


