## Proven Steps to create MBTiles from a large set of georeferenced tifs

## Mapbox Production Pipeline
### 1.0 Batch Project all downloaded raster images into EPSG:3857
The images need to be in 8bit depth, and have a no data value of 255. Furthermore, the processing is done by **4 Cores**
```
ls -1 *.jpg | tr '\n' '\0' | tr -d ".jpg" | xargs -0 -n 1 -P 4 -I {} gdalwarp -s_srs EPSG:31468 -t_srs EPSG:3857 -r average g{}.jpg g{}_3857.tif
```
### 1.1 Build a VRT for each Row GK56**.tif, GK57**.tif etc.
```
gdalbuildvrt -srcnodata "255 255 255" gk56XX_3857.vrt gk56*_3857.tif; gdalbui...; etc...
```
### 1.2 Write the VRT as GTiff with Compression, Tiling and Blocksize Optimization required by Mapbox
```
gdal_translate -of GTIff -co "TILED=YES" -co "COMPRESS=JPEG" -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 gk73XX_3857.vrt gk73XX_3857.tif&
gdal_translate -of GTIff -co "TILED=YES" -co "COMPRESS=JPEG" -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 gk74XX_3857.vrt gk74XX_3857.tif& etc ...
```
### 1.3 Upload all files to Mapbox Servers
```
TODO
```




### 2.0 Open Image in QGIS and save a rendered version
The images are originally saved in UInt16, but values only range from 0-255. As a simplified approach we just use the automatic rendering from QGIS and export the images as UInt8

First, import all images into QGIS, then copy the script into the Python Console of QGIS or run it from terminal
```
python QGIS_prerender.py
```
### 2.1 Crop Image with provided shape file

Unite all polygons into one to make masking more efficient (also done by createCC.py).
```
ogr2ogr outfile.shp inputfile.shp -dialect sqlite -sql 'SELECT ST_Union(geometry) AS geometry FROM shapefile_name'
```
Crop all raster images by their shapefile counterpart (also done by createCC.py)
```
gdalwarp -cutline outfile.shp -crop_to_cutline raster_to_crop.tif cropped_raster.tif
```
### 2.2 Reproject images to EPSG:3857
```
gdalwarp -s_srs EPSG:31467 -t_srs EPSG:3857 -r average input.tif image_warped.tif
```
### 2.3 Change internal Tiling schema & compress images
```
gdal_translate -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "COMPRESS=JPEG" input.tif output.tif
```
or as a QGIS python script:
```
python QGIS_prerender.py
```

### 2.4 Merge into big tif (can be done with QGIS as well)
```
gdal_merge.py -co COMPRESS=JPEG -co JPEG_QUALITY=75 -of GTiff -o outfile.tif input1.tif input2.tif ...
```
### 2.5 Create overviews to display them in Tilemill at higher zoomlevels
Leveloption 16 is equal to Mapbox-Zoomlevel 8; leveloption 32 is equal to MB-zoomlevel 7; Probably goes down by x^2 per Mapbox-Zoomlevel
```
gdaladdo -r average image_final.tif 2 4 8 16 (32)
```
### 2.6 Import merged image into Tilemill and export to .mbtiles

Can also be done programmatically via node-js API (see Docs for more Info).












## ALTERNATIVES (WHICH WHERE HARD TO MANAGE, INEFFICIENT AND WHERE RESULTING IN VERY LARGE FILES!)
#### (just as a reminder)
[5-1] Tile Images with gdal2tiles
```
gdal_vrtmerge.py -o merged.vrt imaged_tiled.tif image2_tiled.tif

gdal2tiles.py -p mercator -r average -s EPSG:3857 -z 7-14 -v merged.vrt output_dir
```
[5-2] Store Tiled Images with mbutil into mbtiles
```
'/Users/Valentin/Documents/GIS-Daten/processing_pipeline (modules)/mbutil/mb-util' --scheme=xyz --image_format=png output_dir output.mbtiles
```
#### Improvements
- alternative tiling method
- compress images after tiling
- try gdal2xyz
