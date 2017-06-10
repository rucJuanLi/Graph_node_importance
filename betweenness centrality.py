#coding:utf-8
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
                if(i%100000==0):
                    print edge[0],edge[1]
        return g

def _single_source_shortest_path_basic(G, s):
        print 's_s_s_p_b',s
        S = []
        P = {}
        for v in G:
            P[v] = []
        sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
        D = {}
        sigma[s] = 1.0
        D[s] = 0
        Q = [s]
        while Q:   # use BFS to find shortest paths
            v = Q.pop(0)
            S.append(v)
            Dv = D[v]
            sigmav = sigma[v]
            for w in G[v]:
                if w not in D:
                    Q.append(w)
                    D[w] = Dv + 1
                if D[w] == Dv + 1:   # this is a shortest path, count paths
                    sigma[w] += sigmav
                    P[w].append(v)  # predecessors
        return S, P, sigma  #S是所有节点 P 每一个节点的前面路径的节点  sigma每个节点最短路径的个数
def _accumulate_basic(betweenness, S, P, sigma, s):
        print 'a_b',s
        delta = dict.fromkeys(S, 0)
        while S:
            w = S.pop()
            coeff = (1.0 + delta[w]) / sigma[w]
            for v in P[w]:
                delta[v] += sigma[v] * coeff
            if w != s:
                betweenness[w] += delta[w]
        return betweenness
def _rescale(betweenness, n, normalized, directed, k=None):
        if normalized is True:
            if n <= 2:
                scale = None  # no normalization b=0 for all nodes
            else:
                scale = 1.0 / ((n - 1) * (n - 2))
        else:  # rescale by 2 for undirected graphs
            if not directed:
                scale = 1.0 / 2.0
            else:
                scale = None
        if scale is not None:
            if k is not None:
                scale = scale * n / k
            for v in betweenness:
                betweenness[v] *= scale
        return betweenness
def betweenness_centrality(g, k=None, normalized=True, weight=None, endpoints=False,seed=None):
        betweenness = dict.fromkeys(g, 0.0)  # b[v]=0 for v in G
        if k is None:
            nodes = g
        for s in nodes:
            print 's',s
            if weight is None:  # use BFS
                S, P, sigma = _single_source_shortest_path_basic(g, s)
            # accumulation
            if not endpoints:
                betweenness = _accumulate_basic(betweenness, S, P, sigma, s)
        # rescaling
        betweenness = _rescale(betweenness, len(g),normalized=normalized,directed=True,k=k)
        return betweenness
g=construct_graph_with_combined_data_self('/home/lijuan/graph_data/nodes.csv','/home/lijuan/graph_data/edges.csv')
#print g.nodes()
print len(g)
betweenness=betweenness_centrality(g, k=None, normalized=False, weight=None,endpoints=False,seed=None)
print 'bn',betweenness
jsobj=json.dumps(betweenness)
fileobject=open('node_betweenness.json','w')
fileobject.write(jsobj)
fileobject.close()
print 'finish ok'
#print 'num_node',g.number_of_nodes()
