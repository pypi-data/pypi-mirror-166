# Localc (Logic Calculator)

## 介绍
一个简单的逻辑计算器。能进行逻辑表达式（即**命题**```Proposition```）的求解运算。

## 安装方法

本项目已上传至[PYPI](https://pypi.org/project/localc/)，直接利用```pip```（```Python```的**包管理器**即可安装）。

只需在控制台输入如下命令：

```
pip install localc
```

即可安装最新版本的*localc*。

## 文档

### 快速开始

*localc*是一个小巧的逻辑计算器，使用起来非常简单。我们分别介绍如下概念：

#### 命名空间与项目结构

想要使用*localc*，就必须导入```localc```包。

```localc```包中包含了如下组件：

- ```node```，包含了用于存储抽象语法树的数据结构
- ```operators```，用于操作符英语与数学表示的相互转换
- ```parser```，利用*token*流，构建抽象语法树
- ```proposition```，**主用户接口**
- ```scanner```，任务是生成*token*流

我并不建议你使用除了```proposition```以外的其他包，除非你知道自己在做什么。对于大多数用户而言，你只需要在*Python*代码文件的头部加上：

```python
from localc import Proposition
```

#### 命题

使用*localc*计算器的核心是命题：