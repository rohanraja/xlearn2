import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from colorama import Fore


class MnistLossFn():

    def __init__(self, hyperParams={}):

        print(Fore.MAGENTA+ "Initializing MNIST LOSS FUNCTION Instance"+ Fore.WHITE)
        self.params = hyperParams

    def calcLoss(self, yPred, yTrue):
        loss = F.nll_loss(yPred, Variable(yTrue) )
        return loss
