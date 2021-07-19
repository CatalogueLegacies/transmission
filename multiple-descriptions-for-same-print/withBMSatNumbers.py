# generates withBMSatNumbers.csv which details LWL records with a BMSat catalogue number in 500 and/or 510 field
# generates withBMSatNumbers_multipleRecords.csv which groups LWL records that refer to the same BMSat number

import re
import html
from collections import defaultdict

catNumber500 = defaultdict(list)
catNumber510 = defaultdict(list)

i = open('parsed_LWLXML.tsv', 'r')
for l in i:
    line = l.strip().split('\t')

    if line[1] == '500':
        # e.g. catalogue number ' Cf. No. 10895 in the Catalogue of'
        catNumber = re.findall(r'([Nn]o\.* \d+ in the Catalogue of prints and drawings in the British Museum)',
                               line[2])
        if catNumber:
            catNumber500[line[0]] = catNumber

    if line[1] == '510':
        catNumber = re.findall(r'<marc:subfield code=\"a\">Catalogue of prints and drawings in the British Museum\.'
                               r' Division I, political and personal satires,</marc:subfield>'
                               r'<marc:subfield code=\"c\">(.*?)</marc:subfield>', line[2])
        if catNumber:
            catNumber510[line[0]] = catNumber
i.close()

# get description text (where available) for each record, and check for wholly quoted descriptions,
recs = set(catNumber500.keys()).union(catNumber510.keys())
descriptions = defaultdict(list)
i = open('parsed_LWLXML.tsv', 'r')
for l in i:
    line = l.strip().split('\t')
    if line[0] in recs:
        if line[1] == '520':
            descriptions[line[0]].append(line[2])  # allowing for a record to have multiple 520 field entries
i.close()

o = open('withBMSatNumbers.csv', 'w')
o.write(
    'LWL number\t500 Match\tBMSat from 500\t510 Match\tBMSat from 510\tBMSat (from 500, else 510)\tBM online\t'
    'Description (from 520)\n')
linesPerBMSatNumber = defaultdict(list)
for r in recs:
    s = re.search(r'\d+', ' '.join(catNumber500[r]))
    if s:
        n500 = s.group(0)
    else:
        n500 = 0

    s = re.search(r'\d{3,}', ' '.join(catNumber510[r]))
    if s:
        n510 = s.group(0)
    else:
        n510 = 0

    if n500 == 0:
        bmsat = n510
    else:
        bmsat = n500

    if descriptions[r]:
        description = html.unescape(" ".join(descriptions[r]))
        description = re.sub(r"\\'", "'", description)
        description = re.sub(r'^\[.*?>', '', description)
        description = re.sub(r'</marc:subfield>\']', '', description)
    else:
        description = 'NO DESCRIPTION'

    if re.search('british museum online', description, re.IGNORECASE):
        bmo = 'BM ONLINE'
    else:
        bmo = '---------'

    o.write(f'{r}\t{catNumber500[r]}\t{n500}\t{catNumber510[r]}\t{n510}\t{bmsat}\t{bmo}\t{description}\n')
    linesPerBMSatNumber[bmsat].append((r, f'{r}\t{catNumber500[r]}\t{n500}\t{catNumber510[r]}\t{n510}\t{bmsat}\t{bmo}\t'
                                          f'{description}'))
o.close()

o1 = open('withBMSatNumbers_multipleRecords.csv', 'w')
o1.write(
    'LWL number\t500 Match\tBMSat from 500\t510 Match\tBMSat from 510\tBMSat (from 500, else 510)\tBM online\t'
    'Description (from 520)\n')
countMultiples = defaultdict(int)
for bmsn in sorted(linesPerBMSatNumber, key=lambda k: (len(linesPerBMSatNumber[k]), int(k)), reverse=True):
    countMultiples[len(linesPerBMSatNumber[bmsn])] += 1
    o1.write(f'\n\nBMSat {bmsn}\n')
    for line in sorted(linesPerBMSatNumber[bmsn], key=lambda k: int(k[0])):
        o1.write(f'{line[1]}\n')
o1.close()
print(countMultiples)
