class FaceContextFilter:
    """
        Args:
        vertex_list: A list of points [x,y,z]
        building_obj :
        height :
        pv_vertex_left_rt :
        pv_vertex_middle_rt :
        pv_vertex_right_rt :
        pv_rectangle_geo :
        pv_center_vertex :
        pv_normal_vector :
    """

    def __init__(self, vertex_list, building_obj):
        self.vertex_list = vertex_list
        self.building_obj = building_obj
        self.height = building_obj.height

