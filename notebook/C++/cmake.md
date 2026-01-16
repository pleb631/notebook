## 1.cmake

### 1.1 基本用法

CMake 是一个配置程序，CMake 不负责运行生成软件构建的命令。相反,而是根据项目、环境和用户提供的配置信息生成一个构建系统。

```cmake
# 1
cmake -B <path-to-build> [-S <path-to-source>]
```

将 `<path-to-build>` 用作构建树，将 `<path-to-source>` 用作源目录。指定的路径可以是绝对路径，也可以是相对于当前工作目录的相对路径。源目录必须包含 `CMakeLists.txt` 文件。如果构建目录不存在，则会自动创建

```cmake
# 2
cmake <path-to-source>
```

将当前工作目录用作构建树，将 `<path-to-source>` 用作源目录

### 1.2其他选项

| 选项                             | 功能                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `-S <path-to-source>`            | 要构建的项目的根目录                                         |
| **-B** <path-to-build>           | 用作构建目录的根目录                                         |
| **-D** <var>=<value>             | 设置变量                                                     |
| **--install-prefix** <directory> | 指定安装目录，由 CMAKE_INSTALL_PREFIX` 变量使用。必须是绝对路径 |
| **--preset** <preset>            | 从 `CMakePresets.json` 和 `CMakeUserPresets.json` 文件中读取一个 [`preset`](https://cmake.com.cn/cmake/help/latest/manual/cmake-presets.7.html#manual:cmake-presets(7)) |
| **-P**                           | 脚本模式                                                     |
| `--build`                        | `cmake --build ./build -j4`编译目录                          |

## 2.基本构建

CMake 的典型用法围绕一个或多个名为 `CMakeLists.txt` （CML）的文件。`CMakeLists.txt` 为 CMake 提供有关如何处理该目录或子目录中的本地文件和操作的说明的任何目录中。

CML 应始终在文件顶部包含以下命令

```cmake
#  CMake最低版本
cmake_minimum_required(VERSION 3.23)
# 工程名称
project(MyProjectName)
```

### 2.1构建可执行文件

使用`add_executable(<name> ...)`指定目标名称，这个和`project()`不同，这个会决定生成的文件名称。

使用`target_sources()`为目标关联属性，比如构建和链接的源文件

```cmake
cmake_minimum_required(VERSION 3.23)
project(MyProjectName)

add_executable(main)
target_sources(main
private
main.cpp
)
```

### 2.2链接权限

在CMake中，链接权限决定了库在何时被链接到目标上。主要有三种权限：

- **PRIVATE** (私有): 当目标自身需要此链接库时使用。
- **PUBLIC** (公共): 当目标自身或其他目标链接了这个目标时使用。
- **INTERFACE** (接口): 当目标自身不需要此链接库，但其他目标链接了这个目标时使用。

```cmake
# demo
target_link_libraries(target PRIVATE lib1)
target_link_libraries(target PUBLIC lib2)
target_link_libraries(target INTERFACE lib3)
```

1.**PRIVATE**

当我们说一个库是以`PRIVATE`方式链接的，我们意味着这个库只对当前目标有意义，而不会被传递给其他链接了此目标的目标。

假设我们正在构建一个项目，其中有一个静态库`libA`和一个可执行文件`exeB`。`libA`需要一个第三方库`libThirdParty`来完成某些功能，但这个功能只在`libA`内部使用，`exeB`并不直接依赖于它。

在这种情况下，我们应该使用`PRIVATE`权限来链接`libThirdParty`到`libA`，因为`exeB`不需要知道或链接到`libThirdParty`。

```cmake
target_link_libraries(libA PRIVATE libThirdParty)
```



2.**PUBLIC**

当我们声明一个库为`PUBLIC`依赖时，不仅当前目标可以访问该库，而且任何链接到当前目标的其他目标也可以访问它。

考虑一个常见的场景：你正在开发一个库，这个库依赖于其他几个库。当其他项目使用你的库时，它们也需要这些依赖。在这种情况下，使用`PUBLIC`权限可以确保这些依赖被正确地传递。

例如，你有一个数学库`math_lib`，它依赖于`matrix_lib`和`vector_lib`。当其他项目使用`math_lib`时，它们也需要`matrix_lib`和`vector_lib`。

这样，任何链接到`math_lib`的项目都会自动获得对`matrix_lib`和`vector_lib`的访问权限。

```cmake
target_link_libraries(math_lib PUBLIC matrix_lib vector_lib)
```



3.**INTERFACE**

考虑一个常见的场景：你有一个只包含头文件的库，例如模板库。这个库本身并不生成任何二进制文件，但它可能有一些公共头文件，需要被其他库或应用程序所知道。

```cmake
add_library(header_only_lib INTERFACE)
target_include_directories(header_only_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
```

2.3 构建库

要构建库，需要引入一个命令：`add_library()`。它的工作方式与 [`add_executable()`](https://cmake.com.cn/cmake/help/latest/command/add_executable.html#command:add_executable) 完全相同

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



如果源文件涉及模板类和内联函数，如下。则源文件需要使用 `PUBLIC`

```cmake
// MathFunctions.h
#pragma once

template <typename T>
class MathFunctions {
public:
    T add(T a, T b);
};

// MathFunctions.cpp
#include "MathFunctions.h"

template <typename T>
T MathFunctions<T>::add(T a, T b) {
    return a + b;
}
```

### 2.3链接库和可执行文件

要把库和可执行文件结合在一起，可引入

```cmake
target_link_libraries(MyProgram
  PRIVATE
    MyLibrary
)
```

在引入外部库，可能要给可执行文件额外增加include目录，不然找不到头文件

```cmake
target_include_directories(Tutorial
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/MathFunctions
    ${CMAKE_CURRENT_SOURCE_DIR}
)
```

### 2.4子目录

命令 `add_subdirectory()` 允许我们包含位于项目子目录中的 CML

```cmake
add_subdirectory(SubdirectoryName)
```

当子目录中的 `CMakeLists.txt` 被 CMake 处理时，子目录 CML 中描述的所有相对路径都相对于该子目录，而不是顶层 CML。

## 3.语言基础

`set()`命令创建一个变量

```cmake
set(var "World!")
message("Hello ${var}")
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

## 4.常用变量和命令

### 4.1变量

|                            | 介绍                                                         | 使用                                    |
| -------------------------- | ------------------------------------------------------------ | --------------------------------------- |
| `CMAKE_INSTALL_PREFIX`     | install目录                                                  | `set(CMAKE_INSTALL_PREFIX "/path/to/")` |
| `PROJECT_SOURCE_DIR`       | 当前的工程目录                                               |                                         |
| `CMAKE_BUILD_TYEP`         | cmake 中的编译选项，默认为空，相当于debug 模式，详情见[5.编译选项](##5.编译选项) | `set(CMAKE_BUILD_TYEP Release)`         |
| `CMAKE_CXX_STANDARD`       | 设置C++ 的编译标准                                           | `set(CMAKE_CXX_STANDARD 11)`            |
| `BUILD_SHARED_LIBS`        | 设置生成库的类型，默认False:静态库,True为动态库              | set(BUILD_SHARED_LIBS  on)              |
| `CMAKE_CURRENT_SOURCE_DIR` | 即跟主CMakeList.txt 的同一级目录                             |                                         |
|                            |                                                              |                                         |
|                            |                                                              |                                         |

### 4.2命令

#### 4.2.1列表

|                                                              | 介绍                                                         | 使用                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `target_include_directories()`                               | 头文件目录                                                   |                                                              |
| `target_link_directories()`                                  | 链接文件目录                                                 |                                                              |
| `target_sources()`                                           | 源文件地址                                                   |                                                              |
| `target_link_libraries()`                                    | 链接文件地址                                                 |                                                              |
| `target_compile_definitions()`                               | 添加预处理器宏定义                                           | `target_compile_definitions(MyLibrary     USE_EXPERIMENTAL_IMPLEMENTATION` |
| `target_compile_features()`                                  | 设置编译需要用的版本特性                                     | `target_compile_features(MyApp PRIVATE cxx_std_20)`          |
| `target_compile_options()`                                   | 添加编译器标志                                               | `target_compile_options(my_program PRIVATE -O3 -Wall -g)`    |
| `file()`                                                     | 文件系统操作                                                 |                                                              |
| `aux_source_directory(<dir> <variable>)`                     | 收集指定目录中所有源文件的名称。但当源文件只是添加到目录中而未修改此文件时，CMake识别不到，必须手动重新运行 CMake |                                                              |
| [`find_package()`]((https://cmake.com.cn/cmake/help/latest/command/find_package.html)) |                                                              |                                                              |
| `add_subdirectory(<source_dir>)`                             | 将子目录添加到构建中                                         |                                                              |
| `install`                                                    |                                                              |                                                              |

#### 4.2.2详细

##### `target_compile_options`

根据不同编译器设置不同的标志

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

##### `target_compile_definitions`

```cmake
target_compile_definitions(MyLibrary TUTORIAL_USE_STD_SQRT)
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

##### `file`

```cmake
file(GLOB <variable> [LIST_DIRECTORIES true|false] [RELATIVE <path>] [CONFIGURE_DEPENDS] <globbing-expressions>...)
file(GLOB_RECURSE <variable> [FOLLOW_SYMLINKS] [LIST_DIRECTORIES true|false] [RELATIVE <path>] [CONFIGURE_DEPENDS] <globbing-expressions>...)
```

##### `install`



```cmake
# Binaries	
install (TARGETS cmake_examples_inst_bin
    DESTINATION bin)

# Library
# Note: may not work on windows
install (TARGETS cmake_examples_inst
    LIBRARY DESTINATION lib)

# Header files
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/ 
    DESTINATION include)

# Config
install (FILES cmake-examples.conf
    DESTINATION etc)
```



## 5.编译标志

### 5.1`CMAKE_BUILD_TYPE`

`CMAKE_BUILD_TYPE` 有一组固定的选项，通常用于指定构建类型。常见的选项包括：

1. **`Debug`**: 无优化，带调试信息。
2. **`Release`**: 高级别优化，禁用断言，适用于发布。
3. **`RelWithDebInfo`**: 适中优化，带调试信息，适用于调试发布版。
4. **`MinSizeRel`**: 为减小可执行文件的大小进行优化。

| type             | 标志              |
| ---------------- | ----------------- |
| `Release`        | `-O3 -DNDEBUG`    |
| `Debug`          | `-g`              |
| `MinSizeRel`     | `-os -DNDEBUG`    |
| `RelWithDebInfo` | `-O2 -g -DNDEBUG` |

编译器的选项

| 选项       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| `-O3`      | 这是一个编译器优化选项，表示使用最高级别的优化（`-O0`, `-O1`, `-O2`, `-O3`）。`-O3` 启用的优化会尽量提高代码的执行效率，但可能会增加编译时间和生成文件的大小。它适用于发布版本，需要最大化性能的情况下。 |
| `-DNDEBUG` | 这是一个预处理器宏定义选项。`-DNDEBUG` 用于禁用 `assert` 宏的代码。在 `C` 或 `C++` 中，`assert` 是一种调试工具，它用于检查条件是否为真。如果条件为假，程序会终止并输出错误信息。通过定义 `NDEBUG`，可以在发布版本中去除所有的 `assert` 语句，减少运行时开销。 |
| `-g`       | 用于生成调试信息。当你在构建时使用 `-g` 标志时，编译器会将调试信息嵌入到生成的二进制文件中。这些调试信息对于使用调试器（例如 `gdb`）调试程序非常有用。使用 `-g` 会增加生成文件的大小，并且通常在调试构建中使用，帮助开发者检查程序的执行情况。 |
| `-Os`      | 这个选项用于优化代码的大小。`-Os` 启用优化，以减小生成的可执行文件的大小，同时尽可能减少性能的损失。它会尝试在不显著牺牲性能的情况下，优化代码的大小。这个选项对于嵌入式系统或资源有限的设备尤为重要，因为它能减少内存占用和文件大小。 |
| `-ggdb`    | 生成专门针对 GDB 调试器的调试信息，提供更多调试细节          |
| `-Wall`    | 启用常见的警告信息，提醒潜在的代码问题                       |



范例代码

```cmake
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message("Setting build type to 'RelWithDebInfo' as none was specified.")
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()
```

### 5.2其他加入标志的方式

#### 5.2.1`CMAKE_CXX_FLAGS` 或 `CMAKE_C_FLAGS`

你可以直接在 `CMakeLists.txt` 文件中设置编译器标志，具体取决于你使用的是 C++ 还是 C 编译器。

**示例：**

```
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -g")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -Wall -g")
```

这种方法会在所有 C++ 或 C 编译时附加这些标志。

#### 5.2.2 `target_compile_options()`

如果你希望只为特定目标（如可执行文件或库）添加编译器标志，可以使用 `target_compile_options()` 命令。

**示例：**

```
add_executable(my_program main.cpp)
target_compile_options(my_program PRIVATE -O3 -Wall -g)
```

这将为 `my_program` 目标添加 `-O3`, `-Wall` 和 `-g` 标志。

#### 5.2.3为不同的构建类型设置标志

CMake 提供了专门的变量来为不同的构建类型（如 `Debug`, `Release`, `RelWithDebInfo` 等）设置编译选项。这些变量是 `CMAKE_CXX_FLAGS_<CONFIG>` 或 `CMAKE_C_FLAGS_<CONFIG>`，其中 `<CONFIG>` 是构建类型。

**示例：**

```
# 设置 Release 构建类型的标志
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")

# 设置 Debug 构建类型的标志
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
```

这会在 `Release` 构建中添加 `-O3` 和 `-DNDEBUG`，在 `Debug` 构建中添加 `-g`。

#### 5.2.4 `CMAKE_BUILD_TYPE` 

在命令行中运行 CMake 时，你可以通过 `-DCMAKE_BUILD_TYPE` 选项指定构建类型，并结合相应的标志进行配置。

**示例：**

```
cmake -DCMAKE_BUILD_TYPE=Release ..
```

你可以在 `CMakeLists.txt` 中针对不同的构建类型（例如 `Release`, `Debug`）使用不同的编译标志，正如上面的例子所示。

## 6.配置和缓存变量

CMake 有多种方式可以让调用者传达这些配置选择

1. 最基本的是 [`-D`](https://cmake.com.cn/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-D) 标志

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



2.给配置选择提供默认值，此功能由 [`option()`](https://cmake.com.cn/cmake/help/latest/command/option.html#command:option) 

```bash
option(COMPRESSION_SOFTWARE_USE_ZLIB "Support Zlib compression" ON)
option(COMPRESSION_SOFTWARE_USE_ZSTD "Support Zstd compression" ON)

if(COMPRESSION_SOFTWARE_USE_ZLIB)
  # Same as before
# ...
```

`-D`标志和`option()` 创建的名称不是普通变量,而是缓存变量。缓存变量是全局可见的、*粘性* 的变量，其值在首次设置后很难更改。



3.`set()`也可以用来操作缓存变量，但不会更改已创建的变量

```cmake
set(StickyCacheVariable "I will not change" CACHE STRING "")
set(StickyCacheVariable "Overwrite StickyCache" CACHE STRING "")

message("StickyCacheVariable: ${StickyCacheVariable}")
# StickyCacheVariable: I will not change
```

缓存变量通常不能更改，但可以被普通变量 *覆盖*。我们可以通过设置一个与缓存变量同名的变量，然后使用`set()` 来设置一个普通变量，然后使用 `unset()` 删除普通变量来观察这一点。

```cmake
set(ShadowVariable "In the shadows" CACHE STRING "")
set(ShadowVariable "Hiding the cache variable")
message("ShadowVariable: ${ShadowVariable}")

unset(ShadowVariable)
message("ShadowVariable: ${ShadowVariable}")

# ShadowVariable: Hiding the cache variable
# ShadowVariable: In the shadows
```



## 7.库概念

[`add_library()`](https://cmake.com.cn/cmake/help/latest/command/add_library.html#command:add_library) 命令接受要创建的库目标的名称作为其第一个参数。第二个参数是一个可选的 `<type>`，其有效值为：

> - `STATIC`
>
>   [静态库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#static-libraries)：一个用于链接其他目标的归档文件。
>
> - `SHARED`
>
>   [共享库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#shared-libraries)：一个动态库，可以被其他目标链接并在运行时加载。
>
> - `INTERFACE`
>
>   一个 [接口库](https://cmake.com.cn/cmake/help/latest/manual/cmake-buildsystem.7.html#interface-libraries)：一个库目标，它为依赖项指定使用要求，但不编译源文件，也不在磁盘上生成库文件。

### 7.1静态库和共享库

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

### 7.2接口库

接口库是指仅为其他目标通信使用要求，自身不构建或生成任何文件的库。因此，接口库的所有属性本身都必须是接口属性，使用 `INTERFACE`

```cmake
add_library(MyInterface INTERFACE)
target_compile_definitions(MyInterface INTERFACE MYINTERFACE_COMPILE_DEF)
```

C++ 开发中最常见的接口库类型是仅头文件库。此类库不构建任何内容，只提供发现其头文件所需的标志。

### 7.3对象库

```cmake
add_library(MyObjects OBJECT)
```

对象库的一个常见用例是将几个库目标合并到一个存档或共享库对象中。即使在单个项目中，由于各种原因（例如属于组织内的不同团队），库也可能被维护为不同的目标。但是，将它们分发为单个面向消费者的二进制文件可能是可取的。对象库使这成为可能。