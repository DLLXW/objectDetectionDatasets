#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import codecs
import cv2
import json
underwater_classes = ['holothurian', 'echinus', 'scallop', 'starfish']
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# 批量重命名文件


def interpr_json():
    test_json_raw = json.load(open("../../data/train/annotations/testA.json", "r"))
    test_json = json.load(open("../../results/cas_r50.bbox.json" , "r"))
    img_dir='../../data/test-A-image'
    root = '../../data/persudo/'
    img = test_json_raw['images']
    images = []
    imgid2anno = {}
    imgid2name = {}
    for imageinfo in test_json_raw['images']:
        imgid = imageinfo['id']
        imgid2name[imgid] = imageinfo['file_name']
    for anno in test_json:
        img_id = anno['image_id']
        if img_id not in imgid2anno:
            imgid2anno[img_id] = []
        imgid2anno[img_id].append(anno)
    for imgid, annos in imgid2anno.items():
        image_name = imgid2name[imgid]
        image_id = image_name.split('.')[0]
        image_path = os.path.join(img_dir, image_id + '.jpg')
        img = cv2.imread(image_path)
        height, width ,depth= img.shape
        with codecs.open(root+ image_id + '_test.xml', 'w', 'utf-8') as xml:
            xml.write('<annotation>\n')
            xml.write('\t<filename>' + image_id + '_test' + '</filename>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>' + str(width) + '</width>\n')
            xml.write('\t\t<height>' + str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
            xml.write('\t</size>\n')
            cnt=0
            for anno in annos:
                xmin, ymin, w, h = anno['bbox']
                xmax = xmin + w
                ymax = ymin + h
                xmin = int(xmin)
                ymin = int(ymin)
                xmax = int(xmax)
                ymax = int(ymax)
                confidence = anno['score']
                class_id = int(anno['category_id'])
                class_name = underwater_classes[class_id - 1]
                image_name = imgid2name[imgid]
                image_id = image_name.split('.')[0]
                #
                if cnt==0:
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>' + class_name + '</name>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
                    cnt+=1
                if confidence>0.4:
                    cnt+=1
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>'+class_name+'</name>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            assert cnt>0
            xml.write('</annotation>')

interpr_json()
