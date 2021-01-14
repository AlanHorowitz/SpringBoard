"""Word Finder: finds random words from a dictionary."""

import numpy as np

class WordFinder:
    def __init__(self, file):
        """ Read words into list and report number read """
        self._words = []
        self._lines = 0
        with open(file) as f:
            for line in f:
                filtered_line = self._filtered_line(line)
                if filtered_line:
                    self._words.append(filtered_line)
                self._lines += 1
        print(self._lines, "lines read")

    def random(self):
        """ Choose a word at random from the list """
        return self._words[int(np.random.randint(len(self._words)))]

    def _filtered_line(self,line):
        return line.strip()


""" SpecialWordFinder filters out blank lines and comments  """
class SpecialWordFinder(WordFinder):
    def _filtered_line(self, line):
        line = line.strip()
        return None if (len(line) == 0 or line.startswith('#')) else line

if __name__ == '__main__':
    wf = WordFinder("python-oo-practice/words.txt")  
    for i in range(1,6):
        print("Word {} found was: {}".format(i,wf.random()))

    swf = SpecialWordFinder("python-oo-practice/special_words.txt")  
    for i in range(1,6):
        print("Word {} found was: {}".format(i,swf.random()))