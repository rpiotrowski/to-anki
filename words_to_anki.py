#!python3 

import sys, re, bs4, requests

def cleanSubtitles():
    subtitlesBefore = open(sys.argv[1],"r")
    subtitlesCleaned = open('subtitles','w')
    
    #zmienna do zamapiętania linii urwanej
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
        soup = dictionarySoup.select('.ipa')
        pronounciation = [soup[0].getText(),soup[1].getText()]
        return pronounciation
    except:
        return ["",""]


cleanSubtitles()

subtitles = open('subtitles','r')
to_anki = open('to_anki','w')

vocabulary = list(input("Podaj po przecinku wyrażenia jakie mam poszukać\n").split(','))

for line in subtitles:
    for vocab in vocabulary:
        if vocab in line:
            pronounciation = getPronounciation(vocab)
            line = line.replace("\n","")
            to_anki.write(vocab + ';' + vocab + ';' + line + ';' + pronounciation[0]+ ';' + pronounciation[1] + '\n')

