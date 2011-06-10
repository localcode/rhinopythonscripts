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
    opt = FileWriteOptions()
    opt.FileVersion = version
    opt.WriteGeometryOnly = geomOnly
    opt.WriteSelectedObjectsOnly = selectedOnly
    return scriptcontext.doc.WriteFile(filePath, opt)

def importFiles(filePathList):
    opt = FileReadOptions()
    opt.ImportMode = True
    for f in filePathList:
        scriptcontext.doc.ReadFile(f, opt)

def deleteAll():
    """Deletes everything in the current Rhino scriptcontext.document. Returns nothing."""
    guidList = []
    objType = Rhino.DocObjects.ObjectType.AnyObject
    objTable = scriptcontext.doc.Objects
    objs = objTable.GetObjectList(objType)
    for obj in objs:
        guidList.append(obj.Id)
    for guid in guidList:
        objTable.Delete(guid, True)

