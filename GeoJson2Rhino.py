"""
Allows for the translation of GeoJSON data to Rhino objects

The GeoJSON Format supports 3D.

The GeoJSON Format Specification can be found here:
    http://geojson.org/geojson-spec.html

The RhinoCommon SDK (where all the Rhino.Geometry objects are documented) is
here:
    http://www.rhino3d.com/5/rhinocommon/

I have decided to extend the GeoJSON specification by adding support for one
more type of geometry that would be really useful in Rhino (and elsewhere),
the Mesh. Here is an example of a json Mesh:

    {"type": "Feature",
     "geometry": {
                  "type": "Mesh",
                  "coordinates": [
                                  [3.43, 54.234, 2343.23],
                                  [...],
                                  [...],
                                  ...,
                                  ]
                  "faces": [
                            [0,3,2],
                            [5,32,1],
                            ...,
                            ]
                  }
      "properties": {"prop0": "value0"}
      }


Example of Use:
    >>> import GeoJson2Rhino as geoj
    >>> myGeoJson = '''
{ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
      "properties": {"prop0": "value0"}
      },
    { "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
          ]
        },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
        }
      },
    { "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
           [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
             [100.0, 1.0], [100.0, 0.0] ]
           ]
       },
       "properties": {
         "prop0": "value0",
         "prop1": {"this": "that"}
         }
       }
     ]
   }'''
   >>> guidList = geoj.load(myGeoJson) #stores guids of new rhino objects

"""

# Import standard library modules
import json

# Import Rhino modules
import Rhino
from Rhino.Geometry import *
from scriptcontext import doc

# import .NET libraries
import System


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
    if len(coordinates) > 2:
        z = coordinates[2]
    else:
        z = 0.0
    x, y = coordinates[0], coordinates[1]
    return Point3d(x, y, z)

def MultiPointToRhinoPoint(coordinates):
    rhPointList = []
    for pair in coordinates:
        rhPointList.append(PointToRhinoPoint(pair))
    return rhPointList

def MeshToRhinoMesh(coordinates, faces):
    rhMesh = Mesh()
    for point in coordinates:
        rhPoint = PointToRhinoPoint(point)
        rhMesh.Vertices.Add(rhPoint)
    for face in faces:
        rhMesh.Faces.AddFace(face)
    rhMesh.Normals.ComputeNormals()
    rhMesh.Compact()
    return rhMesh

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

def addPoint(rhPoint, objAtt):
    return doc.Objects.AddPoint(rhPoint, objAtt)

def addPoints(rhPoints, objAtt):
    return doc.Objects.AddPoints(rhPoints, objAtt)

def addCurve(rhCurve, objAtt):
    return doc.Objects.AddCurve(rhCurve, objAtt)

def addCurves(rhCurves, objAtt):
    guidList = []
    for curve in rhCurves:
        guidList.append(addCurve(curve, objAtt))
    return guidList

def addPolygon(ringList, objAtt):
    # for now this just makes curves
    # but maybe it should make TrimmedSrfs
    # or should group the rings
    return addCurves(ringList, objAtt)

def addPolygons(polygonList, objAtt):
    guidList = []
    for polygon in polygonList:
        # !! Extending the guid list !!!
        guidList.extend(addPolygon(polygon, objAtt))
    return guidList

def addMesh(rhMesh, objAtt):
    return doc.Objects.AddMesh(rhMesh, objAtt)

geoJsonGeometryMap = {
        'Point':(PointToRhinoPoint, addPoint),
        'MultiPoint':(MultiPointToRhinoPoint, addPoints),
        'LineString':(LineStringToRhinoCurve, addCurve),
        'MultiLineString':(MultiLineStringToRhinoCurve, addCurves),
        'Polygon':(PolygonToRhinoCurve, addPolygon),
        'MultiPolygon':(MultiPolygonToRhinoCurve, addPolygons),
        'Mesh':(MeshToRhinoMesh, addMesh),
        'GeometryCollection':(GeometryCollectionToParser),
        }


def processGeoJson(parsedGeoJson,
         destinationLayer=None,
         destinationLayerColor=System.Drawing.Color.Black):
    # get the features
    jsonFeatures = parsedGeoJson['features']
    guidResults = []
    for jsonFeature in jsonFeatures: # for each feature
        # set up object attributes
        att = Rhino.DocObjects.ObjectAttributes()
        # setup layer if requested
        if destinationLayer != None:
            att.LayerIndex = addRhinoLayer(destinationLayer,
                                           destinationLayerColor)
        # deal with the properties
        if jsonFeature['properties']:
            properties = jsonFeature['properties']
            for key in properties:
                att.SetUserString(key, str(properties[key]))
        # deal with the geometry
        geom = jsonFeature['geometry']
        geomType = geom['type'] # this will return a mappable string
        coordinates = geom['coordinates']
        # if this is a mesh, pass the faces
        if geomType == 'Mesh':
            faces = geom['faces']
            rhFeature = geoJsonGeometryMap[geomType][0](coordinates, faces)
        # translate the coordinates to Rhino.Geometry objects
        rhFeature = geoJsonGeometryMap[geomType][0](coordinates)
        # return the GUID(s) for the feature
        guidResults.append(geoJsonGeometryMap[geomType][1](rhFeature, att))
    # return all the guids
    return guidResults

def load(rawGeoJsonData,
         destinationLayer=None,
         destinationLayerColor=System.Drawing.Color.Black):
    # if the data already appears to be a dict literal ...
    if type(rawJsonData) == dict:
        jsonData = rawJsonData
    else: # otherwise, just try to load it
        jsonData = json.loads(rawJsonData)
    # if this is just a GeoJSON ...
    if jsonData["type"] == "FeatureCollection":
        # process the GeoJSON, pass the layer and color in
        return processGeoJson(jsonData, destinationLayer,
                              destinationLayerColor)
    # or if this is a set of layers from PostSites ...
    elif jsonData["type"] == "LayerCollection":
        # make a list for all the guids
        allResults = []
        layersList = jsonData['layers']
        for layer in layersList: # for each layer
            name = layer['name'] # get the name
            if layer['color']: # get the color if it exists
                color = layer['color']
            else:
                color = destinationLayerColor # or just make it black
            geoJson = layer['contents'] # get the GeoJSON for this layer
            # make it
            layerResults = processGeoJson( geoJson, name, color )
            allResults.append(layerResults)
        return allResults
    else:
        return "This doesn't look like correctly formatted GeoJSON data.\nI'm not sure what to do with it, sorry."

