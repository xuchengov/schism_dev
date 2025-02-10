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




