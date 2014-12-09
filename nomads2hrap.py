#  Steps to get this up and running
#  1. Install Anaconda
#  2. conda install libnetcdf
#  3. conda install netcdf4
#  4. conda install basemap

#matplotlib inline 
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import griddata
from pylab import savefig
import math
import time
from struct import pack
import nwsgrid
#from netCDF4 import num2date


#hrap details
oauhhrap ={'xmin' : -963.875,
           'xmax' : -950.125,
           'xnum' : 55,
           'ymin' : 586.625,
           'ymax' : 565.375,
           'ynum' : 85 }


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

#Get the netCDF4 dataset
gfs_fcst = Dataset('http://nomads.ncep.noaa.gov:9090/dods/hiresw/hiresw20141208/hiresw_hiarw_00z')

lats = gfs_fcst.variables['lat'][:] 
lons = gfs_fcst.variables['lon'][:]
lons, lats = np.meshgrid(lons, lats)  # make lats/lons into 2D arrays (needed for plotting)

points =  np.dstack((lats.flatten(),lons.flatten()))

fcst_time = gfs_fcst.variables['time']

#valid_dates = num2date(time[:])

surfprecip = gfs_fcst.variables['apcpsfc']


i=0
for prcp in surfprecip:
    if i!=3:
        i+=1
        continue
    flat = prcp.flatten()
    fig = plt.figure(figsize=(10,10))

    #Set up the basemap
    m = Basemap(projection='stere',lon_0=-158,lat_0=21.4,width=500000,height=500000)
    # convert lats/lons to map projection coordinates
    x,y = m(lons, lats) 
    # Plot the model point locations
    m.scatter(x,y,s=0.5,color="red",alpha=0.5)
    # Plot the model precipitation data
    cs = m.contourf(x,y,prcp,np.linspace(1,50,11),cmap=plt.cm.jet)  # color-filled contours
    #draw latitdue on the map
    parallels = m.drawparallels(np.arange(10,90,2.5),labels=[1,0,0,0])  # draw parallels, label on left
    #draw longitude on the map
    meridians = m.drawmeridians(np.arange(-10,-200,-2.5),labels=[0,0,0,1]) # label meridians on bottom
    # add title
    t = plt.title('1 Hour Precipitation  Timestep %d' % i,fontweight='bold')
    #Put the points in an array [[x1,y1],[x2,y2].....]
    points =  np.dstack((x.flatten(),y.flatten()))
    pts = points[0]
    #Put the hrap coordinates into map coordinates
    hx,hy = m(hraplon,hraplat)

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
    #z,q = m(hlon,hlat)
    #m.scatter(hx,hy,color="blue",s=0.5)

    #save the map
    filename = 'image'+str(i)+imethod+'.png'
    savefig(filename)

    #Create and save the xmrg file
    f = open('myfile','w')
    xmrg = writeXMRG(hrapi[-1][0],hrapj[-1][0],hrapg)
    f.write(xmrg) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if

    plt.show()

    i += 1







