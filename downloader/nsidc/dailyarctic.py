from datetime import datetime
from datetime import date
from datetime import timedelta
import urllib2
import bz2
from osgeo import gdal
from osgeo import osr
import numpy as np
import os


class DailyArctic:
	"""
	Given a date range, this downloads daily grids of sea ice concentration
	from NSIDC (http://nsidc.org/data/nsidc-0051). 

	Raw data is in .bin files. The output from processing functions here is 
	a GeoTiff.

	This was originally created for use within a QGIS Plugin, but can also 
	be used as a standalone module.

	Inputs are:
	start_date (a Python date object)
	end_date   (a Python date object)

	"""

	def __init__(self, start_date, end_date):
		
		self.start_date     = start_date
		self.end_date       = end_date
		self.nodata         = 255
		self.urlpath        = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/north/daily/'

	def download(self, path):
		"""
		Downloads the .bin files, reprojects to 3031 and 
		saves to GeoTiff.

		Input:
		path - where the data will be saved. 
	
		"""
		failed_files = []
		self.path = os.path.join(path)
		filenames = self.__createfilenames()
		filenames = self.__paths(filenames)
		print filenames
		tiffiles = [] 
		for f in filenames:
			binfile = self.__extract(f)
			tif = self.__process(binfile)
			tiffiles.append(tif)
			print tif
		return tiffiles



	def __createfilenames(self):
		"""
		Based on the date range, this creates a list of 
		string dates for the date range specified. 


		"""
	
		filenames = {} #save as (year, date)
		d = self.start_date
		while d <= self.end_date:
			ds = d.strftime('%Y%m%d')
			year = d.year
			
			if filenames.has_key(year):
				dates = filenames[year]
				dates.append(ds)
				filenames[year] = dates
				
			else:
				dates = []
				dates.append(ds)
				filenames[year] = dates
		
			d = d + timedelta(days=1)
		
		return filenames


	def __paths(self, dates_dict):
		"""
		This takes a dictionary of year[datestrings]. 
		
		There are gaps in the data timeseries, and the 
		naming convention is not consistent across all
		years. Therefore, this checks what is on the 
		ftp first. 
		
		"""
		
		filepaths = []
		for year in dates_dict:
			dates = dates_dict[year]
			url = '{0}{1}/'.format(self.urlpath, year)
			data = urllib2.urlopen(url).read()
			
			all_data_dict = {}
			for d in data.split():
				if 'nt' in d:
					all_data_dict[d[3:11]] = d	
			
			for d in dates:
				try:
					filename = all_data_dict[d]
					filepath = url + filename
					filepaths.append(filepath)
				except:
					continue

		return filepaths


	def __extract(self, targetfile):
		"""
		This takes an ftp path to a file and downloads
		the file.

		"""
		print targetfile	
		binfile = targetfile.replace(self.urlpath, '')
		print binfile
		binfile = os.path.join(self.path, binfile[5:])
		print binfile

		
		thefile = urllib2.urlopen(targetfile)
		print 'thefile', thefile
		f = open(binfile, 'wb')
		print 'f', f
		f.write(thefile.read())
		f.close()
		return binfile
		



	def __make_header(self, headerfile):
		"""
		Called only in __process(). Makes a header file
		for the associated .bin file, such that it
		becomes a recognised GDAL dataset. 

		"""

        	f = open(headerfile, 'w')
        	header_info = ['ncols 304',  
	        	        'nrows 448',
	                	'nodata_value 255',
				'xdim 25000', 
	                	'ydim 25000', 
	                	'ulxmap -3750000', 
	                	'ulymap 5850000', 
	                	'pixeltype usignedint', 
	                	'bil', 
	                	'byteorder M', 
	                	'nbits 8', 
	                	'nbands 1', 
                        	'skipbytes 0']
        	for h in header_info:
                	f.write('{}\n'.format(h))
        	f.close()
		


	def __process(self, targetfile):
		"""
		Processes the uncompressed file downloaded 
		in self.__extract()

		1. Reads the file in as an array
		2. Scales to percentage values
		3. Sets coastline/nodata values all as 255
		4. Projects dataset to epsg:3031
		5. Saves as a Geotiff to path
		6. Writes metadata
		
		"""
		print targetfile

		headerfile= targetfile.replace('.bin', '.hdr')
		self.__make_header(headerfile)
		g = gdal.Open(targetfile)
		arr = g.ReadAsArray()

		arr  = np.array(arr, dtype=np.float32)
		[cols, rows] = arr.shape

		scaled = np.empty_like(arr)
		for i in range(0, cols):
			for j in range(0, rows):
				current = arr[i,j]
				if current <= 250:
					newval = (current/250.) * 100.
					newval = round(newval)
					scaled[i,j] = newval
				else:
					scaled[i,j] = 255
		scaled[0,...] = 0

		outgeo = (-3750000, 25000, 0.0, 5850000, 0.0, -25000)

		ref = osr.SpatialReference()
		ref.ImportFromProj4('+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')
		inref = ref.ExportToWkt()
	
		outdata = gdal.GetDriverByName("GTiff")
		dst_ds = outdata.Create('{}.tif'.format(targetfile.replace('.bin', '')), rows, cols, 1, gdal.GDT_Byte)
		band = dst_ds.GetRasterBand(1)
		band.SetNoDataValue(self.nodata)
		dst_ds.SetGeoTransform(outgeo)
		dst_ds.SetProjection(inref)
		band.WriteArray(scaled)
		
		os.remove(headerfile)

		return '{}.tif'.format(targetfile.replace('.bin', ''))

if __name__ == "__main__":
	sd = datetime(1998,6,1)
	ed = datetime(1998,9,30)
	d = DailyArctic(sd,ed)
	l = d.download('/Users/Ireland/rsr/arctic_nsidc_raw/tests/')
	print l
	sd = datetime(1999,6,1)
        ed = datetime(1999,9,30)
        d = DailyArctic(sd,ed)
	l = d.download('/Users/Ireland/rsr/arctic_nsidc_raw/tests/')
	print l
	sd = datetime(2000,6,1)
        ed = datetime(2000,9,30)
        d = DailyArctic(sd,ed)
	l = d.download('/Users/Ireland/rsr/arctic_nsidc_raw/tests/')
	print l
	sd = datetime(2001,6,1)
        ed = datetime(2001,9,30)
        d = DailyArctic(sd,ed)
	l = d.download('/Users/Ireland/rsr/arctic_nsidc_raw/tests/')
	print l

