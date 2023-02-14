from shapely.geometry import Polygon
import matplotlib.pyplot as plt

from ladybug_geometry.geometry3d.brep import Brep

# create two Polygon objects
poly1 = Polygon([(0, 0), (1, 1), (1, 0)])
poly2 = Polygon([(1,0), (1, 1), (2, 1)])

# merge the polygons
merged_poly = poly1.union(poly2)

# create a new figure and axis
fig, ax = plt.subplots()

# plot the polygons
ax.plot(*poly1.exterior.xy, label='poly1')
ax.plot(*poly2.exterior.xy, label='poly2')
ax.plot(*merged_poly.exterior.xy, label='merged_poly')

# set the x and y limits of the axis
ax.set_xlim(-1, 3)
ax.set_ylim(-1, 3)

# add a legend
ax.legend()

# show the plot
plt.show()

# poly_2.translate(1, 0)