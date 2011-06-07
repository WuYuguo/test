#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_kernel_pdf
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#   caculate the kernal density for a user-specified region from the historical
#   genesis longitude and latitue.
#
# INPUTS:
#   genesis_his_ll: a 2 x n single-, or double-precision floating-point vector that is
#                   the longitude, latitude of each historical genesis
#   x0, y0     : the longitude, latitude of kernel area origin (left, down)
#   n_cols, n_rows: the cols and rows of the kernel area
#   grid_size  : a single-, or double-precision floating-point scalar define the grid size
#                of the the kernel area
#   R          : a single-, or double-precision floating-point scalar that defines the
#                radius/distance (kilometer) for kernel density calculation
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   A n_cols x n_rows floating-point array represents the kernel density PDF,
#   where result[0,0] represents the kernel PDF of point x0, y0
#
# OPTIONAL OUTPUTS:

import random
import numpy
from math import asin, sin, cos, acos, radians, degrees, pow, sqrt, hypot, pi
from genesis_get_distance import *

#台风起始点核密度计算
def genesis_get_kernel_pdf(db, genesis_his_ll, x0, y0, n_cols, n_rows, grid_size, R):
    cur = db.cursor()
        
#    sql = 'SELECT "Lon", "Lat" FROM "public"."genesis_his_derive"'
#    cur.execute(sql)
#    rows = cur.fetchall()

#    global genesis_pts = numpy.array(rows)
#    print genesis_pts.shape[0]

#    global genesis_his_ll
#    genesis_his_ll = numpy.array(genesis_his_ll)
    
    n_pts = len(genesis_his_ll)
    print "history data number:", n_pts

    #设定的R对应的经纬度范围
    R_degree = float(R) * 0.015

    pdf_rst = []
    for j in range(n_rows):
        pdf_rst.append([])
        for i in range(n_cols):
            pdf_rst[j].append(0.)
            
    for int_col in range(n_cols):
        for int_row in range(n_rows):
            x_grid_centroid = x0 + (int_col + 0.5) * grid_size
            y_grid_centroid = y0 + (int_row + 0.5) * grid_size
            #print x_grid_centroid, y_grid_centroid

            for int_pt in range(n_pts):
                #print genesis_his_ll[int_pt][0], genesis_his_ll[int_pt][1]
                #选取一定范围内的台风起始点并计算核密度
                if(abs(float(genesis_his_ll[int_pt][0]) - x_grid_centroid) <= R_degree and abs(float(genesis_his_ll[int_pt][1]) - y_grid_centroid) <= R_degree ):
                    dis = genesis_get_distance(float(genesis_his_ll[int_pt][0]), float(genesis_his_ll[int_pt][1]), x_grid_centroid, y_grid_centroid)
                    if(abs(dis) <= R):
                        pdf_rst[int_row][int_col] = pdf_rst[int_row][int_col] + 1.0 - dis/R
                            
                #rst_pdf[j][i] = 2 * rst_pdf[j][i]/(pi * pow(lengthscale,2))
            #print "distribution:", pdf_rst[int_row][int_col]

    pdf_max = max(max(pdf_rst))
    pdf_min = min(min(pdf_rst))
    print 'pdf_max:', pdf_max
    print 'pdf_min:', pdf_min

    #
    #print "pdf_rst:"
    #f = file("C:\VERSION FOR GENESIS_SIM\genesis_sim 5.28 afternoon\dat\kernel_pdf.txt", "a +")
    #for j in range(n_rows):
        #print pdf_rst[n_rows - 1 - j]
        #for i in range(n_cols):
            #f.write(str(pdf_rst[n_rows - 1 - j][i]) + ' ')
        #f.write('\n')
    #f.write("max: " + str(pdf_max))
    #f.write("min: " + str(pdf_min))
    #f.close()
    #


    #核密度的归一化

    for j in range(n_rows):
         for i in range(n_cols):
            pdf_rst[j][i] = (pdf_rst[j][i] - pdf_min) / (pdf_max - pdf_min)

    #for j in range(35,40):
        #for i in range(155,160):
            #print pdf_rst[j][i]
                
    pdf_max = max(max(pdf_rst))
    pdf_min = min(min(pdf_rst))
    print 'pdf_max:', pdf_max
    print 'pdf_min:', pdf_min


    #
    #print "pdf_rst final:"
    #f = file("C:\VERSION FOR GENESIS_SIM\genesis_sim 5.28 afternoon\dat\kernel_pdf_final.txt", "a +")
    #for j in range(n_rows):
        #print pdf_rst[n_rows - 1 - j]
        #for i in range(n_cols):
            #f.write(str(pdf_rst[n_rows - 1 - j][i]) + ' ')
        #f.write('\n')
    #f.write("max: " + str(pdf_max))
    #f.write("min: " + str(pdf_min))
    #f.close()
    #

    
    return pdf_rst

