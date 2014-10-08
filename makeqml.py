qmltext = """
<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.4.0-Chugiak" minimumScale="-4.65661e-10" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <pipe>
    <rasterrenderer opacity="1" alphaBand="0" classificationMax="100" classificationMinMaxOrigin="CumulativeCutFullExtentEstimated" band="1" classificationMin="0" type="singlebandpseudocolor">
      <rasterTransparency/>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0">
          <item alpha="255" value="0" label="0.000000" color="#000000"/>
          <item alpha="255" value="25" label="25.000000" color="#bae4bc"/>
          <item alpha="255" value="50" label="50.000000" color="#7bccc4"/>
          <item alpha="255" value="75" label="75.000000" color="#43a2ca"/>
          <item alpha="255" value="100" label="100.000000" color="#0868ac"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
"""

def makeqml (pth, txt=qmltext):
	f = open('{}/style.qml'.format(pth), 'w')
	f.write(txt)
	f.close()
	return '{}/style.qml'.format(pth)

if __name__ == "__main__":
	x = makeqml('/Users/Ireland')
	print x
