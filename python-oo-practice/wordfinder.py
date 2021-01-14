"""Word Finder: finds random words from a dictionary."""

import numpy as np

class WordFinder:
    def __init__(self, file):
        """ Read words into list and report number read """
        self._words = []
        self._lines = 0
        with open(file) as f:
            for line in f:
                self._words.append(line.strip())
                self._lines += 1
        print(self._lines, "lines read")

    def random(self):
        """ Choose a word at random from the list """
        return self._words[int(np.random.randint(self._lines))]
if __name__ == '__main__':
    w = WordFinder("python-oo-practice/words.txt")  
    for i in range(1,6):
        print("Word {} found was: {}".format(i,w.random()))