#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_his_tc_genesis_time
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   Derive the history typhoon genesis time from the historic typhoon data
#
# INPUTS:
#   genesis_tc_data: a 7 x n vector , repectively,each column represents typhoon N0,typhoon 
#                    genesis time about year、month、day and hour,typhoon genesis location of
#                    longitude and latitude
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   a ineger vector, each element represents the typhoon genesis time in history
#   its unit is hour,for example, if the input of one typhoon genesis time is July,30,2005
#   we cauclute how many hours is it From January,1,2005, it output 5052 hour.
#
# OPTIONAL OUTPUTS:

#台风点时间按小时计算
def genesis_get_his_tc_genesis_time(genesis_his_dat):
    
    #cur = db.cursor()
    #sql = 'SELECT "Year", "Month", "Day", "Hour" FROM "public"."genesis_his_derive"'
    #cur.execute(sql)
    #rows = cur.fetchall()

    #global time_data
    #time_data = rows
    time_data = genesis_his_dat
    #global his_TGT
    his_TGT = []
	
    print len(time_data)
    for i in range(len(time_data)):
        if time_data[i][1] == '1':
            his_TGT.append( 24 * int(time_data[i][2]) + int(time_data[i][3]) )
        elif time_data[i][1] == '2':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31) + int(time_data[i][3]) )
        elif time_data[i][1] == '3':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '4':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 2 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '5':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 2 + 30 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '6':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 3 + 30 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '7':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 3 + 30 * 2 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '8':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 4 + 30 * 2 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '9':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 5 + 30 * 2 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '10':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 5 + 30 * 3 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '11':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 6 + 30 * 3 + 28) + int(time_data[i][3]) )
        elif time_data[i][1] == '12':
            his_TGT.append( 24 * (int(time_data[i][2]) + 31 * 6 + 30 * 4 + 28) + int(time_data[i][3]) )

    #print 'HOUR LIST'

    #for i in range(len(time_data)):
    	#print i, 'th hour', his_TGT[i]
    return his_TGT

    
    
