# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:35:54 2024

@author: oscar
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:33:23 2023

@author: oscar
"""
# Hot Fuss Album

import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider
import os
import pandas as pd

xyz_files = ['C:/Users/oscar/OneDrive - UNSW/cryptophanedraft/Cryptophanes_Output_17_4_2023/Cryptophanes/222/Cs/Inside/Cp222_Cs_Inside_Opt.xyz']
#vdr=1.7 for carbon isn
radius = 1.7
volumes=[]

##you need to do this otherwise things get subtracted in the wrong direction
def buffer_convex_hull(original_hull, radius):
    buffered_vertices = []
    middlebit = np.mean(original_hull.points, axis=0)

    for vertex in original_hull.vertices:
        point = original_hull.points[vertex]
        direction = middlebit - point
        direction /= np.linalg.norm(direction)
        offset_vertex = point + radius * direction
        buffered_vertices.append(offset_vertex)
    return ConvexHull(buffered_vertices)

for xyz_file in xyz_files: 
    file_name = os.path.splitext(os.path.basename(xyz_file))[0]
    with open(xyz_file, 'r') as file:
        lines = file.readlines()

## these are manually selected  atoms. See paper for idea to convert to algorithm. There is stupid list comprehension here
    longlist=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 30, 33, 34, 38, 40, 41, 37, 39, 46, 49, 44, 48, 32, 36, 35, 43, 42, 45]
    new_list = [x+1 for x in longlist]
    boundary_atoms = [lines[i] for i in new_list]
    longth=len(lines)-2
    allatoms=np.arange(0,longth)+1
    boringlist = [i+1 for i in allatoms if i not in longlist]
    boringatoms = [lines[i] for i in boringlist]
    
    # Extract coordinates from the carbon atoms
    coordinates_new_points = []
    for line in boundary_atoms:
        parts = line.split()
        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        coordinates_new_points.append((x, y, z))
        ## you hav to add new atoms here
    boring_coordinates_new_points = []
    for line in boringatoms:
        parts = line.split()
        colordict={"H":"grey","C":"k", "O":"r", "Cs":"m","Rb":"m","Na":"m","K":"m","Li":"m", 'N':'b'}

        at=colordict[parts[0]]

        x2, y2, z2, colorcode = float(parts[1]), float(parts[2]), float(parts[3]) ,at
        boring_coordinates_new_points.append((x2, y2, z2, colorcode))

    coordinates_new_points = np.array(coordinates_new_points)
    hull = ConvexHull(coordinates_new_points)
    buffered_hull = buffer_convex_hull(hull, radius)
    main_hull_volume = hull.volume
    buffered_hull_volume = buffered_hull.volume
#importan
    volumes.append((file_name,main_hull_volume, buffered_hull_volume))
    
    # Create a figure with two 3D subplots
    fig = plt.figure(figsize=(12, 5))

    # Plot the original convex hull and the buffered convex hull on the left subplot
    ax1 = fig.add_subplot(121, projection='3d')
    x, y, z = zip(*coordinates_new_points)
    x2,y2,z2,co =zip(*boring_coordinates_new_points)
    ax1.scatter(x, y, z, c='b', marker='o')
    ax1.scatter(x2, y2, z2, c=co, marker='o')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # Plot the original convex hull
    hull_faces = [coordinates_new_points[s] for s in hull.simplices.tolist()]
    ax1.add_collection3d(Poly3DCollection(hull_faces, facecolors='cyan', linewidths=0.2, edgecolors='b', alpha=0.3))

    # Plot the buffered convex hull
    buffered_faces = [buffered_hull.points[s] for s in buffered_hull.simplices.tolist()]
    ax1.add_collection3d(Poly3DCollection(buffered_faces, facecolors='magenta', linewidths=0.2, edgecolors='g', alpha=0.3))

    ax1.set_title('Aromatic Carbons Convex Hull')

    # Plot the buffered convex hull on the right subplot
    ax2 = fig.add_subplot(122, projection='3d')
    x2, y2, z2 = zip(*buffered_hull.points)
    ax2.scatter(x2, y2, z2, c='b', marker='o')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    # Plot the buffered convex hull
    buffered_faces = [buffered_hull.points[s] for s in buffered_hull.simplices.tolist()]
    ax2.add_collection3d(Poly3DCollection(buffered_faces, facecolors='magenta', linewidths=0.2, edgecolors='g', alpha=0.3))
    ax2.set_title('VDW Convex Hull')

    # Set limits for the axes
    x_min = min(min(x), min(x2))
    x_max = max(max(x), max(x2))
    y_min = min(min(y), min(y2))
    y_max = max(max(y), max(y2))
    z_min = min(min(z), min(z2))
    z_max = max(max(z), max(z2))
##something breaks if you move this?????
    ax1.set_xlabel('X / Ã…')
    ax1.set_ylabel('Y / Ã…')
    ax1.set_zlabel('Z / Ã…')
    ax2.set_xlabel('X / Ã…')
    ax2.set_ylabel('Y / Ã…')
    ax2.set_zlabel('Z / Ã…')
    
    plt.title(f'Plot for {file_name}')
    
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([x_max-x_min, y_max-y_min, z_max-z_min]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x_max+x_min)
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y_max+y_min)
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z_max+z_min)
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
            ax1.plot([xb], [yb], [zb], 'w')
            ax2.plot([xb], [yb], [zb], 'w')
    
    

    #plt.show()

print(volumes)
df = pd.DataFrame(volumes)

## save to xlsx file

