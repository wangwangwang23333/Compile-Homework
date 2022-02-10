## 简介
本项目为软件工程专业编译原理课程大作业，完成内容为自下而上语法分析章节中的算法。
项目演示视频：https://www.bilibili.com/video/BV1Rq4y1y7z4

我们使用Python作为各个算法的编程语言。同时，我们采用了PyQt5作为可视化界面，使用了包括QTableWidget在内的控件实现输入输出的展示。为了实现语法树和DFA图的生成，我们使用了Graphviz包作为有向图（DFA图和语法树）绘制的工具。

<img src="https://s4.ax1x.com/2022/01/12/7uKvkT.png">
<img src="https://s4.ax1x.com/2022/01/12/7uMVAK.png">
<img src="https://s4.ax1x.com/2022/01/12/7uMu1H.png">

## 环境需求
要运行本项目，请先保证电脑中已有Graphviz环境（配置在环境变量中）
通过python运行main.py文件即可
需要python库已添加在requirement.txt中

## 实验内容
- 实验3.1为FIRSTVAL/LASTVAL集合构造算法，要求接收文法产生式，输出文法符号的FIRSTVT和LASTVT集合元素。
- 实验3.2为优先关系表构造算法，要求接收算符文法产生式，输出算符优先关系表。
- 实验3.3为算符优先分析算法，接收算符文法和算符优先分析表，输出算符优先语法分析程序。
- 实验3.4为识别文法活前缀的DFA构造算法，接收上下文无关文法，输出LR(0)和LR(1)项目的DFA图和状态转移矩阵。
- 实验3.5为LR(0)分析表构造算法，接收文法产生式和基于LR(0)项目构造的DFA图或状态转移矩阵，输出LR(0)分析表。
- 实验3.6为SLR分析表构造算法，接收文法产生式和基于LR(0)项目构造的DFA图或状态转移矩阵，输出SLR分析表。
- 实验3.7为LR(1)分析表构造算法，接收文法产生式和于LR(1)项目构造的DFA图或状态转移矩阵，输出LR(1)分析表。
- 实验3.8为LALR分析表构造算法，接收文法产生式和基于LALAR的DFA图或状态转移矩阵，输出LALR分析表。
- 实验3.9为基于LR分析表的语法分析总控程序，接收文法产生式和LR分析表，输出语法分析程序。
- 综合实验为基于LR(1)分析法的语法分析程序生成器，是实验3.4~3.8的综合性实验，接收上下文无关文法，输出语法分析程序。

## 小组分工
- 汪明杰完成了算法3.2、3.4、3.9和综合性实验与界面设计
- 卓正一完成了算法3.7和3.8
- 王立友完成了算法3.1和3.5
- 梁乔完成了算法3.3和3.6

## 实验亮点
- 完成了模块要求的全部算法和综合性实验；
- 通过PyQt5界面，更好的实现了不同算法的输入和输出，让结果呈现更加清晰；
- 通过Graphviz绘制DFA图和语法树，更好的展现了算法的输出；
- 代码逻辑清晰，不同功能的算法定义在了不同的类中（如GrammarManager负责词法分析，LR0类和LR1类等）；
- 有错误捕捉机制，当出现输入错误时程序能够体现在界面上。
