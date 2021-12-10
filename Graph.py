# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 10:59:55 2020

@author: 田晨霄
"""
class Vertex:
    def __init__(self, key,value=None):
        self.id = key
        self.val=value
        self.connectedTo = {}
        self.connectedTovalues={}
    def addNeighbor(self, nbr, weight=0,value=None):
        self.connectedTo[nbr] = weight
        self.connectedTovalues[nbr] = value
    def __str__(self):
         return str(self.id) + 'connectedTo:' + str([x.id for x in self.connectedTo])
    def getConnections(self):
        return self.connectedTo.keys()
    def getId(self):
        return self.id
    def getWeight(self, nbr):
        return  self.connectedTo[nbr]
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.edgevalues={}
    def addVertex(self, key,value=None):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,value)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n ):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost = 0,value=None):
        if f not in self.vertList:
            self.addVertex(f)
        if t not in self.vertList:
            self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],cost)
        self.vertList[t].addNeighbor(self.vertList[f],cost)
        self.edgevalues[(min(f,t),max(f,t))]=value
   
    def getVertices(self):
        return self.vertList.keys()
  
    def __iter__(self):
        return iter(self.vertList.values())
    
    def dfs(self,start):               #注19:深度遍历dfs
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(set(change(list(self.vertList[vertex].connectedTo.keys()))) - visited)
        return visited
    
    def find__all__subs(self):         #注20:寻找所有连通分支，并返回为多重列表
        temp=set(list(self.vertList.keys()))
        allsubs=[]
        while len(temp)>0:
            cur=list(temp)[0]
            temp1=self.dfs(cur)
            allsubs.append(list(temp1))
            s=temp-temp1
            temp=s
        return allsubs
def change(form):                      #注21：辅助函数，将节点列表转化为对应的节点id列表
        for i in range(len(form)):
            form[i]=form[i].id
        return form
def haskey(x,d):                       #注22：辅助函数，查找字典里面是否有key
    if x in d.keys():
        return True
    else:
        return False
def find__diam(graph,form,EdgesvaluesDic):#注23:动态规划版本的弗洛伊德算法，复杂度O(n^3)
    if len(form)==1:
        return 0
    if len(form)==2:
        return 1
    form.sort()
    if len(form)==3:
        temp=[(form[0],form[1]),(form[1],form[2]),(form[0],form[2])]
        if [haskey(x,EdgesvaluesDic) for x in temp]==[True,True,True]:
            return 1
        else:
            return 2
    vertex,inf,dis=len(form),99999999,[]    
    dis=[[inf for j in range(vertex)] for i in range(vertex)]
    for i in range(vertex):
        dis[i][i]=0
        for j in range(i+1,vertex):
            temp=form[i],form[j]
            if haskey(temp,EdgesvaluesDic)==True:
                dis[i][j]=1
                dis[j][i]=1     
    for k in range(vertex):
        for i in range(vertex):
            for j in range(vertex):
                if dis[i][j] > dis[i][k] + dis[k][j]:
                    dis[i][j]= dis[i][k] + dis[k][j] 
    return max(max(dis))
if __name__=="__main__":
    a=Vertex("ds")
    print(a.id)
    g=Graph()
    #添加顶点
    for i in range(30):
        g.addVertex(i)
    #添加边
    g.addEdge(1,0,1)
    g.addEdge(0,2,1)
    g.addEdge(3,2,1)
    g.addEdge(3,2,1)
    g.addEdge(5,4,1)
    g.addEdge(7,5,1)
    g.addEdge(4,6,1)
    g.addEdge(8,12,1)
    g.addEdge(12,9,1)
    g.addEdge(9,10,1)
    g.addEdge(11,8,1)
    g.addEdge(19,20,1)
    g.addEdge(20,21,1)
    g.addEdge(23,24,1)
    g.addEdge(21,22,1)
    g.addEdge(22,24,1)
    f=Graph()
    for i in range(4):
        f.addVertex(i)
    f.addEdge(0,1,1)
    f.addEdge(0,2,1)
    f.addEdge(0,3,1)
    f.addEdge(1,2,1)  
    f.addEdge(1,3,1)
    f.addEdge(2,3,1)
    for v in g:
        for w in v.getConnections():
            print("(%s,%s)" %(v.getId(),w.getId()))
    print(g.find__all__subs())
    
    Actors=[i for i in range(19,25)]
    #s=cutgraph(Actors,g.edgevalues)
    print(find__diam(g,Actors,g.edgevalues))