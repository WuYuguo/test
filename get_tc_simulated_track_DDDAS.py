#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   get_tc_simulated_track_DDDAS
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   simulate the whole typhoon track with the real-time data
#
# INPUTS:
#   the historical data of typhoon track
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS: all the point along the simulated typhoon track


from genesis_get_his_tc_genesis_time import *
from get_tc_simulated_track import *
from numpy import *

#实时数据下的路径模拟
def get_tc_simulated_track_DDDAS(db, genesis_all_dat, all_tc_genesis_time, genesis_end_dat, R):
	
    cur = db.cursor()
    sql = ' SELECT "Lon", "Lat", "TranslationSpeed", "Heading" FROM "public"."bstrack" WHERE "public"."bstrack"."SNBR" = \'200805\' '
    cur.execute(sql)
    rows = cur.fetchall()
	
    global real_time_data
    real_time_data = rows
    real_time_data_num = len(real_time_data)

    print 'real_time_data_num:', real_time_data_num
    
    sql = ' SELECT "Year", "Month", "Day", "Hour", "Lon", "Lat" FROM "public"."bstrack" WHERE "public"."bstrack"."SNBR" = \'200805\' '
    cur.execute(sql)
    rows = cur.fetchall()
    
    global real_time_dat
    real_time_dat = rows
    real_time = genesis_get_his_tc_genesis_time(real_time_dat)

    TRACK_REAL_TIME = empty((real_time_data_num + 1, 35, 3), dtype = 'double')
    TRACK_NUM = []
    TRACK_NUM.append(real_time_data_num)

    a = 0.6
    b = 0.8

    #原始路径
    for i in range(real_time_data_num):
        TRACK_REAL_TIME[0][i][0] = real_time_data[i][0]
        TRACK_REAL_TIME[0][i][1] = real_time_data[i][1]
        TRACK_REAL_TIME[0][i][2] = real_time[i]

    #随着实时数据的不断更新 对不同路径不断更新点
    for i in range(1, real_time_data_num + 1):
        for j in range(i - 1):
            TRACK_REAL_TIME[i][j][0] = TRACK_REAL_TIME[i - 1][j][0]
            TRACK_REAL_TIME[i][j][1] = TRACK_REAL_TIME[i - 1][j][1]
            TRACK_REAL_TIME[i][j][2] = TRACK_REAL_TIME[i - 1][j][2]

        if(i == 1):
            a = 0.
            b = 1.0

        #由上一条路径的对应点和原始路径的对应点计算当前路径的对应点的坐标    
        TRACK_REAL_TIME[i][i - 1][0] = a * TRACK_REAL_TIME[i - 1][i - 1][0] + b * TRACK_REAL_TIME[0][i - 1][0]
	TRACK_REAL_TIME[i][i - 1][1] = a * TRACK_REAL_TIME[i - 1][i - 1][1] + b * TRACK_REAL_TIME[0][i - 1][1]
	TRACK_REAL_TIME[i][i - 1][2] = a * TRACK_REAL_TIME[i - 1][i - 1][2] + b * TRACK_REAL_TIME[0][i - 1][2]
		
	genesis_location = []
	genesis_location.append(TRACK_REAL_TIME[i][i - 1][0])
	genesis_location.append(TRACK_REAL_TIME[i][i - 1][1])
	genesis_time = TRACK_REAL_TIME[i][i - 1][2]

	#进行该条路径的模拟		
	[TRACK_DDDAS, TRACK_DDDAS_NUM] = get_tc_simulated_track(genesis_all_dat, all_tc_genesis_time, genesis_location, genesis_time, R, 0, TRACK_REAL_TIME[i], i, genesis_end_dat, 0., 0.)
	TRACK_NUM.append(TRACK_DDDAS_NUM)
	print 'TRACK_DDDAS_NUM:', TRACK_DDDAS_NUM

	print 'THE', i, 'th simulated process infomation is:'	
	for k in range(TRACK_DDDAS_NUM):
            print 'LON:', TRACK_DDDAS[k][0], 'LAT:', TRACK_DDDAS[k][1], 'TIME:', TRACK_DDDAS[k][2]

    DDDAS_total_num = 0

    #输出不断模拟的路径
    for i in range(real_time_data_num + 1):
        print 'THE', i, 'TH DDDAS_SIMULATION_TRACK'
        for j in range(TRACK_NUM[i]):
            print TRACK_REAL_TIME[i][j][0], TRACK_REAL_TIME[i][j][1], TRACK_REAL_TIME[i][j][2]

            DDDAS_total_num = DDDAS_total_num + 1
            tmpstr = '(' + str(i) + ', ' + str(TRACK_REAL_TIME[i][j][0]) + ', ' + str(TRACK_REAL_TIME[i][j][1]) + ', ' + str(TRACK_REAL_TIME[i][j][2]) + ', ' + str(i) + str(DDDAS_total_num) + ')'
            sql = 'INSERT INTO "public"."DDDAS_track" ("SNBR", "Lon", "Lat", "Hour", "ID")  VALUES' + tmpstr
            cur.execute(sql)
            db.commit()

        print 'total_num', DDDAS_total_num

            
        

