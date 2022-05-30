from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import os
from datetime import date


boulders = {}
URLs = ['https://blocsummer-graz.at/bss/ranking.php?r=1&k=2', 'https://blocsummer-graz.at/bss/ranking.php?r=1&k=3']
hallen = ['blochouse', 'boulderclub', 'newton']
today = date.today().strftime("%d-%B")
boulderclubIds = [9, 10, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]
blochouseIds = [1, 2, 3, 4, 5, 6 , 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

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
        link = 'https://blocsummer-graz.at/bss/' + href
        bouldererLink.append(link)
        #print(f"Parsing boulderer number: {i}")



    for link in bouldererLink:
        boulderPage = requests.get(link)
        boulderSoup = BeautifulSoup(boulderPage.content, 'html.parser')
        idAll = boulderSoup.find_all("button", {"id" : re.compile('b-.*')})


        for i, id in enumerate(idAll):

            number = re.findall("\d+", id.get("id"))[0]
            n = int(number);
            halle = ''
            if n in blochouseIds:
                halle = "blochouse"
            if n in boulderclubIds:
                halle = "boulderclub"
            if n > 61:
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




