"""F212.1 — a lexikongenerátor olvasói sablonmondatainak kigyűjtése (csak olvas).

A generátor és a hozzá tartozó renderelők minden szöveges literálját (f-string esetén a konstans
részeket, a behelyettesített részt `{…}`-ként) AST-ből kigyűjti, és a HAMART-001 lapjának látható
szövegén (a `<!-- … -->` megjegyzések nélkül) soronként illeszti. Kimenet: TSV a stdout-ra:
modul, függvény, sor, sablon, találat_sorok, blokk(ok), első példa (sor:szöveg).

Futtatás: python naplok/F212_sablonmondat_kigyujt.py [--md] > <ideiglenes fájl>  (--md: a lista függeléke)
"""
import ast
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULOK = ['lexikon_general.py', 'olvasoi_kovetkeztetes.py', 'olvasoi_utofeldolg.py', 'tablajegyzet.py',
           'szotari_glossza.py', 'kiejtes_szoveg.py', 'bdb_tagolas.py', 'szerep_karoli.py', 'szerep_nave.py',
           'szerep_kizart.py', 'nyilt_mag_export.py', 'general.py']
LAP = os.path.join(GYOKER, 'lexikon', 'HAMART-001_TUDOMANYOS.md')
HELY = '\x00'
MIN_LITERAL = 6       # ennyi betűnél rövidebb összes konstans rész: túl általános az illesztéshez


def sablonok(modul):
    fa = ast.parse(open(os.path.join(GYOKER, 'eszkozok', modul), encoding='utf-8').read())
    ki = []

    def bejar(csomo, fv, docstr_ids):
        for gy in ast.iter_child_nodes(csomo):
            uj_fv = fv
            if isinstance(gy, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                uj_fv = gy.name if fv == '<modul>' else fv + '.' + gy.name
                if gy.body and isinstance(gy.body[0], ast.Expr) and isinstance(gy.body[0].value, ast.Constant):
                    docstr_ids.add(id(gy.body[0].value))
            elif isinstance(gy, ast.Assign) and fv == '<modul>':
                nevek = [t.id for t in gy.targets if isinstance(t, ast.Name)]
                if nevek:
                    uj_fv = nevek[0]
            if isinstance(gy, ast.JoinedStr):
                reszek = []
                for r in gy.values:
                    if isinstance(r, ast.Constant) and isinstance(r.value, str):
                        reszek.append(r.value)
                    else:
                        reszek.append(HELY)
                ki.append((uj_fv, gy.lineno, ''.join(reszek)))
                continue  # a belső Constant-okat már kezeltük
            if isinstance(gy, ast.Constant) and isinstance(gy.value, str) and id(gy) not in docstr_ids:
                ki.append((uj_fv, gy.lineno, gy.value))
            bejar(gy, uj_fv, docstr_ids)

    d = set()
    if fa.body and isinstance(fa.body[0], ast.Expr) and isinstance(fa.body[0].value, ast.Constant):
        d.add(id(fa.body[0].value))
    bejar(fa, '<modul>', d)
    return ki


def lap_sorai():
    sorok = open(LAP, encoding='utf-8').read().split('\n')
    lathato, blokk = [], []
    akt_gen, akt_cim = '', ''
    for s in sorok:
        m = re.search(r'GENERÁLT-KEZDET: general\.py --cel lexikon#[^#]+#(\w+)', s)
        if m:
            akt_gen = m.group(1)
        m = re.search(r'GENERÁLT-RÉS: (\w+)', s)
        if m:
            akt_gen = 'rés:' + m.group(1)
        if re.match(r'^## ', s):
            akt_cim = s[3:].strip()[:40]
            if 'GENERÁLT' not in s:
                pass
        if 'GENERÁLT-VÉGE' in s:
            blokk.append((akt_cim, akt_gen))
            lathato.append('')
            akt_gen = ''
            continue
        tiszta = re.sub(r'<!--.*?-->', '', s)
        lathato.append(tiszta)
        blokk.append((akt_cim, akt_gen))
    return lathato, blokk


PCT = re.compile(r'%(?:\(\w+\))?[-+ #0]*\d*(?:\.\d+)?[sdifr]|\{[\w.\[\]]*(?:![rs])?(?::[^{}]*)?\}')


def normal(sablon):
    """A %-os és a .format-os helyőrzők is `{…}`-nek számítanak (a f-stringé már az)."""
    return PCT.sub(HELY, sablon)


def minta(sablon):
    sablon = normal(sablon)
    reszek = [r for r in sablon.split(HELY)]
    konst = [r.strip() for r in reszek if r.strip()]
    if sum(len(re.sub(r'[\W\d_]', '', r)) for r in konst) < MIN_LITERAL:
        return None
    if '\n' in sablon.strip('\n') and len(sablon) > 400:
        # többsoros nagy blokk: soronként illesztjük az első érdemi sorát
        pass
    darabok = []
    for r in konst:
        for sor in r.split('\n'):
            sor = sor.strip()
            if len(re.sub(r'[\W\d_]', '', sor)) >= 3:
                darabok.append(sor)
    if not darabok:
        return None
    # olvasói sablon: legalább két szó egy darabon belül, vagy címke (kettőspont / kiemelés / címsor)
    szavas = any(len(re.findall(r'[^\W\d_]{2,}', d)) >= 2 for d in darabok)
    cimke = any(re.search(r'[^\W\d_]{3,}\s*:\s*$|^\*\*?[^*]+\*\*?|^#+ ', d) for d in darabok)
    if not (szavas or cimke):
        return None
    # soronkénti illesztés: a leghosszabb darab kell, hogy egy sorban álljon
    return max(darabok, key=len), darabok


def gyujt():
    """A lapra illeszkedő sablonok sorai és a statisztika (vizsgált, olvasói alakú, illeszkedő literál)."""
    lathato, blokk = lap_sorai()
    sorok, stat = [], {'literal': 0, 'olvasoi': 0, 'illeszkedo': 0}
    for modul in MODULOK:
        for fv, sor, sab in sablonok(modul):
            stat['literal'] += 1
            if not re.search(r'[a-záéíóöőúüű]{3}', sab, re.I):
                continue
            mt = minta(sab)
            if not mt:
                continue
            stat['olvasoi'] += 1
            fo, darabok = mt
            sab = normal(sab)
            talalat = [i for i, t in enumerate(lathato) if fo in t]
            # többrészes egysoros sablon: a darabok sorrendben, egy sorban
            if len(darabok) > 1 and '\n' not in sab.strip('\n'):
                rx = re.compile('.*?'.join(re.escape(d) for d in darabok))
                talalat = [i for i in talalat if rx.search(lathato[i])]
            if not talalat:
                continue
            stat['illeszkedo'] += 1
            blokkok = []
            for i in talalat:
                b = (blokk[i][1] or '—') + ' | ' + blokk[i][0]
                if b not in blokkok:
                    blokkok.append(b)
            sorok.append({'modul': modul, 'fv': fv, 'sor': sor,
                          'sablon': sab.replace(HELY, '{…}').replace('\n', '⏎').replace('\t', ' '),
                          'db': len(talalat), 'blokkok': blokkok, 'elso': talalat[0] + 1,
                          'pelda': lathato[talalat[0]].strip().replace('\t', ' ')})
    return sorok, stat


def md_cella(t, n):
    t = t if len(t) <= n else t[:n - 1] + '…'
    return t.replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')


def main():
    sorok, stat = gyujt()
    if '--md' not in sys.argv:
        for r in sorok:
            print('\t'.join([r['modul'], r['fv'], str(r['sor']), r['sablon'], str(r['db']), ' ; '.join(r['blokkok']),
                             '%d: %s' % (r['elso'], r['pelda'][:300])]))
        print('literál %(literal)d · olvasói alakú %(olvasoi)d · a lapra illeszkedő %(illeszkedo)d' % stat,
              file=sys.stderr)
        return
    # markdown: sablononként egy sor (azonos szövegű literál összevonva), a lap szakaszai szerint
    egyedi = {}
    for r in sorok:
        iro = '%s:%s:%d' % (r['modul'][:-3], r['fv'], r['sor'])
        if r['sablon'] in egyedi:
            egyedi[r['sablon']]['irok'].append(iro)
            continue
        r['irok'] = [iro]
        egyedi[r['sablon']] = r
    rend = sorted(egyedi.values(), key=lambda r: r['elso'])
    print('*Gépi kigyűjtés (`naplok/F212_sablonmondat_kigyujt.py --md`): %d szöveges literál %d modulban; '
          'ebből %d olvasói alakú (legalább két szó vagy címke); ebből %d illeszkedik a HAMART-001 lap látható '
          'szövegére, %d különböző szöveggel.*\n' % (stat['literal'], len(MODULOK), stat['olvasoi'],
                                                    stat['illeszkedo'], len(rend)))

    def szakasz_nev(r):
        return r['blokkok'][0].split(' | ')[1] or '(a lap feje)'

    szakasz = None
    n = 0
    for r in rend:
        sz = szakasz_nev(r)
        if sz != szakasz:
            if szakasz is not None:
                print('\n</details>\n')
            szakasz = sz
            db = sum(1 for x in rend if szakasz_nev(x) == sz)
            print('<details><summary><strong>%s</strong> — %d sablon</summary>\n' % (md_cella(sz, 60), db))
            print('| # | Sablon | Db | Blokk | Író (modul:függvény:sor) | Példa (lapsor: szöveg) |')
            print('|---|---|---|---|---|---|')
        n += 1
        blk = ', '.join(sorted({b.split(' | ')[0] for b in r['blokkok']}))
        print('| %d | %s | %d | %s | %s | %s |' % (
            n, md_cella(r['sablon'], 110), r['db'], md_cella(blk, 40), md_cella(' · '.join(r['irok'][:3]), 80),
            md_cella('%d: %s' % (r['elso'], r['pelda']), 150)))
    print('\n</details>')


if __name__ == '__main__':
    main()
