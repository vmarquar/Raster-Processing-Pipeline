# If Images appear black by the standard preview.app
# load them into QGIS and export a rendered version of the image
# do this step before processing any other image information
# HOWTO: Just copy this script into the QGIS Python Terminal
# HOWTO: Choose between tile256 and export_rendered_version
import os, subprocess

def export_rendered_version(layer,output_dir):
    """
    selected_layer: can be the active layer (e.g. layer = iface.activeLayer()) or can be a loop through the whole QGIS project DOC
    output_file: is the name which should be used for the output image, Default is: imageName_rendered.tif
    """
    #layer = iface.activeLayer()
    output_file= os.path.join(output_dir,layer.name()+'_rendered.tif')
    extent = layer.extent()
    width, height = layer.width(), layer.height()
    renderer = layer.renderer()
    provider=layer.dataProvider()
    crs = layer.crs().toWkt()

    pipe = QgsRasterPipe()
    pipe.set(provider.clone())
    pipe.set(renderer.clone())

    file_writer = QgsRasterFileWriter(output_file)
    try:
        file_writer.writeRaster(pipe,width,height,extent,layer.crs())
    except Exception as e:
        pass

def tile256(layer):
    """
    create a tiled layer and compresses tif to jpeg
    """
    #output_dir
    layer_path = layer.dataProvider().dataSourceUri()
    #layer_path_out = os.path.join(output_dir, os.path.basename(layer_path)[:-4]+'_tiled.tif')
    layer_path_out = layer_path[:-4]+'_tiled.tif'
    print "input <---> output",layer_path,layer_path_out
    # args = ['gdal_translate', '-co', 'TILED=YES', '-co', 'BLOCKXSIZE=256', '-co', 'BLOCKYSIZE=256', '-co', 'COMPRESS=JPEG', '"'+layer_path+'"', '"'+layer_path_out+'"']
    # subprocess.check_call(args, shell=True)
    cmd = 'gdal_translate -co TILES=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=JPEG "'+layer_path+'" "'+layer_path_out+'"'
    os.system(cmd)

# iterate through TOC in QGIS and export a rendered version of each
layers = iface.legendInterface().layers()
for layer in layers:
    #print "Rendering ",layer.name()
    #export_rendered_version(layer,'/Users/Valentin/Desktop/')
    tile256(layer)
