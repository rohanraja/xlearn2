import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from colorama import Fore


class MnistDataset():

    def __init__(self, hyperParams={}):

        print(Fore.YELLOW+ "Initializing MNIST Dataset Instance"+ Fore.WHITE)
        self.params = hyperParams
