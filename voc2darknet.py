# -*- coding: utf-8 -*-

"""
Created on Mon Mar  13 15:40:43 2016
This script is to convert the txt annotation files to appropriate format needed by YOLO
@author: Martin Hwang
Email: dhhwang89@gmail.com
"""

import os
from os import walk, getcwd
from PIL import Image
import xml.etree.ElementTree as ET
import math

class color:
    BOLD = '\033[1m'
    END = '\033[0m'
    DEFAULT = '\033[0;37;40m'
    RED = '\033[91m'

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (round(x,3), round(y,3), round(w,3), round(h,3))

# Custom define class
# classes = ["F_Baby", "F_Kid", "F_10s", "F_20s", "F_30s", "F_40s", "F_50s", "F_Senior", "M_Baby", "M_Kid", "M_10s", "M_20s", "M_30s", "M_40s", "M_50s", "M_Senior"]
classes = ["ram"]

# Configure Paths
annotation_path = "Annotations/"
yolo_label_path = "labels/"

list_file_name = "parts"

wd = getcwd()
list_file = open('%s/%s_list.txt' % (wd, list_file_name), 'w')

# Get input text file list
xml_name_list = []

for (dirpath, dirnames, filenames) in walk(annotation_path):
    xml_name_list.extend(filenames)
    break
print(color.BOLD + "xml file list : {}".format(xml_name_list) + color.END + '\n')

try:
    #Process
    for xml_name in xml_name_list:
        print('------------------------------------------------------------------------')
        # open xml file
        xml_path = annotation_path + xml_name
        xml_file = open(xml_path, "r")
        print("Input file : " + xml_path)

        tree = ET.parse(xml_file)
        root = tree.getroot()

        size = root.find('size')
        if size == None:
            raise Exception("can't find size tag")

        xml_width = int(size.find('width').text)
        xml_height = int(size.find('height').text)

#        img_path = str('%s/voc2012/jpeg/%s.jpg' % (wd, os.path.splitext(xml_name)[0]))
        img_path = str('%s/Images/%s.JPG' % (wd, os.path.splitext(xml_name)[0]))        

        objects = root.findall('object')
        if len(objects) == 0:
            print(color.BOLD + color.RED + "ERROR : can't find object tag"+ color.END)

            if os.path.exists(xml_path):
                os.remove(xml_path)
            if os.path.exists(img_path):
                os.remove(img_path)
            continue



        # open Image filee
        img = Image.open(img_path)
        img_width = int(img.size[0])
        img_height = int(img.size[1])

        print('Image path : ' + img_path + '\n')
        print("xml size (width, height) : " + "(" + str(xml_width) + ',' + str(xml_height) + ")")
        print('image size (width, height) : ' + "(" + str(img_width) + ',' + str(img_height) + ")\n")

        if not xml_width == img_width or not xml_height == img_height:
            print(color.BOLD + color.RED + "xml and image size different" + color.END)
            raise Exception("xml and image size different")

        # Open output result files
        result_outpath = str(yolo_label_path + xml_name[:-3] + "txt")
        result_outfile = open(result_outpath, "w")
        print("Output:" + result_outpath + '\n')

        for object in objects:

            cls = object.find('name').text
            if cls == None:
                raise Exception("can't find name tag")
            elif cls not in classes:
                raise Exception("name tag not involve this classes")

            bndbox = object.find('bndbox')
            if bndbox == None:
                if os.path.exists(xml_path):
                    os.remove(xml_path)
                if os.path.exists(img_path):
                    os.remove(img_path)
                raise Exception("can't find bndbox tag")

            xmin = int(bndbox.find('xmin').text)
            xmax = int(bndbox.find('xmax').text)
            ymin = int(bndbox.find('ymin').text)
            ymax = int(bndbox.find('ymax').text)

            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((img_width, img_height),b)

            cls_id = classes.index(cls)
            print('class name, index : ' + '(' + str(cls) + ", " + str(cls_id) + ')')
            print("bndbox Size : " + str(b))
            print("convert result : " + str(bb) + '\n')
            result_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        result_outfile.close()
#        list_file.writelines('%s/voc2007/jpeg/%s.jpg\n' % (wd, os.path.splitext(xml_name)[0]))
        list_file.writelines('%s/Images/%s.JPG\n' % (wd, os.path.splitext(xml_name)[0]))        

    list_file.close()

except Exception as e:
    print(color.BOLD + color.RED + "ERROR : {}".format(e) + color.END)

    if not result_outfile.closed:
        print(color.BOLD + color.RED + "Close result_outfile" + color.END)
        result_outfile.close()
    if os.path.exists(result_outpath):
        print(color.BOLD + color.RED + "delete result outpath" + color.END)
        os.remove(result_outfile)

