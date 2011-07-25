import os
import sys

import System
import System.Collections.Generic as SCG

import Rhino
from Rhino.FileIO import FileWriteOptions, FileReadOptions
import scriptcontext
import rhinoscriptsyntax as rs

import LayerTools


def exportFile(filePath,
        version=4,
        geomOnly=False,
        selectedOnly=False,
        ):
    '''Export a file.'''
    opt = FileWriteOptions()
    opt.FileVersion = version
    opt.WriteGeometryOnly = geomOnly
    opt.WriteSelectedObjectsOnly = selectedOnly
    return scriptcontext.doc.WriteFile(filePath, opt)

def importFiles(filePathList):
    '''Import a list of files'''
    opt = FileReadOptions()
    opt.ImportMode = True
    for f in filePathList:
        #print 'Importing %s' % f
        scriptcontext.doc.ReadFile(f, opt)

def silentImport(filePathList):
    """Takes one or more file paths and returns RhinoCommon
    File3dm objects for each file, if they exist. Returns an empty
    list if no file is found.
    """
    models = []
    if type(filePathList) == str: # assume it's one path
        filePathList = [filePathList]
    for f in filePathList:
        model = Rhino.FileIO.File3dm.Read(f)
        if not model: continue
        models.append(model)
    return models

def modelsToLayerGeometryDict(models):
    out = {}
    for m in models:
        for layer in m.Layers:
            name = layer.Name
            out[name] = []
            objs = m.Objects.FindByLayer(name)
            for obj in objs:
                geom = obj.Geometry
                geom.EnsurePrivateCopy()
                out[name].append(geom)
        m.Dispose()
    return out

def fileGeometryDict(fileNames):
    models = silentImport(fileNames)
    return modelsToLayerGeometryDict(models)

def importFile(filePath):
    '''import one file.'''
    importFiles([filePath])

def deleteAll():
    """Deletes everything in the current Rhino scriptcontext.doc. Returns nothing."""
    guidList = []
    objType = Rhino.DocObjects.ObjectType.AnyObject
    objTable = scriptcontext.doc.Objects
    objs = objTable.GetObjectList(objType)
    for obj in objs:
        guidList.append(obj.Id)
    for guid in guidList:
        objTable.Delete(guid, True)

def importLayers(filePaths, layerNames):
    '''Input a list of filePaths and a list of layerNames, in order to import all the
    files and return a list of RhinoObjects on each layer, in corresponding layers.
    Layers that do not exist or contain no objects will return empty lists.'''
    outObjs = []
    importFiles(filePaths)
    for ln in layerNames:
        objs = scriptcontext.doc.Objects.FindByLayer(ln)
        outObjs.append(objs)
    return outObjs

def importLayerGeometryDict(filePaths, layerNames=None, silent=True):
    '''Input a list of filePaths and a list of layerNames, in order to import all the
    files and return a list of RhinoObjects on each layer, in corresponding layers.
    Layers that do not exist or contain no objects will return empty lists.'''
    outObjs = []
    importFiles(filePaths)
    if not layerNames:
        layerNames = []
        # get all the layers
        lyrTable = scriptcontext.doc.Layers
        for lyr in lyrTable:
            layerNames.append(lyr.FullPath)
    for ln in layerNames:
        objs = scriptcontext.doc.Objects.FindByLayer(ln)
        if objs:
            outObjs.append([obj.Geometry for obj in objs])
        else:
            outObjs.append([])
    return dict(zip(layerNames, outObjs))

def importSmartLayerDict(filePaths, layerNames):
    '''Input a list of filePaths and a list of layerNames, in order to import all the
    files and return a list of SmartFeatures corresponding to each layer.
    Layers that do not exist or contain no objects will return empty lists.'''
    importFiles(filePaths)
    outFeatures = []
    for ln in layerNames:
        features = LayerTools.getLayerSmartFeatures(ln)
        outFeatures.append(features)
    return dict(zip(layerNames, outFeatures))

def exportLayers(layerNames, filePath, version=4):
    '''Export only the items on designated layers to a file.'''
    # save selection
    oldSelection = rs.SelectedObjects()
    # clear selection
    rs.UnselectAllObjects()
    # add everything on the layers to selection
    for name in layerNames:
        objs = scriptcontext.doc.Objects.FindByLayer(name)
        guids = [obj.Id for obj in objs]
        scriptcontext.doc.Objects.Select.Overloads[SCG.IEnumerable[System.Guid]](guids)
    # export selected items
    exportFile(filePath, version, selectedOnly=True)
    #clear selection
    rs.UnselectAllObjects()
    # restore selection
    if oldSelection:
        scriptcontext.doc.Objects.Select.Overloads[SCG.IEnumerable[System.Guid]](oldSelection)
    #print 'exported %s' % filePath

