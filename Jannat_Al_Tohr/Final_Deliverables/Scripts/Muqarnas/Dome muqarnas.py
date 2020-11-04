# AR3B011 EARTHY (2019/20 Q1)
# Zaatari refugee camp Hammam project: "Janat Al-Tohr
#Group Members: Nikoleta Sidiropoulou,  Hans Gamerschlag, Noah van den Berg, Rick van Dijk, Maximilian Mandat, Hamidreza Shahriari

import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
lst=[]
edges=[]
Mess=[]
bollen=[]
face=[]
Inv=[]
#Finding the naked edges of the Mesh

meshEdg= ghc.MeshEdges(mesh)[0]
Edg= ghc.JoinCurves(meshEdg, True)

#Finding the boundary lines of the mesh
faceBound= ghc.FaceBoundaries(mesh)

#colliding the naked edges with boundary face of the mesh to find the faces touching the naked edges
coll= ghc.CollisionOneXMany(faceBound,Edg)[0]
meshCull= ghc.CullFaces(mesh,coll)

# Sepprating the faces touching the naked edges
meshCullInv= ghc.CullFaces(mesh,[not i for i in coll])
Inv.append(meshCullInv)
lst.append(meshCull)
bollen.append(coll)
face.append(faceBound)
i=0
edges.append(Edg)

#Making a loop to find the slabs of the Muqarnas
while i<400:
    try:
        meshEdg= ghc.MeshEdges(lst[-1])[0]
        Edg= ghc.JoinCurves(meshEdg, True)
        faceBound= ghc.FaceBoundaries(lst[-1])
        coll= ghc.CollisionOneXMany(faceBound,Edg)[0]
        meshCull= ghc.CullFaces(lst[-1],coll)
        meshes= ghc.CullFaces(lst[-1],coll)
        meshCullInv= ghc.CullFaces(lst[-1],[not i for i in coll])
        Inv.append(meshCullInv)
        Mess.append(meshes)
        bollen.append(coll)
        lst.append(meshCull)
        edges.append(Edg)
        face.append(faceBound)
    except:
        break
    i=i+1
