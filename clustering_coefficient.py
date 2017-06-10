#coding:utf-8
import networkx as nx
import json
def construct_graph_with_combined_data_self(node_file,edge_file):
        g = {}
        with open(node_file,'r') as fr:
            lines=fr.readlines()
            for i,line in enumerate(lines):
                node = line.strip('\r\n')
                g[node]=[]
        with open(edge_file,'r') as fr:
            lines=fr.readlines()
            for i,line in enumerate(lines):
                edge=line.strip('\r\n').split(',')
               # if(edge[1] not in g[edge[0]]):
                g[edge[0]].append(edge[1])
                g[edge[1]].append(edge[0])
                if(i%100000==0):
                    print 'read',i
        return g
def _triangles_and_degree_iter(G):
   # l=[]
    #nodes_nbrs= ( (n,G[n]) for n in G.keys() )
    nodes=G.keys()
    with open('cluster_c_tria.txt','w') as fw:
        for i,v in enumerate(nodes):
            v_nbrs=G[v]
            vs=set(v_nbrs)-set([v])
       	    ntriangles=0
            for w in vs:
                ws=set(G[w])-set([w])
                ntriangles+=len(vs.intersection(ws))
            if(ntriangles==0):
            	fw.write(v+'\t'+str(len(vs))+'\t'+str(ntriangles))
            else:
                d=len(vs)
                fw.write(v+'\t'+str(d)+'\t'+str(ntriangles/float(d*(d-1))))
            if(i%100000==0):print i
      
def c_c(g):
    td_iter=_triangles_and_degree_iter(g)
    clusterc={}
    for v,d,t in td_iter:
        if t==0:
            clusterc[v]=0.0
        else:
            clusterc[v]=t/float(d*(d-1))
    return clusterc
g=construct_graph_with_combined_data_self('/home/lijuan/graph_data/nodes.csv','/home/lijuan/graph_data/edges.csv')
_triangles_and_degree_iter(g)
print 'finish ok'

