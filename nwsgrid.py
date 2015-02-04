# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 23:09:39 2014

@author: cranejohnson

Library file that contains HRAP and XMRG functions

"""
import math
from struct import pack

"""
Function: writeXMRG
Purpose: Writes a grid to xmrg pre-97 format (1 header line)
 
@param xorg float    HRAP-X coordinate of the southwest corner of grid
@param yorg float    HRAP-Y coordinate of the southwest corner of grid
@param grid 2darray  Grid of data points    
@return string containing the binary XMRG grid data.
"""
def writeXMRG(xorg,yorg,grid):
    binaryData = ''
    rows,cols = grid.shape

    #xmrg binary header for hawaii
    #00016 00000 63488 50288 22528 17421 00055 00000
    #00085 00000 00016 00000 00016 00000 00001 00000
    #00004 00000 65535 15999 15360 50716 00016 00000

    #Hex header
    #0010 0000 f800 c470 5800 440d 0037 0000
    #0055 0000 0010 0000 0010 0000 0001 0000
    #0004 0000 ffff 3e7f 3c00 c61c 0010 0000

    #Data after this
    
    #Print the first line of header info
    binaryData += pack('iffiii',16,xorg,yorg,cols,rows,16)
    #Print the second line of header info    
    binaryData += pack('iiiffi',16,1,4,0.25,-9999,16)

    for row in grid:
        binaryData += pack('>i',2*cols)
        for c in row:
            binaryData += pack('>i',c)
        binaryData += pack('>i',2*cols)

    #binaryData = ''.join([c for t in zip(binaryData[1::2], binaryData[::2]) for c in t])
    return(binaryData)

    
"""
Function: latLongToHRAP
Purpose: Converts a latitude and longitude into an HRAP grid point.

@param latLong object that defines the point we are converting.
@param roundToNearest boolean specifies if we want to round the hrap point to the nearest integer value.
@param adjustToOrigin boolean specifies if we want to adjust the hrap point to the origin of the file.
@return list with hrap coordiantes [x,y]
"""

def latLongToHRAP(latLong, roundToNearest=False, adjustToOrigin=False):
    flat = math.radians( latLong.latitude )
    flon = math.radians( abs(latLong.longitude) + 180.0 - self.startLong )
    r = self.meshdegs * math.cos(flat)/(1.0 + math.sin(flat))
    x = r * math.sin(flon)
    y = r * math.cos(flon)
    hrap = hrapCoord( x + 401.0, y + 1601.0 )   
    return(hrap)





"""

Function: hraptoLatLong
Purpose: Converts HRAP grid point to latitude and longitude 

@param hrapi float X hrap coordinate
@param hrapj float Y hrap coordinate
@returnlist  Latlon
"""    

def hraptoLatLon(hrapi,hrapj):
    earthr = 6371.2
    stlon = 105
    raddeg = 57.29577951
    xmesh = 4.7625

    tlat = 60/raddeg
    x = hrapi - 401
    y = hrapj - 1601
    rr = pow(x,2) + pow(y,2)
    gi = pow(((earthr * (1+math.sin(tlat)))/xmesh),2)
    lat = math.asin((gi-rr)/(gi+rr))*raddeg
    ang = math.atan2(y,x)*raddeg

    if (ang<0):
        ang=ang+360
    lon = 270+stlon-ang

    if (lon < 0):
        lon=lon+360
    if (lon > 360):
        lon=lon-360

    return (360-lon,lat)
