from anki.anki import Anki
from anki.cleaner import Cleaner
import openpyxl
import sys

SEPARATOR = ';'

cleaner = Cleaner(sys.argv[1])
cleaner.clean_subtitles()

wb = openpyxl.load_workbook('src/frequency.xlsx')
frequencySheet = wb['10000k']

subtitles = open('subtitles', 'r')

vocabulary = list(input("Enter vocabularies separated by colons\n").split(','))
comment = input("Enter comment you want to add\n")

fileLineNumbers = 0
with open('output/to_anki', 'w') as to_anki:
    for line in subtitles:
        for vocab in vocabulary:
            if vocab in line:
                anki = Anki(vocab)
                pronunciation = anki.get_pronunciation()
                polishMeanings = anki.get_polish_meanings()
                frequency = anki.get_frequency(frequencySheet, vocab)
                line = line.replace("\n", "")
                # TODO paste all possible meaningsp
                to_anki.write(polishMeanings[0] + ';;' + vocab + ';' + line + ';' + comment + ';' + pronunciation[0] + ';' +
                              pronunciation[1] + ';' + frequency + '\n')
                # Only find first sentence with that vocabulary
                print(vocab, 'added.')
                vocabulary.remove(vocab)
                fileLineNumbers += 1
print(fileLineNumbers, 'rows added.')

if not vocabulary:
    print('Vocabulary which were not added')
    print(vocabulary)
else:
    print('All vocabulary were added')
