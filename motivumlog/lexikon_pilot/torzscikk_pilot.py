# -*- coding: utf-8 -*-
"""Kereszthivatkozási törzscikk — PILOT render (ISTENTISZT-001).

Pilot-rövidítés: a lexikonoldalból olvas (render a renderből). Éles
változatban a generátor belső adatmodellje és a forrásréteg a bemenet.
Használat: python torzscikk_pilot.py <lexikonoldal.md> <kimenet.md> <statisztika.txt>
"""
import re
import sys

SRC, OUT, STAT = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(SRC, encoding='utf-8').read().split('\n')
stat = {}


def cnt(k, n=1):
    stat[k] = stat.get(k, 0) + n


# ---------- tisztító ----------
def clean(lines):
    out, in_naplo = [], False
    for ln in lines:
        if in_naplo:
            cnt('naplo_sor')
            if '】' in ln:
                in_naplo = False
            continue
        if ln.lstrip().startswith('【NAPLO'):
            cnt('naplo_blokk')
            cnt('naplo_sor')
            if '】' not in ln:
                in_naplo = True
            continue
        if ln.startswith('<!-- GENERÁLT'):
            cnt('marker')
            continue
        if ln.startswith('*Ez a blokk'):
            cnt('hatokor_szoveg')
            continue
        if re.match(r'^\*Forrás: `?konkordancia/', ln):
            cnt('forrasfajl_sor')
            continue
        if re.match(r'^\[\^\d+\]: proveniencia', ln):
            cnt('proveniencia_labjegyzet')
            continue
        n = len(re.findall(r'\[\^\d+\]', ln))
        if n:
            cnt('labjegyzet_jel', n)
            ln = re.sub(r'\[\^\d+\]', '', ln)
        if '*(kézi' in ln:
            cnt('kezi_cimke')
            ln = re.sub(r'\s*\*\(kézi[^)]*\)\*', '', ln)
        out.append(ln)
    # többszörös üres sor összevonása
    res = []
    for ln in out:
        if ln.strip() == '' and res and res[-1].strip() == '':
            continue
        res.append(ln)
    while res and res[0].strip() == '':
        res.pop(0)
    while res and res[-1].strip() == '':
        res.pop()
    return res


def idx(pred, start=0):
    for i in range(start, len(L)):
        if pred(L[i]):
            return i
    raise KeyError('nincs találat')


def h2(title):
    return idx(lambda s: s.startswith('## ') and s[3:].startswith(title))


def block(a, b):
    return L[a:b]


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def anchor(ref):
    a = ref.lower().replace(' ', '-').replace(':', '-')
    return 'v-' + a


KIEJT = {'epikaleō': 'epikaleó', 'kaleō': 'kaleó', 'boaō': 'boaó',
         'qa.ra': 'kárá', 'shem': 'sém'}


def kiejt(s):
    for k, v in KIEJT.items():
        if k in s:
            cnt('kiejtes_csere', s.count(k))
            s = s.replace(k, v)
    return s


# ---------- szakaszhatárok ----------
i_kiv = h2('Kivonat'); i_toc = h2('Tartalomjegyzék'); i_jel = h2('Jelmagyarázat')
i_elo = h2('1. Előfordulások'); i_1b = h2('1/b.'); i_2 = h2('2. Szótári')
i_3 = h2('3. LXX'); i_4 = h2('4. Kereszthiv'); i_5 = h2('5. Kapcsolatok')
i_6 = h2('6. Értelmezés'); i_7 = h2('7. Módszertan'); i_8 = h2('8. Irodalom')
i_kol = h2('Kolofon')
i_1a = idx(lambda s: s.startswith('#### 1/a.'), i_elo)
i_2b = idx(lambda s: s.startswith('### 2/b.'), i_2)
i_mf = idx(lambda s: s.startswith('### Miért fontos'), i_2b)
i_min = idx(lambda s: s.startswith('### Minősítés'), i_4)
i_alat = idx(lambda s: s.startswith('### Alátámasztás'), i_5)
i_rokon = idx(lambda s: s.startswith('### Rokon szavak'), i_2)

# ---------- törzsadat (kolofon) ----------
torzs = {}
for ln in block(i_kol, len(L)):
    if ln.startswith('| ') and not ln.startswith('| Mező') and not ln.startswith('| Forrás'):
        c = cells(ln)
        if len(c) == 2:
            torzs[c[0]] = c[1]
TORZS_KI = ['Forrás-study', 'Kereszthivatkozás-napló', 'Sablon-megfelelőség']
for k in TORZS_KI:
    if k in torzs:
        cnt('uzemeltetoi_torzsmezo')

# ---------- előfordulás-tábla ----------
elo = []
for ln in block(i_elo, i_1a):
    if ln.startswith('| [') :
        c = cells(re.sub(r'\[\^\d+\]', '', ln))
        ref = re.match(r'\[([^\]]+)\]', c[0]).group(1)
        elo.append(dict(ref=ref, kulcs=c[1], funkcio=c[2], szint=c[3], strong=c[4],
                        szotari=c[5], ubs=c[6], megb=c[7]))
ubs_megj = [ln for ln in block(i_elo, i_1a) if ln.startswith('*Az UBS-jelentés')]

# ---------- 1/a szövegek ----------
ige = {}
cur = None
for ln in block(i_1a + 1, i_1b):
    m = re.match(r'<a id="ige-[^"]+"></a>', ln)
    if m:
        cur = None
        continue
    m = re.match(r'^\*\*(.+?)\*\*$', ln)
    if m and cur is None:
        cur = m.group(1)
        ige[cur] = []
        continue
    if cur and not ln.startswith('<!--'):
        ige[cur].append(ln)
for k in ige:
    ige[k] = clean(ige[k])

# ---------- LXX ----------
lxx, lxx_ossz = {}, ''
for ln in block(i_3, i_4):
    if ln.startswith('| ') and not ln.startswith('| Igehely') and not ln.startswith('|---'):
        c = cells(ln)
        lxx[c[0]] = c
    if ln.startswith('*Összesítés'):
        lxx_ossz = ln

# ---------- kereszthivatkozások ----------
kh, cur = {}, None
for ln in block(i_4, i_min):
    m = re.match(r'^#### (.+)$', ln)
    if m:
        cur = m.group(1).strip()
        kh[cur] = []
        continue
    if cur and ln.startswith('- '):
        kh[cur].append(ln[2:])

# ---------- kapcsolatok ----------
kap, mermaid = [], []
blk = block(i_5, i_alat)
for ln in blk:
    if ln.startswith('| ') and not ln.startswith('| Forrás') and not ln.startswith('|---'):
        kap.append(cells(ln))
d0 = next(i for i, s in enumerate(blk) if s.startswith('<details>'))
d1 = next(i for i, s in enumerate(blk) if s.startswith('</details>'))
mermaid = blk[d0:d1 + 1]
alat = []
for ln in clean(block(i_alat + 1, i_6)):
    if ln.startswith('*(A nyers, gépileg'):
        cnt('uzemeltetoi_bekezdes')
        alat.append('@@SKIP')
        continue
    alat.append(ln)
# a "(A nyers ..." bekezdés több soros: a következő üres sorig kihagyjuk
alat2, skip = [], False
for ln in alat:
    if ln == '@@SKIP':
        skip = True
        continue
    if skip:
        if ln.strip() == '':
            skip = False
        continue
    alat2.append(ln)
alat = alat2

# ---------- szótári rész: generált szócikkek ----------
def parse_szocikkek(a, b, tok_lvl, sub_lvl):
    toks, cur, sub = [], None, None
    for ln in block(a, b):
        if ln.startswith(tok_lvl + ' ') and re.match(r'^#+ [GH]\d', ln):
            cur = dict(fej=ln[len(tok_lvl) + 1:], twot='', domen='', subs=[])
            toks.append(cur); sub = None
            continue
        if cur is None:
            continue
        if ln.startswith(sub_lvl + ' '):
            sub = dict(cim=ln[len(sub_lvl) + 1:], sorok=[])
            cur['subs'].append(sub)
            continue
        if sub is None:
            if ln.startswith('**TWOT:**'):
                cur['twot'] = ln.split('**', 2)[2].strip()
            elif ln.startswith('**Szemantikai domén:**'):
                cur['domen'] = ln.split('**', 2)[2].strip()
            continue
        if ln.startswith('<!--') or ln.startswith('### ') or ln.startswith('#### '):
            continue
        sub['sorok'].append(ln)
    for t in toks:
        for s in t['subs']:
            s['sorok'] = clean(s['sorok'])
    return toks


fo_tok = parse_szocikkek(i_2, i_rokon, '###', '####')
rokon_tok = parse_szocikkek(i_rokon, i_2b, '####', '#####')

# ---------- 2/b és "Miért fontos" darabolása ----------
b2 = block(i_2b, i_mf)


def para_from(lines, start_pred):
    i = next(k for k, s in enumerate(lines) if start_pred(s))
    j = i
    while j < len(lines) and lines[j].strip() != '':
        j += 1
    return lines[i:j]


kiemeles_h7121 = para_from(b2, lambda s: s.startswith('**Kiemelés jelentősége:**'))
gyok_h8034 = para_from(b2, lambda s: s.startswith('**Jelentősége:** a **"√ unknown"'))
lsj_jel = para_from(b2, lambda s: s.startswith('**Jelentősége:** a καλέω'))
lsj_epik = para_from(b2, lambda s: s.startswith('*(Az ἐπικαλέω'))
kereszt_elemzes = para_from(b2, lambda s: s.startswith('**Kereszt-elemzés'))
licenc_2b = para_from(b2, lambda s: s.startswith('*Források és licencek'))
sece_h7121 = para_from(b2, lambda s: s.startswith('**SECE H7121'))
sece_h8034 = para_from(b2, lambda s: s.startswith('**SECE H8034'))
tbesh_leiras = para_from(b2, lambda s: s.startswith('**TBESH.lexicon'))
cnt('duplikalt_szocikk_kihagyva', 2)  # LSJ G2564 és TBESH H7121 a 2/b-ben is szerepelt


def table_after(lines, head_pred):
    i = next(k for k, s in enumerate(lines) if head_pred(s))
    rows = []
    for s in lines[i + 1:]:
        if s.startswith('|'):
            if not s.startswith('|---'):
                rows.append(cells(s))
        elif rows:
            break
    return rows[1:]  # fejléc nélkül


mounce = {}
for c in table_after(b2, lambda s: s.startswith('**MCGED')):
    g = re.search(r'G(\d+)\)', c[0]).group(1).zfill(4)
    mounce['G' + g] = c
sece = {}
for c in table_after(b2, lambda s: s.startswith('**SECE (kibővített')):
    g = re.search(r'G(\d+)\)', c[0]).group(1).zfill(4)
    sece['G' + g] = c

mf = clean(block(i_mf + 1, i_3))


def mf_section(title):
    i = next(k for k, s in enumerate(mf) if s.startswith('#### ' + title))
    j = next((k for k in range(i + 1, len(mf)) if mf[k].startswith('#### ')), len(mf))
    return clean(mf[i + 1:j])


mf_g1941, mf_g0994, mf_modszer = mf_section('G1941'), mf_section('G0994'), mf_section('Kiemelt')

# ---------- kimenet ----------
O = []
w = O.append
cim = L[0].replace('# 📖 ', '# ')
w(cim); w('')
w('*Kereszthivatkozási törzscikk — ugyanannak a tartalomnak az olvasói nézete, mint a '
  '[tudományos lexikonoldal](ISTENTISZT-001_TUDOMANYOS.md).*')
w('')

# törzsadat-kártya
n_osz = sum(1 for e in elo if e['ubs'].startswith('— *(ÓSZ)*'))
w('| | |'); w('|---|---|')
for k in ['ID', 'Teljes cím', 'Rövid UI-címke', 'Téma', 'Azonosság típusa', 'PaRDeS-szint', 'Státusz']:
    if k in torzs:
        w('| **%s** | %s |' % (k, torzs[k]))
w('| **Igehelyek** | %d (%d ÓSZ / %d ÚSZ) |' % (len(elo), n_osz, len(elo) - n_osz))
w('| **Kapcsolatok** | %d |' % len(kap))
w('| **Fő szavak** | ἐπικαλέω (epikaleó, G1941) · קָרָא (kárá, H7121) · שֵׁם (sém, H8034) |')
w('| **Negatív kritérium** | %s |' % torzs.get('Negatív kritérium', ''))
w('| **Fölérendelt fogalom** | %s |' % torzs.get('Fölérendelt fogalom', ''))
w('')

w('## Kivonat'); w('')
O += clean(block(i_kiv + 1, i_toc)); w('')

w('## Tartalom'); w('')
for t, a in [('1. Igehelyek és kereszthivatkozások', '1-igehelyek-és-kereszthivatkozások'),
             ('2. Kapcsolatok', '2-kapcsolatok'),
             ('3. A kereszthivatkozások minősítése', '3-a-kereszthivatkozások-minősítése'),
             ('4. LXX-fordítói döntések', '4-lxx-fordítói-döntések'),
             ('5. Szótári háttér', '5-szótári-háttér'),
             ('6. Értelmezés', '6-értelmezés'),
             ('7. Módszertan és nyitott kérdések', '7-módszertan-és-nyitott-kérdések'),
             ('Jelmagyarázat', 'jelmagyarázat'), ('Források és licenc', 'források-és-licenc')]:
    w('- [%s](#%s)' % (t, a))
w('')

# 1. igehelyek
w('## 1. Igehelyek és kereszthivatkozások'); w('')
w('| Igehely | Funkció | PaRDeS-szint | Megbízhatóság |'); w('|---|---|---|---|')
for e in elo:
    w('| [%s](#%s) | %s | %s | %s |' % (e['ref'], anchor(e['ref']), e['funkcio'], e['szint'], e['megb']))
w('')
for s in ubs_megj:
    w(s)
w('')
kh_szam = 0
for e in elo:
    r = e['ref']
    w('<a id="%s"></a>' % anchor(r)); w('')
    w('### %s' % r); w('')
    t = ige.get(r, [])
    if t and t[0].startswith('*'):
        w('> ' + t[0]); w('')
        rest = t[1:]
    else:
        rest = t
    for s in rest:
        w(s + '  ' if s.strip() else s)
    w('')
    w('- **Kulcsszó:** %s' % e['kulcs'])
    w('- **Strong · szótári jelentés:** %s · %s' % (e['strong'], e['szotari']))
    if not e['ubs'].startswith('— *(ÓSZ)*'):
        w('- **UBS-jelentés:** %s' % e['ubs'])
    if r in lxx:
        c = lxx[r]
        w('- **LXX:** %s — %s — %s' % (c[1], kiejt(c[3]), c[4]))
    ki = [k for k in kap if k[0] == r]
    be = [k for k in kap if k[1] == r]
    if ki or be:
        parts = ['→ [%s](#%s) (%s, %s)' % (k[1], anchor(k[1]), k[2], k[4]) for k in ki]
        parts += ['← [%s](#%s) (%s, %s)' % (k[0], anchor(k[0]), k[2], k[4]) for k in be]
        w('- **Kapcsolatok:** ' + '; '.join(parts))
    if kh.get(r):
        tsk = [x[5:] for x in kh[r] if x.startswith('TSK: ')]
        kar = [x[len('Károli-KH: '):] for x in kh[r] if x.startswith('Károli-KH: ')]
        tsk = [re.sub(r' \(Votes: (\d+)\)', r' (\1)', x) for x in tsk]
        kh_szam += len(tsk) + len(kar)
        if tsk:
            w('- **TSK-kereszthivatkozás** (szavazatszám): ' + ', '.join(tsk))
        if kar:
            w('- **Károli-kereszthivatkozás:** ' + ', '.join(kar))
    w('')
stat['kereszthivatkozas_talalat'] = kh_szam

w('### Kizárt és vizsgált helyek'); w('')
for s in clean(block(i_1b + 1, i_2)):
    s = s.replace(' a `jeloltek.tsv`-ben', '').replace(' (`motivumok.tsv`)', '')
    w(s)
w('')

# 2. kapcsolatok
w('## 2. Kapcsolatok'); w('')
w('| Forrás | Cél | Típus | Funkció | Bizonyosság | PaRDeS-szint |'); w('|---|---|---|---|---|---|')
for k in kap:
    w('| [%s](#%s) | [%s](#%s) | %s |' % (k[0], anchor(k[0]), k[1], anchor(k[1]), ' | '.join(k[2:])))
w('')
O += mermaid; w('')
w('### Alátámasztás'); w('')
O += alat; w('')

# 3. minősítés
w('## 3. A kereszthivatkozások minősítése'); w('')
O += clean(block(i_min + 1, i_5)); w('')

# 4. LXX
w('## 4. LXX-fordítói döntések'); w('')
w('| Igehely (Károli) | LXX-igehely | Héber kulcsszó | Görög megfelelő | Egyezés |'); w('|---|---|---|---|---|')
for c in lxx.values():
    w('| [%s](#%s) | %s | %s | %s | %s |' % (c[0], anchor(c[0]), c[1], c[2], kiejt(c[3]), c[4]))
w('')
w(lxx_ossz.replace(', kutatói azonosítás függőben=0, szamozas_elteres=0', '')); w('')

# 5. szótári háttér — szerepkör-mátrix
w('## 5. Szótári háttér'); w('')
w('A szótárak szerepek szerint rendezve: minden kérdésre egy forrás felel, minden szónál azonos sorrendben.')
w('')
w('| Szerep | Görög szó | Héber szó |'); w('|---|---|---|')
w('| Alapjelentés | TBESG | BDB |')
w('| Mélységi szócikk | Thayer | — |')
w('| Jelentés-lista | — | TBESH |')
w('| Szemantikai mező | SDGNT (+ Louw–Nida: SECE) | SDBH |')
w('| Előfordulás és tömör jelentés | Mounce | — |')
w('| Megfelelők a másik nyelven | SECE (héber megfelelők) | SECE (görög megfelelők) |')
w('| Klasszikus háttér | LSJ, ha releváns | — |')
w('| Versenkénti jelentés | UBS (az 1. szakasz igehelyeinél) | — |')
w('')
w('### Áttekintés'); w('')
w('| Szó | Strong | TWOT | Alapjelentés | ÚSZ-előfordulás | Mélységi szócikk | Klasszikus háttér |')
w('|---|---|---|---|---|---|---|')


def fejresz(t):
    m = re.match(r'([GH]\d+) — (.+?) \((.+)\)', t['fej'])
    return m.group(1), m.group(2), kiejt(m.group(3))


def alapjel(t):
    return [s['cim'].split(' — ', 1)[1] for s in t['subs'] if s['cim'].startswith(('TBESG', 'BDB'))]


def van(t, pre):
    for s in t['subs']:
        if s['cim'].startswith(pre):
            return 'függőben' if any('Fordítás függőben' in x for x in s['sorok']) else 'lefordítva'
    return '—'


for t in fo_tok + rokon_tok:
    g, szo, kj = fejresz(t)
    rokon = ' *(rokon)*' if t in rokon_tok else ''
    mo = mounce.get(g)
    w('| [%s (%s)](#szo-%s)%s | %s | %s | %s | %s | %s | %s |' % (
        szo, kj, g.lower(), rokon, g, t['twot'] or '—', '; '.join(alapjel(t)) or '—',
        mo[1].replace('**', '') if mo else '—', van(t, 'Thayer'), 'LSJ' if van(t, 'LSJ') != '—' else '—'))
w('')

SORREND_G = [('Alapjelentés', 'TBESG'), ('Mélységi szócikk', 'Thayer')]
SORREND_H = [('Alapjelentés', 'BDB'), ('Jelentés-lista', 'TBESH')]
jelentoseg = {'G1941': mf_g1941 + [''] + lsj_epik, 'G0994': mf_g0994 + [''] + kereszt_elemzes,
              'G2564': lsj_jel, 'H7121': kiemeles_h7121, 'H8034': gyok_h8034}


def sub_ki(s, szerep):
    w('#### %s — %s' % (szerep, s['cim']))
    w('')
    for x in s['sorok']:
        w(x)
    w('')


for t in fo_tok + rokon_tok:
    g, szo, kj = fejresz(t)
    w('<a id="szo-%s"></a>' % g.lower()); w('')
    w('### %s (%s) — %s%s' % (szo, kj, g, ' · rokon szó' if t in rokon_tok else '')); w('')
    sorrend = SORREND_G if g.startswith('G') else SORREND_H
    for szerep, pre in sorrend:
        for s in [s for s in t['subs'] if s['cim'].startswith(pre)]:
            sub_ki(s, szerep)
            if pre == 'TBESH':
                cnt('uzemeltetoi_bekezdes')  # SQLite-verzió megjegyzés
    w('#### Szemantikai mező'); w('')
    w('- **%s:** %s' % ('SDGNT' if g.startswith('G') else 'SDBH', t['domen'] or '—'))
    if g in sece:
        w('- **Louw–Nida (SECE):** %s' % sece[g][1])
    w('')
    if g in mounce:
        mo = mounce[g]
        w('#### Előfordulás és tömör jelentés — Mounce'); w('')
        w('- %s az Újszövetségben; %s — magyarul: %s' % (mo[1].replace('**', ''), mo[2], mo[3])); w('')
    if g in sece:
        w('#### Héber megfelelők — SECE'); w('')
        w(sece[g][2]); w('')
    for s_ in [s_ for s_ in t['subs'] if s_['cim'].startswith('LSJ')]:
        sub_ki(s_, 'Klasszikus háttér')
    if g == 'H7121':
        w('#### Görög megfelelők — SECE'); w('')
        O.extend(sece_h7121); w('')
    if g == 'H8034':
        w('#### Görög megfelelők — SECE'); w('')
        O.extend(sece_h8034); w('')
    if jelentoseg.get(g):
        w('#### Jelentősége'); w('')
        O.extend(clean(jelentoseg[g])); w('')

w('### A három ige együtt'); w('')
O.extend(mf_modszer); w('')

# 6–7
w('## 6. Értelmezés'); w('')
O += [kiejt(x) if False else x for x in clean(block(i_6 + 1, i_7))]; w('')
w('## 7. Módszertan és nyitott kérdések'); w('')
O += clean(block(i_7 + 1, i_8)); w('')

# jelmagyarázat
w('## Jelmagyarázat'); w('')
jm = clean(block(i_jel + 1, i_elo))
out_jm, skip = [], False
for s in jm:
    if s.startswith('**PaRDeS-szintek**'):
        out_jm.append('**PaRDeS-szintek:**'); continue
    if s.startswith('**Funkció:**'):
        out_jm.append('**Funkció:** a vers szerepe a motívum ívében, a motívum saját tanulmányából átvett megnevezéssel.')
        skip = True; cnt('uzemeltetoi_bekezdes'); continue
    if skip:
        if s.strip() == '':
            skip = False; out_jm.append('')
        continue
    out_jm.append(s)
O += out_jm; w('')

# források és licenc
w('## Források és licenc'); w('')
w('**Hivatkozás:** %s — %s. Státusz: %s.' % (torzs.get('ID', ''), torzs.get('Teljes cím', ''), torzs.get('Státusz', '').replace('`', '')))
w('')
w('**Felhasznált szótárak és adatok:**'); w('')
for s in block(i_8, i_kol):
    if s.startswith('- ') and '(`konkordancia/' in s:
        lic = re.search(r', ([^,`]+)\)$', s)
        nev = re.sub(r' \(`konkordancia/.*$', '', s)
        w('%s — %s' % (nev, lic.group(1) if lic else ''))
        cnt('forrasfajl_utvonal')
w('- Károli Gáspár fordítása (1908) és a Károli-kereszthivatkozások — közkincs')
w('- SECE (kibővített Strong-szótár, Louw–Nida-doménekkel) — közkincs')
w('- Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary')
w('')
w('*LSJ: Liddell–Scott–Jones, Perseus Digital Library, CC BY-SA 3.0. A CC BY-SA forrásokból (SDBH, SDGNT, UBS, LSJ) készült magyar fordítások azonos licenc alatt használhatók.*')
w('')

SZAKASZ_MAP = [
    ('ezért a 2. szakasz generált része nem ad hozzá szócikket; LXX-beli szerepét a 3. szakasz mutatja',
     'ezért rokon szóként szerepel; LXX-beli szerepét a 4. szakasz mutatja'),
    ('adatrétege (1-4. szakasz)', 'adatrétege (1–5. szakasz)'),
    ('(l. 2/b. szakasz)', '(l. 5. szakasz)'),
    ('a 2. szakasz generált részében áll', 'az 5. szakaszban áll'),
    ('(1. szakasz, UBS-oszlop)', '(1. szakasz, UBS-jelentés)'),
]
for i, ln in enumerate(O):
    for a, b in SZAKASZ_MAP:
        if a in ln:
            O[i] = O[i].replace(a, b); cnt('szakaszhivatkozas_atirva'); ln = O[i]

res = []
for ln in O:
    if ln.strip() == '' and res and res[-1].strip() == '':
        continue
    res.append(ln)
open(OUT, 'w', encoding='utf-8').write('\n'.join(res).rstrip() + '\n')

stat['igehely'] = len(elo); stat['igehely_osz'] = n_osz; stat['kapcsolat'] = len(kap)
stat['lxx_sor'] = len(lxx); stat['szo_fo'] = len(fo_tok); stat['szo_rokon'] = len(rokon_tok)
stat['igehely_szoveg'] = len(ige)
with open(STAT, 'w', encoding='utf-8') as f:
    for k in sorted(stat):
        f.write('%s\t%s\n' % (k, stat[k]))
