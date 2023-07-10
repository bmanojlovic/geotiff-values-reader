# geotiff-values-reader

This python library is used to extract information from [CHELSA – Free climate data at high resolution](https://chelsa-climate.org/) provided files, but really it is not limited to just reading values from those files.

Currently it is hardcoded for temperature in Celsiuses if it is run from command line.

Library if imported will NOT change values in any ways possible.

# Installation

depending on your python environment you can use next steps to use this library (this example is for linux):
```
> python3 -m venv pygdal-env
> source pygdal-env/bin/activate
(pygdal-env)> pip install -r requirements.txt
Collecting GDAL==3.6.3 (from -r requirements.txt (line 1))
  Using cached GDAL-3.6.3-cp311-cp311-linux_x86_64.whl
Installing collected packages: GDAL
Successfully installed GDAL-3.6.3
(pygdal-env)> python3 ./geotiff_reader.py
usage: geotiff_reader.py [-h] [-f GEOTIFF_FILE] [-d GEOTIFF_DIR] -p POINTS_FILE [--csv_output CSV_OUTPUT]
geotiff_reader.py: error: the following arguments are required: -p/--points_file
(pygdal-env)>
```


## example run with default logic converting values to degrees celsius

To show how this library works, based on code in library next segment will do.

First download data files:
```
(pygdal-env)> wget https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V2/GLOBAL/monthly/tasmax/CHELSA_tasmax_09_2000_V.2.1.tif \
	https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V2/GLOBAL/monthly/tasmax/CHELSA_tasmax_11_1986_V.2.1.tif
```

After download sample files run code with single file:

```
(pygdal-env)> python3 ./geotiff_reader.py -p points.csv -f CHELSA_tasmax_11_1986_V.2.1.tif
(pygdal-env)> ls -la output.csv; wc -l points.csv output.csv
-rw-r--r-- 1 steki steki 972 Jul 10 14:27 output.csv
  13 points.csv
  13 output.csv
  26 total
(pygdal-env)>
```

### input points file
|id|cellcode|x_3035|y_3035|longitude|latitude|
|----|----|----|----|----|----|
|39071|1kmE5137N2268|5137500|2268500|20.0234472946833|43.0328166857817|
|39073|1kmE5137N2270|5137500|2270500|20.0265023343479|43.0506894324026|
|39074|1kmE5137N2271|5137500|2271500|20.028030781767|43.059625652453|
|39077|1kmE5137N2274|5137500|2274500|20.032619838506|43.0864336999936|
|39079|1kmE5137N2276|5137500|2276500|20.035682308518|43.1043052215359|
|39084|1kmE5137N2281|5137500|2281500|20.0433493497064|43.1489822419448|
|39085|1kmE5137N2282|5137500|2282500|20.0448846234866|43.157917340578|
|39087|1kmE5137N2284|5137500|2284500|20.0479570393676|43.1757872326808|
|39088|1kmE5137N2285|5137500|2285500|20.0494941821639|43.1847220262214|
|39090|1kmE5137N2287|5137500|2287500|20.0525703392096|43.2025913084591|
|39091|1kmE5137N2288|5137500|2288500|20.0541093541562|43.211525797227|
|39094|1kmE5137N2291|5137500|2291500|20.0587301488804|43.2383286545533|


### output file with values populated
|id|cellcode|x_3035|y_3035|longitude|latitude|CHELSA_tasmax_11_1986_V.2.1.tif|
|----|----|----|----|----|----|----|
|39071|1kmE5137N2268|5137500|2268500|20.0234472946833|43.0328166857817|4.9|
|39073|1kmE5137N2270|5137500|2270500|20.0265023343479|43.0506894324026|5.8|
|39074|1kmE5137N2271|5137500|2271500|20.028030781767|43.059625652453|5.7|
|39077|1kmE5137N2274|5137500|2274500|20.032619838506|43.0864336999936|6.6|
|39079|1kmE5137N2276|5137500|2276500|20.035682308518|43.1043052215359|6.5|
|39084|1kmE5137N2281|5137500|2281500|20.0433493497064|43.1489822419448|5.8|
|39085|1kmE5137N2282|5137500|2282500|20.0448846234866|43.157917340578|5.7|
|39087|1kmE5137N2284|5137500|2284500|20.0479570393676|43.1757872326808|5.7|
|39088|1kmE5137N2285|5137500|2285500|20.0494941821639|43.1847220262214|5.4|
|39090|1kmE5137N2287|5137500|2287500|20.0525703392096|43.2025913084591|6.1|
|39091|1kmE5137N2288|5137500|2288500|20.0541093541562|43.211525797227|7.0|
|39094|1kmE5137N2291|5137500|2291500|20.0587301488804|43.2383286545533|7.5|

## Example run with multiple GeoTIFF files in directory

```
(pygdal-env)> python3 ./geotiff_reader.py -p points.csv -d .
(pygdal-env)> ls -la output.csv; wc -l points.csv output.csv
-rw-r--r-- 1 steki steki 1064 Jul 10 14:23 output.csv
  13 points.csv
  13 output.csv
  26 total
(pygdal-env)>
```

### output.csv file would be populated in manner shown bellow

|id|cellcode|x_3035|y_3035|longitude|latitude|CHELSA_tasmax_11_1986_V.2.1.tif|CHELSA_tasmax_09_2000_V.2.1.tif|
|----|----|----|----|----|----|----|
|39071|1kmE5137N2268|5137500|2268500|20.0234472946833|43.0328166857817|4.9|15.0|
|39073|1kmE5137N2270|5137500|2270500|20.0265023343479|43.0506894324026|5.8|15.9|
|39074|1kmE5137N2271|5137500|2271500|20.028030781767|43.059625652453|5.7|15.8|
|39077|1kmE5137N2274|5137500|2274500|20.032619838506|43.0864336999936|6.6|16.7|
|39079|1kmE5137N2276|5137500|2276500|20.035682308518|43.1043052215359|6.5|16.6|
|39084|1kmE5137N2281|5137500|2281500|20.0433493497064|43.1489822419448|5.8|15.8|
|39085|1kmE5137N2282|5137500|2282500|20.0448846234866|43.157917340578|5.7|15.7|
|39087|1kmE5137N2284|5137500|2284500|20.0479570393676|43.1757872326808|5.7|15.6|
|39088|1kmE5137N2285|5137500|2285500|20.0494941821639|43.1847220262214|5.4|15.3|
|39090|1kmE5137N2287|5137500|2287500|20.0525703392096|43.2025913084591|6.1|16.0|
|39091|1kmE5137N2288|5137500|2288500|20.0541093541562|43.211525797227|7.0|16.9|
|39094|1kmE5137N2291|5137500|2291500|20.0587301488804|43.2383286545533|7.5|17.4|


## license
apache-2.0
