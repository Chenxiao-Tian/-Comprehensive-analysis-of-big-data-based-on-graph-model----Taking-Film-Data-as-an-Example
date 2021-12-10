# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 23:11:54 2020

@author: 田晨霄
"""
from brokenaxes import brokenaxes
import matplotlib.pyplot as plt
def draw(namelist=None,lenlist=None,dialist=None,starlist=None):
    x =[0 for i in range(len(lenlist))]                   #注27:一个柱状图中同时作出3个信息
    y =[0 for i in range(len(lenlist))]
    z =[0 for i in range(len(lenlist))]
    width =0.9
    x[0]=x[0]
    y[0]=y[0]+width/9
    z[0]=z[0]+2*width/9
    for i in range(len(x)-1):
        x[i+1] = x[i] + width/3
        y[i+1] = y[i] + width/3
        z[i+1] = z[i] + width/3
    plt.bar(x, dialist, width=width/9, label='Dias Change Function: math.log(dias+1.25,4)',fc = 'g') 
    plt.bar(y, lenlist, width=width/9, label="Lens Change Function: math.log(math.log(math.log(lens,10)+1,2)+1,2)+0.5",tick_label = namelist,fc = 'r')
    plt.bar(z, starlist, width=width/9, label='Stars Change Function: math.log(stars,3.5)',fc = 'y')
    plt.xticks(rotation=-45)
    plt.legend()
    plt.show()
def singledraw(namelist=None,form=None,l=None,color=None):#注28:分别作单个信息的柱状图
     x =list(0 for i in range(len(form)))
     width =0.001
     for i in range(len(x)-1):
         x[i+1] = x[i] + width+0.00005
     plt.bar(x,form, width=width, label=l,tick_label = namelist,fc = color)
     plt.xticks(rotation=-45)
     plt.legend()
     plt.show()
def originaldraw(form=None,labels=None,k=True):          #注29:用坐标截断的方法作信息的折线图
     x =list(0 for i in range(len(form)))
     width =1
     for i in range(len(x)-1):
         x[i+1] = x[i] + width
     if k==True: 
          bax = brokenaxes(ylims=((0,50),(84680,84690)),hspace=0.05, despine=False)
     else:
          bax = brokenaxes(despine=False)
     bax.plot(x,form,label=labels)
     bax.legend(loc=3)
     bax.set_xlabel('The Position Of Connected Component Based On Scale')
     bax.set_ylabel('Value')
def originaldrawall(form1=None,form2=None,form3=None,labels=None,k=None):
     x =list(0 for i in range(len(form1)))            #注30:用坐标截断的方法同时作信息的折线图
     width =1
     for i in range(len(x)-1):
         x[i+1] = x[i] + width
     if k==True:
          bax = brokenaxes(ylims=((0,50),(84680,84690)),hspace=0.05, despine=False)
     else:
          bax = brokenaxes(despine=False)
     bax.plot(x,form1,label=labels[0])
     bax.plot(x,form2,label=labels[1])
     bax.plot(x,form3,label=labels[2])
     bax.legend(loc=3)
     bax.set_xlabel('The Position Of Connected Component Based On Scale')
     bax.set_ylabel('Value')

if __name__=="__main__":
    import shelve
    with shelve.open ('constants') as h:
        Lens=h["L"]
        Dias=h['Dias']
        starlist=h["S"]
    originaldraw(Lens,"lens",True)                 #注31:在draw模块内直接作出截断折现图
    originaldraw(Dias,"dias",False)                #新增补注:此部分函数需一个个调用，避免干扰。
    originaldraw(starlist,"stars",False)
    originaldrawall(Lens,Dias,starlist,["lens","dias","stars"],True)