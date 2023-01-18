import geopandas as gpd
import shapely

def extract_gis(path_gis):
    """ Extract gis file and return the python shapefile object"""
    shape_file = gpd.read_file(path_gis)
    return shape_file

if __name__=="__main__":
    path_gis = "C:\\Users\elie-medioni\OneDrive\OneDrive - Technion\Ministry of Energy Research\Ron and Elie\Double_Train\Double_Train_01"

    shapefile = extract_gis(path_gis)
    print(shapefile["geometry"])