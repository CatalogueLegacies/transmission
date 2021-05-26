
import re
import html
from collections import defaultdict

lwlRecordNumbers = set()
withSVWin655 = set()
withCCin600 = set()
withBMSatNumber500_510 = set()
notInBM500 = set()
quotedDescription520 = set()
bmOnline520 = set()
has520Content = set()
bmRegNumbers =defaultdict(list)
rawDescriptions = defaultdict(list)
processedDescriptions = defaultdict(str)
years264 = defaultdict(list)
years655 = defaultdict(list)

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
        #this could be if in ???
        catNumber = re.findall(r'([Nn]o\.* \d+ in the Catalogue of prints and drawings in the British Museum)', line[2])
        if catNumber:
            withBMSatNumber500_510.add(line[0])
        #do this with regex e.g. for optional (the) LOWERCASE
        if 'not in the catalogue of prints and drawings' in line[2].lower():
            notInBM500.add(line[0])
        regNumber = re.findall(r'(\d\d\d\d\,\d+\.\d+)', line[2])
        #if regNumber:
        bmRegNumbers[line[0]] = regNumber

    if line[1] == '510':
        # this could be if in ???
        catNumber = re.findall(r'\<marc\:subfield code=\"a\"\>Catalogue of prints and drawings in the British Museum\.'
                                     r' Division I\, political and personal satires\,\<\/marc\:subfield\>'
                                     r'\<marc\:subfield code=\"c\"\>(.*?)\<\/marc\:subfield\>', line[2])
        if catNumber:
            withBMSatNumber500_510.add(line[0])

    if line[1] == '520':
        has520Content.add(line[0])
        rawDescriptions[line[0]].append(line[2])  # allowing for a record to have multiple 520 field entries

    if line[1] == '264':
        #years264[line[0]] = re.findall('\{\"c\"\:\".*?\"\}', line[2]) #assumes only one 264 instance per record
        years264[line[0]] = re.findall('\d\d\d\d', line[2])

    if line[1] == '655':
        #years655[line[0]] = re.findall('\{\"y\"\:\".*?\"\}', line[2]) #assumes only one 655 instance per record
        years655[line[0]] = re.findall('\d\d\d\d', line[2])
i.close()

print(f'{len(rawDescriptions)}')
for r in lwlRecordNumbers:
    if r in has520Content:
        description = html.unescape(" ".join(rawDescriptions[r]))
        description = re.sub(r"\\'", "'", description)
        description = re.sub(r'^\[.*?\>', '', description)
        description = re.sub(r'\<\/marc\:subfield\>\'\]', '', description)
    else:
        description = 'NO DESCRIPTION'

    processedDescriptions[r] = description

    if description.startswith('"'):
        quotedDescription520.add(r)

    #regex here e.g. to make 'online' optional
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
                               and (r not in bmOnline520))]#doing this late to get year distributions,
                                                # previously "implemented" in Excel to get the set of 543 descriptions

print(f'Number of selected records SatVis/CartCaric, not BMSat number: {len(recs)}\n\n')
yearDistributionAll = defaultdict(int)
decadeDistributionAll = defaultdict(int)

o = open('forCorpusOfWrittenByLWL.csv', 'w')
o.write('LWL number\t"not in catalogue...(500)"\tBM reg number\tquoted description\tin BM online (520)\t264 year(s)\t'
        '655 years\tmajority year\tdescription\n')
for r in sorted(recs, key = lambda x:int(x)):
    years = years264[r] + years655[r]
    if years:
        yearCount = defaultdict(int)
        for y in years: yearCount[y] += 1
        year = sorted(yearCount, key = yearCount.get, reverse=True)[0]
    else: year = '0000'
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
        for y in years: yearCount[y] += 1
        year = sorted(yearCount, key = yearCount.get, reverse=True)[0]
    else: year = '0000'
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