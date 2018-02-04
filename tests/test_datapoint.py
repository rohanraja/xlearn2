import unittest
from xlearn2 import datapoint, config
from pony.orm import db_session

PROJECT_NAME = "mnist_test"
EXP_NAME = "mnist_experiment_1"
EXP_ID = 1

MODEL_PYFILE = "testdata/mnist_model.py"
MODEL_NAME = "MnistModel"
MODEL_PARAMS = "{}"
DATASET_PYFILE = "testdata/mnist_dataset.py"
DATASET_NAME = "MnistDataset"
DATASET_PARAMS = "{}"

def readPyCodeFromFile(fName):
  f = open(fName, 'r')
  outP = f.read()
  f.close()
  return outP

class TestListAllProjects(unittest.TestCase):
    def test_list_all_projects(self):
        pros = datapoint.ListAllProjects()
        fount_test_project = False
        fount_test_experiment = False
        print("\n\nProjects:")
        for p in pros:
            if p.name == PROJECT_NAME:
                fount_test_project = True
            print(p.name)
            for exp in datapoint.ListExperimentsOfProject(p.id):
                print("Experiment: " + exp.name)
                if exp.name == EXP_NAME:
                    fount_test_experiment = True

        assert fount_test_project
        assert fount_test_experiment

    def test_adding_mnist_experiment_data(self):
        for p in datapoint.ListAllProjects():
            if p.name == PROJECT_NAME:
                assert True
                print("Test Project already present")
                return
            
        print("Creating MNIST test experiment data")

        pid = datapoint.CreateProject(PROJECT_NAME)
        print("Project ID: ", pid)
        eid = datapoint.CreateExperiment(pid, EXP_NAME)
        print("Experiment ID: ", eid)
        
        modelPyCode = readPyCodeFromFile(MODEL_PYFILE)
        datasetPyCode = readPyCodeFromFile(DATASET_PYFILE)

        model_cid = datapoint.CreatePyClass(modelPyCode, MODEL_NAME, MODEL_PARAMS)
        print("MODEL CLASS ID: ", model_cid)

        dataset_cid = datapoint.CreatePyClass(datasetPyCode, DATASET_NAME, DATASET_PARAMS)
        print("DATASET CLASS ID: ", dataset_cid)

        model_entity = datapoint.CreatePyEntity(MODEL_NAME, 0, model_cid)
        print("MODEL PYENTITY ID: ", model_entity)
        dataset_entity = datapoint.CreatePyEntity(DATASET_NAME, 1, dataset_cid)
        print("DATASET PYENTITY ID: ", dataset_entity)

        model_entityParams = datapoint.CreatePyEntityParams(MODEL_NAME+"_testParams", MODEL_PARAMS, model_entity, eid)
        print("MODEL PYENTITYPARAMS ID: ", model_entityParams)

        dataset_entityParams = datapoint.CreatePyEntityParams(DATASET_NAME+"_trainParams", DATASET_PARAMS, dataset_entity, eid)
        print("DATASET PYENTITYPARAMS ID: ", dataset_entityParams)

        testParamId = datapoint.CreatePyEntityParams(DATASET_NAME+"_testParams", DATASET_PARAMS, dataset_entity, eid, config.TEST_TYPE)
        print("TEST DATASET PYENTITYPARAMS ID: ", testParamId)


    def test_listing_experiment_entities(self):

      ens = datapoint.ListPyEntityParamsOfExperiment(EXP_ID)
      pyen = datapoint.GetPyEntityFromParam(ens[0].id)
      print("\nEntity Name: " + pyen.name)
      pycls = datapoint.GetPyClassFromPyEntity(pyen.id)
      if pyen.Type == 0:
          print("PyClass Name: " + pycls.className)
          assert pycls.className == MODEL_NAME
      assert "__init__" in pycls.pycode

       


if __name__ == '__main__':
    unittest.main()
