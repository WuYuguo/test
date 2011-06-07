#!/usr/bin/python
# -*- coding: UTF -8 -*-

def genesis_read_his(db):
    cur = db.cursor()
    sql = 'SELECT COUNT(*) FROM "public"."genesis_his_derive"'
    cur.execute(sql)
    rows = cur.fetchall()

    if rows[0][0] == 0:
        print 'genesis_his_derive IS NULL'
        cur = db.cursor()
        sql = 'SELECT * FROM "public"."bstrack" WHERE "public"."bstrack"."GenesisLysis" = 1'
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            tmpstr1 = "(\'"+row[0]+"\'"+", "+str(row[1])+", "+" \'"+row[2]+"\'"+", "+str(row[3])+", "+str(row[4])+", "+str(row[5])+", "
            tmpstr2 = str(row[6])+", " +str(row[7])+", "+ str(row[8])+", "+"\'"+row[9]+"\'"+","+" \'"+row[10]+"\'"+", "
            tmpstr3 = "\'"+row[11]+"\'"+", "+str(row[12])+", "+str(row[13])+", "+ str(row[14]) +", "+str(row[15])+", "
            tmpstr4 = str(row[16])+", "+str(row[17])+", "+ str(row[18])+", "+   str(row[19])+", "+str(row[20])+")"
                
        sql = 'INSERT INTO "public"."genesis_his_derive" VALUES' +tmpstr1 +tmpstr2 +tmpstr3 +tmpstr4
        cur.execute(sql)

        db.commit()
        #genesis_his_derive.genesis_his_derive(db)
        
    else:
        print 'genesis_his_derive IS NOT NULL'

    sql = 'SELECT "Year", "Month", "Day", "Hour", "Lon", "Lat" FROM "public"."genesis_his_derive"'
    cur.execute(sql)
    rows = cur.fetchall()

    global derive_data
    derive_data = rows
#    for i in range(20):
#        print 'the data:', rows[i]

    return derive_data
