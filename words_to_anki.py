#!python3 

import sys, re, bs4, requests

def cleanSubtitles():
    subtitlesBefore = open(sys.argv[1],"r")
    subtitlesCleaned = open('subtitles','w')
    
    #viriable to remember first part of a sentence
    lineBefore = ""
    for line in subtitlesBefore:
        line = line.replace("...","")
        line = re.sub(r'^\d+\n',"",line)
        line = re.sub(r'^\n',"",line)
        line = re.sub(r'^\d.*\d$\n',"",line)

        if not line:
            continue

        if lineBefore:
            line = lineBefore + ' ' + line
            lineBefore = ""
          
        if line[-2]=='.' or line[-2]=='?' or line[-2]=='!':
            subtitlesCleaned.write(line)        
        else:
            lineBefore = line.replace("\n","")

def getPronounciation(word):
    try:
        url = 'https://dictionary.cambridge.org/dictionary/english/%s' % (word)
        dictionarySite = requests.get(url)
        dictionarySoup = bs4.BeautifulSoup(dictionarySite.text, 'html.parser')
        pronounciationSoup = dictionarySoup.select('.ipa')
        pronounciation = [pronounciationSoup[0].getText(),pronounciationSoup[1].getText()]
        return pronounciation
    except:
        return ["",""]

def getPolishMeanings(word):
    try:
        #word = word.replace(" ","+")
        #TODO fix for example for ATM card
        url = "https://www.diki.pl/slownik-angielskiego?q=%s" % (word)
        dikiResponse = requests.get(url)
        dikiSoup = bs4.BeautifulSoup(dikiResponse.text,'html.parser')
        # print(type(dikiSoup))
        #TODO fix meanings from links in nav
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
        print(meaningsSoup)

        translation = []
        for elem in meaningsSoup:
            translation.append(elem.getText())
        return translation
    except:
        return [""]


cleanSubtitles()

subtitles = open('subtitles','r')
to_anki = open('to_anki','w')

vocabulary = list(input("Podaj po przecinku wyrażenia jakie mam poszukać\n").split(','))
comment = input("Podaj komentarz jaki chcesz umiescic w kartach")

for line in subtitles:
    for vocab in vocabulary:
        if vocab in line:
            pronounciation = getPronounciation(vocab)
            polishMeanings = getPolishMeanings(vocab)
            line = line.replace("\n","")
            #TODO paste all possible meanings
            to_anki.write(polishMeanings[0] + ';;' + vocab + ';' + line + ';' + comment +';' + pronounciation[0]+ ';' + pronounciation[1] + '\n')
            #Only find first sentence with that vocabulary
            vocabulary.remove(vocab)

