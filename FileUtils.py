import os
import sys

import System
import System.Collections.Generic as SCG

import Rhino
from Rhino.FileIO import FileWriteOptions, FileReadOptions
import scriptcontext
import rhinoscriptsyntax as rs


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
        print 'Importing %s' % f
        scriptcontext.doc.ReadFile(f, opt)

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

def importLayerDict(filePaths, layerNames):
    '''Input a list of filePaths and a list of layerNames, in order to import all the
    files and return a list of RhinoObjects on each layer, in corresponding layers.
    Layers that do not exist or contain no objects will return empty lists.'''
    outObjs = []
    importFiles(filePaths)
    for ln in layerNames:
        objs = scriptcontext.doc.Objects.FindByLayer(ln)
        outObjs.append(objs)
    return dict(zip(layerNames, outObjs))

def exportLayers(layerNames, filePath, version=4):
    '''export only the items on designated layers to a file'''
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
    print 'exported %s' % filePath

