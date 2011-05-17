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


