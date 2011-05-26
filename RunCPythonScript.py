# This file is meant to be run by the IronPython Interpreter
# embedded in Rhino 5 WIP, but would probably work in other
# IronPython Interpreters.

# Python Standard Library imports
import os
import sys

# .NET imports
from System.Diagnostics import Process

def return_filter(data):
    """
    This is a hack to parse the data coming back from the
    subprocess.
    I'm sure a more experienced developer would do this
    way better.
    """
    outList = []
    # downside to this: if you try to return strings with
    # trailing whitespace, that whitespace will disappear
    for d in data.rstrip().split('\r\n'):
        try:
            # this should take care of everything but strings
            # this is completely insane
            outList.append(eval(d))
        except:
            outList.append(d)
    if len(outList) == 1:
        return outList[0]
    else:
        return outList


def run_command(args, input=None, verbose=False):
    """
    Run stuff on commandline.
    """
    # credit for this is due here:
    # http://www.ironpython.info/index.php/Launching_Sub-Processes
    p = Process()
    have_stdin = input is not None

    p.StartInfo.UseShellExecute = False
    p.StartInfo.RedirectStandardInput = have_stdin
    p.StartInfo.RedirectStandardOutput = True
    p.StartInfo.RedirectStandardError = True
    p.StartInfo.FileName = args[0]

    # not a precise way to join these! See list2cmdline in CPython's subprocess.py for the proper way.
    p.StartInfo.Arguments = ' '.join([str(a) for a in args[1:]])

    p.Start()
    if have_stdin:
        p.StandardInput.Write(input)
    if verbose:
        while not p.HasExited:
            p.Refresh()
            print
            print "%s -" % p.ToString()
            print "-----------------------"
            print "  physical memory usage: %s" % p.WorkingSet64
            print "  base priority: %s" % p.BasePriority
            print "  user processor time: %s" % p.UserProcessorTime
            print "  privileged processor time: %s" % p.PrivilegedProcessorTime
            print "  total processor time: %s" % p.TotalProcessorTime
            if p.Responding:
                print "Status = Running"
            else:
                print "Status = Not Responding"

    p.WaitForExit()
    stdout = p.StandardOutput.ReadToEnd()
    stderr = p.StandardError.ReadToEnd()
    return stdout, stderr, p.ExitCode

def run(pathToPythonScript, argumentList=[], pathToPython='python', verbose=False):
    # docstring
    """
    Runs a python script using another version of python.
    Intended to be used in IronPython in order to run scripts
    that don't work very well with IronPython. Returns a tuple
    containing [0] stdout (as a string), [1] stderr, and
    [2] exit code.

    Example Usage:
        >>> # a module that prints "hella world"
    >>> myModulePath = "C:\\Path\\To\\hella.py"
    >>> result = run(myModulePath)
    >>> print result
    ('hella world', '' ,0)

    Example 2:
        >>> # a module that prints the sum of two numbers
    >>> myModulePath = "C:\\Path\\To\\my\\module.py"
    >>> arguments = [5.6, 3]
    >>> result = run(myModulePath, arguments)
    >>> print result
    (8.6, '' ,0)

    Example 3:
        >>> # a module that prints "hella world"
    >>> # and then prints the sum of two numbers
    >>> myModulePath = "C:\\Path\\To\\hella.py"
    >>> arguments = [5.6, 3]
    >>> result = run(myModulePath, arguments)
    >>> print result
    (['hella world', 8.6], '', 0)

    Optionally, you can designate a path to the specific
    python interpreter you would like to use (maybe you want
    a specific version, or you did not put the path to
    python in your `Path` Environmental Variable):
        >>> pathToPythonInterpreter = "C:\\Python27\\python.exe"
    >>> result = run(myModulePath, arguments, pathToPythonInterpreter)
    >>> print result
    (8.6,'',0)
    """
    module = os.path.abspath(pathToPythonScript)
    pythonPath = os.path.abspath(pathToPython)
    module_path = '"%s"' % module
    args = [
            pathToPython,
            module_path
            ]
    if len(argumentList) > 0:
        for arg in argumentList:
            args.append(arg)
    std_out, std_err, exit_code = run_command(args, verbose=verbose)

    return std_out, std_err, exit_code


if __name__ == '__main__':
    pass
