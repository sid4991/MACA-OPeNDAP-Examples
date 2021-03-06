#!/usr/bin/python
#This script was run using Python 2.7.3, the Enthought distribution (www.enthought.com)
#author:Katherine Hegewisch (khegewisch@uidaho.edu)
#updated: 01/01/2015
#=========================================================
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
#=========================================================
#            SET TARGET DATA 
#=========================================================
day=1
lat_target=45.0
lon_target=360-117.0
#=========================================================
#             SET OPENDAP PATH 
#=========================================================
pathname = 'http://inside-dev1.nkn.uidaho.edu:8080/thredds/dodsC/agg_maca_huss_BNU-ESM_r1i1p1_historical_1950_2005_WUSA.nc';
#=========================================================
#             GET DATA HANDLES
#=========================================================
filehandle=Dataset(pathname,'r',format="NETCDF4")
lathandle=filehandle.variables['lat']
lonhandle=filehandle.variables['lon']
timehandle=filehandle.variables['time']
datahandle=filehandle.variables['specific_humidity']
#=========================================================
#             GET DATA 
#=========================================================
#get data
time_num=len(timehandle)
timeindex=range(day-1,time_num,365)  #python starts arrays at 0
time=timehandle[timeindex]
lat = lathandle[:]
lon = lonhandle[:]
#=========================================================
#find indices of target lat/lon/day
lat_index =  np.searchsorted(lat,lat_target,side='left')
lon_index =  np.searchsorted(lon,lon_target,side='left')
#check final is in right bounds
if(lat[lat_index]>lat_target):
	if(lat_index!=0):
		lat_index = lat_index - 1
if(lat[lat_index]<lat_target):
	if(lat_index!=len(lat)):
		lat_index =lat_index +1
if(lon[lon_index]>lon_target):
	if(lon_index!=0):
		lon_index = lon_index - 1
if(lon[lon_index]<lon_target):
	if(lon_index!=len(lon)):
		lon_index = lon_index + 1
lat=lat[lat_index]
lon=lon[lon_index]
#=========================================================
#get data
data = datahandle[timeindex,lat_index,lon_index]
#=========================================================
#              MAKE A PLOT
#=========================================================
yearref=1950
years = np.arange(yearref,yearref+len(time))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(u'Year')
ax.set_ylabel(u'Specific Humidity')
ax.set_title(u'Specific Humidity on Day %d ,\n %4.2f\u00b0N, %4.2f\u00b0W' % (day,lat, abs(360-lon)))
#ax.plot_date(x=time,y=data,fmt="b-")
ax.ticklabel_format(style='plain')
ax.plot(years,data,'b-')
plt.savefig("myPythonGraph.png")
plt.show()
