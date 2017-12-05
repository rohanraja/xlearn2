import unittest
from xlearn2.jobs import createProject, loadJob
from xlearn2 import getProjectPath
import os
from shutil import rmtree

class TestCreateProject(unittest.TestCase):
    def test_load_job(self):
        j = loadJob("testProject")

    def test_create_project(self):
        pName = "testProject"
        jobdir = getProjectPath(pName)
        rmtree(jobdir)
        model = "model/mnist_cnn"
        dataset = "dataset/mnist"

        assert not os.path.isdir(jobdir)
        createProject(pName, model, dataset)
        assert os.path.isdir(jobdir)

if __name__ == '__main__':
    unittest.main()
