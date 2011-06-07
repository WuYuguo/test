#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   get_tc_simulated_track
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   simulate the whole typhoon track with the historical data
#
# INPUTS:
#   the simulated number of genesis point
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS: all the point along the simulated typhoon track

from numpy import *
from genesis_get_distance import *
from random import normalvariate
from math import asin, sin, cos, acos, radians, degrees, pow, sqrt, hypot, pi

#路径生成算法
def get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, previous_location, previous_time, R, FLAG, TRACK_POINT, Point_Num, genesis_end_dat, previous_delt_u, previous_delt_v):
	
    EARTH_RADIUS = 6378.137  #地球半径

    if(Point_Num >= 35 ):    #台风路径点数限制
        FLAG = 2
        return TRACK_POINT, Point_Num
    #台风路径研究区域边缘限制
    elif (previous_location[0] >= 180 or previous_location[1] >= 60 or previous_location[0] <= 100 or previous_location[1] <= 0):
        FLAG = 2
        return TRACK_POINT, Point_Num 
    
    dis_end = []
    dis_all = []

    #选取一定范围的终止点
    for i in range(len(genesis_end_dat)):
        dis = genesis_get_distance(genesis_end_dat[i][0], genesis_end_dat[i][1], previous_location[0], previous_location[1])
        if( abs(dis) <= R ):
            dis_end.append(dis)

    #选取一定范围的所有点       
    for i in range(len(genesis_all_dat)):
        dis = genesis_get_distance(genesis_all_dat[i][4], genesis_all_dat[i][5], previous_location[0], previous_location[1])
        if( abs(dis) <= R ):
            dis_all.append(dis)

    n_divide = 0.
    N_divide = 0.

    for i in range(len(dis_end)):
        n_divide = n_divide + 1.0 - dis_end[i] / R

    for i in range(len(dis_all)):
        N_divide = N_divide + 1.0 - dis_all[i] / R
	
	#if(N_divide == 0)
    #P2 = n_divide / N_divide
    
    related_point = empty((len(genesis_all_dat), 3), dtype = 'float')
    related_point_num = 0
    j = 0

    #print 'len(genesis_all_dat):', len(genesis_all_dat)
    #print 'len(all_tc_genesis_time):', len(all_tc_genesis_time)

    #相关点的移动速度和前进方向
    for i in range(len(genesis_all_dat)):
        if( abs(all_tc_genesis_time[i] - previous_time) <= 360 ):
            dis = genesis_get_distance(genesis_all_dat[i][4], genesis_all_dat[i][5], previous_location[0], previous_location[1])
            #print 'dis:', dis
            if( abs(dis) <= R ):
                related_point[j][0] = genesis_all_dat[i][6]      #speed
                related_point[j][1] = genesis_all_dat[i][7]	 #direction
                related_point[j][2] = dis
                j = j + 1
               #print 'j =', j
            
    related_point_num = j
    
    print 'related_point_num:', related_point_num
    
    if(related_point_num == 0):
    	FLAG = 2
    	return TRACK_POINT, Point_Num
	
    mean_u = 0.
    mean_v = 0.
    sum_u_divided = 0.
    sum_v_divided = 0.

    divide = 0.

    for i in range(related_point_num):
        sum_u_divided = sum_u_divided + related_point[i][1] * (1.0 - related_point[i][2] / R)
        sum_v_divided = sum_v_divided + related_point[i][0] * (1.0 - related_point[i][2] / R)
        divide = divide + 1.0 - related_point[i][2] / R
    
    #print 'sum_u_divided', sum_u_divided, 'sum_v_divided', sum_v_divided, 'divide', divide  
    mean_u = sum_u_divided / divide
    mean_v = sum_v_divided / divide
	
    #print 'mean_u:', mean_u, 'mean_v:', mean_v
    #print 'divide:', divide
    
    standard_deviation_u = 0.
    standard_deviation_v = 0.

    sum_u_STDDEV_divided = 0.
    sum_v_STDDEV_divided = 0.
   
    for i in range(related_point_num):
        sum_u_STDDEV_divided = sum_u_STDDEV_divided + pow(mean_u - related_point[i][1], 2) * (1.0 - related_point[i][2] / R)
        sum_v_STDDEV_divided = sum_v_STDDEV_divided + pow(mean_v - related_point[i][0], 2) * (1.0 - related_point[i][2] / R)
    
    #print 'sum_u_STDDEV_divided:', sum_u_STDDEV_divided, 'sum_v_STDDEV_divided:', sum_v_STDDEV_divided 
    standard_deviation_u = sqrt(sum_u_STDDEV_divided / divide)
    standard_deviation_v = sqrt(sum_v_STDDEV_divided / divide)
    
    #print 'sum_u_STDDEV_divided:', sum_u_STDDEV_divided, 'sum_v_STDDEV_divided:', sum_v_STDDEV_divided 
    
    #print 'standard_deviation_u:', standard_deviation_u, 'standard_deviation_v', standard_deviation_v

    if FLAG == 1:
        a = 0.
        b = 1.
    elif FLAG == 0:
        a = 0.8
        b = 0.6
        FLAG = 1

    kese_u = normalvariate(0, 1)
    #print 'kese_u:', kese_u

    kese_v = normalvariate(0, 1)
    #print 'kese_v:', kese_v

    #计算当前点的移动速度和前进方向
    u = mean_u + a * previous_delt_u + b * kese_u * standard_deviation_u
    v = mean_v + a * previous_delt_v + b * kese_v * standard_deviation_v

    print 'u:', u, 'v:', v
    
    delt_u = kese_u * standard_deviation_u
    delt_v = kese_v * standard_deviation_v

    distance = v * 6
    thelt = distance / EARTH_RADIUS
    line = 2 * EARTH_RADIUS * sin(thelt/2)
    line2 = line * cos(radians(u))
    line1 = line * sin(radians(u))
    thelt1 = 2 * asin(line1/(2 * EARTH_RADIUS))
    thelt2 = 2 * asin(line2/(2 * EARTH_RADIUS))

    print 'degrees(thelt1):', degrees(thelt1), 'degrees(thelt2):', degrees(thelt2)
    next_location = []
    next_location.append( previous_location[0] + degrees(thelt1) )
    next_location.append( previous_location[1] + degrees(thelt2) )
    next_time = previous_time + 360
    
    if(next_time >= 8760):
        next_time = next_time - 8760

    Point_Num = Point_Num + 1
    print 'Point_Num:', Point_Num 
    TRACK_POINT[Point_Num - 1][0] = next_location[0]
    TRACK_POINT[Point_Num - 1][1] = next_location[1]
    TRACK_POINT[Point_Num - 1][2] = next_time
    
    print 'NEW POINT:', TRACK_POINT[Point_Num - 1][0], TRACK_POINT[Point_Num - 1][1], TRACK_POINT[Point_Num - 1][2]

    #继续下一点的模拟
    [point_data, num_data]= get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, next_location, next_time, R, FLAG, TRACK_POINT, Point_Num, genesis_end_dat, delt_u, delt_v)
    #num_data = get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, next_location, next_time, R, FLAG, TRACK_POINT, Point_Num, genesis_end_dat, delt_u, delt_v)[1]
    
    return point_data, num_data
        

    
            
                                       
    
    
    
