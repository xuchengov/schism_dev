"""
-- coding: utf-8 --

Documentation for 01000_2dm_to_DomainShapefile.py


Technical Contact(s):
Name:  XC

This script processes a mesh file using the ocsmesh library and converts it into a shapefile.

Language:  Python 3.11

Usage: Run the script to convert a mesh file into a polygon representation and save it as a shapefile.

Arguments:
- inputfile: Path to the mesh file (in .2dm format)

Returns:
- A shapefile representing the polygonal structure of the mesh.

Dependencies:
- ocsmesh
- geopandas

Author Name:  XC       Creation Date:  03/2025

Revisions:
Date          Author             Description
----          ------             -----------
03/2025       XC                Initial creation

"""


import ocsmesh  # Import the ocsmesh library for mesh processing
import geopandas as gpd  # Import GeoPandas for handling geospatial data

# Define the input mesh file path
inputfile = '../2dm_stofs3d/stofs_3d_atl_hgrid.2dm'

# Open the mesh file with the specified coordinate reference system (CRS: EPSG 4326)
mesh = ocsmesh.Mesh.open(inputfile, crs=4326).msh_t

# Extract the polygon representation of the mesh
mesh_poly = ocsmesh.utils.get_mesh_polygons(mesh)

# Create a GeoDataFrame with the extracted mesh polygon
gpd_shp = gpd.GeoDataFrame(geometry=[mesh_poly])

# Set the coordinate reference system (CRS) to EPSG:4326 (WGS 84)
gpd_shp.set_crs(epsg=4326, inplace=True)

# Save the GeoDataFrame as a shapefile
gpd_shp.to_file("output_stofs3d/stofs3d.shp")




