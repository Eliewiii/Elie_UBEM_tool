"""
Additional methods for the Urban_canopy class.
Deals with the context filtering
"""



class Mixin:

    def filter_context_surfaces(self, target_building_face_list, test_context_building_face_list, target_id,
                                VF_criteria):
        """
        Check if the  test_context_building is part of the context
        """
        ## first pass
        for test_face in test_context_building_face_list:
            for target_face in target_building_face_list:
                if max_VF(target_face, test_face) >= VF_criteria:
                    self.building_dict[target_id].context_buildings_HB_faces.append(test_face[0])
                    break
        ## second pass

        # to be continued...