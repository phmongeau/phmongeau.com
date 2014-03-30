"""
mirrorWrap: mirror non-symmetric blendShapes using a wrap deformer

Usage:
    - Select all targets first and the base mesh last.
    - Run the script
    - If the target meshes are named something like "L_shapeName", the script
      will replace the "L" with a "R" and vice versa.
"""
from maya import cmds

def mirrorName(name):
    # assuming obj are named "L_objName"
    if name[0] == "L":
        return "R" + name[1:]
    elif name[0] == "R":
        return "L" + name[1:]
    else:
        return name

def main():
    # duplicate and wrap selection
    selection = cmds.ls(sl=True)
    mainMesh = selection.pop()

    baseMesh = cmds.duplicate(mainMesh, rr=True, name=mainMesh+"_base")[0]
    wrapMesh = cmds.duplicate(mainMesh, rr=True, name=mainMesh+"_wrap")[0]

    # add blendshapes
    cmds.select(selection + [baseMesh], r=True)
    bShapeNode = cmds.blendShape(parallel=True)[0]

    # mirror baseMesh
    cmds.setAttr(baseMesh + ".sx", -1)

    # wrap constraint
    cmds.select([wrapMesh, baseMesh], r=True)
    cmds.CreateWrap()

    newShapes = []
    # duplicate each blendShape
    for shp in cmds.listAttr(bShapeNode, k=True, m=True)[1:]:
        cmds.setAttr(bShapeNode+"."+shp, 1)
        newShapes.extend(cmds.duplicate(wrapMesh, name=mirrorName(shp), rr=True))
        cmds.setAttr(bShapeNode+"."+shp, 0)

    #unparent the new shapes
    cmds.parent(newShapes, w=True)

    #cleanUp
    cmds.delete([baseMesh, wrapMesh])

if __name__ == "__main__": main()
