import unittest
from testdata import mnist_dataset


class TestIDataset(unittest.TestCase):

    batch_size = 45
    imageDimX = 28
    imageDimY = 28

    def loadComponents(self):
        self.trainDataset = mnist_dataset.MnistDataset()

    def test_extracting_batch_from_trainng_dataset(self):
        """
      Steps:
        1. Initialize Dataset
        2. Get Batch Generator 
        3. Extract single batch
        4. Check if the shapes of the tensors are correct
        """

        # Step 1.
        self.loadComponents()

        # Step 2,3
        xTrain, yTrain = self.trainDataset.getSingleBatch(self.batch_size)

        # Step 4.
        assert xTrain.shape[0] == self.batch_size
        assert yTrain.shape[0] == self.batch_size
        assert xTrain.shape[2] == self.imageDimX
        assert xTrain.shape[3] == self.imageDimY


if __name__ == '__main__':
    unittest.main()
