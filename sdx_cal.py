import os
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


class Estimate:
    def __init__(self):
        pass
    
    def est(self,income):
        stage_1=[6000,300,200,0.05]
        stage_2=[8000,1200,500,0.1]
        stage_3=[10000,1700,500,0.1]
        stage_4=[12000,1700,800,0.1]
        stage_5=[15000,1700,1000,0.1]
        stage_6=[99999,1700,1200,0.1]

        #条件
        if 0<=income<stage_1[0]:
            rent,run_fund,a_rate,b_rate=stage_1[1],stage_1[2],stage_1[3],1-stage_1[3]
        elif stage_1[0]<=income<stage_2[0]:
            rent,run_fund,a_rate,b_rate=stage_2[1],stage_2[2],stage_2[3],1-stage_2[3]
        elif stage_2[0]<=income<stage_3[0]:
            rent,run_fund,a_rate,b_rate=stage_3[1],stage_3[2],stage_3[3],1-stage_3[3]
        elif stage_3[0]<=income<stage_4[0]:
            rent,run_fund,a_rate,b_rate=stage_4[1],stage_4[2],stage_4[3],1-stage_4[3]
        elif stage_4[0]<=income<stage_5[0]:
            rent,run_fund,a_rate,b_rate=stage_5[1],stage_5[2],stage_5[3],1-stage_5[3]
        elif stage_5[0]<=income<stage_6[0]:
            rent,run_fund,a_rate,b_rate=stage_6[1],stage_6[2],stage_6[3],1-stage_6[3]

        return rent,run_fund,a_rate,b_rate

    def draw(self):
        plt.figure(1,figsize=(8,5))
        # for i in ran
        # y_rent=selrent
        # y_run_fund=run_fund
        # y_a_income=income*a_rate
        # y_b_income=income*b_rate

        x=[]
        y_rent=[]
        y_run_fund=[]
        y_a_income=[]
        y_b_income=[]
        y_a_true_income=[]

        # x=np.linspace(500,20000,100)

        for i in np.linspace(500,20000,30):
            factor=self.est(i)
            x.append(i)
            y_rent.append(factor[0])
            y_run_fund.append(factor[1])
            y_a_income.append(factor[2]*i)
            y_b_income.append(factor[3]*i)
            y_a_true_income.append(factor[2]*i+factor[0])
            # y_rent,y_run_fund,y_a_income,y_b_income=factor[0],factor[1],factor[2]*i,factor[3]*i
            


            # print(i,y_rent,y_run_fund,y_a_income,y_b_income)
            # plt.plot(i,y_a_income,color='red',marker='o',markersize=1,linestyle='-')
            # plt.plot(i,y_b_income,color='green',marker='o',markersize=1)
            # plt.plot(i,y_rent,color='blue',marker='o',markersize=1)
            # plt.plot(i,y_run_fund,color='purple',marker='o',markersize=1)

            # note that plot returns a list of lines.  The "l_a_income, = plot" usage
            # extracts the first element of the list into l_a_income using tuple
            # unpacking.  So l_a_income is a Line2D instance, not a sequence of lines
        l_a_income,=plt.plot(x,y_a_income,color='red',marker='o',markersize=1)
        l_b_income,=plt.plot(x,y_b_income,color='green',marker='o',markersize=1)
        l_rent,=plt.plot(x,y_rent,color='blue',marker='o',markersize=1,linestyle='dashed')
        l_run_fund,=plt.plot(x,y_run_fund,color='purple',marker='o',markersize=1,linestyle='dashed')
        l_a_true_income,=plt.plot(x,y_a_true_income,color='orange',marker='o',markersize=1)
        
        plt.xlabel('月营业收入（元）',fontsize=14)
        plt.ylabel('收入/成本（元）',fontsize=14)
        plt.xticks([0,6000,8000,10000,12000,15000])

        plt.legend(handles=[l_a_income,l_b_income,l_rent,l_run_fund,l_a_true_income],
                    labels=['甲方收入','乙方收入','成本-房屋租金','成本-运营成本','甲方实际收入'],loc='best')
        # plt.plot(12,13,color='red',marker='o')
        plt.show()

    def cal(self,amt):
        tt=''
        for num in amt:
            rent,run_fund,a_rate,b_rate=self.est(num)
            income_a=(num-rent-run_fund)*a_rate
            income_b=(num-rent-run_fund)*b_rate
            tt=tt+'营收：{},\na收入:{},\nb收入：{}\n\n'.format(num,income_a,income_b)
        return tt

if __name__=='__main__':
    vv=Estimate()
    # vv.draw()
    res=vv.cal([4000,5000,6000,7000])
    print(res)

    # tt(200,200,'优设标题',200)