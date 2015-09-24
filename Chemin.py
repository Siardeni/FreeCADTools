# -*- coding:Utf-8 -*-

import FreeCAD, FreeCADGui, os

def modulePath():
    """returns the current design module path
    @return Module path"""
    path1 = FreeCAD.ConfigGet("AppHomePath") + "Mod/FreeCADTools"
    path2 = FreeCAD.ConfigGet("UserAppData") + "Mod/FreeCADTools"
    if os.path.exists(path2):
        return path2
    else:
        return path1

def iconsPath():
    """returns the current design module icons path
    @return Icons path"""
    path = modulePath() + "/Icones"
    return path

def getPathFromFile(fileName):
    """ Gets the directory path from a file name
    @param fileName Name of the file
    @return Directory path.
    """
    if not fileName:
        return ''
    i = 1
    try:
        while 1:
            i = fileName.index("/", i+1)
    except ValueError:
        pass
    return fileName[0:i+1]
    
def gethomePath():
    """Get the home directory
    @return homedirectory
    """
    path=os.path.expanduser('~')
    return path

def CheminEchange(Choix):
    plateform=os.sys.platform
    if plateform=="linux2":
        if Choix==1:
            CheminEchange='/home/nico/.FreeCAD/Echanges FreeCAD'
    else :
        if Choix==1:
            CheminEchange='E:/Nico/02 - CAO/FreeCAD/Echanges FreeCAD'
    return CheminEchange
