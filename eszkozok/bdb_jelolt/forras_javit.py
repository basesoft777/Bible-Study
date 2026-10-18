#!/usr/bin/env python
"""A BDB forráshibáinak javítótáblája (F107, 5. lépés; DT-F107f (a), felhasználó, 2026-10-18).

Egyetlen hibaosztály (ma): `pe_mem` — a DictBDB.json a dagesses pét dagesses memként írja (0 dagesses pe a JSON-ban,
`naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 2.2). A tábla az `adat/bdb_szakaszok.tsv` `szoveg` mezőjének MINDEN dagesses
memjére egy sort ad (a szó és azon belül a dagesses mem sorszámával), és eldönti:

  javitva       a mem → pe cserével kapott alak az illesztett lexikon-szócikk héber szavai között áll
                (és a változatlan alak nem): a javított alak a SZABÁLYBÓL jön, a lexikon csak igazol (DT-F107a (i))
  valodi_mem    a változatlan (dagesses mem-es) alak áll a lexikon-szócikkben: nem hiba
  jelolt_marad  egyik sem igazolt (a szóalak a lexikonban eltér, vagy a sornak nincs bdb_id-je): nincs javítás

Összevetés: NFD, a kantilláció (U+0591–U+05AF), a meteg (U+05BD), a paszek/szof pászuk (U+05C0, U+05C3) és a
U+200E nélkül, a holem haser for vav (U+05BA) holemként (U+05B9).

A nyers fájl (DictBDB.json) és a szakasztábla NEM változik; a javítás alkalmazása a szöveg-nézetben a DT-F107c (6. lépés)
döntése. Kimenet: adat/bdb_forras_javitas.tsv (séma: adat/SEMA.md, „bdb_forras_javitas.tsv”).

Módok: (alap) írás · --ellenoriz bájtos összevetés a fájllal · --meres csak számok.
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sqlite3
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
LEX_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'BDB.lexicon')
KI_UT = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')

MEM, PE, DAG = 'מ', 'פ', 'ּ'
HEBER_SZO = re.compile(r'[֐-׿]+')
FEJLEC = ['strong', 'sorszam', 'bdb_id', 'hiba', 'szo_sorszam', 'elofordulas', 'forras_alak', 'javitott_alak',
          'allapot', 'indok', 'proveniencia']


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def kod_hash():
    with open(os.path.abspath(__file__), 'rb') as f:
        return hashlib.sha256(f.read().replace(b'\r\n', b'\n')).hexdigest()


def norm(szo):
    s = unicodedata.normalize('NFD', szo)
    s = ''.join(c for c in s if not ('֑' <= c <= '֯' or c in 'ֽ׀׃‎'))
    return s.replace('ֺ', 'ֹ')


def mem_dagesh_helyek(nfd):
    """A dagesses mem-ek indexei (a mem betű pozíciója) az NFD alakban."""
    helyek = []
    for i, c in enumerate(nfd):
        if c == MEM:
            j = i + 1
            while j < len(nfd) and '֑' <= nfd[j] <= 'ׇ':
                if nfd[j] == DAG:
                    helyek.append(i)
                    break
                j += 1
    return helyek


def cserel(nfd, helyek):
    s = list(nfd)
    for i in helyek:
        s[i] = PE
    return ''.join(s)


def lexikon_szavak():
    con = sqlite3.connect('file:' + LEX_UT.replace('\\', '/') + '?mode=ro', uri=True)
    ki = {}
    for t, d in con.execute("select Topic, Definition from Lexicon where Topic like 'BDB%'"):
        szoveg = re.sub(r'<[^>]+>', ' ', d)
        ki[t] = set(norm(w) for w in HEBER_SZO.findall(unicodedata.normalize('NFD', szoveg)))
    con.close()
    return ki


def tabla_sorok():
    with open(TABLA, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]


def general(ts):
    lex = lexikon_szavak()
    ki, stat = [], collections.Counter()
    prov = 'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc) | ts=%s'
    for r in tabla_sorok():
        szavak = HEBER_SZO.findall(unicodedata.normalize('NFD', r['szoveg']))
        for si, szo in enumerate(szavak, 1):
            helyek = mem_dagesh_helyek(szo)
            if not helyek:
                continue
            lszavak = lex.get(r['bdb_id'])
            for ei, h in enumerate(helyek, 1):
                egy = cserel(szo, [h])
                mind = cserel(szo, helyek)
                if lszavak is None:
                    allapot, jav, indok = 'jelolt_marad', '', 'a sornak nincs bdb_id-je (illesztes=%s): nincs igazoló szócikk' % r['illesztes']
                elif norm(egy) in lszavak and norm(szo) not in lszavak:
                    allapot, jav, indok = 'javitva', egy, 'a pe-s alak a %s szócikkben áll, a mem-es nem' % r['bdb_id']
                elif len(helyek) > 1 and norm(mind) in lszavak and norm(szo) not in lszavak:
                    allapot, jav, indok = 'javitva', mind, 'a szó minden dagesses memjét pére cserélve a %s szócikk alakja' % r['bdb_id']
                elif norm(szo) in lszavak:
                    allapot, jav, indok = 'valodi_mem', '', 'a dagesses mem-es alak a %s szócikkben áll: nem hiba' % r['bdb_id']
                else:
                    allapot, jav, indok = 'jelolt_marad', '', 'egyik alak sincs a %s szócikk héber szavai között' % r['bdb_id']
                stat[allapot] += 1
                ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'pe_mem', str(si), str(ei), szo, jav, allapot, indok,
                           prov % (r['strong'], ts)])
    ki.extend(kezi_sorok(stat))
    return ki, stat


# DT-F107g (b), felhasználó, 2026-10-18: a szerkezeti forráshibák (a jelölő a nyers forrásban hiányzik vagy hamis), mindegyik a
# DictBDB.json-ban ÉS a BDB.lexicon-ban igazolva (naplok/F107_BDB_JELOLT_SZOVEG_naplo.md 4.6). Kézi sorok: `allapot=kezi`,
# proveniencia `manual`. A `sorszam` a szakasztábla azon sora, amelynek `jel`+`szoveg`-e a horgonyt tartalmazza (az első);
# a `forras_alak` a nyers JSON rövid részlete, a `javitott_alak` a várt szerkezet (útvonal).
# (strong, horgony, hiba, forras_alak, javitott_alak, indok)
KEZI = [
    ('H0559', 'Qal Perfect', 'jelolo_hianyzik', '— Qal <i>Perfect</i> ׳א Gen 3:1', 'Qal',
     'a „Qal” törzsnév sima szöveg (nem félkövér) a DictBDB.json-ban és a BDB.lexicon-ban is; a törzsszint ezért a táblában '
     'nem nyílik meg (aranyminta: Qal, Qal/1–4; seed-101 M102)'),
    ('H0559', 'Say (subject God', 'jelolo_hianyzik', 'April, 1887, 263</sup>.1<i>Say</i>', 'Qal/1',
     'az „1” a DictBDB.json-ban sima szöveg a lapszám után; a BDB.lexicon ugyanitt jelöl: <div class="section"><p>1. Say '
     '(a JSON hibája, a lexikon igazolja; seed-101 M102)'),
    ('H0539', 'as abstract noun see', 'jelolo_hianyzik', 'see אֵמֻן. Niph`al נֶאֱמַן Prov 11:13', "Niph'al",
     'a „Niph`al” törzsnév sima szöveg mindkét forrásban (seed-101 M117)'),
    ('H0539', 'carried by a nurse', 'jelolo_hianyzik', 'Deut 28:59. 1.<i>carried</i>', "Niph'al/1",
     'az „1.” jelöletlen mindkét forrásban (a lexikonban „28:59. 1. carried”, a 2. pont már <div class="point">) (seed-101 M117)'),
    ('H3318', 'go or come out or forth', 'jelolo_hianyzik', '— </p><p><b>1</b> <i>go</i> or <i>come out</i>', 'Qal/1',
     'a „Qal” törzsnév az első törzs előtt mindkét forrásban hiányzik (lexikon: „— <div class="point"><b>1.</b> go or come '
     'out”) (seed-101 M162)'),
    ('H4900', 'trail seed', 'hamis_jelolo', 'compare </p><p><b>Niph`al 6.</b> <i>trail</i>', 'Qal/6',
     'a „compare Niph`al” hivatkozás törzsneve a 6. jelentés félkövér fejébe olvadt mindkét forrásban (lexikon: '
     '„compare </div><div class="point"><b>Niph`al 6.</b>”); a 6–7. jelentés a Qal-é (aranyminta: Qal/6, Qal/7)'),
    ('H1242', 'figurative of bright joy', 'hamis_jelolo', '<b>d.</b> above, &amp; below </p><p><b>2. g.</b>', '-/1/g',
     'a „2.” a g. alpont fejében téves mindkét forrásban (lexikon: <div class="point"><b>2. g.</b>); a g–h alpont az 1. '
     'jelentésé, a 2. jelentés később következik („morrow, next day”) (aranyminta: -/1/g, -/1/h)'),
]


def kezi_sorok(stat):
    sorok = tabla_sorok()
    ki = []
    for st, horgony, hiba, forras_alak, javitott, indok in KEZI:
        r = next((x for x in sorok if x['strong'] == st and horgony in (x['jel'] + ' ' + x['szoveg'])), None)
        if r is None:
            raise SystemExit('HIBA: a kézi sor horgonya nem található: %s %r' % (st, horgony))
        stat['kezi'] += 1
        ki.append([st, r['sorszam'], r['bdb_id'], hiba, '', '', forras_alak, javitott, 'kezi', indok, 'manual'])
    return ki


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/bdb_jelolt/forras_javit.py --ts %s — kézzel nem szerkesztendő (F107, DT-F107f (a); séma: adat/SEMA.md, bdb_forras_javitas.tsv). A héber alakok NFD-ben.' % ts,
           '# forras: adat/bdb_szakaszok.tsv@%s + konkordancia/lexikonok_nyers/BDB.lexicon@%s (csak igazolás) + kód@%s'
           % (sha256_fajl(TABLA)[:12], sha256_fajl(LEX_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    sorok, stat = general(a.ts)
    print('sor: %d (pe_mem + kezi); %s; érintett Strong (javitva): %d' % (
        len(sorok), dict(stat), len(set(s[0] for s in sorok if s[8] == 'javitva'))))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, a.ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            if f.read() != szoveg:
                print('ELTÉR: %s' % KI_UT)
                return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s' % KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
