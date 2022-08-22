from multiprocessing import Pool
from time import time
import pyvista as pv
from pyviewfactor import compute_viewfactor

def many_VF_cal(rectangle_1,rectangle_2,nb_it):

    nb_process = 10
    # nb_it=3000
    dt=time()
    p=Pool(nb_process)
    p.starmap(compute_viewfactor,[(rectangle_1,rectangle_2) for i in range(nb_it)],chunksize=10)
    p.close()
    p.join()
    # for i in range(nb_it):
    #     h=pvf.compute_viewfactor(rectangle_1, pvf.compute_viewfactor)
    #
    dt=time()-dt
    # print(dt)
    return(dt)