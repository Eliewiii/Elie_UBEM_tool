import  os
import copy

from honeybee_energy.lib.constructionsets import construction_set_by_identifier


from tools._save_and_load_objects import save_object_pickle, load_object_pickle
from honeybee.model import Model,Face,Room
import honeybee_energy

hb_f=Face.from_vertices("zob",[(0,0,0),(0,1,0),(1,1,0),(0,1,0)])

hb_room=Room.from_box(identifier="zob_2")
hb_room.properties.energy.construction_set = construction_set_by_identifier("Elie_LCA_BER_R0-W0-G1")
# hb_m = Model.from_hbjson("D:\Elie\PhD\Simulation\Program_output\Simulation_55\Buildings\Building_0\HBjson_model\in.hbjson")

a=copy.deepcopy(hb_room)