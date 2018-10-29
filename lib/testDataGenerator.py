
import urllib, json
import globalData
globalData.init()

def rotoLinkForOffset(offset):
    return "http://www.rotoworld.com/services/mobile.asmx/GetNews?articleid=" + str(offset) + "&sport=NBA&token=m1rw-xor-434s-bbjt-1"

def generateTestData(fileName, num):
    url = rotoLinkForOffset(0)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    arr = []
    for d in data:
        arr.append(d['NEWS'] + " " + d['ANALYSIS'])
    # with open(fileName, 'w') as f:
    #     for i in range(num):
    #         result = []
    #         for i in range(random.choice([1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5])):
    #             split = random.choice(globalData.BODY_SPLITS)
    #             if not contains(result, split):
    #                 result.append(str(random.choice([1, 1, 2, 2, 2, 3, 3, 4])) + ' ' + split)
    #         f.write('#'.join(result)+'\n')

def contains(list, string):
    for i in list:
        if string in i:
            return True
    return False
