from src.anki.english_card import EnglishCard
from src.anki.cleaner import Cleaner
from src.config import SEPARATOR
import openpyxl
import sys


def app():
    try:
        cleaner = Cleaner(sys.argv[1])
    except IndexError as e:
        print('You must enter the subtitles filepath', f'{e!r}')
        sys.exit(1)

    cleaner.clean_subtitles()

    work_book = openpyxl.load_workbook('src/frequency.xlsx')
    frequency_sheet = work_book['10000k']

    vocabulary = input("Enter vocabularies separated by colons\n").split(',')
    comment = input("Enter comment you want to add\n")

    rows_added_counter = 0
    with open('output/to_anki', 'w') as to_anki, open('subtitles', 'r') as subtitles:
        for row in subtitles:
            for word in vocabulary:
                if word in row:
                    card = EnglishCard(word)
                    pronunciation = card.get_pronunciation()
                    polish_meanings = card.get_polish_meanings()
                    frequency = card.get_frequency(frequency_sheet, word)
                    row = row.replace("\n", "")
                    # TODO paste all possible meaningsp
                    to_anki.write(polish_meanings[0] + ';;' + word + ';' + row + ';' + comment + ';' + pronunciation[0] + ';' +
                                  pronunciation[1] + ';' + frequency + '\n')
                    # Only find first sentence with that vocabulary
                    print(word, 'added.')
                    vocabulary.remove(word)
                    rows_added_counter += 1
    print(rows_added_counter, 'rows added.')

    if not vocabulary:
        print('Vocabulary which were not added')
        print(vocabulary)
    else:
        print('All vocabulary were added')



