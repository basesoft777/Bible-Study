#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bdb_konyvfeloldas_javit.py — F240.L7: a BDB-szöveg rosszul feloldott könyvhivatkozásai („Joel 1Sam 4:13”).

A BDB a hivatkozás könyvét rövidítéssel adja (Jo, Is, Am, Jb …); a forrás (`konkordancia/BDB_teljes_unabridged.tsv`,
a DictBDB.json alapján) ezt néhol szóként hagyta meg, és utána egy rosszul feloldott hivatkozás áll: „בָּשַׁל Joel 1Sam
4:13” (helyesen Joel 4:13). Az olvasó így hamis igehelyet lát, és a jelentés-fejléc a könyvszónál vág (F240 L3 maradéka).
Az F46 (`bdb_konyv_javit.py`) könyvfeloldási javítása ezeket nem fogta meg, mert az igazolására használt OpenScriptures-
kivonat (`konkordancia/OSHL_BDB_igehelyek.tsv`, 2 814 Strong) nem fedi őket (D11–D13).

Igazolás (D12): elsődleges tanú az OpenScriptures BDB-XML (openscriptures/HebrewLexicon @ 21c9add, CC BY 4.0), ahol a
hely ott jelölt; a második a TAHOT: a hivatkozott szó Strongja a javított (Károli-számozású) versben áll, a hibásban nem.
Ahol egyik sem dönt egyértelműen, nincs javítás: a hely a kivétellistára kerül `nem_eldontheto` jelöléssel (D11 (2)).

A javítás a forrásban történik (pozícióhoz kötött, egyedi szövegcsere), onnan halad tovább, mint az L3-ban
(`bdb_konyvketto_javit.py`): a szakasz-nézet javítótáblája a `forras_javit.py` újrafuttatásával követi; a magyar fordítás
(`adat/forditasok.tsv`) ugyanazon a helyen javul, a `forras_hash` a friss sorokon frissül, fizetős újrafordítás nélkül.
Kapu: `ellenoriz.py` 49. szabály (`konyvfeloldas_maradek`): a teljes táblán a „könyvszó + más könyv hivatkozása” minta minden
előfordulása vagy javítva van, vagy a `KIVETEL` listán áll, egy sor indokkal.

Futtatás a repó gyökeréből:
    python eszkozok/bdb_konyvfeloldas_javit.py            # száraz: mit cserélne, és mi marad a mintából
    python eszkozok/bdb_konyvfeloldas_javit.py --ir       # forrás + javítótábla + fordítás + napló
I/O: split('\\t') / '\\t'.join (csv modul nélkül); írás előtt sor-összevetés.
"""
import argparse
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_konyvketto_javit as KK  # noqa: E402

GYOKER = KK.GYOKER
NAPLO = os.path.join(GYOKER, 'naplok', 'LXXBDB_konyvfeloldas_csere.tsv')
VJ_TS = '2026-11-10'   # a vers -> jelentés tábla rögzített ts-e (a fejléc szerint)

# (Strong, angol régi, angol új, [(magyar régi, magyar új)], tanú)
CSERE = [
    ('H1310', 'Joel 1Sam 4:13', 'Joel 4:13', [('Jóel 1Sám 4:13', 'Jóel 4:13')],
     'TAHOT: H1310 a Jóel 3:13-ban (MT 4:13) áll, az 1Sám 4:13-ban nem'),
    ('H2505', 'Joel 1Chr 4:2', 'Joel 4:2', [('Joel 1Krón 4:2', 'Jóel 4:2')],
     'TAHOT: H2505 a Jóel 3:2-ben (MT 4:2) áll, az 1Krón 4:2-ben nem'),
    ('H3092', 'Joel 1Chr 4:2', 'Joel 4:2', [('Joel 1Krón 4:2', 'Jóel 4:2'), ('Jóel 1Krón 4:2', 'Jóel 4:2')],
     'TAHOT: H3092 a Jóel 3:2-ben (MT 4:2) áll, az 1Krón 4:2-ben nem'),
    ('H4649', 'Isa 1Chr 16:4', 'Isa 16:4', [('Ézs 1Krón 16:4', 'Ézs 16:4')],
     'OpenScriptures BDB-XML (m.bw.ab: „מֵץ … only הַמֵּץ Is 16:4”); TAHOT: H4160 az Ézs 16:4-ben'),
    ('H0689', 'for Amos Deut 8:8', 'for Amos 8:8', [('Ámós 5Móz 8:8', 'Ámós 8:8')],
     'TAHOT: H2975 (יְאֹר) az Ámós 8:8-ban áll, az 5Móz 8:8-ban nem'),
    ('H4136', 'Joel Josh 8:33', 'Josh 8:33', [('Jóel Józs 8:33', 'Józs 8:33')],
     'TAHOT: H4136 a Józs 8:33-ban áll; a „Joel” fölös könyvszó'),
    ('H5186', 'against Joel Jer 51:25', 'against Jer 51:25', [('Joel Jer 51:25', 'Jer 51:25')],
     'TAHOT: H5186 a Jer 51:25-ben áll; a „Joel” fölös könyvszó'),
    ('H5327', 'Lev Jer 1:16', 'Lev 1:16', [('3Móz Jer 1:16', '3Móz 1:16')],
     'TAHOT: H5133 (נוֹצָה) a 3Móz 1:16-ban áll, a Jer 1:16-ban nem'),
    ('H2023', 'CanaanNum Ezek 20:22', 'Canaan Num 20:22', [('4Móz Ez 20:22', '4Móz 20:22')],
     'TAHOT: H2023 a 4Móz 20:22-ben áll, az Ez 20:22-ben nem'),
    ('H4673', 'feetJosh Isa 4:3', 'feet Josh 4:3', [('Józs Ézs 4:3', 'Józs 4:3')],
     'TAHOT: H4673 a Józs 4:3-ban áll, az Ézs 4:3-ban nem'),
    ('H6981', 'Levites: 1 Chron Judg 9:19', 'Levites: 1 1Chr 9:19', [('1Krón Bír 9:19', '1Krón 9:19')],
     'TAHOT: H6981 az 1Krón 9:19-ben áll, a Bír 9:19-ben nem'),
    ('H7655', 'pluralEzra Dan 7:14', 'plural Ezra 7:14', [('Ezsd Dán 7:14', 'Ezsd 7:14')],
     'TAHOT: H7655 az Ezsd 7:14-ben áll, a Dán 7:14-ben nem'),
    ('H7655', '3:19 seven times', 'Dan 3:19 seven times', [('3:19 hétszer', 'Dán 3:19 hétszer')],
     'a csupasz „3:19” eddig a Dánt örökölte; az Ezra 7:14 javítás után kiírt könyv kell. TAHOT: H7655 a Dán 3:19-ben (javítókör)'),
    ('H7650', 'by me Psalms; Psa 102:9', 'by me Psa 102:9', [('Zsoltárok; Zsolt 102:9', 'Zsolt 102:9')],
     'kettőzött könyvszó (ψ → „Psalms;”, F240 L3 mintája); TAHOT: H7650 a Zsolt 102:9-ben'),
    ('H4161', 'marchNum 2Chr 33:2', 'march Num 33:2', [('helye4Móz 2Krón 33:2', 'helye 4Móz 33:2')],
     'TAHOT: H4161 a 4Móz 33:2-ben áll, a 2Krón 33:2-ben nem'),
    ('H4196', '30, Songs 2Chr 4:1', '30, 2Chr 4:1', [('30, Én 2Krón 4:1', '30, 2Krón 4:1')],
     'TAHOT: H4196 a 2Krón 4:1-ben áll; a „Songs” fölös könyvszó'),
    ('H1740', 'Ezek 40:38, Songs 2Chr 4:6', 'Ezek 40:38, 2Chr 4:6', [('Ez 40:38, Énekek 2Krón 4:6', 'Ez 40:38, 2Krón 4:6')],
     'TAHOT: H1740 a 2Krón 4:6-ban áll; a „Songs” fölös könyvszó'),
    ('H4709', 'exceptHos Josh 5:1', 'except Hos 5:1', [('kivéveHós Józs 5:1', 'kivéve Hós 5:1')],
     'TAHOT: H4709 a Hós 5:1-ben áll, a Józs 5:1-ben nem (javítókör)'),
    ('H1962', 'Hab Micah 6:2', 'Job 6:2', [('Hab Mik 6:2', 'Jób 6:2')],
     'OpenScriptures-kivonat (OSHL_BDB_igehelyek: H1962 Jób 6:2); a szócikk saját szövege („הַיָּתִי Job 6:2 Kt”); TAHOT: H1942 a Jób 6:2-ben (javítókör)'),
    ('H5920', 'Psalm 1Sam 2:10', '1Sam 2:10', [('Zsolt 1Sám 2:10', '1Sám 2:10')],
     'TAHOT: H5921 (az עַל ragozott alakja) az 1Sám 2:10-ben; a „Psalm” fölös könyvszó (javítókör)'),
]

# A minta nem hiba-előfordulásai: (Strong, fejezet:vers) → indok
KIVETEL = {
    ('H0295', '1:12'): 'személynév: „a chief of Dan” (Dán törzse)',
    ('H0357', '19:42'): 'helynév: „city in Dan” (Dán törzsének területe)',
    ('H0573', '14:25'): 'személynév: „the prophet Jonah”',
    ('H0884', '21:2'): 'helynév: „from Beersheba to Dan”',
    ('H1405', '19:44'): 'helynév: „assigned to Dan”',
    ('H1482', '33:22'): 'személynév: „of Dan” (Dán törzse)',
    ('H1667', '19:45'): 'helynév: „a location in Dan”',
    ('H3020', '34:22'): 'személynév: „chief of tribe of Dan”',
    ('H3494', '19:42'): 'helynév: „a location in (Southern) Dan”',
    ('H5175', '49:17'): 'személynév: „figurative of Dan”',
    ('H5905', '19:41'): 'helynév: „assigned to Dan”',
    ('H2518', '4:8'): 'személynév: „contemp. of Ezra”; a „Neh 4:8” maga számcsere-gyanús (TAHOT: H2518 a Neh 8:4-ben) — más hibaosztály, nyitott tétel',
    ('H3226', '8:7'): 'személynév: „time of Ezra” (Neh 8:7: Jámin)',
    ('H0223', '8:33'): 'személynév: „priest in time of Nehemiah” (Ezsd 8:33)',
    ('H0520', '3:3'): 'közszó: „all numbers” (számok), nem Numbers könyve',
    ('H3290', '26:42'): 'a BDB darabszám-összegzése („3t. Jeremiah”), utána új hivatkozás (Lev 26:42)',
    ('H3548', '1:1'): 'személynév: „of Joshua” (Józsué főpap, Hag 1:1)',
    ('H6290', '12:16'): 'közszó: „in Exodus” (a kivonulás), nem Exodus könyve',
    ('H1888', '2:9'): 'a „Jer” a Jeruzsálemi targum jele (ᵑ7^Jer), nem Jeremiás könyve',
    ('H5439', '3:11'): 'a „Psalms,” a forrásban hivatkozás nélküli ψ-jel; a hivatkozás (Amos 3:11) helyes (TAHOT: H5439 az Ámós 3:11-ben)',
}

TELJES_NEV = {'Genesis': 'Gen', 'Exodus': 'Exod', 'Leviticus': 'Lev', 'Numbers': 'Num', 'Deuteronomy': 'Deut', 'Joshua': 'Josh',
              'Judges': 'Judg', 'Nehemiah': 'Neh', 'Esther': 'Est', 'Psalm': 'Psa', 'Psalms': 'Psa', 'Paslm': 'Psa', 'Proverbs': 'Prov',
              'Ecclesiastes': 'Eccl', 'Isaiah': 'Isa', 'Jeremiah': 'Jer', 'Lamentations': 'Lam', 'Ezekiel': 'Ezek', 'Daniel': 'Dan',
              'Obadiah': 'Obad', 'Micah': 'Mic', 'Nahum': 'Nah', 'Habakkuk': 'Hab', 'Zephaniah': 'Zeph', 'Haggai': 'Hag',
              'Zechariah': 'Zech', 'Malachi': 'Mal', 'Songs': 'Song', 'Hos': 'Hosea', '1 Chron': '1Chr', '2 Chron': '2Chr', 'Esth': 'Est'}
_SZO = '|'.join(sorted(set(KK.REF.replace('Esth?', 'Esth|Est').split('|')) | set(TELJES_NEV), key=len, reverse=True))
# könyvszó (önállóan vagy az előző szóhoz tapadva), majd szóköz és MÁS könyv hivatkozása; írásjel után nem (a BDB
# darabszám-összegzése, „16t. Daniel; Ezra 5:11”, nem hiba)
EN_MINTA = re.compile(r'(?:(?<=[a-z])|(?<![\w`^]))(' + _SZO + r') (' + KK.REF + r') (\d+:\d+)')
HU_KONYV = sorted(set(KK.HU.values()), key=len, reverse=True)
HU_MINTA = re.compile(r'(?:(?<=[a-záéíóöőúüű])|(?<![\w]))(%s|Zsoltárok|Zsoltár|Énekek|Joel) (%s) (\d+:\d+)' % ('|'.join(map(re.escape, HU_KONYV)),
                                                                                 '|'.join(map(re.escape, HU_KONYV))))


def _kod(szo):
    return TELJES_NEV.get(szo, szo).replace('Esth', 'Est')


def en_maradek(strong, t):
    """[(c:v, szövegrész)] a minta nem kivételes előfordulásai egy angol szócikkben."""
    ki = []
    for m in EN_MINTA.finditer(t):
        a, b, cv = m.groups()
        if _kod(a) == b.replace('Esth', 'Est') or a in KK.KONYVSZO.get(b, ()):
            continue          # kettőzés: az L3 kapuja (47.) méri
        if (strong, cv) in KIVETEL:
            continue
        ki.append((cv, t[max(0, m.start() - 25):m.end()]))
    return ki


def hu_maradek(strong, t):
    ki = []
    for m in HU_MINTA.finditer(t):
        a, b, cv = m.groups()
        if a == b or (b == 'Zsolt' and a in ('Zsoltár', 'Zsoltárok')) or (a, b) == ('Joel', 'Jóel'):
            continue          # kettőzés: a 47. kapu méri
        if (strong, cv) in KIVETEL:
            continue
        ki.append((cv, t[max(0, m.start() - 25):m.end()]))
    return ki


def maradek(gyoker=GYOKER):
    """(angol, magyar) maradék-listák a teljes táblán: [(Strong, c:v, szövegrész)]."""
    en, hu = [], []
    with open(os.path.join(gyoker, 'konkordancia', 'BDB_teljes_unabridged.tsv'), encoding='utf-8') as f:
        for sor in f:
            p = sor.rstrip('\n').rstrip('\r').split('\t')
            if len(p) >= 3 and p[0] != 'Strong_padded':
                en += [(p[0], cv, x) for cv, x in en_maradek(p[0], p[-1])]
    sorok = KK.tsv(os.path.join(gyoker, 'adat', 'forditasok.tsv'))
    fej = next(s for s in sorok if s.startswith('szotar\t')).split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    for s in sorok:
        if s.startswith('BDB\t'):
            p = s.split('\t')
            hu += [(p[ix['strong']], cv, x) for cv, x in hu_maradek(p[ix['strong']], p[ix['forditas_hu']])]
    return en, hu


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ir', action='store_true')
    a = ap.parse_args()
    f_sorok = KK.tsv(KK.FORRAS)
    poz = {s.split('\t')[0]: i for i, s in enumerate(f_sorok) if s and not s.startswith('Strong_padded')}
    en_uj, erintett, alkalmazott = {}, set(), set()
    for k, (st, regi, uj, _hu, _t) in enumerate(CSERE):
        i = poz[st]
        p = f_sorok[i].split('\t')
        t = en_uj.get(i, (p, p[-1]))[1]
        if uj in t:
            continue          # már javítva (újrafuttatás; az új szöveg a régit is tartalmazhatja)
        if t.count(regi) != 1:
            sys.exit('%s: az angol régi szöveg nem egyszer áll (%d): %s' % (st, t.count(regi), regi))
        en_uj[i] = (p, t.replace(regi, uj))
        erintett.add(st)
        alkalmazott.add(k)
    fsor = KK.tsv(KK.FORD)
    fej = next(s for s in fsor if s.startswith('szotar\t')).split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    hu_uj, hu_db = {}, 0
    for k, (st, _r, _u, hu, _t) in enumerate(CSERE):
        if k not in alkalmazott:
            continue
        talalt = 0
        for i, s in enumerate(fsor):
            if not s.startswith('BDB\t'):
                continue
            p = hu_uj.get(i, s.split('\t'))
            if p[ix['strong']] != st:
                continue
            for hr, hn in hu:
                n = p[ix['forditas_hu']].count(hr)
                if n:
                    p[ix['forditas_hu']] = p[ix['forditas_hu']].replace(hr, hn)
                    talalt += n
                    hu_uj[i] = p
        if not talalt:
            sys.exit('%s: a magyar fordításban a régi alak nem található' % st)
        hu_db += talalt
    print('angol: %d csere %d szócikkben; magyar: %d csere %d sorban' % (len(CSERE), len(erintett), hu_db, len(hu_uj)))
    if not a.ir:
        en, hu = maradek()
        print('a minta maradéka a kivételeken kívül (a mostani állapoton): angol %d, magyar %d' % (len(en), len(hu)))
        for x in en[:40]:
            print('  EN', x)
        for x in hu[:40]:
            print('  HU', x)
        return
    # a csere-napló a forras_javit előtt kell (a javítósorok forrás-attribúciója ebből jön)
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/bdb_konyvfeloldas_javit.py --ir (F240.L7) — a rosszul feloldott könyvhivatkozások csere-naplója; '
                'a kivételek (név, nem eldönthető) a szkript KIVETEL listájában, indokkal.\n')
        f.write('\t'.join(['strong', 'regi', 'uj', 'magyar', 'tanu']) + '\n')
        for st, regi, uj, hu, t in CSERE:
            f.write('\t'.join([st, regi, uj, '; '.join('%s → %s' % x for x in hu), t]) + '\n')
    regi_sz = KK.szakasz_hashek(erintett)
    regi_en = {f_sorok[i].split('\t')[0]: KK.sha1(f_sorok[i].split('\t')[-1]) for i in en_uj}
    for i, (p, t) in en_uj.items():
        f_sorok[i] = '\t'.join(p[:-1] + [t])
    with open(KK.FORRAS, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(f_sorok))
    # A forras_javit hivatkozott-vers-próbája a vers -> jelentés táblából olvas, a tábla a javítótáblából: a kettőt a
    # nyugalmi pontig felváltva generáljuk (a független ellenőr: fordított sorrendben három heber_sorrend-javítás elveszett).
    for _kor in range(4):
        for parancs in (['olvaso_szerver/bdb_vers_jelentes.py', '--ts', VJ_TS], ['bdb_jelolt/forras_javit.py'] + KK.FJ_ARGS):
            r = subprocess.run([sys.executable, os.path.join(GYOKER, 'eszkozok', parancs[0])] + parancs[1:],
                               cwd=GYOKER, capture_output=True, text=True, encoding='utf-8')
            if r.returncode:
                sys.exit('%s hiba:\n%s' % (parancs[0], r.stderr[-2000:]))
        e = subprocess.run([sys.executable, os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver/bdb_vers_jelentes.py'), '--ts', VJ_TS,
                            '--ellenoriz'], cwd=GYOKER, capture_output=True, text=True, encoding='utf-8')
        if e.returncode == 0:
            break
    else:
        sys.exit('a vers -> jelentés tábla és a javítótábla nem jutott nyugalmi pontra')
    uj_sz = KK.szakasz_hashek(erintett)
    uj_en = {p[0]: KK.sha1(t) for p, t in en_uj.values()}
    hash_db = 0
    for i, s in enumerate(fsor):
        if not s.startswith('BDB\t'):
            continue
        p = hu_uj.get(i, s.split('\t'))
        st, jsz, h = p[ix['strong']], p[ix['jelentes_szam']], p[ix['forras_hash']]
        if jsz == 'teljes' and st in regi_en and h == regi_en[st]:
            p[ix['forras_hash']] = uj_en[st]
            hash_db += 1
        elif (st, jsz) in regi_sz and h == regi_sz[(st, jsz)] and uj_sz.get((st, jsz)) not in (None, h):
            p[ix['forras_hash']] = uj_sz[(st, jsz)]
            hash_db += 1
        fsor[i] = '\t'.join(p)
    eredeti = KK.tsv(KK.FORD)
    if len(eredeti) != len(fsor) or any(x != y and x.split('\t')[:5] != y.split('\t')[:5] for x, y in zip(eredeti, fsor)):
        sys.exit('kulcs- vagy sorszám-eltérés a fordítási táblában; nem írom')
    with open(KK.FORD, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(fsor))
    print('kiírva: forrás (%d szócikk), javítótábla, fordítás (%d sor, %d hash), napló' % (len(erintett), len(hu_uj), hash_db))


if __name__ == '__main__':
    main()
