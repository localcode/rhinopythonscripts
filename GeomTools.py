'''A module of tools for short simpel geometry conversions and calculations. This module is likely to be split up into pieces in the future.'''
import Rhino

def pointsToCircles(pointList, radii):
    circles = []
    if len(radii) == 1:
        radii = [radii[0] for n in range(len(pointList))]
    if type(radii) == float or type(radii) == int:
        radii = [radii for n in range(len(pointList))]
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


