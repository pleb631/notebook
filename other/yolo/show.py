import cv2


path = '/root/dataset/train_fake/images/0.png'

im =cv2.imread(path)
label_path  = path.replace("images","labels").replace(".png",'.txt')
txt_file = open(label_path, "r", encoding="UTF-8")
anno = [line.replace("\n", "") for line in txt_file]
h,w,_=im.shape
for item in anno:
    clss,xc,yc,wc,hc=list(map(float,item.split()))
    x1,y1 = int((xc-wc/2)*w),int((yc-hc/2)*h)
    x2,y2 = int((xc+wc/2)*w),int((yc+hc/2)*h)
    cv2.rectangle(im,(x1, y1),(x2, y2),[255,0,0],3)
    cv2.imwrite("test.png",im)

