import shapefile
import numpy as np

def read_2dm(file_path):
    nodes = {}
    elements = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'ND':
                node_id = int(parts[1])
                x, y, z = map(float, parts[2:5])
                nodes[node_id] = (x, y, z)
            elif parts[0] == 'E3T':
                element_id = int(parts[1])
                node_ids = list(map(int, parts[2:5]))
                elements.append((element_id, node_ids))
    return nodes, elements

def write_shapefile(nodes, elements, shp_path):
    # Create a shapefile writer object for polygons
    w = shapefile.Writer(shp_path, shapeType=shapefile.POLYGON)
   
    # Define the fields for the shapefile
    w.field('ID', 'N')

    for element_id, node_ids in elements:
        if all(node_id in nodes for node_id in node_ids):
            # Create the polygon for the triangular element
            polygon = [(nodes[node_id][0], nodes[node_id][1]) for node_id in node_ids]
            polygon.append(polygon[0])  # Close the polygon
            w.poly([polygon])
            w.record(ID=element_id)

    # Save the shapefile
    w.close()

def convert_2dm_to_shapefile(twodm_file, shapefile_path):
    nodes, elements = read_2dm(twodm_file)
    write_shapefile(nodes, elements, shapefile_path)


# Usage
input_2dm_path='./hgrid_SECOFS_Mar2024.2dm.txt'
output_shapefile_path='./output_shapefile/hgrid_SECOFS_Mar2024.shp'
convert_2dm_to_shapefile(input_2dm_path, output_shapefile_path)




