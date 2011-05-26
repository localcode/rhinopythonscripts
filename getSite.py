import os
import sys

del sys.modules['RunCPythonScript']
del sys.modules['GeoJson2Rhino']

from RunCPythonScript import run as runC
import GeoJson2Rhino as geoJ


scriptToRun = 'C:\\Users\\demonchaux\\Dropbox\\localcode\\postsites\\postsites.py'
path2python = 'C:\\Program Files (x86)\\Python26\\python.exe'
vars = [45]
results = runC(scriptToRun, vars, path2python)
geoJ.loadLayers(results[0])