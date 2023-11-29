# 图像读入

## 基本

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

## bmp读入细节

bmp文件的头文件占14个字节，如果按照struct去构建

```c++
typedef struct tagBITMAPFILEHEADER {
	WORD    bfType;
	DWORD   bfSize;
	WORD    bfReserved1;
	WORD    bfReserved2;
	DWORD   bfOffBits;
} BITMAPFILEHEADER;
```

由于内存对齐原则，这个struct一共占16个字节！

所以在使用fread和fwrite的需要一个成员一个成员的进行读写而不能以struct为整体进行。可替代的方法就是使用预处理指令

```c++
#pragma pack(n)
```

可以指定struct的对齐系数为n，n必须是2的幂次方，例如1，2，4，8，16等。这样，结构体的每个成员的起始地址必须是n和该成员类型的大小中较小的那个数的整数倍，同时，结构体的总大小也必须是n和结构体中最大成员类型的大小中较小的那个数的整数倍。

头文件中biSizeImage并不等于h\*w\*3，因为bmp每一行像素的字节数需要内存对齐，比如w=313时，byte=313*3=919，不是4的倍数，所以在存储上每一行数据后会填补无用字节。在手动读取和写入的时候需要手动去填补。
