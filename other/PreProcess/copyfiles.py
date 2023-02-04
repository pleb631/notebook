# -*- coding: utf-8 -*-
#!/usr/bin/python
#test_copyfile.py

import os,shutil
import pathlib

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

srcfile='/home/andy/test.py'
dstfile='/home/andy/devWorkSpace/test.py'

mymovefile(srcfile,dstfile)


def draw_img(img, box, clr, message):
    '''Draw bounding box on image'''
    x1, y1, x2, y2 = map(int, box) # map appley the first parameter function to the second parameter
    cv2.rectangle(img, (x1,y1), (x2,y2), clr, 1)
    cv2.putText(img, message, (x1-10,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, clr, 1)
    return img