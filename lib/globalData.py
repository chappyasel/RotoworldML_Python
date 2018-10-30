import urllib
import json

def init():
    global SENTIMENTS
    SENTIMENTS = ["+", "-", "0"]
                # positive, negative, neutral

def cleanArticles(articles):
    response = urllib.urlopen("http://www.rotoworld.com/services/mobile.asmx/GetPlayers?sport=NBA&token=m1rw-xor-434s-bbjt-1")
    data = json.loads(response.read())
    names = [item for d in data for item in [d['FIRSTNAME'], d['LASTNAME']]]
    filteredArticles = []
    for a in articles:
        for n in names:
            a = a.replace(' ' + n + ' ', ' NAME ')
            a = a.replace(' ' + n + '\'s ', ' NAME\'s ')
        filteredArticles.append(a)
    return filteredArticles
