import cpnet
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import genfromtxt
import planarity
import networkx as nx
import networkx.algorithms.community as nx_comm

def buildgraph():
    df = pd.read_csv('/2017.csv',encoding='utf-8')
    nodes = [a for a in df.columns]

    df = genfromtxt('/2017.csv', delimiter=',')
    adjacency = df[1:,1:]

    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    for i in range(len(G)):
        for j in range(len(G)):
            G.add_edge(nodes[j], nodes[i], weight=adjacency[i][j])

    weights = nx.get_edge_attributes(G, "weight")

    pos = nx.circular_layout(G)
    # pos = nx.spring_layout(G)
    plt.figure(3,figsize=(20,20))
    nx.draw_networkx(G, pos, with_labels=True, node_size = 2000, font_size=10, width=[float(d['weight']*0.6) for (u,v,d) in G.edges(data=True)])
    return plt

# PMFG减边
def get_network_PMFG(G):
    sorted_edges = []
    for source, dest, data in G.edges(data=True):
        sorted_edges.append({'source': source, 'dest': dest, 'weight': abs(data.get('weight', 1))})
    sorted_edges.sort(key=lambda x: x['weight'], reverse=True)

    PMFG = nx.DiGraph()
    for edge in sorted_edges:
        PMFG.add_edge(edge['source'], edge['dest'], weight=edge['weight'])
        if not planarity.is_planar(PMFG):
            PMFG.remove_edge(edge['source'], edge['dest'])
        if PMFG.number_of_edges() == 6 * (G.number_of_nodes() - 2):
            break
    return PMFG

#draw figure
def drawplot(G):
    pos = nx.circular_layout(G)
    plt.figure(3,figsize=(20,20))
    nx.draw_networkx(G, pos, with_labels=True, node_size = 2000, font_size=10, width=[float(d['weight']*0.6) for (u,v,d) in G.edges(data=True)])
    return plt

def cal_in_and_out_degree(G):
    for n,d in G.in_degree():
        print(d)

    for n,d in G.out_degree():
        print(d)

#计算同配系数
def cal_correlation_coefficient(G):
    correlation_coefficient_set = []

    # 无向
    correlation_coefficient_set.append(nx.degree_pearson_correlation_coefficient(G,weight='weight'))

    #有向 出-出
    correlation_coefficient_set.append(nx.degree_pearson_correlation_coefficient(G,x='out', y='out',weight='weight'))

    #有向 出-入
    correlation_coefficient_set.append(nx.degree_pearson_correlation_coefficient(G,x='out', y='in',weight='weight'))

    #有向 入-入
    correlation_coefficient_set.append(nx.degree_pearson_correlation_coefficient(G,x='in', y='in',weight='weight'))

    #有向 入-出
    correlation_coefficient_set.append(nx.degree_pearson_correlation_coefficient(G,x='in', y='out',weight='weight'))

    return correlation_coefficient_set

def cal_other(G):
    other_set = []

    #计算平均最短路径长度
    other_set.append(nx.average_shortest_path_length(G,weight='weight'))

    #计算平均聚类系数
    other_set.append(nx.average_clustering(G,weight='weight'))

    return other_set

# 鲁汶社区检测
def Louvain(G):
    # 有向图转无向图
    G = G.to_undirected()

    com=list(nx_comm.louvain_communities(G,weight='weight',resolution=0.8))
    print('社区数量',len(com))

    pos = nx.spring_layout(G) # 节点的布局为spring型

    NodeId = list(G.nodes())
    node_size = [G.degree(i)**1.2*90 for i in NodeId] # 节点大小

    plt.figure(figsize = (8,6)) # 图片大小
    nx.draw(G,pos,with_labels=True, node_size =node_size, node_color='w', node_shape = '.')

    color_list = ['pink','orange','r','g','b','y','m','gray','black','c','brown']

    for i in range(len(com)):
        nx.draw_networkx_nodes(G, pos, nodelist=com[i], node_color=color_list[i])

    return plt

def cal_centrality(G):
    #计算群体度中心性
    group_degree_centrality=[]
    for i in range(0,len(com)):
        group_degree_centrality.append(nx.group_degree_centrality(G,com[i]))

    #计算群体介数中心性
    group_betweenness_centrality=[]
    for i in range(0,len(com)):
        group_betweenness_centrality.append(nx.group_betweenness_centrality(G, com[i], weight='weight'))

    #计算群体亲近中心性
    group_closeness_centrality=[]
    for i in range(0,len(com)):
        group_closeness_centrality.append(nx.group_closeness_centrality(G, com[i], weight='weight'))

    return group_degree_centrality, group_betweenness_centrality, group_closeness_centrality


