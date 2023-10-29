#!/usr/bin/env python
from osgeo import gdal, ogr
from pprint import pprint
import csv
import argparse
import os
import re

class ChelsaReader:
    dataset_file = ""
    dataset = ""
    geotransform = None
    raster_band = 1

    def __init__(self, dataset_file,raster_band=1):
        self.dataset_file = dataset_file
        self.raster_band = raster_band
        self.rastercount = 1
        self.open_dataset()
        self.get_geotransform()

    def get_file(self):
        return self.dataset_file

    def open_dataset(self):
        self.dataset =gdal.Open(self.dataset_file)
        self.rastercount = self.dataset.RasterCount
        if self.dataset is None:
            print("Failed to open the GeoTIFF file.")
            return None

    def get_geotransform(self):
        self.geotransform = self.dataset.GetGeoTransform()
        if self.geotransform is None:
            print("Failed to retrieve the geotransformation information.")
            self.dataset = None
            return None
    
    def read_value_at(self, latitude, longitude):
        # Convert latitude and longitude to pixel coordinates
        x = int((longitude - self.geotransform[0]) / self.geotransform[1])
        y = int((latitude - self.geotransform[3]) / self.geotransform[5])
        
        return self.dataset.GetRasterBand(self.raster_band).ReadAsArray(x, y, 1, 1)[0, 0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process GeoTIFF file')
    parser.add_argument('-f','--geotiff_file', type=str, required=False,
                         help='GeoTIFF file location')
    
    parser.add_argument('-d','--geotiff_dir', type=str, required=False,
                         help='Directory with bunch of GeoTIFF files inside')
    
    parser.add_argument('-p','--points_file', type=str, required=True,
                         help='File with points columns (longitude,latitude)')
    
    parser.add_argument('-b','--raster_band', type=int, required=False, default=1,
                         help='Raster band in tiff file you would like to read data from')

    parser.add_argument('-a','--all_bands', required=False, default=False,
                         action='store_true', help='Read values from all raster bands')


    parser.add_argument('--csv_output',default="output.csv", help='')

    args = parser.parse_args()

    

    with open(args.points_file, newline='') as points_file, open(args.csv_output, mode='w') as csv_output:
        
        fieldnames = ['id', 'cellcode','x_3035', 'y_3035', 'longitude','latitude']
        files = []
        cr = {}
        if args.geotiff_file != None:
            if args.all_bands == True:
                cr[args.geotiff_file] = ChelsaReader(args.geotiff_file,args.raster_band)
                for band in range(1,cr[args.geotiff_file].rastercount + 1):
                    cr['-'.join([args.geotiff_file,f'band{band}'.format(band)]) ] = ChelsaReader(args.geotiff_file,band)
                    files.append('-'.join([args.geotiff_file,f'band{band}'.format(band)]))
                    fieldnames.append(os.path.basename('-'.join([args.geotiff_file,f'band{band}'.format(band)])))
            else:
                files.append(args.geotiff_file)
                cr[args.geotiff_file] = ChelsaReader(args.geotiff_file,args.raster_band)
                fieldnames.append(os.path.basename(args.geotiff_file))
        elif args.geotiff_dir != None and len(os.listdir(args.geotiff_dir)) > 0 :
            for filename in os.listdir(args.geotiff_dir):
                if re.search('(.*).tif$', filename):
                    cr[filename] = ChelsaReader(filename,args.raster_band)
                    for band in range(1,cr[filename].rastercount + 1):
                        cr['-'.join([filename,f'band{band}'.format(band)]) ] = ChelsaReader(filename,band)
                        files.append('-'.join([filename,f'band{band}'.format(band)]))
                        fieldnames.append(os.path.basename('-'.join([filename,f'band{band}'.format(band)])))
        else:
            print ('no can do')

        csv_reader = csv.DictReader(points_file, delimiter=',', quotechar='"')
        csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames,dialect=csv.unix_dialect)
        csv_writer.writeheader()
            
        for row in csv_reader:
            for file in files:
                row[os.path.basename(file)] = round(cr[file].read_value_at(float(row['latitude']), float(row['longitude'])),5)
            csv_writer.writerow(row)

        
            