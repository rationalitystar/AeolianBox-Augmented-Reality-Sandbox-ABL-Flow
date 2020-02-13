''' This script creates the animation movie for the wind simulation. This is genetated using the trace program in paraview.
Ir runs using .pvpython in .....Paraviewxxxx/bin . This removes the prequisite of generating an environment specifically to run this.
Please Edit the line 12 ,109 and 362 with their appropriate directories. 
'''

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
controlDict = OpenFOAMReader(FileName='/home/pradyumn/Windsim_AR/SimpleFoam/system/controlDict')
controlDict.MeshRegions = ['internalMesh']
controlDict.CellArrays = ['U', 'epsilon', 'k', 'nut', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1485, 804]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# show data in view
controlDictDisplay = Show(controlDict, renderView1)
# trace defaults for the display properties.
controlDictDisplay.Representation = 'Surface'
controlDictDisplay.ColorArrayName = ['POINTS', 'p']
controlDictDisplay.LookupTable = pLUT
controlDictDisplay.OSPRayScaleArray = 'p'
controlDictDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
controlDictDisplay.SelectOrientationVectors = 'U'
controlDictDisplay.ScaleFactor = 18.676409149169924
controlDictDisplay.SelectScaleArray = 'p'
controlDictDisplay.GlyphType = 'Arrow'
controlDictDisplay.GlyphTableIndexArray = 'p'
controlDictDisplay.DataAxesGrid = 'GridAxesRepresentation'
controlDictDisplay.PolarAxes = 'PolarAxesRepresentation'
controlDictDisplay.ScalarOpacityFunction = pPWF
controlDictDisplay.ScalarOpacityUnitDistance = 8.19633274099326
controlDictDisplay.GaussianRadius = 9.338204574584962
controlDictDisplay.SetScaleArray = ['POINTS', 'p']
controlDictDisplay.ScaleTransferFunction = 'PiecewiseFunction'
controlDictDisplay.OpacityArray = ['POINTS', 'p']
controlDictDisplay.OpacityTransferFunction = 'PiecewiseFunction'


# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
controlDictDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Transform'
transform1 = Transform(Input=controlDict)
transform1.Transform = 'Transform'

# Properties modified on transform1.Transform
transform1.Transform.Translate = [0.0, 0.0, -10.0]

# Properties modified on transform1.Transform
transform1.Transform.Translate = [0.0, 0.0, -10.0]

# show data in view
transform1Display = Show(transform1, renderView1)
# trace defaults for the display properties.
transform1Display.Representation = 'Surface'
transform1Display.ColorArrayName = ['POINTS', 'p']
transform1Display.LookupTable = pLUT
transform1Display.OSPRayScaleArray = 'p'
transform1Display.OSPRayScaleFunction = 'PiecewiseFunction'
transform1Display.SelectOrientationVectors = 'U'
transform1Display.ScaleFactor = 18.676409149169924
transform1Display.SelectScaleArray = 'p'
transform1Display.GlyphType = 'Arrow'
transform1Display.GlyphTableIndexArray = 'p'
transform1Display.DataAxesGrid = 'GridAxesRepresentation'
transform1Display.PolarAxes = 'PolarAxesRepresentation'
transform1Display.ScalarOpacityFunction = pPWF
transform1Display.ScalarOpacityUnitDistance = 8.19633274099326
transform1Display.GaussianRadius = 9.338204574584962
transform1Display.SetScaleArray = ['POINTS', 'p']
transform1Display.ScaleTransferFunction = 'PiecewiseFunction'
transform1Display.OpacityArray = ['POINTS', 'p']
transform1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(controlDict, renderView1)

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'OpenFOAMReader'
controlDict_1 = OpenFOAMReader(FileName='/home/pradyumn/Windsim_AR/SimpleFoam/system/controlDict')
controlDict_1.MeshRegions = ['internalMesh']
controlDict_1.CellArrays = ['U', 'epsilon', 'k', 'nut', 'p']

# Properties modified on controlDict_1
controlDict_1.MeshRegions = ['depth_img']
controlDict_1.CellArrays = ['U']

# show data in view
controlDict_1Display = Show(controlDict_1, renderView1)
# trace defaults for the display properties.
controlDict_1Display.Representation = 'Surface'
controlDict_1Display.ColorArrayName = [None, '']
controlDict_1Display.DiffuseColor = [0.0, 0.0, 0.0]
controlDict_1Display.OSPRayScaleArray = 'U'
controlDict_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
controlDict_1Display.SelectOrientationVectors = 'U'
controlDict_1Display.ScaleFactor = 18.676409149169924
controlDict_1Display.SelectScaleArray = 'None'
controlDict_1Display.GlyphType = 'Arrow'
controlDict_1Display.GlyphTableIndexArray = 'None'
controlDict_1Display.DataAxesGrid = 'GridAxesRepresentation'
controlDict_1Display.PolarAxes = 'PolarAxesRepresentation'
controlDict_1Display.GaussianRadius = 9.338204574584962
controlDict_1Display.SetScaleArray = [None, '']
controlDict_1Display.ScaleTransferFunction = 'PiecewiseFunction'
controlDict_1Display.OpacityArray = [None, '']
controlDict_1Display.OpacityTransferFunction = 'PiecewiseFunction'


# update the view to ensure updated data information
renderView1.Update()

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(Input=transform1,
    Source=controlDict_1)

# show data in view
resampleWithDataset1Display = Show(resampleWithDataset1, renderView1)
# trace defaults for the display properties.
resampleWithDataset1Display.Representation = 'Surface'
resampleWithDataset1Display.ColorArrayName = ['POINTS', 'p']
resampleWithDataset1Display.DiffuseColor = [0.0, 0.0, 0.0]
resampleWithDataset1Display.LookupTable = pLUT
resampleWithDataset1Display.OSPRayScaleArray = 'p'
resampleWithDataset1Display.OSPRayScaleFunction = 'PiecewiseFunction'
resampleWithDataset1Display.SelectOrientationVectors = 'U'
resampleWithDataset1Display.ScaleFactor = 18.676409149169924
resampleWithDataset1Display.SelectScaleArray = 'p'
resampleWithDataset1Display.GlyphType = 'Arrow'
resampleWithDataset1Display.GlyphTableIndexArray = 'p'
resampleWithDataset1Display.DataAxesGrid = 'GridAxesRepresentation'
resampleWithDataset1Display.PolarAxes = 'PolarAxesRepresentation'
resampleWithDataset1Display.GaussianRadius = 9.338204574584962
resampleWithDataset1Display.SetScaleArray = ['POINTS', 'p']
resampleWithDataset1Display.ScaleTransferFunction = 'PiecewiseFunction'
resampleWithDataset1Display.OpacityArray = ['POINTS', 'p']
resampleWithDataset1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(transform1, renderView1)

# hide data in view
Hide(controlDict_1, renderView1)

# show color bar/color legend
resampleWithDataset1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=resampleWithDataset1)

# show data in view
extractSurface1Display = Show(extractSurface1, renderView1)
# trace defaults for the display properties.
extractSurface1Display.Representation = 'Surface'
extractSurface1Display.ColorArrayName = ['POINTS', 'p']
extractSurface1Display.DiffuseColor = [0.0, 0.0, 0.0]
extractSurface1Display.LookupTable = pLUT
extractSurface1Display.OSPRayScaleArray = 'p'
extractSurface1Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractSurface1Display.SelectOrientationVectors = 'U'
extractSurface1Display.ScaleFactor = 18.676409149169924
extractSurface1Display.SelectScaleArray = 'p'
extractSurface1Display.GlyphType = 'Arrow'
extractSurface1Display.GlyphTableIndexArray = 'p'
extractSurface1Display.DataAxesGrid = 'GridAxesRepresentation'
extractSurface1Display.PolarAxes = 'PolarAxesRepresentation'
extractSurface1Display.GaussianRadius = 9.338204574584962
extractSurface1Display.SetScaleArray = ['POINTS', 'p']
extractSurface1Display.ScaleTransferFunction = 'PiecewiseFunction'
extractSurface1Display.OpacityArray = ['POINTS', 'p']
extractSurface1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(resampleWithDataset1, renderView1)

# show color bar/color legend
extractSurface1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Generate Surface Normals'
generateSurfaceNormals1 = GenerateSurfaceNormals(Input=extractSurface1)

# show data in view
generateSurfaceNormals1Display = Show(generateSurfaceNormals1, renderView1)
# trace defaults for the display properties.
generateSurfaceNormals1Display.Representation = 'Surface'
generateSurfaceNormals1Display.ColorArrayName = ['POINTS', 'p']
generateSurfaceNormals1Display.DiffuseColor = [0.0, 0.0, 0.0]
generateSurfaceNormals1Display.LookupTable = pLUT
generateSurfaceNormals1Display.OSPRayScaleArray = 'p'
generateSurfaceNormals1Display.OSPRayScaleFunction = 'PiecewiseFunction'
generateSurfaceNormals1Display.SelectOrientationVectors = 'U'
generateSurfaceNormals1Display.ScaleFactor = 18.676409149169924
generateSurfaceNormals1Display.SelectScaleArray = 'p'
generateSurfaceNormals1Display.GlyphType = 'Arrow'
generateSurfaceNormals1Display.GlyphTableIndexArray = 'p'
generateSurfaceNormals1Display.DataAxesGrid = 'GridAxesRepresentation'
generateSurfaceNormals1Display.PolarAxes = 'PolarAxesRepresentation'
generateSurfaceNormals1Display.GaussianRadius = 9.338204574584962
generateSurfaceNormals1Display.SetScaleArray = ['POINTS', 'p']
generateSurfaceNormals1Display.ScaleTransferFunction = 'PiecewiseFunction'
generateSurfaceNormals1Display.OpacityArray = ['POINTS', 'p']
generateSurfaceNormals1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(extractSurface1, renderView1)

# show color bar/color legend
generateSurfaceNormals1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Glyph'
glyph1 = Glyph(Input=generateSurfaceNormals1,
    GlyphType='Arrow')
glyph1.Scalars = ['POINTS', 'p']
glyph1.Vectors = ['POINTS', 'U']
glyph1.ScaleFactor = 18.676409149169924
glyph1.GlyphMode = 'Every Nth Point'
glyph1.Stride = 15
glyph1.GlyphTransform = 'Transform2'

# Properties modified on glyph1
glyph1.Scalars = ['POINTS', 'None']
glyph1.ScaleFactor = 4
glyph1.Stride = 2

# show data in view
glyph1Display = Show(glyph1, renderView1)
# trace defaults for the display properties.
glyph1Display.Representation = 'Surface'
glyph1Display.ColorArrayName = ['POINTS', 'None']
glyph1Display.DiffuseColor = [0.0, 0.0, 0.0]
glyph1Display.LookupTable = pLUT
glyph1Display.OSPRayScaleArray = 'None'
glyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
glyph1Display.SelectOrientationVectors = 'GlyphVector'
glyph1Display.ScaleFactor = 19.077804565429688
glyph1Display.SelectScaleArray = 'None'
glyph1Display.GlyphType = 'Arrow'
glyph1Display.GlyphTableIndexArray = 'None'
glyph1Display.DataAxesGrid = 'GridAxesRepresentation'
glyph1Display.PolarAxes = 'PolarAxesRepresentation'
glyph1Display.GaussianRadius = 9.538902282714844
glyph1Display.SetScaleArray = ['POINTS', 'None']
glyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
glyph1Display.OpacityArray = ['POINTS', 'None']
glyph1Display.OpacityTransferFunction = 'PiecewiseFunction'


# show color bar/color legend
glyph1Display.SetScalarBarVisibility(renderView1, False)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(generateSurfaceNormals1)

# Properties modified on glyph1.GlyphTransform
#glyph1.GlyphTransform.Translate = [0.0, 0.0, 1.0]

# Properties modified on glyph1.GlyphTransform
#glyph1.GlyphTransform.Translate = [0.0, 0.0, 1.0]


# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
pLUT.ApplyPreset('jet', True)

# set active source
SetActiveSource(glyph1)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# set active source
SetActiveSource(generateSurfaceNormals1)

# set scalar coloring
ColorBy(generateSurfaceNormals1Display, ('POINTS', 'U', 'Magnitude'))



# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
generateSurfaceNormals1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
generateSurfaceNormals1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')


# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# Rescale transfer function
uLUT.RescaleTransferFunction(0.0, 20.0)

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# Rescale transfer function
uPWF.RescaleTransferFunction(0.0, 20.0)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
uLUT.ApplyPreset('jet', True)

# hide color bar/color legend
generateSurfaceNormals1Display.SetScalarBarVisibility(renderView1, False)

# Properties modified on renderView1
renderView1.UseGradientBackground = 0

# Properties modified on renderView1
renderView1.Background = [0.0, 0.0, 0.0]

# current camera placement for renderView1
renderView1.CameraPosition = [-2.7701603520527467, -3.499059476334448, 320.4257736347992]
renderView1.CameraFocalPoint = [-2.7701603520527467, -3.499059476334448, 55.78660583496094]
renderView1.CameraParallelScale = 146.82223607242062

# save animation
SaveAnimation('/home/pradyumn/Windsim_AR/SimpleFoam/sim.avi', renderView1, ImageResolution=[1552, 804],
    FrameWindow=[5, 19])

