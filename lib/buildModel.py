from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
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
            X.append(row[1])
            hotClassifications = [0] * len(globalData.SENTIMENTS)
            hotClassifications[globalData.SENTIMENTS.index(row[0])] = 1
            Y.append(hotClassifications)

    maxFeatures = 2000
    maxWords = 400

    tokenizer = Tokenizer(num_words=maxFeatures, split=' ')
    tokenizer.fit_on_texts(X)
    X = tokenizer.texts_to_sequences(X)

    X = pad_sequences(X, maxlen=maxWords)

    trainingData = numpy.array(X)
    expectedOutput = numpy.array(Y)

    print(trainingData)

    # create model
    model = Sequential()
    model.add(Embedding(maxFeatures, 32, input_length=maxWords))
    model.add(Flatten())
    model.add(Dense(200, activation='relu'))
    model.add(Dense(len(globalData.SENTIMENTS), kernel_initializer = 'uniform', activation = 'softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(trainingData, expectedOutput, epochs = 200, batch_size = len(trainingData))

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
