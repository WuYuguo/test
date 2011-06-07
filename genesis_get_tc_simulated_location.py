#!/usr/bin/python
# -*- coding: UTF -8 -*-

# NAME:
#   genesis_get_tc_simulated_location
#
# AUTHOR:
#   zhengguangyuan, Peking University
#   guanxiaoyuan@gmail.com
#
# PURPOSE:
#    Derive simulated location according to the kernel pdf
#
# INPUTS:
#   kernel_pdf      : An n_cols x n_rows floating-point array represents the kernel density PDF,
#                     where result[0,0] represents the kernel PDF of point x0, y0
#   x0, y0          : the longitude, latitude of kernel area origin (left, down)
#   grid_size       : a single-, or double-precision floating-point scalar define the grid size
#                     of the the kernel area
#   n_cols, n_rows  : the cols and rows of the kernel area
#   n_points        : a int or long scalar that represent how many simulated location point 
#                     will be derived
#
# OPTIONAL INPUTS:
#
# KEYWORD PARAMETERS:
#
# OUTPUTS:
#   A 2*n_points floating arrary that contains the simulated location of longitude and latitude
#
# OPTIONAL OUTPUTS:


import genesis_get_distance
import random

#台风起始点位置模拟算法
def genesis_get_tc_simulated_location(kernel_pdf, x0, y0, n_cols, n_rows, grid_size, n_points):
    #point = ogr.Geometry(ogr.wkbPoint)
    
    rst_location = []
    for j in range(n_points):
        rst_location.append([])
        for i in range(2):
            rst_location[j].append(0.)
            
    #for i in range(n_points):
        #rst_location[i][0] = 0.
        #rst_location[i][1] = 0.

    int_point = 0

    while int_point < n_points:
        #生成随机点
        x_rand = random.uniform(0.,1.)
        y_rand = random.uniform(0.,1.)
        #point.AddPoint(random_x,random_y)

        int_col = int(x_rand * n_cols) + 1
        if int_col > n_cols - 1:
            int_col = n_cols - 1
        int_row = int(y_rand * n_rows) + 1
        if int_row > n_rows - 1:
            int_row = n_rows - 1

        pdf = kernel_pdf[int_row][int_col]
        rand_pdf = random.uniform(0., 1.)

        #判断是否接受作为起始点
        if rand_pdf < pdf:
            #print 'add a genesis_point'
            rst_location[int_point][0] = x_rand
            rst_location[int_point][1] = y_rand
            int_point = int_point + 1

    #生成的起始点坐标	
    for i in range(n_points):
        rst_location[i][0] = rst_location[i][0] * grid_size * n_cols + x0
        rst_location[i][1] = rst_location[i][1] * grid_size * n_rows + y0
    	print "rst_location", i, rst_location[i][0], rst_location[i][1]
    return rst_location            
            
