# AR3B011 EARTHY (2019/20 Q1)
# Zaatari refugee camp Hammam project: "Janat Al-Tohr
#Group Members: Nikoleta Sidiropoulou,  Hans Gamerschlag, Noah van den Berg, Rick van Dijk, Maximilian Mandat, Hamidreza Shahriari
#This is script is drived from the work of  Sung, Woojae; 'COMPONENT ORIENTED SCRIPTING IN GRASSHOPPER VBRHINO GRASSHOPPER VISUAL BASIC WORKSHOP, 2011.11.18' ,www.woojsung.com 

import Rhino.Geometry as rg
import math
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

pathCount=0
newPath= GH_Path(pathCount)
pts=[]
tree=DataTree [rg.Point3d]()

for point in pointss:
    pathCount += 1
    newPath= GH_Path(pathCount)
    # Finding the normal normal vector of the point at mesh
    po=surface.ClosestMeshPoint(point,0.1)
    normal_vector=surface.NormalAt(po)
    # Geting the cross product vector
    drainVector= rg.Vector3d.CrossProduct(normal_vector,rg.Vector3d.ZAxis)
    drainVector.Unitize()
    # Rotating the cross product vector by 90 degree clock wise to find the drain slope vector
    drainVector.Transform(rg.Transform.Rotation(math.pi * 0.5, normal_vector, point))
    # Moving the initial point by the drain vector to find the position of the new vector
    movedPoint = point + distance * drainVector
    # Finding the position of the movedPoint on the mesh
    try:
        outPt= surface.NormalAt(surface.ClosestMeshPoint(movedPoint,0.1))
    except:
        break
    pts.append(point)
    pts.append(movedPoint)
    # Making a loop to simiulate the water flow on the mesh
    tol= 0.01
    dis=1
    while dis > tol:
        po=surface.ClosestMeshPoint(movedPoint,0.2)
        try:
            normal_vector=surface.NormalAt(po)
        except:
            break
        drainVector= rg.Vector3d.CrossProduct(normal_vector,rg.Vector3d.ZAxis)
        drainVector.Unitize()
        drainVector.Transform(rg.Transform.Rotation(math.pi * 0.5, normal_vector, point))
        movedPoint = movedPoint + distance * drainVector
        dis= movedPoint.DistanceTo(pts[-1])
        pts.append(movedPoint)
        tree.Add(movedPoint,newPath)