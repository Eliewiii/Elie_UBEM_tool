import random

from PIL import Image, ImageEnhance

import os
import random
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry.point import Point
import shapely
from shapely.ops import transform
from shapely.geometry.polygon import Polygon
from shapely.affinity import rotate, translate,scale
import shutil
from math import  sqrt

import multiprocessing as mp



def generate_data_base_from_sample(path_file_shp,index,output_building_type_path,nb_sample_noise,is_deg):
    """


    """
    ## Extract shape
    polygon = extract_shape_shp(path_file_shp)
    ## Convert to meter and move
    if is_deg :
        shape = convert_shape_to_meter(polygon)
    # print("zob")
    # Remove collinear vertices
    shape = clean_polygon(shape)
    ## original image
    image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
    Polygon_to_png_BnW(shape, image_output_path)
    # increase the counter
    index += 1
    ## rotated original image
    for angle in range(10,360,10) : # 1 shape per degree
        # rotate the shape
        rotated_shape = rotate_shape(shape,angle)
        # generate the image
        image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
        Polygon_to_png_BnW(rotated_shape,image_output_path)
        # increase the counter
        index += 1
    ## images with moise
    for i in range(nb_sample_noise) :
        # rotate the shape
        noisy_shape = add_noise_to_shape(shape)
        # generate the image
        image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
        Polygon_to_png_BnW(noisy_shape,image_output_path)
        # #test
        # image_output_path = os.path.join(output_building_type_path, "sample_x_{}.png".format(index))
        # Polygon_to_png_BnW_test(noisy_shape,image_output_path)
        # increase the counter
        index += 1

    return(index)



def generate_data_base_from_sample_parallel(path_file_shp,index,output_building_type_path,nb_sample_noise,is_deg):
    """


    """
    ## Extract shape
    polygon = extract_shape_shp(path_file_shp)
    ## Convert to meter and move
    if is_deg :
        shape = convert_shape_to_meter(polygon)
    # print("zob")
    # Remove collinear vertices
    shape = clean_polygon(shape)
    ## original image
    image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
    Polygon_to_png_BnW(shape, image_output_path)
    # increase the counter
    index += 1
    ## rotated original image
    nb_angles = 36
    step_angle =360/nb_angles

    pool = mp.Pool(10)
    result=[pool.apply(generate_angle,args=(shape,step_angle*i,output_building_type_path,index+i)) for i in range(1,nb_angles)]
    pool.close()


    ## images with moise
    index+= index+ nb_angles-1

    for i in range(nb_sample_noise) :
        # rotate the shape
        noisy_shape = add_noise_to_shape(shape)
        # generate the image
        image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
        Polygon_to_png_BnW(noisy_shape,image_output_path)
        # #test
        # image_output_path = os.path.join(output_building_type_path, "sample_x_{}.png".format(index))
        # Polygon_to_png_BnW_test(noisy_shape,image_output_path)
        # increase the counter
        index += 1

    return(index)





def generate_angle(shape,angle,output_building_type_path,index) :
    """
    """
    # rotate the shape
    rotated_shape = rotate_shape(shape, angle)
    # generate the image
    image_output_path = os.path.join(output_building_type_path, "sample_{}.png".format(index))
    Polygon_to_png_BnW(rotated_shape, image_output_path)



def convert_shape_to_meter(shape):
    """

    :param shape:
    :return:
    """


    ## Convert to meters
    factor = 111139
    shape = scale(shape,xfact=factor,yfact=factor,origin=(0,0,0))
    x, y = shape.exterior.xy
    # print([x,y])
    ## Shift to the center
    centroid = shape.centroid
    [x,y] = [centroid.x,centroid.y]
    shape = translate(shape,-x,-y)

    # centroid = shape.centroid
    # [x,y] = [centroid.x,centroid.y]
    # print([x,y])

    return (shape)



def convert_vertex_to_meter(vertex):
    factor = 111139  #scaling factor
    [x, y] = [vertex[0], vertex[1]]
    return((x + random.uniform(-max_shift,max_shift), y + random.uniform(-max_shift,max_shift)))

def extract_shape_shp(path_file_shp):
    """
    """
    data = gpd.read_file(path_file_shp)
    shape = data['geometry'][0]
    return(shape)


def Polygon_to_png_BnW(shape,path) :
    """ 
    """
    ## Generate RGB image
    x, y = shape.exterior.xy
    plt.plot(x, y)
    plt.axis('off')
    plt.axis('equal')
    plt.savefig(path, bbox_inches=0,dpi=300)
    plt.clf()

    ## Convert to black and white
    file = path
    img = Image.open(file)
    img = img.convert("L")
    img.save(path)

# def Polygon_to_png_BnW_test(shape,path) :
#     """
#     """
#     ## Generate RGB image
#     x, y = shape.exterior.xy
#     plt.plot(x[:-1], y[:-1], "x")
#     # plt.axis('off')
#     plt.axis('equal')
#     plt.savefig(path, bbox_inches=0,dpi=300)
#     plt.clf()
#
#     ## Convert to black and white
#     file = path
#     img = Image.open(file)
#     img = img.convert("L")
#     img.save(path)

def rotate_shape(shape,angle):
    """
    Rotate the shape according to the given angle
    * input :
        - shape : Polygon (obj)
        - angle [deg]
    * output :
        - new shape/Polygon object rotated
    """
    return(rotate(shape, angle, origin='centroid'))



def add_noise_to_shape(polygon):
    """

    """
    # rotation

    polygon = rotate(polygon, random.random()*360, origin='centroid')
    # noise on vertices position
    exterior = polygon.exterior.coords
    interiors = polygon.interiors
    new_exterior = []
    new_interiors = []

    for vertex in exterior[:-1] :
        new_exterior.append(add_noise_to_point(vertex))
    for interior in interiors :
        new_hole=[]
        for vertex in interior[:-1]:
            new_hole.append(add_noise_to_point(vertex))
        new_interiors.append(new_hole)
    return(Polygon(shell=new_exterior,holes=new_interiors))

### ADD MIRROR EFFECT EVENTUALLY


def add_noise_to_point(vertex):
    max_shift = 1  # max
    [x, y] = [vertex[0], vertex[1]]
    return((x + random.uniform(-max_shift,max_shift), y + random.uniform(-max_shift,max_shift)))




#################################### remove collinear vertices in polygons #############################################

def clean_polygon(polygon) :
    """
    """
    exterior = polygon.exterior.coords    # exterior vertices of the polygon
    interiors = polygon.interiors # list of holes vertices of the polygon
    # initialization
    new_interiors=[]
    # Computation
    new_exterior = remove_collinear_vertices(exterior)
    for hole in interiors :
        new_interiors.append(remove_collinear_vertices(hole.coords))

    return(Polygon(shell=new_exterior,holes=new_interiors))

def remove_collinear_vertices(vertex_list):
    """
    extract the points from a polygon
    """
    # tolerance
    tol = 0.01 # if the distance from C to (AB) is greater than the tolerance the AC abd AB are not collinear
    # Computation
    if len(vertex_list) <= 4 : # no need if there is less than 4 vertices (and can create problems)
        return(vertex_list)
    else :
        new_vertex_list = []
        n_ver = len(vertex_list) # number of vertices in the polygon
        pt_A_index = 0
        pt_B_index = 2
        pt_C_index = 1
        for i in range(n_ver-2) :
            d = distance_line([vertex_list[pt_A_index],vertex_list[pt_B_index]], vertex_list[pt_C_index]) # compute distance
            if d < tol : # if collinear, we don't keep the vertex C
                pt_B_index += 1
                pt_C_index += 1
            else : # if not, we keep it
                new_vertex_list.append(vertex_list[pt_C_index])
                pt_A_index += 1
                pt_B_index += 1
                pt_C_index += 1
        # check for the last point
        d = distance_line([new_vertex_list[-1],vertex_list[0]], vertex_list[-1]) # compute distance
        if d >= tol : # if not collinear we keep it
            new_vertex_list.append(vertex_list[-1])

        # check or the first point
        d = distance_line([new_vertex_list[-1], new_vertex_list[0]], vertex_list[0])  # compute distance
        if d >= tol:  # if not collinear we keep it
            new_vertex_list.insert(0,vertex_list[0])

        return(new_vertex_list)


def distance_line(pt_line,pt_C) :
    """
    Compute the distance from pt_C to the line going through pt_A and pt_B
    pt_line = [(x_a,y_a),(x_b,y_b)]
    pt_C    = (x_c,y_c)
    """
    [(x_a, y_a), (x_b, y_b)] = pt_line
    (x_c, y_c) = pt_C
    # characteristic values of the line mx+p=y
    m = (y_b-y_a)/(x_b-x_a)
    p = y_a-m*x_a
    # distance
    d = abs((m*x_c - y_c+p)/sqrt(m**2+1))
    return(d)







def clean_directory(path):
    """

    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def degree_to_meter(x,y,z=None) :
    """
    """
    factor = 111139
    return tuple(filter(None, [x * factor, y * factor]))






# building_type_folder_path = "D://Elie//PhD//Programming//GIS//Building_type//North_Tel_Aviv//double_z//sample_1//double_z.shp"
#
# factor = 111139
#
# shape=extract_shape_shp(building_type_folder_path)
# print(shape.exterior)
#
# new= scale(shape,xfact=factor,yfact=factor,origin=(0,0,0))
# print(new.exterior)
#
# centroid = new.centroid
# [x, y] = [centroid.x, centroid.y]
# renew = translate(new, -x, -y)
# print(renew.exterior)




