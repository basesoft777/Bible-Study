#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
torzscikk_general.py -- RENDER_BRIEF.md R1.7 (G7): a kereszthivatkozási
törzscikk (`lexikon/[ID]_TORZSCIKK.md`) generátora.

A `motivumlog/lexikon_pilot/torzscikk_pilot.py` (D18: kiindulási alap, nem
célállapot) általánosítása mind a 8 motívumra: a MÁR MEGÍRT lexikonoldalt
(`lexikon/[ID]_TUDOMANYOS.md`, l. `lexikon_general.py`) olvassa vissza --
"render a renderből" (a pilot D1-D5, D7-D11, D13 döntése érvényes). Az 5.
szakasz a pilot régi szerepkör-mátrixa helyett a G6 szerepmátrixot
(`adat/szotar_szerepek.tsv`) és a motívum szavankénti lefedettségét mutatja
(G7); a régi 5. szakasz és a lábléc (D12/G7: a ténylegesen használt
forrásokra szűkítve) az egyetlen pont, ahol a pilot-diff megengedett (K9).

A kiejtés-transzliteráció (SBL-stílus -> magyaros, pl. epikaleō -> epikaleó)
NEM a RENDER tárgya (l. CLAUDE.md/RENDER_BRIEF.md "Nincs benne" -- a
`kiejtes.py` a SZOTAR_BRIEF.md dolga); a pilot KIEJT táblája ISMÉRT,
ISTENTISZT-001-specifikus javításokat tartalmazott -- ez itt megmarad
(a K9 pilot-diff ezekre a szavakra épp emiatt nem térhet el), de a többi
motívum egyéb szavaira NEM terjed ki: azok nyers (SBL-stílusú) alakban
jelennek meg, amíg a SZOTAR_BRIEF kiejtes.py-ja nem old meg egy általános
átírást.

TSV-olvasás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).

CLI: a `general.py --cel torzscikk` hívja (l. ott).
"""

import io
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import general as G
import lexikon_general as LG

ROOT = G.ROOT

# ISTENTISZT-001-specifikus, ismert SBL->magyaros kiejtés-javítások (a pilot
# öröksége, l. a modul docstringje). Új szó esetén nincs csere.
KIEJT = {'epikaleō': 'epikaleó', 'kaleō': 'kaleó', 'boaō': 'boaó',
         'qa.ra': 'kárá', 'shem': 'sém'}


def kiejt(s):
    for k, v in KIEJT.items():
        if k in s:
            s = s.replace(k, v)
    return s


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def anchor(ref):
    a = ref.lower().replace(' ', '-').replace(':', '-')
    return 'v-' + a


def clean(lines):
    """A kézi rész-szövegekben előforduló 【NAPLO...】 blokkok, GENERÁLT
    markerek, hatókör-sorok, forrás-sorok, lábjegyzet-jelek és *(kézi...)*
    címkék eltávolítása -- a pilot clean()-jének változatlan logikája."""
    out, in_naplo = [], False
    for ln in lines:
        if in_naplo:
            if '】' in ln:
                in_naplo = False
            continue
        if ln.lstrip().startswith('【NAPLO'):
            if '】' not in ln:
                in_naplo = True
            continue
        if ln.startswith('<!-- GENERÁLT') or ln.startswith('<!-- RÉS-'):
            continue
        if ln.startswith('*Ez a blokk'):
            continue
        if re.match(r'^\*Kézzel írandó', ln):
            # G7: "A helyőrző ... kimarad" -- még ki nem töltött (`lap`
            # forrású) rés helyőrző-prózája nem kerül a törzscikkbe.
            continue
        if re.match(r'^\*Forrás: `?konkordancia/', ln):
            continue
        if re.match(r'^\[\^\d+\]: proveniencia', ln):
            continue
        ln = re.sub(r'\[\^\d+\]', '', ln)
        ln = re.sub(r'\s*\*\(kézi[^)]*\)\*', '', ln)
        out.append(ln)
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


def _uzemeltetoi_bekezdes_nelkul(lines):
    """A pilot 'uzemeltetoi_bekezdes' szűrője: a '*(A nyers, gépileg' kezdetű
    (a nyers, gépi feldolgozásra utaló, olvasóknak nem szánt) bekezdés a
    következő üres sorig kimarad."""
    out, skip = [], False
    for ln in lines:
        if ln.startswith('*(A nyers, gépileg'):
            skip = True
            continue
        if skip:
            if ln.strip() == '':
                skip = False
            continue
        out.append(ln)
    return out


def idx(lines, pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]):
            return i
    raise KeyError('nincs találat a törzscikk-parszoláshoz (%r)' % pred)


def h2(lines, title):
    return idx(lines, lambda s: s.startswith('## ') and s[3:].startswith(title))


def torzscikk_szoveg(m, lex_szoveg, model):
    L = lex_szoveg.split('\n')

    i_kiv = h2(L, 'Kivonat'); i_toc = h2(L, 'Tartalomjegyzék'); i_jel = h2(L, 'Jelmagyarázat')
    i_elo = h2(L, '1. Előfordulások'); i_1b = h2(L, '1/b.'); i_2 = h2(L, '2. Szótári')
    i_3 = h2(L, '3. LXX'); i_4 = h2(L, '4. Kereszthiv'); i_5 = h2(L, '5. Kapcsolatok')
    i_6 = h2(L, '6. Értelmezés'); i_7 = h2(L, '7. Módszertan'); i_8 = h2(L, '8. Irodalom')
    i_kol = h2(L, 'Kolofon')
    i_1a = idx(L, lambda s: s.startswith('#### 1/a.'), i_elo)
    i_min = idx(L, lambda s: s.startswith('### Minősítés'), i_4)
    i_alat = idx(L, lambda s: s.startswith('### Alátámasztás'), i_5)

    def block(a, b):
        return L[a:b]

    # törzsadat (kolofon)
    torzs = {}
    for ln in block(i_kol, len(L)):
        if ln.startswith('| ') and not ln.startswith('| Mező') and not ln.startswith('| Forrás'):
            c = cells(ln)
            if len(c) == 2:
                torzs[c[0]] = c[1]

    # előfordulás-tábla
    elo = []
    for ln in block(i_elo, i_1a):
        if ln.startswith('| ['):
            c = cells(re.sub(r'\[\^\d+\]', '', ln))
            ref = re.match(r'\[([^\]]+)\]', c[0]).group(1)
            elo.append(dict(ref=ref, kulcs=c[1], funkcio=c[2], szint=c[3], strong=c[4],
                             szotari=c[5], ubs=c[6], megb=c[7]))
    ubs_megj = [ln for ln in block(i_elo, i_1a) if ln.startswith('*Az UBS-jelentés')]

    # 1/a szövegek
    ige = {}
    cur = None
    for ln in block(i_1a + 1, i_1b):
        if re.match(r'<a id="ige-[^"]+"></a>', ln):
            cur = None
            continue
        mm = re.match(r'^\*\*(.+?)\*\*$', ln)
        if mm and cur is None:
            cur = mm.group(1)
            ige[cur] = []
            continue
        if cur and not ln.startswith('<!--'):
            ige[cur].append(ln)
    for k in ige:
        ige[k] = clean(ige[k])

    # LXX
    lxx, lxx_ossz = {}, ''
    for ln in block(i_3, i_4):
        if ln.startswith('| ') and not ln.startswith('| Igehely') and not ln.startswith('|---'):
            c = cells(ln)
            lxx[c[0]] = c
        if ln.startswith('*Összesítés'):
            lxx_ossz = ln

    # kereszthivatkozások
    kh, cur = {}, None
    for ln in block(i_4, i_min):
        mm = re.match(r'^#### (.+)$', ln)
        if mm:
            cur = mm.group(1).strip()
            kh[cur] = []
            continue
        if cur and ln.startswith('- '):
            kh[cur].append(ln[2:])

    # kapcsolatok
    kap, mermaid = [], []
    blk = block(i_5, i_alat)
    for ln in blk:
        if ln.startswith('| ') and not ln.startswith('| Forrás') and not ln.startswith('|---'):
            kap.append(cells(ln))
    d0_candidates = [i for i, s in enumerate(blk) if s.startswith('<details>')]
    if d0_candidates:
        d0 = d0_candidates[0]
        d1 = next(i for i, s in enumerate(blk) if s.startswith('</details>'))
        mermaid = blk[d0:d1 + 1]
    alat = _uzemeltetoi_bekezdes_nelkul(clean(block(i_alat + 1, i_6)))

    # ---------- kimenet ----------
    O = []
    w = O.append
    cim = L[0].replace('# 📖 ', '# ')
    w(cim); w('')
    w('*Kereszthivatkozási törzscikk — ugyanannak a tartalomnak az olvasói nézete, mint a '
      '[tudományos lexikonoldal](%s_TUDOMANYOS.md).*' % m['id'])
    w('')

    n_osz = sum(1 for e in elo if e['ubs'].startswith('— *(ÓSZ)*'))
    w('| | |'); w('|---|---|')
    for k in ['ID', 'Teljes cím', 'Rövid UI-címke', 'Téma', 'Azonosság típusa', 'PaRDeS-szint', 'Státusz']:
        if k in torzs:
            w('| **%s** | %s |' % (k, torzs[k]))
    w('| **Igehelyek** | %d (%d ÓSZ / %d ÚSZ) |' % (len(elo), n_osz, len(elo) - n_osz))
    w('| **Kapcsolatok** | %d |' % len(kap))
    fo_szavak = []
    for token in model['tokenek']:
        lk = LG.lemma_kiejtes(token)
        if lk:
            lemma_nfc = unicodedata.normalize('NFC', lk[0])
            fo_szavak.append('%s (%s, %s)' % (lemma_nfc, kiejt(lk[1]), token))
        else:
            fo_szavak.append(token)
    if fo_szavak:
        w('| **Fő szavak** | %s |' % ' · '.join(fo_szavak))
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
                 ('5. Szótári háttér — szerepek és lefedettség', '5-szótári-háttér--szerepek-és-lefedettség'),
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

    w('### Kizárt és vizsgált helyek'); w('')
    for s in clean(block(i_1b + 1, i_2)):
        s = s.replace(' a `jeloltek.tsv`-ben', '').replace(' (`motivumok.tsv`)', '')
        w(s)
    w('')

    # 2. kapcsolatok
    w('## 2. Kapcsolatok'); w('')
    if kap:
        w('| Forrás | Cél | Típus | Funkció | Bizonyosság | PaRDeS-szint |'); w('|---|---|---|---|---|---|')
        for k in kap:
            w('| [%s](#%s) | [%s](#%s) | %s |' % (k[0], anchor(k[0]), k[1], anchor(k[1]), ' | '.join(k[2:])))
        w('')
        O += mermaid; w('')
    else:
        w('Nincs kapcsolat-sor a `kapcsolatok.tsv`-ben ehhez a motívumhoz.'); w('')
    w('### Alátámasztás'); w('')
    O += alat; w('')

    # 3. minősítés
    w('## 3. A kereszthivatkozások minősítése'); w('')
    O += clean(block(i_min + 1, i_5)); w('')

    # 4. LXX
    w('## 4. LXX-fordítói döntések'); w('')
    if lxx:
        w('| Igehely (Károli) | LXX-igehely | Héber kulcsszó | Görög megfelelő | Egyezés |'); w('|---|---|---|---|---|')
        for c in lxx.values():
            w('| [%s](#%s) | %s | %s | %s | %s |' % (c[0], anchor(c[0]), c[1], c[2], kiejt(c[3]), c[4]))
        w('')
        if lxx_ossz:
            w(lxx_ossz.replace(', kutatói azonosítás függőben=0, szamozas_elteres=0', '')); w('')
    else:
        w('A motívumnak nincs ÓSZ-i előfordulása, ezért az LXX-fordítói döntések szakasz üres.'); w('')

    # 5. szótári háttér -- szerepmátrix (G6) + lefedettség szavanként (G7)
    w('## 5. Szótári háttér — szerepek és lefedettség'); w('')
    w('A szerepek jelentése és mai forrása (`adat/szotar_szerepek.tsv`, RENDER_BRIEF.md G6):'); w('')
    w('| Szerep | Görög forrás | Héber forrás |'); w('|---|---|---|')
    gorog_szerepek = {r['szerep']: r for r in model['szerepek'] if r['nyelv'] == 'gorog'}
    heber_szerepek = {r['szerep']: r for r in model['szerepek'] if r['nyelv'] == 'heber'}
    szerep_sorrend = sorted(gorog_szerepek, key=lambda k: int(gorog_szerepek[k]['sorrend']))
    for szerep in szerep_sorrend:
        gr = gorog_szerepek[szerep]
        hr = heber_szerepek.get(szerep, {})
        w('| %s | %s | %s |' % (szerep, gr.get('forras', '—'), hr.get('forras', '—')))
    w('')

    w('### Lefedettség szavanként'); w('')
    w('A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b '
      'résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'); w('')
    fejlec_cellak = ['Szó'] + szerep_sorrend
    w('| ' + ' | '.join(fejlec_cellak) + ' |')
    w('|' + '---|' * len(fejlec_cellak))
    for token in model['tokenek']:
        nyelv = 'gorog' if token.startswith('G') else 'heber'
        szerepek = gorog_szerepek if nyelv == 'gorog' else heber_szerepek
        sor = [token]
        for szerep in szerep_sorrend:
            r = szerepek.get(szerep, {})
            if r.get('allapot') == 'adatosítva':
                sor.append(r.get('forras', '—'))
            elif m['id'] == 'ISTENTISZT-001' and szerep == 'Megfelelők a másik nyelven':
                sor.append('kézi (2/b)')
            else:
                sor.append('nincs adatosítva')
        w('| ' + ' | '.join(sor) + ' |')
    w('')

    # 6-7
    w('## 6. Értelmezés'); w('')
    O += clean(block(i_6 + 1, i_7)); w('')
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
            out_jm.append('**Funkció:** a vers szerepe a motívum ívében, a motívum saját '
                           'tanulmányából átvett megnevezéssel.')
            skip = True; continue
        if skip:
            if s.strip() == '':
                skip = False; out_jm.append('')
            continue
        out_jm.append(s)
    O += out_jm; w('')

    # források és licenc (a ténylegesen felhasznált forrásokra szűkítve, D12/G7)
    w('## Források és licenc'); w('')
    w('**Hivatkozás:** %s — %s. Státusz: %s.' % (
        torzs.get('ID', ''), torzs.get('Teljes cím', ''), torzs.get('Státusz', '').replace('`', '')))
    w('')
    w('**Felhasznált szótárak és adatok:**'); w('')
    for s in block(i_8, i_kol):
        if s.startswith('- ') and '(`konkordancia/' in s:
            lic = re.search(r', ([^,`]+)\)$', s)
            nev = re.sub(r' \(`konkordancia/.*$', '', s)
            w('%s — %s' % (nev, lic.group(1) if lic else ''))
    w('- Károli Gáspár fordítása (1908) és a Károli-kereszthivatkozások — közkincs')
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
                O[i] = O[i].replace(a, b)

    res = []
    for ln in O:
        if ln.strip() == '' and res and res[-1].strip() == '':
            continue
        res.append(ln)
    torzscikk_tartalom = '\n'.join(res).rstrip() + '\n'

    stat = {
        'igehely': len(elo), 'igehely_osz': n_osz, 'kapcsolat': len(kap),
        'lxx_sor': len(lxx), 'kereszthivatkozas_talalat': kh_szam,
    }
    return torzscikk_tartalom, stat


def run(args, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek):
    elof_id_szerint = G.elofordulasok_id_szerint(elofordulasok)
    kimenet_gyoker = (
        os.path.join(G.ROOT, 'lexikon') if (args.ir or args.ellenoriz)
        else os.path.join(args.kimenet, 'lexikon')
    )

    for m in motivumok:
        sorai = elof_id_szerint.get(m['id'], [])
        if not sorai:
            continue

        lex_path = os.path.join(G.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % m['id'])
        if not os.path.exists(lex_path):
            print('  %s: nincs lexikonoldal (%s) -- kihagyva' % (m['id'], lex_path), file=sys.stderr)
            continue
        with io.open(lex_path, encoding='utf-8', newline='') as f:
            lex_szoveg = f.read()

        model = LG.modell_epit(m, sorai, konyv_sorrend, hianyzo_konyvek, lexikon_szoveg=lex_szoveg)
        torzscikk_tartalom, stat = torzscikk_szoveg(m, lex_szoveg, model)

        cel_ut = os.path.join(kimenet_gyoker, '%s_TORZSCIKK.md' % m['id'])
        if args.ellenoriz:
            regi = None
            if os.path.exists(cel_ut):
                with io.open(cel_ut, encoding='utf-8', newline='') as f:
                    regi = f.read()
            allapot = 'változatlan lenne' if regi == torzscikk_tartalom else (
                'frissülne' if regi is not None else 'új fájl lenne')
            print('  %s: --ellenoriz, nincs írás (%s) -- igehely=%d (%d ÓSZ), '
                  'kapcsolat=%d, lxx_sor=%d, kereszthivatkozas=%d'
                  % (m['id'], allapot, stat['igehely'], stat['igehely_osz'],
                     stat['kapcsolat'], stat['lxx_sor'], stat['kereszthivatkozas_talalat']))
            continue

        os.makedirs(kimenet_gyoker, exist_ok=True)
        with io.open(cel_ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(torzscikk_tartalom)
        print('  %s: %s (%d bájt) -- igehely=%d (%d ÓSZ), kapcsolat=%d, lxx_sor=%d, kereszthivatkozas=%d'
              % (m['id'], os.path.relpath(cel_ut, ROOT), os.path.getsize(cel_ut),
                 stat['igehely'], stat['igehely_osz'], stat['kapcsolat'], stat['lxx_sor'],
                 stat['kereszthivatkozas_talalat']))
    return 0
