#!/usr/bin/env python3

from tf.app import use
import unicodedata

# If you haven't run text-fabric before, you'll need to
# extract Genesis so the script isn't trying to run on the
# entire Bible (which takes a few GB of memory).
# To do that run
#   from tf.app import use
#   A = use('bhsa', hoist=globals())
#   A.extract({'GenesisBook': ('genesis',)})
# which will save a version of the text-fabric data
# which only contains the book of Genesis (much more manageable).
# On the other hand, if you want to run on everything
# (and have enough RAM), you can drop the `volume` argument
# to run on everything.

use('bhsa', hoist=globals(), volume='ExodusBook')

def norm(s):
    # normalize and drop cantillation marks
    # We want to eventually deal with cantillation,
    # but for now it just makes forms with different
    # punctuation appear as different entries,
    # which is unhelpful.
    return ''.join(c for c in unicodedata.normalize('NFC', s) if ord(c) not in range(0x591, 0x5af + 1))

TAG_MAP = {
    'subs': 'n',
    'verb': 'v',
    'art': 'det',
    'prep': 'pr',
    'nmpr': 'np',
    'adjv': 'adj',
    'advb': 'adv',
    'm': 'm',
    'f': 'f',
    'sg': 'sg',
    'du': 'du',
    'pl': 'pl',
    'c': 'cons',
    'p1': 'p1',
    'p2': 'p2',
    'p3': 'p3',
    'perf': 'perf',
    'impf': 'impf',
    'qal': 'actv',
    'hif': 'caus',
    'hof': 'caus><pass',
    'nif': 'pass',
    'piel': 'ints',
    'pual': 'ints><pass',
    'hit': 'recip',
    'infc': 'inf',
    'infa': 'inf', # TODO: this is not the same
    'ptca': 'pprs',
    'ptcp': 'pp',
    'intj': 'ij',
    'prps': 'prn><pers',
    'impv': 'imp',
    'nega': 'adv><neg',
    'prde': 'prn><dem',
    'inrg': 'itg',
    'prin': 'prn><itg'
}

def feat(w, f):
    v = F.__getattribute__(f).v(w)
    if not v or v in ['NA', 'unknown', 'none']:
        return ''
    elif v in TAG_MAP:
        return '<' + TAG_MAP[v] + '>'
    elif f in ['gn', 'nu', 'st']:
        return ''
    else:
        return '<' + v + '??>'

def word(w):
    surf = norm(T.text(w))
    tail = F.trailer_utf8.v(w)
    if tail:
        surf = surf[:-len(tail)]
    ana = norm(F.lex_utf8.v(w))
    pos = feat(w, 'sp')
    if pos == '<conj??>':
        if ana in ['ו', 'או']:
            pos = '<cnjcoo>'
        else:
            pos = '<cnjsub>'
    if pos == '<n>' and feat(w, 'ls') == '<card??>':
        pos = '<num>'
    ana += pos
    if pos == '<det>':
        ana += '<def>'
    elif pos == '<n>' or pos == '<np>':
        if ana == 'ארץ<n>':
            ana += '<f>'
        else:
            ana += (feat(w, 'gn') or '<mf>')
        ana += feat(w, 'nu') + feat(w, 'st')
    elif pos == '<num>':
        gn = feat(w, 'gn') or '<mf>'
        if gn == '<m>':
            ana += '<f>'
        else:
            ana += '<m>'
        ana += feat(w, 'st')
    elif pos == '<prn><pers>':
        ana = 'הוא<prn><pers>'
        ana += feat(w, 'ps')
        ana += feat(w, 'gn') or '<mf>'
        ana += feat(w, 'nu')
    elif pos == '<prn><dem>':
        if ana == 'זאת<prn><dem>':
            ana = 'זה<prn><dem><f><sg>'
        elif ana == 'זה<prn><dem>':
            ana = 'זה<prn><dem><m><sg>'
        elif ana == 'אלה<prn><dem>':
            ana = 'זה<prn><dem><mf><pl>'
    elif pos == '<v>':
        ana += feat(w, 'vs')
        tense, cons = feat(w, 'vt'), ''
        if tense == '<wayq??>':
            tense = '<impf>'
            cons = '<consec>'
        ana += tense
        if tense != '<inf>':
            ana += feat(w, 'ps')
            ana += (feat(w, 'gn') or '<mf>')
            ana += feat(w, 'nu')
        ana += cons
    prn = feat(w, 'prs_ps')
    if prn:
        if pos == '<n>':
            ana += '<cons>'
        ana += '+הוא<prn><pers>' + prn
        ana += feat(w, 'prs_gn') or '<mf>'
        ana += feat(w, 'prs_nu')
    return (surf, bool(tail), ana)

with open('raw.txt', 'w') as raw_f:
    with open('ana.txt', 'w') as ana_f:
        surf = ''
        ana = ''
        for w in F.otype.s('word'):
            s, t, a = word(w)
            surf += s
            if ana:
                ana += '+'
            ana += a
            if t:
                raw_f.write(surf + '\n')
                ana_f.write(f'^{surf}/{ana}$\n')
                surf = ''
                ana = ''
