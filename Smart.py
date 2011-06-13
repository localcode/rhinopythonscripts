'''A module for wrapping geometry with UserString and Attribute Dictionaries'''

import Rhino

class SmartFeature(object):
    def __init__(self, rhinoObjectOrTuple):
        self._parseConstructor(rhinoObjectOrTuple)

    def _parseConstructor(self, rhinoObjectOrTuple):
        # determine if it is a tuple
        kind = type(rhinoObjectOrTuple)
        if kind == tuple or kind == list:
            # build from geom, user string pair
            pair = rhinoObjectOrTuple
            self.geom = pair[0] # geometry
            self.attributes = pair[1] # properties (as dictionary)
        else: # assume RhinoObject
            rhObj = rhinoObjectOrTuple
            self.geom = rhObj.Geometry
            self.attributes = {}
            numAtts = rhObj.Attributes.UserStringCount
            rawAtts = rhObj.Attributes.GetUserStrings()
            keys = rawAtts.AllKeys
            for key in keys:
                self.attributes[key] = rhObj.Attributes.GetUserString(key)

    def objAttributes(self, objectAttributes):
        for key in self.attributes:
            objectAttributes.SetUserString(key, self.attributes[key])
        return objectAttributes


