import sys
sys.path.append('./lib')
from buildModel import buildModelWithTrainingFiles
from testModel import testWithTestFiles
from testDataGenerator import generateTestData
from exportModel import exportToCoreML

#buildModelWithTrainingFiles(['testData/testData1.csv'])

#testWithTestFiles(['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv', 'testData/testData4.csv'], True, False)

generateTestData('testData/tempTestData.csv', 500, 330000) # 1 - 370,000 OR 0 for most recent
testWithTestFiles(['testData/tempTestData.csv'], False, True)

#exportToCoreML('src/BTWorkoutClassification.mlmodel')
