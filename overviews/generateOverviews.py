#!?!assuming fields are not split over lines

import re
import os
from collections import defaultdict
from statistics import mean, median
from random import shuffle

datafieldCount = defaultdict(int)
datafieldContent = defaultdict(list)
datafieldContentSplitSubfields = defaultdict(list)
datafieldWordList = defaultdict(lambda: defaultdict(int))
datafieldBigramList = defaultdict(lambda: defaultdict(int))
datafieldTrigramList = defaultdict(lambda: defaultdict(int))
datafield4gramList = defaultdict(lambda: defaultdict(int))
datafield5gramList = defaultdict(lambda: defaultdict(int))
datafield6gramList = defaultdict(lambda: defaultdict(int))
datafield7gramList = defaultdict(lambda: defaultdict(int))
datafield8gramList = defaultdict(lambda: defaultdict(int))

i = open('bib_walpole.xml', 'r')
for line in i:
    datafields = re.findall('\<marc:datafield tag=\"(.*?)\".*?\>(.*?)\<\/marc:datafield\>', line.strip())
    for (tag, content) in datafields:
        datafieldCount[tag] += 1
        datafieldContent[tag].append(content)
i.close()

o = open('XML_analysis2.txt', 'w')
for t in sorted(datafieldCount.keys(), key=datafieldCount.get, reverse=True):
#for t in ['655', '520']:
    o.write(f'\n\n\ntag = "{t}",  frequency = {datafieldCount[t]}\n')
    wordCounts = list ( map (lambda x: len(re.sub('\<.*?\>', ' ', x).split()) , datafieldContent[t]) )
    mode = max(set(wordCounts), key=wordCounts.count) #won't return top equal modes!
                                                #??Python 3.8 for multimode, or scipy stats.mode, to handle >1 mode
    o.write(f"Average number of words, ignoring <>'s (mean, median, mode) = "
            f"{round(mean(wordCounts),2)}, {median(wordCounts)}, {mode}\n\n")
    o.write("Random sample of 20 examples...\n-------------------------------\n")
    shuffle(datafieldContent[t])
    for c in datafieldContent[t][0:20]:
        o.write(f'{c}\n')

    print(f'doing n-grams for {t}')
    for c in datafieldContent[t]:
        subparts = re.split('\<.*?\>', c) #to not run-over datafields
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
#for df in ['655', '520']:
    if not os.path.exists(f'./allNgrams/{df}'):
        os.makedirs(f'./allNgrams/{df}')

    o = open(f'./allNgrams/{df}/textSplitBySubfields_{df}.txt', 'w')
    for l in datafieldContentSplitSubfields[df]:
        o.write(f'{l}\n')
    o.close()

    o = open(f'./allNgrams/{df}/wordlist_{df}.txt' , 'w')
    for w in sorted(datafieldWordList[df].keys(), key=datafieldWordList[df].get, reverse=True):
        o.write(f'{w}\t{datafieldWordList[df][w]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/bigramlist_{df}.txt' , 'w')
    for b in sorted(datafieldBigramList[df].keys(), key=datafieldBigramList[df].get, reverse=True):
        o.write(f'{b}\t{datafieldBigramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/trigramlist_{df}.txt', 'w')
    for b in sorted(datafieldTrigramList[df].keys(), key=datafieldTrigramList[df].get, reverse=True):
        o.write(f'{b}\t{datafieldTrigramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/4gramlist_{df}.txt', 'w')
    for b in sorted(datafield4gramList[df].keys(), key=datafield4gramList[df].get, reverse=True):
        o.write(f'{b}\t{datafield4gramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/5gramlist_{df}.txt', 'w')
    for b in sorted(datafield5gramList[df].keys(), key=datafield5gramList[df].get, reverse=True):
        o.write(f'{b}\t{datafield5gramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/6gramlist_{df}.txt', 'w')
    for b in sorted(datafield6gramList[df].keys(), key=datafield6gramList[df].get, reverse=True):
        o.write(f'{b}\t{datafield6gramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/7gramlist_{df}.txt', 'w')
    for b in sorted(datafield7gramList[df].keys(), key=datafield7gramList[df].get, reverse=True):
        o.write(f'{b}\t{datafield7gramList[df][b]}\n')
    o.close()

    o = open(f'./allNgrams/{df}/8gramlist_{df}.txt', 'w')
    for b in sorted(datafield8gramList[df].keys(), key=datafield8gramList[df].get, reverse=True):
        o.write(f'{b}\t{datafield8gramList[df][b]}\n')
    o.close()