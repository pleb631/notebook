## 0.开始之前

```bash
$ cmake --version
cmake version 3.23.5
```

CMake 是一个配置程序，CMake 不负责运行生成软件构建的命令。相反,而是根据项目、环境和用户提供的配置信息生成一个构建系统。

CMake 支持将多个构建系统作为此配置过程的输出。这些输出后端被称为“生成器”，因为它们生成构建系统。CMake 支持许多生成器.其文档可以在 [`cmake-generators(7)`](https://cmake.com.cn/cmake/help/latest/manual/cmake-generators.7.html#manual:cmake-generators(7)) 中找到

基础用法：

- [`cmake -S `](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-S)

  指定项目根目录，CMake 将在此找到要构建的项目。它包含教程第 1 步将要讨论的根 `CMakeLists.txt` 文件。如果未指定，则默认为当前工作目录。

- [`cmake -B `](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-B)

  指定构建目录，CMake 将在此输出生成的构建系统的文件，以及在运行构建系统时构建本身的工件。如果未指定，则默认为当前工作目录。

- [`cmake --build `](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-build)

  在指定的构建目录中运行构建系统。这是所有生成器的通用命令。对于多配置生成器，可以通过以下方式请求所需的配置：`cmake --build <dir> --config <cfg>`

范例代码：

```cmake
#CMakeLists.txt
cmake_minimum_required(VERSION 3.16.3)

project(Tutorial)

add_executable(hello)
target_sources(hello
  PRIVATE
    HelloWorld.cxx
)

```

```cpp
//HelloWorld.cxx
#include <cstdio>

int main()
{
  std::printf("Hello World\n");
}

```



## 1.CMake 入门

CMake 的典型用法围绕一个或多个名为 `CMakeLists.txt` （CML）的文件。`CMakeLists.txt` 为 CMake 提供有关如何处理该目录或子目录中的本地文件和操作的说明的任何目录中。

CML 应始终在文件顶部包含以下命令

```cmake
#  CMake最低版本
cmake_minimum_required(VERSION 3.23)
# 工程名称
project(MyProjectName)
```

### 1.1 构建可执行文件

使用[add_executable(<name> ...)](https://cmake.com.cn/cmake/help/latest/command/add_executable.html#id1)指定目标名称，这个和`project()`不同，这个会指定生成的文件名称。



接下来使用[`target_sources()`](https://cmake.com.cn/cmake/help/latest/command/target_sources.html#command:target_sources)为目标关联属性，比如构建和链接的源文件

每个文件集合都以一个[作用域关键字](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#target-command-scope)为前缀。通常，没有什么依赖于可执行文件。其他程序和库不需要链接到可执行文件，也不需要继承头文件或其他类似的东西。因此，最适合在此处使用的作用域是 `PRIVATE`，它通知 CMake 此属性仅属于 `MyProgram` 且不可继承。这条规则几乎在所有地方都适用。

### 1.2 构建库

要构建库，我们只需要引入一个命令：[`add_library()`](https://cmake.com.cn/cmake/help/latest/command/add_library.html#command:add_library)。它的工作方式与 [`add_executable()`](https://cmake.com.cn/cmake/help/latest/command/add_executable.html#command:add_executable) 完全相同

```cmake
add_library(MathFunctions)
target_sources(MathFunctions
  PRIVATE
    MathFunctions/MathFunctions.cxx
  PUBLIC
    MathFunctions/MathFunctions.h
)
```

我们将实现文件作为 `PRIVATE` 源，这与之前用于可执行文件的文件相同。但是，我们现在对头文件使用了 `PUBLIC`。这允许库的消费者“看到”库的头文件

### 1.3 链接库和可执行文件

要把库和可执行文件结合在一起，可引入

```cmake
target_link_libraries(MyProgram
  PRIVATE
    MyLibrary
)
```

[作用域关键字](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#target-command-scope) 有三个：`PRIVATE`、`INTERFACE` 和 `PUBLIC`。它们描述了属性如何提供给目标。

- `PRIVATE` 属性（仅可供拥有它的目标使用，例如 `PRIVATE` 头文件将仅对附加到它们的目标可见。
- 一个 `INTERFACE` 属性仅对*链接*拥有目标的那些目标可用。拥有目标本身无法访问这些属性。一个仅限头文件的库是 `INTERFACE` 属性集合的一个例子，因为仅限头文件的库本身不构建任何内容，也不需要访问自己的文件。
- `PUBLIC` 不是一种独立的属性类型，而是 `PRIVATE` 和 `INTERFACE` 属性的并集。因此，使用 `PUBLIC` 描述的需求对于拥有目标和消费目标都可用。

但在引入外部库，可能要给可执行文件额外增加include目录，不然找不到头文件

```cmake
target_include_directories(Tutorial
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/MathFunctions
    ${CMAKE_CURRENT_SOURCE_DIR}
)
```

### 1.4子目录

命令 [`add_subdirectory()`](https://cmake.com.cn/cmake/help/latest/command/add_subdirectory.html#command:add_subdirectory) 允许我们包含位于项目子目录中的 CML

```cmake
add_subdirectory(SubdirectoryName)
```

当子目录中的 `CMakeLists.txt` 被 CMake 处理时，子目录 CML 中描述的所有相对路径都相对于该子目录，而不是顶层 CML。





## 2.CMake 语言基础

`set()`命令创建一个变量

```cmake
set(var "World!")
message("Hello ${var}")
```

```bash
$ cmake -P CMakeLists.txt # -P 脚本模式
# Hello World!
```

CMakeLang 只有字符串，条件判断完全依赖于约定。“True”、“On”、“Yes”以及（代表）非零数字的字符串是 truthy。而“False”、“Off”、“No”、“0”、“Ignore”、“NotFound”以及空字符串都被认为是 false



`list`是包含分号的字符串,使用`foreach`命令来迭代列表

```cmake
set(stooges "Moe;Larry")
list(APPEND stooges "Curly")

message("Stooges contains: ${stooges}")

foreach(stooge IN LISTS stooges)
  message("Hello, ${stooge}")
endforeach()
```

```bash
$cmake -P CMakeLists.txt
# Stooges contains: Moe;Larry;Curly
# Hello, Moe
# Hello, Larry
# Hello, Curly
```



函数和宏

```cmake
macro(MyMacro MacroArgument)
  message("${MacroArgument}\n\t\tFrom Macro")
endmacro()

function(MyFunc FuncArgument)
  MyMacro("${FuncArgument}\n\tFrom Function")
endfunction()

MyFunc("From TopLevel")
```

[`function()`](https://cmake.com.cn/cmake/help/latest/command/function.html#command:function) 会创建自己的变量作用域，因此副作用对调用者不可见。为了将更改传播给调用函数的父级，我们必须使用 `set(<var> <value> PARENT_SCOPE)`，这与 [`set()`](https://cmake.com.cn/cmake/help/latest/command/set.html#command:set) 的工作方式相同，但作用于调用者上下文中的变量。





条件判断

```cmake
if(True)
  message("Constant Value: True")
else()
  message("Constant Value: False")
endif()
```

[`if()`](https://cmake.com.cn/cmake/help/latest/command/if.html#command:if) 提供了几种有用的比较模式，例如用于字符串匹配的 `STREQUAL`，用于检查变量是否存在的 `DEFINED`，以及用于正则表达式检查的 `MATCHES`。它还支持典型的逻辑运算符：`NOT`、`AND` 和 `OR`



CMake 还提供了两种循环结构：`while`和`foreach`

## 3.配置和缓存变量

CMake 有多种方式可以让调用者传达这些配置选择，但其中最基本的是 [`-D`](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-D) 标志

```cmake
if(COMPRESSION_SOFTWARE_USE_ZLIB)
  message("I will use Zlib!")
  # ...
endif()

if(COMPRESSION_SOFTWARE_USE_ZSTD)
  message("I will use Zstd!")
  # ...
endif()
```

```bash
$cmake -B build \
    -DCOMPRESSION_SOFTWARE_USE_ZLIB=ON \
    -DCOMPRESSION_SOFTWARE_USE_ZSTD=OFF
...
# I will use Zlib!
```

可以给配置选择提供默认值，此功能由 [`option()`](https://cmake.com.cn/cmake/help/latest/command/option.html#command:option) 

```bash
option(COMPRESSION_SOFTWARE_USE_ZLIB "Support Zlib compression" ON)
option(COMPRESSION_SOFTWARE_USE_ZSTD "Support Zstd compression" ON)

if(COMPRESSION_SOFTWARE_USE_ZLIB)
  # Same as before
# ...
```

[`-D`](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-D) 标志和 [`option()`](https://cmake.com.cn/cmake/help/latest/command/option.html#command:option) 创建的名称不是普通变量,而是缓存变量。缓存变量是全局可见的、*粘性* 的变量，其值在首次设置后很难更改。



[`set()`](https://cmake.com.cn/cmake/help/latest/command/set.html#command:set) 也可以用来操作缓存变量，但不会更改已创建的变量

```cmake
set(StickyCacheVariable "I will not change" CACHE STRING "")
set(StickyCacheVariable "Overwrite StickyCache" CACHE STRING "")

message("StickyCacheVariable: ${StickyCacheVariable}")
# StickyCacheVariable: I will not change
```

缓存变量通常不能更改，但可以被普通变量 *覆盖*。我们可以通过设置一个与缓存变量同名的变量，然后使用 [`set()`](https://cmake.com.cn/cmake/help/latest/command/set.html#command:set) 来设置一个普通变量，然后使用 [`unset()`](https://cmake.com.cn/cmake/help/latest/command/unset.html#command:unset) 删除普通变量来观察这一点。

```cmake
set(ShadowVariable "In the shadows" CACHE STRING "")
set(ShadowVariable "Hiding the cache variable")
message("ShadowVariable: ${ShadowVariable}")

unset(ShadowVariable)
message("ShadowVariable: ${ShadowVariable}")

# ShadowVariable: Hiding the cache variable
# ShadowVariable: In the shadows
```

## 4.cmake命令

有陷阱：

头文件目录：

[`target_include_directories()`](https://cmake.com.cn/cmake/help/latest/command/target_include_directories.html#command:target_include_directories)

链接文件目录

[`target_link_directories()`](https://cmake.com.cn/cmake/help/latest/command/target_link_directories.html#command:target_link_directories)

常用：

源文件地址

[`target_sources()`](https://cmake.com.cn/cmake/help/latest/command/target_sources.html#command:target_sources)

链接文件地址

[`target_link_libraries()`](https://cmake.com.cn/cmake/help/latest/command/target_link_libraries.html#command:target_link_libraries)

添加预处理器宏定义

[`target_compile_definitions()`](https://cmake.com.cn/cmake/help/latest/command/target_compile_definitions.html#command:target_compile_definitions)

```cmake
target_compile_definitions(MyLibrary
  PRIVATE
    MYLIBRARY_USE_EXPERIMENTAL_IMPLEMENTATION

  PUBLIC
    MYLIBRARY_EXCLUDE_DEPRECATED_FUNCTIONS
)
```

通过宏定义决定函数如何运行
```c++
double sqrt(double x)
{
#ifdef TUTORIAL_USE_STD_SQRT
  return std::sqrt(x);
#else
  return mysqrt(x);
#endif
}
```



设置编译需要用的版本特性

[`target_compile_features()`](https://cmake.com.cn/cmake/help/latest/command/target_compile_features.html#command:target_compile_features)

```cmake
target_compile_features(MyApp PRIVATE cxx_std_20)
```



高级：

[`target_compile_options()`](https://cmake.com.cn/cmake/help/latest/command/target_compile_options.html#command:target_compile_options)

```cmake

if(
  (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC") OR
  (CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
)
  target_compile_options(Tutorial PRIVATE /W3)
elseif(
  (CMAKE_CXX_COMPILER_ID STREQUAL "GNU") OR
  (CMAKE_CXX_COMPILER_ID MATCHES "Clang")
)
  target_compile_options(Tutorial PRIVATE -Wall)
endif()
```



## 5.库概念

[`add_library()`](https://cmake.com.cn/cmake/help/latest/command/add_library.html#command:add_library) 命令接受要创建的库目标的名称作为其第一个参数。第二个参数是一个可选的 `<type>`，其有效值为：

> - `STATIC`
>
>    [静态库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#static-libraries)：一个用于链接其他目标的归档文件。
>
> - `SHARED`
>
>    [共享库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#shared-libraries)：一个动态库，可以被其他目标链接并在运行时加载。
>
> - `INTERFACE`
>
>   一个 [接口库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#interface-libraries)：一个库目标，它为依赖项指定使用要求，但不编译源文件，也不在磁盘上生成库文件。

### 5.1静态库和共享库

虽然 [`add_library()`](https://cmake.com.cn/cmake/help/latest/command/add_library.html#command:add_library) 命令支持显式设置 `STATIC` 或 `SHARED`，

当未指定类型时，创建 `STATIC` 或 `SHARED` 库，具体取决于 [`BUILD_SHARED_LIBS`](https://cmake.com.cn/cmake/help/latest/variable/BUILD_SHARED_LIBS.html#variable:BUILD_SHARED_LIBS) 的值。如果 [`BUILD_SHARED_LIBS`](https://cmake.com.cn/cmake/help/latest/variable/BUILD_SHARED_LIBS.html#variable:BUILD_SHARED_LIBS) 为 true，将创建一个 `SHARED` 库，否则将创建 `STATIC` 库。一般最好将第二个参数留空，以便大多数“普通”库可以作为两者使用

```cmake
add_library(MyLib-static STATIC)
add_library(MyLib-shared SHARED)

# Depends on BUILD_SHARED_LIBS
add_library(MyLib)
```

```bash
cmake --preset tutorial -DBUILD_SHARED_LIBS=ON
# 只构建MathFunctions
cmake --build build -t MathFunctions
```

### 5.2接口库

接口库是指仅为其他目标通信使用要求，自身不构建或生成任何文件的库。因此，接口库的所有属性本身都必须是接口属性，使用 `INTERFACE`

```cmake
add_library(MyInterface INTERFACE)
target_compile_definitions(MyInterface INTERFACE MYINTERFACE_COMPILE_DEF)
```

C++ 开发中最常见的接口库类型是仅头文件库。此类库不构建任何内容，只提供发现其头文件所需的标志。

### 5.3对象库

```cmake
add_library(MyObjects OBJECT)
```

对象库的一个常见用例是将几个库目标合并到一个存档或共享库对象中。即使在单个项目中，由于各种原因（例如属于组织内的不同团队），库也可能被维护为不同的目标。但是，将它们分发为单个面向消费者的二进制文件可能是可取的。对象库使这成为可能。