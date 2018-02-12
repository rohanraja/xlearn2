import unittest
from testdata import mnist_model, mnist_dataset, mnist_lossfn, mnist_optimizer
from xlearn2 import modeltrainer
import math
from types import MethodType
import threading
import time


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
        3. Inject Mock method to train only single batch
        4. Train and compute loss
        5. Check that loss decreases during 2nd run
        """
        # Step 1.
        self.loadComponents()

        # Step 2.
        self.attachComponents()
        
        # Step 3.
        x, y = self.trainDataset.getSingleBatch(self.batch_size)
        batches = [(x,y) , (x,y)]
        def tempFun(self):
          return batches
        self.modelTrainer.getTrainingBatches = MethodType(tempFun, self.modelTrainer)

        # Step 4.
        losses = self.modelTrainer.StartTraining()[0]
        losses2 = self.modelTrainer.StartTraining()[0]

        # Step 5.
        assert losses.data[0] > losses2.data[0]

    def test_starting_long_training_and_stopping_training(self):
        # Step 1.
        self.loadComponents()

        # Step 2.
        self.attachComponents()
        
        # Step 3.
        x, y = self.trainDataset.getSingleBatch(self.batch_size)

        # Step 4.
        trainerThread = threading.Thread(target=self.modelTrainer.StartTraining)
        trainerThread.daemon = True
        trainerThread.start()

        # Let it train for some time
        time.sleep(5)

        assert trainerThread.isAlive() == True

        # Stop the training thread
        self.modelTrainer.StopTraining()

        # Wait for the trainer to stop
        time.sleep(2)

        assert trainerThread.isAlive() == False


if __name__ == '__main__':
    unittest.main()
