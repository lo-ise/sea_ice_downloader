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
import makeqml
import os



class DownloadThread(QtCore.QThread):
    def __init__(self, path, mindate, maxdate, composite, pole):
        self.path    = os.path.join(path)
        self.mindate = mindate.toPyDate()
        self.maxdate = maxdate.toPyDate()
        self.pole = pole
	self.compcalc = 'median'
	self.composite = composite
	QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def log(self, text):
        self.emit( QtCore.SIGNAL('update(QString)'), text )
 
    def run(self):
	if self.maxdate >= self.mindate:
	    self.log("Downloading...")
       	    self.log("Date range {0} to {1}".format(self.mindate.strftime('%Y/%m/%d'), self.maxdate.strftime('%Y/%m/%d')))
            C = downloader.get(self.pole)
	    d = C(self.mindate, self.maxdate)
	    self.tifs = d.download(self.path)
	    self.log("Downloaded.".format(self.path))
	    if self.composite == True:
	        self.log("Creating composite from {} files...".format(len(self.tifs)))
	        Comp = Composite(self.tifs, self.mindate, self.maxdate, self.compcalc)
	        Comp.composite()
		self.log("Composite completed: {}".format(Comp.composite_name))
		self.tifs.append(Comp.composite_name)
	else:
	    self.log("Invalid date range")


class SeaIceDataDialog(QtGui.QDialog, Ui_SeaIceData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
	self.setupUi(self)
	self.composite = False
	self.iface = iface
   	self.canvas = False


    def log(self, text):
	"""
	Adds log info to the UI, coming from 
	DownloadThread.
	"""
        
	self.plainTextEdit.appendPlainText(text)


    def open(self):
	"""
	Opens a file dialog for user to select doanload path.
	"""
	
	self.fileDialog = QtGui.QFileDialog(self)
	self.txtPath.setText(self.fileDialog.getExistingDirectory())


    def update(self):
	"""
	Records whether user wants composite
	"""

	if self.checkBoxComposite.isChecked() == True:
            self.composite = True
	else:
            self.composite = False


    def accept(self):
	"""
	Initiates the download and processing once user 
	clicks 'Download'
	"""
       
        self.btnDownload.setEnabled(False)
        mindate  = self.startDate.date()
        maxdate  = self.endDate.date()
        path     = self.txtPath.text()
	pole     = self.datasetBox.currentText()

	if path == "":
	    self.plainTextEdit.appendPlainText("Error: Enter a download directory.")
        else:
            self.downloadThread = DownloadThread(path, mindate, maxdate, self.composite, pole)
            self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
	    self.downloadThread.start()
            self.connect(self.downloadThread, QtCore.SIGNAL('finished()'), self.addlayers)

    def addlayers(self):
	"""
	Handles adding and styling data to canvas once downloaded,
	if users wants to add it. 
	"""
        self.btnDownload.setEnabled(True)
	if self.checkBoxCanvas.isChecked() == True and hasattr(self.downloadThread, 'tifs'):
	    tifs = self.downloadThread.tifs
	    for t in tifs:
	        self.iface.addRasterLayer(t)

	    layers = self.iface.legendInterface().layers()
	    pth = os.path.dirname(tifs[0])
	    qml = makeqml.makeqml(pth)
	    for l in layers:

		l.loadNamedStyle(qml)
		self.iface.legendInterface().refreshLayerSymbology(l)

	    os.remove(qml)



