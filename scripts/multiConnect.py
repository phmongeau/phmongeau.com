"""
multiConnect: connect from one attribute to another attribute on multiple objects

Usage:
    - Select all targets first and the source last
    - Run the script:

        from multiConnect import MultiConnect
        MultiConnect()

    - use the ui to specify which attributes to connect
    - the buttons to the right of the fields can be used
      to select from a list of attributes
"""

import maya.cmds as cmds

class MultiConnect(object):
    def __init__(self):
        
        # delete previous window
        if cmds.window("multiConnect", exists=True):
            cmds.deleteUI("multiConnect")
        
        # create window
        self.mainWindow = cmds.window("multiConnect", title="multiConnect",
                            mnb=False, mxb=False, sizeable=False)
        
        self.mainLayout = cmds.columnLayout(w=300, h=300)

        cmds.separator(h=5)
        self.fromField = cmds.textFieldButtonGrp("fromField", label="From: ",
                                                 cw3=(50,240,50),
                                                 cc=self.connect, bc=lambda : self.getAttrWindow("from"))

        cmds.separator(h=5)
        self.toField = cmds.textFieldButtonGrp("toField", label="To: ",
                                               cw3=(50,240,50),
                                               cc=self.connect, bc=lambda : self.getAttrWindow("to"))

        cmds.separator(h=5)
        self.button = cmds.button(label="Connect", w=300, h=30,
                    c=lambda x: self.connect())
        
        # show window
        cmds.showWindow(self.mainWindow)

    def connect(self, *args):
        attrFrom = cmds.textFieldButtonGrp(self.fromField, query=True, tx=True)
        attrTo = cmds.textFieldButtonGrp(self.toField, query=True, tx=True).split(",")
        sel = cmds.ls(sl=True)
        fromObj = sel.pop()
        for obj in sel:
            try:
                for to in attrTo:
                    cmds.connectAttr(fromObj + "." + attrFrom,
                                    obj + "." + to, force=True)
            except RuntimeError:
                print "attributes already connected for " + obj

    def getAttrWindow(self, field):
        # delete previous window
        if cmds.window("attrList", exists=True):
            cmds.deleteUI("attrList")
        
        # create window
        window = cmds.window("attrList", title="attrList",
                            mnb=False, mxb=False, sizeable=False)

        mainLayout = cmds.columnLayout()

        sel = cmds.ls(sl=True)
        if field == "from":
            obj = sel.pop()
            attributes = cmds.listAttr(obj, connectable=True)
        else:
            obj = sel[0]
            attributes = cmds.listAttr(obj, connectable=True)

        self.attrList = cmds.textScrollList("attributes", h=500, ams=True, append=attributes, sc=lambda : self.onAttrSelect(field))

        cmds.showWindow(window)

    def onAttrSelect(self, field):
        items = cmds.textScrollList(self.attrList, q=True, si=True)
        cmds.textFieldButtonGrp(field + "Field", e=True, tx=",".join(items))

