from dbmodels import *
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
def CreatePyEntityParams(name, params, pyEntityId, experimentId):
    pyEntity = getPyEntityById(pyEntityId)
    exp = getExperimentById(experimentId)
    cls = PyEntityParams(name=name, params=params, py_entity=pyEntity, experiment=exp)
    commit()
    return cls.id

@db_session
def CreatePyEntityForExperiment(name, pyCode, params, experimentId, Type):
    cid = CreatePyClass(pyCode, name, params)
    enId = CreatePyEntity(name, Type, cid)
    enParamId = CreatePyEntityParams(name+"_params", params, enid, experimentId)
    return enParamId

@db_session
def ListPyEntityParamsOfExperiment(experimentId):
    exp = getExperimentById(experimentId)
    return exp.py_entity_paramss.select()[:] 

@db_session
def GetPyEntityFromParam(enParamId):
    pyPm = PyEntityParams.get(id=enParamId)
    pyPm.py_entity.load()
    return pyPm.py_entity

@db_session
def GetPyClassFromPyEntity(enId):
    pyPm = PyEntity.get(id=enId)
    pyPm.python_class.load()
    return pyPm.python_class
