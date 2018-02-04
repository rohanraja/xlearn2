from pony.orm import *


db = Database()


class Project(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    experiments = Set('Experiment')


class Experiment(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    project = Required(Project)
    trained_weights = Set('TrainedWeight')
    epoch = Optional(int)
    hyperparams = Optional(str)
    py_entities = Set('PyEntity')


class TrainedWeight(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    experiment = Required(Experiment)
    binary_file = Optional('BinaryFile')


class BinaryFile(db.Entity):
    id = PrimaryKey(int, auto=True)
    filepath = Optional(str)
    trained_weight = Required(TrainedWeight)


class PyEntity(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    python_class = Required('PythonClass')
    Type = Optional(int)
    experiments = Set(Experiment)


class PythonClass(db.Entity):
    id = PrimaryKey(int, auto=True)
    pycode = Optional(str)
    className = Optional(str)
    defaultParams = Optional(str)
    pyentity = Optional(PyEntity)


db.bind(provider='sqlite', filename='xlearn.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
