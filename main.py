import sys
sys.path.append('./lib')
from buildModel import buildModelWithTrainingFiles
from testModel import testWithTestFiles
from testDataGenerator import generateTestData
from exportModel import exportToCoreML

#buildModelWithTrainingFiles(['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv', 'testData/testData4.csv'])

#testWithTestFiles(['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv', 'testData/testData4.csv'], True, False)

generateTestData('testData/tempTestData.csv', 200)
#testWithTestFiles(['testData/tempTestData.csv'], False, True)

#exportToCoreML('src/BTWorkoutClassification.mlmodel')
