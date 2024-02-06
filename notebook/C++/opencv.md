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

## 数据格式

### Point_

```c++
template<typename _Tp> class Point_
//! dot product
_Tp dot(const Point_& pt) const;
//! dot product computed in double-precisionarithmetics
double ddot(const Point_& pt) const;
//! cross-product
double cross(const Point_& pt) const;
//! checks whether the point is inside thespecified rectangle
bool inside(const Rect_<_Tp>& r) const;
_Tp x; //!< x coordinate of the point
_Tp y; //!< y coordinate of the point


typedef Point_<int> Point2i;
typedef Point_<int64> Point2l;
typedef Point_<float> Point2f;
typedef Point_<double> Point2d;
typedef Point2i Point;
```

### Point3_

```c++
    template<typename _Tp> class Point3_
    //! dot product
    _Tp dot(const Point3_& pt) const;
    //! dot product computed in     double-precisionarithmetics
    double ddot(const Point3_& pt) const;
    //! cross product of the 2 3D points
    Point3_ cross(const Point3_& pt) const;
    _Tp x; //!< x coordinate of the 3D point
    _Tp y; //!< y coordinate of the 3D point
    _Tp z; //!< z coordinate of the 3D point

typedef Point3_<int> Point3i;
typedef Point3_<float> Point3f;
typedef Point3_<double> Point3d;
```

### Size_

```c++
    template<typename _Tp> class Size_
    //! the area (width*height)
    _Tp area() const;
    //! aspect ratio (width/height)
    double aspectRatio() const;
    //! true if empty
    bool empty() const;
    //! conversion of another data type.
    template<typename _Tp2> operator Size_<_Tp2>()const;
    _Tp width; //!< the width
    _Tp height; //!< the height

typedef Size_<int> Size2i;
typedef Size_<int64> Size2l;
typedef Size_<float> Size2f;
typedef Size_<double> Size2d;
typedef Size2i Size;
```

### Rect_

```c++
    template<typename _Tp> class Rect_
    //! the top-left corner
    Point_<_Tp> tl() const;
    //! the bottom-right corner
    Point_<_Tp> br() const;

    //! size (width, height) of the rectangle
    Size_<_Tp> size() const;
    //! area (width*height) of the rectangle
    _Tp area() const;
    //! true if empty
    bool empty() const;

    //! conversion to another data type
    template<typename _Tp2> operator Rect_<_Tp2>() const;

    //! checks whether the rectangle contains the point
    bool contains(const Point_<_Tp>& pt) const;

    _Tp x; //!< x coordinate of the top-left corner
    _Tp y; //!< y coordinate of the top-left corner
    _Tp width; //!< width of the rectangle
    _Tp height; //!< height of the rectangle

typedef Rect_<int> Rect2i;
typedef Rect_<float> Rect2f;
typedef Rect_<double> Rect2d;
typedef Rect2i Rect;
```

### RotatedRect

### Range


### matx
```c++
    template<typename _Tp, int m, int n> class Matx
    CV_NODISCARD_STD static Matx all(_Tp alpha);
    CV_NODISCARD_STD static Matx zeros();
    CV_NODISCARD_STD static Matx ones();
    CV_NODISCARD_STD static Matx eye();
    CV_NODISCARD_STD static Matx diag(const diag_type& d);
    /** @brief Generates uniformly distributed random numbers
    @param a Range boundary.
    @param b The other range boundary (boundaries don't have to be ordered, the lower boundary is inclusive,
    the upper one is exclusive).
     */
    CV_NODISCARD_STD static Matx randu(_Tp a, _Tp b);
    /** @brief Generates normally distributed random numbers
    @param a Mean value.
    @param b Standard deviation.
     */
    CV_NODISCARD_STD static Matx randn(_Tp a, _Tp b);

    //! dot product computed with the default precision
    _Tp dot(const Matx<_Tp, m, n>& v) const;

    //! dot product computed in double-precision arithmetics
    double ddot(const Matx<_Tp, m, n>& v) const;

    //! conversion to another data type
    template<typename T2> operator Matx<T2, m, n>() const;

    //! change the matrix shape
    template<int m1, int n1> Matx<_Tp, m1, n1> reshape() const;

    //! extract part of the matrix
    template<int m1, int n1> Matx<_Tp, m1, n1> get_minor(int base_row, int base_col) const;

    //! extract the matrix row
    Matx<_Tp, 1, n> row(int i) const;

    //! extract the matrix column
    Matx<_Tp, m, 1> col(int i) const;

    //! extract the matrix diagonal
    diag_type diag() const;

    //! transpose the matrix
    Matx<_Tp, n, m> t() const;

    //! invert the matrix
    Matx<_Tp, n, m> inv(int method=DECOMP_LU, bool *p_is_ok = NULL) const;

    //! solve linear system
    template<int l> Matx<_Tp, n, l> solve(const Matx<_Tp, m, l>& rhs, int flags=DECOMP_LU) const;
    Vec<_Tp, n> solve(const Vec<_Tp, m>& rhs, int method) const;

    //! multiply two matrices element-wise
    Matx<_Tp, m, n> mul(const Matx<_Tp, m, n>& a) const;

    //! divide two matrices element-wise
    Matx<_Tp, m, n> div(const Matx<_Tp, m, n>& a) const;

    //! element access
    const _Tp& operator ()(int row, int col) const;
    _Tp& operator ()(int row, int col);

    //! 1D element access
    const _Tp& operator ()(int i) const;
    _Tp& operator ()(int i);

    Matx(const Matx<_Tp, m, n>& a, const Matx<_Tp, m, n>& b, Matx_AddOp);
    Matx(const Matx<_Tp, m, n>& a, const Matx<_Tp, m, n>& b, Matx_SubOp);
    template<typename _T2> Matx(const Matx<_Tp, m, n>& a, _T2 alpha, Matx_ScaleOp);
    Matx(const Matx<_Tp, m, n>& a, const Matx<_Tp, m, n>& b, Matx_MulOp);
    Matx(const Matx<_Tp, m, n>& a, const Matx<_Tp, m, n>& b, Matx_DivOp);
    template<int l> Matx(const Matx<_Tp, m, l>& a, const Matx<_Tp, l, n>& b, Matx_MatMulOp);
    Matx(const Matx<_Tp, n, m>& a, Matx_TOp);

    _Tp val[m*n]; //< matrix elements
    ```
### Vec

```c++
    template<typename _Tp, int cn> class Vec : public Matx<_Tp, cn, 1>
        static Vec all(_Tp alpha);
    static Vec ones();
    static Vec randn(_Tp a, _Tp b);
    static Vec randu(_Tp a, _Tp b);
    static Vec zeros();
#ifdef CV_CXX11
    static Vec diag(_Tp alpha) = delete;
    static Vec eye() = delete;
#endif

    //! per-element multiplication
    Vec mul(const Vec<_Tp, cn>& v) const;

    //! conjugation (makes sense for complex numbers and quaternions)
    Vec conj() const;

    /*!
      cross product of the two 3D vectors.

      For other dimensionalities the exception is raised
    */
    Vec cross(const Vec& v) const;
    //! conversion to another data type
    template<typename T2> operator Vec<T2, cn>() const;

    /*! element access */
    const _Tp& operator [](int i) const;
    _Tp& operator[](int i);
    const _Tp& operator ()(int i) const;
    _Tp& operator ()(int i);

#ifdef CV_CXX11
    Vec<_Tp, cn>& operator=(const Vec<_Tp, cn>& rhs) = default;
#endif

    Vec(const Matx<_Tp, cn, 1>& a, const Matx<_Tp, cn, 1>& b, Matx_AddOp);
    Vec(const Matx<_Tp, cn, 1>& a, const Matx<_Tp, cn, 1>& b, Matx_SubOp);
    template<typename _T2> Vec(const Matx<_Tp, cn, 1>& a, _T2 alpha, Matx_ScaleOp);


typedef Vec<uchar, 2> Vec2b;
typedef Vec<uchar, 3> Vec3b;
typedef Vec<uchar, 4> Vec4b;

typedef Vec<short, 2> Vec2s;
typedef Vec<short, 3> Vec3s;
typedef Vec<short, 4> Vec4s;

typedef Vec<ushort, 2> Vec2w;
typedef Vec<ushort, 3> Vec3w;
typedef Vec<ushort, 4> Vec4w;

typedef Vec<int, 2> Vec2i;
typedef Vec<int, 3> Vec3i;
typedef Vec<int, 4> Vec4i;
typedef Vec<int, 6> Vec6i;
typedef Vec<int, 8> Vec8i;

typedef Vec<float, 2> Vec2f;
typedef Vec<float, 3> Vec3f;
typedef Vec<float, 4> Vec4f;
typedef Vec<float, 6> Vec6f;

typedef Vec<double, 2> Vec2d;
typedef Vec<double, 3> Vec3d;
typedef Vec<double, 4> Vec4d;
typedef Vec<double, 6> Vec6d;
```

### Scalar_

```c++
    template<typename _Tp> class Scalar_ : public Vec<_Tp, 4>
        //! returns a scalar with all elements set to v0
    static Scalar_<_Tp> all(_Tp v0);

    //! conversion to another data type
    template<typename T2> operator Scalar_<T2>() const;

    //! per-element product
    Scalar_<_Tp> mul(const Scalar_<_Tp>& a, double scale=1 ) const;

    //! returns (v0, -v1, -v2, -v3)
    Scalar_<_Tp> conj() const;

    //! returns true iff v1 == v2 == v3 == 0
    bool isReal() const;

typedef Scalar_<double> Scalar;
```

### KeyPoint

### Matx
