import os
import sys
import numpy as np
import matplotlib.pyplot as plt


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

        for i in np.linspace(500,20000,100):
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
        plt.plot(x,y_a_income,color='red',marker='o',markersize=1)
        plt.plot(x,y_b_income,color='green',marker='o',markersize=1)
        plt.plot(x,y_rent,color='blue',marker='o',markersize=1)
        plt.plot(x,y_run_fund,color='purple',marker='o',markersize=1)
        plt.plot(x,y_a_true_income,color='orange',marker='o',markersize=1)
        # plt.plot(12,13,color='red',marker='o')
        plt.show()


if __name__=='__main__':
    vv=Estimate()
    vv.draw()


    # tt(200,200,'优设标题',200)