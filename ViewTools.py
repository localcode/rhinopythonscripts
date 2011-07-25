import Rhino
import scriptcontext

def _vp():
    return scriptcontext.doc.Views.ActiveView.ActiveViewport

def directionTargetView( view_vector, target_point ):
    viewport = _vp()
    viewport.SetCameraDirection(view_vector, True)
    viewport.SetCameraTarget(target_point, True)

def zoomToGeometry( geometry ):
    viewport = _vp()
    bbox = geometry.GetBoundingBox(True)
    viewport.ZoomBoundingBox(bbox)

def getCameraFrame():
    viewport = _vp()
    return viewport.GetCameraFrame()[1]

