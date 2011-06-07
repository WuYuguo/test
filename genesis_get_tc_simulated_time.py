#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_tc_simulated_time
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   Get the simulated genesis time of typhoon
#
# INPUTS:
#   tc_genesis_time_pdf : a 2*n vetor,the first row represent the inteval time cauculated by hour
#                         the second row represent the probability of each inteval
#   tc_num              : a integer scalar ,represent the number of simulated typhoon genesis time
#                         is  derived
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   a integer vector ,each element repesents the simulated genesis time of each typhoon,its unit is hour
#
# OPTIONAL OUTPUTS:


#import sys
#from ctypes import *
#from imsl import *
#from numpy import *

import sys
from numpy import *
from imsl.stat.continuousTableSetup import continuousTableSetup
from imsl.stat.randomOption import randomOption
from imsl.stat.randomGeneralContinuous import randomGeneralContinuous
from imsl.stat.randomSeedSet import randomSeedSet


def cdf(x):
	return

#台风起源时间模拟算法	
def genesis_get_tc_simulated_time(tc_genesis_time_pdf, n_tc_num_sim):
    pdf_arr_info = array(tc_genesis_time_pdf)
    tc_genesis_time_cdf = []
    
    #for i in range(73):
    	#print 'tc_genesis_time_pdf_time', i, tc_genesis_time_pdf[0][i]
    	#print 'tc_genesis_time_pdf_pdf', i, tc_genesis_time_pdf[1][i]
    
    for i in range(73):
    	tc_genesis_time_cdf.append(0.)
    	for j in range(i + 1):
    		tc_genesis_time_cdf[i] = tc_genesis_time_cdf[i] + tc_genesis_time_pdf[1][j]
    	print 'tc_genesis_time_cdf', i, 'is', tc_genesis_time_cdf[i]

    #台风起源时间的累计概率密度
    print 'CDF'
    for i in range(73):
        print tc_genesis_time_cdf[i]
    print 'over'
    #

    iopt = 1
    ndata = pdf_arr_info.shape[1] + 1

    print 'ndata:', ndata

    table = []
    for j in range(5):
        table.append([])
        for i in range(ndata):
            table[j].append(0.)

    for i in range(ndata-1):
        table[0][i] = tc_genesis_time_pdf[0][i]
    table[0][ndata-1] = 8760

    table[1][0] = float(0.)
    for i in range(1, ndata):
        table[1][i] = tc_genesis_time_cdf[i - 1]

    table[1][ndata-1] = float(1.)
    
    new_table = empty ((ndata,5), dtype='float')
    
    for i in range(ndata):
    	new_table[i][0] = float(table[0][i])
    	new_table[i][1] = float(table[1][i])
    	#print new_table[i][0], new_table[i][1]
    		
	
    iopt = 1
    
    continuousTableSetup (cdf, iopt, [new_table])
    
    
    #randomOption (1)
    randomSeedSet(0)
    
    #tc_simulated_time = empty((tc_num,2), dtype = 'int')
    print "number:", n_tc_num_sim
    #根据累计概率密度生成连续时间
    tc_simulated_time = randomGeneralContinuous(int(n_tc_num_sim), new_table)
	
    for i in range(n_tc_num_sim):
    	tc_simulated_time[i] = round(tc_simulated_time[i])
    	print "tc_simulated_time", i, tc_simulated_time[i]
    return tc_simulated_time


                                   
    
