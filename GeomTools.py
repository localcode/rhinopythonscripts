'''A module of tools for short simpel geometry conversions and calculations. This module is likely to be split up into pieces in the future.'''
import Rhino
import scriptcontext

def pointsToCircles(pointList, radii):
    circles = []
    if type(radii) == float or type(radii) == int:
        radii = [radii for n in range(len(pointList))]
    elif len(radii) == 1:
        radii = [radii[0] for n in range(len(pointList))]
    for i in range(len(pointList)):
        point = pointList[i]
        radius = radii[i]
        circles.append(Rhino.Geometry.Circle(point, radius))
    return circles

def pointGrid(xrows=10, ycols=10, xspacing=1, yspacing=1):
    xA = range(0, (xrows*xspacing), xspacing)
    yA = range(0, (ycols*yspacing), yspacing)
    xVals = [float(x-((xrows-1)*xspacing/2)) for x in xA]
    yVals = [float(y-((ycols-1)*yspacing/2)) for y in yA]
    out = []
    for y in yVals:
        for x in xVals:
            out.append(Rhino.Geometry.Point3d(x, y, 0.0))
    return out

def curveClosestPoint3d(curve, point, searchDistance=1000.0):
    '''enter curve and point (and optional max distance),
    and returns a point3d or None (if no points within distance)'''
    result = curve.ClosestPoint(point, searchDistance)
    # if something could be found within the search distance
    if result[0]:
        t = result[1]
        return curve.PointAt(t) # get the point
    else: # no point found
        return None

def vectorToClosestCurve(point, curves, searchDistance=1000.0):
    '''get the vector from a point to the closest curve in a
    set of curves. If none are within searchDistance, return None.'''
    testDistance = searchDistance
    vector = None
    for curve in curves:
        closestPt = curveClosestPoint3d(curve, point, searchDistance)
        if closestPt:
            newVector = point.Subtract(closestPt, point)
            if newVector.Length < testDistance:
                testDistance = newVector.Length
                vector = newVector
    return vector

def moveMany(listOfThings, vector):
    '''Translate (move) a list of geometries.'''
    out = []
    for thing in listOfThings:
        out.append(thing.Translate(vector))
    return out

def rotateMany(listOfThings, radiansAngle, axisVector, origin):
    '''Rotate a list of geometries.'''
    out = []
    for thing in listOfThings:
        out.append(thing.Rotate(radiansAngle, axisVector, origin))
    return out

def bakeMany(listOfThings, objectAttributes=None):
    if not objectAttributes:
        objectAttributes = Rhino.DocObjects.ObjectAttributes()
    for thing in listOfThings:
        # move from specific to broad
        if isinstance(thing, Rhino.Geometry.Point3d):
            scriptcontext.doc.Objects.AddPoint(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Curve):
            scriptcontext.doc.Objects.AddCurve(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Brep):
            scriptcontext.doc.Objects.AddBrep(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Surface):
            scriptcontext.doc.Objects.AddSurface(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Mesh):
            scriptcontext.doc.Objects.AddSurface(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Hatch):
            scriptcontext.doc.Objects.AddHatch(thing, objectAttributes)
        elif isinstance(thing, Rhino.Display.Text3d):
            scriptcontext.doc.Objects.AddText(thing, objectAttributes)


