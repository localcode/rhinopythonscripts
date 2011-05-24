"""
Allows for the translation of GeoJSON data to Rhino objects

Note that the GeoJSON data format is not 3D.

The GeoJSON Format Specification can be found here:
    http://geojson.org/geojson-spec.html

The RhinoCommon SDK (where all the Rhino.Geometry objects are documented) is
here:
    http://www.rhino3d.com/5/rhinocommon/

"""

# Import standard library modules
import json

# Import Rhino modules
import Rhino
from Rhino.Geometry import *
from scriptcontext import doc
import rhinoscriptsyntax as rs

# Import third party modules

# Import local modules



geoJsonGeometryMap = {
        'Point':(PointToRhinoPoint, addPoint)
        'MultiPoint':(MultiPointToRhinoPoint, addPoints)
        'LineString':(LineStringToRhinoCurve, addCurve)
        'MultiLineString':(MultiLineStringToRhinoCurve, addCurves)
        'Polygon':(PolygonToRhinoCurve, addPolygon)
        'MultiPolygon':(MultiPolygonToRhinoCurve, addPolygons)
        'GeometryCollection':(GeometryCollectionToParser)
        }

def addRhinoLayer(layerName, layerColor=System.Drawing.Color.Black):
    """Creates a Layer in Rhino using a name and optional color. Returns the
    index of the layer requested. If the layer
    already exists, the color is updated and no new layer is created."""
    docLyrs = doc.Layers
    layerIndex = docLyrs.Find(layerName, True)
    if layerIndex == -1:
        layerIndex = docLyrs.Add(layerName,layerColor)
    else: # it exists
        layer = docLyrs[layerIndex] # so get it
        if layer.Color != layerColor: # if it has a different color
            layer.Color = layerColor # reset the color
    return layerIndex

def PointToRhinoPoint(coordinates):
    x, y = coordinates[0], coordinates[1]
    z = 0.0
    return Point3d(x, y, z)

def MultiPointToRhinoPoint(coordinates):
    rhPointList = []
    for pair in coordinates:
        rhPointList.append(PointToRhinoPoint(pair))
    return rhPointList

def LineStringToRhinoCurve(coordinates):
    rhPoints = MultiPointToRhinoPoint(coordinates)
    return Curve.CreateControlPointCurve(rhPoints, 1)

def MultiLineStringToRhinoCurve(coordinates):
    rhCurveList = []
    for lineString in coordinates:
        rhCurveList.append(LineStringToRhinoCurve(lineString))
    return rhCurveList

def PolygonToRhinoCurve(coordinates):
    # each ring is a separate list of coordinates
    ringList = []
    for ring in coordinates:
        ringList.append(LineStringToRhinoCurve(ring))
    return ringList

def MultiPolygonToRhinoCurve(coordinates):
    polygonList = []
    for polygon in coordinates:
        polygonList.append(PolygonToRhinoCurve(polygon))
    return polygonList

def GeometryCollectionToParser(geometries):
    pass # I need to figure this one out still

def addPoint(rhPoint):
    pass

def addPoints(rhPoints):
    pass

def addCurve(rhCurve):
    pass

def addCurves(rhCurves):
    pass

def addPolygon(ringList):
    pass

def addPolygons(polygonList):
    pass


def load(rawGeoJsonData,
         destinationLayer=None,
         destinationLayerColor=System.Drawing.Color.Black):
    geoJson = json.loads(rawGeoJsonData)
    jsonFeatures = geoJson['features']
    rhFeatures = []
    for jsonFeature in jsonFeatures:

        # set up object attributes
        att = Rhino.DocObjects.ObjectAttributes()
        # setup layer if requested
        if destinationLayer != None:
            att.LayerIndex = addRhinoLayer(destinationLayer,
                                           destinationLayerColor)
        # deal with the geometry
        geom = jsonFeature['geometry']
        geomType = geom['type'] # this will return a mappable string
        coordinates = geom['coordinates']
        # translate the coordinates to Rhino.Geometry objects
        rhFeature = geoJsonGeometryMap[geomType][0](coordinates)

        # deal with the properties
        if jsonFeature['properties']:
            properties = jsonFeature['properties']
            for key in properties:
                att.SetUserString(key, str(properties[key]))

        doc.Objects.











