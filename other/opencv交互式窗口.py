import cv2
import copy
class EventCv():
    def __init__(self,image=None):
        self.image = image
        self.add_mouse_event('input images')
        self.plotparam=[]

    def update_image(self, image):
        self.image = image

    def callback_print_image(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("(x,y)=({},{}),data={}".format(x, y, self.image[y][x]))
            cv2.circle(self.image, [x,y],thickness=5, color=[0,255,255],radius=5)
            self.show()

    def add_mouse_event(self, winname, param=None, callbackFunc=None):
        '''
         添加点击事件
        :param winname:
        :param param:
        :param callbackFunc:
        :return:
        '''
        cv2.namedWindow(winname,cv2.WINDOW_NORMAL) ## cv2.WINDOW_AUTOSIZE		不可调窗口大小;cv2.WINDOW_NORMAL		可调整窗口大小
        if callbackFunc is None:
            callbackFunc = self.callback_print_image
        cv2.setMouseCallback(winname, callbackFunc, param=param)
    
    def show(self):
        copy_img = copy.copy(self.image)
        copy_img = self.plot(copy_img)
        cv2.imshow('input images', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def plot(self,img):
        return img

        


im = cv2.imread(r'C:\Users\admin\Pictures\Frostpunk\Screen_04-06-2022_21-26-27.png')
m=EventCv(im)
m.show()


