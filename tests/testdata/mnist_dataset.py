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


    def getXYGen(self, batch_size=50):
        self.train_loader = torch.utils.data.DataLoader(
            datasets.MNIST('data', train=True, download=True, transform=transforms.ToTensor()),
            batch_size=batch_size, shuffle=True)
        return self.train_loader

    def getSingleBatch(self, batch_size=50):
        batchGen = self.getXYGen(batch_size)
        return iter(batchGen).next()

