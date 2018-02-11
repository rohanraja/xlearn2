from . import datapoint

from .iPyComponent import PyComponent

class PyComponentManager():

    @datapoint.db_session
    def GetPYComponentsForExperiment(self, experimentId):
        entityParams = datapoint.ListPyEntityParamsOfExperiment(experimentId) 
        outP = []
        for entityParam in entityParams:
            entity = datapoint.GetPyEntityFromParam(entityParam.id)
            pycls = datapoint.GetPyClassFromPyEntity(entity.id)
            pyComponent = PyComponent(entity.name, pycls.className, pycls.pycode, entityParam.params, entityParam.role)
            outP.append(pyComponent)

        return outP


pyComponentManager = PyComponentManager()
