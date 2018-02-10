import unittest
from xlearn2 import componentloader
from xlearn2 import config

DATASET_PYFILE = "testdata/mnist_dataset.py"
DATASET_CLASS_NAME = "MnistDataset"

class MockDataPoint:

    def ListPyEntityParamsOfExperiment(self, expId):
        return []


def readPyCodeFromFile(fName):
    f = open(fName, 'r')
    outP = f.read()
    f.close()
    return outP

class TestLoadingPYEntites(unittest.TestCase):
    def test_loading_dataset_from_pycode_text(self):

        pyCode = readPyCodeFromFile(DATASET_PYFILE)
        print(pyCode)
        DS_CLASS = componentloader.loadPyClassFromPyCode(pyCode, DATASET_CLASS_NAME)
        print(DS_CLASS)
        obj = DS_CLASS()
        assert obj.__class__.__name__ == DATASET_CLASS_NAME

    def test_components_loader(self):

      mockDP = MockDataPoint()
      c = componentloader.ComponentsLoader()
      c.experimentId = 1
      c.loadComponents()

      print(c.Components)
      assert len(c.Components[config.MODEL_TYPE]) == 1
      assert DATASET_CLASS_NAME == c.train_dataset.__class__.__name__
      assert DATASET_CLASS_NAME == c.test_dataset.__class__.__name__


if __name__ == '__main__':
    unittest.main()
