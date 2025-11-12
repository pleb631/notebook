# 机器学习

## 1. 基本

机器学习的方法一般主要由三部分构成：模型、策略和算法，可以认为：

机器学习方法 =模型 +策略 +算法

- 模型：总结数据的内在规律，用数学语言描述的参数系统

- 策略：选取最优模型的评价准则

- 算法：选取最优模型的具体方法

## 2.特征工程

**特征工程**（Feature Engineering）是机器学习过程中非常重要的一步，指的是通过对原始数据的处理、转换和构造，生成新的特征或选择有效的特征，从而提高模型的性能。简单来说，特征工程是将原始数据转换为可以更好地表示问题的特征形式，帮助模型更好地理解和学习数据中的规律。优秀的特征工程可以显著提高模型的表现；反之，忽视特征工程可能导致模型性能欠佳。

实际上，特征工程是一个**迭代过程**。特征工程取决于具体情境。它需要大量的数据分析和领域知识。其中的原因在于，特征的有效编码可由所用的模型类型、预测变量与输出之间的关系以及模型要解决的问题来确定。在此基础上，辅以不同类型的数据集（如文本与图像）则可能更适合不同的特征工程技术。因此，要具体说明如何在给定的机器学习算法中最好地实施特征工程可能并非易事。

### 2.1 生成特征的方向

#### 2.1.1特征选择

从原始特征中挑选出与目标变量关系最密切的特征，剔除冗余、无关或噪声特征。这样可以减少模型的复杂度、加速训练过程、并减少过拟合的风险。

特征选择不会创建新特征，也不会改变数据结构。

（1）过滤法

基于统计测试（如卡方检验、相关系数、信息增益等）来评估特征与目标变量之间的关系，选择最相关的特征。

（2）包裹法

使用模型（如递归特征消除 RFE）来评估特征的重要性，并根据模型的表现进行特征选择。

（3）嵌入法

使用模型本身的特征选择机制（如决策树的特征重要性，L1正则化的特征选择）来选择最重要的特征。

#### 2.1.2特征转换

对数据进行数学或统计处理，使其变得更加适合模型的输入要求。

（1）归一化（Normalization）

将特征缩放到特定的范围（通常是0到1之间）。适用于对尺度敏感的模型（如KNN、SVM）。

（2）标准化（Standardization）

通过减去均值并除以标准差，使特征的分布具有均值0，标准差1。

（3）对数变换

对于有偏态的分布（如收入、价格等），对数变换可以将其转化为更接近正态分布的形式。

（4）类别变量的编码

独热编码：将类别型变量转换为二进制列，常用于无序类别特征。

标签编码：将类别型变量映射为整数，常用于有序类别特征。

目标编码：将类别变量的每个类别替换为其对应目标变量的平均值或其他统计量。

频率编码：将类别变量的每个类别替换为该类别在数据集中的出现频率。

#### 2.1.3特征构造

特征构造是基于现有的特征创造出新的、更有代表性的特征。通过组合、转换、或者聚合现有的特征，形成能够更好反映数据规律的特征。

（1）交互特征

将两个特征组合起来，形成新的特征。例如，两个特征的乘积、和或差等。

例如，将年龄与收入结合创建新的特征，可能能更好地反映某些模式。

（2）统计特征

从原始特征中提取统计值，例如求某个时间窗口的平均值、最大值、最小值、标准差等。

例如，在时间序列数据中，你可以从原始数据中提取每个小时、每日的平均值。

（3）日期和时间特征

从日期时间数据中提取如星期几、月份、年份、季度等特征。

例如，将“2000-01-01”转换为“星期几”、“是否节假日”、“月初或月末”等特征。

#### 2.1.4特征降维

当数据集的特征数量非常大时，特征降维可以帮助减少计算复杂度并避免过拟合。通过降维方法，可以在保持数据本质的情况下减少特征的数量。

（1）主成分分析（PCA）

通过线性变换将原始特征映射到一个新的空间，使得新的特征（主成分）尽可能地保留数据的方差。

（2）线性判别分析（LDA）

一种监督学习的降维方法，通过最大化类间距离与类内距离的比率来降维。

（3）t-SNE（t分布随机近邻嵌入）

一种非线性的降维技术，特别适合可视化高维数据。

（4）自编码器（Auto Encoder）

一种神经网络模型，通过压缩编码器来实现数据的降维。

### 2.2 常用方法

对于一个模型来说，有些特征可能很关键，而有些特征可能用处不大。

例如：

某个特征取值较接近，变化很小，可能与结果无关。

某几个特征相关性较高，可能包含冗余信息。

因此，**特征选择** 在特征工程中是最基本、也最常见的操作。

另外，在训练模型时有时也会遇到维度灾难，即特征数量过多。我们希望能在确保不丢失重要特征的前提下减少维度的数量，来降低训练模型的难度。所以在特征工程中，也经常会用到 **特征降维** 方法。

#### 2.2.1低方差过滤法

对于特征的选择，可以直接基于方差来判断，这是最简单的。低方差的特征意味着该特征的所有样本值几乎相同，对预测影响极小，可以将其去掉。

```python
from sklearn.feature_selection import VarianceThreshold

# 低方差过滤：删除方差低于 0.01 的特征
var_thresh = VarianceThreshold(threshold=0.01)
X_filtered = var_thresh.fit_transform(X)

```

#### 2.2.2相关系数法

通过计算特征与目标变量或特征之间的相关性，筛选出高相关性特征（与目标相关）或剔除冗余特征（特征间高度相关）。

（1）皮尔逊相关系数

皮尔逊相关系数（Pearson Correlation）用于衡量两个变量的线性相关性，取值范围。

$r=\frac{\Sigma_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\Sigma_i(x_i-\bar{x})^2}\Sigma{y_i-\bar{y})^2}}$

例如，现有一数据集包括不同渠道广告投放金额与销售额。

使用`pandas.DataFrame.corrwith(method="pearson")`计算各个特征与标签间的皮尔逊相关系数。

```python
import pandas as pd

advertising = pd.read_csv("data/advertising.csv")
advertising.drop(advertising.columns[0], axis=1, inplace=True)
advertising.dropna(inplace=True)
X = advertising.drop("Sales", axis=1)
y = advertising["Sales"]
# 计算皮尔逊相关系数
print(X.corrwith(y, method="pearson"))
# TV           0.782224
# Radio        0.576223
# Newspaper    0.228299
# dtype: float64


import seaborn as sns
import matplotlib.pyplot as plt

# 计算皮尔逊相关系数矩阵
corr_matrix = advertising.corr(method="pearson")
# 可视化热力图
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")
plt.show()

```

（2）斯皮尔曼相关系数

斯皮尔曼相关系数的定义是等级变量之间的皮尔逊相关系数。用于衡量两个变量之间的单调关系，即当一个变量增加时，另一个变量是否总是增加或减少（不要求是线性关系）。适用于非线性关系或数据不符合正态分布的情况。

$r_s=1-\frac{6\Sigma d_i^2}{n(n^2-1)}$

其中：

d  是两个变量的等级之差

n 是样本数

斯皮尔曼相关系数的取值范围为[-1,1]

例如，现有一组每周学习时长与数学考试成绩的数据：

![](ml.assets/QQ_1761914618056.png)

按数值由小到大排出x,y的等级，并计算等级差：

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/QQ_1761914671422.png)

```python
import pandas as pd

# 每周学习时长
X = [[5], [8], [10], [12], [15], [3], [7], [9], [14], [6]]
# 数学考试成绩
y = [55, 65, 70, 75, 85, 50, 60, 72, 80, 58]
# 计算斯皮尔曼相关系数
X = pd.DataFrame(X)
y = pd.Series(y)
print(X.corrwith(y, method="spearman"))
# 0.987879

```

#### 2.2.3主成分分析（PCA）

主成分分析（Principal Component Analysis，PCA）是一种常用的降维技术，通过线性变换将高维数据投影到低维空间，同时保留数据的主要变化模式。

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

n_samples = 1000

component1 = np.random.normal(0, 1, n_samples)
component2 = np.random.normal(0, 0.2, n_samples)

noise = np.random.normal(0, 0.1, n_samples)
# 构造3维数据
X = np.vstack([component1 - component2, component1 + component2, component2 + noise]).T

# 标准化
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

# 应用PCA，将3维数据降维到2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_standardized)

# 可视化
# 转换前的3维数据可视化
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(121, projection="3d")
ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c="g")

ax1.set_title("Before PCA (3D)")
ax1.set_xlabel("Feature 1")
ax1.set_ylabel("Feature 2")
ax1.set_zlabel("Feature 3")
# 转换后的2维数据可视化
ax2 = fig.add_subplot(122)
ax2.scatter(X_pca[:, 0], X_pca[:, 1], c="g")
ax2.set_title("After PCA (2D)")
ax2.set_xlabel("Principal Component 1")
ax2.set_ylabel("Principal Component 2")
plt.show()

```

## 3. 入门案例

### 3.1 KNN工作原理

K近邻算法属于监督学习算法。其核心思想是通过计算给定样本与数据集中所有样本的距离，找到距离最近的K个样本，然后根据这K个样本的类别或值来预测当前样本的类别或值。

1. 分类任务：统计K个近邻各类别的数量，将待分类样本归为数量最多的类别。

   ```python
   from sklearn.neighbors import KNeighborsClassifier
   
   knn = KNeighborsClassifier(n_neighbors=2)  # KNN分类模型，K值为2
   X = [[2, 1], [3, 1], [1, 4], [2, 6]]  # 特征
   y = [0, 0, 1, 1]  # 标签
   knn.fit(X, y)  # 模型训练
   knn.predict([[4, 9]])  # 预测
   
   ```

2. 回归任务：取K个近邻的平均值作为预测结果。

   ```python
   from sklearn.neighbors import KNeighborsRegressor
   
   knn = KNeighborsRegressor(n_neighbors=2)  # KNN回归模型，K值为2
   X = [[2, 1], [3, 1], [1, 4], [2, 6]]  # 特征
   y = [0.5, 0.33, 4, 3]  # 标签
   knn.fit(X, y)  # 模型训练
   knn.predict([[4, 9]])  # 预测
   
   ```

### 3.2距离度量方法

欧式距离：$d(x,y)=\sqrt{\Sigma_i(x_i-y_i)^2}$

曼哈顿距离 $d(x,y)=\Sigma_i|x_i-y_i|$

切比雪夫距离  $d(x,y)=max|x_i-y_i|$

闵可夫斯基距离 $d(x,y)=(\Sigma_i|x_i-y_i|^p)^{\frac{1}{p}}$

### 3.3 归一化与标准化

#### 3.3.1 归一化

1）定义

将数据按比例缩放到一个固定范围$[x_{min},x_{max}]$,通常是[0,1]或[-1,1]

$x^{'}=\frac{x-x_{min}}{x_{max}-x_{min}}$

2）目的

- 消除量纲差异：不同特征的单位或量纲可能差异巨大（例如身高以米为单位，体重以千克为单位），归一化可消除这种差异，避免模型被大范围特征主导。

- 加速模型收敛：对于梯度下降等优化算法，归一化后特征处于相近的尺度，优化路径更平滑，收敛速度更快。

- 适配特定模型需求：某些模型（如神经网络、K近邻、SVM）对输入数据的范围敏感，归一化能显著提升其性能。

3）适用场景

归一化不改变原始分布形状，但对异常值比较敏感。当数据分布有明显边界（如图像像素值、文本词频），或模型对输入范围敏感时可以优先考虑归一化。

```python
from sklearn.preprocessing import MinMaxScaler

X = [[2, 1], [3, 1], [1, 4], [2, 6]]
# 归一化，区间设置为(-1,1)
X = MinMaxScaler(feature_range=(-1, 1)).fit_transform(X)
print(X)

```

#### 3.3.2 标准化

1）定义

将数据调整为均值为0、标准差为1的标准分布。

$x^{'}=\frac{x-\mu}{\sigma}$

其中$\mu$是均值，$\sigma$是标准差

2）目的

- 适应数据分布：将数据转换为均值为0、标准差为1的分布，适合假设数据服从正态分布的模型（如线性回归、逻辑回归）。

- 稳定模型训练：标准化后的数据对异常值的敏感度较低（相比归一化），鲁棒性更强。

- 统一特征尺度：与归一化类似，标准化也能消除量纲差异，但更关注数据的统计分布而非固定范围。

3）场景

大多数场景下标准化更通用，尤其是数据分布未知或存在轻微异常值时。

```python
from sklearn.preprocessing import StandardScaler

X = [[2, 1], [3, 1], [1, 4], [2, 6]]
# 标准化
X = StandardScaler().fit_transform(X)
print(X)

```

### 3.4 案例

Heart Disease数据集<https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset>

1）特征转换

数据集中包含多种类型的特征：

- 类别型特征（需要特殊处理）

 1. 胸痛类型：4种分类（名义变量）
 2. 静息心电图结果：3种分类（名义变量）
 3. 峰值ST段的斜率：3种分类（有序变量）
 4. 地中海贫血：4种分类（名义变量）

- 数值型特征（可直接标准化）：年龄、静息血压、胆固醇、最大心率、运动后的ST下降、主血管数量

- 二元特征（保持原样）：性别、空腹血糖、运动性心绞痛

对于类别型特征，直接使用整数编码的类别特征会被算法视为有序数值，导致错误的距离计算（例如：会认为 胸痛类型=1 和 胸痛类型=2 之间的差异比 胸痛类型=1和 胸痛类型=3之间差异更小，而实际上它们都是类别）。使用 **独热编码**可将类别特征转换为二元向量，消除虚假的顺序关系。

```python
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler # 独热编码和标准化
from sklearn.neighbors import KNeighborsClassifier
import joblib

# 加载数据集
heart_disease_data = pd.read_csv("../data/heart_disease.csv")

# 处理缺失值
heart_disease_data.dropna(inplace=True)

heart_disease_data.info()


X = heart_disease_data.drop("是否患有心脏病", axis=1)
y = heart_disease_data["是否患有心脏病"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# 特征工程
# 数值型特征
numerical_features = ["年龄", "静息血压", "胆固醇", "最大心率", "运动后的ST下降", "主血管数量"]
# 类别型特征
categorical_features = ["胸痛类型", "静息心电图结果", "峰值ST段的斜率", "地中海贫血"]
# 二元特征
binary_features = ["性别", "空腹血糖", "运动性心绞痛"]

# 创建一个列转换器
columnTransformer = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_features),
        ("cat", OneHotEncoder(drop="first"), categorical_features),
        ("bin", "passthrough", binary_features)
    ]
)

# 特征转换
X_train = columnTransformer.fit_transform(X_train)
X_test = columnTransformer.transform(X_test)

# 创建模型
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# 模型评估，计算预测准确率
score = knn.score(X_test, y_test)
print(score)

# 保存模型
joblib.dump(value=knn, filename="knn_model")

# 加载模型，对新数据进行预测
knn_loaded = joblib.load("knn_model")
y_pred = knn_loaded.predict(X_test[10:11])
print(f"预测类别：{y_pred}, 真实类别：{y_test[10]}")
```

### 3.5 网格搜索

网格搜索（Grid Search）是一种系统化的超参数调优方法，通过遍历预定义的超参数组合，找到使模型性能最优的参数配置。通过自动化调参避免手动试错，提高效率。

网格搜索通常嵌套交叉验证，与交叉验证结合以提高调参的可靠性：

- 外层循环：遍历参数网格中的每个参数组合。

- 内层循环：对每个参数组合使用交叉验证评估模型性能。

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

knn = KNeighborsClassifier()
# 网格搜索参数，K值设置为1到10
param_grid = {"n_neighbors": list(range(1, 10))}
# GridSearchCV(estimator=模型, param_grid=网格搜索参数, cv=k折交叉验证)
knn = GridSearchCV(estimator=knn, param_grid=param_grid, cv=10)

# 模型训练
knn.fit(x_train, y_train)
print(pd.DataFrame(knn.cv_results_))  # 所有交叉验证结果
print(knn.best_estimator_)  # 最佳模型
print(knn.best_score_)  # 最佳得分

# 使用最佳模型进行评估
knn = knn.best_estimator_
print(knn.score(x_test, y_test))

```

### 3.6 正则化

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge   # 线性回归模型，Lasso回归，岭回归
from sklearn.preprocessing import PolynomialFeatures    # 构建多项式特征
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error



plt.rcParams['font.sans-serif']=['KaiTi']
plt.rcParams['axes.unicode_minus']=False

# 1. 生成数据
X = np.linspace(-3, 3, 300).reshape(-1, 1)
y = np.sin(X) + np.random.uniform(low=-0.5, high=0.5, size=300).reshape(-1, 1)

# 画出散点图（2×3 子图）
fig, ax = plt.subplots(2, 3, figsize=(25, 12))
ax[0,0].scatter(X, y, c='y')
ax[0,1].scatter(X, y, c='y')
ax[0,2].scatter(X, y, c='y')
# plt.show()

# 2. 划分训练集和测试集（验证集）
trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=42)

# 过拟合情况（20次多项式）
poly20 = PolynomialFeatures(degree=20)
x_train = poly20.fit_transform(trainX)
x_test = poly20.fit_transform(testX)
print(x_train.shape)
print(x_test.shape)

# 一、不加正则化项

# 定义模型
model = LinearRegression()

# 4. 训练模型
model.fit(x_train, trainY)

# 5. 预测结果，计算误差
y_pred1 = model.predict(x_test)
test_loss1 = mean_squared_error(testY, y_pred1)

# 画出拟合曲线，并写出训练误差和测试误差
ax[0,0].plot(X, model.predict(poly20.fit_transform(X)), 'r')
ax[0,0].text(-3, 1, f"测试误差：{test_loss1:.4f}")
# 画所有系数的直方图
ax[1,0].bar(np.arange(21), model.coef_.reshape(-1))

# 二、加L1正则化项（Lasso回归）

# 定义模型
lasso = Lasso(alpha=0.01)

# 4. 训练模型
lasso.fit(x_train, trainY)

# 5. 预测结果，计算误差
y_pred2 = lasso.predict(x_test)
test_loss2 = mean_squared_error(testY, y_pred2)

# 画出拟合曲线，并写出训练误差和测试误差
ax[0,1].plot(X, lasso.predict(poly20.fit_transform(X)), 'r')
ax[0,1].text(-3, 1, f"测试误差：{test_loss2:.4f}")
# 画所有系数的直方图
ax[1,1].bar(np.arange(21), lasso.coef_.reshape(-1))

# 三、加L2正则化项（岭回归）

# 定义模型
ridge = Ridge(alpha=1)

# 4. 训练模型
ridge.fit(x_train, trainY)

# 5. 预测结果，计算误差
y_pred3 = ridge.predict(x_test)
test_loss3 = mean_squared_error(testY, y_pred3)

# 画出拟合曲线，并写出训练误差和测试误差
ax[0,2].plot(X, ridge.predict(poly20.fit_transform(X)), 'r')
ax[0,2].text(-3, 1, f"测试误差：{test_loss3:.4f}")
# 画所有系数的直方图
ax[1,2].bar(np.arange(21), ridge.coef_.reshape(-1))

plt.show()


```
