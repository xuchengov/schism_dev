import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# **1. Read latitude and longitude from out2d_1.nc**
grid_file = "out2d_1.nc"
ds_grid = nc.Dataset(grid_file)

lon = ds_grid.variables["SCHISM_hgrid_node_x"][:]
lat = ds_grid.variables["SCHISM_hgrid_node_y"][:]

# Read connectivity and convert masked array to normal NumPy array
connectivity = ds_grid.variables["SCHISM_hgrid_face_nodes"][:] - 1
connectivity = np.array(connectivity.filled(-1), dtype=int)  # Convert masked array to normal NumPy

# **2. Read temperature data from temperature_2.nc**
temp_file = "temperature_5.nc"
ds_temp = nc.Dataset(temp_file)

# Extract sea surface temperature (first time step, surface level)
temperature = ds_temp.variables["temperature"][22, :, 49]

# **3. Convert Quadrilateral Elements to Triangles using Fast NumPy Processing**
quad_mask = connectivity[:, 3] != -1  # True if it's a quadrilateral
triangles_from_quads = np.column_stack([
    connectivity[quad_mask][:, [0, 1, 2]],  # First triangle from quad
    connectivity[quad_mask][:, [0, 2, 3]]   # Second triangle from quad
]).reshape(-1, 3)  # Reshape into (N, 3) shape

triangles_from_triangles = connectivity[~quad_mask][:, :3]  # Existing triangles

# Combine all triangles efficiently
connectivity = np.vstack([triangles_from_triangles, triangles_from_quads])

# **4. Remove invalid elements before triangulation**
valid_mask = (connectivity >= 0) & (connectivity < len(lon))
connectivity = connectivity[np.all(valid_mask, axis=1)]

# **5. Create triangulation**
triang = tri.Triangulation(lon, lat, connectivity)

# **6. Plot the temperature distribution**
plt.figure(figsize=(10, 8))
plt.tripcolor(triang, temperature, shading='flat', cmap="jet")
plt.colorbar(label="Sea Surface Temperature (°C)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Sea Surface Temperature - First Time Step")
plt.show()





