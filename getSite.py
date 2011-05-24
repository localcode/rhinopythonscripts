import os
import sys

del sys.modules['RunCPythonScript']

import RunCPythonScript

scriptToRun = 'C:\\Users\\demonchaux\\Dropbox\\localcode\\postsites\\postsites.py'
vars = [45]
print RunCPythonScript.run(scriptToRun, vars, verbose=True)