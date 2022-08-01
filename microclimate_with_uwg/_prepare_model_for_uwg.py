"""
Functions to generate modified EPW files (for EnergyPlus) considering the microclimate
"""
import dragonfly.building
import honeybee


def hb_models_to_df_buildings(hb_model_list):
    """ """
    building_list = []
    for hb_model in hb_model_list:
        building_list.append(dragonfly.building.Building.from_honeybee(hb_model))
    return building_list




if __name__=="__main__" :
    hb_json_example = "D:\Elie\PhD\Simulation\Simulation_saved\BER_LCA_proj\\New_ref_3_floors\IS_5280_A_Tel_Aviv\Simulation_BER_ref_A_east\Buildings\Building_0\HBjson_model\in.hbjson"
    hb_model = honeybee.model.Model.from_hbjson(hb_json_example)

    hb_model_list=[hb_model]

    df_building_list = hb_models_to_df_buildings(hb_model_list)
    df_building=df_building_list[0]

    print(df_building.properties.uwg.program)
