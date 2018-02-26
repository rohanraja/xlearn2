from types import MethodType


def train_step(self, model, batch, lossFunction, optimizer):

    x = batch[0]
    y = batch[1]
    yPred = model.Forward(x)
    loss = lossFunction.calcLoss(yPred, y)
    weights = model.GetWeights()
    grads = model.GetGradients(loss)
    newWeights = optimizer.calcTrainedWeights(weights, grads)
    model.SetWeights(newWeights)
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
            self.train_step = MethodType(train_step, self)
        else:
            self.train_step = MethodType(self.model.train_step, self)

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
            loss = self.train_step(self.model, batch, self.lossFunction, self.optimizer)
            self.updateTrainingStatus(loss)
            losses.append(loss)

        return losses


    def StopTraining(self):

        self.StopExecutionFlag = True


    # def SelectWeights
