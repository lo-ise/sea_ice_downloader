# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeaIceData
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load SeaIceData class from file SeaIceData
    from seaicedata import SeaIceData
    return SeaIceData(iface)
