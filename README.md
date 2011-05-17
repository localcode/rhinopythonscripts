# RhinoPythonScripts

---

This is a repository for storing various useful python scripts for the embedded [IronPython](http://ironpython.codeplex.com/) engines in McNeel's [Rhino 5](http://download.rhino3d.com/rhino/5.0/wip) and [Grasshopper](www.grasshopper3d.com). Please feel free to fork this repo and add your own scripts or edit the exsiting ones. For any given scripts, please do your best to document any dependencies it has and put examples of use in the docstrings. If you want to edit or add to any of these scripts, please do.

Some of these scripts may be generally useful for IronPython, and for interfacing with related tools. I'm hoping to start a very general open repository of scripts that can become a shared collective resource.

For help and more information:

* [Rhino 5 Forums](http://v5.rhino3d.com)
* [Grasshopper Scripting Forum](http://www.grasshopper3d.com/forum/categories/vb-c-and-python-coding/listForCategory)
* [RhinoPython Scripting Forum](http://python.rhino3d.com/)
* [RhinoCommon SDK](http://www.rhino3d.com/5/rhinocommon/)
* [McNeel GitHub repos](https://github.com/mcneel)
* [Help with GitHub](http://help.github.com/)
* [Pro Git](www.progit.org)


---


## Currently Included Scripts


* #### GeoJson2Rhino
    
    A module for translating [GeoJSON](http://wiki.geojson.org/Main_Page) objects into Rhino objects, using RhinoCommon.

* #### RunCPythonScript

    A function for running python scripts that do not play well with IronPython. This script sends arguments to a script that is run on the normal CPython interpreter, and returns stdout, stderr, and exit code results. Obviously depends on having a [CPython](http://www.python.org/download/) (aka "traditional" Python) installed on the system.

* #### Make2D
    
    A module for automatically setting up camera views and exporting Make2Ds from Rhino

* #### InfraPy

    A module with some very general functions for managing data. Not Rhino or IronPython specific.


## Basic Use

### Checking Your Path

The following code will reveal what folders python can see. If folders are missing from the resulting list, then you cannot use the modules they contian.

    import sys
    for directory in sys.path:
        print directory

to add a folder to `sys.path`, assuming you already have the `import sys` line:

    sys.path.append("path/to/my/folder/that/contains/python/scripts")

Then you can import scripts from you folder.

### To Import Into a Script

The main folder, `rhinopythonscripts`, has been provided with an `__init__.py` file, so the whole thing can be treated as a package. Assuming your new script has access to the folder that teh `rhinopythonscripts` folder is _inside_ of, you can import various modules in the following way:

    from rhinopythonscripts import RunCPythonScript
    out = RunCPythonScript.run("someCPythonScript", argumentList)

or you can do stuff like this to import individual functions or give things shorter names:

    import rhinopythonscripts.InfraPy as ip
    from rhinopythonscripts import RunCPythonScript.run as runC
    out = runC("someCPythonScript", argumentList)

### Using GitHub to Contribute

coming soon ...
