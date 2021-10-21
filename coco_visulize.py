import os
import cv2

from pycocotools.coco import COCO

json_file = '/home/trojanjet/baidu_qyl/tianma/detect/mmdetection/data/coco/annotations/instances_val2017.json'
dataset_dir = '/home/trojanjet/baidu_qyl/tianma/detect/mmdetection/data/coco/val2017/'
coco = COCO(json_file)
imgIds = coco.getImgIds() # 
for i in range(len(imgIds)):
    img = coco.loadImgs(imgIds[i])[0]
    image = cv2.imread(dataset_dir + img['file_name'])
    annIds = coco.getAnnIds(imgIds=img['id'])
    annos = coco.loadAnns(annIds)
    for ann in annos:
        bbox = ann['bbox']
        x, y, w, h = bbox
        anno_image = cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), 2) 
    cv2.imwrite('demo.jpg', anno_image)
    break

