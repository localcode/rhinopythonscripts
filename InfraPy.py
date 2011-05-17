'''
A bunch of functions for general use. For now these mostly deal with
managing files and manipulating lists. I'm sure that many of these functions
could be replaced by commands form the standard library, or simply better use
python's existing commands.

Contains the following commands:
    listFiles(folder[, fullPath, fileExtension])
    listToText(inputList[, folder, outputName])
    editFilePrefix(oldPrefix, newPrefix, fileList)
    editFileExt(oldExt, newExt, fileList)
    linesToList(filePath)
    chopList(indices, anyList)

'''

import os


def get_modules(output):
    f = open(output, 'w')
    modules = str(help('modules'))
    f.write(modules)
    f.close()


def listFiles(folder, fullPath=False, fileExtension=None):
    """Returns a list of the files and folders in a given folder. The fullPath option determines whether it returns the
    full paths or just th efile names, and the fileExtension option restricts the result to files with a specific
    extension."""
    fileList = os.listdir(folder)
    if fullPath == True:
        folderPath = os.path.abspath(folder)
        fpList = []
        for filePath in fileList:
            newFilePath = os.path.join(folderPath, filePath)
            fpList.append(newFilePath)
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


