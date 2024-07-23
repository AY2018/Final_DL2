import xml.etree.ElementTree as ET
import json
import os

# NOM DU FICHIER 
file_name = '00012-42'
xml_file_path = f'/Users/ayoub/Documents/GitHub/Final_DL2/annotations/xml/{file_name}.xml'

# Dossier JSON
output_json_path = f'/Users/ayoub/Documents/Github/Final_DL2/annotations/coco/{file_name}.json'

# Load and parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

ns = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}

# Extract file name with correct extension from the XML file
file_name_tag = root.find('.//alto:fileName', ns)
if file_name_tag is not None:
    image_file_name = file_name_tag.text
else:
    raise ValueError("fileName tag not found in the XML file.")

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

# Function to extract coordinates from the polygon points and convert them to integers
def extract_coordinates(polygon):
    return [int(float(coord)) for point in polygon.split() for coord in point.split(',')]

# Get width and height from the Page tag
page = root.find('.//alto:Page', ns)
if page is not None:
    image_width = int(page.get('WIDTH'))
    image_height = int(page.get('HEIGHT'))
else:
    raise ValueError("Page tag with WIDTH and HEIGHT not found in the XML file.")

# ID counters
image_id = 1
annotation_id = 1

# Add image info to COCO JSON
image_info = {
    "id": image_id,
    "width": image_width,
    "height": image_height,
    "file_name": image_file_name  # Use the file name with correct extension
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



# Save the COCO JSON to a file
with open(output_json_path, 'w') as json_file:
    json.dump(coco_json, json_file, indent=4)

print(f"COCO JSON file saved to {output_json_path}")
