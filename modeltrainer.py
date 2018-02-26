class ModelTrainer():

    def initialize(self, trainDataset, model, optimizer, lossFunction, trainStep):
        self.trainDataset = trainDataset
        self.model = model
        self.optimizer = optimizer
        self.lossFunction = lossFunction
        self.trainStep = trainStep

        self.batch_size = 50
        self.StopExecutionFlag = False


    def getTrainingBatches(self):
        return self.trainDataset.getXYGen(self.batch_size)

    def updateTrainingStatus(self, loss):
        print(loss.data[0])

    def StartTraining(self):

        losses = []
        allBatches = self.getTrainingBatches()
        for batch in allBatches:
            if self.StopExecutionFlag:
                break
            if not hasattr(self.model, "trainStep"):
                loss = self.trainStep.step(self.model, batch, self.lossFunction, self.optimizer)
            else:
                loss = self.model.trainStep(self.model, batch, self.lossFunction, self.optimizer)
            self.updateTrainingStatus(loss)
            losses.append(loss)

        return losses


    def StopTraining(self):

        self.StopExecutionFlag = True


    # def SelectWeights
