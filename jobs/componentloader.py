import json
import sys
import os
from xlearn2 import getFullPathofLib
from os import listdir

def readClassFromPyFile(pyDir, pyFileName, className):
    sys.path.insert(0, os.path.abspath(pyDir))
    mod = __import__(pyFileName)
    cls = getattr(mod, className)
    return cls

def loadClass(classJsonPath):

    cInfo = ClassInfo(classJsonPath)
    cls = cInfo.getClassFactory()
    return cls


class ClassInfo:
    def __init__(self, classJsonPath):
        modelPath = getFullPathofLib(classJsonPath)
        modelJsonPath = os.path.join(modelPath, "classInfo.json")
        self.modelPath = modelPath
        self.jsonData = json.load(open(modelJsonPath))
        self.parseJson()

    def parseJson(self):
        self.modelPyFile = self.jsonData["pyFileName"]
        self.modelClassName = self.jsonData["pyClassName"]

    def getDefaultParams(self):
        return self.jsonData["DefaultParams"]

    def getClassFactory(self):
        self.Cls = readClassFromPyFile(self.modelPath, self.modelPyFile, self.modelClassName)
        return self.Cls


def getDefaultParamsForModel(modelId):
    cInfo = ClassInfo(modelId)
    return cInfo.getDefaultParams()


def getClassIndex(clsName):

    try:
        itemsPath = getFullPathofLib(clsName)
        items = listdir(itemsPath)
        out = []
        for i in items:
            out.append("%s/%s" % (clsName, i) )
        return out
    except:
        return []

class ComponentsLoader():
    
    def loadComponents(self):

        print "Loading Dataset"
        self.loadDataset()   # self.dataset contains the final dataset
        print "Loading Mapper"
        self.loadMapper()    
        print "Loading Embedding"
        self.loadEmbedding()     
        print "Loading Model"
        self.loadModel()     # self.model contains the final model



    def loadMapper(self):
        if "mapper_id" not in self.jinfo:
            return
        M = loadClass(self.jinfo["mapper_id"])
        self.mapper = M(self.dataset)
        # self.mapper_test = M(self.dataset_test, False)

    def loadTestMapper(self, dataset_id, num):
        DS = loadClass(dataset_id)
        try:
            nums = num.split(' ')
            print nums
            dataset_test = DS(int(nums[0]),int(nums[1]))
        except Exception, e:
            print e
            dataset_test = DS()
        M = mappersIndex.get(self.jinfo["mapper_id"])
        self.mapper_test = M(dataset_test)

        # dataset_test = DS(3000, int(num))
        # self.X_test, self.Y_test = self.mapper.getXY(dataset_test)
        self.X_test = self.mapper_test.X
        self.Y_test = self.mapper_test.Y
        # M = mappersIndex.get(self.jinfo["mapper_id"])
        # self.mapper_test = M(dataset_test)

    def loadDataset(self):
        DS = loadClass(self.jinfo["dataset_id"])
        self.dataset = DS()
    

    def loadModel(self):
        modelClass = loadClass(self.jinfo["model_id"])
        try:
            if self.params == {}:
                self.params = modelClass.defaultParams()
        except:
            pass
        self.params["jobDir"] = self.jobDir
        self.params["jinfo"] = self.jinfo
        self.model = modelClass(self.params)
        self.model.jobDir = self.jobDir
        self.model.jinfo = self.jinfo

    def loadEmbedding(self):
        if "embedding_id" not in self.jinfo:
            return
        try:
            E = loadClass(self.jinfo["embedding_id"])
            self.embedding = E(self.mapper)
            self.params["embedding"] = self.embedding
        except Exception, e:
            print e
            pass

    def loadWeights(self):
        return []

    def loadHyperparams(self):
        return []


