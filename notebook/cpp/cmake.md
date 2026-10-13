# CMake 日常笔记

这篇笔记只记录普通 C++ 项目中经常会用到的内容，不追求覆盖 CMake 的所有功能。

## 1. 配置、构建和测试

CMake 通常不直接编译代码。它读取 `CMakeLists.txt`，生成 Ninja、Makefile 或 Visual Studio 工程，再由对应的构建工具调用编译器。

日常最常用的三步：

```bash
# 配置：读取 CMakeLists.txt，生成构建系统
cmake -S . -B build

# 构建：编译并链接
cmake --build build --parallel

# 测试：运行已经构建并注册的测试
ctest --test-dir build --output-on-failure
```

`-S .` 指定源码目录，`-B build` 指定构建目录。建议始终使用独立的构建目录，避免生成文件混入源码。

只构建某个 target：

```bash
cmake --build build --target app
```

## 2. 最小项目

```text
hello/
├── CMakeLists.txt
└── main.cpp
```

```cmake
cmake_minimum_required(VERSION 3.23)

project(Hello
  VERSION 1.0.0
  LANGUAGES CXX
)

add_executable(hello main.cpp)
target_compile_features(hello PRIVATE cxx_std_20)
```

- `cmake_minimum_required()`：要求的最低 CMake 版本；
- `project()`：项目名称、版本和使用的语言；
- `add_executable()`：创建可执行 target；
- `target_compile_features()`：声明该 target 需要 C++20。

## 3. Target

Target 是 CMake 中最重要的概念。可执行文件和库都是 target，它们记录自己的源文件、头文件目录、编译选项和依赖关系。

### 3.1 可执行文件

源码少时直接列出：

```cmake
add_executable(app
  src/main.cpp
  src/application.cpp
)
```

也可以先创建，再补充源码：

```cmake
add_executable(app)

target_sources(app
  PRIVATE
    src/main.cpp
    src/application.cpp
)
```

### 3.2 库

```cmake
add_library(math src/math.cpp)

target_include_directories(math
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
```

显式指定库类型：

```cmake
add_library(math_static STATIC src/math.cpp)
add_library(math_shared SHARED src/math.cpp)
```

省略类型时，`BUILD_SHARED_LIBS` 决定生成静态库还是共享库：

```cmake
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
add_library(math src/math.cpp)
```

仅头文件库不生成二进制文件，使用 `INTERFACE` target：

```cmake
add_library(math_headers INTERFACE)

target_include_directories(math_headers
  INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
```

### 3.3 Include 和 link 的区别

```cmake
target_include_directories(app PRIVATE some/include/path)
```

它告诉编译器去哪里寻找头文件，解决的是：

```cpp
#include <foo/foo.hpp>
```

能否找到的问题。

```cmake
target_link_libraries(app PRIVATE foo)
```

它让 `app` 链接 `foo`，解决函数或对象的实现来自哪里的链接问题。

如果 `foo` 是配置正确的 CMake target，它会把自己的公共 include 目录传给 `app`。消费者通常只需要链接它：

```cmake
target_link_libraries(app PRIVATE foo)
```

不需要再给 `app` 重复添加 `foo` 的头文件目录。

## 4. `PRIVATE`、`PUBLIC` 和 `INTERFACE`

它们描述一项配置由谁使用，而不是 C++ 的访问权限。

| 关键字 | 当前 target 使用 | 传给依赖它的 target |
| --- | :---: | :---: |
| `PRIVATE` | 是 | 否 |
| `PUBLIC` | 是 | 是 |
| `INTERFACE` | 否 | 是 |

判断一个库依赖的作用域时，可以看它出现在哪里：

- 只在 `.cpp` 中使用：`PRIVATE`；
- 在 `.cpp` 和公开头文件中都使用：`PUBLIC`；
- 当前实现不用，只有公开头文件需要：`INTERFACE`。

```cmake
target_link_libraries(archive
  PUBLIC  compression_api
  PRIVATE compression_backend
)
```

如果 `archive` 的公开头文件暴露了 `compression_api` 的类型，它的消费者也需要该依赖，因此使用 `PUBLIC`。如果 `compression_backend` 只在实现文件中使用，则使用 `PRIVATE`。

这套规则同样适用于：

```cmake
target_include_directories()
target_compile_features()
target_compile_definitions()
target_compile_options()
```

## 5. 多目录项目

```text
project/
├── CMakeLists.txt
├── app/
│   ├── CMakeLists.txt
│   └── main.cpp
└── lib/
    ├── CMakeLists.txt
    ├── include/math/math.hpp
    └── src/math.cpp
```

顶层 `CMakeLists.txt`：

```cmake
cmake_minimum_required(VERSION 3.23)
project(Demo LANGUAGES CXX)

add_subdirectory(lib)
add_subdirectory(app)
```

`lib/CMakeLists.txt`：

```cmake
add_library(math src/math.cpp)
target_include_directories(math PUBLIC include)
target_compile_features(math PUBLIC cxx_std_20)
```

`app/CMakeLists.txt`：

```cmake
add_executable(app main.cpp)
target_link_libraries(app PRIVATE math)
```

子目录中的相对路径以该子目录为基准。上例中，`app` 只需要链接 `math`，便会获得它公开的 include 目录和 C++ 标准要求。

## 6. 构建类型

### 6.1 单配置生成器

Ninja、Unix Makefiles 等生成器在配置阶段确定构建类型：

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

常见值：

- `Debug`
- `Release`
- `RelWithDebInfo`
- `MinSizeRel`

没有设置 `CMAKE_BUILD_TYPE` 不等于 Debug，通常只是空配置。

### 6.2 多配置生成器

Visual Studio、Xcode 和 Ninja Multi-Config 可以在同一个构建目录中保存多种配置，构建时再选择：

```bash
cmake -S . -B build
cmake --build build --config Debug
cmake --build build --config Release
```

对多配置生成器设置 `CMAKE_BUILD_TYPE` 通常不起作用。

### 6.3 与配置有关的选项

```cmake
target_compile_definitions(app
  PRIVATE
    $<$<CONFIG:Debug>:APP_ENABLE_TRACE>
)
```

`$<CONFIG:Debug>` 是生成器表达式。它对单配置和多配置生成器都有效，用来判断当前实际构建的配置是否为 Debug。

## 7. 常用编译设置

设置 C++ 标准：

```cmake
target_compile_features(app PRIVATE cxx_std_20)
```

设置预处理器宏：

```cmake
target_compile_definitions(app PRIVATE APP_ENABLE_LOG)
```

设置警告参数：

```cmake
if(MSVC)
  target_compile_options(app PRIVATE /W4 /permissive-)
else()
  target_compile_options(app PRIVATE -Wall -Wextra -Wpedantic)
endif()
```

`CMAKE_CXX_FLAGS` 会影响整个构建中的所有 C++ target。它不是不能使用，但日常给某个 target 添加参数时，`target_compile_options()` 的作用范围更准确。

## 8. `find_package()`

日常使用第三方库时，优先使用包提供的 target：

```cmake
find_package(fmt CONFIG REQUIRED)
target_link_libraries(app PRIVATE fmt::fmt)
```

`fmt::fmt` 通常已经携带 include 目录、编译设置和传递依赖，不需要手工填写库文件路径。

`find_package()` 常见的两种模式：

- **Config 模式**：寻找包安装的 `FooConfig.cmake` 或 `foo-config.cmake`；
- **Module 模式**：寻找 CMake 或项目提供的 `FindFoo.cmake`。

不是所有库都提供 Config 文件，具体用法以第三方库文档为准。

### 8.1 找不到包时提供搜索路径

假设配置文件位于：

```text
D:/libs/Foo/lib/cmake/Foo/FooConfig.cmake
```

常用变量：

| 变量 | 应该指向哪里 |
| --- | --- |
| `CMAKE_PREFIX_PATH` | 一个或多个安装前缀，例如 `D:/libs/Foo` |
| `Foo_ROOT` | `Foo` 的安装根目录，例如 `D:/libs/Foo` |
| `Foo_DIR` | `FooConfig.cmake` 所在目录 |

```bash
cmake -S . -B build -DCMAKE_PREFIX_PATH="D:/libs/Foo;D:/libs/Bar"
cmake -S . -B build -DFoo_ROOT=D:/libs/Foo
cmake -S . -B build -DFoo_DIR=D:/libs/Foo/lib/cmake/Foo
```

这些是机器相关路径，适合通过命令行、Preset 或包管理器提供，不要硬编码在共享的 `CMakeLists.txt` 中。

## 9. CMake Preset

如果每天都要重复输入同一组配置参数，可以写进项目根目录的 `CMakePresets.json`：

```json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/debug",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "BUILD_TESTING": "ON",
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "debug",
      "configurePreset": "debug"
    }
  ]
}
```

```bash
cmake --preset debug
cmake --build --preset debug
```

`configurePresets` 保存配置阶段的参数，`buildPresets` 保存构建阶段的参数。项目共享配置写进 `CMakePresets.json`；个人机器专用的路径可写进通常不提交的 `CMakeUserPresets.json`。

## 10. 测试

CTest 是 CMake 配套的测试运行工具。它负责运行和汇总测试，但不会编译测试程序。

### 10.1 `enable_testing()` 和 `add_test()`

假设我们先创建了一个测试程序，它对应的可执行 target 名为 `math_tests`：

```cmake
enable_testing()

add_executable(math_tests tests/math_tests.cpp)
target_link_libraries(math_tests PRIVATE math)
```

接下来把这个程序登记到 CTest。每条测试记录都需要一个名字；这里采用“模块.场景”的命名方式，把它命名为 `math.basic`：

```cmake
add_test(
  NAME math.basic
  COMMAND math_tests
)
```

- `enable_testing()`：为当前目录及其子目录启用 CTest 测试生成，通常放在顶层 `CMakeLists.txt`；
- `add_test()`：把一个命令登记为 CTest 测试；
- `NAME math.basic`：这条测试在 CTest 中的名字，由项目作者自行决定，不必与文件名或 target 名相同；
- `COMMAND math_tests`：运行名为 `math_tests` 的可执行 target，CMake 会将它替换成实际文件路径；
- 测试命令返回 `0` 表示通过，返回非零值表示失败。

因此这段配置可以直译为：“注册一条名为 `math.basic` 的测试，执行它时运行 `math_tests`”。这个名字会出现在 CTest 的结果中，也可以用于筛选：

```bash
ctest --test-dir build -R '^math\.basic$'
```

必须先构建测试程序，再运行 CTest：

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

### 10.2 `include(CTest)` 和 `BUILD_TESTING`

如果希望用户能够关闭测试，常见写法是：

```cmake
include(CTest)

if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
```

`include(CTest)` 会创建默认开启的 `BUILD_TESTING` 选项，并在它为 `ON` 时自动调用 `enable_testing()`。因此这里不用再重复调用 `enable_testing()`。

关闭测试：

```bash
cmake -S . -B build -DBUILD_TESTING=OFF
```

### 10.3 GoogleTest

GoogleTest 用来编写 C++ 测试，CTest 用来统一运行它们：

```cmake
find_package(GTest REQUIRED)

add_executable(math_tests tests/math_tests.cpp)
target_link_libraries(math_tests PRIVATE math GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(math_tests)
```

`include(GoogleTest)` 只是加载 CMake 的辅助模块；真正链接的库是 `GTest::gtest_main`。上层仍需要通过 `enable_testing()` 或 `include(CTest)` 启用测试。

多配置生成器运行测试时需要指定配置：

```bash
cmake --build build --config Debug
ctest --test-dir build -C Debug --output-on-failure
```

## 11. 常用目录变量

| 变量 | 含义 |
| --- | --- |
| `PROJECT_SOURCE_DIR` | 最近一次 `project()` 对应的源码根目录 |
| `PROJECT_BINARY_DIR` | 最近一次 `project()` 对应的构建根目录 |
| `CMAKE_SOURCE_DIR` | 最外层项目的源码根目录 |
| `CMAKE_BINARY_DIR` | 最外层项目的构建根目录 |
| `CMAKE_CURRENT_SOURCE_DIR` | 当前 `CMakeLists.txt` 对应的源码目录 |
| `CMAKE_CURRENT_BINARY_DIR` | 当前目录对应的构建目录 |

项目被其他工程通过 `add_subdirectory()` 引入后，`CMAKE_SOURCE_DIR` 会指向最外层工程，因此可复用子项目不要默认它就是自己的根目录。

## 12. 常见排查

- 找不到头文件：检查依赖 target 是否公开了 include 目录，以及当前 target 是否正确链接它。
- 编译通过但链接失败：检查实现所在的库和传递依赖是否正确链接。
- `find_package()` 失败：确认包是否提供 Config 文件，再检查 `CMAKE_PREFIX_PATH`、`Foo_ROOT` 或 `Foo_DIR`。
- `ctest` 提示没有测试：检查是否调用了 `enable_testing()` 或 `include(CTest)`，以及 `BUILD_TESTING` 是否被关闭。
- 找不到测试可执行文件：先运行 `cmake --build`，CTest 不负责构建。
- Visual Studio 下 Debug 条件不生效：使用 `$<CONFIG:Debug>`，不要用 `CMAKE_BUILD_TYPE` 判断多配置构建。

## 13. 安装与动态库部署

构建把文件放进 build 目录；安装则按约定整理程序、库和头文件。动态库项目还需要解决两件事：程序运行时去哪里找库，以及库向外提供哪些接口。

### 13.1 安装程序、库和头文件

假设项目包含共享库 `math`、使用它的程序 `app`，公共头文件放在 `include/math/`：

```cmake
include(GNUInstallDirs)

add_library(math SHARED src/math.cpp)
add_executable(app src/main.cpp)
target_link_libraries(app PRIVATE math)

target_include_directories(math PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
  "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>"
)

install(TARGETS app math
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

`GNUInstallDirs` 提供安装目录变量，通常为 `bin`、`lib`（有些平台是 `lib64`）、`include`。`DESTINATION` 使用相对路径，相对于安装前缀；`include/` 末尾的斜杠表示复制目录中的内容。

| 类别 | 安装内容 |
| --- | --- |
| `RUNTIME` | 可执行文件、Windows DLL |
| `LIBRARY` | Linux `.so` 等共享库 |
| `ARCHIVE` | 静态库、Windows DLL 对应的导入库 `.lib` 等 |

`BUILD_INTERFACE` 指定源码构建时的 include 路径，`INSTALL_INTERFACE` 指定安装后消费者使用的路径，后者相对于安装前缀。这样不会把开发机器的源码绝对路径写进安装接口。

先构建，再安装：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
cmake --install build --config Release --prefix ./stage
```

`--prefix` 指定本次安装位置，也可以在配置时设置 `-DCMAKE_INSTALL_PREFIX=...`。`--config Release` 用于多配置生成器，单配置生成器仍以配置时的 `CMAKE_BUILD_TYPE` 为准。安装不会自动编译，也不会自动把所有第三方运行库一起打包。

此时只是安装文件；要让其他项目通过 `find_package()` 使用 `math`，还需要另外提供 target 导出和包配置文件。[安装文档](https://cmake.org/cmake/help/latest/command/install.html)

### 13.2 RPATH：安装后去哪里找动态库

链接成功只说明构建时找到了库。程序启动时，操作系统还需要找到对应的动态库。RPATH 是写入二进制文件的运行时库搜索路径，不是头文件路径，也不负责复制库。

CMake 通常自动为构建目录设置所需的 RPATH；安装时则改用 `INSTALL_RPATH`，默认是空的。构建目录能运行，不代表安装后也能运行。[BUILD_RPATH](https://cmake.org/cmake/help/latest/prop_tgt/BUILD_RPATH.html)、[INSTALL_RPATH](https://cmake.org/cmake/help/latest/prop_tgt/INSTALL_RPATH.html)

接着上例，在 Linux 上假定安装布局为 `bin/app` 和 `lib/` 中的动态库（安装目录变量使用相对路径）：

```cmake
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
  set_target_properties(app PROPERTIES
    INSTALL_RPATH "$ORIGIN/../${CMAKE_INSTALL_LIBDIR}"
  )
  set_target_properties(math PROPERTIES
    INSTALL_RPATH "$ORIGIN"
  )
endif()
```

`$ORIGIN` 表示当前程序或动态库所在目录。相对布局不变时，这些设置允许整体移动安装目录；若更改 `bin`、`lib` 的布局，应相应调整路径。

库自身的 RPATH 用于查找它依赖的其他动态库，因此上例也为 `math` 设置了同目录搜索路径。

Windows 不使用上述 RPATH 机制。常见做法是将 DLL 放在 `.exe` 同目录，或配置 `PATH`。上例将程序和本项目 DLL 都安装到 `bin`，第三方 DLL 仍需要额外部署。

### 13.3 跨平台导出宏：动态库提供哪些接口

在公共头文件 `include/math/export.h` 中定义导出宏：

```cpp
#pragma once

#if defined(_WIN32)
#ifdef MYLIB_BUILD
#define MYLIB_API __declspec(dllexport)
#else
#define MYLIB_API __declspec(dllimport)
#endif
#else
#define MYLIB_API __attribute__((visibility("default")))
#endif
```

构建 Windows DLL 时定义 `MYLIB_BUILD`，使用 DLL 时不定义，分别选择导出和导入；Linux GCC/Clang 使用默认可见性属性公开接口。CMake 只给库自身定义构建宏：

```cmake
target_compile_definitions(math PRIVATE MYLIB_BUILD)
set_target_properties(math PROPERTIES
  CXX_VISIBILITY_PRESET hidden
  VISIBILITY_INLINES_HIDDEN YES
)
```

`MYLIB_BUILD` 必须用 `PRIVATE`，避免消费者也把接口当成导出。在 `include/math/math.hpp` 中用 `MYLIB_API` 标记公共接口：

```cpp
#pragma once
#include <math/export.h>

MYLIB_API int add(int a, int b);

class MYLIB_API Calculator {
public:
    int multiply(int a, int b) const;
};
```

默认隐藏配合 `MYLIB_API`，让公共接口可见、内部实现保持隐藏。`export.h` 位于公共 include 目录，随前面的 `install(DIRECTORY include/ ...)` 一起安装。这份宏用于共享库；若支持 Windows 静态库，应另设静态库分支，将 `MYLIB_API` 定义为空。

# ImageLite-CMake 学习补充

从项目的配置开始，依次整理模块、引入依赖，再把代码生成和运行任务接入构建流程。

## 1. 先确定配置，再创建模块

CMake 按顺序执行配置，`add_subdirectory()` 会立即处理子目录。因此，C++ 标准、输出目录等默认设置应放在创建 target 之前：

```cmake
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")

option(IMAGELITE_BUILD_TESTS "Build tests" ON)

add_subdirectory(libs/core)
add_subdirectory(libs/filters)
if(IMAGELITE_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()
```

这三个标准变量分别表示使用 C++17、不允许退回较低标准、不请求编译器扩展模式。它们初始化后续 target 的属性，不会追溯修改已创建的 target；需要向消费者传递标准要求时，仍使用 `target_compile_features(... PUBLIC cxx_std_17)`。

普通 `set(NAME value)` 设置当前作用域的变量；`set(NAME value CACHE STRING "说明")` 将值保存在 `CMakeCache.txt` 中，后续配置时保留。`option()` 创建布尔缓存选项，可以通过 `-DIMAGELITE_BUILD_TESTS=OFF` 修改；`FORCE` 则会覆盖已有缓存值。

多个模块的创建方式相同时，可以用函数统一配置：

```cmake
function(add_image_module name lib_type)
  add_library(${name} ${lib_type} ${ARGN})
  target_include_directories(${name} PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
  )
  target_compile_features(${name} PUBLIC cxx_std_17)
endfunction()

# 在 libs/core/CMakeLists.txt 中调用。
add_image_module(ImageLite_core STATIC
  src/core.cpp src/image.cpp src/platform_info.cpp
)
```

`name`、`lib_type` 接收前两个参数，`ARGN` 接收剩余参数。函数中的普通变量有独立作用域，但创建的 target 会保留；这里的 `CMAKE_CURRENT_SOURCE_DIR` 指向调用时正在处理的源码目录。

## 2. 为模块设置属性和条件

创建 target 后，可以用 `set_target_properties()` 设置属性，用 `get_target_property()` 读取：

```cmake
set_target_properties(ImageLite_core PROPERTIES
  POSITION_INDEPENDENT_CODE ON
  CXX_VISIBILITY_PRESET hidden
)
get_target_property(visibility ImageLite_core CXX_VISIBILITY_PRESET)
message(STATUS "Core visibility: ${visibility}")
```

`POSITION_INDEPENDENT_CODE` 请求位置无关代码，常用于将静态库链接进共享库；`CXX_VISIBILITY_PRESET hidden` 在支持的编译器上隐藏默认符号可见性，开发共享库时仍需显式导出公共 API。

输出目录也是 target 属性。`RUNTIME_OUTPUT_DIRECTORY` 对应可执行文件和 Windows DLL，`LIBRARY_OUTPUT_DIRECTORY` 对应 Linux/macOS 共享库等，`ARCHIVE_OUTPUT_DIRECTORY` 对应静态库和 Windows 导入库。按配置指定目录时使用后缀：

```cmake
set_target_properties(ImageLite PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY_DEBUG "${PROJECT_BINARY_DIR}/bin/debug"
  RUNTIME_OUTPUT_DIRECTORY_RELEASE "${PROJECT_BINARY_DIR}/bin/release"
)
```

需要按编译器、平台或配置选择设置时，可以组合生成器表达式：

```cmake
target_compile_options(ImageLite PRIVATE
  "$<$<CXX_COMPILER_ID:GNU>:-Wall;-Wextra>"
  "$<$<CXX_COMPILER_ID:MSVC>:/W4>"
  "$<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU>>:-g;-O0>"
)
target_compile_definitions(ImageLite PRIVATE
  "$<$<PLATFORM_ID:Windows>:IMAGELITE_WINDOWS>"
  "$<$<PLATFORM_ID:Darwin>:IMAGELITE_MACOS>"
)
```

`$<条件:内容>` 在条件成立时保留内容；`AND` 要求全部成立，`OR` 要求至少一个成立。多个编译选项用分号分隔，并给整个表达式加引号，避免空格将表达式拆开。

普通 `if()` 在配置阶段执行，生成器表达式在生成构建系统时求值，适合处理多配置差异。平台判断中的 `WIN32` 包括 64 位 Windows，`APPLE` 包括 macOS；`UNIX` 不等于 Linux，只判断 Linux 时使用 `CMAKE_SYSTEM_NAME STREQUAL "Linux"`。

## 3. 引入第三方依赖

已有安装包时使用 `find_package()`；需要随项目获取第三方源码时，可以使用 `FetchContent`：

```cmake
include(FetchContent)
FetchContent_Declare(googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(googletest)

target_link_libraries(core_tests PRIVATE GTest::gtest_main)
```

`Declare` 声明来源，`MakeAvailable` 在配置阶段获取源码，并在依赖提供 CMake 构建系统时加入工程。Git 来源使用 `GIT_REPOSITORY` 和 `GIT_TAG`，固定提交比跟随 `master` 更容易复现；压缩包可用 `URL_HASH` 校验。`DOWNLOAD_EXTRACT_TIMESTAMP TRUE` 使用解压时的时间戳，避免更新依赖后因旧时间戳漏掉重建。

如果源码没有提供 target，例如 stb，就手动包装它的使用要求：

```cmake
# 已通过 FetchContent 获取 stb 源码。
add_library(stb_image INTERFACE)
target_include_directories(stb_image SYSTEM INTERFACE "${stb_SOURCE_DIR}")
target_link_libraries(ImageLite_core PRIVATE stb_image)
```

`SYSTEM` 将目录标为系统头文件目录，通常减少第三方头文件警告。这里链接的是 include 等配置，不是 stb 二进制库；实现仍需按 stb 的约定在源文件中启用。

另一种情况是系统中只有库文件，可以用 `find_library(FOO_LIBRARY NAMES foo REQUIRED)` 获取其路径，再传给 `target_link_libraries()`。它不会自动补齐头文件目录或传递依赖，因此优先使用包提供的 target。

## 4. 将生成文件接入构建流程

ImageLite 的 `formats.h` 来自 Python 脚本。需要把“输入脚本 → 输出头文件 → 编译程序”的依赖关系告诉构建系统：

```cmake
find_package(Python3 REQUIRED COMPONENTS Interpreter)
set(script "${PROJECT_SOURCE_DIR}/scripts/generate_formats.py")
set(header "${PROJECT_BINARY_DIR}/include/imagelite/formats.h")

add_custom_command(
  OUTPUT "${header}"
  COMMAND "${CMAKE_COMMAND}" -E make_directory
          "${PROJECT_BINARY_DIR}/include/imagelite"
  COMMAND Python3::Interpreter "${script}"
  DEPENDS "${script}"
  WORKING_DIRECTORY "${PROJECT_BINARY_DIR}"
  COMMENT "Generating formats.h"
  VERBATIM
)
add_custom_target(GenerateFormats DEPENDS "${header}")
add_dependencies(ImageLite GenerateFormats)
target_include_directories(ImageLite PRIVATE "${PROJECT_BINARY_DIR}/include")
```

`COMPONENTS Interpreter` 只请求 Python 解释器。脚本按相对路径写文件，所以将 `WORKING_DIRECTORY` 设为构建目录；`VERBATIM` 让 CMake 正确转义命令参数。

`add_custom_command(OUTPUT ...)` 定义文件的生成规则，`DEPENDS` 声明输入。输出缺失或输入更新时才需要重新生成，因此必须把脚本也列入依赖。`add_custom_target()` 将输出接入一个任务，`add_dependencies()` 保证程序编译前完成该任务；它只安排构建顺序，不负责链接或传递 include 目录。

给自定义 target 加 `ALL` 会将其纳入默认构建，但不会让已经是最新状态的输出文件每次重新生成。

## 5. 接入运行、收尾和测试任务

有了程序和生成规则后，还可以定义一键运行任务：

```cmake
add_custom_target(run
  COMMAND ImageLite blur
          "${PROJECT_SOURCE_DIR}/sample_images/input.jpg"
          "${PROJECT_BINARY_DIR}/output.jpg" 5
  DEPENDS ImageLite
  VERBATIM
)
```

执行 `cmake --build build --target run` 时先构建 `ImageLite`，再运行命令；命令中的 target 名会被替换为程序路径。

构建结束后复制文件，则使用绑定 target 的构建事件：

```cmake
add_custom_command(TARGET ImageLite POST_BUILD
  COMMAND "${CMAKE_COMMAND}" -E copy_if_different
          "${PROJECT_SOURCE_DIR}/README.md"
          "$<TARGET_FILE_DIR:ImageLite>/README.md"
  VERBATIM
)
```

`${CMAKE_COMMAND} -E` 提供跨平台的复制、创建目录等操作；`$<TARGET_FILE_DIR:ImageLite>` 获取程序实际所在目录。`PRE_LINK` 在编译完成、链接前执行，`POST_BUILD` 在构建完成后执行；`PRE_BUILD` 只有 Visual Studio 提供特殊的构建前行为，其他生成器通常按 `PRE_LINK` 处理，不能用它跨平台保证头文件先于编译生成。

最后给已注册的测试设置超时和标签，便于控制执行：

```cmake
set_tests_properties(CoreTests PROPERTIES
  TIMEOUT 10
  LABELS "core;fast"
)
```

`ctest --test-dir build -L '^fast$'` 按标签筛选，`-V` 显示详细命令和日志。这里的超时为 10 秒，针对整条 `CoreTests`；如果它通过 `add_test()` 运行整个 GoogleTest 程序，超时就不是针对其中每个用例。
