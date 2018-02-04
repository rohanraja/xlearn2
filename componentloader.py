import os
import sys
from config import *
import datapoint

def readClassFromPyFile(pyDir, pyFileName, className):
    sys.path.insert(0, os.path.abspath(pyDir))
    mod = __import__(pyFileName)
    cls = getattr(mod, className)
    return cls

def generateTmpPyFileName(clsName=""):
    return "%s"%(clsName)

def getTmpPyDir():
    return TMP_DIR

def loadPyClassFromPyCode(pycode, className):
    tmp_py_filename = generateTmpPyFileName(className)
    tmp_py_dir = getTmpPyDir()
    f = open(os.path.join(tmp_py_dir, tmp_py_filename+".py") , 'w') 
    f.write(pycode)
    f.close()
    return readClassFromPyFile(tmp_py_dir, tmp_py_filename, className)



class ComponentsLoader():
    
    def loadComponents(self):
        self.loadEntityList()

    def getPyObject(self, entityParam):
        ent = entityParam.py_entity
        pycls = ent.python_class

        CLASS_FACTORY = loadPyClassFromPyCode(pycls.pycode, pycls.className)
        initParams = entityParam.params
        clsObj = CLASS_FACTORY(initParams)
        clsObj.entityParam = entityParam

        return clsObj

    def loadEntityList(self):

        self.entityParams = datapoint.ListPyEntityParamsOfExperiment(self.experimentId) 
        print("\nLoaded %d Python Class Entities for Experiment %s"%(len(self.entityParams) , self.experimentId))

        self.Components = {}


        for entityParam in self.entityParams:
            entity = entityParam.py_entity

            entity_py_object = self.getPyObject(entityParam)

            compList = self.Components.get(entity.Type, [])
            compList.append(entity_py_object)

            self.Components[entity.Type] = compList

            if entity.Type == MODEL_TYPE:
                print("Found Model: %s"%entity.name)

            if entity.Type == DATASET_TYPE:
                print("Found Dataset: %s"%entity.name)

            if entity.Type == PREPROCESSOR_TYPE:
                print("Found Preprocessor: %s"%entity.name)
