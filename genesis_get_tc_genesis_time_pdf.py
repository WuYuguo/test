#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_tc_genesis_time_pdf
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   Derive probability density distribution of Typhoon Genesis Time (TGT) by smoothing
#   empirical probability density distribution (histogram) derived from historical data,
#   using Epanechnikov kernel function.
#
# INPUTS:
#   A integer vector containing the genesis time of historical typhoon events.
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#   BIN: The time interval for TGT probablility density distribution.
#   The default value of BIN is 120 (hour).
#     System will calculate the number of interval by following equation
#   NBINS = 365*24/BIN
#
# OUTPUTS:
#   a ineger vector,contains N_years elements,each element represents the number of typhoons to be simulated in one year
#
# OPTIONAL OUTPUTS:

from numpy import *
from math import *

def KERNEL(u):
    k = 0
    if(u <= -5**0.5 or u >= 5**0.5):
        return k
    k = 3 * 5**0.5 *(1 - u**2 /5) /20
    return k

#台风起源时间概率密度算法
def genesis_get_tc_genesis_time_pdf(HIST_TGT):

    BIN = 120
    #时间的分段
    N_BINS = 365 * 24 / BIN     

    TGT_UNIQ = []      
    TGT_FREQ = []      
    HIST_TGT.sort()  #起始时间的排序
    N_TYPHOON = len(HIST_TGT)  
    print 'N_TYPHOON:', N_TYPHOON
    
    i = 0

    while i < len(HIST_TGT):
        #起始时间的去重复及统计出现年数
        TGT_UNIQ.extend([HIST_TGT[i]])
        TGT_FREQ.extend([HIST_TGT.count(HIST_TGT[i])])
        i = i + HIST_TGT.count(HIST_TGT[i])
	
    L = len(TGT_UNIQ)
    #for i in range(L):
    	#print 'TGT_UNIQ', i, TGT_UNIQ[i]
    	#print 'TGT_FREQ', i, TGT_FREQ[i]

    TMP = array(HIST_TGT)
    TGT_MEAN = TMP.mean()   #均值
    TGT_STDD = TMP.std()    #标准差
    print 'TGT_MEAN:', TGT_MEAN
    print 'TGT_STDD:', TGT_STDD


    N_TGT = len(TGT_UNIQ)
    TGT_PDF_HIST = []

    for i in range(N_TGT):
    	#print 'TGT_FREQ[', i, ']', '/N_TYPHOON:', long(TGT_FREQ[i])/N_TYPHOON
        TGT_PDF_HIST.append( float(TGT_FREQ[i])/N_TYPHOON )
        #print 'TGT_PDF_HIST', i, TGT_PDF_HIST[i]  
	
    #print 1./N_TYPHOON    
    H_WIDTH = (TGT_STDD/2) * (pow((1./N_TYPHOON),(1./3)))
    print 'H_WIDTH:', H_WIDTH
    
    TGT_PDF = []
    for j in range(2):
        TGT_PDF.append([])
        for i in range(N_BINS):
            TGT_PDF[j].append(0.)

    for i in range(N_BINS):
        TGT_PDF[0][i] = i * BIN

    TGT_TMP = []

    for i in range(N_BINS -1):
        TGT_TMP.append((TGT_PDF[0][i+1] + TGT_PDF[0][i]) / 2)
    TGT_TMP.append((8760 + TGT_PDF[0][N_BINS - 1]) /2)

    for j in range(N_BINS):
        for i in range(N_TGT):
            K = KERNEL(long(TGT_TMP[j] - TGT_UNIQ[i]) / H_WIDTH)
            #print TGT_TMP[j] - TGT_UNIQ[i]
            #print H_WIDTH
            #print 'K:', K
            TGT_PDF[1][j] = TGT_PDF[1][j] + TGT_PDF_HIST[i] * K

    #归一化
    sum_TGT_PDF = sum(TGT_PDF[1])
    for j in range(N_BINS):
        TGT_PDF[1][j] = TGT_PDF[1][j] / sum_TGT_PDF
        
  	#for j in range(N_BINS):
  		#print 'time:', TGT_PDF[0][j], 'pdf:', TGT_PDF[1][j]

    #
    print 'TGT_PDF:'
    print 'TIME'
    for j in range(N_BINS):
        print TGT_PDF[0][j]
    print 'PDF'
    for j in range(N_BINS):
        print TGT_PDF[1][j]
    #

    return TGT_PDF





                
