#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script that automates the data import,
data renaming and flattening of the downloads.
Secondly, it crops the provided raster images by its shapefile counterparts
Finally, it transforms the raster datasets into a EPSG:3857 (Google Web Mercator) Projection
"""
import subprocess, os, re, shutil

regexGK = re.compile('(gk)\d+')
regexNegative = re.compile('(arc|style|datenblatt|AGB|Allgemeine|General)')
#newdir = "/Users/Andrea/Desktop/Valentin-Stuff/Data/CC200_flat/"
newdir = "/Users/Valentin/Documents/GIS-Daten/CC200_Deutschland/CC200"
orDir = "/Users/Valentin/Documents/GIS-Daten/CC200_Deutschland/CC200"
#
# #TODO: rename guek to gk!!!
# for root, direc, files in os.walk(orDir):
#         for file1 in files:
#             if 'guek' in file1:
#                 newName = file1.replace('guek', 'gk')
#                 os.rename(os.path.join(os.path.abspath(root),file1), os.path.join(os.path.abspath(root),newName))
#             if 'GUEK' in file1:
#                 newName = file1.replace('GUEK', 'gk')
#                 os.rename(os.path.join(os.path.abspath(root),file1), os.path.join(os.path.abspath(root),newName))
#
# # flatten directory
# for root, direc, files in os.walk(orDir):
#     # if filename is in regex then mv to CC200_flat
#     for file1 in files:
#         matchGK = regexGK.match(file1) # check if gk or guek
#         matchNegative = regexNegative.match(file1) # check if it contains illegal words
#         if (matchNegative == None) and (matchGK != None):
#             alt = os.path.join(os.path.abspath(root),file1)
#             neu = os.path.join(newdir,os.path.basename(file1))
#             #print('\n altes DIR: '+alt)
#             #print('\n neues DIR: '+ neu)
#             shutil.move(alt, neu)

# check for pairs
print "Check for pairs: \n\n"
for root, direc, files in os.walk(newdir):
        for file1 in files:
            if file1[-4:] == '.shp':
                tifPair = file1[:-4]+'.tif'

                # if (os.path.isfile(os.path.join(os.path.abspath(root),file1))):
                #     print 'is FILE:',(os.path.join(os.path.abspath(root),file1))
                if not (os.path.isfile(os.path.join(os.path.abspath(root),tifPair))):
                    print 'is MISSING FILE:',os.path.join(os.path.abspath(root),tifPair)

# walk directory and do gdal
for root, direc, files in os.walk(newdir):
        for file1 in files:
            if file1[-4:] == '.shp' and ('_merge' not in file1): #TODO check for 3857.tif
                #(os.path.isfile(os.path.join(os.path.abspath(root),(file1[-4:]+'_3857.tif')))
                # 1. create new filename with _merge
                mergeFile = file1[:-4]+'_merge.shp'
                mergePath = os.path.join(os.path.abspath(root),mergeFile)
                mergeOrigPath = os.path.join(os.path.abspath(root),file1)
                rasterOrigPath = mergeOrigPath[:-4]+'.tif'
                rasterPath = mergeOrigPath[:-4]+'_crop.tif'
                rasterPath[:-4]+'_3857.tif'
                # 2. call ogr2ogr to create merged polygon version
                callArgs = ['ogr2ogr', mergePath, mergeOrigPath, '-dialect', 'sqlite', '-sql', 'SELECT ST_Union(geometry) AS geometry FROM '+file1[:-4]]
                print callArgs
                subprocess.check_call(callArgs)

                # 3. get associated raster file
                # easily by string manipulation

                # 4. cut raster with newly created shapefile

                if not (os.path.isfile(rasterPath)):
                    call2 = ['gdalwarp', '-cutline', mergePath, '-crop_to_cutline', rasterOrigPath, rasterPath]
                    subprocess.check_call(call2)

                # 5. reproject tif:
                call3 = ['gdalwarp', '-t_srs', 'EPSG:3857', '-r', 'bilinear', rasterPath, rasterPath[:-4]+'_3857.tif']
                subprocess.check_call(call3)

                # 6 [OPTIONAL] del _merge del _uncropped tifs -> rasterOrigPath
                os.remove(mergePath) #TODO: shx xml usw. mit loeschen
                os.remove(rasterPath)

# # gdalwarp -cutline tmp_cropper.shp -crop_to_cutline -dstalpha guek6326.tif guek6326_crop.tif
