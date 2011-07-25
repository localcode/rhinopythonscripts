"""A module of graph (nodes/links, not charts) tools for Rhino built off of NetworkX
    Requires that the networkx module is installed and available on sys.path.
    For more information on NetworkX visit the site at:
        http://networkx.lanl.gov/contents.html
"""

import networkx
import Rhino

class MeshGraph(object):
    def __init__(self, mesh):
        self.mesh = mesh
