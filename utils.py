import numpy
from xlearn2 import CONFIG
import os

def getProjectPath(path):

    return os.path.join(os.path.abspath(CONFIG["ProjectsPath"]) , path)

def getFullPathofLib(path):

    return os.path.join(os.path.abspath(CONFIG["LibraryPath"]) , path)

def dense_to_one_hot(labels_dense, num_classes=10):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = numpy.arange(num_labels) * num_classes
  labels_one_hot = numpy.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot

