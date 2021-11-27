import re


class Cleaner:

    def __init__(self, filename):
        self.filename = filename

    def clean_subtitles(self):
        subtitles_before = open(self.filename, "r")
        subtitles_cleaned = open('subtitles', 'w')

        # remember first part of a sentence
        line_before = ""
        for line in subtitles_before:
            line = self.clean_line_regexp(line)

            if line == "":
                continue
            if line_before:
                line = line_before + ' ' + line
                line_before = ""
            if line[-2] == '.' or line[-2] == '?' or line[-2] == '!':
                subtitles_cleaned.write(line)
            else:
                line_before = line.replace("\n", "")

    @staticmethod
    def clean_line_regexp(line: str) -> str:
        """

        :param line:
        :type: string
        :return: A cleaned line.
        :rtype: string
        """

        line = line.replace("...", "")
        line = re.sub(r'^\d+\n', "", line)
        line = re.sub(r'^\n', "", line)
        line = re.sub(r'^\d.*\d$\n', "", line)
        return line
