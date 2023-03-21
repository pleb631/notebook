# opencv

| 模块/方法 | 作用 | 备注 |
|---|---|---|
| cv2.imread(path，flag=1) | 读入path路径的图片 | cv.IMREAD_COLOR： 加载彩色图像。任何图像的透明度都会被忽视。它是默认标志。<br>cv.IMREAD_GRAYSCALE：以灰度模式加载图像  <br>cv.IMREAD_UNCHANGED：加载图像，包括alpha通道 <br>注意 除了这三个标志，你可以分别简单地传递整数1、0或-1。 读入后是BGR模式,<numpy.ndarray> |
| cv2.imwrite(path,img) | 保存图片 | 以BGR模式保存 |
| b,g,r = cv2.split(img) >>><br> img = cv2.merge((b,g,r)) | 拆分和合并通道 | 耗时，尽量用numpy索引 |
| cv2.copyMakeBorder(img,top，bottom，left，right,borderType,value) | 为图片填充边缘 | cv.BORDER_CONSTANT - 添加恒定的彩色边框。该值应作为下一个参数给出。<br>cv.BORDER_REFLECT - 边框将是边框元素的镜像，如下所示： <br>fedcba \| abcdefgh \| hgfedcb \|<br>cv.BORDER_REFLECT_101或 cv.BORDER_DEFAULT与上述相同，但略有变化，例如： gfedcb \| abcdefgh \| gfedcba \|<br>cv.BORDER_REPLICATE最后一个元素被复制，像这样： aaaaaa \| abcdefgh \| hhhhhhh \|<br>cv.BORDER_WRAP难以解释，它看起来像这样： cdefgh \| abcdefgh \| abcdefg \| value -边框的颜色，如果边框类型为cv.BORDER_CONSTANT |
| cv2.add(x,y) | 图像加法 |  |
| cv.addWeighted(x,0.7,y,0.3,0) | 图像融合 | 把x,y以0.7，0.3和gamma=0的偏移量相加 |
| cv2.cvtColor(img,flag) | 改变颜色空间 | flag有cv2.COLOR_BGR2RGB,cv2.COLOR_RGB2BGR，cv2.COLOR_BGR2GRAY |
| cv2.resize(img,Size,fx=0, fy=0,interpolation = INTER_LINEAR) | 改变图片尺寸 | 优先判断Size合不合法，如果不合法，则按fx，fy比例缩放 |
| cv2.bitwise_or(src, dst) ||
| cv2.bitwise_and(src, dst) ||
| cv2.bitwise_not(src) ||
| cv2.bitwise_xor(src, dst) ||
|cv2.convexHull([point])|凸包找到所有点的外轮廓||
|contours, hierarchy=cv2.findContours(image,mode,method)|轮廓检测|image：输入图像<br>mode：轮廓的模式。cv2.RETR_EXTERNAL只检测外轮廓；cv2.RETR_LIST检测的轮廓不建立等级关系；cv2.RETR_CCOMP建立两个等级的轮廓，上一层为外边界，内层为内孔的边界。如果内孔内还有连通物体，则这个物体的边界也在顶层；cv2.RETR_TREE建立一个等级树结构的轮廓。<br>method：轮廓的近似方法。cv2.CHAIN_APPROX_NOME存储所有的轮廓点，相邻的两个点的像素位置差不超过1；cv2.CHAIN_APPROX_SIMPLE压缩水平方向、垂直方向、对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需要4个点来保存轮廓信息；cv2.CHAIN_APPROX_TC89_L1，cv2.CV_CHAIN_APPROX_TC89_KCOS<br>contours：返回的轮廓<br>hierarchy：每条轮廓对应的属性<br>注意：cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），所以读取的图像要先转成灰度的，再转成二值图。
|cv2.drawContours|根据边界点绘制轮廓|
|cv2.minAreaRect(contour)|寻找最小外接矩形，带角度|
| cv2.contourArea(contour)|计算轮廓面积
|im = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)<br>cv2.imencode(".png", im)[1].tofile(save_img_path)|可以读入/写入汉字路径的文件|
