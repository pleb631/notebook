[toc]

## 经典论文

- Googlenet


文章一上来首先表明了提高网络性能的方法就是增加网络的深度和宽度，

但是会有两个缺点：

1. 这样不可避免的带来参数量的增加，训练集过小时会导致过拟合。
2. 造成了计算资源的浪费（大量神经元的权重接近零），实践中计算资源有限

作者认为把全连接的结构转化为稀疏连接的结构，参考Hebbian principle，提出**Inception模块**，这个模块的最重要的作用就是让神经网络在学习的过程中自发的选择合适的路径或感受野，从而增加模型的**稀疏性**。

## REID
 ### [Bag of Tricks and A Strong Baseline for Deep Person Re-identification](https://openaccess.thecvf.com/content_CVPRW_2019/papers/TRMTMCT/Luo_Bag_of_Tricks_and_a_Strong_Baseline_for_Deep_Person_CVPRW_2019_paper.pdf)

1. Warmup, 
2. Random Erasing,
3. Label Smoothing,
4. 最后一个stride从2改为1，计算量不会增加很多,
5. 作者认为ID-loss是对特征划分超平面，类间距离会很明显，类内分布不明确；triptle-loss 是对特征聚合，没有全局约束；直接结合两者的损失会训不好，因为两种损失的所带来特征分布是有极大区别，所以需要卷积进行过渡，在输出的两个上分别作损失计算
6. 作者认为triplet-loss只考虑的特征之间的绝对距离，所以增加一个center-loss来改善类内特征的紧密性
7. 消融实验中，作者认为batch_size的选择很重要，要兼顾类间和类内，并且认为图片尺寸对REID没有影响

可用trick
Bag of Freebies(BoF):
1. Circle loss
2. Freeze backbone training
3. Cutout data augmentation & Auto Augmentation
4. Cosine annealing learning rate decay
5. Soft margin triplet loss

Bag of Specials(BoS):
1. Non-local block
2. GeM pooling

### [Deep Learning for Person Re-identification:A Survey and Outlook](https://arxiv.org/pdf/2001.04193v2.pdf)
1. Non-local Attention
2. Generalized-mean Pooling
3. Weighted Regularization Triplet loss
代码在[fast-reid](https://github.com/JDAI-CV/fast-reid/tree/39887a102eeec84661f0c0332000f8138aa9109d)

### [Learning Discriminative Features with Multiple Granularities for Person Re-Identification](https://arxiv.org/pdf/1804.01438v1.pdf)
基于高级语义特征，多分支，沿着垂直方向分成若干个stripe，在对每一个stripe产生的特征做损失，推理时对多分枝的特征进行堆叠

### [Learning Generalisable Omni-Scale Representations for Person Re-Identification](https://arxiv.org/pdf/1910.06827v5.pdf)
1. 采用DW卷积
2. 将单分支bottleneck改成改成多分支，并用gate把多尺寸特征进行结合
3. 插入Instance Normalisation，有助于去除图像风格带来的差异

### [Parsing-based View-aware Embedding Network for Vehicle Re-Identification](https://openaccess.thecvf.com/content_CVPR_2020/papers/Meng_Parsing-Based_View-Aware_Embedding_Network_for_Vehicle_Re-Identification_CVPR_2020_paper.pdf)
1. 使用图像分割网络把汽车解构成几个子部分，再用带掩膜的平均池化提取子部分的高级语义嵌入特征，并使用这些嵌入特征做triplet损失
## 理解

### 模型的稀疏性

这表现在两方面，第一是模型参数的稀疏性，模型权重只有一小部分不为0，其他都为0。另一方面是每一层提取特征的稀疏性，对于输出结果判断无用的特征（噪声特征）应给予抑制，使其置0，只保留对结果判断、拉大类间距离有用的特征。

**参数稀疏有什么好处**

1）特征选择： 大家对稀疏规则化趋之若鹜的一个关键原因在于它能实现特征的自动选择。一般来说，xi的大部分元素（也就是特征）都是和最终的输出yi没有关系或者不提供任何信息的，在最小化目标函数的时候考虑xi这些额外的特征，虽然可以获得更小的训练误差，但在预测新的样本时，这些没用的信息反而会被考虑，从而干扰了对正确yi的预测。稀疏规则化算子的引入就是为了完成特征自动选择的光荣使命，它会学习地去掉这些没有信息的特征，也就是把这些特征对应的权重置为0。

2）可解释性(Interpretability)： 另一个青睐于稀疏的理由是，模型更容易解释。例如患某种病的概率是y，然后我们收集到的数据x是1000维的，也就是我们需要寻找这1000种因素到底是怎么影响患上这种病的概率的。假设我们这个是个回归模型：y=w1*x1+w2*x2+…+w1000*x1000+b（当然了，为了让y限定在[0,1]的范围，一般还得加个Logistic函数）。通过学习，如果最后学习到的w*就只有很少的非零元素，例如只有5个非零的wi，那么我们就有理由相信，这些对应的特征在患病分析上面提供的信息是巨大的，决策性的。也就是说，患不患这种病只和这5个因素有关，那医生就好分析多了。但如果1000个wi都非0，医生面对这1000种因素.