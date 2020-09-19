import xml.etree.ElementTree as ET
import os
import cv2
classes = ['window_shielding', 'multi_signs', 'non_traffic_sign']

def convert_annotation(image_id):
    in_file = open('demo/voc/Annotations/%s.xml' % image_id)

    if not os.path.exists('demo/yolov3/custom/labels/'):
        os.makedirs('demo/yolov3/custom/labels/')
    out_file_img = open('demo/yolov3/custom/trainval.txt', 'a')  # 生成txt格式文件

    out_file_label = open('demo/yolov3/custom/labels/%s.txt' % image_id,'a')  # 生成txt格式文件

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    voc_img_dir='demo/voc/JPEGImages/{}.jpg'.format(image_id)
    out_file_img.write(voc_img_dir)
    out_file_img.write("\n")
    img=cv2.imread(voc_img_dir)
    dh = 1. / img.shape[0]
    dw = 1. / img.shape[1]
    cnt=len(root.findall('object'))
    if cnt==0:
        print('nulll null null.....')
        print(image_id)
    cc=0
    for obj in root.iter('object'):
        cc+=1
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        if dw*float(xmlbox.find('xmin').text)<0. or dw*float(xmlbox.find('xmax').text)<0. or dh*float(xmlbox.find('ymin').text)<0. or dh*float(xmlbox.find('ymax').text)<0.:
            print(image_id)

        b = (dw*float(xmlbox.find('xmin').text), dw*float(xmlbox.find('xmax').text), dh*float(xmlbox.find('ymin').text),
             dh*float(xmlbox.find('ymax').text))
        out_file_label.write(str(cls_id)+ " " + str((b[0]+b[1])/2) + " " + str((b[2]+b[3])/2) + " " + str(b[1]-b[0]) + " " + str(b[3]-b[2]))
        if cc<cnt:
            out_file_label.write("\n")
    out_file_label.close()


imgname_list = []
part_name = 'trainval.txt'  # test.txt
with open(os.path.join('demo/voc/', 'ImageSets/Main/' + part_name)) as f:
    all_lines = f.readlines()

for a_line in all_lines:
    imgname_list.append(a_line.split()[0].strip())

print(len(imgname_list))
for image_id in imgname_list:
    convert_annotation(image_id)