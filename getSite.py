import os
import sys

del sys.modules['RunCPythonScript']

import RunCPythonScript

scriptToRun = 'C:\\Users\\demonchaux\\Dropbox\\localcode\\postsites\\postsites.py'
path2python = 'C:\\Program Files (x86)\\Python26\\python.exe'
vars = [45]
results = RunCPythonScript.run(scriptToRun, vars, path2python)
print results