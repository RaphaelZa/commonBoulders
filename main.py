from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import os
from datetime import date


boulders = {}
URLs = ['https://blocsummer-graz.at/bloc-summer-sessions/ranking.php?r=2', 'https://blocsummer-graz.at/bloc-summer-sessions/ranking.php?r=3']
hallen = ['blochouse', 'boulderclub', 'boulderpoint', 'cac', 'newton']
today = date.today().strftime("%d-%B")

for halle in hallen:
    buffer = {}
    for i in range(1, 31):
         buffer[i] = 0
    boulders[halle] = buffer


def boulderIncrement(halle, boulder):
    preInc = boulders[halle][boulder]
    boulders[halle][boulder] = preInc+1


def blocScraper(url):

    bouldererPage = requests.get(url)
    bouldererSoup = BeautifulSoup(bouldererPage.content, 'html.parser')


    boulderers = bouldererSoup.find_all("div", {"id" : re.compile('f.*')})
    bouldererLink = []


    for i, b in enumerate(boulderers):
        href = b.find('a').attrs['href']
        link = 'https://blocsummer-graz.at/bloc-summer-sessions/' + href
        bouldererLink.append(link)
        #if i == 3:
            #break


    for link in bouldererLink:
        boulderPage = requests.get(link)
        boulderSoup = BeautifulSoup(boulderPage.content, 'html.parser')
        idAll = boulderSoup.find_all("button", {"id" : re.compile('b-.*')})


        #print(idAll)
        for i, id in enumerate(idAll):
            halle = ''
            if i < 30:
                halle = "blochouse"
            if i > 29 and i < 60:
                halle = "boulderclub"
            if i > 59 and i < 90:
                halle = "boulderpoint"
            if i > 89 and i < 120:
                halle = "cac"
            if i > 119:
                halle = "newton"

            nummerString = id.get_text()
            nummerInt = int(nummerString)

            if 'btn-success' in id["class"]:
                boulderIncrement(halle, nummerInt)




if not os.path.exists('plots'):
    os.mkdir('plots')

if not os.path.exists('plots/' + today):
    os.mkdir('plots/' + today)




for URL in URLs:
    blocScraper(URL)

for halle in hallen:
    boulderDict = boulders[halle]
    keys = boulderDict.keys()
    values = boulderDict.values()
    clrs = []

    plt.figure(figsize=(15,5))
    plt.bar(keys, values)
    plt.xticks(list(keys))
    plt.title(halle)
    for i, v in enumerate(values):
        plt.text(i + .75, v + .02, str(v))

    plt.savefig('plots/'+ today + '/' + halle)




