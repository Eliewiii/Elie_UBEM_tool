"""

"""


def HB_apply_buildings_characteristics(self):
    """
    Force construction set and program on rooms depending on if they are conditioned or not
    """
    for room in self.HB_model.rooms:
        zob = construction_set_by_identifier("2004::ClimateZone1::SteelFramed")
        ## assign construction set
        room.properties.energy.construction_set = construction_set_by_identifier(self.typology.constructions_set_id)
        ## assign program
        if room.properties.energy.is_conditioned:
            room.properties.energy.program_type = program_type_by_identifier(
                self.typology.program_type_apartment_id)  # if conditioned => apartment
        else:
            room.properties.energy.program_type = program_type_by_identifier(self.typology.program_type_core_id)