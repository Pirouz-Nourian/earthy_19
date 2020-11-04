
__author__ = "Ioannis_Tsionis"
__version__ = "2019.09.30"

#This script creates the surface geometry of a groined vault
#depending on the grid length and number of openings.
#By changing the arc radius and the angle,
#different sizes of semicircular or pointed vaults can be produced.


import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

cPoints = []
headArcN = []
arcPtsL = []
arcPtsR = []
startN = []
endN = []
planeN = []

#The script runs with a single point as an input.
#For the specific script [ x=0 ,0,0] is considered for the base point
x = 0
#This point will be the middle point
#of the length of the first arch opening in the array.

#For the number of arcs input,
#a series of components is generated linearly through a loop

for i in range(0,numArc):
    cPoint = rs.AddPoint(x,0,0)
    
    #The first arch is created.
    
    arcPtL = rs.PointAdd(cPoint, [-arcRad, 0, 0])
    arcPtsL.append(arcPtL)
    arcPtR = rs.PointAdd(cPoint, [arcRad, 0, 0])
    arcPtsR.append(arcPtR)
    
    uPoint = rs.PointAdd(cPoint, [0, 0, arcRad])
    plane = rs.WorldZXPlane()
    plane = rs.RotatePlane(plane, -90, axis=(0,1,0))
    headArcL = rs.AddArc(plane, arcRad, angle)
    rs.MoveObject(headArcL, [x,0,0])
    headArcR = rs.RotateObject(headArcL, cPoint, 180, axis=(0,0,1), copy=True)
    
    endL = rs.CurveEndPoint(headArcL)
    endR = rs.CurveEndPoint(headArcR)
    endN.append(endL)
    endN.append(endR)
    
    #If a different than 90 degrees angle is selected as the arc radius,
    #the arch sides have to reconnect and form the tip of the arch.
    
    gap = rs.DistanceToPlane(rs.WorldYZPlane(), endL)
    rs.MoveObject(headArcL, [-gap + x, 0, 0])
    rs.MoveObject(headArcR, [gap - x, 0, 0])
    
    #The arch perpendicular to the linear array (corridor pathway) is created.
    
    if i == 0:
        start1 = rs.CurveStartPoint(headArcL)
        perpArc = rs.JoinCurves([headArcL, headArcR], delete_input=False)
        perpArc = rs.RotateObject(perpArc, start1, 90, axis=(0,0,1), copy=True)
        start2 = rs.CurveEndPoint(perpArc)
        dis = start1.DistanceTo(start2)
        gapPerp = abs(gridLen-dis)/2
        perpArc = rs.MoveObject(perpArc, [0,gapPerp,-heightDiff])
    
    cPoints.append(cPoint)
    headArcN.append(headArcL)
    headArcN.append(headArcR)
    
    startL = rs.CurveStartPoint(headArcL)
    startR = rs.CurveStartPoint(headArcR)
    startN.append(startL)
    startN.append(startR)
    
    x = x + gridLen
    
extrDis = start1.DistanceTo(startN[-1])
print(extrDis)
