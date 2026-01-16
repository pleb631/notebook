## **前言**

在进行性能优化时，常常需验证改进的方法是否有效；或有时灵光一现，觉得某段代码的写法 A 比写法 B 更高效，这时都需要一个 benchmark 工具来对比方法改进前后的性能。这里给大家推荐一个好用的库： [Google Benchmark](https://link.zhihu.com/?target=https%3A//github.com/google/benchmark)

## **使用方式**

### **基本用法**

基本的用法如下：

1.  写待测量的方法。
2.  使用宏 `BENCHMARK` 注册方法。
3.  最后调用宏 `BENCHMARK_MAIN()`。

举个简单的例子：

```cpp
static void Method_A(benchmark::State& state) {
  for (auto _ : state) {
    std::vector<std::string> v;
    for (int i = 0; i < state.range(0); ++i) {
      benchmark::DoNotOptimize(v.emplace_back(s));
      benchmark::ClobberMemory();
    }
  }
}

BENCHMARK(Method_A)->Arg(10086);
BENCHMARK_MAIN();
```

这个例子是传入参数 `10086`，测量 `Method_A` 方法，输出如下：

```text
2024-06-30T16:31:20+08:00
Running ./output/method_a
Run on (2 X 2595.12 MHz CPU s)
CPU Caches:
  L1 Data 32 KiB (x2)
  L1 Instruction 32 KiB (x2)
  L2 Unified 4096 KiB (x2)
  L3 Unified 16384 KiB (x1)
Load Average: 0.08, 0.06, 0.06
-----------------------------------------------------------
Benchmark                 Time             CPU   Iterations
-----------------------------------------------------------
Method_A/10086     211701 ns       211682 ns         3265
```

输出结果中，`Time` 列表示时钟时间；`CPU` 列表示 CPU 消耗时间；`Iterations` 列表示 benchmark 获得相对稳定的结果运行的次数，一般而言，速度快的方法该值较大，速度慢的方法该值较小。此外还展示了运行的机器信息。

值得一提的是，代码中的`for (auto _ : state)` 是使用了 `ranged-based for loop` 语法糖代替了 `while (state.KeepRunning())`的实现，并不是遍历传入的 `Arg` 参数。获取参数方式是通过 `state.range(x)`。

在 `BENCHMARK` 宏后可以设置多个参数，通过 `->` 级联，下面整理了一些常用的设置：

### **传参**

```cpp
// 两组测量，分别传入 1 和 2 两个参数
BENCHMARK(Method_A)->Arg(1)->Arg(2);

// 多组测量，参数范围 [8, 8k]，默认间隔乘 8
BENCHMARK(Method_A)->Range(8, 8<<10);
// 相当于
BENCHMARK(Method_A)->Arg(8)->Arg(64)->Arg(512)->Arg(4<<10)->Arg(8<<10);
// 修改间隔乘子为 2
BENCHMARK(Method_A)->RangeMultiplier(2)->Range(8, 8<<10);

// 多组测量，参数范围 [0, 512]，默认间隔加 128
BENCHMARK(Method_A)->DenseRange(0, 512, 128);
// 相当于
BENCHMARK(Method_A)->Arg(0)->Arg(128)->Arg(256)->Arg(384)->Arg(512);

// 一组测量，传入 1 和 2 两个参数
BENCHMARK(Method_A)->Args({1, 2});

// 多组测量，每次传入多个参数，固定间隔
BENCHMARK(Method_A)->Ranges({{1<<10, 8<<10}, {128, 512}});
// 相当于
BENCHMARK(Method_A)
    ->Args({1<<10, 128})
    ->Args({2<<10, 128})
    ->Args({4<<10, 128})
    ->Args({8<<10, 128})
    ->Args({1<<10, 512})
    ->Args({2<<10, 512})
    ->Args({4<<10, 512})
    ->Args({8<<10, 512});

// 多组测量，每次传入多个参数，非固定间隔
BENCHMARK(Method_A)
    ->ArgsProduct({{1<<10, 3<<10, 8<<10}, {20, 40, 60, 80}});
// 相当于
BENCHMARK(Method_A)
    ->Args({1<<10, 20})
    ->Args({3<<10, 20})
    ->Args({8<<10, 20})
    ->Args({3<<10, 40})
    ->Args({8<<10, 40})
    ->Args({1<<10, 40})
    ->Args({1<<10, 60})
    ->Args({3<<10, 60})
    ->Args({8<<10, 60})
    ->Args({1<<10, 80})
    ->Args({3<<10, 80})
    ->Args({8<<10, 80});
// 更简洁的写法
BENCHMARK(Method_A)
    ->ArgsProduct({
      benchmark::CreateRange(8, 128, /*multi=*/2),
      benchmark::CreateDenseRange(1, 4, /*step=*/1)
    })
// 相当于
BENCHMARK(Method_A)
    ->ArgsProduct({
      {8, 16, 32, 64, 128},
      {1, 2, 3, 4}
    });

// 当然，还可以自定义传参
static void CustomArguments(benchmark::internal::Benchmark* b) {
  for (int i = 0; i <= 10; ++i)
    for (int j = 32; j <= 1024*1024; j *= 8)
      b->Args({i, j});
}
BENCHMARK(Method_A)->Apply(CustomArguments);
```

要想传任意类型的参数，官网给出的例子：

```cpp
template <class ...Args>
void BM_takes_args(benchmark::State& state, Args&&... args) {
  auto args_tuple = std::make_tuple(std::move(args)...);
  for (auto _ : state) {
    std::cout << std::get<0>(args_tuple) << ": " << std::get<1>(args_tuple)
              << '\n';
    [...]
  }
}

// `int_string_test` 是方法名，后面是参数
BENCHMARK_CAPTURE(BM_takes_args, int_string_test, 42, std::string("abc"));

// `int_test`是方法名，后面是参数
BENCHMARK_CAPTURE(BM_takes_args, int_test, 42, 43);
```

### **Setup 和 TearDown**

如果待测量方法需要初始化和清理工作，可以这样设置：

```cpp
static void DoSetup(const benchmark::State& state) {
}

static void DoTeardown(const benchmark::State& state) {
}

static void Method_A(benchmark::State& state) {...}

BENCHMARK(Method_A)->Arg(1)->Arg(3)->Setup(DoSetup)->Teardown(DoTeardown);
```

注意，每组测量用例都会执行一次 `Setup` 和 `Teardown`。

### **Fixture**

如果想在多个待测量方法之间共享初始化、清理代码或一些变量，可以使用 `Fixture`:

```cpp
class MyFixture : public benchmark::Fixture {
public:
  void SetUp(::benchmark::State& state) {
  }

  void TearDown(::benchmark::State& state) {
  }
};

BENCHMARK_F(MyFixture, FooTest)(benchmark::State& st) {
   for (auto _ : st) {
     // ...
  }
}

BENCHMARK_DEFINE_F(MyFixture, BarTest)(benchmark::State& st) {
   for (auto _ : st) {
     // ...
  }
}

BENCHMARK_REGISTER_F(MyFixture, BarTest)->Threads(2);
```

### **增加统计信息**

默认测量结果只输出一些时间相关的统计，要想自行增加一些统计信息，可用 `state.counters`，举些例子：

```cpp
static void Method_A(benchmark::State& state) {
  double x = 0, y = 0, z = 0;
  for (auto _ : state) {
    // ... 操作 x,y,z
  }
  state.counters["x"] = x;
  state.counters["y"] = y;
  state.counters["z"] = z;
}
```

一般在 `for (auto _ : state)` 结束后，即测量完成后，设置 `state.counters`来保存自定义的统计信息。在输出结果里，有专门一列 `UserCounters` 会输出设置 `counters` 的值，如：

```text
----------------
UserCounters...
----------------
x=1 y=2 z=3
```

`state.counters` 还支持一些计算，比如用于统计待测量方法处理 bytes 的速度。贴些官方的例子，有需要时再研究。

```cpp
// sets a simple counter
state.counters["Foo"] = numFoos;

// Set the counter as a rate. It will be presented divided
// by the duration of the benchmark.
// Meaning: per one second, how many 'foo's are processed?
state.counters["FooRate"] = benchmark::Counter(numFoos, benchmark::Counter::kIsRate);

// Set the counter as a rate. It will be presented divided
// by the duration of the benchmark, and the result inverted.
// Meaning: how many seconds it takes to process one 'foo'?
state.counters["FooInvRate"] = benchmark::Counter(numFoos, benchmark::Counter::kIsRate | benchmark::Counter::kInvert);

// Set the counter as a thread-average quantity. It will
// be presented divided by the number of threads.
state.counters["FooAvg"] = benchmark::Counter(numFoos, benchmark::Counter::kAvgThreads);

// There's also a combined flag:
state.counters["FooAvgRate"] = benchmark::Counter(numFoos, benchmark::Counter::kAvgThreadsRate);

// This says that we process with the rate of state.range(0) bytes every iteration:
state.counters["BytesProcessed"] = benchmark::Counter(state.range(0), benchmark::Counter::kIsIterationInvariantRate,benchmark::Counter::OneK::kIs1024);
```

若运行了多次测量（通过 `--benchmark_repetitions` 指定），可以通过自定义的 `ComputeStatistics` 来统计多次测量结果的信息。如想看多次测量中耗时最长的一次：

```cpp
void Method_A(benchmark::State& state) {
  for (auto _ : state) {
    for (int x = 0; x < state.range(0); ++x) {
      // ...
    }
  }
}

BENCHMARK(Method_A)
  ->ComputeStatistics("max", [](const std::vector<double>& v) -> double {
    return *(std::max_element(std::begin(v), std::end(v)));
  })
  ->Arg(100);
```

### **测量基准**

上述提到，框架会多次运行待测量的方法，以便获得相对稳定的测量结果。默认情况下，框架运行次数的基准是基于主线程的 CPU 消耗时间，因此输出结果中的 `CPU` 列表示的也是主线程的 CPU 消耗时间。可通过以下方式设置不同的基准：

```cpp
// 使用时钟时间作为基准，适用于需要实际时间的测量，特别是多线程程序
BENCHMARK(Method_A)->UseRealTime();
// 在 `CPU` 列展示总的 CPU 消耗时间，并使用该时间作为基准。适用于测量多线程程序的总 CPU 消耗时间
BENCHMARK(Method_A)->MeasureProcessCPUTime();
// 综合使用，在 `CPU` 列展示总的 CPU 消耗时间，但使用时钟时间作为基准
BENCHMARK(Method_A)->MeasureProcessCPUTime()->UseRealTime();
```

支持手动忽略代码片段的耗时统计，如：

```cpp
static void Method_A(benchmark::State& state) {
  for (auto _ : state) {
    state.PauseTiming();
    // ...
    // 忽略之间的耗时统计
    state.ResumeTiming();
    // ..
  }
}
```

支持设置输出结果的时间单位，如：

```cpp
BENCHMARK(Method_A)->Unit(benchmark::kSecond);
```

### **防止编译期优化**

在代码中，变量可能因为没有被使用而被编译器优化，使用 `benchmark::DoNotOptimize` 可防止该行为，如：

```cpp
static void Method_A(benchmark::State& state) {
  for (auto _ : state) {
      int x = 0;
      for (int i=0; i < 64; ++i) {
        benchmark::DoNotOptimize(x += i);
      }
  }
}
```

注意的是，`benchmark::DoNotOptimize` 不会防止编译期优化表达式里的行为。

使用 `benchmark::ClobberMemory` 确保编译器不会将内存访问优化掉，一般配合 `benchmark::DoNotOptimize` 使用，如：

```cpp
static void Method_A(benchmark::State& state) {
  for(auto _ : state) {
    std::vector<int> v(state.range(0), state.range(0));
    auto data = v.data();
    benchmark::DoNotOptimize(data);
    benchmark::ClobberMemory();
  }
}
```

### **注意与个人推荐写法**

除了 `counters` 变量外，应该把和方法实现相关的变量定义在 `for (auto _ : state)` 内部。因为 `for (auto _ : state)` 在框架里会运行多次，以便取得相对稳定的结果。若把可变的变量声明在外部，会导致方法实现有误。如把 `vector` 错误声明在外部，除了导致方法实现与预期不符，还可能会造成 oom，如：

```cpp
// 错误，还会导致 oom
static void Method_A(benchmark::State& state) {
  std::vector<int> v;
  v.reserve(state.range(0));
  for (auto _ : state) {
    for (int i = 0; i < state.range(0); ++i) {
      v.push_back(1);
    }
  }
}
BENCHMARK(Method_A)->Arg(1);

// 正确
static void Method_A(benchmark::State& state) {
  for (auto _ : state) {
    std::vector<int> v;
    v.reserve(state.range(0));
    for (int i = 0; i < state.range(0); ++i) {
      v.push_back(1);
    }
  }
}
BENCHMARK(Method_A)->Arg(1);
```

个人推荐写法，单独写一个函数实现待测量的方法，如：

```cpp
// 单独写一个函数
void _Method_A(benchmark::State& state) {
  std::vector<int> v;
  v.reserve(state.range(0));
    for (int i = 0; i < state.range(0); ++i) {
      v.push_back(1);
    }
}
// 在 `for (auto _ : state)` 里调用上述函数
static void Method_A(benchmark::State& state) {
  for (auto _ : state) {
    _Method_A(state);
  }
}
BENCHMARK(Method_A)->Arg(1);
```

### **命令行选项**

运行二进制时，还可以设置一些运行参数，不得不说 Google 的库真为用户着想！加上 `--help` 命令运行后，可以显示所有可设置的参数列表，如：

```powershell
% ./reserve --help
benchmark [--benchmark_list_tests={true|false}]
          [--benchmark_filter=<regex>]
          [--benchmark_min_time=`<integer>x` OR `<float>s` ]
          [--benchmark_min_warmup_time=<min_warmup_time>]
          [--benchmark_repetitions=<num_repetitions>]
          [--benchmark_enable_random_interleaving={true|false}]
          [--benchmark_report_aggregates_only={true|false}]
          [--benchmark_display_aggregates_only={true|false}]
          [--benchmark_format=<console|json|csv>]
          [--benchmark_out=<filename>]
          [--benchmark_out_format=<json|console|csv>]
          [--benchmark_color={auto|true|false}]
          [--benchmark_counters_tabular={true|false}]
          [--benchmark_context=<key>=<value>,...]
          [--benchmark_time_unit={ns|us|ms|s}]
          [--v=<verbosity>]
```

个人常用的选项有：

-   `--benchmark_filter` 指定运行某些测量方法。
-   `--benchmark_repetitions` 指定运行次数。
-   `--benchmark_out_format` 指定输出不同格式的结果，方便后处理。

剩余的读者可自行探索。

### **其他**

还有一些不那么常用的设置，如：

```cpp
// 修改测量结果中显示的 benchmark 名
BENCHMARK(Method_A)->Name("Method_B");

// 方便统计方法处理 Bytes 的速度
state.SetBytesProcessed(YourBytes);

// 另一种生成、注册和运行 benchmark 的方法
auto Method_A = [](benchmark::State& st, auto Inputs) { /* ... */ };
int main(int argc, char** argv) {
  for (auto& test_input : { /* ... */ })
      benchmark::RegisterBenchmark(test_input.name(), Method_A, test_input);
  benchmark::Initialize(&argc, argv);
  benchmark::RunSpecifiedBenchmarks();
  benchmark::Shutdown();
}
```

另外，该库还支持对模板进行 benchmark，对多线程进行 benchmark、可以自定义测量时间等，有需要时再深入了解。

## **性能对比**

为了更好地展示性能的对比结果，该库还贴心准备了一个 `compare.py` 脚本，在 `tools` 目录下。使用该脚本可以对比不同方法的测量结果，方便展现（ppt 汇报），常用方式：

```cpp
# 对比不同程序中同名方法的测量结果，a.out 里的方法是 baseline
$ ./compare.py benchmarks ./a.out ./b.out

# 对比同一程序中不同方法的测量结果，method_a 是 baseline
$ ./compare.py filters ./a.out method_a method_b

# 对比不同程序中不同方法的测量结果，method_a 是 baseline
$ ./compare.py benchmarksfiltered ./a.out method_a ./b.out method_b
```

简单给个输出的例子：

```text
Benchmark                                                 Time             CPU      Time Old      Time New       CPU Old       CPU New
--------------------------------------------------------------------------------------------------------------------------------------
[reserve vs. no_reserve]/8/real_time                   +1.1429         +1.1430            73           156            73           155
[reserve vs. no_reserve]/64/real_time                  +0.4568         +0.4567           459           669           459           669
[reserve vs. no_reserve]/512/real_time                 +0.1816         +0.1831          3293          3891          3289          3891
[reserve vs. no_reserve]/4096/real_time                +1.3172         +1.3169         23971         55545         23970         55537
[reserve vs. no_reserve]/8192/real_time                +1.7580         +1.7597         47579        131222         47536        131186
OVERALL_GEOMEAN                                        +0.3746         +0.3748             0             0             0             0
```

`Time Old` 列表示 baseline 执行的时钟时间，`Time New` 列表示要对比方法的时钟时间；`CPU Old` 列和 `CPU NEW` 列同理可得。`Time` 列和 `CPU` 列通过 `(new - old) / |old|` 计算所得。上述结果中，可以看出 `reserve` 方法更高效。

目前只支持对比两个方法，或许可以看看怎么支持多个方法的对比~

[tools](https://link.zhihu.com/?target=https%3A//github.com/google/benchmark/blob/main/docs/tools.md)里还提到了一些统计学理论，有兴趣的读者也可以研究研究。

## **快速使用**

我编写了一个简单的、能快速运行自定义 benchmark 的工程模版 [quick\_bench](https://link.zhihu.com/?target=https%3A//github.com/Xiaoccer/quick_bench.git)，方便大家使用，方式如下：

### **拉取项目**

```powershell
git clone --recurse-submodules https://github.com/Xiaoccer/quick_bench.git
```

### **编写自定义用例**

在 `benchmark` 目录下编写自己的测量用例，并在 `benchmark/CMakeLists.txt` 里添加对应文件。

### **配置 cmake**

```powershell
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -S . -B "build"
```

默认使用 C++17 标准和 -O3 优化级别进行编译。

### **编译**

```powershell
cd build && make -j && make install
```

生成的二进制在 `build/output` 目录下。

我把 `compare.py` 运行相关的文件也拷贝到里面了，若要使用需安装 python3.10 及以上的版本，并通过 `pip` 安装对应的包：

```powershell
pip3 install -r requirements.txt
```

当然还有更简洁的方法，网速好的可以直接使用早有大佬开发的网页版 benchmark, [地址](https://link.zhihu.com/?target=https%3A//quick-bench.com/)。

