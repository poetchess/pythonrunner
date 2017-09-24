"""Build an index mapping word -> list of occurrences"""

import sys
import re

WORD_RE = re.compile('\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)

            # an inefficient way
            # get the list of occurrences for word, or [] if not found.
            occurrences = index.get(word, [])
    
            occurrences.append(location)

            # put changed occurrences into index dict, this entails a second
            # search through the index.
            index[word] = occurrences

for word in sorted(index, key=str.upper):
    print(word, index[word])
