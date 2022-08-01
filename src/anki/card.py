class Card:
    def __init__(self, word):
        self._word = word

    @staticmethod
    def get_frequency(frequency_sheet, word: str) -> str:
        for i in range(4, frequency_sheet.max_row):
            if frequency_sheet.cell(row=i, column=2).value == word:
                # returns position on frequency list
                return str(frequency_sheet.cell(row=i, column=1).value)
        return "Out of range"

    @property
    def word(self):
        return self._word
