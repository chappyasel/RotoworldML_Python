from keras.models import Sequential, model_from_json
from keras.layers import Embedding, Dense, Flatten, LSTM
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import plot_model
import urllib
import pydot
import csv
import json
import numpy
numpy.random.seed(1)
import globalData
globalData.init()


def buildModelWithTrainingFiles(trainingFiles):
    X, Y = [], []

    for fileName in trainingFiles:
        for row in csv.reader(open(fileName)):
            X.append(row[1])
            hotClassifications = [0] * len(globalData.SENTIMENTS)
            hotClassifications[globalData.SENTIMENTS.index(row[0])] = 1
            Y.append(hotClassifications)

    X = globalData.cleanArticles(X)

    tokenizer = Tokenizer(num_words=globalData.MAX_FEATURES, split=' ')
    tokenizer.fit_on_texts(X)
    tokenDict = {k : v for k, v in tokenizer.word_index.iteritems() if v <= globalData.MAX_FEATURES - 1}

    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=globalData.MAX_WORDS)

    trainingData = numpy.array(X)
    expectedOutput = numpy.array(Y)

    embed_dim = 32

    # create model
    model = Sequential()
    model.add(Embedding(globalData.MAX_FEATURES, embed_dim, input_length=globalData.MAX_WORDS))
    model.add(LSTM(100))
    model.add(Dense(len(globalData.SENTIMENTS), kernel_initializer = 'uniform', activation = 'softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit model
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

    # serialize token dict to JSON
    with open("src/token_dict.json", "w") as token_file:
        token_file.write(json.dumps(tokenDict))

    print("Saved model to disk")
