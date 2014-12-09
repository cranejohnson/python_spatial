# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 22:08:11 2014

@author: cranejohnson
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import re
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
from scipy.interpolate import griddata
from nwsgrid import *
from pylab import savefig


#hrap details
oauhhrap ={'xmin' : -963.875,
           'xmax' : -950.125,
           'xnum' : 55,
           'ymin' : 586.625,
           'ymax' : 565.375,
           'ynum' : 85 }

#Model domain details
mgrid=  {  'xmin' : 197.65,
           'xmax' : 207.64,
           'xnum' : 223,
           'ymin' : 16.4,
           'ymax' : 24.005,
           'ynum' : 170 }

hrap = oauhhrap
    
#Set up the hrap grid and create a mesh of both hrapi and hrapj 
hrapi = np.linspace(hrap['xmin'],hrap['xmax'],hrap['xnum'])
hrapj = np.linspace(hrap['ymin'],hrap['ymax'],hrap['ynum'])
hrapi, hrapj = np.meshgrid(hrapi, hrapj)  # make lats/lons into 2D arrays (needed for plotting)

hraplat = np.empty((hrap['ynum'],hrap['xnum']))
hraplon = np.empty((hrap['ynum'],hrap['xnum']))

#hrapp = numpy.empty((0,2))
for rindx, row in enumerate(hrapi):
   for cindx, element in enumerate(row):
       x,y = hraptoLatLon(hrapi[rindx,cindx],hrapj[rindx,cindx])
       hraplon[rindx,cindx],hraplat[rindx,cindx] = x,y

#Get the corners of the grid    
hlat = hraplat[[0,0,-1,-1],[0,-1,0,-1]]
hlon = hraplon[[0,0,-1,-1],[0,-1,0,-1]]



filename = 'HiResW-ARW-HI-2014-12-08-12-FH-048.h5'
            
file = h5py.File(filename, 'r')   # 'r' means that hdf5 file is open in read-only mode

for g in file:
    if re.search('TP3hr',g):
        dataset = g
        
group = file[dataset]

data = group['Data']

flat = np.zeros(0)
for d in data:
    flat = np.append(flat,d)

print flat

lats = np.linspace(mgrid['ymin'],mgrid['ymax'],mgrid['ynum'])
lons = np.linspace(mgrid['xmin'],mgrid['xmax'],mgrid['xnum'])
lons, lats = np.meshgrid(lons, lats)  # make lats/lons into 2D arrays (needed for plotting)


#Set up the basemap
centy = (hraplat[0][0]+hraplat[0][-1])/2
centx = (hraplon[0][0]+hraplon[-1][0])/2
print centx
print centy
m = Basemap(projection='stere',lon_0=centx,lat_0=centy,width=500000,height=500000)
# convert lats/lons to map projection coordinates
x,y = m(lons, lats) 
# Plot the model point locations
m.scatter(x,y,s=0.5,color="red",alpha=0.5)
# Plot the model precipitation data
cs = m.contourf(x,y,data,np.linspace(1,50,11),cmap=plt.cm.jet)  # color-filled contours
#draw latitdue on the map
parallels = m.drawparallels(np.arange(10,90,2.5),labels=[1,0,0,0])  # draw parallels, label on left
#draw longitude on the map
meridians = m.drawmeridians(np.arange(-10,-200,-2.5),labels=[0,0,0,1]) # label meridians on bottom
# add title
t = plt.title('1 Hour Precipitation',fontweight='bold')

#Get a list of lat long points
points =  np.dstack((x.flatten(),y.flatten()))
pts = points[0]

#Put the hrap coordinates into map coordinates
hx,hy = m(hraplon,hraplat)

#grid the data from the model onto the new hrap grid
imethod = 'linear'
hrapg = griddata(pts,flat,(hx,hy), method=imethod)

#Plot the hrap precip grid on map
#hs = m.contourf(hx,hy,hrapg,np.linspace(1,50,11),cmap=plt.cm.jet)

cb = m.colorbar(cs)  # draw colorbar
#add shaded releif as basemap
m.shadedrelief(scale=0.5)
#draw county lines on map
m.drawcounties(linewidth=1, linestyle='solid', color='k')

#Get map coordinates for grid corners and plot them
z,q = m(hlon,hlat)
m.scatter(z,q,color="blue",s=5)

i=99
#save the map
filename = 'image'+str(i)+imethod+'.png'
savefig(filename)

#Create and save the xmrg file
f = open('myfile','w')
xmrg = writeXMRG(hrapi[-1][0],hrapj[-1][0],hrapg)
f.write(xmrg) # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call if



plt.show()

