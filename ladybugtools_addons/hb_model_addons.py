"""
Additional functions to apply on honeybee model
"""


from honeybee.room import Room
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.lib.programtypes import program_type_by_identifier

def hb_model_apply_constructionset(hb_model, constructions_set_id):
    """
    Assign construction set and program type to each room of the model
    """
    for room in hb_model.rooms:
        ## assign construction set
        room.properties.energy.construction_set = construction_set_by_identifier(constructions_set_id)
        ## assign program


def hb_model_apply_programs(hb_model, program_type_apartment_id, program_type_core_id):
    """
    Assign construction set and program type to each room of the model
    """
    for room in hb_model.rooms:
        ## assign program
        if room.properties.energy.is_conditioned:
            # if conditioned => apartment
            room.properties.energy.program_type = program_type_by_identifier(program_type_apartment_id)
        else:
            room.properties.energy.program_type = program_type_by_identifier(program_type_core_id)


def hb_model_window_by_facade_ratio_per_direction(hb_model, ratio_per_direction, min_length_wall_for_window=2.,only_conditioned=True):
    """
    Assign window to each room of the model
    """
    for room in hb_model.rooms:
        if room.properties.energy.is_conditioned or only_conditioned==False:
            for face in room.faces:
            # get the length of the surface => projection of the face on the XY plane
                pt_a , pt_b = room.min, room.max # extreme points of the
