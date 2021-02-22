import bs4
import requests


class Anki:

    def __init__(self, word):
        self.word = word

    def getPronunciation(self):
        word = self.word
        try:
            url = 'https://dictionary.cambridge.org/dictionary/english/%s' % (word)
            dictionarySite = requests.get(url)
            dictionarySoup = bs4.BeautifulSoup(dictionarySite.text, 'html.parser')
            pronunciationSoup = dictionarySoup.select('.ipa')
            pronunciation = [pronunciationSoup[0].getText(), pronunciationSoup[1].getText()]
            return pronunciation
        except:
            return ["", ""]

    def getPolishMeanings(self):
        word = self.word
        try:
            # word = word.replace(" ","+")
            # TODO fix for example for ATM card
            url = "https://www.diki.pl/slownik-angielskiego?q=%s" % (word)
            dikiResponse = requests.get(url)
            dikiSoup = bs4.BeautifulSoup(dikiResponse.text, 'html.parser')
            # print(type(dikiSoup))
            # TODO fix meanings from links in nav
            # soup = dikiSoup.find("div", {"class": "diki-results-left-column"})
            # print(len(soup))
            # print(soup[0])
            # soup = soup[0].findAll("a", {"class": ".plainLink"})
            # print(soup)

            # dikiSoup2 = bs4.BeautifulSoup(soup[0],'html.parser')
            # print(type(dikiSoup2))
            # print(soup)
            # soup = soup.select('.plainLink')
            # print(soup)

            meaningsSoup = dikiSoup.select('.plainLink')
            # print(meaningsSoup)

            translation = []
            for elem in meaningsSoup:
                translation.append(elem.getText())

            if translation:
                return translation
            else:
                return [""]
        except:
            return [""]
