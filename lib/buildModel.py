from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils import to_categorical
import pydot
import csv
import numpy
numpy.random.seed(1)
import globalData
globalData.init()


def buildModelWithTrainingFiles(trainingFiles):
    X, Y = [], []

    for fileName in trainingFiles:
        data = csv.reader(open(fileName))
        for row in data:
            bodySplit = row[0].split('#')
            intSplit = [0] * len(globalData.BODY_SPLITS)
            for split in bodySplit:
                arr = split.split(' ', 1)
                i = globalData.BODY_SPLITS.index(arr[1])
                intSplit[i] = arr[0]
            X.append(intSplit)
            hotClassifications = [0] * len(globalData.CLASSIFICATIONS)
            hotClassifications[globalData.CLASSIFICATIONS.index(row[1])] = 1
            Y.append(hotClassifications)

    trainingData = numpy.array(X)
    expectedOutput = numpy.array(Y)

    # create model
    model = Sequential()
    model.add(Dense(10, input_dim = len(globalData.BODY_SPLITS), kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(14, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(len(globalData.CLASSIFICATIONS), kernel_initializer = 'uniform', activation = 'softmax'))

    # Compile model
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    # Fit the model
    model.fit(trainingData, expectedOutput, epochs = 100000, batch_size = len(trainingData))

    # evaluate the model
    scores = model.evaluate(trainingData, expectedOutput)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    # serialize model to JSON
    model_json = model.to_json()
    with open("src/model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("src/model.h5")
    plot_model(model, to_file='src/model.png', show_shapes = True, show_layer_names = True)
    print("Saved model to disk")
