#!/usr/bin/env python3

from collections import defaultdict

unknown = 0

ana_lists = defaultdict(list)

replacements_bhsa = [
    ('הנה<ij>', 'הנה<adv>'),
    ('<impf><p2><m><sg>', '<impf><p3><f><sg>'),
    ('<impf><p2><f><pl>', '<impf><p3><f><pl>')
]

replacements_ap = [
    ('<pause>', ''),
    ('<impf><p2><m><sg>', '<impf><p3><f><sg>'),
    ('<impf><p2><f><pl>', '<impf><p3><f><pl>'),
    ('אחרי<pr>', 'אחר<n><m><pl><cons>'),
    ('תחת<pr>', 'תחת<n><m><sg><cons>'),
    ('בין<pr>', 'בין<n><m><sg><cons>')
]

with open('ana_morph.txt') as fin:
    for line in fin:
        if '*' in line:
            unknown += 1
            continue
        elif ' ' in line:
            unknown += 1
            continue
        ap, bhsa = line.strip().split('[')
        bhsa = bhsa[:-1]
        surf, ap = ap[1:-1].split('/', 1)
        for src, dest in replacements_bhsa:
            bhsa = bhsa.replace(src, dest)
        for src, dest in replacements_ap:
            ap = ap.replace(src, dest)
        ana_lists[surf].append((ap, bhsa))

def process_dict(dct):
    tp = 0 # reference in fst output
    fp = 0 # reference not in fst output
    fn = 0 # fst output not in reference
    for surf, ls in dct.items():
        ap = set(ls[0][0].split('/'))
        bhsa = set(x[1] for x in ls)
        for b in bhsa:
            if b in ap:
                tp += len(ls)
            else:
                fp += len(ls)
        for a in ap:
            if a not in bhsa:
                fn += len(ls)
    return tp, fp, fn

tp, fp, fn = process_dict(ana_lists)
fp += unknown
print(f'tp {tp}, fp {fp}, fn {fn}')
prec = 100 * tp / (tp + fp)
rec = 100 * tp / (tp + fn)
f1 = 2 * prec * rec / (prec + rec)
print('precision', round(prec, 2))
print('recall', round(rec, 2))
print('F1', round(f1, 2))
