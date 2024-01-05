import cv2
from pathlib import Path
import tqdm


def save_txt(txt_path, info, mode='w'):
    '''保存txt文件

    Args:
        txt_path: str, txt文件路径
        info: list, txt文件内容
        mode: str, 'w'代表覆盖写；'a'代表追加写
    '''
    with open(txt_path, mode) as txt_file:
        for line in info:      
            txt_file.write(' '.join(list(map(str,line))) + '\n')
            
            
def slice(image,boxes,h_num,w_num):
    h,w,c=image.shape
    single_h = h//h_num
    single_w = w//w_num
    result = []
    for hi in range(h_num):
        for wi in range(w_num):
            x1 = wi*single_w
            y1 = hi*single_w
            x2 = (wi+1)*single_w if wi<w_num-1 else w
            y2 = (hi+1)*single_h if hi<h_num-1 else h
            current_image = image[y1:y2,x1:x2,:].copy()
            current_box = []
            for box in boxes:
                clss,bx1,by1,bx2,by2=box   

                if x2>(bx1+bx2)/2>x1 and y2>(by1+by2)/2>y1:
                    box_w = bx2-bx1
                    box_h = by2-by1
                    new_box = [clss,bx1-x1,by1-y1,bx2-x1,by2-y1]
                    new_box = list(map(lambda x: max(x,0),new_box))
                    new_box_w = new_box[3]-new_box[1]
                    new_box_h = new_box[4]-new_box[2]

                    if (new_box_w*new_box_h)/(box_w*box_h)>0.4:
                        current_box.append(new_box)
            result.append([current_image,current_box.copy()])
    return result
                        

if __name__=='__main__':
    root = '/root/dataset/val'
    dst = '/root/dataset/val_slice'
    items = list(Path(root).rglob('*.jpg'))
    for item in tqdm.tqdm(items):
        anno_path = item.parent.parent/"labels"/(item.with_suffix('.txt').name)
        txt_file = open(anno_path, "r", encoding="UTF-8")
        anno = [line.replace("\n", "") for line in txt_file]
        im = cv2.imread(str(item))
        h,w,c=im.shape
        boxes = []
        for i,line in enumerate(anno):
            line = list(map(float, line.split()))
            x1, y1 = line[1] - line[3] / 2, line[2] - line[4] / 2
            x2, y2 = x1 + line[3], y1 + line[4]
            box = [int(line[0]),int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h)]
            boxes.append(box)
        result = slice(im,boxes,1,4)
        for i,(image,boxes) in enumerate(result):
            dst_image_path = Path(dst)/(item.stem)/"images"/f'{i}.png'
            dst_label_path = Path(dst)/(item.stem)/"labels"/f'{i}.txt'
            dst_image_path.parent.mkdir(exist_ok=True,parents=True)
            dst_label_path.parent.mkdir(exist_ok=True,parents=True)
            cv2.imwrite(str(dst_image_path),image)
            box_wh=[]
            for box in boxes:
                clss,x1,y1,x2,y2=box
                h,w,c = image.shape
                xc,yc=(x1+x2)/2,(y1+y2)/2
                wc,hc = x2-x1,y2-y1
                box = [clss,xc/w,yc/h,wc/w,hc/h]
                box_wh.append(box)
            save_txt(dst_label_path,box_wh)
        
            
            

    