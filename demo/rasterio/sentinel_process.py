import os
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio import plot
from osgeo import gdal

# import bands as separate 1 band raster
imagePath = 'E:/Data/Raster/Sentinel-2/S2A_MSIL2A_20210115T023041_N0214_R046_T51QUF_20210115T051635/GRANULE/L2A_T51QUF_A029072_20210115T023713/IMG_DATA\R10m/'
band2 = rasterio.open(imagePath+'T51QUF_20210115T023041_B02_10m.jp2', driver='JP2OpenJPEG') #blue
band3 = rasterio.open(imagePath+'T51QUF_20210115T023041_B03_10m.jp2', driver='JP2OpenJPEG') #green
band4 = rasterio.open(imagePath+'T51QUF_20210115T023041_B04_10m.jp2', driver='JP2OpenJPEG') #red
band8 = rasterio.open(imagePath+'T51QUF_20210115T023041_B08_10m.jp2', driver='JP2OpenJPEG') #nir


# #number of raster bands
# print(band4.count)
# #number of raster columns
# print(band4.width)
# #number of raster rows
# print(band4.height)
# #plot band 
# plot.show(band4)
#type of raster byte
# print(band4.dtypes[0])
# #raster sytem of reference
# print(band4.crs)
# #raster transform parameters
# print(band4.transform)
# #raster values as matrix array
# print(band4.read(1))

#multiple band representation
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
# plot.show(band2, ax=ax1, cmap='Blues')
# plot.show(band3, ax=ax2, cmap='Greens')
# plot.show(band4, ax=ax3, cmap='Reds')
# fig.tight_layout()

#export true color image
# trueColor = rasterio.open(imagePath+'SentinelTrueColor2.tiff','w',driver='Gtiff',
#                          width=band4.width, height=band4.height,
#                          count=3,
#                          crs=band4.crs,
#                          transform=band4.transform,
#                          dtype=band4.dtypes[0]
#                          )
# trueColor.write(band2.read(1),3) #blue
# trueColor.write(band3.read(1),2) #green
# trueColor.write(band4.read(1),1) #red
# trueColor.close()

# #export false color image
# falseColor = rasterio.open(imagePath+'SentinelFalseColor.tiff', 'w', driver='Gtiff',
#                           width=band2.width, height=band2.height,
#                           count=3,
#                           crs=band2.crs,
#                           transform=band2.transform,
#                           dtype='uint16'                   
#                          )
# falseColor.write(band3.read(1),3) #Blue
# falseColor.write(band4.read(1),2) #Green
# falseColor.write(band8.read(1),1) #Red
# falseColor.close()

#generate histogram
trueColor = rasterio.open(imagePath+'SentinelTrueColor2.tiff')
plot.show_hist(trueColor, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title="Histogram")


## To do

# Download Sentinel-2 data

# Read Sentinel-2 data

# Composite True Color Image

# Clip to a region of interest

# Calculate NDVI

# Plot NDVI