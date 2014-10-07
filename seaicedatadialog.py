# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeaIceDataDialog
                                 A QGIS plugin
 Downloads sea ice concentration data from NSIDC
                             -------------------
        begin                : 2014-10-02
        copyright            : (C) 2014 by Louise Ireland
        email                : louireland@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from downloader import downloader
from downloader.composite import Composite
from PyQt4 import QtCore, QtGui
from ui_seaicedata import Ui_SeaIceData
from qgis.utils import iface

class DownloadThread(QtCore.QThread):
    def __init__(self, path, mindate, maxdate, composite):
        self.path    = '{}/'.format(path)
        self.mindate = mindate.toPyDate()
        self.maxdate = maxdate.toPyDate()
        self.datatype = 'dailyantarctic'
	self.composite = composite
	QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def log(self, text):
        self.emit( QtCore.SIGNAL('update(QString)'), text )
 
    def run(self):
	self.log("Downloading...")
	self.log("Date range {0} to {1}".format(self.mindate.strftime('%Y/%m/%d'), self.maxdate.strftime('%Y/%m/%d')))
        C = downloader.get(self.datatype)
	d = C(self.mindate, self.maxdate)
	self.tifs = d.download(self.path)
	self.log("Downloaded.".format(self.path))
	if self.composite == True:
	    self.log("Creating composite from {} files...".format(len(tifs)))
	    Comp = Composite(self.tifs)
	    Comp.composite()
	    self.log("Composite completed.")

	#self.log("Adding to canvas...")
	#self.iface.addRasterLayer('/Users/Ireland/rsr/qgis-dev/seaice/nt_20120101_f17_v01_s.tif')
	#for t in self.tifs:
	#	self.iface.addRasterLayer(t)
	#	self.log('{}'.format(t))
	#self.log("Added.")


class SeaIceDataDialog(QtGui.QDialog, Ui_SeaIceData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
	self.composite = False
	self.iface = iface
    
    def log(self, text):
        self.plainTextEdit.appendPlainText(text)


    def open(self):
	self.fileDialog = QtGui.QFileDialog(self)
	#self.fileDialog.show()
	self.txtPath.setText(self.fileDialog.getExistingDirectory())


    def update(self):
        if self.checkBoxComposite.isChecked() == True:
            self.composite = True
	else:
            self.composite = False


    def accept(self):
        mindate  = self.startDate.date()
        maxdate  = self.endDate.date()
        path     = self.txtPath.text()
	#self.iface.addRasterLayer('/Users/Ireland/rsr/qgis-dev/seaice/nt_20120101_f17_v01_s.tif')
        self.downloadThread = DownloadThread(path, mindate, maxdate, self.composite)
        self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
        self.downloadThread.start()

	#self.iface.addRasterLayer('/Users/Ireland/rsr/qgis-dev/seaice/nt_20120101_f17_v01_s.tif')


