#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_sim
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   simulate the original point of typhoon and the whole typhoon track, in addition, simulate the typhoon track with real-time data in some method of DDDAS
#
# INPUTS:
#   genesis_tc_data: a 7 x n vector , repectively,each column represents typhoon N0,typhoon genesis time about year、month、day and hour,typhoon genesis location of longitude and latitude
#   x0, y0         : the longitude, latitude of kernel area origin (left, down)
#   N_years        : a integer scalar ,represent the number of years to be simulated
#   n_cols, n_rows : the cols and rows of the kernel area
#   grid_size      : a single-, or double-precision floating-point scalar define the grid size of the the kernel area
#   R              : a single-, or double-precision floating-point scalar that defines the radius/distance (kilometer) for kernel density calculation
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS: all the simulated genesis points of typhoon are stored in the PostgreSQL table derive_simulation. all the simulated typhoon tracks with historical data are
#           stored in the PostgreSQL table track. all the simulated typhoon tracks with real-time data are stored in the PostgreSQL DDDAS_track

from genesis_get_kernel_pdf import *
from genesis_get_his_annual_TC_num import *
from genesis_get_annual_tc_frequency_pdf import *
from genesis_get_his_tc_genesis_time import *
from genesis_get_simulated_tc_num import *
from genesis_get_tc_genesis_time_pdf import *
from genesis_get_tc_simulated_time import *
from genesis_get_tc_simulated_location import *
from get_tc_simulated_track import *
from get_tc_simulated_track_DDDAS import *

import sys
from ctypes import *
from imsl import *
from numpy import *

def genesis_sim(db, genesis_his_dat, n_years_sim, x0, y0, n_cols, n_rows, grid_size, R, genesis_all_dat, genesis_end_dat):

    genesis_his_ll = []
    for j in range(len(genesis_his_dat)):
        genesis_his_ll.append([])
        for i in range(2):
            genesis_his_ll[j].append(0.)

    for j in range(len(genesis_his_dat)):
        genesis_his_ll[j][0] = genesis_his_dat[j][4]
        genesis_his_ll[j][1] = genesis_his_dat[j][5]

    #台风起始点核密度计算
    print "genesis_get_kernel_pdf STARTS"    
    kernel_pdf = genesis_get_kernel_pdf(db, genesis_his_ll, x0, y0, n_cols, n_rows, grid_size, R)

    #台风年发生频次统计
    print "genesis_get_his_annual_TC_num STARTS"
    annual_tracknum = genesis_get_his_annual_TC_num(db, genesis_his_dat)

    #台风年发生频次概率密度算法
    print "genesis_get_annual_tc_frequency_pdf STARTS"
    tc_frequency_pdf = genesis_get_annual_tc_frequency_pdf(db, annual_tracknum)

    #台风点时间按照小时计算
    print "genesis_get_his_tc_genesis_time STARTS"
    his_tc_genesis_time = genesis_get_his_tc_genesis_time(genesis_his_dat)
    all_tc_genesis_time = genesis_get_his_tc_genesis_time(genesis_all_dat)

    #台风起源时间概率密度算法
    print "genesis_get_tc_genesis_time_pdf STARTS"
    tc_genesis_time_pdf = genesis_get_tc_genesis_time_pdf(his_tc_genesis_time)

    #台风年发生频次模拟算法
    print "genesis_get_simulated_tc_num STARTS"
    genesis_tc_num = genesis_get_simulated_tc_num(tc_frequency_pdf, n_years_sim)
    
    n_tc_num_sim = sum(genesis_tc_num)
    print "n_tc_num_sim", n_tc_num_sim

    #台风起源时间模拟算法
    print "genesis_get_tc_simulated_time STARTS"
    genesis_time = genesis_get_tc_simulated_time(tc_genesis_time_pdf, n_tc_num_sim)

    #台风起始点位置模拟算法
    print "genesis_get_simulated_location STARTS"
    genesis_location = genesis_get_tc_simulated_location(kernel_pdf, x0, y0, n_cols, n_rows, grid_size, n_tc_num_sim)
    
    cur = db.cursor()
    for i in range(n_tc_num_sim):
        tmpstr = '(' + str(genesis_location[i][0]) + ', ' + str(genesis_location[i][1]) + ', ' + str(genesis_time[i]) + ',' + str(i + 1) + ')'
        sql = 'INSERT INTO "public"."derive_simulation" ("Lon", "Lat", "Hour", "ID")  VALUES' + tmpstr
        cur.execute(sql)
        db.commit()       
	
    total_num = 0
    for i in range(n_tc_num_sim):
        print 'THE', i, 'TH SIMULATED_TRACK:'
        FLAG = 0
        Point_Num = 1
        TRACK_POINT = empty( (35, 3), dtype = 'double')
        #print TRACK_POINT
        TRACK_POINT[0][0] =  genesis_location[i][0]
        TRACK_POINT[0][1] =  genesis_location[i][1]
        TRACK_POINT[0][2] =  genesis_time[i]
                   
        print 'genesis:', TRACK_POINT[0][0], TRACK_POINT[0][1], TRACK_POINT[0][2]

        print 'get_tc_simulated_track STARTS:'
        
        [TRACK, NUM] = get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, genesis_location[i], genesis_time[i], R, FLAG, TRACK_POINT, Point_Num, genesis_end_dat, 0., 0.)
        #NUM = get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, genesis_location[i], genesis_time[i], R, FLAG, TRACK_POINT, Point_Num, genesis_end_dat, 0., 0.)[1]

        print 'NUM:', NUM
        for j in range(NUM):
            #print "TRACK_POINT_DATA", TRACK_POINT[j][0], TRACK_POINT[j][1], TRACK_POINT[j][2]
            print 'LON:', TRACK[j][0], 'LAT:', TRACK[j][1], 'TIME:', TRACK[j][2]
            total_num = total_num + 1
            tmpstr = '(' + str(i) + ', ' + str(TRACK[j][0]) + ', ' + str(TRACK[j][1]) + ', ' + str(TRACK[j][2]) + ', ' + str(i) + str(total_num) + ')'
            sql = 'INSERT INTO "public"."track" ("SNBR", "Lon", "Lat", "Hour", "ID")  VALUES' + tmpstr
            cur.execute(sql)
            db.commit()
        print 'total_num', total_num


    get_tc_simulated_track_DDDAS(db, genesis_all_dat, all_tc_genesis_time, genesis_end_dat, R)
	
	
           
            
	

