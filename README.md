Sea Ice Concentration Downloader V1.0.0
=======================================

##What it does
QGIS Plugin which allows easy donwload of sea ice concentration data from NSIDC (National Snow and Ice Data Centre), within a time range and with an option to create an averaged composite of all the data within the time range. The data is saved in GeoTiff format, to Antarctic Polar Stereographic projection (EPSG: 3031). 

The Plugin is currently working, but has not been subject to wide use. Therefore there may be problems with it. 


##The data
The data is sourced from (NSIDC)[website] (put details here). For full details on the input data, please refer to the (official documentation.)[website] 

The plugin sources the daily grids of sea ice concenration. Valid date range is from 1979 to 2013.

##Using the plugin
Add the following plugin repository to QGIS Desktop.

PUT PLUGIN REPO HERE

Search for the plugin, named, SeaIceData

Install it. 

It should appear as an icon on the toolbar. 


##Dev notes
This currently works and produces a composite also. 


###To do
1. Write up information on the data itself
2. the actual downloading is a bit clunky. Would be better to use ftplib, but I couldnt get this to work.
3. Option to display the grids in the iface. I don't understand why this isn't working at the moment. 
4. Add the northern dataset. 

