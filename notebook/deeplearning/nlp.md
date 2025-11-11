## 1. 分词

### 1.1 英文分词

按照分词粒度的大小，可分为词级（Word-Level）分词、字符级（Character-Level）分词
和子词级（Subword‑Level）分词。

#### 1.1.1 Word-Level

词级分词是指将文本按词语进行切分，是最传统、最直观的分词方式。在英文中，空格
和标点往往是天然的分隔符。

词级分词虽便于理解和实现，但在实际应用中容易出现 OOV（Out-Of-Vocabulary，未
登录词）问题。所谓 OOV，是指在模型使用阶段，输入文本中出现了不在预先构建词表中
的词语，常见的包括网络热词、专有名词、复合词及拼写变体等。由于模型无法识别这些词，
通常会将其统一替换为特殊标记（如 <UNK>），从而导致语义信息的丢失，影响模型的理
解与预测能力。

"transformer often outperform traditional sequence model ."

==>

["transformer", "often", "outperform", "traditional", "sequence", "model","."]

#### 1.1.2 Character-Level

字符级分词（Character-level Tokenization）是以单个字符为最小单位进行分词的方法，
文本中的每一个字母、数字、标点甚至空格，都会被视作一个独立的 token。

在这种分词方式下，词表仅由所有可能出现的字符组成，因此词表规模非常小，覆盖率
极高，几乎不存在 OOV（Out-of-Vocabulary）问题。无论输入中出现什么样的新词或拼写变
体，只要字符在词表中，都能被表示出来。
然而，由于单个字符本身语义信息极弱，模型必须依赖更长的上下文来推断词义和结构，
这显著增加了建模难度和训练成本。此外，输入序列也会变得更长，影响模型效率。

"hello world !"

==>

["h","e","l","l","o"," ","w","o","r","l","d"," ","!"]

#### 1.1.3 Sub-word

子词级分词是一种介于词级分词与字符级分词之间的分词方法，它将词语切分为更小的
单元——子词（subword），例如词根、前缀、后缀或常见词片段。与词级分词相比，子词分
词可以显著缓解 OOV 问题；与字符级分词相比，它能更好地保留一定的语义结构。
子词分词的基本思想是：即使一个完整的词没有出现在词表中，只要它可以被拆分为词
表中存在的子词单元，就可以被模型识别和表示，从而避免整体被替换为<UNK>。

"transformers often outperform traditional sequence model ."

==>

["transform", "ers"," often", " out","perform", " traditional", " sequence", " model","."]

相关代码库：**SentencePiece**

- BPE（字节对编码）[docs]([Byte-Pair Encoding tokenization - Hugging Face LLM Course](https://hf-mirror.com/learn/llm-course/chapter6/5?fw=pt))
   基本步骤：
   1. 准备足够大的训练语料，并确定期望的Subword词表大小；
   2. 将单词拆分为成最小单元。比如英文中26个字母加上各种符号，这些作为初始词表；
   3. 在语料上统计单词内相邻单元对的频数，选取频数最高的单元对合并成新的Subword单元；
   4. 重复第3步直到达到第1步设定的Subword词表大小或下一个最高频数为1.

- WordPiece（词汇片段）
    与BPE不同的是第3个步骤，WordPiece选择能够提升语言模型概率最大的相邻子词加入词表。假设句子$S=(t_{0},t_{1},t_{2},...,t_{n-1})$ 等n个单词构成，则句子的语言模型似然值等价于所有子词概率的乘积：$$logP(S)=\sum logP(t_{i})$$
    假设把相邻位置的x和y两个子词进行合并，合并后产生的子词记为z，此时句子似然值的变化可表示为：$$logP(t_{z}-(logP(t_{x})+logP(t_{y})))=log(\frac{P(t_{x})}{P(t_{x})P(t_{y})})$$很容易发现，似然值的变化就是子词之间的互信息值

### 1.2 中文分词

#### 1.2.1 字符级分词

字符级分词是中文处理中最简单的一种方式，即将文本按照单个汉字进行切分，文本中
的每一个汉字都被视为一个独立的 token

“你好世界!”

==》

["你", “好”, “世”, “界”，“!”]

由于汉字本身通常具有独立语义，因此字符级分词在中文中具备天然的可行性。相比英
文中的字符分词，中文的字符分词更加“语义友好”

#### 1.2.2 词级分词

词级分词是将中文文本按照完整词语进行切分的传统方法，切分结果更贴近人类阅读习
惯。

"transformer的表现通常优于传统的序列模型。"

==》

["transformer","的",“表现”,'"通常","优于",“传统”,“的”,"序列模型",“。”]

由于中文没有空格等天然词边界，词级分词通常依赖词典、规则或模型来识别词语边界。

#### 1.2.3 子词级分词

虽然中文没有英文中的子词结构（如前缀、后缀、词根等），但子词分词算法（如 BPE）
仍可直接应用于中文。它们以汉字为基本单位，通过学习语料中高频的字组合（如“自然”、
“语言”、“处理”），自动构建子词词表。这种方式无需人工词典，具有较强的适应能力。
在当前主流的中文大模型（如通义千问、DeepSeek）中，子词分词已成为广泛采用的文
本切分策略。

### 1.3 分词工具

目前市面上可用于中文分词的工具种类繁多，按照实现方式大致可以分为如下两类：
➢
一类是基于词典或模型的传统方法，主要以“词”为单位进行切分；
➢
另一类是基于子词建模算法（如 BPE）的方式，从数据中自动学习高频字组合，构
建子词词表。
前者的代表工具包括 jieba、HanLP 等，这些工具广泛应用于传统 NLP 任务中。
后者的代表工具包括 Hugging Face Tokenizer、SentencePiece、tiktoken 等，常用于大
规模预训练语言模型中。

#### 1.3.1  jieba

```python
import jieba
text = "小明毕业于北京大学计算机系"
words_generator = jieba.cut(text) # 返回一个生成器
for word in words_generator:
print(word)
words_list = jieba.lcut(text) # 返回一个列表
print(words_list)
```

jieba 支持用户自定义词典，以便包含 jieba 词库里没有的词，用于增强特定领域词汇的
识别能力。
自定义词典的格式为：一个词占一行，每一行分三部分：词语、词频（可省略，词频决
定某个词在分词时的优先级。词频越高被优先切分出来的概率越大）、词性标签（可省略，
不影响分词结果），用空格隔开，顺序不可颠倒。例如

```txt
云计算
云原生 5
大模型 10 n
```

可使用 jieba.load_userdict(file_name)加载词典文件，也可以使用 jieba.add_word(word,
freq=None, tag=None)与 jieba.del_word(word)动态修改词典。

```python
import jieba
jieba.load_userdict('dict.txt')
words_list = jieba.lcut("随着云计算技术的普及，越来越多企业开始采用云原生架
构来部署服务，并借助大模型能力提升智能化水平，实现业务流程的自动化与智能决策。
")
print(words_list)
```

## 2. 词表示

在分词完成之后，文本被转换为一系列的 token（词、子词或字符）。然而，这些符号本
身对计算机而言是不可计算的。因此，为了让模型能够理解和处理文本，必须将这些 token
转换为计算机可以识别和操作的数值形式，这一步就是所谓的词表示（word representation）。
词表示的发展经历了从稀疏的 one-hot 编码，到稠密的语义化词向量，再到近年来的上
下文相关的词表示。不同的词表示方法在表达能力、语义建模、上下文适应性等方面存在显
著差异。

最早期的词向量表示方式是 One-hot 编码：它将词汇表中的每个词映射为一个稀疏向
量，向量的长度等于整个词表的大小。该词在对应的位置为 1，其他位置为 0。

### 2.1 Word2Vec

传统的 one-hot 表示虽然结构简单，但它无法反映词语之间的语义关系，也无法衡量词
与词之间的相似度,且计算效率低下。为了解决这个问题，研究者提出了 Word2Vec 模型，它通过对大规模语
料的学习，为每个词生成一个具有语义意义的稠密向量表示。这些向量能够在连续空间中表
达词与词之间的关系，使得“意思相近”的词在空间中距离更近。

#### 2.1.1 概述

Word2Vec 的设计理念源自“[分布语义](https://en.wikipedia.org/wiki/Distributional_semantics)”——即一个词的含义由它周围的词决定。

基于这一假设，Word2Vec 构建了一个简洁的神经网络模型，通过学习词与上下文之间 的关系，自动为每个词生成一个能够反映语义特征的向量表示

Word2Vec 提供了两种典型的模型结构，用于实现对词向量的学习：

- CBOW（Continuous Bag-of-Words）模型

  输入是一个词的上下文（即前后若干个词），模型的目标是预测中间的目标词。

  ```python
  # “我每天乘坐地铁上班”
  # 训练样本：
  {
      "input":["乘坐","上班"],
      "target":"地铁"
  }
  ```

- Skip-gram 模型
  输入是一个中心词，模型的目标是预测其上下文中的所有词（即前后若干个词）。
  
  ```python
  # “我每天乘坐地铁上班”
  # 训练样本：
  { 
      "input":"地铁",
      "target":["乘坐","上班"],
      
  }
  ```

#### 2.2.2 获取词向量

词向量的获取通常有两种方式：一种是直接使用他人公开发布的词向量，另一种是在特 定语料上自行训练。  在实际工作中，无论是加载已有模型还是从零训练，都可借助Gensim来完成，它提供 了便捷的接口来加载 Word2Vec 格式的词向量，也支持基于自有语料训练属于自己的词向量模型。

1）使用公开词向量  

公开的中文词向量，可从<https://github.com/Embedding/Chinese-Word-Vectors> 下载，其提 供了基于多个数据集训练得到的词向量。  词向量文件的格式为：第一行记录基本信息，包括两个整数，分别表示总词数和词向量 维度。从第二行起，每一行表示一个词及其对应的词向量，格式为：词 + 向量的各个维度 值。所有内容通过空格分隔，该格式已成为自然语言处理领域中广泛接受的约定俗成的通用 格式。具体格式如下

```txt
<词汇总数> <向量维度> 
word1 val11 val12 ... val1N 
word2 val21 val22 ... val2N 
... 
```

```python
# 加载
from gensim.models import KeyedVectors 
model_path = 'sgns.weibo.word.bz2' 
model = KeyedVectors.load_word2vec_format(model_path) 

print(model.vector_size) # 查看词向量维度 
print(model['地铁'])  # 查看某个词的向量
similarity = model.similarity('地铁', '公交')  # 查看两个向量的相似度
similar_words = model.most_similar(positive=["上班"], topn=5)  # 找出与某个词最相似的topn个词 
result = model.most_similar(positive=["爸爸", "女性"], negative=["男性"], 
topn=3) 
```

2）自行训练词向量

（1）准备语料  Word2Vec的训练语料需要是已分词的文本序列，格式为：  

```python
sentences = [['我', '每天','乘坐', '地铁', '上班'], ['我','每天', '乘坐',  '公交', '上班']]
```

（2）训练模型

```python
from gensim.models import Word2Vec 
 
model = Word2Vec( 
    sentences,            # 已分词的句子序列 
    vector_size=100,      # 词向量维度 
    window=5,             # 上下文窗口大小 
    min_count=2,          # 最小词频（低于将被忽略） 
    sg=1,                 # 1:Skip-Gram，0:CBOW 
    workers=4             # 并行训练线程数 
) 
model.wv.save_word2vec_format('my_vectors.kv') 
```

(3)加载词向量

```python
from gensim.models import KeyedVectors 
 
my_model = KeyedVectors.load_word2vec_format('my_vectors.kv') 
```

### 2.2 应用词向量

训练好的词向量，通常用于初始化下游NLP任务的嵌入层。  

在现代深度学习的 NLP 模型中，大多数任务的输入第一层都是嵌入层。本质上，嵌入 层就是一个查找表（lookup table）：输入是词在词汇表中的索引；输出是该词对应的向量表 示。  

嵌入层的参数矩阵可以有两种典型的初始化方式：  

➢ 随机初始化  模型训练开始时，嵌入向量是随机生成的，模型会通过反向传播逐步学习每个词的表示。  

➢ 使用预训练词向量初始化  加载训练好的词向量（如 Word2Vec）到嵌入层中作为初始参数，这样可以为模型注入 丰富的语言知识，尤其在低资源任务中优势明显。并且，加载预训练词向量后，可选择是否 让嵌入层继续参与训练。

 下面以PyTorch为例，演示如何使用预训练词向量初始化Embedding层

```python
from torch import nn
embedding_layer = nn.Embedding.from_pretrained( 
    embedding_matrix, # 词向量矩阵，形状为(num_embeddigns,embedding_dim) 
    freeze=False  # 是否冻结词向量 

```

完整案例

```python
import torch 
from torch import nn
from gensim.models import KeyedVectors 
 
# 1. 加载预训练的 Word2Vec 模型 
word_vectors = KeyedVectors.load_word2vec_format("my_vectors.kv") 
 
# 2. 构建词表和词向量矩阵 
word2index = word_vectors.key_to_index  # 词到索引的映射 
embedding_dim = word_vectors.vector_size  # 词语向量维度 
num_embeddings = len(word2index)  # 词表大小 
 
embedding_matrix = torch.zeros(num_embeddings, embedding_dim)  # 构造词
向量矩阵,形状为(词表大小,词向量维度大小) 
for word, idx in word2index.items(): 
    embedding_matrix[idx] = torch.tensor(word_vectors[word]) 
 
# 3. 构建 PyTorch 的嵌入层 
embedding_layer = nn.Embedding.from_pretrained( 
    embedding_matrix, # 词向量矩阵，形状为(num_embeddigns,embedding_dim) 
    freeze=False  # 是否冻结词向量 
) 
 
# 4. 示例：将词索引转换为向量 
input_words = ["我", "喜欢", "乘坐", "地铁"]  # 分词后的句子 
input_indices = [word2index[word] for word in input_words]  # token转为
索引 
input_tensor = torch.tensor([input_indices])  # 构造嵌入层输入张量 
 
# 5. 查询嵌入（即词向量查找） 
output = embedding_layer(input_tensor)  # 通过嵌入层查找预训练词向量 
 
print(output.shape)  # 例如 torch.Size([1, 4, 100]) 
```

### 2.3 上下文相关词表示

虽然像Word2Vec这样的模型已经能够为词语提供具有语义的向量表示，但是它只为每 个词分配一个固定的向量表示，不论它在句中出现的语境如何。这种表示被称为静态词向量 （static embeddings）。

然而，语言的表达极其灵活，一个词在不同上下文中可能有完全不同的含义。

上下文相关词表示（Contextual Word Representations），是指词语的向量表示会根据它所 在的句子上下文动态变化，从而更好地捕捉其语义。一个具有代表性的模型是——ELMo。  该模型全称为 Embeddings from Language Models，发表于2018年2月。其基于LSTM  语言模型，使用上下文动态生成每个词的表示，每个词的向量由其前文和后文共同决定，是 第一个被广泛应用于下游任务的上下文词向量模型。

## 论文

### [Bert](https://arxiv.org/abs/1810.04805)

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

### [CTRL](https://arxiv.org/pdf/1909.05858)

在每一个序列的具体内容前加了入类型描述，使得在计算Attention过程中，类型与序列中的所有元素建立联系

### [albert](https://arxiv.org/abs/1909.11942)

ALBERT 是一种轻量级的自监督学习语言表示模型，它在降低参数量的同时保持了性能。

1. 嵌入矩阵分解
    ALBERT 使用了矩阵分解的思想来解决 BERT 中嵌入向量维度和隐藏层维度相等的问题。在嵌入向量后面添加了一个全连接层，将嵌入向量从 E 维度映射到 H 维度。这样，E 可以设置为较小的维度（例如 128），而全连接层将其映射到与隐藏层相同的维度（例如 768）。参数量从 O(V×H) 降低到 O(V×E + E×H)，在 BERT-base 情况下，嵌入矩阵参数量减少了约 17%。
2. 参数共享
    ALBERT 默认选择了共享全部参数，即一份数据在 Transformer 的一个编码层上来回传递多次。
3. 句子顺序判断（Sentence-Order Prediction，SOP）：
    BERT 使用的 NSP 预训练任务对于下游微调任务效果不佳。ALBERT 引入了 SOP 任务，让模型预测两个相邻句子是否被调换前后顺序。SOP 专注于句子间的连贯性，不依赖主题信息，有效提高了模型性能。

### [DistilBERT](<https://arxiv.org/pdf/1910.01108>

使用知识蒸馏，使用温度T的softmax概率，而不是原始的softmax概率。损失有三部分构成：

1. 蒸馏损失soft loss
2. 原本bert的自带的hard-loss
3. Cosine Embedding Loss，利于让student学习和teacher一样的hidden state vector

### [T5](https://arxiv.org/pdf/1910.10683)

T5是编码器-解码器模型，并将所有NLP问题转换为文本到文本格式

### [BART](https://arxiv.org/abs/1910.13461)

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

### [longformer](https://arxiv.org/abs/2004.05150)

为了解决长文本的建模问题。该架构可以有效地处理超过 2048 个token

1. 滑动窗口
    对滑动窗口内的token进行局部注意力计算，而对于比如[cls]标签,则在局部注意力的基础上，对标签也进行全局注意力计算。在QA任务上，就在整个问句上计算全局注意力。视任务不同，需要计算全局注意力的位置也不同

### [DeBERTa](https://arxiv.org/abs/2006.03654)

为了解决 BERT 中的位置编码问题，DeBERTa 提出了一种新的位置编码方法，该方法能够更好地捕捉序列中词之间的相对位置信息。

1. 注意力解耦
    DeBERTa 将注意力机制分为两个部分，内容的注意力加上内容与位置的注意力之和，因为位置是相对位置，相对位置间的注意力无意义，故舍弃
2. enhanced mask decoder
    由于某些词的语义相似性，而相对位置难以区分，因此在attention层后面会加上绝对位置区分语义相似性

### [BigBird](https://arxiv.org/abs/2007.14062)

为了减少注意力计算的复杂度，提出一种稀疏注意力，用特殊token+滑动窗口token+随机token来计算注意力，从而减少计算量。实验上发现对特殊token的注意力效果提升很明显

### [ConvBERT](https://arxiv.org/pdf/2008.02496)

轻量级bert

- 使用一维卷积和注意力机制进行混合
- 在全连接上使用分组
- 维持了头的嵌入维度，但是减少了头的数量，相当于瓶颈结构

### [CANINE](https://arxiv.org/abs/2103.06874)

使用unicode编码token，使用stride=4的一维卷积对token进行降维，输入长度为2048，深层长度为512

### [ByT5](https://arxiv.org/abs/2105.13626)

byT5是在字节序列而不是句子片段子词标记序列上预训练的T5模型。避免不同tokenizer分词，词表带来的对语言模型的影响，考虑直接使用字节list(uft-8) 进行语言模型的实现。eg.`list("hello".encode("utf-8"))`

### [ELECTRA](https://arxiv.org/pdf/2003.10555)

提出了新的预训练任务和框架，把生成式的Masked language model(MLM)预训练任务改成了判别式的Replaced token detection(RTD)任务，判断当前token是否被语言模型替换过。用生成模型生成句子，然后用判别模型判断句子是否被替换过。实验发现，生成器的大小在判别器的1/4到1/2之间效果是最好的。

### [ERNIE-M](https://arxiv.org/abs/2012.15674)

提出了CAMLM(Cross-attention Masked Language Modeling), 对于平行语料语言A和语言B，语言A的[MASK]只能通过语言B来还原、语言B的[MASK]只能通过语言A来还原。这样是为了避免information leakage，即语言直接通过自己的上下文来还原[MASK]。这样"逼着"模型来学双语的semantic alignment。例如：输入的句子对是<明天会[MASK][MASK]吗，Will it be sunny tomorrow>，模型需要只使用英文句子<Will it be sunny tomorrow>来推断中文句子中掩盖住的词<天晴>，使模型初步建模了语言间的对齐关系。

### [Falcon](https://arxiv.org/abs/2306.01116)

原始多头 (head) 注意力方案每个头都分别有一个查询 (query) 、键 (key) 以及值 (value)，而多查询注意力方案改为在所有头上共享同一个键和值

### [FNet](https://arxiv.org/abs/2105.03824)

使用离散傅里叶变换替代自注意力层
