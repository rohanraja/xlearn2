from types import MethodType


def train_step(self, batch, lossFunction, optimizer):

    x = batch[0]
    y = batch[1]
    yPred = self.Forward(x)
    loss = lossFunction.calcLoss(yPred, y)
    weights = self.GetWeights()
    grads = self.GetGradients(loss)
    newWeights = optimizer.calcTrainedWeights(weights, grads)
    self.SetWeights(newWeights)
    return loss

class ModelTrainer():

    def initialize(self, trainDataset, model, optimizer, lossFunction):
        self.trainDataset = trainDataset
        self.model = model
        self.optimizer = optimizer
        self.lossFunction = lossFunction

        self.batch_size = 50
        self.StopExecutionFlag = False

        
    def prepareModelForTraining(self):

        if not hasattr(self.model, "train_step"):
            self.model.train_step = MethodType(train_step, self.model)

    def getTrainingBatches(self):
        return self.trainDataset.getXYGen(self.batch_size)

    def updateTrainingStatus(self, loss):
        print(loss.data[0])

    def StartTraining(self):

        losses = []
        allBatches = self.getTrainingBatches()
        self.prepareModelForTraining()
        for batch in allBatches:
            if self.StopExecutionFlag:
                break
            loss = self.model.train_step(batch, self.lossFunction, self.optimizer)
            self.updateTrainingStatus(loss)
            losses.append(loss)

        return losses


    def StopTraining(self):

        self.StopExecutionFlag = True


    # def SelectWeights
