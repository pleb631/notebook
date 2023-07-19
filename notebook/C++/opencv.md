[TOC]

## 图像加载显示

见 [c1.cpp](cpp/c1.cpp)

### imread  
  
从文件加载图像。函数 imread 从指定文件加载图像并返回它。如果无法读取图像（由于缺少文件、权限不当、格式不受支持或无效），该函数将返回一个空矩阵 （ Mat：:d ata==NULL ）  

```c++
#include <opencv2/imgcodecs.hpp>
Mat cv::imread ( const String &  filename,
int  flags = IMREAD_COLOR 
)  

/*filename 要加载的文件的地址。
flags 可以采用 cv：：ImreadMode 值的标志：
IMREAD_UNCHANGED（<0）按原样加载图像（包括alpha通道（如果存在）
IMREAD_GRAYSCALE（0）将图像作为强度加载
IMREAD_COLOR（> 0）以RGB格式加载图像
```

python:`cv.imread( filename[, flags] ) -> retval`

### namedWindow

创建一个窗口。该窗口可用作图像和跟踪栏的占位符。创建的窗口由其名称引用。如果已存在同名窗口，则该函数不执行任何操作。可以调用 `cv:destroyWindow`或 `cv:destroyAllWindows` 来关闭窗口并取消分配任何关联的内存使用量。

```c++
#include <opencv2/highgui.hpp>
void cv::namedWindow ( const String &  winname,
int  flags = WINDOW_AUTOSIZE 
) 
/*winname 窗口标题中可用作窗口标识符的窗口名称。
flags 窗口的标志。支持的标志是：（cv：：WindowFlags)
WINDOW_NORMAL允许您调整窗口大小，
WINDOW_AUTOSIZE会自动调整窗口大小以适合显示的图像，并且无法手动更改窗口大小。

```

**存疑**，某些标志不起作用，比如`WINDOW_FREERATIO`和`WINDOW_KEEPRATIO`  
python:`cv.namedWindow( winname[, flags] ) -> None`

### imshow

在指定的窗口中显示图像。如果窗口是使用 cv：：WINDOW_AUTOSIZE 标志创建的，则图像将以其原始大小显示，但仍受屏幕分辨率的限制。否则，图像将缩放以适合窗口。该函数可能会缩放图像，具体取决于其深度：

- 如果映像为 8 位无符号，则按原样显示。
- 如果图像为 16 位无符号，则像素除以 256。也就是说，值范围 [0，255*256] 映射到 [0，255]。
- 如果图像是 32 位或 64 位浮点数，则像素值乘以 255。也就是说，值范围 [0，1] 映射到 [0，255]。
- 由于所需转换的模糊性，不再处理 32 位整数图像。使用特定于图像上下文的自定义预处理转换为 8 位无符号矩阵。
  
如果窗口不是在此函数之前创建的，则假定使用 `cv::WINDOW_AUTOSIZE` 创建一个窗口。
>注意
此函数后应调用 `cv::waitKey` 或 `cv::pollKey`，以执行实际显示给定图像并使窗口响应鼠标和键盘事件所必需的 GUI 内务处理任务。否则，它不会显示图像，并且窗口可能会锁定。例如，`waitKey（0）`将无限显示窗口，直到按下任何键（它适用于图像显示）。`waitKey（25）` 将显示一个帧并等待大约 25 毫秒的按键（适用于逐帧显示视频）。要删除窗口，使用 `cv::d estroyWindow`。

```c++
#include <opencv2/highgui.hpp>
void cv::imshow ( const String &  winname,
InputArray  mat 
) 
/*
winname 窗口的名称。
mat 要显示的图像。

```

python:`cv.imshow(winname, mat) ->None`

## 图像的修改

见 [c2.cpp](cpp/c2.cpp)

### cvtColor

该函数将输入图像从一个颜色空间转换为另一个颜色空间。在从 RGB 颜色空间转换的情况下，应明确指定通道的顺序（RGB 或 BGR）。请注意，OpenCV 中的默认颜色格式通常称为 RGB，但它实际上是 BGR（字节颠倒）。因此，标准（24 位）彩色图像中的第一个字节将是 8 位蓝色分量，第二个字节将是绿色，第三个字节将是红色。第四、第五和第六个字节将是第二个像素（蓝色，然后是绿色，然后是红色），依此类推。
RGB 通道值的常规范围为：

- 0 到 255 表示 CV_8U 图像
- 0 到 65535 表示 CV_16U 图像
- 0 到 1 表示CV_32F图像

```c++
#include <opencv2/imgproc.hpp>
void cv::cvtColor ( InputArray  src,
OutputArray  dst,
int  code,
int  dstCn = 0 
) 
/*
src 输入图像：8 位无符号、16 位无符号 （ CV_16UC... ） 或单精度浮点。
dst 输出与SRC相同大小和深度的图像。
code 色彩空间转换代码（请参见颜色转换代码）。
dstCn 目标图像中的通道数;如果参数为 0，则通道数自动从 SRC 和代码派生。

常见code有：
COLOR_BGR2BGRA ，COLOR_BGR2BGRA ，COLOR_HSV2RGB ，COLOR_Lab2RGB 
```

对于线性变换，范围无关紧要。但在非线性变换的情况下，应将输入RGB图像规范化到适当的值范围以获得正确的结果，例如，对于 `RGB→L*u*v*`变换。例如，如果您有一个直接从 32 位图像转换而没有任何缩放的 8 位浮点图像，那么它将具有 0..255 的值范围，而不是函数假定的 0..1。因此，在调用 `cvtColor` 之前，您首先需要缩小图像：

```c++
img *= 1./255;
cvtColor(img, img, COLOR_BGR2Luv);
```

python: `cv.cvtColor( src, code[, dst[, dstCn]] ) -> dst`

### imwrite

将图像保存到指定文件。图像格式是根据文件扩展名选择的

```c++
#include <opencv2/imgcodecs.hpp>
bool cv::imwrite ( const String &  filename,
InputArray  img,
const std::vector< int > &  params = std::vector< int >() 
) 
/*

filename 文件的名称。
img (垫子或垫子的矢量）图像或要保存的图像。
params 编码为对（paramId_1、paramValue_1、paramId_2、paramValue_2等）的特定于格式的参数，请参见 cv：：ImwriteFlags

```

Python:`cv.imwrite( filename, img[, params] ) -> retval`
