Sea Ice Concentration Downloader V1.0.0
=======================================

##What it does
This is a QGIS Plugin which allows easy download of sea ice concentration data from [NSIDC](http://nsidc.org/data/seaice_index/) (National Snow and Ice Data Centre). 

It downloads daily sea ice concentration grids within a defined time range and gives the option of output of an averaged composite. The data is saved in GeoTiff format, and projected to Antarctic Polar Stereographic (EPSG: 3031). 

The Plugin is currently working, but has not been subject to wide use. Therefore, there may be problems with it. 


##The data
The data is sourced from [NSIDC](http://nsidc.org/data/nsidc-0051). For full details on the input data, please refer to the [official documentation.](http://nsidc.org/data/docs/daac/nsidc0051_gsfc_seaice.gd.html) 

Valid date range is from 1978/10/26 to 2013/12/31.

##Using the plugin

Add the following repository:

    http://plugins.remotesensing.io/plugins.xml?qgis=2.4

Install the plugin, name Sea Ice Concentration Downloader.
