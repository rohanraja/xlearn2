import unittest
from xlearn2 import datapoint

PROJECT_NAME = "mnist_test"
EXP_NAME = "mnist_experiment_1"

class TestListAllProjects(unittest.TestCase):
    def test_list_all_projects(self):
        pros = datapoint.ListAllProjects()
        print("\n\nProjects:")
        for p in pros:
            print(p.name)
            for exp in datapoint.ListExperimentsOfProject(p.id):
              print("Experiment: ", exp.name)
        assert len(pros) > 0

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

if __name__ == '__main__':
    unittest.main()
