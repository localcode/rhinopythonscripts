import os
import sys
import Rhino
from Rhino.FileIO import FileWriteOptions, FileReadOptions
import scriptcontext


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
        objs = scriptcontext.doc.Objects.FindByLayer(ln, True)
        outObjs.append(objs)
    return outObjs

