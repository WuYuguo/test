#!/usr/bin/python
# -*- coding: UTF -8 -*-

def genesis_read_all(db):
    cur = db.cursor()
    sql = 'SELECT "Year", "Month", "Day", "Hour", "Lon", "Lat", "TranslationSpeed", "Heading" FROM "public"."bstrack"'
    cur.execute(sql)
    rows = cur.fetchall()

    global all_data
    all_data = rows

    return all_data
