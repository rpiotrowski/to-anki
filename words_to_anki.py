#!python3 

import sys, re

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



cleanSubtitles()

subtitles = open('subtitles','r')
to_anki = open('to_anki','w')

vocabulary = list(input("Podaj po przecinku wyrażenia jakie mam poszukać\n").split(','))

for line in subtitles:
    for vocab in vocabulary:
        if vocab in line:
            to_anki.write(vocab + ';' + vocab + ';' + line)


