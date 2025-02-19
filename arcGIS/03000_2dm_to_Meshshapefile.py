import shapefile
import numpy as np

def read_2dm(file_path):
    """
    Reads a 2DM mesh file and extracts node coordinates and triangular elements.
    
    Parameters:
        file_path (str): Path to the 2DM file.
    
    Returns:
        dict: Dictionary containing node IDs as keys and (x, y, z) coordinates as values.
        list: List of triangular elements represented as tuples (element_id, [node_id1, node_id2, node_id3]).
    """
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
    """
    Writes the extracted mesh data to a shapefile in polygon format.
    
    Parameters:
        nodes (dict): Dictionary of node coordinates.
        elements (list): List of triangular elements.
        shp_path (str): Output file path for the shapefile.
    """
    # Initialize a shapefile writer for polygon features
    w = shapefile.Writer(shp_path, shapeType=shapefile.POLYGON)
   
    # Define attribute fields for the shapefile
    w.field('ID', 'N')

    for element_id, node_ids in elements:
        if all(node_id in nodes for node_id in node_ids):
            # Construct the polygon using the node coordinates
            polygon = [(nodes[node_id][0], nodes[node_id][1]) for node_id in node_ids]
            polygon.append(polygon[0])  # Ensure the polygon is closed
            w.poly([polygon])
            w.record(ID=element_id)

    # Save the generated shapefile
    w.close()

def convert_2dm_to_shapefile(twodm_file, shapefile_path):
    """
    Converts a 2DM mesh file to a shapefile format.
    
    Parameters:
        twodm_file (str): Path to the input 2DM file.
        shapefile_path (str): Path to the output shapefile.
    """
    nodes, elements = read_2dm(twodm_file)
    write_shapefile(nodes, elements, shapefile_path)

# Define input and output file paths
input_2dm_path = './hgrid_SECOFS_Mar2024.2dm.txt'
output_shapefile_path = './output_shapefile/hgrid_SECOFS_Mar2024.shp'

# Execute the conversion process
convert_2dm_to_shapefile(input_2dm_path, output_shapefile_path)






