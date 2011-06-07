#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_simulated_tc_num
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#    Derive the number of typhoons each year
#
# INPUTS:
#   tc_frequency_pdf: The parameters and P-value of Chi-square test of
#                     Poisson distribution and Negtive Binomial distribution
#                     TAO_PDF must be an 3*2 array
#   N_years         : a integer scalar ,represent the number of years to be simulated
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   a ineger vector,contains N_years elements,each element represents the number of typhoons to be simulated in one year
#
# OPTIONAL OUTPUTS:


from numpy import *
from imsl.stat.randomPoisson import randomPoisson
from imsl.stat.randomNegBinomial import randomNegBinomial

#台风年发生频次模拟算法
def genesis_get_simulated_tc_num(tc_frequency_pdf, N_years):
    genesis_tc_num = []
    if max(tc_frequency_pdf[0][2], tc_frequency_pdf[1][2]) < 0.05:
        print 'Neither of the distributiongs is satisfactory.'
        return []
    else:
        #在泊松分布和负二项分布中选取适当的拟合方法进行模拟
        if tc_frequency_pdf[0][2] > tc_frequency_pdf[1][2]:
            genesis_tc_num = randomPoisson(N_years, tc_frequency_pdf[0][0])
        else:
            genesis_tc_num = randomNegBinomial(N_years, tc_frequency_pdf[1][1], 1 - tc_frequency_pdf[1][0])
	
    for i in range(N_years):
    	print "genesis_tc_num", i, genesis_tc_num[i]

    #
    print 'year'
    for i in range(N_years):
        print i
    print 'genesis_tc_num'
    for i in range(N_years):
        print genesis_tc_num[i]       

    #
    return genesis_tc_num
