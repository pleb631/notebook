# 一、矩阵微积分

## 1.1常见公式



$$
\nabla_x(c)=0
$$

$$
\nabla_x(a^Tx)=a
$$

$$
\nabla_x(x^Tx)=2x
$$
$$
\nabla_x(x^TAx)=(A+A^T)x
$$
$$
\nabla_x\|Ax-b\|^2=2A^T(Ax-b)
$$

## 1.2一些推导

### 求导 $x^TAx$

令 $f(x)=x^TAx$。注意 $f(x)$ 是标量，因此

$$
x^TAx=(x^TAx)^T=x^TA^Tx.
$$

把 $A$ 分解为对称部分与反对称部分：

$$
A=\frac{A+A^T}{2}+\frac{A-A^T}{2}.
$$

反对称部分 $S=(A-A^T)/2$ 满足 $S^T=-S$，且对任意 $x$ 都有 $x^TSx=0$。因此二次型实际上只由对称部分决定：

$$
x^TAx=x^T\frac{A+A^T}{2}x.
$$

对对称矩阵 $B$，$\nabla_x(x^TBx)=2Bx$，从而

$$
\nabla_x(x^TAx)=2\cdot\frac{A+A^T}{2}x=(A+A^T)x.
$$

特别地，若 $A=A^T$，则

$$
\boxed{\nabla_x(x^TAx)=2Ax}.
$$

### 求导 $\|Ax-b\|^2$

令 $f(x)=\|Ax-b\|^2$。展开平方：

$$
\begin{aligned}
f(x)&=(Ax-b)^T(Ax-b)\\
&=x^TA^TAx-x^TA^Tb-b^TAx+b^Tb.
\end{aligned}
$$

中间两项都是标量，且 $x^TA^Tb=b^TAx$，故

$$
f(x)=x^TA^TAx-2b^TAx+b^Tb.
$$

由于 $A^TA$ 是对称矩阵，逐项求导得到

$$
\nabla_x f(x)=2A^TAx-2A^Tb
=2A^T(Ax-b)
$$



# 二、线性代数

## 2.1正交矩阵->QR分解->最小二乘法

### 正交矩阵由来

在二维平面中，取两个向量

$$
\alpha=(a_1,a_2),\qquad
\beta=(b_1,b_2)
$$

如果它们都是单位向量，并且彼此垂直，那么有：

$$
\|\alpha\|=1,\qquad \|\beta\|=1
$$

因此：

$$
a_1^2+a_2^2=1
$$

$$
b_1^2+b_2^2=1
$$

又因为 $\alpha,\beta$ 相互垂直，所以它们的内积为 0：

$$
\alpha\cdot\beta=0
$$

即：

$$
a_1b_1+a_2b_2=0
$$

同样：

$$
b_1a_1+b_2a_2=0
$$

于是可以把这四个关系统一写成矩阵形式。

设

$$
A=
\begin{bmatrix}
a_1&a_2\\
b_1&b_2
\end{bmatrix}
$$

这里 $A$ 的两行分别是向量 $\alpha,\beta$。

那么：

$$
AA^T
=
\begin{bmatrix}
a_1&a_2\\
b_1&b_2
\end{bmatrix}
\begin{bmatrix}
a_1&b_1\\
a_2&b_2
\end{bmatrix}
$$

乘开得到：

$$
AA^T
=
\begin{bmatrix}
a_1^2+a_2^2 & a_1b_1+a_2b_2\\
b_1a_1+b_2a_2 & b_1^2+b_2^2
\end{bmatrix}
$$

根据单位向量和正交条件：

$$
AA^T
=
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}
=I
$$

因此：

$$
\boxed{AA^T=I}
$$

对于方阵 $A$，这意味着：

$$
\boxed{A^{-1}=A^T}
$$

满足这个条件的矩阵称为**正交矩阵**。

所以可以把正交矩阵理解为：

$$
\boxed{
\text{由一组两两正交、长度为1的向量组成的方阵}
}
$$

如果这些正交单位向量按列排列，则有：

$$
A^TA=I
$$

如果按行排列，则有：

$$
AA^T=I
$$

对于方阵正交矩阵，两者同时成立：

$$
A^TA=AA^T=I
$$

### 施密特正交化

施密特正交化（Gram–Schmidt）本质上就做一件事：

$$
\boxed{\text{把一组线性无关向量，变成一组两两正交的单位向量}}
$$

给一组线性无关向量

$$
a_1,a_2,\dots,a_n
$$

依次处理。

先：

$$
q_1=\frac{a_1}{\|a_1\|}
$$

然后第二个向量减掉它在 $q_1$ 上的投影：

$$
u_2=a_2-(q_1^Ta_2)q_1
$$

再单位化：

$$
q_2=\frac{u_2}{\|u_2\|}
$$

第三个向量同理，减掉它在前面所有 $q$ 上的投影：

$$
u_3=a_3-(q_1^Ta_3)q_1-(q_2^Ta_3)q_2
$$

再单位化。

直观地说：**减去已知方向上的分量，留下垂直于这些方向的新分量；再把它缩放到单位长度。**

### QR分解

```python
# Q就是正交矩阵
Q, R = np.linalg.qr(A)
```

设 $A\in\mathbb R^{m\times n}$，$m\ge n$，且 $A$ 列满秩（即 $\operatorname{rank}(A)=n$）。对 $A$ 的列做 Gram–Schmidt，可得

$$
A=QR
$$
其中：$Q\in\mathbb R^{m\times n},\quad Q^TQ=I_n,
\qquad R\in\mathbb R^{n\times n}\ \text{为可逆上三角矩阵}.$



为什么是上三角矩阵呢？

因为 在施密特正交化时，每次生成新的正交基$a_j$，只会用到：
$$
q_1,\dots,q_j
$$

不会用到后面还没产生的：

$$
q_{j+1},q_{j+2},\dots
$$

所以左下角自然全是 0。



可逆情况：
$$
\text{方阵 QR：}Q\text{ 必可逆，}R\text{ 可逆}\iff A\text{ 可逆}
$$

$$
\text{瘦 QR：}Q\text{ 不可逆但有左逆 }Q^T,\quad
R\text{ 可逆}\iff A\text{ 列满秩}
$$



### 超定方程和最小二乘

```python
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
# x：最小二乘解
# residuals：残差平方和
# rank：A 的秩
# s：A的奇异值
# 核心公式如下
# x = np.linalg.inv(A.T @ A) @ A.T @ b
```

令 $A\in\mathbb R^{m\times n}$，通常 $m>n$。方程 $Ax=b$ 往往无精确解，因此寻找使残差最小的 $x$：我们要求：

$$
\min_x\|Ax-b\|^2
$$

由矩阵求导可得$\nabla_x f(x)=2A^TAx-2A^Tb$，令$\nabla_x f(x)=0$

若 $A$ 列满秩，则 $A^TA$ 可逆，最小二乘解唯一，则
$$
x=(A^TA)^{-1}A^Tb
$$
若 $A$ 不列满秩，$A^TA$ 不可逆，最小二乘解可能不唯一；此时不能直接使用该逆矩阵公式。

### 用 QR 分解求解最小二乘

在 $A$ 列满秩且 $A=QR$时，
$$
\|Ax-b\|^2=\|QRx-b\|^2.
$$

由 $Q^TQ=I$ 可得正规方程

$$
R^TRx=R^TQ^Tb.
$$

由于 $R$ 可逆，消去 $R^T$ 后有

$$
Rx=Q^Tb
$$

因此只需回代求上三角方程，而不必显式计算逆：

$$
x=R^{-1}Q^Tb
$$

这在数值上通常比计算 $(A^TA)^{-1}A^Tb$ 更可靠，因为形成 $A^TA$ 会放大条件数问题。

### 欠定方程与最小范数解

欠定系统中 $A\in\mathbb R^{m\times n}$ 且 $m<n$：未知数多于方程数。即便 $Ax=b$ 有解，解通常也不唯一。为了从无穷多个解中选出一个，常用准则是最小二范数：

$$
\min_x\|x\|\quad\text{s.t.}\quad Ax=b
$$

若 $A$ **行满秩**（$\operatorname{rank}(A)=m$），则 $AA^T$ 可逆，并且对任意 $b\in\mathbb R^m$，系统都有解。唯一的最小范数解为

$$
x=A^T(AA^T)^{-1}b=A^+b
$$

其中 $A^+$ 是 Moore–Penrose 伪逆。

为什么这正是最小范数解？令

$$
x_\star=A^T(AA^T)^{-1}b.
$$

首先 $Ax_\star=b$。任意其他解都可写成 $x=x_\star+z$，其中 $Az=0$。而 $x_\star\in\mathcal C(A^T)$，$z\in\mathcal N(A)$；这两个空间正交，所以

$$
\|x\|^2=\|x_\star\|^2+\|z\|^2\ge\|x_\star\|^2.
$$

等号仅当 $z=0$ 时成立，故 $x_\star$ 唯一地具有最小范数。

若 $A$ 不行满秩，或者 $Ax=b$ 本身不相容，通用的写法仍是 $x=A^+b$；它给出最小二乘解中范数最小的那个解。

### 岭回归

实际数据常含噪声，或者 $A$ 的列几乎线性相关。仅最小化残差时，解可能对数据的微小扰动极其敏感。岭回归在拟合误差之外惩罚过大的参数：

$$
\min_x\ \|Ax-b\|^2+\lambda\|x\|^2,
\qquad \lambda>0.
$$

其中第一项鼓励拟合数据，第二项鼓励较小、较稳定的 $x$；$\lambda$ 控制两者的权衡。

对目标函数求导并令其为零：

$$
2A^T(Ax-b)+2\lambda x=0,
$$

即

$$
(A^TA+\lambda I)x=A^Tb.
$$

因此

$$
x=(A^TA+\lambda I)^{-1}A^Tb
$$

只要 $\lambda>0$，矩阵 $A^TA+\lambda I$ 就是正定的、可逆的，即使 $A$ 不满列秩也成立。代价是引入偏差：$\lambda$ 越大，解通常越小、越稳定，但对训练数据的拟合会更弱。

## 2.2 SVD 分解

奇异值分解（Singular Value Decomposition，SVD）把一个矩阵拆成“两个正交变换 + 一次按坐标轴的缩放”。它不仅适用于方阵，也适用于任意 $m\times n$ 矩阵。本节先说明分解本身，再用它求解超定齐次方程组。

### SVD 的定义及性质

对任意实矩阵 $A\in\mathbb R^{m\times n}$，都可以写成

$$
\boxed{A=U\Sigma V^T.}
$$

其中：

- $U\in\mathbb R^{m\times m}$ 是正交矩阵，即 $U^TU=I$；$U$ 的列向量称为**左奇异向量**。
- $V\in\mathbb R^{n\times n}$ 是正交矩阵，即 $V^TV=I$；$V$ 的列向量称为**右奇异向量**。
- $\Sigma\in\mathbb R^{m\times n}$ 除主对角线外均为零；对角线元素 $\sigma_i\geq0$ 称为**奇异值**，通常约定

  $$
  \sigma_1\geq\sigma_2\geq\cdots\geq0.
  $$

从右往左看，矩阵 $A$ 的作用可理解为：先由 $V^T$ 改变输入坐标系，再由 $\Sigma$ 沿各轴缩放，最后由 $U$ 改变输出坐标系。

**两个重要性质**

设 $V=(v_1,v_2,\ldots,v_n)$，$U=(u_1,u_2,\ldots,u_m)$。

**1. 奇异向量的对应关系**

$$
Av_i=\sigma_i u_i.
$$

也就是说，右奇异向量 $v_i$ 经 $A$ 作用后，方向变成左奇异向量 $u_i$，长度变为原来的 $\sigma_i$ 倍。

**2. 与 $A^TA$ 的特征分解的关系**

$$
A^TA=V\Sigma^T\Sigma V^T.
$$

因此 $A^TA$ 的特征向量就是右奇异向量 $v_i$，对应特征值为 $\sigma_i^2$：

$$
A^TAv_i=\sigma_i^2v_i.
$$

这条性质正是后面求解问题的关键。

### SVD 求解超定齐次线性方程组

**问题：为什么不能直接解 $Ax=0$？**

设 $A\in\mathbb R^{m\times n}$，且 $m>n$。这表示方程个数多于未知数个数，因此称为**超定方程组**。若 $A$ 列满秩（$\operatorname{rank}(A)=n$），则

$$
Ax=0
$$

只有零解 $x=0$。

但在许多实际问题中，我们需要的不是零向量，而是一个非零方向 $x$，使得 $Ax$ 尽量接近零。于是问题写成

$$
\min_x\|Ax\|^2.
$$

这个式子有一个问题：$x=0$ 会让目标值变成 $0$，显然总是最优，却没有意义。

齐次方程中，$x$ 乘任意非零常数仍表示同一个方向。因此只需固定 $x$ 的长度，例如令

$$
\|x\|^2=1.
$$

最终要求解的是

$$
\boxed{
\hat{x}=\arg\min_{\|x\|^2=1}\|Ax\|^2
}.
$$

**第一步：把最小化问题变成特征值问题**

引入拉格朗日乘子 $\lambda$：

$$
L(x,\lambda)=\|Ax\|^2+\lambda(1-\|x\|^2).
$$

将范数展开：

$$
L(x,\lambda)=x^TA^TAx+\lambda(1-x^Tx).
$$

对 $x$ 求导并令其为零：

$$
\frac{\partial L}{\partial x}
=2A^TAx-2\lambda x=0.
$$

整理得到

$$
\boxed{A^TAx=\lambda x.}
$$

这正是特征值问题：满足约束最优解的 $x$，必须是 $A^TA$ 的一个特征向量。

那么该选哪一个特征向量？由上式和 $x^Tx=1$ 可得

$$
\begin{aligned}
\|Ax\|^2
&=x^TA^TAx\\
&=x^T(\lambda x)\\
&=\lambda x^Tx\\
&=\lambda.
\end{aligned}
$$

因此，残差 $\|Ax\|^2$ 恰好等于所选特征向量对应的特征值。要让残差最小，就应选取 $A^TA$ 的**最小特征值**对应的特征向量。

**第二步：SVD 告诉我们这个特征向量是什么**

对 $A$ 做奇异值分解：

$$
A=U\Sigma V^T,
$$

其中奇异值按从大到小排列：

$$
\sigma_1\geq\sigma_2\geq\cdots\geq\sigma_n\geq0.
$$

设

$$
V=(v_1,v_2,\ldots,v_n).
$$

将 SVD 代入 $A^TA$：

$$
\begin{aligned}
A^TA
&=(U\Sigma V^T)^T(U\Sigma V^T)\\
&=V\Sigma^TU^TU\Sigma V^T\\
&=V\Sigma^T\Sigma V^T.
\end{aligned}
$$

因为 $V$ 的列向量 $v_i$ 构成一组正交基，所以

$$
A^TAv_i=\sigma_i^2v_i.
$$

这说明：

- $A^TA$ 的特征值是 $\sigma_1^2,\sigma_2^2,\ldots,\sigma_n^2$；
- 对应的特征向量分别是 $v_1,v_2,\ldots,v_n$。

由于最小特征值是 $\sigma_n^2$，其对应特征向量就是 $v_n$，即 $V$ 的最后一列。因此

$$
\boxed{\hat{x}=v_n.}
$$

同时有

$$
\boxed{\|A\hat{x}\|^2=\sigma_n^2.}
$$

**结论**

对于列满秩的超定齐次方程组，求单位向量中使 $\|Ax\|^2$ 最小的近似解：

$$
\boxed{
A=U\Sigma V^T
\quad\Longrightarrow\quad
\hat{x}=V\text{ 的最后一列}=v_n.
}
$$

若最小奇异值 $\sigma_n=0$，则 $v_n$ 满足 $Av_n=0$，它是精确的非零解；若 $\sigma_n>0$，则 $v_n$ 是最小二乘意义下最接近零空间的方向。

**NumPy 实现**

```python
import numpy as np

# A 的形状为 (m, n)，并且 m > n
U, S, Vt = np.linalg.svd(A)

x = Vt[-1]       # V 的最后一列 v_n（转置后即 Vt 的最后一行）
residual = S[-1]  # ||A @ x||
```

# 三、概率解释与正则化

第 2.1 节从优化角度定义了最小二乘问题：

$$
\min_x \|Ax-b\|^2.
$$

实际上，最小二乘还可以从**概率模型和最大似然估计**自然推导出来。

---

## 3.1 从线性模型开始

假设观测数据满足线性关系

$$
b=Ax+\varepsilon,
$$

其中

* $A\in\mathbb R^{m\times n}$ 为已知设计矩阵；
* $x\in\mathbb R^n$ 为待估计参数；
* $b\in\mathbb R^m$ 为观测值；
* $\varepsilon$ 为测量噪声。

假设每个观测的噪声相互独立，并服从均值为 $0$、方差为 $\sigma^2$ 的高斯分布：

$$
\varepsilon_i\sim\mathcal N(0,\sigma^2).
$$

于是对于第 $i$ 个观测，有

$$
b_i=a_i^Tx+\varepsilon_i,
$$

因此

$$
b_i\mid x\sim\mathcal N(a_i^Tx,\sigma^2).
$$

也就是说：

$$
p(b_i\mid x)
=
\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left(
-\frac{(b_i-a_i^Tx)^2}{2\sigma^2}
\right).
$$

---

## 3.2 最大似然估计

由于假设各个样本的噪声相互独立，因此观测向量的联合概率密度为

$$
p(b\mid x)
=
\prod_{i=1}^{m}p(b_i\mid x).
$$

这就是似然函数：

$$
L(x)=p(b\mid x).
$$

最大似然估计希望找到一个 $x$，使当前观测数据 $b$ 的似然最大：

$$
\hat x_{\mathrm{MLE}}
=
\arg\max_x p(b\mid x).
$$

将高斯分布代入：

$$
p(b\mid x)
=
\left(\frac{1}{\sqrt{2\pi\sigma^2}}\right)^m
\exp\left(
-\frac{1}{2\sigma^2}
\sum_{i=1}^{m}(b_i-a_i^Tx)^2
\right).
$$

由于乘积形式不方便处理，通常取对数：

$$
\log p(b\mid x)
=
-\frac{m}{2}\log(2\pi\sigma^2)
-\frac{1}{2\sigma^2}
\sum_{i=1}^{m}(b_i-a_i^Tx)^2.
$$

第一项与 $x$ 无关，因此最大化对数似然等价于最小化

$$
\sum_{i=1}^{m}(b_i-a_i^Tx)^2.
$$

写成矩阵形式就是

$$
\boxed{
\hat x_{\mathrm{MLE}}
=
\arg\min_x\|Ax-b\|^2
}.
$$

因此：

$$
\boxed{
\text{高斯噪声假设}
+\text{最大似然估计}
\Longrightarrow
\text{最小二乘}
}
$$

这也给出了平方误差的概率意义：

> 在独立、同方差的高斯观测噪声模型下，最小化平方误差等价于最大似然估计。

---

## 3.3 从最大似然到最大后验估计

最大似然估计只考虑

$$
p(b\mid x),
$$

即：

> 在参数 $x$ 已知的情况下，当前数据 $b$ 出现的可能性有多大？

如果我们还对参数 $x$ 本身具有一定先验认识，就可以使用贝叶斯公式：

$$
p(x\mid b)
=
\frac{p(b\mid x)p(x)}{p(b)}.
$$

其中：

* $p(b\mid x)$：似然；
* $p(x)$：参数的先验分布；
* $p(x\mid b)$：观察数据之后参数的后验分布。

最大后验估计（MAP）寻找：

$$
\hat x_{\mathrm{MAP}}
=
\arg\max_x p(x\mid b).
$$

由于 $p(b)$ 与 $x$ 无关：

$$
\hat x_{\mathrm{MAP}}
=
\arg\max_x p(b\mid x)p(x).
$$

取负对数后：

$$
\boxed{
\hat x_{\mathrm{MAP}}
=
\arg\min_x
\left[
-\log p(b\mid x)
-\log p(x)
\right]
}
$$

因此可以理解为：

$$
\boxed{
\text{MAP}
=
\text{数据拟合项}
+
\text{先验约束项}
}
$$

而机器学习中的很多**正则化项**，实际上都可以解释成某种参数先验。

---

## 3.4 高斯先验与岭回归

仍然假设观测噪声为高斯分布：

$$
b\mid x\sim\mathcal N(Ax,\sigma^2I).
$$

因此负对数似然中与 $x$ 有关的部分为

$$
-\log p(b\mid x)
\propto
\frac{1}{2\sigma^2}\|Ax-b\|^2.
$$

现在进一步假设参数 $x$ 本身也服从零均值高斯分布：

$$
x\sim\mathcal N(0,\tau^2I).
$$

于是

$$
p(x)
\propto
\exp\left(
-\frac{1}{2\tau^2}\|x\|^2
\right),
$$

因此

$$
-\log p(x)
\propto
\frac{1}{2\tau^2}\|x\|^2.
$$

MAP 估计就变成

$$
\hat x_{\mathrm{MAP}}
=
\arg\min_x
\left[
\frac{1}{2\sigma^2}\|Ax-b\|^2
+
\frac{1}{2\tau^2}\|x\|^2
\right].
$$

整体乘以 $2\sigma^2$ 不会改变最优解：

$$
\hat x_{\mathrm{MAP}}
=
\arg\min_x
\left[
\|Ax-b\|^2
+
\frac{\sigma^2}{\tau^2}\|x\|^2
\right].
$$

令

$$
\lambda=\frac{\sigma^2}{\tau^2},
$$

就得到第 2.1 节的岭回归目标函数。该节已给出求导过程和闭式解；这里补充其概率来源：**高斯观测噪声 + 高斯参数先验 + MAP 估计，对应岭回归**。

高斯先验意味着我们认为：

> 参数通常应该靠近 $0$，特别大的参数出现概率较低。

所以岭回归会倾向于把参数整体向 $0$ 收缩。

---

## 3.5 拉普拉斯先验与 Lasso

如果不对参数使用高斯先验，而是假设每个参数独立服从**拉普拉斯分布（Laplace distribution）**：

$$
p(x_i)
=
\frac{1}{2s}
\exp\left(
-\frac{|x_i|}{s}
\right).
$$

那么所有参数的联合先验为

$$
p(x)
\propto
\exp\left(
-\frac{1}{s}\sum_i|x_i|
\right).
$$

由于

$$
\sum_i|x_i|=\|x\|_1,
$$

因此：

$$
-\log p(x)
\propto
\frac{1}{s}\|x\|_1.
$$

如果观测噪声仍为独立同方差的高斯噪声，将负对数后验乘以 $2\sigma^2$ 后，令 $\lambda=2\sigma^2/s$，就得到 **Lasso（L1 正则化）**：

$$
\boxed{
\hat x
=
\arg\min_x
\left(
\|Ax-b\|^2+\lambda\|x\|_1
\right)
}
$$

因此：

$$
\boxed{
\text{高斯似然}
+
\text{拉普拉斯参数先验}
+
\text{MAP}
\Longrightarrow
\text{Lasso}
}
$$

拉普拉斯分布在 $0$ 附近比高斯分布更加尖锐，因此 L1 正则化更倾向于直接把部分参数压到 $0$，从而产生**稀疏解**。

---

## 3.6 高斯先验与拉普拉斯先验的区别

两种正则化可以统一理解为对参数 $x$ 的不同概率假设：

| 概率假设         | 优化形式                      | 方法    | 典型效果   |
| ------------ | ------------------------- | ----- | ------ |
| 不加参数先验       | $\lVert Ax-b\rVert_2^2$                | 最小二乘  | 单纯拟合数据 |
| $x$ 服从高斯分布   | $\lVert Ax-b\rVert_2^2+\lambda\lVert x\rVert_2^2$ | Ridge | 参数整体变小 |
| $x$ 服从拉普拉斯分布 | $\lVert Ax-b\rVert_2^2+\lambda\lVert x\rVert_1$   | Lasso | 参数趋于稀疏 |

所以正则化并不只是人为给损失函数“加一项”，从概率角度看：

$$
\boxed{
\text{正则化项}
\quad\Longleftrightarrow\quad
-\log p(x)
}
$$

即**正则化实际上是在给参数加入先验分布**。

---

## 3.7 拉普拉斯噪声与最小绝对偏差

需要区分：

* **参数 $x$ 使用拉普拉斯先验** $\rightarrow$ Lasso；
* **观测噪声 $\varepsilon$ 服从拉普拉斯分布** $\rightarrow$ L1 残差。

如果假设

$$
\varepsilon_i\sim\operatorname{Laplace}(0,s),
$$

那么

$$
p(b_i\mid x)
\propto
\exp\left(
-\frac{|b_i-a_i^Tx|}{s}
\right).
$$

最大似然估计得到：

$$
\boxed{
\hat x
=
\arg\min_x
\sum_i|b_i-a_i^Tx|
=
\arg\min_x\|Ax-b\|_1
}
$$

这称为**最小绝对偏差（Least Absolute Deviations，LAD）**。

因此可以把几个关系总结成：

$$
\boxed{
\begin{aligned}
\text{高斯噪声}+\mathrm{MLE}
&\Longrightarrow L_2\text{ 残差}\\
\text{拉普拉斯噪声}+\mathrm{MLE}
&\Longrightarrow L_1\text{ 残差}\\
\text{高斯噪声}+\text{高斯先验}+\mathrm{MAP}
&\Longrightarrow \text{Ridge}\\
\text{高斯噪声}+\text{拉普拉斯先验}+\mathrm{MAP}
&\Longrightarrow \text{Lasso}
\end{aligned}
}
$$

从这个角度看，损失函数中的范数并不是凭空选择出来的，而是可以对应到具体的概率分布假设。
