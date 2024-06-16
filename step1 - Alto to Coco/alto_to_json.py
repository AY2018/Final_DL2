# Ce script permet de passer d'un fichier ALTO crée par le modèle 47 à un fichier COCO JSON que l'on peut utiliser sur makesense.ai pour corriger les polygones.
# Il ne prend pas en compte les baselines, mais seulement les coordonées des polygones. 

### Le fichier prend les coordonnées de tout les polygonnes et les assigne à la catégorie "text"

### INPUTS = Nom du fichier $file_name, taille et largeur de l'image : $image_info (lignes 52,53)

import xml.etree.ElementTree as ET
import json
import os

# NOM DU FICHIER 
file_name = '18030-31'


xml_file_path = f'/Users/ayoub/Desktop/Final_DL2/annotations/xml/{file_name}.xml'
image_file_path = f'/Users/ayoub/Desktop/Final_DL2/images/{file_name}.JPG'

# Load and parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

ns = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}

# COCO JSON structure
coco_json = {
    "info": {"description": "my-project-name"},
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 1, "name": "default"},
        {"id": 2, "name": "text"},
        {"id": 3, "name": "Title"},
        {"id": 4, "name": "SteleArea"},
        {"id": 5, "name": "Commentary"},
        {"id": 6, "name": "Numbering"},
        {"id": 7, "name": "Intext"}
    ]
}

# Function to extract coordinates from the polygon points
def extract_coordinates(polygon):
    return [float(coord) for point in polygon.split() for coord in point.split(',')]

# ID counters
image_id = 1
annotation_id = 1

# Add image info to COCO JSON
image_info = {
    "id": image_id,
    "width": 801,
    "height": 2246,
    "file_name": file_name
}
coco_json["images"].append(image_info)

# Extract polygons from the XML and add to annotations
for textline in root.findall('.//alto:TextLine', ns):
    for polygon in textline.findall('.//alto:Polygon', ns):
        points = polygon.get('POINTS')
        segmentation = extract_coordinates(points)
        bbox = [
            min(segmentation[::2]),  # min x
            min(segmentation[1::2]),  # min y
            max(segmentation[::2]) - min(segmentation[::2]),  # width
            max(segmentation[1::2]) - min(segmentation[1::2])  # height
        ]
        area = bbox[2] * bbox[3]

        annotation = {
            "id": annotation_id,
            "iscrowd": 0,
            "image_id": image_id,
            "category_id": 2,
            "segmentation": [segmentation],
            "bbox": bbox,
            "area": area
        }

        coco_json["annotations"].append(annotation)
        annotation_id += 1

# Increment the image ID for the next image
image_id += 1

# Define the output path for the COCO JSON file
output_json_path = f'/Users/ayoub/Desktop/Final_DL2/annotations/coco/{file_name}.json'

# Save the COCO JSON to a file
with open(output_json_path, 'w') as json_file:
    json.dump(coco_json, json_file, indent=4)

print(f"COCO JSON file saved to {output_json_path}")
