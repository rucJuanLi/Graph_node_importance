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
            g[edge[0]].append(edge[1])
            g[edge[1]].append(edge[0])
            if(i%100000==0):
                print 'read',i
    return g
def edge_a(g,edge_file,result_file):
   # edge_dict={}
    with open(edge_file,'r') as fr:
        with open(result_file,'w') as fw: 
            lines=fr.readlines()
            for i,line in enumerate(lines):
                edge=line.strip('\r\n').split(',') 
             	common_size=len(set(g[edge[0]]).intersection(set(g[edge[1]])))
          	#edge_dict[(edge[0],edge[1])]=common_size
                fw.write(edge[0]+'\t'+edge[1]+'\t'+str(common_size)+'\n')
                if(i%10000==0):print i
   # return edge_dict
g=construct_graph_with_combined_data_self('/home/lijuan/graph_data/nodes.csv','/home/lijuan/graph_data/edges.csv')
edge_dict=edge_a(g,'/home/lijuan/graph_data/edges.csv','/home/lijuan/graph_data/edges_embeding.txt')
#jsobj=json.dumps(edge_dict)
#fileobject=open('edge_dict.json','w')
#fileobject.write(jsobj)
#fileobject.close()
print 'finish ok'

