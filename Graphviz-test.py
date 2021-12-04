# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 19:10:49 2021

@author: 12094
"""
from graphviz import Digraph

g = Digraph('测试图片')
g.node(name='a',color='red')
g.node(name='b',color='blue')
g.edge('a','b',color='green')
g.view()
