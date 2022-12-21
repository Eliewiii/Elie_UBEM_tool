import matplotlib.pyplot as plt

# Variables initialization

data1 = [list(range(-5, 11)), list(range(-5, 6))]
mark = ["co2_emission","energy_consumption"]
x_position_bar = []
building_id = ["Building_1","Building_2","Building_3","Building_4"]

def generate_graph_result():
    bar_location = -0.1
    colors = [(202/255.,96/255.,17/255.),(255/255.,217/255.,102/255.)]
    for i in range(4):
        bar_location += 1.1
        x_position_bar.append(bar_location+0.15)
        plt1 = plt.boxplot(data1, patch_artist=True, labels=mark, positions=(bar_location, bar_location+0.3), widths=0.3)
        for patch, color in zip(plt1['boxes'],colors):
            patch.set_facecolor(color)

        # adding text inside the plot
        plt.text(bar_location+0.15, 6.3, 'A', fontsize=10)

        if bar_location == 1:
            plt.legend(plt1['boxes'], mark)

    plt.xticks(x_position_bar, labels=building_id)
    plt.ylabel("Energy consumption in KWh/m2")
    plt.savefig("D:\\Pycharm\\graph2.png")
    plt.show()

# Execute the function
generate_graph_result()


