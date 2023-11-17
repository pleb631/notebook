# 图像读入

常见的图片都是通过高效的压缩算法制作成的。如果用以下方式读入图像，data就是连续的16进制数，因为2个16进制数才是8字节，所以data的长度就是该文件存储的字节数，np.frombuffer可以把16进制数转为10进制数，比如‘\xff’转为255。

这些数据中不仅包含了图片内容，也包含了图片的基本信息和压缩算法相关的信息。cv2.imdecode会自动寻找压缩算法的相关标志，并分配不同解码算法从而得到图片数据。

```python
file = r'9.jpeg'
with open(file,'rb') as f:
 data=f.read()
data1 = np.frombuffer(data, np.uint8)
data2 = np.fromfile(file,dtype=np.uint8) #data1和dat2等价
im1 = cv2.imdecode(data2,cv2.IMREAD_COLOR)
im2 = cv2.imread(file,cv2.IMREAD_COLOR) #im1和im2等价
##a3 = io.BytesIO(data2.tobytes()).getvalue()  a3与data等价
```

stb_image和opencv解码图片并存储在内存的格式如图所示，对于图片的每一行像素，channel会进行展开按照格式进行存放，opencv的存储格式是[B,G,R,B,G,R...], stb_image的存储格式是RGB。
![2023-11-15-16-22-43](https://cdn.jsdelivr.net/gh/pleb631/ImgManager@main/img/2023-11-15-16-22-43.png)

以下是stb_image转换opencv的代码,需要注意的是img的存储格式仍然是RGB

```c++
std::string filename = "9.jpeg";

int x,y,n;
unsigned char *data = stbi_load(filename.c_str(), &x, &y, &n, 0);
cout << "x: " << x << endl << "y: " << y << endl << "n: " << n << endl;
cv::Mat img = cv::Mat(y,x, CV_8UC3, data, x * 3);
```
