[toc]

## 经典论文

- Googlenet

![asd](https://thumbnail1.baidupcs.com/thumbnail/dfc730f46p9e899abfdf441a53d77b5d?fid=2652311658-250528-525722132197257&rt=pr&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-Hj8lasb3LrsFRbfWSTURmqHbLy4%3d&expires=8h&chkbd=0&chkv=0&dp-logid=8737040498903573115&dp-callid=0&time=1674982800&size=c1920_u1080&quality=90&vuk=2652311658&ft=image&autopolicy=1)

文章一上来首先表明了提高网络性能的方法就是增加网络的深度和宽度，

但是会有两个缺点：

1. 这样不可避免的带来参数量的增加，训练集过小时会导致过拟合。
2. 造成了计算资源的浪费（大量神经元的权重接近零），实践中计算资源有限

作者认为把全连接的结构转化为稀疏连接的结构，参考Hebbian principle，提出**Inception模块**，这个模块的最重要的作用就是让神经网络在学习的过程中自发的选择合适的路径或感受野，从而增加模型的**稀疏性**。



## 理解

### 模型的稀疏性

这表现在两方面，第一是模型参数的稀疏性，模型权重只有一小部分不为0，其他都为0。另一方面是每一层提取特征的稀疏性，对于输出结果判断无用的特征（噪声特征）应给予抑制，使其置0，只保留对结果判断、拉大类间距离有用的特征。