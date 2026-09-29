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
