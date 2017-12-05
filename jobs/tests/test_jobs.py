import unittest
from xlearn2.jobs import componentloader, Job
import numpy as np
import tensorflow as tf

class TestJobLoading(unittest.TestCase):

    def test_loading_job(self):
        jDir = "0/0"
        jInfo = {
                "dataset_id": "dataset/mnist",
                "model_id": "model/mnist_cnn"
        }
        params = {}
        j = Job(jDir, jInfo, params)

        tf.reset_default_graph()

    def test_loading_dataset(self):
        clsPath = "dataset/mnist"
        c = componentloader.loadClass(clsPath)
        obj = c()
        assert obj.canTrain() == False

    def test_loading_model(self):
        clsPath = "model/mnist_cnn"
        c = componentloader.loadClass(clsPath)
        obj = c(c.defaultParams())
        assert obj.canTrain() == False

        tf.reset_default_graph()

if __name__ == '__main__':
    unittest.main()
