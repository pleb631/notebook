from matplotlib import pyplot as plt
import cv2
import numpy as np
import glob
import os

def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.
 
    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([mask.shape[-1], 4], dtype=np.int32)
    for i in range(mask.shape[-1]):
        m = mask[:, :, i]
        # Bounding box.
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            # x2 and y2 should not be part of the box. Increment by 1.
            x2 += 1
            y2 += 1
        else:
            # No mask for this instance. Might happen due to
            # resizing or cropping. Set bbox to zeros
            x1, x2, y1, y2 = 0, 0, 0, 0
        x1 = 0 if x1<0 else x1
        y1 = 0 if y1<0 else y1
        y2 = mask.shape[0] -1 if y2>=mask.shape[0] else y2
        x2 = mask.shape[1]-1 if x2 >= mask.shape[1] else x2
        boxes[i] = np.array([y1,x1,y2,x2])
    return boxes.astype(np.int32)

ratio=[1.3,1.3]
imgroot = r'C:\Users\admin\Downloads\Compressed\PennFudanPed\PennFudanPed\PNGImages\*.png'
gtroot = r'C:\Users\admin\Downloads\Compressed\PennFudanPed\PennFudanPed\PedMasks'
dst = r'C:\Users\admin\Downloads\Compressed\PennFudanPed\PennFudanPed\penn'
os.makedirs(os.path.join(dst,'img'),exist_ok=True)
os.makedirs(os.path.join(dst,'gt'),exist_ok=True)
for path in glob.glob(imgroot):
    
    file = os.path.basename(path)
    name = os.path.splitext(file)[0]
    sgt = os.path.join(gtroot,file.replace('.png','_mask.png'))

    gt = cv2.imread(sgt,1)
    img_h,img_w = gt.shape[:-1]
    img =cv2.imread(path,1)
    num = np.max(gt)
    for i in range(1,num+1):
        mask=(gt==i)
    #mask=mask[:,:,np.newaxis]
        box = extract_bboxes(mask)[0]  
        y1,x1,y2,x2 = box
        w = x2 -x1
        h = y2- y1
        new_w = max(4 * w, 3 * h) * 1.25 / 4
        new_h = max(4 * w, 3 * h) * 1.25 / 3
        new_w = w* ratio[1]
        new_h = h* ratio[0]
        xx1 = int(x1 - (new_w - w) // 2)
        yy1 = int(y1 - (new_h - h) // 2)
        xx2 = int(x2 + (new_w - w) // 2)
        yy2 = int(y2 + (new_h -  h) // 2)
        xx1 = min(max(xx1, 0), img_w)
        yy1 = min(max(yy1, 0), img_h)
        xx2 = min(max(xx2, 0), img_w)
        yy2 = min(max(yy2, 0), img_h)
        sub_im = img[yy1:yy2,xx1:xx2,:]
        sub_gt = mask[yy1:yy2,xx1:xx2]
        sub_gt[sub_gt>0.5]=1
        dim = os.path.join(dst,"img",str(name)+"_"+str(i)+".jpg")
        dgt = os.path.join(dst,"gt",str(name)+"_"+str(i)+".png")
        cv2.imwrite(dim,sub_im)
        cv2.imwrite(dgt,sub_gt)


