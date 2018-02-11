import unittest
from testdata import mnist_model, mnist_dataset, mnist_lossfn, mnist_optimizer
from xlearn2 import modeltrainer
import math
from types import MethodType


class TestModelTrainer(unittest.TestCase):

    batch_size = 50
    num_classes = 10


    def loadComponents(self):
        self.model = mnist_model.MnistModel()
        self.trainDataset = mnist_dataset.MnistDataset()
        self.optimizer = mnist_optimizer.MnistOptimizer()
        self.lossFunction = mnist_lossfn.MnistLossFn()
        self.modelTrainer = modeltrainer.ModelTrainer()


    def attachComponents(self):
        self.modelTrainer.initialize(self.trainDataset, self.model, self.optimizer, self.lossFunction)


    def test_performing_single_training_step_and_check_that_loss_decreases(self):
        """
    Steps:
        1. Initialize Model, Dataset, Trainer, LossFunction
        2. Attach these components to ModelTrainer
        3. 
        """
        self.loadComponents()
        self.attachComponents()
        x, y = self.trainDataset.getSingleBatch(self.batch_size)
        batches = [(x,y) , (x,y)]

        def tempFun(self):
          return batches

        # Injecting Mock method
        self.modelTrainer.getTrainingBatches = MethodType(tempFun, self.modelTrainer)

        losses = self.modelTrainer.StartTraining()[0]
        losses2 = self.modelTrainer.StartTraining()[0]

        assert losses.data[0] > losses2.data[0]




if __name__ == '__main__':
    unittest.main()
