from job import Job
from project import createProject
from project import loadJob
from componentloader import loadClass
from xlearn2 import getFullPathofLib
from os import listdir
import os


def getClassIndex(clsName):

    itemsPath = getFullPathofLib(clsName)
    items = listdir(itemsPath)
    out = []
    for i in items:
        out.append("%s/%s" % (clsName, i) )
    return out


modelsIndex = getClassIndex("model")
datasetsIndex = getClassIndex("dataset")


