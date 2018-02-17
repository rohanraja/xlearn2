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
        """
    Steps:
        1. Initialize Model, Dataset, Trainer, LossFunction
        2. Attach these components to ModelTrainer
        3. Start training in a new thread
        """

        # Step 1.
        self.loadComponents()

        # Step 2.
        self.attachComponents()

        # Step 3.
        trainerThread = threading.Thread(target=self.modelTrainer.StartTraining)
        trainerThread.daemon = True
        trainerThread.start()

        # Step 4. Let it train for some time
        time.sleep(3)

        assert trainerThread.isAlive() is True

        # Step 5. Stop the training thread
        self.modelTrainer.StopTraining()

        # Step 6. Wait for the trainer to stop
        time.sleep(2)

        # Step 7. Check if trainer thread has exited
        assert trainerThread.isAlive() is False


if __name__ == '__main__':
    unittest.main()
