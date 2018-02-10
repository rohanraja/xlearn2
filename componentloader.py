import os
import sys
from .config import *
from . import datapoint
import pickle

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

    def __init__(self, pDatapoint=None):
        if pDatapoint == None:
            self.datapoint = datapoint
        else:
            self.datapoint = pDatapoint
    
    def loadComponents(self):
        self.loadEntityList()

        if MODEL_TYPE in self.Components:
            self.model = self.Components[MODEL_TYPE][0]

        if DATASET_TYPE in self.Components:
            self.train_dataset = self.Components[DATASET_TYPE][0]

        if TEST_TYPE in self.Components:
            self.test_dataset = self.Components[TEST_TYPE][0]

        if VALIDATION_TYPE in self.Components:
            self.validation_dataset = self.Components[VALIDATION_TYPE][0]

        if PREPROCESSOR_TYPE in self.Components:
            self.preprocessors = self.Components[PREPROCESSOR_TYPE]
            self.preprocessors.sort(key=lambda x: x.entityParam.role)

    def getPyObject(self, entityParam, ent, pycls):
        CLASS_FACTORY = loadPyClassFromPyCode(pycls.pycode, pycls.className)
        initParams = entityParam.params
        clsObj = CLASS_FACTORY(initParams)
        clsObj.entityParam = entityParam

        return clsObj

    def loadEntityList(self):

        self.entityParams = self.datapoint.ListPyEntityParamsOfExperiment(self.experimentId) 
        # pickle.dumps(self.entityParams)

        print("\nLoaded %d Python Class Entities for Experiment %s"%(len(self.entityParams) , self.experimentId))

        self.Components = {}


        for entityParam in self.entityParams:
            entity = self.datapoint.GetPyEntityFromParam(entityParam.id)
            # pickle.dumps(entity)
            pycls = self.datapoint.GetPyClassFromPyEntity(entity.id)
            # pickle.dumps(pycls)

            entity_py_object = self.getPyObject(entityParam, entity, pycls)

            key = min(entityParam.role, PREPROCESSOR_TYPE)


            compList = self.Components.get(key, [])
            compList.append(entity_py_object)

            self.Components[key] = compList

            if entity.Type == MODEL_TYPE:
                print("Found Model: %s"%entity.name)

            if entity.Type == DATASET_TYPE:
                print("Found Dataset: %s"%entity.name)

            if entity.Type == PREPROCESSOR_TYPE:
                print("Found Preprocessor: %s"%entity.name)
