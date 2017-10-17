'''
1. move all labels (labels/*txt) to Images/
2. set a percentage of images to be used for validation/test
3. create a list of training data (train.txt) and a list of validation/test data (test.txt)
4. create the cfg/ for darknet including the .data, the .names, and the .cfg file (for network srchitecture)
5. make changes in the .cfg file to incorporate the current data. Required changes to yolo-cov.cfg for this dataset:
  - batch=[<=number of training images] (line3)
  - subdivisions=1 (lin3 4)
  - classes=[len(classes]) (line 244)
  - filters=[(len(classes)+5)*5] (line 237)
6. Download the YOLOv2 convolutional weights to help the start of the network (from here: https://pjreddie.com/media/files/darknet19_448.conv.23) to use as the baseline of the model
7. run darknet
'''

import os
import shutil
import sys
import wget
import subprocess

current_dir = os.getcwd()
# directory where data and config for this project are going to be (relative to your local darknet dir)
darknet_root_dir = '/home/saghar/darknet/'
darknet_model_dir = 'cfg/'
darknet_data_dir = 'data/pc/'
model = 'yolo-voc'
#model  = str(sys.argv[1])
classes = ['RAM']

##1
source = 'labels/'
dest = 'Images/'
labels = os.listdir(source)
images = os.listdir(dest)
for l in labels:
    shutil.copy(source+l, dest)

##2
test_percentage = 15

##3
with open(os.path.join(darknet_root_dir, darknet_data_dir, 'train.txt'), 'w') as train_file:
    with open(os.path.join(darknet_root_dir, darknet_data_dir, 'test.txt'), 'w') as test_file:
        counter = 1
        index_test = round(100 / test_percentage)
        for i in images:
            if counter == index_test:
                counter = 1
                print counter, 'test', i
                test_file.write(os.path.join(current_dir, dest, i) + "\n")
            else:
                print counter, 'train', i
                train_file.write(os.path.join(current_dir, dest, i) + "\n")
                counter += 1
    
##4
#data_file = open(os.path.join(darknet_root_dir, darknet_data_dir, 'pc.data'), 'w')
#names_file = open(os.path.join(darknet_root_dir, darknet_data_dir, 'pc.names'), 'w')

with open(os.path.join(darknet_root_dir, darknet_data_dir, 'pc.data'), 'w') as data_file:
    with open(os.path.join(darknet_root_dir, darknet_data_dir, 'pc.names'), 'w') as names_file:
        data_file.write('calsses=%d\n'%(len(classes)))
        data_file.write('train=%s\n'%(os.path.join(darknet_root_dir, darknet_data_dir, 'train.txt')))
        data_file.write('valid=%s\n'%(os.path.join(darknet_root_dir, darknet_data_dir, 'test.txt')))
        data_file.write("names=%s\n"%(os.path.join(darknet_root_dir, darknet_data_dir, 'pc.names')))
        data_file.write("backup=backup/")

        for cl in classes:
            names_file.write('%s\n'%cl)
            try:
                shutil.copy(os.path.join(darknet_root_dir, darknet_model_dir, '%s.cfg'%model), os.path.join(darknet_root_dir, darknet_model_dir, '%s_pc.cfg'%(model)))
            except:       
                model = 'yolo-voc'
                shutil.copy(os.path.join(darknet_root_dir, darknet_model_dir, '%s.cfg'%model), os.path.join(darknet_root_dir, darknet_model_dir, '%s_pc.cfg'%(model)))                

##5 - MANUAL

##6 - MANUAL
#darknet19_448.conv.23 = wget.download("https://pjreddie.com/media/files/darknet19_448.conv.23")

##7 - MANUAL
#os.chdir(darknet_root_dir)
#subprocess.Popen("./darknet", "detector", "train", os.path.join(darknet_data_dir, 'pc.data'),  os.path.join(darknet_model_dir, model, '.cfg'), "darknet19_448.conv.23")
