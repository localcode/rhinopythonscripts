'''
Created on Oct 24, 2010

@author: Benjamin
'''

import os

# Contains the following commands:
#     listFiles(folder, fullPath, fileExtension)
#     listToText(inputList, folder, outputName)
#     editFilePrefix(oldPrefix, newPrefix, fileList)
#     editFileExt(oldExt, newExt, fileList)
#     linesToList(filePath)
#     chopList(indices, anyList)

def get_modules(output):
    f = open(output, 'w')
    modules = str(help('modules'))
    f.write(modules)
    f.close()


def excelToXML(filePath, headerHeight=1, includeDeclaration=True):
    """
    reads an excel file and converts each line to a separate XML object
    Does not read the first line, but uses it for labelling each tag.
    Returns the tab formatted XML text.
    the headerHeight variable can be set to ignore larger
    headers, in case there are more lines in the header than 1.
    includeDeclaration is a boolean that determines if an xml declaration
    should be included at the beginning of the string.
    """



def excelToJSON(filePath, headerHeight=1):
    """
    reads an excel file and converts each line to a separate JSON object
    Does not read the first line, but instead uses it to extract labels
    for the object attributes.
    Returns the JSON format text, with one object per line.
    the headerHeight variable can be set to ignore larger
    headers, in case there are more lines in the header than 1.
    """


def xmlToJSON(xmlTextString):
    """
    reads a string of XML text and converts it to JSON format
    returns the JSON formatted text.
    """


def jsonToXML(jsonTextString, includeDeclaration=True):
    """
    reads a string of JSON formatted text and converts it to
    XML format. returns the formatted XML text.
    includeDeclaration is a boolean that determines if an xml declaration
    should be included at the beginning of the string.
    """

def excelToDjangoModel(filePath):
    """
    reads an excel file and uses the first two lines to create attributes
    and data types for each attribute. The first line determines the name
    of each attribute, and the second line determines the data type of each attribute.
    returns a string that can be pasted into a models.py file for a django
    app.
    """



def listFiles(folder, fullPath=False, fileExtension=None):
    """Returns a list of the files and folders in a given folder. The fullPath option determines whether it returns the
    full paths or just th efile names, and the fileExtension option restricts the result to files with a specific
    extension."""
    fileList = os.listdir(folder)
    if fullPath == True:
        fpList = []
        for file in fileList:
            # this needs to be adjusted for the interpreter
            # it seems that Rhino5 can take either \,/, or \\
            # but that IDLE takes one type for each
            # operating system
            file = folder+'/'+file
            fpList.append(file)
        fileList = fpList

    if fileExtension != None:
        newList = []
        chop = -len(fileExtension)
        for file in fileList:
            if file[chop:] == fileExtension:
                newList.append(file)
        return newList
    return fileList

def listToText(inputList, folder=None, outputName='list.txt'):
    '''
    Creates a text file from a list (with each list item on a separate line). May be placed in any given folder, but will otherwise be created in the working directory of the python interpreter.
    '''
    fname = outputName
    if folder != None:
        fname = folder+'/'+fname
    f = open(fname, 'w')
    for file in inputList:
        f.write(file+'\n')
    f.close()

def editFilePrefix(oldPrefix, newPrefix, fileList):
    """Changes the file names of a list of files. Could be used on any list fo strings."""
    splitIndx = len(oldPrefix)
    newList = []
    for fileName in fileList:
        nameBit = fileName[splitIndx:]
        newName = newPrefix + nameBit
        newList.append(newName)
    return newList

def editFileExt(oldExt, newExt, fileList):
    splitIndex = -len(oldExt)
    returnList = []
    for fileName in fileList:
        nameBit = fileName[:splitIndex]
        newName = nameBit+newExt
        returnList.append(newName)
    return returnList

def linesToList(filePath):
    f = open(filePath)
    lineList = f.read().splitlines()
    return lineList

def chopList(indices, anyList):
    newList = anyList[:]
    if type(indices) == tuple:
        indexSpread = list(indices)
    elif type(indices) == list:
        indexSpread = indices[:]
    else:
        indexSpread = [indices]
    indexSpread.append(len(newList))
    chunks = []
    for i in range(len(indexSpread) - 1):
        chunks.append(newList[indexSpread[i]:indexSpread[i+1]])
    return chunks


if __name__=='__main__':

    # these declared variables will need to be inputs
    folder = '/LocalCodeFullBatch/GIS_data/bmpBuffers'
    cnnFileFolder = '/LocalCodeFullBatch'
    reportFile = cnnFileFolder + '/ShapefileImportReport.txt'


    # load CNN list
    bufferlist = listFiles(folder, fullPath=True, fileExtension='.shp')
    blist = listFiles(folder, fullPath=False, fileExtension='.shp')
    mPatchList = editFilePrefix('Buffers2_Buffer','MultiPatchTerrain', blist)
    listToText(blist, cnnFileFolder, 'bufferList.txt')
    listToText(mPatchList, cnnFileFolder, 'mPatchList.txt')





