# input is two sets of descriptions S1, S2 -- one description per line in two .txt files
# output is all pairs of (S1 description, S2 description) with text similarity over a threshold value

import difflib

lwl_descriptions = []
bmsat_descriptions = []
i = open('LWL-4545descriptions-29Jan2021.txt', 'r', encoding='utf-8')
for l in i:
    lwl_descriptions.append(l.strip())
i.close()
i = open('CurV-corpus-27Jan2019.txt', 'r', encoding='utf-8')
for l in i:
    bmsat_descriptions.append(l.strip())
i.close()

o = open('trial3_LWL_X_BMSat_RESULTS.tsv', 'w', encoding='utf-8')
o.write('SM.ratio\tlength\tBM online\tLWL description\tBMSat description\n')
for count, lwl in enumerate(lwl_descriptions):
    print(count)
    for bmsat in bmsat_descriptions:
        s = difflib.SequenceMatcher(None, lwl, bmsat)  # only doing it this way round although not commutative!?!
        if s.real_quick_ratio() < 0.9:
            continue
        score = round(s.ratio(), 2)
        if score < 0.5:
            continue
        length = len(lwl)
        bmo = ('british museum online' in lwl.lower()).__str__()
        o.write(f'{score}\t{length}\t{bmo}\t{lwl}\t{bmsat}\n')
o.close()
