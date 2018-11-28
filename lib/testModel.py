from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
import csv
import numpy
import globalData
import json
globalData.init()

def testModelWithTestFiles(fileNames, verbose, writeToFile):
    # load json and create model
    json_file = open('src/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("src/model.h5")
    print("Loaded model from disk")

    total, numCorrect = 0, 0

    for fileName in fileNames:
        testingData, expectedOutput = [], []

        for row in csv.reader(open(fileName)):
            testingData.append(row[1])
            if not writeToFile:
                hotClassifications = [0] * len(globalData.SENTIMENTS)
                hotClassifications[globalData.SENTIMENTS.index(row[0])] = 1
                expectedOutput.append(hotClassifications)

        # tokenize articles using saved token dict
        testingData = globalData.cleanArticles(testingData)
        tokenDict = json.loads(open('src/token_dict.json').read())
        testingData = map(lambda x: tokenize(x, tokenDict), testingData)
        testingData = pad_sequences(testingData, maxlen=globalData.MAX_WORDS)

        # calculate predictions
        predictions = model.predict(numpy.array(testingData))
        f = open('testData/resultData.csv', 'w')
        if (len(expectedOutput) > 0):
            for i in range(len(predictions)):
                pred = predictions[i].argmax(axis = 0)
                actl = expectedOutput[i].index(1)
                total += 1
                if pred == actl:
                    numCorrect += 1
                elif verbose:
                    print fileName, i+1, ':   ', globalData.SENTIMENTS[pred], '  --should be->  ', globalData.SENTIMENTS[actl], '   certainty:', predictions[i][pred] * 100
                if writeToFile:
                    f.write(globalData.SENTIMENTS[pred] + ',' + row[1] + ',' + str(predictions[i][pred] * 100)[:4] + '\n')
        else:
            i = 0
            for row in csv.reader(open(fileName)):
                pred = predictions[i].argmax(axis = 0)
                if verbose:
                    print i+1, ':   ', row[0], '  --guess->  ', globalData.SENTIMENTS[pred], '   certainty:', predictions[i][pred] * 100
                if writeToFile:
                    article = '"' + row[1].replace('&quot;', '\'') + '"'
                    f.write(globalData.SENTIMENTS[pred] + ',' + article + ',' + str(predictions[i][pred] * 100)[:4] + '\n')
                i += 1

    if total:
        print("*************************************************************** Actual accuracy: %.2f%%" % (float(numCorrect) / total * 100))

def tokenize(article, dict):
    words = article.lower().split(' ')
    tokenized = []
    for word in words:
        if dict.get(word) != None:
            tokenized.append(dict[word])
        else:
            tokenized.append(0)
    return tokenized
