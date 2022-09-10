
def extract_to_csv(file_path, urban_canopy_obj):

    with open(file_path, 'w') as csvfile:
        csvfile.write("Building, tot_cop[kWh/m2], tot_ber[kWh/m2], rating[kWh/m2]\n")

    with open(file_path, 'a') as csvfile:
        for building_id in urban_canopy_obj.building_to_simulate:
            building_obj = urban_canopy_obj.building_dict[building_id]
            #for apartment_obj in building_obj.apartment_dict.values():
                #if apartment_obj.is_core == False:
            csvfile.write("{}, {}, {}, {}\n".format(
                building_obj.name,
                round(building_obj.energy_consumption["total_w_cop"], 3),
                round(building_obj.energy_consumption["total_BER_no_light"], 3),
                building_obj.rating))

