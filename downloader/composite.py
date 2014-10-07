from osgeo import gdal
import numpy as np
import os
from datetime import datetime

class Composite:

	def __init__(self, filelist, calculation='mean'):
		
		self.filelist = filelist
		self.outputname = '{0}/{1}_composite_seaice.tif'.format(os.path.dirname(self.filelist[0]), calculation) 


		g = gdal.Open(self.filelist[0])	
		self.proj   = g.GetProjection()
		self.outgeo = g.GetGeoTransform()
		
		self.nodata = g.GetRasterBand(1).GetNoDataValue()
		self.calculation = calculation

		arr = g.ReadAsArray()
		[self.cols, self.rows] = arr.shape


	def composite(self):
		"""
		This one creates the composite from the other private functions
		"""
		
		arr = self.__getarray(self.filelist)
		arr = self.__averagearr(arr, self.calculation)
		tif = self.__savearr(arr, self.outputname)


	def __getarray(self, filelist):
		"""
		Puts together a 3d array from the list of input files
		Could put in a catch here if the array is too big?
		"""

		g = gdal.Open(filelist[0])
		x = g.ReadAsArray()

		[cols,rows] = x.shape

		new_arr = np.empty((len(filelist),cols,rows), dtype=np.uint8)
		[dims,cols,rows] = new_arr.shape


		for f in filelist:
			i = filelist.index(f)
			g = gdal.Open(f)
			arr = g.ReadAsArray()
			new_arr[i,...] = arr
			g = None
	
		return new_arr


	def __averagearr(self, arr, calculation):
		"""
		this one creates a median or a mean array
		default is mean
		"""

		med = arr[0,...]
		[dims,cols,rows] = arr.shape

		for i in range(0,cols-1):
			for j in range(0,rows-1):
				values = arr[...,i,j]
				if calculation == 'mean':
					new_val = np.mean(values)
					med[i,j] = new_val
				if calculation == 'median':
					new_val = np.median(values)
					med[i,j] = new_val
		
		return med	
 

	def __savearr(self, arr, outputname):
		"""
		Saves the output file as a geotif
		"""
		outfile = gdal.GetDriverByName("GTiff")
		dst_ds  = outfile.Create(outputname, self.rows, self.cols, 1, gdal.GDT_Byte)
		dst_ds.SetProjection(self.proj)
		dst_ds.SetGeoTransform(self.outgeo)

		dst_ds.SetMetadataItem('PRODUCT', '{} sea ice concentration'.format(self.calculation))
		dst_ds.SetMetadataItem('UNITS', 'Percentage %')
		dst_ds.SetMetadataItem('DATA_PROVIDER', 'NSIDC')
		dt  = datetime.now()
		dts = dt.strftime('%Y-%m-%d')
		dst_ds.SetMetadataItem('CREATION_DATE', dts)
		dst_ds.SetMetadataItem('RESOLUTION', '25km')
		dst_ds.SetMetadataItem('PARAMETER', 'Sea ice concentration')
		dst_ds.SetMetadataItem('ALGORITHM', 'NASA Team')

		band = dst_ds.GetRasterBand(1)
		band.WriteArray(arr)
		band.SetNoDataValue(self.nodata)



if __name__ == "__main__":
	files = ['/Users/Ireland/rsr/qgis-dev/compositeseaice/nt_19950101_f11_v01_s.tif', '/Users/Ireland/rsr/qgis-dev/compositeseaice/nt_19950102_f11_v01_s.tif']
	Comp = Composite(files)
	Comp.composite()


