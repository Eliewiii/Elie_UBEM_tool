import matplotlib.pyplot as plt

# Variables initialization
heating = {"Building_1": 20, "Building_2": 30, "Building_3": 40, "Building_4": 50}
cooling = {"Building_1": 10, "Building_2": 20, "Building_3": 30, "Building_4": 40}
tot_ber = {"Building_1": 30, "Building_2": 50, "Building_3": 70, "Building_4": 90}
carbon_max = {"Building_1": -5, "Building_2": -10, "Building_3": -15, "Building_4": -20}
carbon_min = {"Building_1": 30, "Building_2": 40, "Building_3": 50, "Building_4": 60}
model = ["Building_1", "Building_2", "Building_3", "Building_4"]
#energy_consumption={"tot_h_cop_compared_to_ref":2.,


def generate_graph_result():
    """

    """
    fig, ax = plt.subplots()
    width = 0.3
    bar_location = -0.1
    # model = []  # A list in the form of ["Building_1", "Building_2",...]
    x_position_bar = []   # A list used to record the location of the center of bar for each building in the graph

    # building_id
    for i in range(4):
        bar_location += 1.1
        x_position_bar.append(bar_location)
        heating_bar = ax.bar(bar_location - width, heating["Building_"+str(i+1)],
                             width, color="red", label="heating", zorder=10)
        cooling_bar = ax.bar(bar_location - width, cooling["Building_"+str(i+1)],
                             width, color="blue",
                             bottom=heating["Building_"+str(i+1)],
                             label="cooling", zorder=10)
        carbon_ftp_bar = ax.bar(bar_location, carbon_min["Building_"+str(i+1)]-carbon_max["Building_"+str(i+1)],
                                width, color="green",
                                bottom=carbon_max["Building_"+str(i+1)],
                                label="carbon_ftp", zorder=10)
        #carbon_ftp_bar = ax.bar(bar_location,
                                #- carbon_min["Building_" + str(i + 1)] + carbon_max["Building_" + str(i + 1)],
                                #width, color="green",
                                #bottom=carbon_min["Building_" + str(i + 1)],
                                #label="carbon_ftp", zorder=10)
        tot_impact_bar = ax.bar(bar_location + width,
                                carbon_min["Building_"+str(i+1)]-carbon_max["Building_"+str(i+1)],
                                width, color="orange",
                                bottom=tot_ber["Building_"+str(i+1)]+carbon_max["Building_"+str(i+1)],
                                label="total environmental impact", zorder=10)
        if bar_location == 1:
            ax.legend()
    ax.set_xticks(x_position_bar, labels=model)
    ax.set_ylabel("Environmental impact in KWh/m2 compared to reference")

    fig.tight_layout()
    plt.savefig("D:\\Pycharm\\graph.png")
    plt.show()

# Execute the function
generate_graph_result()




# todo: to plot multiple graphs next to each other use the library subplot