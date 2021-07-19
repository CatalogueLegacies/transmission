# generateOverviews.py (previously analyseXML2.py)

# generates an overview of the contents for each MARC 21 field found in the input file which is hardcoded as i
#   - the input file is a dump of records comprising MARC 21 fields, formatted in XML, e.g. 'LWL_export.xml'
#   - 'overviewsPart1.txt' gives for each field: frequency, average "word" length, and a sample of up to 20 examples
#       - the fields are ordered by frequency
#   - '/overviewsPart2/' contains a directory for each field which contains 8 ngram lists (1 <= n <= 8)


import re
import os
from collections import defaultdict
from statistics import mean, median
from random import shuffle

i = open('LWL_export.xml', 'r')
datafieldCount = defaultdict(int)
datafieldContent = defaultdict(list)
datafieldContentSplitSubfields = defaultdict(list)
datafieldWordList , datafieldBigramList , datafieldTrigramList , datafield4gramList , datafield5gramList , \
    datafield6gramList , datafield7gramList , datafield8gramList = \
    [defaultdict(lambda: defaultdict(int)) for x in range(8)]

for line in i:
    datafields = re.findall('<marc:datafield tag=\"(.*?)\".*?>(.*?)</marc:datafield>', line.strip())
    for (tag, content) in datafields:
        datafieldCount[tag] += 1
        datafieldContent[tag].append(content)
i.close()

o = open('overviewsPart1.txt', 'w')
for t in sorted(datafieldCount.keys(), key=datafieldCount.get, reverse=True):
    o.write(f'\n\n\ntag = "{t}",  frequency = {datafieldCount[t]}\n')
    wordCounts = list ( map ( lambda x: len(re.sub('<.*?>', ' ', x).split()) , datafieldContent[t]) )
    mode = max(set(wordCounts), key=wordCounts.count) # won't return top equal modes; could use scipy stats.mode
    o.write(f"Average number of words, ignoring <>'s (mean, median, mode) = "
            f"{round(mean(wordCounts),2)}, {median(wordCounts)}, {mode}\n\n")
    o.write("Random sample of 20 examples...\n-------------------------------\n")
    shuffle(datafieldContent[t])
    for c in datafieldContent[t][0:20]:
        o.write(f'{c}\n')

    print(f'doing n-grams for {t}')
    for c in datafieldContent[t]:
        subparts = re.split('<.*?>', c)
        for sp in subparts:
            datafieldContentSplitSubfields[t].append(sp)
            words = sp.split()

            for w in words:
                datafieldWordList[t][w] +=1

            bigrams = list ( map (lambda x: f'{x[0]} {x[1]}', zip(words[:-1:1], words[1::1])))
            for b in bigrams:
                datafieldBigramList[t][b] +=1

            trigrams = list ( map (lambda x: f'{x[0]} {x[1]} {x[2]}', zip(words[:-2:1], words[1:-1:1], words[2::1])))
            for tr in trigrams:
                datafieldTrigramList[t][tr] +=1

            fourgrams = list(map(lambda x: f'{x[0]} {x[1]} {x[2]} {x[3]}',
                                 zip(words[:-3:1], words[1:-2:1], words[2:-1:1], words[3::1])))
            for tr in fourgrams:
                datafield4gramList[t][tr] += 1

            fivegrams = list(map(lambda x: f'{x[0]} {x[1]} {x[2]} {x[3]} {x[4]}',
                                 zip(words[:-4:1], words[1:-3:1], words[2:-2:1], words[3:-1:1], words[4::1])))
            for tr in fivegrams:
                datafield5gramList[t][tr] += 1

            sixgrams = list(map(lambda x: f'{x[0]} {x[1]} {x[2]} {x[3]} {x[4]} {x[5]}',
                    zip(words[:-5:1], words[1:-4:1], words[2:-3:1], words[3:-2:1], words[4:-1:1], words[5::1])))
            for tr in sixgrams:
                datafield6gramList[t][tr] += 1

            sevengrams = list(map(lambda x: f'{x[0]} {x[1]} {x[2]} {x[3]} {x[4]} {x[5]} {x[6]}',
                zip(words[:-6:1], words[1:-5:1], words[2:-4:1], words[3:-3:1], words[4:-2:1],
                    words[5:-1:1], words[6::1])))
            for tr in sevengrams:
                datafield7gramList[t][tr] += 1

            eightgrams = list(map(lambda x: f'{x[0]} {x[1]} {x[2]} {x[3]} {x[4]} {x[5]} {x[6]} {x[7]}',
                                  zip(words[:-7:1], words[1:-6:1], words[2:-5:1], words[3:-4:1], words[4:-3:1],
                                      words[5:-2:1], words[6:-1:1], words[7::1])))
            for tr in eightgrams:
                datafield8gramList[t][tr] += 1

o.close()

for df in datafieldCount.keys():
    if not os.path.exists(f'./overviewsPart2/{df}'):
        os.makedirs(f'./overviewsPart2/{df}')

    for s, d in zip(['wordlist' , 'bigramlist' , 'trigramlist' , '4gramlist' , '5gramlist' , '6gramlist' , '7gramlist'\
            , '8gramlist'], [datafieldWordList , datafieldBigramList , datafieldTrigramList , datafield4gramList ,\
            datafield5gramList , datafield6gramList , datafield7gramList , datafield8gramList]):
        o = open(f'./overviewsPart2/{df}/{s}_{df}.txt', 'w')
        for w in sorted(d[df].keys(), key=d[df].get, reverse=True):
         o.write(f'{w}\t{d[df][w]}\n')
        o.close()

    o = open(f'./overviewsPart2/{df}/textSplitBySubfields_{df}.txt', 'w')
    for l in datafieldContentSplitSubfields[df]:
        o.write(f'{l}\n')
    o.close()
