#!python3 

import sys, re, bs4, requests, openpyxl

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

def getPronunciation(word):
    try:
        url = 'https://dictionary.cambridge.org/dictionary/english/%s' % (word)
        dictionarySite = requests.get(url)
        dictionarySoup = bs4.BeautifulSoup(dictionarySite.text, 'html.parser')
        pronunciationSoup = dictionarySoup.select('.ipa')
        pronunciation = [pronunciationSoup[0].getText(),pronunciationSoup[1].getText()]
        return pronunciation
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
        # print(meaningsSoup)

        translation = []
        for elem in meaningsSoup:
            translation.append(elem.getText())
        return translation
    except:
        return [""]

def getFrequency(frequencySheet,word):
    for i in range(4,frequencySheet.max_row):
        if frequencySheet.cell(row=i, column=2).value == word:
            # returns position on frequency list
            return str(frequencySheet.cell(row=i,column=1).value)
    return "Out of range"


cleanSubtitles()
wb = openpyxl.load_workbook('frequency.xlsx')
# print(wb.sheetnames)
frequencySheet = wb['10000k']
# print(sheet['A1'].value)





subtitles = open('subtitles','r')
to_anki = open('to_anki','w')

vocabulary = list(input("Podaj po przecinku wyrażenia jakie mam poszukać\n").split(','))
comment = input("Podaj komentarz jaki chcesz umiescic w kartach\n")

fileLineNumbers = 0
for line in subtitles:
    for vocab in vocabulary:
        if vocab in line:
            pronunciation = getPronunciation(vocab)
            polishMeanings = getPolishMeanings(vocab)
            frequency = getFrequency(frequencySheet,vocab)
            line = line.replace("\n","")
            #TODO paste all possible meanings
            to_anki.write(polishMeanings[0] + ';;' + vocab + ';' + line + ';' + comment +';' + pronunciation[0]+ ';' + pronunciation[1] + ';' + frequency + '\n')
            #Only find first sentence with that vocabulary
            print(vocab,'added.')
            vocabulary.remove(vocab)
            fileLineNumbers += 1
print(fileLineNumbers, 'lines added.')

