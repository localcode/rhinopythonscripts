import Rhino
import scriptcontext


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

def deleteLayer(layer_index):
    """Deletes a layer by index. returns nothing."""
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()
    settings.LayerIndexFilter = layer_index
    objs = scriptcontext.doc.Objects.FindByFilter(settings)
    ids = []
    for obj in objs:
        obj.Attributes.Visible = True
        obj.CommitChanges()
        ids.append(obj.Id)
    for id in ids:
        scriptcontext.doc.Objects.Delete(id, True)
    scriptcontext.doc.Layers.Delete(layer_index, True)

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



