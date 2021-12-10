# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:30:44 2020

@author: 田晨霄
"""

"""读取整理原始json文件"""
#########################
import time
import json
"""读取json文件"""
start=time.time()
file_path = 'Film.json'
with open(file_path,"rb") as f:
    js = json.load(f)  # 
"""actor转为列表"""
for i in range(len(js)):
    js[i]["actor"]=js[i]["actor"].split(",")
    # if "" in js[i]["actor"]:       #注1：由于数据质量原因，本应去掉空串考虑顿号等因素，但
    #     js[i]["actor"].remove("")  统一标准起见，本次项目暂时依照原始数据，不做额外预处理
"""type转为列表"""
for i in range(len(js)):
        js[i]["type"]=js[i]["type"].split(",")
"""依次统计所有actors"""
Actors=[]                            #注2：Actors用于记录所有出现过的演员
for i in range(len(js)):
    for j in range(len(js[i]["actor"])):
        Actors.append(js[i]["actor"][j])
Actors=list(set(Actors))             #注3:去掉重复演员名
"""记录演员于列表中位置的字典"""
find={}                              #注4:一个辅助反查演员于表位置的字典，减小
for i in range(len(Actors)):         #后续一些算法的复杂度
    find[Actors[i]]=i
"""依次统计所有演员演过的Movies以及记录此电影的星级、种类。"""
Movies=[[] for i in range(len(Actors))]#注5:用于整理Actors相应位置演员演过的电影，为多重列表
Stars=[[]for i in range(len(Actors))]  #注6:用于记录Movies相应位置的电影星级数，为多重列表
Types=[[] for i in range(len(Actors))] #注7:用于记录Movies相应位置的电影所属种类，为多重列表
findmovies={}                          #增补：为提高一些算法的效率，记录每部电影的index位置
for i in range(len(js)):
    x=js[i]
    temp1=x["actor"]
    temp2=x["title"]
    temp3=x["star"]
    temp4=x["type"]
    findmovies[temp2]=i
    for y in temp1:
            index=find[y]
            Movies[index].append(temp2)
            Stars[index].append(temp3)
            Types[index].append(temp4)   
"""依次统计所有参与了同一电影演出的演员对,及其所有合作电影列表"""
from collections import defaultdict #注8:用于字典初始化的value都自动设为空表                               
EdgesValuesDic=defaultdict(list) #注9:初始化字典，每个key是共同出演的演员元组，value为电影列表
for x in js:
    temp=x["actor"]
    if len(temp)>1:              #注10:至少有大于1个演员，才成对出现 
        for a in range(len(temp)):
            for b in range(a+1,len(temp)):
                if temp[a]!=temp[b]:
                    co=(min(temp[a],temp[b]),max(temp[a],temp[b]))
                    EdgesValuesDic[co].append(x["title"])
end=time.time()
print(end-start)
start=time.time()
"""构建图"""
import Graph as G
graph=G.Graph()
for i in range(len(Actors)):
    graph.addVertex(Actors[i],Movies[i]) #注11：遍历Actors表，以其所演电影为节点附加属性
for keys in EdgesValuesDic:              #注12: 遍历EdgesValuesDic字典，以其value为边属性
    graph.addEdge(keys[0],keys[1],1,EdgesValuesDic[keys])
end=time.time() 
print(end-start)   
"""求连通分支数目、每个分支所含演员数目、前20和后20规模的连通分支所含电影类别的前三名""" 
from collections import Counter
start=time.time()
def counter(arr):       #注13:统计一个列表中出现的最多的三种元素及其出线次数
    return Counter(arr).most_common(3)
def movietypes(form):   #注14:form输入的为每个连通分支的演员列表，返回电影种类统计列表（去重的)
    temp=[]
    for s in form:
        k=Movies[find[s]]
        for t in k:
            temp.append(t)
    temp=list(set(temp))
    types=[]
    for t in temp:
        for k in js[findmovies[t]]["type"]:
            types.append(k)
    return types                            
s=graph.find__all__subs()#注15:调用Graph.py模块中的find__all__subs()函数遍历寻找所有连通分支
print("连通分支数目：",len(s))             
w=sorted(s,key=(lambda x:len(x)))#注16:按连通分支大小，从小到大排序
print("每个连通分支所含的演员数: ")
print([len(x) for x in w])
mostthreetypesfirst={}           #注17:用于记录前20最大的分支的电影种类
mostthreetypeslast={}            #注18:用于记录后20最小的分支的电影种类
print("前20和后20规模的连通分支所含电影类别的前三名(未考虑个别电影重名的情况): ")
tobesort=[]
for i in range(len(w)):
    if len(w[i])>1:
        break
    tobesort.append(w[i])
tobesort.sort(key=lambda ele:ele[0])   #新增调整：后20并列中,字符串升序取前20。
for i in range(20):
    mostthreetypeslast["倒数第"+str(i+1)+"大小的分支"]=counter(movietypes(tobesort[i]))
for i in range(20):
     mostthreetypesfirst["正数第"+str(i+1)+"大小的分支"]=counter(movietypes(w[-1-i]))
print(mostthreetypesfirst)
print(mostthreetypeslast)
end=time.time()
print(end-start)
"""求直径"""
start=time.time()
import shelve
Dias=[]
s=graph.edgevalues
for i in range(len(w)-1):  ##注24:最大的不计算
    Dias.append(G.find__diam(graph,w[i],s))
Dias.append(-1)
end=time.time()
print(end-start)
with shelve.open ('constants') as h: #注25: 储存算好的直径表于constants中
      h["Dias"]=Dias
with shelve.open ('constants') as h: #注26: 从constants中提取直径表
      Dia=h["Dias"]
print(Dias)
"""做条形图""" 
start=time.time()
import matplotlib
import draw as d
import math
lenlist2=[math.log(math.log(math.log(len(x),10)+1,2)+1,2)+0.5 for x in w]
lenlist1=[math.log(math.log(math.log(math.log(len(x),10)+1,2)+1,2)+1,2)+0.2 for x in w]
namelist=[]
for i in range(len(w)):
    if i%400==0:
        namelist.append("position: "+str(i))
    else:
        namelist.append("")
starlist=[]
for i in range(len(w)):                   #注32：统计每个分支的平均星级
    temp1=w[i]
    S=0
    L=0
    for j in range(len(temp1)):
        temp2=Stars[find[temp1[j]]]
        L=L+len(temp2)
        S=S+sum(temp2)
    starlist.append(round(S/L,2)) 
print("平均星级表",starlist)
with shelve.open ('constants') as h:      #注33:储存数据
    h["L"]=[len(x) for x in w]
    h["S"]=starlist                       #注34:作图
d.singledraw(namelist,lenlist1,"Lens Change Function:math.log(math.log(math.log(math.log(lens,10)+1,2)+1,2)+1,2)+0.2","r")
d.singledraw(namelist, Dias,"Dias Change Function:  Keep Original Data","g")
d.singledraw(namelist,[math.log(x+1.25,4) for x in Dias],"Dias Change Function: math.log(x+1.25,4)","g")
d.singledraw(namelist,starlist,"Average Stars Change Function : Keep Original Data","y")
d.draw(namelist,lenlist2,[math.log(x+1.25,4) for x in Dias],[math.log(x,3.5) for x in starlist])
end=time.time()
print(end-start)
"""特定演员个人统计"""
start=time.time()
index=find["周星驰"]
#print("平均星级为: ",round(sum(Stars[index])/len(Stars[index]),2))#周星驰平均星级
company=[]
for y in js:
    if "周星驰" in y["actor"]:
            company=company+y["actor"]
company=list(set(company))
print("共同出演者人数 含周星驰本人 不去空串: ",len(company))
recordnum={}                             #注35:3个字典分别储存周星驰共同出演者各自所演电影数
                                          #增补注释：以下用于记录平均星级数、电影种类
recordstar={}
recordtypes={}
for x in company:
    recordnum[x]=len(Movies[find[x]])
    recordstar[x]=round(sum(Stars[find[x]])/len(Stars[find[x]]),2)
    temp1=Types[find[x]]
    temp2=[]
    for i in range(len(temp1)):
        for j in range(len(temp1[i])):
            temp2.append(temp1[i][j])
    recordtypes[x]=counter(temp2)
print("各自所演的电影数: ",recordnum)
print("各自所演电影的平均星级数： ",recordstar)
print("各自所演电影种类的前3名：",recordtypes)
end=time.time()
print(end-start)
"""图算法发现""" #注36:整合的py文件中自选发现部分由于时间成本较高，且未加dat文件，所以不执行，
                #如需验证可在网盘提交源代码文件中运行。
print("""此部分内容，由于整合的py文件中自选发现部分时间成本较高，且未加dat文件，所以暂不执行，
如需验证可在网盘提交源代码文件中运行""")
start=time.time()
Edgelist=[]
for keys in EdgesValuesDic:
    Edgelist.append([keys[0],keys[1],len(EdgesValuesDic[keys])])
import pagerank as p
# print("begin")
# h=p.pagerank(Edgelist)
# end=time.time()
# print(end-start)
# with shelve.open('constants') as t:     #注36:存储排名结果
#       t["rank"]=h
with shelve.open('constants') as t:
      h=t["rank"]
print(h)
# start=time.time()
g=p.setup(Edgelist)
for x in h[:5]:
    p.show__rankfirst__subgraph(x[0],g)#注37:作出前5名演员的相对位置子图
end=time.time()
print(end-start)