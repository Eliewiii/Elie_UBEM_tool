"""
Additional methods for the Building class.
Mainly used to generate HB objects that will be used for plotting purposes
"""

from ladybug_geometry.geometry3d import Polyface3D
from honeybee.room import Room

class Mixin:

    def LB_face_to_HB_room_envelop(self):
        """ create a honeybee room with extruded footprints of the building, mostly for plotting purposes  """
        ## NEED TO FIND SOMETHING ELSE? IT 'S ONLY FOR TEST
        # if self.height==None:
        #     self.height=0.

        extruded_face = Polyface3D.from_offset_face(self.LB_face_footprint, self.height)
        identifier = "building_{}".format(self.id)
        self.HB_room_envelop = Room.from_polyface3d(identifier, extruded_face)
