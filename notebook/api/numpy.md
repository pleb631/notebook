# numpy

| 模块/方法                         | 作用                          | 备注        |
| --------------------------------- | ----------------------------- | ----------- |
| np.stack((arr1,arry2,...),axis=0) | 把指定array按新的维度进行堆叠 | 维度默认为0 |
| np.linalg.matrix_power（gragh,n） | 计算图节点距离为n的节点       |             |
| np.ascontiguousarray(array)       | 使array在内存空间中连续       |             |
|np.alltrue(array）|检查是否所有元素都是True|array.all()同样功能，array.any()至少一个true则输出true
## CheatSheet

此处罗列部分相关 API 用法，以二维为主，多维可自行拓展。


| 说明 | 用法 |备注|
|------|-----|----|
||**创建和生成**|
|从list创建|`np.array(list)`|
|从range创建|`np.arange(int).reshape(int, int, ...)`|np.arange(start, end, step)可以指定范围和步长
|按线性间隔创建|`np.linspace(start, stop, num).reshape(int, int)`|
|从对数间隔创建|`np.logspace(start, stop, num, base).reshape(int, int)`|
|全1|`np.ones(int)`|
|全0|`np.zeros((int, int, ...))`|
|和给定array同shape的0向量|`np.zeros_like(array)`|
|随机 Generator|`rng = np.random.default_rng()`|
|随机整数|`rng.integers(low, high, (int, int))`|
|均匀分布|`rng.uniform(low, high, (int, int))`|
|标准正态分布|`rng.standard_normal((int, int))`|
|高斯分布|`rng.normal(loc, scale, (int, int))`|
|输出0-1 连续均匀分布的一个数|np.random.rand()|np.random.rand(dim1, dim2)与np.random.random((dim1, dim2))同样功能
|高斯分布|np.random.normal(low, high, (int, int))|
|存储单个array|`np.save(file, array)`|格式为npy
|存储多个array|`np.savez(file, name=array)`|格式为npz，np.savez("./data/b", a=np.arange(12).reshape(3, 4), b=np.arange(12.).reshape(4, 3))|
|存储多个array并压缩|`np.savez_compressed(file, name=array)`|与上一个无异
|加载|`np.load(file)`|可以加载npy、npz
||**统计和属性**|
|维度|`arr.ndim`|
|形状|`arr.shape`|
|数据个数|`arr.size`|
|按维度取最大值|`arr.max(aixs)`|
|按维度取最小值并保持维度|`arr.min(axis, keepdims=True)`|
|中位数|`np.median(arr)`|
|分位数|`np.quantile(arr, q, axis)`|
|求和|`np.sum(arr)`|
|按维度求均值|`np.average(arr, axis)`|
|按维度求累加和|`np.cumsum(arr, axis)`|
|标准差|np.std(arr)|
|方差|np.var(arr)|
||**形状和转换**|
|改变形状|`arr.reshape(int, int, ...)`|可以使用-1
|原地改变|`arr.resize(int, int, ...)`|如果新arr元素数量小于旧arr的，会发生截断。arr.resize((2,3), refcheck=False)，如果元素数量不够，则会用0填充
|展平|`arr.ravel()`|arr.flatten() ,返回copy
|扩展1维度|`np.expand_dims(arr, axis)`|
|去掉1维度|`np.squeeze(arr, axis)`|指定 axis 的shape必须为1
|反序|`arr[::-1]`|
|列反序|`arr[:, ::-1]`|
|行反序|`arr[::-1, :]`|
|二维转置|`arr.T`|
|高维转置|`np.transpose(arr, axes)`|
||**分解和组合**|
|删除元素|`np.delete(arr, 1, 0)`|删除arr的第0维的第1行
|索引|`arr[int]`|
|范围索引|`arr[int: int]`|
|离散索引|`arr[[int, int]]`|
|范围+离散|`arr[int:int, int]`|
|范围+范围|`arr[int:int, int:int]`|
|离散+离散|`arr[[int, int], [int, int]]`|
|步长跳跃|`arr[start: end: step]`|
|多维度步长跳跃|`arr[start: end: step, start: end: step]`|
|按维度拼接|`np.concatenate((arr1, arr2), axis)`|默认第0维
|按维度堆叠|`np.stack((arr1, arr2), axis)`|默认第0维，拓展新维度并堆叠
|重复|`np.repeat(arr, int, axis)`|
|按维度切分|`np.split(arr, parts, axis)`|
||**筛选和过滤**|
|筛选|`np.where(condition)`|会返回多个维度的坐标
|筛选后赋值|`np.where(condition, arr, not_satisfy_condition_with_new_val)`|如果不满足条件则用new_val替代
|提取|`np.extract(condition, arr)`|返回值，一维向量
|唯一值|`np.unique(arr)`|
|抽样|`np.random.choice(arr, int, bool)`|bool代表结果是否可以重复，返回坐标
|按维度取最大值index|`np.argmax(arr, axis)`|
|按维度排序的索引|`np.argsort(arr, axis)`|
|返回满足条件的索引|`np.argwhere(arr)`|
||**矩阵和运算**|
|四则运算| `arr [+-*/] num`                 |
|其他运算 | `np.[sqrt/floor/round/mod](arr)` |
|array乘法| `np.dot(arr1, arr2)`             |
|array乘法| `np.matnul(arr1, arr2)`          |
|点积     | `np.vdot(arr1, arr2)`            |np.sum(arr1*arr2)
|内积     | `np.inner(arr1, arr2)`           |向量的内积
|行列式   | `np.linalg.det(arr)`             |
|逆矩阵   | `np.linalg.inv(arr)`             |
|log|`np.log(arr)`|
|向下取整、向上取整|`np.floor（arr）`、`np.ceil(arr)`|
|四舍五入，保留int位|`np.round(arr,int)`|
|mod|`np.mod(arr, val)`|arr%val
|最小公倍数|`np.lcm(val1,val2)` or `np.lcm.reduce(list)`|后者可以对多个数同时
|最大公约数|`np.gcd(val1, val2)` or `np.gcd.reduce(list)`
|累差|`np.diff(arr，int，axis)`|沿着axis轴计算第int维的离散差值|`np.cumsum()`累加，`np.cumprod()` 累乘
|符号函数|`np.sign(arr)`|
|截断|`np.clip(arr,a_min,a_max)`
|多项式|`p = np.polynomial.Polynomial([3, 2, 1])`|`3x+2x+x**2`|`p.deriv()`为p的导数函数，`p.integ()`为P的定积分
|逻辑和|`np.logical_and(arr1,arr2)`|
|判断所有值是否在阈值范围内|`np.allclose`|
|叉积|`np.cross(a, b)`|外积 np.outer(a, b)，克罗内克积np.kron(a,b)
|以特征值为对角线的方阵|np.diag(list)
|Einsum|np.einsum()