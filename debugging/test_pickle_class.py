import dill
import numpy as np
#
#
# class Zob():
#     def __init__(self):
#         self.name = "zob"
#         self.matrix=np.array([1,2,3])



path= "D:\\Elie\\PhD\\test\\zob.p"
#
# with open(path, "wb") as pickle_file:
#     dill.dump(Zob, pickle_file)

class_obj=None
with open(path, "rb") as pickle_file:
    class_obj=dill.load(pickle_file)

print(class_obj().matrix)

