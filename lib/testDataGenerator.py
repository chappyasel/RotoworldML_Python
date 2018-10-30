
import urllib, json
import globalData
globalData.init()

def rotoLinkForOffset(offset):
    return 'http://www.rotoworld.com/services/mobile.asmx/GetNews?articleid=' + str(offset) + '&sport=NBA&token=m1rw-xor-434s-bbjt-1'

def generateTestData(fileName, num):
    arr = []
    lastOffset = 0
    for i in range(num / 50):
        url = rotoLinkForOffset(lastOffset)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for d in data:
            arr.append(d['ANALYSIS'])
        lastOffset = data[-1]['NEWSID'] - 1
    with open(fileName, 'w') as f:
        f.write('Sentiment, Analysis\n')
        for a in arr:
            f.write((',' + '"' + a.replace('&quot;', '\'') + '"').encode("ascii", "ignore").decode('UTF-8') + '\n')
