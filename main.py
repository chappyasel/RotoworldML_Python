import sys
sys.path.append('./lib')
from buildModel import buildModelWithTrainingFiles
from testModel import testWithTestFiles
from testDataGenerator import generateTestData
from exportModel import exportToCoreML

buildModelWithTrainingFiles(['testData/testData1.csv', 'testData/testData2.csv'])

testModelWithTestFiles(['testData/testData3.csv'], verbose = True, writeToFile = False)

#generateTestData('testData/tempTestData.csv', num = 200, articleid = 340000) # 1 - 370,000 OR 0 for most recent
#testModelWithTestFiles(['testData/tempTestData.csv'], verbose = False, writeToFile = True)

#exportModelToCoreML('src/BTWorkoutClassification.mlmodel')
