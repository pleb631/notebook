## tokenization(分词)

### Sub-word

Subword主要是处于word和char level两个粒度级别之间的一种方法，设计的目的主要是用于解决word级别面临的以下几个问题：

- 超大的vocabulary size, 比如中文的常用词可以达到20W个
- 通常面临比较严重的OOV问题
- vocabulary 中存在很多相似的词。

以及char level存在的以下问题：

- 文本序列会变得很长，想象以下如果是一篇英文文章的分类，char level级别的输入长度可以达到上万
- 无法对语义进行比较好的表征

相关代码库：SentencePiece

- BPE（字节对编码）
   基本步骤：
   1. 准备足够大的训练语料，并确定期望的Subword词表大小；
   2. 将单词拆分为成最小单元。比如英文中26个字母加上各种符号，这些作为初始词表；
   3. 在语料上统计单词内相邻单元对的频数，选取频数最高的单元对合并成新的Subword单元；
   4. 重复第3步直到达到第1步设定的Subword词表大小或下一个最高频数为1.

- WordPiece（词汇片段）
    与BPE不同的是第3个步骤，WordPiece选择能够提升语言模型概率最大的相邻子词加入词表。假设句子$S=(t_{0},t_{1},t_{2},...,t_{n-1})$ 等n个单词构成，则句子的语言模型似然值等价于所有子词概率的乘积：$$logP(S)=\sum logP(t_{i})$$
    假设把相邻位置的x和y两个子词进行合并，合并后产生的子词记为z，此时句子似然值的变化可表示为：$$logP(t_{z}-(logP(t_{x})+logP(t_{y})))=log(\frac{P(t_{x})}{P(t_{x})P(t_{y})})$$很容易发现，似然值的变化就是子词之间的互信息值

## 论文

### Bert

#### 预训练的任务

    1. masked language model
        随机选取15%的token进行mask，然后预测被mask的token，其中被选中的token有80%的概率被替换为[MASK],10%的概率被替换为随机词，10%的概率保持不变。(比如替换成同义词、反义词、人物称呼指代等)
    2. next sentence prediction
        选择A和B两个句子，A和B之间用[SEP]隔开，A是随机选取的句子，B是A之后的一个句子。如果B是A的后续句子，则预测结果为1，否则预测结果为0。这种预训练有助于 QA 和 NLI任务

#### 下游任务

- GLUE
    加入[cls]token,进行预测
- SQuAD v1.1
    任务是预测段落中的答案文本范围,让文本和问题用[sep]连接,并预测每个token的是S(start)或E(end)的概率,并找到最大概率的位置组合，作为答案
- SWAG
    任务是问答多选一，将问题与选项用[sep]连接，并预测每个token是得分，取最大评分的选项

### albert

ALBERT 是一种轻量级的自监督学习语言表示模型，它在降低参数量的同时保持了性能。

1. 嵌入矩阵分解
    ALBERT 使用了矩阵分解的思想来解决 BERT 中嵌入向量维度和隐藏层维度相等的问题。在嵌入向量后面添加了一个全连接层，将嵌入向量从 E 维度映射到 H 维度。这样，E 可以设置为较小的维度（例如 128），而全连接层将其映射到与隐藏层相同的维度（例如 768）。参数量从 O(V×H) 降低到 O(V×E + E×H)，在 BERT-base 情况下，嵌入矩阵参数量减少了约 17%。
2. 参数共享
    ALBERT 默认选择了共享全部参数，即一份数据在 Transformer 的一个编码层上来回传递多次。
3. 句子顺序判断（Sentence-Order Prediction，SOP）：
    BERT 使用的 NSP 预训练任务对于下游微调任务效果不佳。ALBERT 引入了 SOP 任务，让模型预测两个相邻句子是否被调换前后顺序。SOP 专注于句子间的连贯性，不依赖主题信息，有效提高了模型性能。

### DeBERTa

为了解决 BERT 中的位置编码问题，DeBERTa 提出了一种新的位置编码方法，该方法能够更好地捕捉序列中词之间的相对位置信息。

1. 注意力解耦
    DeBERTa 将注意力机制分为两个部分，内容的注意力加上内容与位置的注意力之和，因为位置是相对位置，相对位置间的注意力无意义，故舍弃
2. enhanced mask decoder
    由于某些词的语义相似性，而相对位置难以区分，因此在attention层后面会加上绝对位置区分语义相似性

### longformer

为了解决长文本的建模问题。该架构可以有效地处理超过 2048 个token

1. 滑动窗口
    对滑动窗口内的token进行局部注意力计算，而对于比如[cls]标签,则在局部注意力的基础上，对标签也进行全局注意力计算。在QA任务上，就在整个问句上计算全局注意力。视任务不同，需要计算全局注意力的位置也不同

### BART

提出的是一种符合生成任务的预训练方法，BART的全称是Bidirectional and Auto-Regressive Transformers，即兼具上下文语境信息和自回归特性的Transformer

GPT，BERT与BART的区别：

- GPT是一种Auto-Regressive(自回归)的语言模型。它也可以看作是Transformer的Decoder部分，通常用于文本生成，输出的结果是一个序列。
- BERT是一种Auto-Encoding(自编码)的语言模型。它也可以看作是Transformer的Encoder部分，在输入端随机使用一种特殊的[MASK]token来替换序列中的token，然后预测这些token，输出的长度和输入的长度一致，所以bert不能用于文本生成
- BART吸收了BERT的双向encoder和GPT的从左到右decoder各自的特点，建立在标准的seq2seq Transformer 模型的基础之上，这使得它比BERT更适合文本生成的场景；相比GPT，也多了双向上下文语境信息。在生成任务上获得进步的同时，它也可以在一些文本理解类任务上取得SOTA。

- 是一个seq2seq结构
- 预训练，采用更加多样的噪声函数对文本进行加噪，学习序列到序列模型以重建原始文本
    1. Token Masking: 就是BERT的方法----随机将token替换成[MASK]；
    2. Token Deletion: 随机字符将从输入中删除。与字符屏蔽相反，该模型必须确定哪些位置缺少输；
    3. Text Infilling: 随机将一段连续的token（称作span）替换成一个[MASK]，span的长度服从泊松分布。注意span长度为0就相当于插入一个[MASK]。
    4. Sentence Permutation: 根据句号将文档分为多个句子，然后将这些句子随机排列；
    5. Document Rotation: 从document序列中随机选择一个token，然后使得该token作为document的开头


### BigBird

为了减少注意力计算的复杂度，提出一种稀疏注意力，用特殊token+滑动窗口token+随机token来计算注意力，从而减少计算量。实验上发现对特殊token的注意力效果提升很明显