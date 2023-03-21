import tkinter as tk
from PIL import ImageTk, Image
import cv2 
import numpy as np
import os
from functools import partial
import time
import pickle
import  argparse
import glob
from encrypt import Encrypt
from pathlib import Path
from io import BytesIO



def read_pkl(pkl_path):
    '''读取txt文件

    Args:
        pkl_path: str, pickle文件路径

    Returns:
        pkl_data: list, txt文件内容
    '''
    with open(pkl_path, 'rb') as pkl_file:
        pkl_data = pickle.load(pkl_file)

    return pkl_data


class markf():
    def __init__(self,args):
        self.args=args
        self.img_root = args.dataset_folder
        self.imglist = sorted(glob.glob(self.img_root+'\**\*.jpg',recursive=True))
        self.root = tk.Tk()
        #self.checkpoint_path = os.path.join(args.dataset_folder,'.checkpoint')
        self.enable_encrypt  = args.encrypt
        if self.enable_encrypt:
            self.encrypt = Encrypt("$xzyalg$")
        
        tk.Button(self.root, text="正面", command=partial(self.recode, 0)).grid(row=2, sticky="w")
        tk.Button(self.root, text="侧面", command=partial(self.recode, -1)).grid(row=3, sticky="w")
        tk.Button(self.root, text="反面", command=partial(self.recode, 1)).grid(row=4, sticky="w")
        tk.Button(self.root, text="前一张", command=partial(self.change_img, -1)).grid(row=5,column=2, sticky="w")
        tk.Button(self.root, text="后一张", command=partial(self.change_img, 1)).grid(row=5,column=3, sticky="w")
        self.b=tk.Button(self.root, text="保存", command=self.save_anno)
        self.b.grid(row=3,column=4, sticky="w")
        self.cache={}
        self.imgnum = len(self.imglist)
        self.pointer = 0
        self.labeled_num = 0
        
        self.la1=tk.Label(self.root,text=f'标注数量:{self.labeled_num}/{self.imgnum}')
        self.la1.grid(row=0,column=2, sticky="w")
        self.la2=tk.Label(self.root,text=f'当前位置:{self.pointer}/{self.imgnum}')
        self.la2.grid(row=0,column=3, sticky="w")

        
        self.start()
        
    def show_img(self,draw=False):
        
        
        if not self.enable_encrypt:
            img = cv2.imdecode(np.fromfile(self.CurImPath, dtype=np.uint8), -1)
        else:
            data = Path(self.CurImPath).read_bytes()
            image_data = self.encrypt.decrypt(data)
            file = BytesIO(image_data)
            img = cv2.imdecode(np.asarray(bytearray(file.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
        if draw:
            img = self.draw(img)
        self.photo = ImageTk.PhotoImage(Image.fromarray(img[:,:,::-1]).resize((512,512)))
        image_Label = tk.Label(self.root, image=self.photo)
        image_Label.grid(row=2, column=2, rowspan=3, columnspan=2,padx='4px', pady='5px')
        
    
    def draw(self,img):
        key = self.imglist[self.pointer].replace(self.img_root,'')
        if key not in self.cache:
            return img
        
        text = self.cache[key]
        if text==0:
            text='front'
        elif text==1:
            text='back'
        elif text==-1:
            text='side'
        img = cv2.putText(img, str(text), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0),3)

        return img
        
    def recode(self,CLS):
        
        self.process_cls(CLS)
        self.get_next_img()
        self.show_img()
        
    def process_cls(self,CLS,key=None):
        if key==None:
            key = self.CurImPath.replace(self.img_root,'')
        if key not in self.cache:
            self.labeled_num+=1
            self.update_tk(labeled_num=True)
        self.cache[key]=CLS
        return

        
    def change_img(self,tar):
        if tar==-1:
            if self.pointer==0:
                return 0
            self.pointer-=1
        elif tar ==1:
            if self.pointer==(self.imgnum-1):
                return 0
            self.pointer+=1
        self.update_tk(pointer=True)
            
            
        self.CurImPath = self.imglist[self.pointer]
        self.show_img(draw=True)
            
    def start(self,):
        self.read_anno()
        self.CurImPath = self.imglist[self.pointer]
        self.show_img(True)
        self.root.mainloop()
    
    
    def get_next_img(self,):
        self.change_img(tar=1)
        self.CurImPath = self.imglist[self.pointer]
        
        
    def write_checkpoint(self, checkpoint_path):
        if not os.path.exists(os.path.dirname(checkpoint_path)):
            os.makedirs(os.path.dirname(checkpoint_path))
        checkpoint_file = open(checkpoint_path, "w")
        checkpoint_file.writelines('||'.join([str(self.pointer),self.imglist[self.pointer].replace(self.img_root,''),str(self.labeled_num)]))

    def read_checkpoint(self, checkpoint_path):
        if not os.path.exists(checkpoint_path):
            return -1
        checkpoint_file = open(checkpoint_path, "r")
        content = checkpoint_file.readline().strip()
        checkpoint_file.close()
        pointer,key,labeled_num = content.split('||')
        if self.imglist[int(pointer)].replace(self.img_root,'') == key:
            self.pointer = int(pointer)
            self.labeled_num=int(labeled_num)
            self.update_tk(pointer=True,labeled_num=True)
        else:
            return
        
    def save_anno(self,):
        outname = str(int(time.time()))
        self.write_checkpoint(os.path.join(self.img_root,'result', outname+'.checkpoint'))

        self.b['text']="保存中,请勿关闭程序"
        
        with open(os.path.join(self.img_root,'result', outname+'.pkl'), 'wb') as f:
            pickle.dump(self.cache, f)
        self.b['text']="保存"
        
    
    def read_anno(self,):
        
        
        if not os.path.exists(os.path.join(self.img_root,'result')):
            return
        timelist = os.listdir(os.path.join(self.img_root,'result'))
        if len(timelist)==0:
            return
        maxtime = str(max([int(f.split('.')[0]) for f in timelist]))
        
        self.cache = read_pkl(os.path.join(self.img_root,'result',maxtime+'.pkl'))
        print(f"read checkpoint {os.path.join(self.img_root,'result',maxtime+'.checkpoint')}")
        self.read_checkpoint(os.path.join(self.img_root,'result',maxtime+'.checkpoint'))
    
    
    def update_tk(self,pointer=False,labeled_num=False):
        if pointer:
            self.la2['text']=f'当前位置:{self.pointer+1}/{self.imgnum}'
        if labeled_num:
            self.la1['text']=f'标注数量:{self.labeled_num}/{self.imgnum}'
            
     
     
     

    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_folder", type=str, help="the path of reviewed images",default=r'D:\dml\Veri_mark\code\back')
    parser.add_argument("--task", type=str, default="pedestrain", help="task name")
    parser.add_argument("--encrypt", action="store_true", help="whether to encrypt")
    parser.add_argument("--scale", action="store_true", help="whether to show original images")
    args = parser.parse_args()
    markf(args)


if __name__ == '__main__':
    main()