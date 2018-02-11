from .dbmodels import *
from pony.orm import *

# set_sql_debug(True)

@db_session
def ListAllProjects():
    return Project.select()[:]

@db_session
def GetProjectById(projectId):
    p = Project.get(id=projectId)
    return p

@db_session
def ListExperimentsOfProject(projectId):
    p = GetProjectById(projectId)
    return p.experiments.select()[:]


@db_session
def CreateProject(projectName):
    p = Project(name=projectName)
    commit()
    return p.id

@db_session
def CreateExperiment(projectId, expName):
    p = GetProjectById(projectId)
    e = Experiment(name=expName, project=p)
    commit()
    return e.id

@db_session
def getExperimentById(expId):
    p = Experiment.get(id=expId)
    return p

@db_session
def CreatePyClass(pyCode, className, defParams):
    cls = PythonClass(className=className, pycode=pyCode, defaultParams=defParams)
    commit()
    return cls.id

@db_session
def getPyClassById(clsId):
    p = PythonClass.get(id=clsId)
    return p

@db_session
def getPyEntityById(clsId):
    p = PyEntity.get(id=clsId)
    return p

@db_session
def CreatePyEntity(name, entityType, pyClassId):
    pyClass = getPyClassById(pyClassId)
    cls = PyEntity(name=name, Type=entityType, python_class=pyClass)
    commit()
    return cls.id

@db_session
def CreatePyEntityParams(name, params, pyEntityId, experimentId, role=-1):

    pyEntity = getPyEntityById(pyEntityId)

    if role == -1:
        role = pyEntity.Type

    exp = getExperimentById(experimentId)
    cls = PyEntityParams(name=name, params=params, py_entity=pyEntity, experiment=exp, role=role)
    commit()
    return cls.id

@db_session
def CreatePyEntityForExperiment(name, pyCode, params, experimentId, Type, role=-1):
    if role == -1:
        role = Type

    cid = CreatePyClass(pyCode, name, params)
    enId = CreatePyEntity(name, Type, cid)
    enParamId = CreatePyEntityParams(name+"_params", params, enId, experimentId, role)
    return enParamId

@db_session
def ListPyEntityParamsOfExperiment(experimentId):
    exp = getExperimentById(experimentId)
    outP = exp.py_entity_paramss.select()[:] 
    # for epm in outP:
    #     epm.py_entity.load()
    #     epm.py_entity.python_class.load()
    return outP


@db_session
def GetPyEntityFromParam(enParamId):
    pyPm = PyEntityParams.get(id=enParamId)
    pyId = pyPm.py_entity.id
    outP = PyEntity[pyId]
    outP.load()
    return outP

@db_session
def GetPyClassFromPyEntity(enId):
    pyPm = PyEntity.get(id=enId)
    pyPm.python_class.load()
    return pyPm.python_class

@db_session
def ListPyEntitiesOfExperiment(experimentId):
    enParams = ListPyEntityParamsOfExperiment(experimentId)
    outP = list(map(lambda x: GetPyEntityFromParam(x.id) , enParams))
    return outP

