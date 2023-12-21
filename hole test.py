# Author- Phil Butterworth
# Description- Select a hole and it will select all holes of the same size in the document

import math
import traceback
import adsk.cam
import adsk.core
import adsk.fusion


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        faces = adsk.core.ObjectCollection.create()
        
        holeSize = None
        
        while holeSize is None:           
        # Get input for hole size
            dialog = ui.selectEntity('Select a hole', 'Faces')
            if dialog.entity.geometry.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
                ui.messageBox('Please select a hole')
                continue
            holeSize = dialog.entity.geometry.radius * 2

        # fild all bodies in the document
        for body in rootComp.bRepBodies:
            # find all the faces in the body
            for face in body.faces:
                if face.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType:
                    for edge in face.edges:
                        if edge.geometry.curveType == adsk.core.Curve3DTypes.Circle3DCurveType:
                            # Get the diameter of the circular edge
                            radius = edge.length / math.pi
                            if abs(radius - holeSize) < 0.01:
                                # Add the face to the collection
                                faces.add(face)
                                ui.activeSelections.add(face)



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
