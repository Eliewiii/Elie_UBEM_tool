
import urban_canopy

from ladybug_geometry.geometry3d import Point3D,Face3D,Polyface3D,Vector3D

import dragonfly as df
import dragonfly.building
from dragonfly.room2d import Room2D
from dragonfly.story import Story

import honeybee
from honeybee.room import Room
from honeybee.face import Face
from honeybee.model import Model
from honeybee import orientation

import honeybee_energy
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.lib.programtypes import program_type_by_identifier
from honeybee_energy.writer import model_to_idf
from math import sqrt
from honeybee_energy.internalmass import InternalMass
from honeybee_energy.lib.constructions import opaque_construction_by_identifier

from honeybee.model import Model
from honeybee.face import Face
from honeybee.shade import Shade

class Building:
    """
    description ............


    Properties:
        * urban_canopy [Urban_Canopy object] : urban canopy the building belongs
        * id [int] : id of the building in the urban canopy
        * footprint [list of lists] : list of the points of the footprint ((x,y),(x,y)...)
        * holes [list of lists of lists] : list of the points of the holes [((x,y),(... ] (optional)
        * name [str] : name of the building (optional in the shape file, but it will get a name automatically anyway)
        * group [str] : name of the group the building belongs if it has one (optional)
        * age [int] : year of construction of the building (optional)
        * typo [str] : typology the building belongs to (optional, but will be assigned one anyway)
        * height [float] : height of the building in meter
        * num_floor [int] : number of floors

    Ladybug:
        * LB_face_footprint [int] : number of floors

    Dragonfly:
        * zob
        *

    Honeybee:
        *
        *


    """
    def __init__(self, urban_canopy, id, footprint, holes_footprint=None, name= None, group=None, age=None, typo=None, height=None, num_floor=None, building_id_shp=None, elevation=0., dimension = 2 ):
        """Initialize a building"""
        ## add building to urban canopy dictionary
        urban_canopy.add_building(id,self)
        self.urban_canopy = urban_canopy
        # # # # # # # properties # # # # # # #
        self.id        = id
        self.footprint = footprint
        self.holes     = holes_footprint
        self.name      = name
        self.group     = group
        self.age       = age
        self.typology  = typo
        self.height    = height
        self.num_floor = num_floor
        self.elevation = elevation
        self.dimension = dimension
        self.shp_id    = building_id_shp # id in the shp file, can be useful to see which is the building if a problem is spotted
        self.floor_height = None
        self.int_mass_ratio = None

        self.is_target = False
        self.is_simulated = False

        # # Ladybug #
        self.LB_face_footprint = None #  EVENTUALLY ANOTHER VERSION FOR THE FIRST FLOOR IF DIFFERENT
        self.LB_face_centroid = None
        self.LB_apartments = None
        self.LB_cores = None
        self.LB_balconies = None
        self.LB_extruded_building = None
        # # Honeybee # #
        self.HB_room_envelop = None
        self.HB_model =None
        # # DragonFly # #
        self.DF_story = None
        self.DF_building = None
        # # View factor # #
        self.context_buildings_id = []
        self.context_buildings_HB_faces = []
        # # additional characteristics
        self.cores_per_floor = None   # number of cores per floor
        self.use = None               # use of the building, given by the GIS por the typology: ["residential", "residential with 1st floor commercial", "office"]
        # # EnergyPlus
        self.idf_path = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                      Properties             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        if name==None:
            self.__name="Building_"+str(self.id)
        else:
            None # for now, will add the real name of the building when we define properly how to treat it

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        if age==None:
            self.__age = None
        else:
            try:
                int(age)
            except:
                print("the format of the age is wrong")
            else:
                self.__age = float(age)


    # @property
    # def use(self):
    #     return self.__use
    # @use.setter
    # def use(self, use):
    #     if use==None:
    #         self.__use = None
    #     else:
    #         try:
    #             int(use)
    #         except:
    #             print("the format of the use is wrong")
    #         else:
    #             self.__use = float(use)



    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, height):
        if height==None:
            self.__height=9.0 # by default 3 floors of 3 meters
        else:
            try:
                float(height)
            except:
                print("the format of height is wrong")
            else:
                self.__height = float(height)
    @property
    def num_floor(self):
        return self.__num_floor
    @num_floor.setter
    def num_floor(self, num_floor):
        if num_floor==None :
            self.__num_floor=self.height//3. # by default 3 meters
        else:
            None
            try:
                float(num_floor)
            except:
                print("the format of the number of floor is wrong")
            else:
                self.__num_floor = int(num_floor)

    @property
    def floor_height(self):
        return self.__floor_height
    @floor_height.setter
    def floor_height(self, floor_height):
        if floor_height==None:
            self.__floor_height=self.height/self.num_floor
        else:
            try:
                float(floor_height)
            except:
                print("the format of the floor height is wrong")
                self.__floor_height = self.height / self.num_floor
            else:
                if floor_height>0 :
                    self.__floor_height = float(floor_height)
                else :
                    self.__floor_height=self.height/self.num_floor


    @property
    def is_target(self):
        return self.__is_target
    @is_target.setter
    def is_target(self, is_target):
        if is_target==False:
            self.__is_target = False
        elif is_target == True :
            self.__is_target = True
            self.is_simulated = True #if it's a target building we simulate it...
            if self.id not in self.urban_canopy.target_buildings :
                self.urban_canopy.target_buildings.append(self.id)
        else:
            None

    @property
    def is_simulated(self):
        return self.__is_simulated
    @is_simulated.setter
    def is_simulated(self, is_simulated):
        if is_simulated==False:
            self.__is_simulated = False
        elif is_simulated == True :
            self.__is_simulated = True
            if self.id not in self.urban_canopy.building_to_simulate :
                self.urban_canopy.building_to_simulate.append(self.id)
        else:
            None

    @property
    def int_mass_ratio(self):
        return self.__int_mass_ratio
    @int_mass_ratio.setter
    def int_mass_ratio(self, int_mass_ratio):
        if int_mass_ratio==None:
            self.__int_mass_ratio = 1.5 # by default 1.5, value of the Israeli standard 5282
        else:
            try:
                float(int_mass_ratio)
            except:
                print("the format of height is wrong")
            else:
                self.__int_mass_ratio = float(int_mass_ratio)



    # @property
    # def is_simulated(self):
    #     return self.__is_simulated
    # @is_simulated.setter
    # def is_simulated(self, is_simulated):
    #     if is_simulated==None:
    #         self.__is_simulated="Building_"+str(self.id)
    #     else:
    #         None

    # CHECK IF IT HAS ENOUGH PROPERTIES TO BE SIMULATED, MAYBE JUST MENTION IT DOESN'T HAVE AND ADD STANDARD PROPERTIES
    # MIGHT HAVE TO CHANGE THE WAY WE USE THE SETTERS FOR THE HEIGHT ETC...
    #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                   Class methods             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @classmethod
    def from_shp_2D(cls, id, point_list_footprints, urban_canopy, shape_file, building_id_shp,unit):
        """  create a building object from geometry in a shapefile """

        ## create the building object from POLYGON fron shp file
        building_obj=cls(urban_canopy,id,footprint=point_list_footprints[0],holes_footprint=point_list_footprints[1], building_id_shp=building_id_shp, dimension= 2)
        ## convert footprint and holes to lists
        building_obj.point_tuples_to_list()
        ## convert to the correct unit (meter instead of degrees if necessary)
        building_obj.scale_unit(unit)
        ## Delete the points that are too close to each other in the footprint and holes
        building_obj.check_point_proximity()
        ## affect the properties from  the shp file
        building_obj.affect_properties_shp(shape_file, building_id_shp)
        ## check if the properties given are sufficient to run building simulation
        building_obj.check_property()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # #  Initialization  and verification shape files # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def affect_properties_shp(self,shp_file,building_id_shp):
        """ collect the building properties from the shp file and assign them to the building properties """

        ## need to move these list somewhere else, where they can be edited, but for now they stay there
        age_possibilities =["age","date"]
        typology_possibilities =["typo","typology","type","Typology"]
        # height_possibilities = ["height","Height"]
        height_possibilities = ["height", "Height", "govasimple"]
        number_floor_possibilities =["number_floor","nb_floor","mskomot"]
        name_possibilities = ["name","full_name_"]
        group_possibilities = ["group"]

        ## age ##
        for property_name in age_possibilities: # loop on all the possible name
            try: # check if the property name exist
                shp_file[property_name]
            except: # if it doesn't, don't do anything
                None
            else: # if it does, assign the information to the building then break = get out of the loop
                self.age=int(shp_file[property_name][building_id_shp])
                break
        ## name ##
        for property_name in name_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.name=shp_file[property_name][building_id_shp]
                break
        ## group ##
        for property_name in group_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.group=shp_file[property_name][building_id_shp]
                break
        ## height ##
        for property_name in height_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.height=shp_file[property_name][building_id_shp]
                self.floor_height = None
                break
        ## number of floor ##
        for property_name in number_floor_possibilities:
            try:
                shp_file[property_name]
            except:
                self.num_floor = None
                self.floor_height = None # not optimized, find a way  to put it outside
            else:
                self.num_floor=shp_file[property_name][building_id_shp]
                self.floor_height = None
                break

        ## typology ##
        for property_name in typology_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.typo=shp_file[property_name][building_id_shp]
                break

      ## MIGHT ADD ELEVATION


    def point_tuples_to_list(self):
        """ Convert the points from tuples (originally in GIS file) to list for more convenience """

        ## footprints ##
        new_point_list_footprint = []
        for point in self.footprint:
            new_point_list_footprint.append(list(point))
        self.footprint=new_point_list_footprint
        ## reverse the orientation, for the normal of the surface o face down = ground floor
        self.footprint.reverse()

        ## holes ##
        new_list_hole=[]
        if self.holes!=[]:
            for hole in self.holes:
                list_point=[]
                if len(hole)==1:
                    hole=hole[0]
                for point in hole:
                    list_point.append(list(point))
                list_point.reverse()
                new_list_hole.append(list_point)
            ## reverse the orientation, for the normal of the surface o face down = ground floor
            self.holes = new_list_hole

        if self.holes==[None]:
            self.holes=[]


    def scale_unit(self,unit):
        """ Apply a conversion factor if the GIS file is in degree """

        if unit=="deg":
            factor = 111139 # conversion factor, but might be a bit different, it depends on the altitude, but the
                            # deformation induced would be small if it' not on a very high mountain
            for point in self.footprint:
                point[0] = point[0] * factor
                point[1] = point[1] * factor

            for hole in self.holes:
                for point in hole:
                    point[0] = point[0] * factor
                    point[1] = point[1] * factor
        elif unit=="m":
            factor = 1
        else:
            factor = 1


    def check_property(self):
        """ check if there is enough information about the building to create a model"""

        None

        # TO DO #
        # have to define the criteria later


    def check_point_proximity(self):
        """
        + Delete the redundant points and the points that are too close to each other in the footprints and holes in the footprints.
        + Reduce the complexity of the shapes of buildings.
        + Prevent, à priori, some mistakes. Honeybee doesn't seem to handle when points are too close to each other, or at least there is a problem
          when such geometries are created in Python, converted in json and then sent to Grasshopper.
        """

        tol = 0.5    # tolerance in meter. if the distance between 2 consecutive point is lower than this value, one of the point is deleted

        ## footprint
        number_of_points = len(self.footprint)
        i=0
        while i<=number_of_points -1 :  # the condition to exist the loop is not good here as the number of points is modified everytime a point is deleted
                                        # but we needed one, the real conditio is inside of it
            if distance(self.footprint[i],self.footprint[i+1])<tol :
                self.footprint.pop(i+1)
            else :
                i+=1
            if i >= len(self.footprint)-1 : # if we reach the end of the footprint, considering some points were removed, the loop ends
                break
        if distance(self.footprint[0], self.footprint[-1]) < tol: # check also with the first and last points in the footprint
            self.footprint.pop(-1)

        ## holes
        if self.holes !=None :
            for hole in self.holes : # same thing as above with the holes
                number_of_points = len(hole)
                i = 0
                while i <= number_of_points - 1:
                    if distance(hole[i], hole[i + 1]) < tol:
                        hole.pop(i+1)
                    else:
                        i += 1
                    if i >= len(hole) - 1:
                        break
                if distance(hole[0], hole[-1]) < tol:
                    hole.pop(-1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                   Ladybug                   # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def footprint_to_LB_face(self):
        """ Convert the footprints into Ladybug Face3D geometry object, the elevation will be 0,  """

        footprint_point_list=[] # list containing the Ladybug Point3D of the external contour of the footprint
        ## External footprint
        for point in self.footprint :
            footprint_point_list.append(Point3D(point[0],point[1],0))
        ## internal holes
        if self.holes != [] and self.holes != None:
            holes_list =[] # list of list of points of holes
            for hole in self.holes :
                holes_point_list=[] # list of points for a hole
                for point in hole :
                    holes_point_list.append(Point3D(point[0], point[1], 0))
                holes_list.append(holes_point_list)
        else :
            holes_list = None
        ## Create the Ladybug face for the footprint
        self.LB_face_footprint = Face3D(footprint_point_list,holes=holes_list , enforce_right_hand=True )
        self.LB_face_centroid = self.LB_face_footprint.centroid



    def LB_face_to_HB_room_envelop(self):
        """ create a honeybee room with extruded footprints of buildings, mostly for plotting purposes  """
        ## NEED TO FIND SOMETHING ELSE? IT 'S ONLY FOR TEST
        # if self.height==None:
        #     self.height=0.

        extruded_face= Polyface3D.from_offset_face(self.LB_face_footprint,self.height)
        identifier = "building_{}".format(self.id)
        self.HB_room_envelop = Room.from_polyface3d(identifier,extruded_face)

    def LB_face_to_LB_extruded(self):
        """
        Extrude the footprint to get an extruded building (before the floor layout is applied) for the 1st use of
        the context filter algorithm.
        """
        # ## NEED TO FIND ANOTHER CRITERION, IT 'S ONLY FOR TEST
        # if self.height==None:
        #     self.height=1.

        self.LB_extruded_building = Polyface3D.from_offset_face(self.LB_face_footprint,self.height)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #               Honeybee modeling             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def select_context_buildings(self, min_VF):
        """
        Select the context buildings from the buildings in the GIS file extracted by the urban_canopy
        using a approximate version of the context pass filter 1 (VF criteria).
        """
        None

    def context_buildings(self):
        """
        Select the context buildings from the buildings in the GIS file extracted by the urban_canopy
        """

        None

    def prepare_face_for_context(self,reverse=False):
        """
        return a list as followed:
        [  [face_obj, area, centroid], [], .... ]
        order from the smallest area to the biggest
        if reverse==True, it is sorted reverse

        """
        face_list=[] # list to return
        z_vertices= [Vector3D(0,0,1),Vector3D(0,0,-1)] # vertical vertices
        for face in self.HB_room_envelop.faces:
            if face.normal not in z_vertices: # do not keep the roof and ground
                face_list.append([face,face.geometry.area,face.geometry.centroid])

        face_list.sort(key=lambda x:x[1],reverse=reverse) # sort the list according to the 2nd element = the area
        return(face_list)




    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #              Typology extraction            # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def extract_face_typo(self):
        """
        Extract the typology faces from txt file

        input:
        * path_file :

        outputs:
        * apartments :
        * core :
        """
        path_file=self.typology.path_file_layout
        ## Apartments
        self.LB_apartments = surface_txt_to_LB_surfaces(path_file + "//apartment.txt")
        self.LB_cores = surface_txt_to_LB_surfaces(path_file + "//core.txt")
        self.LB_balconies = surface_txt_to_LB_surfaces(path_file + "//balcony.txt")
        ## Move the elements to be a the position of building
        [x,y,z] = [self.LB_face_centroid.x,self.LB_face_centroid.y,self.LB_face_centroid.z]
        mov_vector = Vector3D (x,y,z)
        if self.LB_apartments :
            for i,apartment in enumerate (self.LB_apartments):
                self.LB_apartments[i] = apartment.move(mov_vector)
        if self.LB_cores :
            for i,core in enumerate(self.LB_cores):
                self.LB_cores[i] = core.move(mov_vector)
        if self.LB_balconies:
            for i,balcony in enumerate(self.LB_balconies):
                self.LB_balconies[i] = balcony.move(mov_vector)


    def load_characteristic_typo(self):
        """
        Load the constructions, constructions sets, loads etc... of the typology of the building
        """
        None


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #              Dragonfly modeling             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def LB_layout_to_DF_story(self):
        """
        Convert the LB layout to a DF story

        The difference between the first floor and the other floor might have to be made in the future
        """
        DF_room2Dlist = [] # list with all the Room2D objects for the story

        # Create DF Room2D for each apartment (originally a Ladybug 3Dface)
        for i,room in enumerate(self.LB_apartments):
            DF_room2Dlist.append(df.room2d.Room2D("apartment_"+str(i),floor_geometry=room,floor_to_ceiling_height=self.floor_height))
        # Create DF Room2D for each core
        if self.LB_cores :
            for i,room in enumerate(self.LB_cores):
                DF_room2Dlist.append(df.room2d.Room2D("core_"+str(i),floor_geometry=room,floor_to_ceiling_height=self.floor_height))

        # Create the story
        self.DF_story = df.story.Story(identifier="floor",room_2ds=DF_room2Dlist,multiplier=self.num_floor)
        # Solve adjacency and boundary conditions for all the Rooms/Faces
        self.DF_story.intersect_room_2d_adjacency() # prevent some issues with non identified interior walls.
        self.DF_story.solve_room_2d_adjacency()


    def DF_story_to_DF_building(self):
        """
        Convert DF story to DF building.

        Will need to be modified to consider different stories for the same building, especially a first floor.
        """

        self.DF_building=df.building.Building(identifier="Building_"+str(self.id),unique_stories= [self.DF_story])

    def DF_building_to_HB_model(self):
        """ Create an extruded DF building from LB geometry footprint """

        self.HB_model= self.DF_building.to_honeybee(use_multiplier=False)
        # print(self.id,self.LB_face_centroid)






    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #               Honeybee modeling             # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def HB_solve_adjacencies(self):
        """
        Solve the adjacency ...
        Correct the boundary conditions, here especially for the floor/ceiling and the ground floor and roof.
        In addition to the one from Dragonfly, but
        """

        Room.solve_adjacency(self.HB_model.rooms)
        # correct the adiabatic surfaces on the ground and on roof (need to check why it happens)
        for room in self.HB_model.rooms: # loop on rooms (could be just do the ground floor and last floor but whatever)
            for face in room.faces:      # loop on the faces
                if isinstance(face.boundary_condition, honeybee.boundarycondition.Adiabatic):
                    if room.average_floor_height==0: # if can be ground => it's ground floor
                        face.boundary_condition = honeybee.boundarycondition.boundary_conditions.ground
                    else : # if it's not ground and it's adiabatic it's roof a priori, but need to investigate deeper.
                        face.boundary_condition = honeybee.boundarycondition.boundary_conditions.outdoors

    # # # # # # # # # # # # # # # #                  force rotation                 # # # # # # # # # # # # # # # # # # # # #

    def HB_model_force_rotation(self,angle):
        """
        Rotate the model around its centroid
        """
        z_vect = Vector3D(0,0,1)
        self.HB_model.rotate(axis=z_vect,angle=angle,origin=self.LB_face_centroid)

    # # # # # # # # # # # # # # # #                  Internal mass                # # # # # # # # # # # # # # # # # # # # #

    def HB_add_thermalmass_int_wall(self):
        """
        Add the internal mass due the non-load-bearing internal walls
        Israeli Standards suggests 1.5m2 of intwall per floor m2 for a 3m height floor
        Can be generalize to 0.5m2*height
        The intwall is only half an int wall here, the surface counts both sides of the walls
        The default value for self.int_wall_ratio is 1.5
        """
        for room in self.HB_model.rooms:
            if room.properties.energy.is_conditioned:
                int_mass_area = room.floor_area * self.int_mass_ratio
                construction_internal_wall = opaque_construction_by_identifier(self.typology.construction_int_wall_int_mass)
                mass = InternalMass(identifier="int_mass"+room.identifier, construction=construction_internal_wall,
                                    area=int_mass_area)
                room.properties.energy.add_internal_mass(mass)


    # # # # # # # # # # # # # # # #                Create Windows              # # # # # # # # # # # # # # # # # # # # #
    def HB_building_window_generation_floor_area_ratio(self):
        """
        Generate windows on a building according to floor area % per direction
        """
        ratio_per_direction = [self.typology.window_floor_area_ratio_per_direction['north'],
                               self.typology.window_floor_area_ratio_per_direction['east'],
                               self.typology.window_floor_area_ratio_per_direction['south'],
                               self.typology.window_floor_area_ratio_per_direction['west']]

        min_length_wall_for_window = 2. # minimum length of external wall to put a window on, should be extracted from the typology though

        (rooms_per_floor,floor_elevation) = Room.group_by_floor_height(self.HB_model.rooms) # group rooms per floors

        # print(self.id,self.height,self.num_floor,self.floor_height,floor_elevation)
        floor_elevation.append(self.height) # add the height of the building to the list to make the floor height
                                            # calculation below

        orientation_angles = orientation.angles_from_num_orient() # orientation subdivisions for the orientation identification

        floor_heights=[floor_elevation[i+1]-floor_elevation[i] for i in range(len(floor_elevation)-1)] #floor height of all the floors

        for i in range (len(rooms_per_floor)): # do the generation for each floor individually
            self.HB_floor_window_generation_floor_area_ratio( rooms_per_floor[i],floor_heights[i],ratio_per_direction,min_length_wall_for_window,orientation_angles)

    def HB_floor_window_generation_floor_area_ratio(self,rooms,floor_height,ratio_per_direction,min_length_wall_for_window,orientation_angles):
        """
        Generate windows on a floor according to floor area % per direction.
        Called by the function for the whole building.
        """
        floor_area = sum([room.floor_area for room in rooms]) # copute the floor area
        # list with the faces for all directions
        north_faces = []
        east_faces = []
        south_faces = []
        west_faces = []

        for room in rooms:
            # use only conditioned rooms
            if room.properties.energy.is_conditioned == True :
                for face in room.faces :
                    # outdoor faces only
                    if isinstance(face.boundary_condition, honeybee.boundarycondition.Outdoors):
                        # faces with sufficient length according to the min_length_wall_for_window criteria
                        if face.area/floor_height > min_length_wall_for_window :
                            face_orientation = orientation.face_orient_index(face,orientation_angles)
                            # add to the proper orientation list
                            if face_orientation == 0 : #North
                                north_faces.append(face)
                            elif face_orientation == 1:  # East
                                east_faces.append(face)
                            elif face_orientation == 2:  # South
                                south_faces.append(face)
                            elif face_orientation == 3:  # West
                                west_faces.append(face)
        # North
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(north_faces,floor_area, ratio_per_direction[0])
        # East
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(east_faces, floor_area, ratio_per_direction[1])
        # South
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(south_faces, floor_area, ratio_per_direction[2])
        # West
        self.HB_floor_window_generation_floor_area_ratio_per_orientation(west_faces, floor_area, ratio_per_direction[3])

    def HB_floor_window_generation_floor_area_ratio_per_orientation(self,face_list,floor_area, floor_ratio):
        """
        Generate windows on one direction for a floor according to floor area % per direction.
        Called by the function for the whole floor called by the function for the whole building.
        """
        if floor_ratio>0:
            facade_area= sum([face.area for face in face_list]) # compute façade area
            window_ratio = floor_area * floor_ratio / facade_area # compute the % window ratio on the façade
            # Tests to ensure correct windows
            if window_ratio < 0.01 :
                window_ratio = 0.01
            elif window_ratio > 0.95 :
                window_ratio = 0.95
            # Create window for all faces
            for face in face_list:
                face.apertures_by_ratio(window_ratio)

    # # # # # # # # # # # # # # # #                   Blinds                   # # # # # # # # # # # # # # # # # # # # #



    # # # # # # # # # # # # # # # #                 Construction               # # # # # # # # # # # # # # # # # # # # #
    def HB_assign_conditioned_zone(self):
        """
        Assign an ideal hvac system for every apartment types rooms, turning them into conditioned zones
        """
        for room in self.HB_model.rooms: # loop on all rooms
            if "core" not in room.identifier: # if not a core, add ideal air Hvac system, making it a conditioned zone
                room.properties.energy.add_default_ideal_air()


    def HB_apply_buildings_characteristics(self):
        """
        Force construction set and program on rooms depending on if they are conditioned or not
        """
        for room in self.HB_model.rooms:
            zob=construction_set_by_identifier("2004::ClimateZone1::SteelFramed")
            ## assign construction set
            room.properties.energy.construction_set = construction_set_by_identifier(self.typology.constructions_set_id)
            ## assign program
            if room.properties.energy.is_conditioned:
                room.properties.energy.program_type = program_type_by_identifier(self.typology.program_type_apartment_id)  # if conditioned => apartment
            else :
                room.properties.energy.program_type = program_type_by_identifier(self.typology.program_type_core_id)

    # # # # # # # # # # # # # # # #                     IDF                    # # # # # # # # # # # # # # # # # # # # #

    def generate_IDF_from_HB_model(self, simulation_parameters_idf_str,path_folder_idf):
        """ create an IDF from the HB model """
        idf_str  = '\n\n'.join((simulation_parameters_idf_str, model_to_idf(self.HB_model)))
        self.idf_path = path_folder_idf + "in.idf"
        with open(self.idf_path,"w") as idf_file :
            idf_file.write(idf_str)



    def GIS_context_to_hbjson(self, path_folder_context_hbjson):
        """
        Generate a hbjson file to plot the context in Rhinoceros
        The hbjson is a HB model.
        Each room of the model represent one building.
        Rooms are generated with the building envelop = LB polyface3D
        """

        room_list = [] # list of the rooms

        for id in range(self.urban_canopy.num_of_buildings) :
            # plot only the buildings that are not simulated/modeled = the rest of the GIS for now
            if id != self.id:
                room_list.append(self.urban_canopy.building_dict[id].HB_room_envelop)

        model = Model(identifier=("GIS_context_{}").format(self.name),rooms=room_list)
        # generate model
        model.to_hbjson(name="GIS_context",folder=path_folder_context_hbjson)



    def context_surfaces_to_hbjson(self,path):
        """
        Convert HB_face context surface to HBjson file
        """
        surface_list=[]
        for i,surface in enumerate(self.context_buildings_HB_faces) :
            surface_list.append(Face(("context_surface_{}_building_{}").format(i,self.id),surface.geometry))
        model = Model(identifier=("context_building_{}").format(self.id), orphaned_faces=surface_list)
        model.to_hbjson(name=("context_building_{}").format(self.id), folder=path)

    def add_context_surfaces_to_HB_model(self):
        """
        Convert HB_face context surface to HBjson file
        """
        for i,surface in enumerate(self.context_buildings_HB_faces) :
            shade_obj = Shade(identifier=("shade_{}_building_{}").format(i,self.id),geometry=surface.geometry,is_detached=True)
            self.HB_model.add_shade(shade_obj)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #            Dragonfly modeling for UWG       # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # def DF_buildings_for_not_simulated_buildings :








# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # #          Additional useful functions        # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def distance(pt_1,pt_2) :
    """
    :param pt_1: list for the point 1 
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return (sqrt((pt_1[0]-pt_2[0])**2+(pt_1[1]-pt_2[1])**2))




def surface_txt_to_LB_surfaces(path_file):
    """
    description
    input :
             * path_file
    output :
             * LB_surfaces
    """

    LB_surfaces = [] #initialization of the output

    with open(path_file,"r") as txt_file:
        data = txt_file.read() # read the file
        data=data.split("\n")       # separate

        for surface in data:
            point_list = []
            if len(surface)>0:
                surface=surface.split(";")
                for point in surface :
                    [x, y] = point[1:-1].split(",")
                    point = [float(x), float(y)]
                    point_list.append(Point3D(point[0], point[1], 0))
                LB_surfaces.append(Face3D(point_list,enforce_right_hand=False))

    if LB_surfaces==[]:
        LB_surfaces=None

    return (LB_surfaces)





    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # #                  Now useless                # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # def LB_layout_to_DF_building(self):
    #     """
    #     DF building directly from LB layout
    #     """
    #     ## floor height computation ##
    #     floor_to_floor_heights = [3.,3.,3.] # TEST
    #     # TO DO BETTER THAN THIS
    #
    #     self.DF_building= dragonfly.building.Building.from_footprint(identifier=self.name,footprint=self.LB_apartments+self.LB_cores,floor_to_floor_heights=floor_to_floor_heights)


    # def LB_face_to_DF_building(self):
    #     """ Create an extruded DF building from LB geometry footprint """
    #
    #     floor_to_floor_heights = [3.] # TEST
    #
    #     self.DF_building= df_b.Building.from_footprint(self.name,[self.LB_face_footprint],floor_to_floor_heights)

    # def check_name(self):
    #     """ check the name of the building and if it doesn't have one name it"""
    #     max_size= 50 # maximum size of the name (EnergyPlus does accept file name that are too long)
    #
    #     if self.name == None :
    #         self.name = "buildind" # if it does not have a name, give it one
    #     else :
    #         self.name.replace(" ", "_")  # replace all the spaces by _
    #         if len(self.name)>max_size : # reduce the size if the name is too long
    #             self.name=self.name[:50]
    #     self.name=self.name+"_"+str(self.id) # add the id in the end to identify it easily


    # def check_name_DF(self):
    #     """ The name of the building 'Building_x' with x the id of the building, in order to avoid the hebrew characters and the 'hidden' spaces """
    #     self.name = "Building_"+str(self.id)


    # def check_height(self):
    #     """ check the name of the building and if it doesn't have one name it"""
    #
    #     if self.height == None or self.height<0 :
    #         self.height = 6. # if it does not have a name, give it one



























