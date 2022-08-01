import bs4
import requests
from src.anki.card import Card


class EnglishCard(Card):
    """This is a representation of english type card

    """

    def get_pronunciation(self):
        try:
            url = f'https://dictionary.cambridge.org/dictionary/english/{self.word}'
            dictionary_site = requests.get(url)
            dictionary_soup = bs4.BeautifulSoup(dictionary_site.text, 'html.parser')
            pronunciation_soup = dictionary_soup.select('.ipa')
            pronunciation = [pronunciation_soup[0].getText(), pronunciation_soup[1].getText()]
            return pronunciation
        except:
            return ["", ""]

    def get_polish_meanings(self):
        try:
            # word = word.replace(" ","+")
            # TODO fix for example for ATM card
            url = f"https://www.diki.pl/slownik-angielskiego?q={self.word}"
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

            meanings_soup = dikiSoup.select('.plainLink')
            # print(meanings_soup)

            translation = []
            for elem in meanings_soup:
                translation.append(elem.getText())

            if translation:
                return translation
            else:
                return [""]
        except:
            return [""]


