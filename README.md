# RhinoPythonScripts

---

This is a repository for storing various useful python scripts for the embedded [IronPython](http://ironpython.codeplex.com/) engines in McNeel's [Rhino 5](http://download.rhino3d.com/rhino/5.0/wip) and [Grasshopper](www.grasshopper3d.com). Please feel free to fork this repo and add your own scripts or edit the exsiting ones. For any given scripts, please do your best to document any dependencies it has and put examples of use in the docstrings. If you want to edit or add to any of these scripts, please do.

Some of these scripts may be generally useful for IronPython, and for interfacing with related tools. I'm hoping to start a very general open repository of scripts that can become a shared collective resource.

For help and more information:

* [Rhino 5 Forums](http://v5.rhino3d.com) - For help and suggestions about Rhino 5
* [Grasshopper Scripting Forum](http://www.grasshopper3d.com/forum/categories/vb-c-and-python-coding/listForCategory) - For help with scripting in Grasshopper
* [RhinoPython Scripting Forum](http://python.rhino3d.com/) - For help with scripting in Rhino.
* [RhinoCommon SDK](http://www.rhino3d.com/5/rhinocommon/) - The API reference.
* [McNeel GitHub repos](https://github.com/mcneel) - Official McNeel code repositories.
* [Help with GitHub](http://help.github.com/) - For learning how to use Git and GitHub.
* [Pro Git](http://www.progit.org) - For learning more about Git.
* [StackOverflow](http://stackoverflow.com/) - For general programming questions.


## Currently Included Scripts


* #### GeoJson2Rhino
    
    A module for translating [GeoJSON](http://wiki.geojson.org/Main_Page) objects into Rhino objects, using RhinoCommon.

* #### RunCPythonScript

    A function for running python scripts that do not play well with IronPython. This script sends arguments to a script that is run on the normal CPython interpreter, and returns stdout, stderr, and exit code results. Obviously depends on having a [CPython](http://www.python.org/download/) (aka "traditional" Python) installed on the system.

* #### Make2D
    
    A module for automatically setting up camera views and exporting Make2Ds from Rhino

* #### InfraPy

    A module with some very general functions for managing data. Not Rhino or IronPython specific.


## Download and Getting Started (for beginners who don't want to learn about Git)


You can easily download the entire collection of scripts in one folder, and
quickly get started. Here's how:

1. Choose a folder on your computer where you would like to keep downloaded scripts.
2. Look for the link right here on [this webpage](https://github.com/bengolder/rhinopythonscripts) named 'Downloads'. Click on it, and then select the zip file.
3. After you download the zip file, make sure that the unzipped folder is in the folder where you want to keep downloaded scripts. Rename the unzipped folder to `rhinopythonscripts`.
4. The unzipped folder contains all the scripts in this repository. If you look in the folder, you'll notice a file called `__init__.py`, along with all the other scripts. In Python lingo, this folder is a [_package_](http://docs.python.org/tutorial/modules.html#packages) of [_modules_](http://docs.python.org/tutorial/modules.html).
5. Start writing your own script. On Windows you can do this using the `EditPythonScript` Rhino command, which will open a script editor. On Mac or Windows, you can write a script with any basic text editor, and there are many to choose from. Some popular text editors for people who use Python are [TextMate](http://macromates.com/)(Mac), [E Text Editor](http://www.e-texteditor.com/) (Windows), [Notepad++](http://notepad-plus-plus.org/) (Windows), or you can set up a full [IDE](http://en.wikipedia.org/wiki/Integrated_development_environment) using [Steve Baer's helpful instructions](http://python.rhino3d.com/entries/12-Configuring-Pydev-for-Rhino.Python) on setting up [PyDev](http://pydev.org/). If you enjoy scripting in Rhino and using a command line, you might like [Vim](http://www.vim.org/download.php), which is a scriptable text editor that, like Rhino, includes a command line.
6. In your script, write the following, and then save it (make sure it has the `.py` extension).

    ```python
    # 'sys' is a built-in python module containing system utilities
    import sys
    # sys.path is the list of folders that python can 'see'
    for i in sys.path:   # for each folder path in the list:
        print i          # print the folder path
    ```

7. Run the script using the `RunPythonScript` command in Rhino, or by simply pressing the green 'play' button in the Rhino python script editor. You should see a list of file paths to different folders.
8. Make sure that the folder _containing_ your `rhinopythonscripts` folder is in the list of folders. If not, then add the following to your script (using the appropriate file path):

    ```python
    # here we are appending a folder path to the list
    # of folders that python can 'see'
    sys.path.append("the/path/to/the/folder/that/contains/rhinopythonscripts")
    ```

9. Add the following to the end of your script, and then run it again:

    ```python
    import rhinopythonscripts
    ```

10. If you don't see any errors when you run it, that means it's working. You can now import any of the functions from the package and use them in your own scripts. For example, the following code would move objects from one layer in your current Rhino document to another. You can add this to the end of your script and it should work (assuming both layers exist and you have objects on the first layer).

    ```python
    # first we import the switchLayers function from the Make2D module
    from rhinopythonscripts.Make2D import switchLayers
    # now we can run it. It will moves objects from the first layer
    # to the second layer.
    switchLayers("Layer 5000", "Layer 2999") 
    ```
    
11. A couple quick ways to explore the package using python:

    ```python
    # .__doc__ will print out the docstring of a function or module
    switchLayers.__doc__
    # dir() will print out a list available commands for any module,
    # function or object in python
    dir(rhinopythonscripts.Make2D)
    ```

Enjoy! See above for more places to get help.


## Basic Use

### Checking Your Path

The following code will reveal what folders python can see. If folders are missing from the resulting list, then you cannot use the modules they contian.

```python
import sys
for directory in sys.path:
    print directory
```

To add a folder to `sys.path`, assuming you already have the `import sys` line:

```python
sys.path.append("path/to/my/folder/that/contains/python/scripts")
```

Then you can import scripts from you folder.

### To Import Into a Script

The main folder, `rhinopythonscripts`, has been provided with an `__init__.py` file, so the whole thing can be treated as a package. Assuming your new script has access to the folder that the `rhinopythonscripts` folder is _inside_ of (see _Checking Your Path_ above), you can import various modules in the following way:

```python
from rhinopythonscripts import RunCPythonScript
out = RunCPythonScript.run("someCPythonScript", argumentList)
```

or you can do stuff like this to import individual functions or give things shorter names:

```python
import rhinopythonscripts.InfraPy as ip
from rhinopythonscripts.RunCPythonScript import run as runC
out = runC("someCPythonScript", argumentList)
```

### Using GitHub to Download, Update, and Contribute

1. First, [install git](http://git-scm.com/) for your system and set it up.

#### Forking

1. [Fork the repository](http://help.github.com/fork-a-repo/) on GitHub.
1. Get to the folder where you want things to be stored

    * On Windows, open the Git Bash program, and use `cd foldername` and `cd ..` to get to the folder you want.
    * On Mac, open Terminal and use `cd foldername` and `cd ..` to get to the folder you want.

1. Using Terminal (Mac) or Git Bash (Windows), use git to clone the repository onto your computer by typing the following command:

    `git clone git@github.com:yourusername/rhinopythonscripts.git` Where `yourusername` is replaced by your user name, obviously.

1. Now you have created a folder, inside of whatever folder you were in, called `rhinopythonscripts`. Everything is inside of that folder and you can use it. :)

#### Updating

coming soon ...

#### Contributing

coming soon ...

#### Quickly Patching Something in the Code

coming soon ...

#### Noting Issues

coming soon ...
 

