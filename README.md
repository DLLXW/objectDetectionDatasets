# objectDetectionDatasets
目标检测数据集制作:VOC,COCO,YOLO等常用数据集格式的制作和互相转换脚本,demo/目录提供的原始的voc格式的20张原图和对应20个.xml标注．
下面的脚本都可以通过这个demo数据跑通.
## voc_split_trainVal.py
该脚本用于生成voc/目录下的ImageSets/..目录,分割了训练和验证集
## voc_to_coco_V1.py　和　voc_to_coco_V2.py
这两个脚本都是实现从voc的.xml标注格式转换到coco的.json格式,只是有所区别
> - v1版本实现了转换的同时进行训练／验证的分割
> - v2版本包含了segemetation字段(当训练htc等需要分割的任务时候网络需要用到)
## convert_voc_to_yoloV5.py　和 convert_voc_to_yoloV3.py
两个脚本实现的功能几乎相同,灵活取用
> - V5脚本实现将voc格式的数据转化为yoloV5需要的.txt标注文件,运行该脚本，会在voc/目录下生成
worktxt/目录(yolo需要的格式).
> - V3这个脚本除了生成.txt的标注(同上)，还会生成一个trianval.txt的索引,以前的yolov3系列用的多一点

## coco_split_trainVal.py
该脚本实现coco格式的数据分割出训练集和验证集,同时里面还实现了一个去除背景图的方法(没有标注框的图)，可以结合上面的
voc_to_coco_v2.py使用.

## make_voc.py(其余各种格式转voc)
前面没有写coco转voc格式的脚本,make_voc.py就提供了一个制作voc格式数据的通用套路（核心代码）.
```python
`img = cv2.imread(image_path)
            height, width, depth = img.shape
            with codecs.open(anno_dir + imgId_frame_name[:-4] + '.xml', 'w', 'utf-8') as xml:
                xml.write('<annotation>\n')
                xml.write('\t<filename>' + imgId_frame_name + '</filename>\n')
                xml.write('\t<size>\n')
                xml.write('\t\t<width>' + str(width) + '</width>\n')
                xml.write('\t\t<height>' + str(height) + '</height>\n')
                xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
                xml.write('\t</size>\n')
                cnt = 0
                for bbox in bboxs:
                    xmin, ymin, xmax, ymax = bbox
                    class_name = 'obstacles'
                    #
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>' + class_name + '</name>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
                    cnt += 1
                assert cnt > 0
                xml.write('</annotation>')`
```
