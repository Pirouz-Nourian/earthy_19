# AR3B011 EARTHY (2019/20 Q1)
# Zaatari refugee camp Hammam project: "Janat Al-Tohr
#Group Members: Nikoleta Sidiropoulou,  Hans Gamerschlag, Noah van den Berg, Rick van Dijk, Maximilian Mandat, Hamidreza Shahriari

import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
lst=[]
face=[]
Inv=[]

#Finding the boundary lines of the mesh
faceBound= ghc.FaceBoundaries(mesh)

#colliding the wall edges with boundary face of the mesh to find the faces touching the walls
coll= ghc.CollisionOneXMany(faceBound,Edg)[0]
meshCull= ghc.CullFaces(mesh,coll)

# Sepprating the faces touching the walls
meshCullInv= ghc.CullFaces(mesh,[not i for i in coll])
lst.append(meshCull)
face.append(faceBound)
Inv.append(meshCullInv)
meshEdg= ghc.MeshEdges(Inv[-1])[0]

#Making a loop to find the slabs of the Muqarnas
while i<100:
    try:
        meshEdg= ghc.MeshEdges(Inv[-1])[0]
        InEdg= ghc.JoinCurves(meshEdg, True)
        faceBound= ghc.FaceBoundaries(lst[-1])
        coll= ghc.CollisionOneXMany(faceBound,InEdg)[0]
        meshCull= ghc.CullFaces(lst[-1],coll)
        meshCullInv= ghc.CullFaces(lst[-1],[not i for i in coll])
        meshes= ghc.CullFaces(lst[-1],coll)
        lst.append(meshCull)
        Inv.append(meshCullInv)
        face.append(faceBound)
    except:
        break
    i=i+1
