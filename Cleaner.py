import re


class Cleaner:

    def __init__(self, filename):
        self.filename = filename

    def cleanSubtitles(self):
        subtitlesBefore = open(self.filename, "r")
        subtitlesCleaned = open('subtitles', 'w')

        # viriable to remember first part of a sentence
        lineBefore = ""
        for line in subtitlesBefore:
            line = line.replace("...", "")
            line = re.sub(r'^\d+\n', "", line)
            line = re.sub(r'^\n', "", line)
            line = re.sub(r'^\d.*\d$\n', "", line)

            if not line:
                continue

            if lineBefore:
                line = lineBefore + ' ' + line
                lineBefore = ""

            if line[-2] == '.' or line[-2] == '?' or line[-2] == '!':
                subtitlesCleaned.write(line)
            else:
                lineBefore = line.replace("\n", "")
