from System.Collections.Generic import List

import Rhino
import scriptcontext
from Smart import SmartFeature
import RangeTools

from Rhino.Geometry import Vector3d, Point3d, Plane, Curve

def smartPointProject(smartPoints, brep, vector=Vector3d(0.0,0.0,1.0), tolerance=0.001):
    resultSet = []
    # project everything
    for smartPt in smartPoints:
        result = Rhino.Geometry.Intersect.Intersection.ProjectPointsToBreps([brep],
                [smartPt.geom],
                vector, tolerance)
        if len(result) > 0:
            smartPt.geom = result[0]
            resultSet.append(smartPt)
    return resultSet

def smartPointLayerProject(pointLayerName, surfaceLayerName,
        objectAttributes=None, vector=Vector3d(0.0,0.0,1.0),
        tolerance=0.001):
    '''Project a layer contining only points onto a layer containing a surface,
    and maintain UserString associations between the original and projected points.
    ObjectAttributes can be passed in to predetermine a layer or other data. Returns
    a list of (Geometry, ObjAttributes) pairs, with user keys set. If anything fails,
    should print an error message and return an empty set.'''
    objs = scriptcontext.doc.Objects.FindByLayer(pointLayerName)
    if len(objs) == 0:
        print 'No Curves found on %s' % pointLayerName
        return []
    # get the surface(s)
    srfObjs = scriptcontext.doc.Objects.FindByLayer(surfaceLayerName)
    if len(srfObjs) == 0:
        print 'no surfaces found on %s' % surfaceLayerName
        return []
    else:
        srf = srfObjs[0].Geometry
    # deal with ObjectAttributes
    if objectAttributes:
        att = objectAttributes
    else:
        att = Rhino.DocObjects.ObjectAttributes()
    resultSet = []
    # project everything
    for ptObj in objs:
        smartPt = SmartFeature(ptObj)
        smartAtt = smartPt.objAttributes(att)
        projPoints = Rhino.Geometry.Intersect.Intersection.ProjectPointsToBreps([srf],
                [smartPt.geom.Location],
                vector,
                tolerance)
        for pt in projPoints:
            smartPair = (pt, smartAtt)
            resultSet.append(smartPair)
    return resultSet

def smartCurveLayerProject(curveLayerName, surfaceLayerName,
        objectAttributes=None, vector=Vector3d(0.0,0.0,1.0),
        tolerance=0.001):
    '''Project a layer contining only curves onto a layer containing a surface,
    and maintain UserString associations between the original and projected curves.
    ObjectAttributes can be passed in to predetermine a layer or other data. Returns
    a list of (Geometry, ObjAttributes) pairs, with user keys set. If anything fails,
    should print an error message and return an empty set.'''
    # get the curves
    objs = scriptcontext.doc.Objects.FindByLayer(curveLayerName)
    if len(objs) == 0:
        print 'No Curves found on that layer'
        return []
    # get the surface(s)
    srfObjs = scriptcontext.doc.Objects.FindByLayer(surfaceLayerName)
    if len(srfObjs) == 0:
        print 'no surfaces found on that layer'
        return []
    else:
        srf = srfObjs[0].Geometry
    # deal with ObjectAttributes
    if objectAttributes:
        att = objectAttributes
    else:
        att = Rhino.DocObjects.ObjectAttributes()
    resultSet = []
    # project everything
    for crvObj in objs:
        smartCurve = SmartFeature(crvObj)
        smartAtt = smartCurve.objAttributes(att)
        projCurves = smartCurve.geom.ProjectToBrep(smartCurve.geom,
                                                srf,
                                                vector,
                                                tolerance)
        for crv in projCurves:
            smartPair = (crv, smartAtt)
            resultSet.append(smartPair)

    return resultSet


def interpolatePointsToTerrainMesh(points, terrainMesh):
    out = []
    for pt in points:
        pts = [pt]
        meshes = [terrainMesh]
        vect = Vector3d(0.0,0.0, 1.0)
        tol = 0.001
        intResult = Rhino.Geometry.Intersect.Intersection.ProjectPointsToMeshes(meshes, pts, vect, tol)
        if len(intResult) == 1: # it hit, and just once
            out.append(intResult[0]) # add the result
        elif len(intResult) < 1: # it missed
            # approximate the z value
            line = Rhino.Geometry.Line(pt, vect)
            closPt = terrainMesh.ClosestPoint(pt)
            roughPt = line.ClosestPoint(closPt, False)
            closestTerrain = terrainMesh.ClosestPoint(roughPt)
            roughPt.Z = closestTerrain.Z
            out.append(roughPt)
        else: # it hit twice??!!
            # this appears to happen often.
            out.append(intResult[0]) # use the first intersection anyway
    return out


def contourBrepInZ(brep, stepSize):
    # get the upper and lower limits
    bbox = brep.GetBoundingBox(True)
    zMin, zMax = bbox.Min.Z, bbox.Max.Z
    zRange = zMax-zMin
    vect = Vector3d(0.0,0.0,1.0)
    # the next line is dense
    planes = [Plane(Point3d(0.0, 0.0, z), vect) for z in RangeTools.drange(zMin,zMax, 0.5)]
    resultList = []
    for plane in planes:
        curves = brep.CreateContourCurves(brep, plane)
        resultList.append(curves)
    return resultList





