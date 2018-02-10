import unittest
from testdata import mnist_model, mnist_dataset, mnist_lossfn
from xlearn2 import modeltrainer
import math


class TestStartTraining(unittest.TestCase):

    batch_size = 50
    num_classes = 10


    def loadComponents(self):
        self.model = mnist_model.MnistModel()
        self.trainDataset = mnist_dataset.MnistDataset()
        self.optimizer = None
        self.lossFunction = mnist_lossfn.MnistLossFn()
        self.modelTrainer = modeltrainer.ModelTrainer()


    def attachComponents(self):
        self.modelTrainer.initialize(self.trainDataset, self.model, self.optimizer, self.lossFunction)


    def test_executing_forward_pass_on_model_and_check_output(self):
        self.loadComponents()
        self.attachComponents()

        x, y = self.trainDataset.getSingleBatch(self.batch_size)
        assert x.shape[2] == 28
        assert x.shape[0] == self.batch_size
        yPred = self.model.Forward(x)
        assert yPred.shape[0] ==self.batch_size
        assert yPred.shape[1] ==self.num_classes
        yForVal = (yPred[0].exp().sum().data[0])
        assert math.isclose(yForVal, 1, rel_tol=1e-5, abs_tol=0.0)



    def test_executing_forward_pass_on_network_and_compute_loss(self):
        self.loadComponents()
        self.attachComponents()

        x, y = self.trainDataset.getSingleBatch(self.batch_size)
        yPred = self.model.Forward(x)

        loss = self.lossFunction.calcLoss(yPred, y)
        assert isinstance(loss.data[0], float)


    def test_performing_single_training_step_and_check_that_loss_decreases(self):
        """
    Steps:
        1. Initialize Model, Dataset, Trainer, LossFunction
        2. Attach these components to ModelTrainer
        3. 
        """
        assert True 

if __name__ == '__main__':
    unittest.main()
