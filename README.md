## Proven Steps to create MBTiles from a large set of georeferenced tifs

### 0 Open Image in QGIS and save a rendered version
The images are originally saved in UInt16, but values only range from 0-255. As a simplified approach we just use the automatic rendering from QGIS and export the images as UInt8

First, import all images into QGIS, then copy the script into the Python Console of QGIS or run it from terminal
```
python QGIS_prerender.py
```
### 1 Crop Image with provided shape file

Unite all polygons into one to make masking more efficient (also done by createCC.py).
```
ogr2ogr outfile.shp inputfile.shp -dialect sqlite -sql 'SELECT ST_Union(geometry) AS geometry FROM shapefile_name'
```
Crop all raster images by their shapefile counterpart (also done by createCC.py)
```
gdalwarp -cutline outfile.shp -crop_to_cutline raster_to_crop.tif cropped_raster.tif
```
### 2 Reproject images to EPSG:3857
```
gdalwarp -s_srs EPSG:31467 -t_srs EPSG:3857 -r average input.tif image_warped.tif
```
### 3 Change internal Tiling schema & compress images
```
gdal_translate -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "COMPRESS=JPEG" input.tif output.tif
```
or as a QGIS python script:

### 4 Merge into big tif (can be done with QGIS as well)
```
gdal_merge.py -co COMPRESS=JPEG -co JPEG_QUALITY=75 -of GTiff -o outfile.tif input1.tif input2.tif ...
```
### 5 Create overviews to display them in Tilemill at higher zoomlevels
Leveloption 16 is equal to Mapbox-Zoomlevel 8; leveloption 32 is equal to MB-zoomlevel 7; Probably goes down by x^2 per Mapbox-Zoomlevel
```
gdaladdo -r average image_final.tif 2 4 8 16 (32)
```
### 6 Import merged image into Tilemill and export to .mbtiles

Can also be done programmatically via node-js API (see Docs for more Info).












## ALTERNATIVES (WHICH WHERE CRAP!)
#### (just as a reminder)
[5-1] Tile Images with gdal2tiles

gdal_vrtmerge.py -o merged.vrt imaged_tiled.tif image2_tiled.tif

gdal2tiles.py -p mercator -r average -s EPSG:3857 -z 7-14 -v merged.vrt output_dir

[5-2] Store Tiled Images with mbutil into mbtiles

'/Users/Valentin/Documents/GIS-Daten/processing_pipeline (modules)/mbutil/mb-util' --scheme=xyz --image_format=png output_dir output.mbtiles

#### Improvements
- alternative tiling method
- compress images after tiling
- try gdal2xyz
