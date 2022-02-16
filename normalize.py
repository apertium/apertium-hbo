#!/usr/bin/env python3

import sys
import unicodedata as u

def cls(*ns):
    return [chr(n + 0x500) for n in ns]
def crng(n1, n2):
    return [chr(n + 0x500) for n in range(n1, n2+1)]

vav = chr(0x5d5)
holam = [chr(0x5b9), chr(0x5ba)]
vav_holam = chr(0xfb4b)

shin_base = chr(0x5e9)
shin = chr(0xfb2a)
shin_dot = chr(0x5c1)
sin = chr(0xfb2b)
sin_dot = chr(0x5c2)

dagesh = chr(0x5bc)
rafe = chr(0x5bf)

vowels = crng(0xb0, 0xb8) + cls(0xc7, 0xbb)

lower_punct = cls(0x91, 0x96, 0x9b, 0xaa, 0xc5) + crng(0xa2, 0xa7)

yetiv_dehi = cls(0x9a, 0xad)

upper_punct = crng(0x92, 0x95) + cls(0x97, 0x98) + crng(0x9c, 0xa1) + cls(0xa8, 0xab, 0xac, 0xaf, 0xc4) + [chr(0x307)]

post_punct = cls(0xae, 0xa9, 0x99)

cur = []

def update(ch, dia, res):
    global cur
    if cur[0] == ch and dia in cur[1:]:
        cur.remove(dia)
        cur[0] = res

def concat(ops):
    global cur
    l = [cur[0]]
    for c in cur[1:]:
        if c in ops:
            l[0] += c
        else:
            l.append(c)
    cur = l

def output():
    global cur
    if not cur:
        return
    elif len(cur) == 1:
        sys.stdout.write(cur[0])
        cur = []
        return
    # combined characters
    update(shin_base, shin_dot, shin)
    update(shin_base, sin_dot, sin)
    update(vav, holam[0], vav_holam)
    update(vav, holam[1], vav_holam)
    # order based on https://www.sbl-site.org/Fonts/SBLHebrewUserManual1.5x.pdf
    concat(shin_dot)
    concat(sin_dot)
    concat([dagesh])
    concat([rafe])
    concat(holam)
    concat(vowels)
    concat(lower_punct)
    concat(yetiv_dehi)
    concat(upper_punct)
    concat(post_punct)
    sys.stdout.write(''.join(cur))
    cur = []

while True:
    c = sys.stdin.read(1)
    if not c:
        output()
        break
    elif u.category(c) not in ['Lo', 'Mn']:
        output()
        sys.stdout.write(c)
    elif c == vav and holam[0] in cur:
        cur.remove(holam[0])
        output()
        cur.append(vav_holam)
    elif c == vav and holam[1] in cur:
        cur.remove(holam[1])
        output()
        cur.append(vav_holam)
    else:
        if u.category(c) == 'Lo':
            output()
        cur.append(c)
