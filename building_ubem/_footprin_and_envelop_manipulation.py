"""
Additional methods for the Building class.
Mainly used to generate HB objects that will be used for plotting purposes
"""

from math import pi

from ladybug_geometry.geometry3d import Point3D, Vector3D, Face3D, Polyface3D
from ladybug_geometry.bounding import bounding_domain_x, bounding_domain_y, bounding_rectangle_extents, _orient_geometry

from honeybee.room import Room


class Mixin:

    def LB_footprint_to_HB_room_envelop(self):
        """ create a honeybee room with extruded footprints of the building, mostly for plotting purposes """
        extruded_face = Polyface3D.from_offset_face(self.LB_face_footprint, self.height)
        identifier = "building_{}".format(self.id)
        self.HB_room_envelop = Room.from_polyface3d(identifier, extruded_face)

    def generate_oriented_bounding_box(self):
        """  """
        self.hb_oriented_bounding_box = lb_footprint_to_hb_bounding_box(self.LB_face_footprint, self.height,
                                                                        "building_{}_BB".format(self.id))

    def correct_envelop_elevation(self):
        """ Correct the elevation of the building envelop from z=0 (EnergyPlus) to its real elevation """
        hb_room_move_vertically(self.HB_room_envelop, self.elevation)

    def correct_bounding_box_elevation(self):
        """ Correct the elevation of the building bounding box from z=0 (EnergyPlus) to its real elevation """
        hb_room_move_vertically(self.hb_oriented_bounding_box, self.elevation)


def lb_footprint_to_hb_bounding_box(lb_face_footprint, height, identifier):
    """ Convert ladybug geometry footprint to bounding box """
    # Identify the oriented bounding rectangle
    bounding_rectangle, angle = lb_oriented_bounding_rectangle([lb_face_footprint])
    # extrude the rectangle to obtain the oriented bounding box
    bounding_box = lb_extrude_face_to_hb_room(bounding_rectangle, height, identifier)
    return (bounding_box)


def lb_extrude_face_to_hb_room(lb_face_footprint, height, identifier):
    """ Extrude the     """
    extrusion = Polyface3D.from_offset_face(lb_face_footprint, height)
    return Room.from_polyface3d(identifier, extrusion)


def bounding_rectangle(geometries, axis_angle=0):
    """Get the oriented bounding rectangle around 2D or 3D geometry according to the axis_angle.

    Args:
        geometries: An array of 2D or 3D geometry objects. Note that all objects
            must have a min and max property.
        axis_angle: The counter-clockwise rotation angle in radians in the XY plane
            to represent the orientation of the bounding rectangle extents. (Default: 0).

    Returns:
        A Face3D type rectangle representing the oriented bounding box.
    """
    if axis_angle != 0:  # rotate geometry to the bounding box
        cpt = geometries[0].vertices[0]
        geometries = _orient_geometry(geometries, axis_angle, cpt)
    xx = bounding_domain_x(geometries)
    yy = bounding_domain_y(geometries)
    pt_1 = Point3D(xx[0], yy[0])
    pt_2 = Point3D(xx[0], yy[1])
    pt_3 = Point3D(xx[1], yy[1])
    pt_4 = Point3D(xx[1], yy[0])
    if axis_angle != 0:  # rotate the points back
        cpt = Point3D(cpt.x, cpt.y, 0.)  # cast Point3D to Point2D
        pt_1 = pt_1.rotate_xy(axis_angle, cpt)
        pt_2 = pt_2.rotate_xy(axis_angle, cpt)
        pt_3 = pt_3.rotate_xy(axis_angle, cpt)
        pt_4 = pt_4.rotate_xy(axis_angle, cpt)

    return Face3D([pt_1, pt_2, pt_3, pt_4])  # The rectangle doesn't need to be counterclock, the transformation into
    # face3D will solve the issue automaically


def lb_oriented_bounding_rectangle(lb_geometry_list, n_step=360):
    """ Get the Face3D oriented bounding rectangle/box of a Face3D geometry"""
    # Initialization
    bounding_rectangle_area_list = []
    angle = 0
    step = 2 * pi / 360
    # loop for all the angles
    for i in range(n_step):
        length, width = bounding_rectangle_extents(lb_geometry_list, axis_angle=angle)
        bounding_rectangle_area_list.append(length * width)
        angle += step
    # get the angle that minimize the area of the bounding rectangle
    angle = step * bounding_rectangle_area_list.index(min(bounding_rectangle_area_list))
    # get the bounding rectangle for the best angle
    oriented_bounding_rectangle = bounding_rectangle(lb_geometry_list, axis_angle=angle)

    return oriented_bounding_rectangle, angle


def hb_room_move_vertically(hb_room, height):
    """ Move vertically a HB Room object """
    moving_vector = Vector3D(0., 0., height)
    hb_room.move(moving_vector)

if __name__ == "__main__":
    pts = [Point3D(0, -1, 0), Point3D(1, 0, 0), Point3D(0, 1, 0), Point3D(-1, 0, 0)]
    face = Face3D(pts)
    # print(face)
    oriented_bounding_box, angle = lb_oriented_bounding_rectangle([face])
    print(oriented_bounding_box.vertices, angle)
