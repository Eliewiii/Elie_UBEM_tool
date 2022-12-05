





class Mixin:
    def generate_oriented_bounding_box(self):
        """  """
        # Identify the oriented bounding rectangle
        bounding_box, angle = lb_oriented_bounding_box(self.LB_face_footprint)
        # extrude the rectangle to obtain the oriented bounding box
        extrude_lb_face_to_hb_room
        # assign the bounding box
        self.hb_oriented_bounding_box = bounding_box