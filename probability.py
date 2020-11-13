#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:32:17 2020

@author: georgiaroussos
"""

import numpy as np


data1=np.load('0783SYNC.npy')


for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            for tb in range(30):
                if data1[i,y,x,tb] != 0:
                    data1[i,y,x,tb]=data1[i,y,x,tb]-9.62

relevant = []
p=[]
for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            
            tbsum = np.sum(data1[i,y,x])
            
            if tbsum > 300:# change 300 to i 0-1000
                relevant.append([i,y,x])
   
#percentage of events used for tracklets 
print((len(relevant)/(3*12*144*len(data1)))*100) 
#uncertainty
print(np.std(relevant)/np.sqrt(3*12*144*len(data1)))