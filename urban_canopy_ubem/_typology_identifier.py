"""

"""


class Mixin:

    def identify_shapes_type_building_to_simulate(self, footprint, path_model_pkl, path_model_param_json):
        """ For all the shapes """
        # Clean the folder that will host the

        # load teh ML parameters
        identifier, path_training_data, path_test_data, path_model_pkl, shapes, shapes_to_labels_dic, labels_to_shapes_dic, \
        nb_shapes, pixel_size = load_ml_parameters(path_model_param_json)
        # load the ML model (done once)
        load_ml_model(path_model_pkl, path_model_param_json)
        # loop for all the shapes
        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]  # building object
            if not building_obj.typology : # if the building doesn't have a typology already



    # clean temp file with the tempoary images genetrated for the identification
