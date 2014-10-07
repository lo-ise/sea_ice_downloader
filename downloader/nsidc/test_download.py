import contextlib
import urllib
import urllib2


path = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/1981/'

'''
with contextlib.closing(urllib.urlopen(path)) as x:
	for lines in x:
		print lines
'''


data = urllib2.urlopen(path).read()
for d in data.split():
	if '19811129' in d:
		f = urllib2.urlopen(path+d).read()
		download = open('test.bin', 'wb')
		download.write(f)
		download.close()

#now what this needs is some regex.. I think!!!



