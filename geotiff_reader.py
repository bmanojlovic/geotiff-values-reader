#!/usr/bin/python3
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

    def __init__(self, dataset_file):
        self.dataset_file = dataset_file
        self.open_dataset()
        self.get_geotransform()

    def get_file(self):
        return self.dataset_file

    def open_dataset(self):
        self.dataset =gdal.Open(self.dataset_file)
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
        
        return self.dataset.GetRasterBand(1).ReadAsArray(x, y, 1, 1)[0, 0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process GeoTIFF file')
    parser.add_argument('-f','--geotiff_file', type=str, required=False,
                         help='GeoTIFF file location')
    
    parser.add_argument('-d','--geotiff_dir', type=str, required=False,
                         help='Directory with bunch of GeoTIFF files inside')
    
    parser.add_argument('-p','--points_file', type=str, required=True,
                         help='File with points columns (longitude,latitude)')
    
    parser.add_argument('--csv_output',default="output.csv", help='')

    args = parser.parse_args()

    

    with open(args.points_file, newline='') as points_file, open(args.csv_output, mode='w') as csv_output:
        
        fieldnames = ['id', 'cellcode','x_3035', 'y_3035', 'longitude','latitude']
        files = []
        if args.geotiff_file != None:
            files.append(args.geotiff_file)
            fieldnames.append(os.path.basename(args.geotiff_file))
        elif args.geotiff_dir != None and len(os.listdir(args.geotiff_dir)) > 0 :
            for filename in os.listdir(args.geotiff_dir):
                if re.search('(.*).tif$', filename):
                    fieldnames.append(filename)
                    files.append(os.path.join(args.geotiff_dir,filename))
        else:
            print ('no can do')

        csv_reader = csv.DictReader(points_file, delimiter=',', quotechar='"')
        csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        csv_writer.writeheader()
        cr = {}
        for filename in files:
            cr[filename] = ChelsaReader(filename)
            
        for row in csv_reader:
            for file in files:
                row[os.path.basename(file)] = round(cr[file].read_value_at(float(row['latitude']), float(row['longitude']))/10 - 273.4,5)
            csv_writer.writerow(row)

        
            