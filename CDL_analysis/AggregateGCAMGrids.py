#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 21:33:10 2018

@author: lejoflores
"""


import gdal
import glob
import os
from joblib import Parallel, delayed


#=============================================================================#

AggRes = 3.0

#=============================================================================#
# Set master working  directories                                             #
#=============================================================================#
# Base user directories
lejo_test = '/Users/lejoflores/IM3-BoiseState/CDL_analysis/'
#kendra_test = '/Users/kek25/Documents/GitRepos/IM3-BoiseState/CDL_analysis/'

user = lejo_test
#user = kendra_test

# Specific directories of where to find the data
# GCAM_GridDir = 'D:\Dropbox\BSU\Python\Data\GCAM_SRP'
GCAM_ReadDir   = user + 'GCAM_SRP/'
GCAM_ReadFiles = glob.glob(GCAM_ReadDir+'gcam*srb.tiff')

# Location and name of output file
GCAM_ReprojWriteDir  = GCAM_ReadDir + '3km/'


#=============================================================================#
# FUNCTION DEFINITIONS    
def AggregateGCAMGrid(GCAM_ReadDir,GCAM_ReadFile,GCAM_WriteDir,AggRes):
    
    # Open the GeoTiff based on the input path and file
    src_ds = gdal.Open(GCAM_ReadDir+GCAM_ReadFile)

    # Create the name of the output file by modifying the input file
    GCAM_WriteFile = GCAM_ReadFile.replace('srb','srb_utm11N'+'_'+str(int(AggRes)))

    # Get key info on the source dataset    
    src_ncols = src_ds.RasterXSize
    src_nrows = src_ds.RasterYSize
    
    src_geot = src_ds.GetGeoTransform()
    src_proj = src_ds.GetProjection()
    src_res  = src_ds.GetGeoTransform()[1]

    agg_factor = AggRes / src_res

    dst_ncols = (int)(src_ncols/agg_factor)
    dst_nrows = (int)(src_nrows/agg_factor)
    
    dst_driver = gdal.GetDriverByName('Gtiff')
    
    dst_geot = (src_geot[0], src_geot[1]*agg_factor, src_geot[2], src_geot[3], src_geot[4], src_geot[5]*agg_factor)
    dst_proj = src_proj
    
    dst_ds = dst_driver.Create(GCAM_AggWriteDir+GCAM_AggWriteFile, dst_ncols, dst_nrows, 1, gdal.GDT_Float32)
    dst_ds.SetGeoTransform(dst_geot)
    dst_ds.SetProjection(dst_proj)



