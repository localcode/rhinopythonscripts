import System

import Rhino
import scriptcontext

import Smart



def addRhinoLayer(layerName, layerColor=System.Drawing.Color.Black):
    """Creates a Layer in Rhino using a name and optional color. Returns the
    index of the layer requested. If the layer
    already exists, the color is updated and no new layer is created."""
    scriptcontext.docLyrs = scriptcontext.doc.Layers
    layerIndex = scriptcontext.docLyrs.Find(layerName, True)
    if layerIndex == -1:
        layerIndex = scriptcontext.docLyrs.Add(layerName,layerColor)
    else: # it exists
        layer = scriptcontext.docLyrs[layerIndex] # so get it
        if layer.Color != layerColor: # if it has a different color
            layer.Color = layerColor # reset the color
    return layerIndex

def layerAttributes(layerName, layerColor=System.Drawing.Color.Black):
    """Returns a Rhino ObjectAttributes object for a rhino layer with an optional color."""
    att = Rhino.DocObjects.ObjectAttributes()
    att.LayerIndex = addRhinoLayer(layerName, layerColor)
    return att

def deleteLayer(layerName, quiet=True):
    """Deletes a layer by Name. returns nothing."""
    layer_index = scriptcontext.doc.Layers.Find(layerName, True)
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()
    settings.LayerIndexFilter = layer_index
    objs = scriptcontext.doc.Objects.FindByFilter(settings)
    ids = [obj.Id for obj in objs]
    scriptcontext.doc.Objects.Delete(ids, quiet)
    scriptcontext.doc.Layers.Delete(layer_index, quiet)

def switchLayers(fromLayer, toLayer):
    """gets the objects on fromLayer and moves them to toLayer."""
    objs = scriptcontext.doc.Objects.FindByLayer(fromLayer)
    lIndex = scriptcontext.doc.Layers.Find(toLayer, True)
    for obj in objs:
        obj.Attributes.LayerIndex = lIndex
        obj.CommitChanges()

def restoreLayers():
    """Ensures that all layers are visible."""
    for i in range(scriptcontext.doc.Layers.ActiveCount):
        scriptcontext.doc.Layers.SetCurrentLayerIndex(i, True)
        name = scriptcontext.doc.Layers.CurrentLayer.Name
        rs.LayerVisible(name, True)
    scriptcontext.doc.Layers.SetCurrentLayerIndex(0, True)

def getLayerGeometry(layerName):
    '''uses doc.Objects.FindByLayer and returns the Geometry of the
    resulting RhinoObjects. If nothing found, returns an empty list.'''
    out = []
    objs = scriptcontext.doc.Objects.FindByLayer(layerName)
    if objs:
        for obj in objs:
            out.append(obj.Geometry)
    return out

def layerNames():
    '''Returns a list of strings, the name of each layer in the current
    document.'''
    names = []
    for l in scriptcontext.doc.Layers:
        names.append(l.Name)
    return names

def getLayerGuids(layerName):
    '''uses doc.Objects.FindByLayer and returns the Geometry of the
    resulting RhinoObjects. If nothing found, returns an empty list.'''
    out = []
    objs = scriptcontext.doc.Objects.FindByLayer(layerName)
    if objs:
        for obj in scriptcontext.doc.Objects.FindByLayer(layerName):
            out.append(obj.Id)
    return out

def getLayerSmartFeatures(layerName):
    out = []
    objs = scriptcontext.doc.Objects.FindByLayer(layerName)
    if objs and len(objs) > 0:
        out = Smart.RhinoObjectsToSmartFeatures(objs)
    return out


