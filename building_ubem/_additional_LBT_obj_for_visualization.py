"""
Additional methods for the Building class.
Mainly used to generate HB objects that will be used for plotting purposes
"""

from ladybug_geometry.geometry3d import Polyface3D
from honeybee.room import Room

from math import pi

from ladybug_geometry.geometry3d import Point3D

from ladybug_geometry.geometry3d import Face3D
from ladybug_geometry.bounding import bounding_domain_x, bounding_domain_y, bounding_rectangle_extents, _orient_geometry


class Mixin:

    def LB_face_to_HB_room_envelop(self):
        """ create a honeybee room with extruded footprints of the building, mostly for plotting purposes
        and the context filter algorithm that will use these geometry as    """
        extruded_face = Polyface3D.from_offset_face(self.LB_face_footprint, self.height)
        identifier = "building_{}".format(self.id)
        self.HB_room_envelop = Room.from_polyface3d(identifier, extruded_face)


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


def lb_oriented_bounding_box(lb_geometry, n_step=360):
    """ Get the Face3D oriented bounding rectangle/box of a Face3D geometry"""

    bounding_box_area_list = []
    angle = 0
    step = 2 * pi / 360
    for i in range(n_step):
        length, width = bounding_rectangle_extents(lb_geometry, axis_angle=angle)
        bounding_box_area_list.append(length * width)
        angle += step

    angle = step * bounding_box_area_list.index(min(bounding_box_area_list))

    oriented_bounding_box = bounding_rectangle(lb_geometry, axis_angle=angle)

    return oriented_bounding_box, angle


if __name__ == "__main__":
    pts = [Point3D(0, -1, 0), Point3D(1, 0, 0), Point3D(0, 1, 0), Point3D(-1, 0, 0)]
    face = Face3D(pts)
    # print(face)
    oriented_bounding_box, angle = oriented_bounding_box([face])
    print(oriented_bounding_box.vertices, angle)
