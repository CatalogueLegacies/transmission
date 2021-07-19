# forCorpusofWrittenByLWL.py
# extracts various features from each record in the input file that can be used to select records
#   - features described in lines 15-22 below, i.e. where sets are declared
#   - output as .csv for sorting/selecting records in a spreadsheet program, or for further processing
# in the Legacies project, these particular features were used to select records considered to have been written by the
#   Lewis Walpole Library, rather than by the British Museum
# OUTPUT IS !?!?!?!
# the descriptions are processed in preparation for corpus linguistic analysis
# this script also generates distribution data about the dates (years) found in the 264 and 655 fields

import re
import html
from collections import defaultdict

lwlRecordNumbers = set()  # all the record numbers seen
withSVWin655 = set()  # (the numbers of) all records in which 'Satires (Visual works)' is present in 655 field
withCCin600 = set()  # all records in which 'Caricatures and cartoons' is present in 600 field
withBMSatNumber500_510 = set()  # all records in which a BMSat catalogue number is present (according to regex patterns)
notInBM500 = set()  # all records in which 'not in the catalogue of prints and drawings' is present in 500 field
quotedDescription520 = set()  # all records in which the description in 520 field starts with "
bmOnline520 = set()  # all records in which '--british museum online catalogue' is present in 520 field (case insens.)
has520Content = set()  # all records with a 520 field

bmRegNumbers = defaultdict(list)

rawDescriptions = defaultdict(list)
processedDescriptions = defaultdict(str)  # descriptions prepared for subsequent corpus linguistic analysis

years264, years655 = defaultdict(list), defaultdict(list)  # date distribution data

i = open('parsed_LWLXML.tsv', 'r')
for l in i:
    line = l.strip().split('\t')

    lwlRecordNumbers.add(line[0])

    if line[1] == '655':
        if 'Satires (Visual works)' in line[2]:
            withSVWin655.add(line[0])

    if line[1] == '600':
        if 'Caricatures and cartoons' in line[2]:
            withCCin600.add(line[0])

    if line[1] == '500':
        catNumber = re.findall(r'([Nn]o\.* \d+ in the Catalogue of prints and drawings in the British Museum)', line[2])
        if catNumber:
            withBMSatNumber500_510.add(line[0])
        if 'not in the catalogue of prints and drawings' in line[2].lower():
            notInBM500.add(line[0])
        regNumber = re.findall(r'(\d\d\d\d,\d+\.\d+)', line[2])
        bmRegNumbers[line[0]] = regNumber

    if line[1] == '510':
        catNumber = re.findall(r'<marc:subfield code=\"a\">Catalogue of prints and drawings in the British Museum\.'
                               r' Division I, political and personal satires,</marc:subfield>'
                               r'<marc:subfield code=\"c\">(.*?)</marc:subfield>', line[2])
        if catNumber:
            withBMSatNumber500_510.add(line[0])

    if line[1] == '520':
        has520Content.add(line[0])
        rawDescriptions[line[0]].append(line[2])  # allowing for a record to have multiple 520 field entries

    if line[1] == '264':
        years264[line[0]] = re.findall(r'\d\d\d\d', line[2])

    if line[1] == '655':
        years655[line[0]] = re.findall(r'\d\d\d\d', line[2])
i.close()

print(f'{len(rawDescriptions)}')
for r in lwlRecordNumbers:
    if r in has520Content:
        description = html.unescape(" ".join(rawDescriptions[r]))
        description = re.sub(r"\\'", "'", description)
        description = re.sub(r'^\[.*?>', '', description)
        description = re.sub(r'</marc:subfield>\']', '', description)
    else:
        description = 'NO DESCRIPTION'

    processedDescriptions[r] = description

    if description.startswith('"'):
        quotedDescription520.add(r)

    # ?use regex here e.g. to make 'online' optional
    if '--british museum online catalogue' in description.lower():
        bmOnline520.add(r)

print(f'\nCounts before selection:\n\tAll LWL records - {len(lwlRecordNumbers)}\n\tSatires (Visual works) in 655 - '
      f'{len(withSVWin655)}\n\tCaricatures and cartoons in 600 - {len(withCCin600)}\n\t'
      f'Has 520 content - {len(has520Content)}\n\t'
      f'not in the catalogue of prints and drawings in 500 - {len(notInBM500)}\n\tBMSat number in 500, 510 - '
      f'{len(withBMSatNumber500_510)}\n\tQuoted descriptions - {len(quotedDescription520)}\n\tBM ONLINE - '
      f'{len(bmOnline520)}\n\tBM reg number - {len(bmRegNumbers)}\n\n')

recs = ((withSVWin655.union(withCCin600)).difference(withBMSatNumber500_510)).intersection(has520Content)
selected = [r for r in recs if ((r in notInBM500) and (bmRegNumbers[r] == []) and (r not in quotedDescription520)
            and (r not in bmOnline520))]

print(f'Number of selected records SatVis/CartCaric, not BMSat number: {len(recs)}\n\n')
yearDistributionAll = defaultdict(int)
decadeDistributionAll = defaultdict(int)

o = open('forCorpusOfWrittenByLWL.csv', 'w')
o.write('LWL number\t"not in catalogue...(500)"\tBM reg number\tquoted description\tin BM online (520)\t264 year(s)\t'
        '655 years\tmajority year\tdescription\n')
for r in sorted(recs, key=lambda x: int(x)):
    years = years264[r] + years655[r]
    if years:
        yearCount = defaultdict(int)
        for y in years:
            yearCount[y] += 1
        year = sorted(yearCount, key=yearCount.get, reverse=True)[0]
    else:
        year = '0000'
    yearDistributionAll[year] += 1
    decadeDistributionAll[f'{year[0:3]}0\'s'] += 1
    o.write(f'{r}\t{r in notInBM500}\t{bmRegNumbers[r]}\t{r in quotedDescription520}\t{r in bmOnline520}\t'
            f'{years264[r]}\t{years655[r]}\t{year}\t{processedDescriptions[r]}\n')
o.close()

yearDistributionSelected = defaultdict(int)
decadeDistributionSelected = defaultdict(int)
for r in selected:
    years = years264[r] + years655[r]
    if years:
        yearCount = defaultdict(int)
        for y in years:
            yearCount[y] += 1
        year = sorted(yearCount, key=yearCount.get, reverse=True)[0]
    else:
        year = '0000'
    yearDistributionSelected[year] += 1
    decadeDistributionSelected[f'{year[0:3]}0\'s'] += 1

o = open('forCorpusOfWrittenByLWL_dateDistributions.tsv', 'w')
o.write('By decade...\n')
o.write('\t"all" records\tthe 543\n')
for d in sorted(decadeDistributionAll):
    o.write(f'{d}\t{decadeDistributionAll[d]}\t{decadeDistributionSelected[d]}\n')
o.write('\n\nBy year...\n')
o.write('\t"all" records\tthe 543\n')
for y in sorted(yearDistributionAll):
    o.write(f'{y}\t{yearDistributionAll[y]}\t{yearDistributionSelected[y]}\n')
o.close()
