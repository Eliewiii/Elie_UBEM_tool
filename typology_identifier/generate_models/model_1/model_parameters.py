"""
All the parameters of the model
To put in a json file, will be easier to load
"""
# Path to the folder with the training and test images for the ML model
path_training_data =
path_test_data =

# Size in pixel
height = 90
width = 90

# List of the shape types in the model
shapes = ['double_z', 'h_type_1', 'h_type_2', 'rect_crop', 'square']
# Dictionary with the shape name and their associated index
shapes_to_label_dic = {}
for index, shape in enumerate(shapes):
    shapes_to_label_dic[index] = shape
# Number of labels
nb_labels = len(shapes)
