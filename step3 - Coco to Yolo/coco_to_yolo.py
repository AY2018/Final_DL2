import json

def coco_to_yolo(coco_json_path, yolo_txt_path):
    with open(coco_json_path) as f:
        coco_data = json.load(f)

    image_info = coco_data['images'][0]
    img_width = image_info['width']
    img_height = image_info['height']

    yolo_annotations = []

    for annotation in coco_data['annotations']:
        if annotation['category_id'] == 2:  # Category ID = "text"
            segmentation = annotation['segmentation'][0]

            # Normalize and clamp the polygon coordinates
            normalized_segmentation = [
                min(max(coord / img_width if i % 2 == 0 else coord / img_height, 0), 1)
                for i, coord in enumerate(segmentation)
            ]

            # Format: class x1 y1 x2 y2 ... xn yn
            yolo_line = ["0"] + list(map(str, normalized_segmentation))
            yolo_annotations.append(" ".join(yolo_line))

    # Write to YOLO format text file
    with open(yolo_txt_path, 'w') as f:
        for annotation in yolo_annotations:
            f.write(f"{annotation}\n")

# Define the file name (without extension) as a variable
file_name = '00012-42'

# Construct the input and output paths
coco_json_path = f'/Users/ayoub/Documents/Github/Final_DL2/intext_annotations/coco/{file_name}_intext.json'
yolo_txt_path = f'/Users/ayoub/Documents/Github/Final_DL2/intext_annotations/yolo/{file_name}_intext.txt'

# Convert COCO to YOLO
coco_to_yolo(
    coco_json_path=coco_json_path,
    yolo_txt_path=yolo_txt_path
)

print(f"YOLO annotations saved to {yolo_txt_path}")
