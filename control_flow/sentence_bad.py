import re
import reprlib

RE_WORD = re.compile('\w+')

# The implementation makes each Sentence instance at the same time an iterable
#   and iterator over itself. It can work, but is a bad idea.

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
        self.index = 0

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return Sentence(self.text)

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    for word in s:
        print(word)

    for word in s:
        print(word)
