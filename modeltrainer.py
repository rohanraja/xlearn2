from types import MethodType


def train_step(self, x, y):

    yPred = self.Forward(x)
    loss = self.lossFunction.calcLoss(yPred, y)
    weights = self.GetWeights()
    grads = self.GetGradients(loss)
    newWeights = self.optimizer.calcTrainedWeights(weights, grads)
    self.SetWeights(newWeights)
    return loss

class ModelTrainer():

    def initialize(self, trainDataset, model, optimizer, lossFunction):
        self.trainDataset = trainDataset
        self.model = model
        self.optimizer = optimizer
        self.lossFunction = lossFunction

        self.batch_size = 50

        
    def prepareModelForTraining(self):
        self.model.optimizer = self.optimizer
        self.model.lossFunction = self.lossFunction

        if not hasattr(self.model, "train_step"):
            self.model.train_step = MethodType(train_step, self.model)

    def getTrainingBatches(self):
        return self.trainDataset.getXYGen(self.batch_size)

    def updateTrainingStatus(self, loss):
        print(loss)

    def StartTraining(self):

        losses = []
        allBatches = self.getTrainingBatches()
        self.prepareModelForTraining()
        for xBatch, yBatch in allBatches:
            loss = self.model.train_step(xBatch, yBatch)
            self.updateTrainingStatus(loss)
            losses.append(loss)

        return losses
