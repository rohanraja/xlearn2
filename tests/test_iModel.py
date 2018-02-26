import unittest
from testdata import mnist_model, mnist_dataset, mnist_lossfn, mnist_optimizer, mnist_trainstep
from xlearn2 import modeltrainer
import math


class TestIModelAndComponents(unittest.TestCase):

    batch_size = 50
    num_classes = 10


    def loadComponents(self):
        self.model = mnist_model.MnistModel()
        self.trainDataset = mnist_dataset.MnistDataset()
        self.optimizer = mnist_optimizer.MnistOptimizer()
        self.lossFunction = mnist_lossfn.MnistLossFn()
        self.modelTrainer = modeltrainer.ModelTrainer()
        self.trainStep = mnist_trainstep.MnistTrainStep()


    def attachComponents(self):
        self.modelTrainer.initialize(self.trainDataset, self.model, self.optimizer, self.lossFunction, self.trainStep)


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

        self.x, self.y = self.trainDataset.getSingleBatch(self.batch_size)
        yPred = self.model.Forward(self.x)
    
        loss = self.lossFunction.calcLoss(yPred, self.y)
        assert isinstance(loss.data[0], float)
        return loss

    def test_executing_forward_pass_on_network_and_compute_gradient(self):
        
        loss = self.test_executing_forward_pass_on_network_and_compute_loss()
        assert isinstance(loss.data[0], float)

        grads = self.model.GetGradients(loss)
        assert next(iter(grads)).shape[0] == 32


    def test_performing_single_training_step_and_check_that_loss_decreases(self):
        """
    Steps:
        1. Initialize Model, Dataset, Trainer, LossFunction
        2. Attach these components to ModelTrainer
        3. 
        """
        loss = self.test_executing_forward_pass_on_network_and_compute_loss()
        initialLoss = loss.data[0]

        assert isinstance(initialLoss, float)

        weights = self.model.GetWeights()
        grads = self.model.GetGradients(loss)

        newWeights = self.optimizer.calcTrainedWeights(weights, grads)

        self.model.SetWeights(newWeights)

        yPredNew = self.model.Forward(self.x)
        lossNew = self.lossFunction.calcLoss(yPredNew, self.y)
        newLoss = lossNew.data[0]

        print(newLoss, initialLoss)

        assert newLoss < initialLoss

    def test_extracting_model_weights(self):
        self.loadComponents()
        self.attachComponents()
        weights = self.model.GetWeights()
        firstWeight = next(iter(weights)) 
        assert firstWeight.shape[0] == 32

if __name__ == '__main__':
    unittest.main()
