#!/usr/bin/python
# -*- coding: UTF -8 -*-

def genesis_read_end(db):
    cur = db.cursor()
    sql = 'SELECT "Lon", "Lat" FROM "public"."bstrack" WHERE "public"."bstrack"."GenesisLysis" = 2'
    cur.execute(sql)
    rows = cur.fetchall()

    global end_data
    end_data = rows

    return end_data
