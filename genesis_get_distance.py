#!/usr/bin/python
# -*- coding: UTF -8 -*-

from math import asin, sin, cos, acos, radians, degrees, pow, sqrt, hypot, pi

# 根据经纬度计算两点间距离
# 经度 long  纬度 lat

def genesis_get_distance( lng1,  lat1,  lng2,  lat2):
    #'''''计算两点间球面距离 单位为km'''
    EARTH_RADIUS = 6378.137
    # 地球周长/2*pi 此处地球周长取40075.02km pi=3.1415929134165665
    from math import asin,sin,cos,acos,radians, degrees,pow,sqrt, hypot,pi

    # 方法0
    # 最简单的求平面两点间距离 误差比较大
    #d=hypot(lng2-lng1,lat2-lat1)*40075.02/360
    #print 'd0=',d

    #方法1
    #'''经纬坐标为P(x1,y1) Q(x2,y2) '''
    #   D=2*arcsin(sqrt(pow(2*R*sin((y2-y1)/2),2)+pow(2*R*sin((x2-x1)/2),2))/(2*R))*2*R
    radLat1 = radians(lat1) # a点经度(单位是弧度）
    radLat2 = radians(lat2) # b点纬度(单位是弧度）
    a = radLat1 - radLat2 # 两点间的纬度弧度差

    radLng1 = radians(lng1) # a点经度(单位是弧度)
    radLng2 = radians(lng2) # b点经度(单位是弧度）
    b = radLng1 - radLng2 # 两点间的经度弧度差

    l1 = 2 * EARTH_RADIUS * sin(a/2)
    l2 = 2 * EARTH_RADIUS * sin(b/2)
    l3 = sqrt(pow(l1,2) + pow(l2,2))

    d = EARTH_RADIUS * 2 * asin(l3/(2 * EARTH_RADIUS))
    #print 'd1=', d

    # 方法2
    #  '''  d＝111.12cos{1/[sinΦAsinΦB+cosΦAcosΦBcos(λB—λA)]}    '''
    # ''' 其中A点经度、纬度分别为λA和ΦA，B点的经度、纬度分别为λB和ΦB，d为距离。'''
    #m=cos(radians(lat1))*cos(radians(lat2))*cos(radians(lng2-lng1))
    #x=1/(sin(radians(lat1))*sin(radians(lat2)) +m)
    #d=111.12*cos(radians(1/x))    
    #print 'd2=',d

    # 方法3
    #radLat1 = radians(lat1) # a点纬度(单位是弧度)
    #radLat2 = radians(lat2) # b点纬度(单位是弧度
    #a = radLat1 - radLat2 # 两点间的纬度弧度差
    #b = radians(lng1) - radians(lng2) # 两点间的经度弧度差
    #s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2))) # 两点间的弧度
    #s = s * EARTH_RADIUS
    #   s = round(s * 10000) / 10000 # 四舍五入保留小数点后4位
    #d=s
    #print 'd3=',d

    # 方法4
    # ''' 经纬坐标为P(x1,y1) Q(x2,y2) '''
    #   D=arccos[cosy1*cosy2*cos(x1-x2)+siny1*siny2]*2*PI*R/360
    #d=acos(cos(radians(lat1))*cos(radians(lat2))*cos(radians(lng1-lng2))+sin(radians(lat1))*sin(radians(lat2)))*EARTH_RADIUS
    #print 'd4=',d

    #方法5
    #'''经纬坐标为P(x1,y1) Q(x2,y2)'''
    #   D=arctan[sqrt(pow(cosy2*sin(x1-x2),2)+pow(cosy1*siny2-siny1*cosy2*cos(x1-x2),2))/siny1*siny2+cosy1*cosy2*cos(x1-x2)]*2*PI*R/360
    #d=atan(sqrt(pow(cos(radians(lat2)*sin(radians(lng1-lng2)),2)+pow(cos(radians(lat1)*sin(radians(lat2)-sin(radians(lat1)*cos(radians(lat2))*cos(radians(lng1-lng2)),2)/
    #print 'd5=', d
    
    return d
