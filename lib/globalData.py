import urllib
import json
from string import digits

def init():
    global SENTIMENTS
    SENTIMENTS = ["+", "-", "0", "!"]
                # positive, negative, neutral

# anonymize player names in article string list
def cleanArticles(articles):
    response = urllib.urlopen("http://www.rotoworld.com/services/mobile.asmx/GetPlayers?sport=NBA&token=m1rw-xor-434s-bbjt-1")
    data = json.loads(response.read())
    names = [item for d in data for item in [d['FIRSTNAME'], d['LASTNAME']]]
    filteredArticles = []
    for a in articles:
        for n in names:
            a = a.replace(' ' + n + ' ', ' NAME ')
            a = a.replace(' ' + n + '\'s ', ' NAME\'s ')
        a = a.replace('NAME NAME', 'NAME') # first and last name -> NAME
        a = a.replace('<i>', '') # remove italics
        a = a.replace('</i>', '') # ""
        filteredArticles.append(a)
    return filteredArticles
