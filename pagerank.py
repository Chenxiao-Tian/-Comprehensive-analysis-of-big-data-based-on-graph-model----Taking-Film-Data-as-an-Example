# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 23:02:52 2020

@author: 田晨霄
"""
import networkx as nx
import matplotlib.pyplot as plt
import warnings
def setup(edgelist):
    G = nx.Graph()
    for x in edgelist:
        G.add_edge(x[0],x[1],weight=x[2])
    return G
def pagerank(edgelist):
    G = nx.Graph()
    for x in edgelist:
        G.add_edge(x[0],x[1],weight=x[2])
    fb=G
    pos = nx.spring_layout(fb)                      
    warnings.filterwarnings('ignore')
    
    plt.style.use('fivethirtyeight')
    plt.rcParams['figure.figsize'] = (20, 15)
    plt.axis('off')
    nx.draw_networkx(fb, pos, with_labels = False, node_size = 35)
    plt.show()
    pagerank = nx.pagerank(fb)
    import operator
    sorted_pagerank = sorted(pagerank.items(), key=operator.itemgetter(1),reverse=True)
    print(sorted_pagerank)
    return [sorted_pagerank,G]
def show__rankfirst__subgraph(s,G):
    fb=G
    first_degree_connected_nodes = list(fb.neighbors(s))
    second_degree_connected_nodes = []
    for x in first_degree_connected_nodes:
         second_degree_connected_nodes+=list(fb.neighbors(x))
    second_degree_connected_nodes.remove(s)
    second_degree_connected_nodes = list(set(second_degree_connected_nodes))
    subgraph_Mannheim= nx.subgraph(fb,first_degree_connected_nodes+second_degree_connected_nodes,)
    pos = nx.spring_layout(subgraph_Mannheim)
    warnings.filterwarnings('ignore')
    node_color = ['yellow' if v == s else 'red' for v in subgraph_Mannheim]
    node_size =  [1000 if v == s else 35 for v in subgraph_Mannheim]
    plt.style.use('fivethirtyeight')
    plt.rcParams['figure.figsize'] = (20, 15)
    plt.axis('off')
    nx.draw_networkx(subgraph_Mannheim, pos, with_labels = False, node_color=node_color,node_size=node_size )
    plt.show()
if __name__=="__main__":
    edgelist = [['Mannheim', 'Frankfurt', 85], ['Mannheim', 'Karlsruhe', 80], ['Erfurt', 'Wurzburg', 186], ['Munchen', 'Numberg', 167], ['Munchen', 'Augsburg', 84], ['Munchen', 'Kassel', 502], ['Numberg', 'Stuttgart', 183], ['Numberg', 'Wurzburg', 103], ['Numberg', 'Munchen', 167], ['Stuttgart', 'Numberg', 183], ['Augsburg', 'Munchen', 84], ['Augsburg', 'Karlsruhe', 250], ['Kassel', 'Munchen', 502], ['Kassel', 'Frankfurt', 173], ['Frankfurt', 'Mannheim', 85], ['Frankfurt', 'Wurzburg', 217], ['Frankfurt', 'Kassel', 173], ['Wurzburg', 'Numberg', 103], ['Wurzburg', 'Erfurt', 186], ['Wurzburg', 'Frankfurt', 217], ['Karlsruhe', 'Mannheim', 80], ['Karlsruhe', 'Augsburg', 250],["Mumbai", "Delhi",400],["Delhi", "Kolkata",500],["Kolkata", "Bangalore",600],["TX", "NY",1200],["ALB", "NY",800]]
    G = nx.Graph()
    for x in edgelist:
        G.add_edge(x[0], x[1], weight=1)
    fb=G
    pagerank(edgelist)
    show__rankfirst__subgraph("Mannheim",fb)