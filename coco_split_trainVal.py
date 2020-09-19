import json
import os
import shutil
json_dir="demo/coco/annotations/annotations.json"
with  open(json_dir)  as f:
    json_file = json.load(f)
print('所有图片的数量：', len(json_file['images']))
print('所有标注的数量：', len(json_file['annotations']))


def get_key(images, image_id):
    for image in images:
        if image["id"] == image_id:  # 根据anno的id反推图像的名称
            return image["file_name"]

background=[]
obj=[]
# read box info for csv format
annotations = json_file['annotations']
images = json_file['images']

all_images=[]
for image in images:
    all_images.append(image["file_name"])

for annotation in annotations:
    key = annotation["image_id"] # 图像的名字
    im_id=get_key(images,key)
    if im_id not in obj:
        obj.append(im_id)

    #value = annotation["bbox"] + annotation["category_id"]

#删除背景图像
print('原始图像数量:', len(images))

print('有标注的图像数量:', len(obj))

for img in images:
    if img["file_name"] not in obj:
        background.append(img)

for i in background:
    images.remove(i)
print('删除背景后的图像数量',len(images))#
#根据obj筛选图片
image_dir='demo/coco/images'
#dst_dir='/home/limzero/clear_images'
#for name in obj:
    #shutil.copy(os.path.join(image_dir,name),os.path.join(dst_dir,name))

json_file['images']=images
with  open('demo/coco/annotations/annotations_washed.json',  'w')  as f:
    json.dump(json_file, f)

#分割训练集和验证集
import random
val = random.sample(obj, int(len(images)*0.1))
train=[]
for o in obj:
    if o not in val:
        train.append(o)

#
train_dir='demo/coco/train2017'
val_dir='demo/coco/val2017'
if not os.path.exists(train_dir):
    os.makedirs(train_dir)
if not os.path.exists(val_dir):
    os.makedirs(val_dir)
for v in val:
    shutil.copy(os.path.join(image_dir,v),os.path.join(val_dir,v))
for t in train:
    shutil.copy(os.path.join(image_dir,t),os.path.join(train_dir,t))


#annotations

val_images=images[:]
train_images=images[:]
val_annotations=annotations[:]
train_annotations=annotations[:]

print('images:',len(images),'val:',len(val),'train',len(train))
c=0
for img in images:
    if img['file_name'] in train:
        c=c+1
        val_images.remove(img)
    else:
        train_images.remove(img)
print('len(images):',len(images))
print("c:",c)
print('val_images:',len(val_images),'train_images:',len(train_images))

def get_id(images,name):
    for image in images:
        if image['file_name']==name:
            return image['id']
for t in train:
    id=get_id(images,t)
    for ann in annotations:
        if ann['image_id']==id:
            val_annotations.remove(ann)
for v in val:
    id=get_id(images,v)
    for ann in annotations:
        if ann['image_id']==id:
            train_annotations.remove(ann)
print('train_ann:',len(train_annotations),'val_ann:',len(val_annotations))

json_train=json_file.copy()
json_val=json_file.copy()
json_train['images']=train_images
json_train['annotations']=train_annotations
json_val['images']=val_images
json_val['annotations']=val_annotations

#reindex
for idx in  range(len(json_train['annotations'])):
    json_train['annotations'][idx]['id']  = idx

for idx in  range(len(json_val['annotations'])):
    json_val['annotations'][idx]['id']  = idx

#write in json file
with  open('demo/coco/annotations/train2017.json',  'w')  as f:
    json.dump(json_train, f)

with  open('demo/coco/annotations/val2017.json',  'w')  as f:
    json.dump(json_val, f)


