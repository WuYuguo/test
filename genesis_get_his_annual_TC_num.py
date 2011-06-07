#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_his_annual_TC_num
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   Derive the typhoon frequency by year in history
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
#   a integer vector, each element represents the frequency of each year
#
# OPTIONAL OUTPUTS:

#台风年发生平频次的统计
def genesis_get_his_annual_TC_num(db, genesis_his_dat):

    cur = db.cursor()
    sql = 'SELECT COUNT(*) FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        print 'all', row

    if rows[0][0] == 0:
        print 'frequency IS NULL'
        #genesis_his_annual_num_derive.genesis_his_annual_num_derive(db)
        
        cur = db.cursor()
        sql = 'SELECT "Year", COUNT(*) AS "Count" FROM "public"."genesis_his_derive" GROUP BY "public"."genesis_his_derive"."Year" ORDER BY "Year"'
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            tmpstr = "(\'"+row[0]+"\', "+str(row[1])+")"
            sql = 'INSERT INTO "public"."frequency" ("Year", "Count") VALUES'+tmpstr
            cur.execute(sql)

        db.commit()
        
    else:
        print 'frequency:', rows[0][0]

    sql = 'SELECT COUNT(*) FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        print 'frequency now is ', row

    sql = 'SELECT * FROM "public"."frequency"'
    cur.execute(sql)
    rows = cur.fetchall()

    global annual_tracknum
    annual_tracknum = rows

    return annual_tracknum
