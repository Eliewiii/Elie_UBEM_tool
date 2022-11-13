
# Variables initialization

energy_consumption={"tot_h_cop_compared_to_ref":2.,


def generate_graph_result():
    """

    """
    fig, ax = plt.subplots()
    width = 0.3
    bar_location = -0.1
    # model = []  # A list in the form of ["Building_1", "Building_2",...]
    x_position_bar = []  # A list used to record the location of the center of bar for each building in the graph

    # building_id

        bar_location += 1.1
        x_position_bar.append(bar_location)
        heating_bar = ax.bar(bar_location - width, energy_consumption["tot_h_cop_compared_to_ref"],
                             width, color="red", label="heating", zorder=10)
        cooling_bar = ax.bar(bar_location - width, building_obj.energy_consumption["tot_c_cop_compared_to_ref"],
                             width, color="blue",
                             bottom=building_obj.energy_consumption["tot_h_cop_compared_to_ref"],
                             label="cooling", zorder=10)
        carbon_ftp_bar = ax.bar(bar_location,
                                building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["mini"] -
                                building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
                                width, color="green",
                                bottom=building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
                                label="carbon footprint", zorder=10)
        tot_impact_bar = ax.bar(bar_location + width,
                                building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["mini"] -
                                building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
                                width, color="green",
                                bottom=building_obj.energy_consumption["tot_BER_compared_to_ref"],
                                label="total environmental impact", zorder=10)
        if bar_location == 1:
            ax.legend()
    ax.set_xticks(x_position_bar, labels=model)
    ax.set_ylabel("Environmental impact in KWh/m2 compared to reference")

    fig.tight_layout()
    plt.savefig(join(path_folder_building_results, "graph.png"))
    plt.show()

# Execute the function
generate_graph_result()




# todo: to plot multiple graphs next to each other use the library subplot