from ..jobs import project
import trainer
from xlearn2.jobs import getDefaultParamsForModel
from xlearn2.jobs import getClassIndex
from xlearn2 import loadClass

def getActiveJobs(params):

    return trainer.getActiveJobs(params)

def getModelInfo(params):
    
    mid = params["modelId"]

    p = project.Project(str(mid))
    out = p.getJobInfo()

    return out

def getParamsInfo(params):
    
    mid = params["modelId"]
    pid = params["paramsId"]

    p = project.Project(str(mid))
    out = p.getParamsInfo(str(pid))

    return out

def delete_param(params):
    
    mid = params["modelId"]
    pid = params["paramsId"]

    p = project.Project(str(mid))
    out = p.delete_param(str(pid))

    return out
    

def createParamsInfo(params):

    mid = params["modelId"]
    pInfo = params["pInfo"]

    p = project.Project(str(mid))
    newPid = p.createParamsInfo(pInfo)

    return newPid

def createModelInfo(params):

    mInfo = params["mInfo"]
    pInfo = params["pInfo"]

    newMid = project.Project.createModelInfo(mInfo)
    
    p2 = {"modelId": newMid, "pInfo": pInfo}
    newPid = createParamsInfo(p2)

    return [newMid, newPid]

def getDatasetName(dataId):

    return dataId.split("/")[-1]

def loadDatasets(params):

    projects = project.Project.list()

    # projects = map(lambda p: project.Project(p).getJobInfo(), projects)
    
    outMap = {}

    for p in projects:
        pro = project.Project(p)
        pMap2 = pro.getJobInfo()
        pMap = {}
        pMap["id"] = p
        pMap["name"] = pMap2["name"] #.split("/")[-1] #getJobName(pro)
        pMap["params"] = pro.listJobs()

        pxmap = []
        for pp in pMap["params"]:
            pinfo = pro.getParamsInfo(pp)
            try:
                ppx = float(pinfo.get("ppx", 0.00))
                pxmap.append({pp: "%.2f"%ppx})
            except:
                pxmap.append({pp: "0.00"})

        pMap["params_px"] = pxmap 

        outMap[pMap2["dataset_id"]] = outMap.get(pMap2["dataset_id"], []) + [pMap]

    out = []
    for k in outMap:

        curr = {}
        curr["name"] = getDatasetName(k)
        curr["id"] = (k)
        curr["models"] = outMap[k]
        out.append(curr)

    return out


def start_training(params):

    trainer.start_training(params)

    return "Started Training"

def stop_training(params):

    trainer.stop_training(params)

    return "Stopped Training"

def get_epoch_list(params):

    return trainer.get_epoch_list(params)




def start_evaluation(params):

    return evaluate.start_evaluation(params)

def Test_sentance(params):

    return evaluate.test_sentance(params)

def Test_sentance_prediction(params):

    return evaluate.predict_next_words(params)

def generate_sequence(params):

    return evaluate.generate_sequence(params)

def predict_word_embedding(params):

    return evaluate.predict_word_embedding(params)

def mappers_list(params):
    
    out = []
    
    arr = getClassIndex("mapper")

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = k
        out.append(obj)

    return out

def get_mapper_stats(params):
    jinfo = getModelInfo(params)

    DS = loadClass(jinfo["dataset_id"])
    data = DS()
    M = loadClass(jinfo["mapper_id"])
    m = M(data)

    return m.getstats()

def dataset_list(params):
    
    out = []
    
    arr = getClassIndex("dataset")

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = k # arr[k].__name__
        out.append(obj)

    return out
def search_dataset(params):

    jinfo = getModelInfo(params)
    DS = loadClass(jinfo["dataset_id"])
    data = DS()
    phrase = params["phrase"]

    return data.search(phrase)



def models_list(params):
    
    out = []
    
    arr = getClassIndex("model")

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = k
        obj["params"] = getDefaultParamsForModel(k)

        out.append(obj)

    return out


def embeddings_list(params):
    
    out = []
    
    arr = getClassIndex("embedding")

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = k
        out.append(obj)

    return out



def add_dataset(params):

    fname = params['fname']
    addOtherFiles(fname)
