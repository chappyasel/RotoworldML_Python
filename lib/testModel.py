
from keras.models import model_from_json
import csv
import numpy
import globalData
globalData.init()

def testWithTestFiles(fileNames, verbose, writeToFile):
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
            bodySplit = row[0].split('#')
            intSplit = [0] * len(globalData.BODY_SPLITS)
            for split in bodySplit:
                arr = split.split(' ', 1)
                i = globalData.BODY_SPLITS.index(arr[1])
                intSplit[i] = arr[0]
            testingData.append(intSplit)
            if (len(row) > 1):
                hotClassifications = [0] * len(globalData.CLASSIFICATIONS)
                hotClassifications[globalData.CLASSIFICATIONS.index(row[1])] = 1
                expectedOutput.append(hotClassifications)
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
                    print fileName, i+1, globalData.CLASSIFICATIONS[pred], '  --should be->  ', globalData.CLASSIFICATIONS[actl], '   certainty:', predictions[i][pred] * 100
                if writeToFile:
                    f.write(row[0] + ',' + globalData.CLASSIFICATIONS[pred] + ',' + str(predictions[i][pred] * 100)[:4] + '\n')
        else:
            i = 0
            for row in csv.reader(open(fileName)):
                pred = predictions[i].argmax(axis = 0)
                if verbose:
                    print i+1, row[0], '  --guess->  ', globalData.CLASSIFICATIONS[pred], '   certainty:', predictions[i][pred] * 100
                if writeToFile:
                    f.write(row[0] + ',' + globalData.CLASSIFICATIONS[pred] + ',' + str(predictions[i][pred] * 100)[:4] + '\n')
                i += 1

    if total:
        print("*********************************************** Actual accuracy: %.2f%%" % (float(numCorrect) / total * 100))
