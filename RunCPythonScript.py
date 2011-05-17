# This file is meant to be run by the IronPython Interpreter
# embedded in Rhino 5 WIP, but would probably work in other
# IronPython Interpreters.

# Python Standard Library imports
import os
import sys

# .NET imports
from System.Diagnostics import Process



def run_command(args, input=None):
    # credit for this si due here:
    # http://www.ironpython.info/index.php/Launching_Sub-Processes
    p = Process()
    have_stdin = input is not None
    p.StartInfo.UseShellExecute = False
    p.StartInfo.RedirectStandardInput = have_stdin
    p.StartInfo.RedirectStandardOutput = True
    p.StartInfo.RedirectStandardError = True
    p.StartInfo.FileName = args[0]

    # not a precise way to join these! See list2cmdline in CPython's subprocess.py for the proper way.
    p.StartInfo.Arguments = args[1]

    p.Start()
    if have_stdin:
        p.StandardInput.Write(input)
    p.WaitForExit()
    stdout = p.StandardOutput.ReadToEnd()
    stderr = p.StandardError.ReadToEnd()
    return stdout, stderr, p.ExitCode

def run(pathToPythonScript, argumentList, pythonToPath='python'):
    module = os.path.abspath(pathToPythonScript)
    module_path = '"%s"' % module
    args = [
            pythonPath,
            module_path
            ]
    if len(argumentList) > 0:
        for arg in argumentList:
            args.append(arg)
    std_out, std_err, exit_code = run_command(args)
    return std_out, std_err, exit_code



