"""

"""
from typology_identifier.generate_models._load_ml_parameters import load_ml_parameters
from typology_identifier.typology_identifier import load_ml_model, identify_shape_type


class Mixin:
    None

    def identify_shapes_type_building_to_simulate(self, path_model_param_json, path_temp_image_folder, min_prob):
        """ For all the shapes """

        # load teh ML parameters
        identifier, path_training_data, path_test_data, path_model_pkl, shapes, shapes_to_labels_dic, labels_to_shapes_dic, \
        nb_shapes, pixel_size = load_ml_parameters(path_model_param_json)
        # load the ML model (done once)
        ml_model = load_ml_model(path_model_pkl, nb_shapes)

        # loop for all the shapes
        for building_id in list(self.building_dict.keys()):
            building_obj = self.building_dict[building_id]  # building object
            if not building_obj.typology:  # if the building doesn't have a typology already
                typology_id = identify_shape_type(lb_face_footprint=building_obj.LB_face_footprint, ml_model=ml_model,
                                                  path_folder_image=path_temp_image_folder, pixel_size=pixel_size,
                                                  labels_to_shapes_dic=labels_to_shapes_dic, min_prob=min_prob)
                building_obj.typology=self.typology_dict[typology_id]

    # clean temp file with the tempoary images genetrated for the identification
