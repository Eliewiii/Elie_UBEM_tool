
def extract_to_csv(file_path, urban_canopy_obj):

    with open(file_path, 'w') as csvfile:
        csvfile.write(" , h_cop, c_cop, tot_ber_no_light[kWh/m2], rating[kWh/m2]\n")

    # define the content of csv file
    with open(file_path, 'a') as csvfile:
        for building_id in urban_canopy_obj.building_to_simulate:
            building_obj = urban_canopy_obj.building_dict[building_id]
            for apartment_obj in building_obj.apartment_dict.values():
                if apartment_obj.is_core == False:
                    csvfile.write("Apartment_{}, {}, {}, {}, {}\n".format(
                        apartment_obj.identifier,
                        round(apartment_obj.heating["total_cop"], 3),
                        round(apartment_obj.cooling["total_cop"], 3),
                        round(apartment_obj.total_BER_no_light, 3),
                        apartment_obj.rating))
            # define the "total data" of csv file
            csvfile.write("Total, rating={}, tot_cop={}kWh/m2, tot_ber={}kWh/m2 ".format(
                building_obj.rating,
                round(building_obj.energy_consumption["total_w_cop"], 3),
                round(building_obj.energy_consumption["total_BER_no_light"], 3)))

