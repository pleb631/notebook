from pathlib import Path
import tqdm
import random
import cv2
import numpy as np


def save_txt(txt_path, info, mode='w'):

    with open(txt_path, mode) as txt_file:
        for line in info:
            
            txt_file.write(' '.join(list(map(str,line))) + '\n')
            
            
def crop(im,boxes,h,w):
    h1,w1,_ = im.shape
    x1 = random.randint(0,max(w1-w,0))
    y1 = random.randint(0,max(h1-h,0))
    x2 = min(x1 + int((random.random()*0.5+1)*w),w1)
    y2 = min(y1 + int((random.random()*0.5+1)*h),h1)
    im_crop = im[y1:y2,x1:x2,:].copy()
    crop_xyxy = []
    for box in boxes:
        if x1<box[1]<x2 and y1<box[2]<y2:
            clss,xc,yc,wc,hc = box
            x11,y11 =max(xc-wc//2-x1,0),max(yc-hc//2-y1,0)
            x21,y21 = min(x11+wc,x2-x1),min(y11+hc,y2-y1)
                
            crop_xyxy.append([clss,x11,y11,x21,y21])

    return im_crop,crop_xyxy
    
    
def getdata(bg):
    anno_path = bg.parent.parent/"labels"/(bg.with_suffix('.txt').name)
    txt_file = open(anno_path, "r", encoding="UTF-8")
    anno = [line.replace("\n", "") for line in txt_file]
    imbg = cv2.imread(str(bg))
    h,w,c=imbg.shape
    boxes = []
    for i,line in enumerate(anno):
        line = list(map(float, line.split()))
        clss,xc,yc,wc,hc = line
        box = [int(line[0]),xc * w, yc * h, wc * w, hc * h]
        boxes.append(box)  
        
    return imbg,boxes



def rotate(ps,m):
    pts = np.float32(ps).reshape([-1, 2])  # 要映射的点
    pts = np.hstack([pts, np.ones([len(pts), 1])]).T
    target_point = np.dot(m, pts)
    target_point = [[target_point[0][x],target_point[1][x]] for x in range(len(target_point[0]))]
    return target_point

def _rotate_img_and_point(img,points,angle,resize_rate=1.0):
    h,w,c = img.shape
    M = cv2.getRotationMatrix2D((w//2,h//2), angle, resize_rate)
    res_img = cv2.warpAffine(img, M, (w, h))
    out_points = rotate(points,M)
    return res_img,out_points

def crop_fgimg_box(im,box):
    clss,xc,yc,wc,hc = box
    x1,y1 =xc-wc//2,yc-hc//2
    x2,y2 = x1+wc,y1+hc
    h,w,c=im.shape
    pt = [[x1,y1],[x2,y2],[x1,y2],[x2,y1]]
    x11,y11,x21,y21=-1,-1,-1,-1
    i=0
    while(not (0<=x11<=w and 0<=x21<=w and 0<=y11<=h and 0<=y21<=h)):
        i+=1
        if i>20:
            return None
        res_img,out_points = _rotate_img_and_point(im,pt,random.randint(0,45))
        x11,y11 = min(np.array(out_points)[:,0]),min(np.array(out_points)[:,1])
        x21,y21 = max(np.array(out_points)[:,0]),max(np.array(out_points)[:,1])
    xyxy = [clss,int(x11),int(y11),int(x21),int(y21)]
    im_crop = res_img[int(y11):int(y21),int(x11):int(x21),:].copy()
    im_crop = cv2.resize(im_crop,None,fx=random.random()*0.4+0.8,fy=random.random()*0.4+0.8)
    
    return im_crop

if __name__ =="__main__":
    bg_root = r'/root/dataset/train'
    fw_root = r'/root/dataset/train_crop'

    dst = r'/root/dataset/train_fake'

    bg_items = list(Path(bg_root).rglob('*.jpg'))
    random.shuffle(bg_items)

    sample=4000
    prog = tqdm.tqdm(total=sample)
    ht,wt=640,640
    i=0
    while(i<sample):
        bg = random.choices(bg_items)[0]

        imbg,bgboxes = getdata(bg)
        crop_im,crop_xyxys = crop(imbg,bgboxes,ht,wt)
        h,w,_=crop_im.shape
        repeat = random.randint(1,4)
        j=0
        while(j<repeat):
            fg = random.choices(bg_items)[0]
            imfg,fgboxes = getdata(fg)
            fgbox = random.choice(fgboxes)
            imfg_crop = crop_fgimg_box(imfg,fgbox)
            if imfg_crop is None:
                continue
            j+=1
            fg_h,fg_w,_ = imfg_crop.shape
            x1 = random.randint(0,max(w-fg_w,0))
            y1 = random.randint(0,max(h-fg_h,0))
            x2 = x1+fg_w
            y2 = y1+fg_h
            crop_im[y1:y2,x1:x2,:]=0.5*crop_im[y1:y2,x1:x2,:]+0.5*imfg_crop
            crop_xyxys.append([fgbox[0],x1,y1,x2,y2])
        
        dst_image_path = Path(dst)/"images"/f'{i}.png'
        dst_label_path = Path(dst)/"labels"/f'{i}.txt'
        dst_image_path.parent.mkdir(exist_ok=True,parents=True)
        dst_label_path.parent.mkdir(exist_ok=True,parents=True)
        cv2.imwrite(str(dst_image_path),crop_im)
        box_wh=[]
        for box in crop_xyxys:
            clss,x1,y1,x2,y2=box
            h,w,c = crop_im.shape
            xc,yc=(x1+x2)/2,(y1+y2)/2
            wc,hc = x2-x1,y2-y1
            box = [clss,xc/w,yc/h,wc/w,hc/h]
            box_wh.append(box)
        save_txt(dst_label_path,box_wh)
        
        prog.update()
        i+=1

