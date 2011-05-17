import Rhino
import System
from Rhino.Geometry import *
from scriptcontext import doc
import rhinoscriptsyntax as rs
import Rhino.RhinoApp as app
from InfraPy import *

import os
import sys

def addRhinoLayer(layerName, layerColor=System.Drawing.Color.Black):
    """Creates a Layer in Rhino using a name and optional color. Returns the index of the created layer. If the layer
    already exists, no new layer is created."""
    docLyrs = doc.Layers
    layerIndex = docLyrs.Find(layerName, True)
    if layerIndex == -1:
        layerIndex = docLyrs.Add(layerName,layerColor)
    return layerIndex

def layerAttributes(layerName, layerColor=System.Drawing.Color.Black):
    """Returns a Rhino ObjectAttributes object for a rhino layer with an optional color."""
    att = Rhino.DocObjects.ObjectAttributes()
    att.LayerIndex = addRhinoLayer(layerName, layerColor)
    return att

def addBBoxOutlines():
    """Adds a wireframe of the bounding box to use for zooming"""
    bAtt = layerAttributes("bBoxWires", System.Drawing.Color.BlanchedAlmond)
    bBox = doc.Objects.FindByLayer("boundingBox")[0].Geometry
    bCurves = bBox.DuplicateEdgeCurves()
    for curve in bCurves:
        doc.Objects.AddCurve(curve, bAtt)
    return True

def switchLayers(fromLayer, toLayer):
    """gets the objects on fromLayer and moves them to toLayer."""
    objs = doc.Objects.FindByLayer(fromLayer)
    lIndex = doc.Layers.Find(toLayer, True)
    for obj in objs:
        obj.Attributes.LayerIndex = lIndex
        obj.CommitChanges()


def deleteEverything():
    """Deletes everything in the current Rhino document. Returns nothing."""
    guidList = []
    objType = Rhino.DocObjects.ObjectType.AnyObject
    objTable = doc.Objects
    objs = objTable.GetObjectList(objType)
    for obj in objs:
        guidList.append(obj.Id)
    for guid in guidList:
        objTable.Delete(guid, True)

def viewportSetup(lensLength=900.0, size=800):
    app.RunScript("4View -NewFloatingViewport Projection=Perspective", False)
    cameraLine = doc.Objects.FindByLayer("viewLine")[0].Geometry
    targetPoint = cameraLine.PointAtEnd
    cameraPoint = cameraLine.PointAtStart
    view = doc.Views.ActiveView.ActiveViewport
    view.SetCameraLocations(targetPoint, cameraPoint)
    view.Camera35mmLensLength = lensLength
    app.RunScript("-ViewportProperties Size "+str(size)+" "+str(size)+" Enter", False)
    bBox = doc.Objects.FindByLayer("boundingBox")[0].Geometry.GetBoundingBox(True)
    view.ZoomBoundingBox(bBox)
    
def viewportRectangle():
    m = doc.Views.ActiveView.ActiveViewport.GetNearRect()
    rect = Rhino.Geometry.Curve.CreateControlPointCurve(m, 1)
    att = layerAttributes("viewportRectangle", System.Drawing.Color.Cyan )
    att.Mode = Rhino.DocObjects.ObjectMode.Normal
    id = doc.Objects.AddCurve(rect, att)
    doc.Objects.Find(id).CommitChanges()

def viewportFramework():
    view = doc.Views.ActiveView.ActiveViewport
    near = view.GetNearRect()
    far = view.GetFarRect()
    att = layerAttributes("viewportFramework", System.Drawing.Color.Cyan )
    pairs = crossMatch(near, far)
    for pair in pairs:
        cv = Rhino.Geometry.Curve.CreateControlPointCurve(pair, 1)
        id = doc.Objects.AddCurve( cv, att )
        doc.Objects.Find(id).CommitChanges()

        

def crossMatch(list1, list2):
    outList = []
    for i in list1:
        for j in list2:
            pair = ( i, j )
            outList.append(pair)
    return outList


def configureLayers(layerConfigTable):
    for layerSettings in layerConfigTable:
        rs.LayerVisible(layerSettings[0], layerSettings[1])
        if layerSettings[2] != None:
            rs.LayerColor(layerSettings[0], layerSettings[2])

def restoreLayers():
    for i in range(doc.Layers.ActiveCount):
        doc.Layers.SetCurrentLayerIndex(i, True)
        name = doc.Layers.CurrentLayer.Name
        rs.LayerVisible(name, True)
    doc.Layers.SetCurrentLayerIndex(0, True)

def deleteLayer(layer_index):
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()
    settings.LayerIndexFilter = layer_index
    objs = doc.Objects.FindByFilter(settings)
    ids = []
    for obj in objs:
        obj.Attributes.Visible = True
        obj.CommitChanges()
        ids.append(obj.Id)
    for id in ids:
        doc.Objects.Delete(id, True)
    doc.Layers.Delete(layer_index, True)
    
def fixCurves():
    app.RunScript("-SelNone", False)
    for i in range(doc.Layers.ActiveCount):
        if doc.Layers[i].IsVisible == True:
            doc.Layers.SetCurrentLayerIndex(i, True)
            name = doc.Layers.CurrentLayer.Name
            objs = doc.Objects.FindByLayer(name)
            for obj in objs:
                obj.Select(True)
            app.RunScript("-Join Enter", False)
            app.RunScript("-SelNone", False)
            
    

def zoomToLayer(layerName):
    """
    selects the first item in the named layer and zooms to that object
    """
    objs = doc.Objects.FindByLayer(layerName)
    ptList = []
    for obj in objs:
        ptList.append(obj.Geometry.PointAtStart)
        ptList.append(obj.Geometry.PointAtEnd)
    bbx = Rhino.Geometry.BoundingBox(ptList)
    doc.Views.ActiveView.ActiveViewport.ZoomBoundingBox(bbx)
    

if __name__=="__main__":
    
    layerConfigurationTable = [
            ("boundingBox", False, None),
            ("viewLine", False, None),
            ("BuildingVolumes", False, None)
            ]
    make2DLayerTable = [
            ("TerrainWireframe - Hidden", False, None),
            ("BuildingWireframes - Hidden", False, None),
            ("BuildingVolumes", False, None),
            ("LabelLines - Hidden", True, None)
            ]
    
    files = listFiles("C:\\LocalCodeFullBatch\\AxoPrep", True, ".3dm")
    files = files[680:]
    n = editFilePrefix("C:\\LocalCodeFullBatch\\AxoPrep\\AxoPrep","C:\\LocalCodeFullBatch\\AiAxo\\AiAxo",files)
    exports = editFileExt(".3dm", ".ai", n)
    opt = Rhino.FileIO.FileReadOptions()
    opt.ImportMode=True
    
    for i in range(len(files)): # slice the files list here to limit the size of the batch (files[:10])
        file = files[i]
        export = exports[i]
        
        # restoreLayers()
        restoreLayers()
        app.RunScript("Show ", False)
        
        # clear the current file
        deleteEverything()
        app.RunScript("-CloseViewport ", False)
        
        # import the new file
        doc.ReadFile(file, opt)
        
        # set up the viewport
        viewportSetup(275, 800)
        
        viewportFramework()
        
        addBBoxOutlines()
        
        
        # set up the layers
        configureLayers(layerConfigurationTable)
        
        ## Do a make 2D
        app.RunScript("SelAll -Make2D DrawingLayout=CurrentView "
                +"ShowTangentEdges=Yes "
                +"CreateHiddenLines=Yes "
                +"MaintainSourceLayers=Yes Enter "
                +"-Invert Hide SetView World Top ZE SelNone",
                False)
        
        switchLayers("viewportFramework - Hidden", "viewportFramework - Visible")
        
        zoomToLayer("viewportFramework - Visible")
        
        
        app.RunScript("SelAll -Export "+export
                +" PreserveUnits=No "
                +"ViewportBoundary=Yes Enter", False)
        
        

