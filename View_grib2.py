# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 09:58:02 2014

@author: cranejohnson
"""
#  conda install -c https://conda.binstar.org/jjhelmus pygrib
#  export GRIB_DEFINITION_PATH=/Users/cranejohnson/anaconda/share/grib_api/definitions
# 

import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
#import sys

np.set_printoptions(threshold='nan')

plt.figure()


data = np.loadtxt(open("data.txt","rb"),delimiter=",")

x = np.zeros(0)
y = np.zeros(0)
for row in data:
    if row[2] == 100:
        
        x = np.append(x,[row[0]])
        y = np.append(y,[row[1]])


grib = 'snowsmall.GRIB2'
grbs=pygrib.open(grib)
#
#grbs.seek(0)
#for grb in grbs:
#    print grb 

grb = grbs.select(name='Snow cover')[0]
#snowcover=grb.values
#print snowcover
lat,lon = grb.latlons()

print lon.max()
print lon.min()
print lat.max()
print lat.min()
lon_0 = lon.mean()
lat_0 = lat.mean()

print lon_0
print lat_0

m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=63,lon_0=190)
            

#x, y = m(*np.meshgrid(lon,lat))


m.drawcoastlines()
#m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,10.),labels=[0,0,0,1])
x,y = m(x, y)
m.scatter(x,y,s=.01, c="red", alpha=0.5)
#m.colorbar(cs,orientation='vertical')
plt.title('Example 2: NWW3 Significant Wave Height from GRiB')
plt.show()