#!/usr/bin/env python
"""A BDB forráshibáinak javítótáblája (F107, 5. lépés; DT-F107f (a), felhasználó, 2026-10-18).

Az első hibaosztály: `pe_mem` — a DictBDB.json a dagesses pét dagesses memként írja (0 dagesses pe a JSON-ban,
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


def sha256_adatsorok(ut):
    """A fájl adatsorainak (a `#` kezdetű fejlécsorok nélkül, LF-re normalizálva) sha256-ja. A `bdb_vers_jelentes.tsv`-hez:
    annak fejléce e tábla hash-ét hordozza (a `hivatkozas_kezi` sorok miatt), ez a tábla pedig az övét (F105, a
    hivatkozott-vers-próba) — a fejléc nélküli hash töri meg a kört."""
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for sor in f:
            if not sor.startswith(b'#'):
                h.update(sor.replace(b'\r\n', b'\n'))
    return h.hexdigest()


def kod_hash():
    """A forras_javit.py és a heber_sorrend.py (a heber_sorrend osztály szabálya) együttes hash-e."""
    h = hashlib.sha256()
    for ut in (os.path.abspath(__file__), os.path.join(ITT, 'heber_sorrend.py')):
        with open(ut, 'rb') as f:
            h.update(f.read().replace(b'\r\n', b'\n'))
    return h.hexdigest()


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


def general(ts, ts_heber=None, ts_atiras=None, ts_vers=None):
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
    ki.extend(hivatkozas_sorok(stat, ts))
    ki.extend(kezi_hivatkozas_sorok(stat))
    ki.extend(heber_sorrend_sorok(stat, ts_heber or ts, ts_vers))
    ki.extend(atiras_sorok(stat, ts_atiras or ts))
    ki.extend(kezi_szoveg_sorok(stat))
    return ki, stat


# ---------------------------------------------------------------- heber_sorrend (N-F131y, DT445)
# A DictBDB.json héber kifejezéseinek szórend- és geres-hibája (naplok/BDB_HEBER_SORREND_meres.md). A szabály és a Biblia-próba:
# heber_sorrend.py. Egy sor = egy változó kifejezés (R_hib ≠ a forrás alakja) a szakasztábla sorában; `elofordulas`: a `forras_alak`
# hányadik (héber betűvel nem határos) előfordulása a sor `szoveg`-ében; a héber alakok a forrás alakjában (nem NFD), mert a
# megjelenítés betű szerint cserél (bdb_rovidites.heber_sorrend_javit). `javitva`: a Biblia igazolja a javított, tiszta alakot;
# `valodi_sorrend`: a Biblia a forrás alakját igazolja; `jelolt_marad`: eldönthetetlen, vagy írásjel / sziglum a futamban.
#
# Hivatkozott-vers-próba (F105, DT-F105a, 2026-11-10): ahol a „bármely vers” próba nem dönt (`jelolt_marad`, tiszta kifejezés),
# a kifejezés után hivatkozott vers (heber_sorrend.HivatkozottVers: BDB_teljes_unabridged.tsv + bdb_vers_jelentes.tsv) dönt:
# ha a TAHOT-ban a hivatkozott vers a javított alakot illeszti, a forrásét nem, a sor `javitva` (a proveniencia ezt a próbát
# nevezi meg). A több `<heb>` elemre bontott futam (a szakasz szövegében egymás mellett álló kifejezések, amelyeknek nincs
# saját sora) ugyanígy új `javitva` sort kap, a lexikon nélküli R_hib-bel (geres nélkül R0, geresnél R_str). A meglévő
# `javitva` és `valodi_sorrend` sorokhoz a próba nem nyúl; a hivatkozott verssel ütköző két `valodi_sorrend` kézi sor
# (KEZI_HEBER_SORREND).
JSON_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'DictBDB.json')
TAHOT_UT = os.path.join(GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')
BDB_EN_UT = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
VJ_UT = os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv')
FUTAM_RE = re.compile(r'[֑-ׇא-״יִ-ﭏ]+(?: [֑-ׇא-״יִ-ﭏ]+)+')
# (strong, forrás alak, hivatkozott vers, indok): a DT445 `valodi_sorrend` sora, amelyet a hivatkozott vers cáfol (F105)
KEZI_HEBER_SORREND = [
    ('H2638', 'ח לֵֿב׳אָדָם', 'Péld 17:18',
     'a hivatkozott vers (Péld 17:18, „אָדָם חֲסַר־לֵב”) a javított szórendet adja; a DT445 bármely-vers-próbája a forrás alakját '
     'a Sir 4:7-ben találta, a rövidítés 8 betűs résével (véletlen egyezés), ezért lett valodi_sorrend'),
    ('H3801', 'קֹדֶשׁ׳כּ בַּֿד', '3Móz 16:4',
     'a hivatkozott vers (3Móz 16:4, „כְּתֹנֶת־בַּד קֹדֶשׁ”) a javított szórendet adja; a DT445 bármely-vers-próbája a forrás '
     'alakját a 3Móz 23:8-ban találta, a rövidítés 8 betűs résével (véletlen egyezés), ezért lett valodi_sorrend'),
]
def heber_jel(c):
    """Héber betű (a prezentációs alak is), pontozás vagy geres / gerszajim: a kifejezés ezzel nem határos."""
    return 'א' <= c <= 'ת' or '\ufb1d' <= c <= '\ufb4f' or '֑' <= c <= 'ׇ' or c in '׳״'


def kifejezes_elofordulasok(szoveg, alak):
    """Az `alak` előfordulásai, amelyek előtt és után nem áll héber betű vagy jel."""
    ki, i = [], szoveg.find(alak)
    while i >= 0:
        e = i + len(alak)
        if not (i and heber_jel(szoveg[i - 1])) and not (e < len(szoveg) and heber_jel(szoveg[e])):
            ki.append(i)
        i = szoveg.find(alak, i + 1)
    return ki


def heber_sorrend_sorok(stat, ts, ts_vers=None):
    sys.path.insert(0, ITT)
    import heber_sorrend as HS
    import json
    import html as html_mod
    import bont
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver'))
    import bdb_szelet
    with open(JSON_UT, encoding='utf-8') as f:
        defek = {it['top']: it.get('def', '') for it in json.load(f)}
    lex = HS.lexikon_csoportok(LEX_UT)
    bib = HS.Biblia(TAHOT_UT)
    hv = HS.HivatkozottVers(BDB_EN_UT, VJ_UT, bdb_szelet.lapit)
    kezi = {(s, unicodedata.normalize('NFC', a)): (v, i) for s, a, v, i in KEZI_HEBER_SORREND}
    prov_vers = ('scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc): heber_sorrend.py R_hib + hivatkozott-vers-próba '
                 '(TAHOT a bdb_vers_jelentes.tsv Károli-versén; F105, DT-F105a) | ts=%s')
    sorok_kulcs = collections.OrderedDict()
    for r in tabla_sorok():
        top, blokk = r['forras'].split(':', 1)[1].split('#')
        sorok_kulcs.setdefault(top, {})[int(blokk)] = r
    prov = 'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc): heber_sorrend.py R_hib + TAHOT-próba (DT445) | ts=%s'
    ki = []
    for top, sorok in sorok_kulcs.items():
        # a kifejezések a bontó blokkjai szerint (a tábla sora = a blokk, `forras` #n), a blokkon belül sorrendben
        kif, blokk_idx = [], []
        for bi, (bh, _s1) in enumerate(bont.json_blokkok(defek.get(top, ''))):
            for m in re.finditer(r'<heb><ref0[^>]*>(.*?)</ref0>', bh, re.S):
                kif.append(HS.ws(html_mod.unescape(re.sub(r'<[^>]+>', '', m.group(1)))))
                blokk_idx.append(bi)
        bdb_idk = []
        for bi in sorted(sorok):
            if sorok[bi]['bdb_id'] and sorok[bi]['bdb_id'] not in bdb_idk:
                bdb_idk.append(sorok[bi]['bdb_id'])
        csop = [c for b in bdb_idk for c in lex.get(b, [])]
        darabok = HS.parosit(kif, csop)
        kurzor = collections.Counter()
        for js, dar, bi in zip(kif, darabok, blokk_idx):
            r = sorok.get(bi)
            poz = [p for p in kifejezes_elofordulasok(r['szoveg'], js) if p >= kurzor[bi]] if r else []
            hol = (bi, poz[0]) if poz else None
            uj = HS.r_hib(js, dar)
            if hol is None:
                if uj != js:
                    stat['heber_sorrend_nem_talalt'] += 1
                continue
            kurzor[bi] = hol[1] + len(js)
            if uj == js:
                continue
            k = kifejezes_elofordulasok(r['szoveg'], js).index(hol[1]) + 1
            it, v_js, v_uj = HS.itelet(bib, js, uj)
            if not HS.tiszta(js):
                allapot, jav = 'jelolt_marad', ''
                indok = 'írásjel vagy sziglum a futamban: gépi javítás nincs (DT445); a szabály javaslata: %s' % uj
            elif it == 'helyes':
                allapot, jav = 'javitva', uj
                indok = ('a héber Biblia igazolja: a javított szórend a TAHOT %s versében áll, a forrás alakja egy versben sem '
                         '(R_hib%s)' % (v_uj, ', a BDB.lexicon darabhatára szerint' if HS.G in js and dar is not None else ''))
            elif it == 'rontott' and (r['strong'], unicodedata.normalize('NFC', js)) in kezi:
                v, kindok = kezi[(r['strong'], unicodedata.normalize('NFC', js))]
                if HS.itelet_versen(bib, js, uj, v) != 'helyes' or hv.vers(r['strong'], r['szoveg'], hol[1], js) != v:
                    raise SystemExit('HIBA: a kézi heber_sorrend sor (%s %s) próbája már nem áll' % (r['strong'], v))
                stat['heber_sorrend_kezi'] += 1
                ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'heber_sorrend', '', str(k), js, uj, 'javitva', kindok,
                           'manual'])
                continue
            elif it == 'rontott':
                allapot, jav = 'valodi_sorrend', ''
                indok = ('a héber Biblia a forrás alakját igazolja (TAHOT %s), a javítottat nem: a sorrend marad; a szabály '
                         'javaslata: %s' % (v_js, uj))
            else:
                v = hv.vers(r['strong'], r['szoveg'], hol[1], js)
                if v and HS.itelet_versen(bib, js, uj, v) == 'helyes':
                    stat['heber_sorrend_vers_javitva'] += 1
                    ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'heber_sorrend', '', str(k), js, uj, 'javitva',
                               'a hivatkozott vers igazolja: a javított szórend a TAHOT %s versében áll, a forrás alakja nem '
                               '(R_hib%s; a bármely-vers-próba nem döntött)' % (
                                   v, ', a BDB.lexicon darabhatára szerint' if HS.G in js and dar is not None else ''),
                               prov_vers % (r['strong'], ts_vers or ts)])
                    continue
                allapot, jav = 'jelolt_marad', ''
                indok = ('a héber Biblia nem dönt (%s): gépi javítás nincs (DT445); a szabály javaslata: %s'
                         % ('mindkét alak áll' if v_js and v_uj else 'egyik alak sem áll, vagy kevés az anyag', uj))
            stat['heber_sorrend_' + allapot] += 1
            ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'heber_sorrend', '', str(k), js, jav, allapot, indok,
                       prov % (r['strong'], ts)])
        # a több <heb> elemre bontott futamok (saját sor nélkül): hivatkozott-vers-próba, lexikon nélküli R_hib
        for bi in sorted(sorok):
            r = sorok[bi]
            sajat = {js for js, b in zip(kif, blokk_idx) if b == bi}
            for m in FUTAM_RE.finditer(r['szoveg']):
                futam = m.group(0)
                if futam in sajat:
                    continue
                uj = HS.r0(futam) if HS.G not in futam else HS.r_str(futam)
                if uj == futam:
                    continue
                v = hv.vers(r['strong'], r['szoveg'], m.start(), futam)
                if not v or HS.itelet_versen(bib, futam, uj, v) != 'helyes':
                    continue
                hely = kifejezes_elofordulasok(r['szoveg'], futam)
                if m.start() not in hely:
                    continue
                k = hely.index(m.start()) + 1
                stat['heber_sorrend_futam_javitva'] += 1
                ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'heber_sorrend', '', str(k), futam, uj, 'javitva',
                           'több <heb> elemre bontott futam, saját sor nélkül; a hivatkozott vers igazolja: a javított '
                           'szórend a TAHOT %s versében áll, a forrás alakja nem (lexikon nélküli R_hib)' % v,
                           prov_vers % (r['strong'], ts_vers or ts)])
    return ki


# ---------------------------------------------------------------- atiras (B3, DT-F164a)
# A DictBDB.json latin betűs átírásainak betűkészlet-hibája: a „®” a redukált magánhangzó (ᵉ), a „°” az álef (ʾ) rossz kódja
# (pl. „Sh®°ôl” = Sheʾôl, H0011 és 32 további Strong). Egy sor = egy „®”-t tartalmazó szóalak egy előfordulása a szakasztábla
# sorában (`elofordulas`: a `forras_alak` hányadik részszöveg-előfordulása a sor `szoveg`-ében). A javított alak a SZABÁLYBÓL jön
# („e?®” → „e”, „°” → „ʾ”); a BDB.lexicon csak igazol: `javitva`, ha a javított alak (ʾ → ') a lexikon bármely szócikkében tiszta
# szóként áll (DT225 (i)); különben `jelolt_marad`, javítás nélkül. A csak „°”-t hordozó alakok (fokjel, akkád/egyiptomi átírás)
# kívül esnek (N-F164a). A megjelenítés (bdb_rovidites.atiras_javit) részszöveg szerint cserél, az angol szövegben és a magyar
# fordításban is (a torz alak a fordításban szó szerint áll, toldalékkal); a fordító bemenete és az `sz<n>` hash nem változik.
ATIRAS_ALAK = re.compile(r'(?:[^\W\d_]|[®°])*®(?:[^\W\d_]|[®°])*')
LEX_SZO = re.compile(r"(?:[^\W\d_]|['ʾ])+")


def atiras_szabaly(alak):
    return re.sub('e?®', 'e', alak).replace('°', 'ʾ')


def lexikon_latin_szavak():
    """A BDB.lexicon latin betűs szóalakjai (kisbetűsítve), az igazoláshoz; a torz jelet hordozók nélkül."""
    import html as html_mod
    con = sqlite3.connect('file:' + LEX_UT.replace('\\', '/') + '?mode=ro', uri=True)
    ki = set()
    for (d,) in con.execute("select Definition from Lexicon where Topic like 'BDB%'"):
        ki.update(w.casefold() for w in LEX_SZO.findall(html_mod.unescape(re.sub(r'<[^>]+>', ' ', d))))
    con.close()
    return ki


def atiras_sorok(stat, ts):
    lex = lexikon_latin_szavak()
    prov = 'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc): atiras-szabály + BDB.lexicon-igazolás | ts=%s'
    ki = []
    for r in tabla_sorok():
        kurzor = collections.Counter()
        for m in ATIRAS_ALAK.finditer(r['szoveg']):
            alak = m.group(0)
            kurzor[alak] += 1
            jav = atiras_szabaly(alak)
            if jav.replace('ʾ', "'").casefold() in lex:
                allapot, indok = 'javitva', ('a szabály szerinti alak (%s) tiszta szóként áll a BDB.lexiconban: a „®” a redukált '
                                             'magánhangzó, a „°” az álef torz kódja' % jav.replace('ʾ', "'"))
            else:
                allapot, jav, indok = 'jelolt_marad', '', ('a szabály szerinti alak (%s) a BDB.lexiconban nem áll: gépi javítás '
                                                           'nincs' % atiras_szabaly(alak))
            stat['atiras_' + allapot] += 1
            ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'atiras', '', str(kurzor[alak]), alak, jav, allapot, indok,
                       prov % (r['strong'], ts)])
    return ki


# ---------------------------------------------------------------- hivatkozas (DT-F107c (d), felhasználó, 2026-10-18)
# A BDB_teljes_unabridged.tsv 247 sorát a #34 (ψ, naplok/F34_M2_csere.tsv) és a #46 (könyvfeloldás,
# naplok/BDB_KONYVFELOLDAS_csere.tsv és _kezi.tsv) utólag javította. Ezek a javítások a nyers JSON-ban nincsenek; hogy a táblából
# generált nézet ne lépjen vissza, a javítótábla átveszi őket: a TSV és a JSON (a _convert_bdb.py szerint újrakonvertálva) szóköz
# szerinti tokenjeinek eltérő szakaszai (difflib), soronként egy. `elofordulas` = a `forras_alak` hányadik egész-token előfordulása
# a Strong nézet-szövegében (a jel + szoveg sorok egy szóközzel); `sorszam` = a táblasor, amelyben ez az előfordulás áll.
F34_CSERE = os.path.join(GYOKER, 'naplok', 'F34_M2_csere.tsv')
F46_CSERE = os.path.join(GYOKER, 'naplok', 'BDB_KONYVFELOLDAS_csere.tsv')
F46_KEZI = os.path.join(GYOKER, 'naplok', 'BDB_KONYVFELOLDAS_kezi.tsv')
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')


def _ws(t):
    return re.sub(r'\s+', ' ', t).strip()


def _tsv_olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


# A csere-naplókban nem szereplő, a git-történettel igazolt TSV-javítások (git log -G Pharaoh -- konkordancia/BDB_teljes_unabridged.tsv:
# a három sort a 6400b5a7 „F46.6: gépi csere a DT-F46 szerint” írta át; ellenőrizve 2026-10-18)
GIT_FORRAS = {
    (st, 'Phoenician', 'Pharaoh'): 'F46.6 (git 6400b5a7, gépi csere; a csere-naplóban nem szerepel)'
    for st in ('H5973', 'H7588', 'H9005')
}


def ref_kulcs(ref):
    """Hivatkozás-kulcs: (a könyvnév első 3 betűje kisbetűvel, a számelőtaggal; fejezet:vers) — „1Ki 50:1” = „1Kin 50:1”."""
    m = re.search(r'([1-3]?)\s*([A-Za-z]+)\.?\s+(\d+:\d+)', ref)
    if not m:
        return None
    return (m.group(1) + m.group(2)[:3].lower(), m.group(3))


def forrasjavitas_index():
    """(strong, az ÚJ hivatkozás kulcsa) → a javítás forrása (F34 / F46 csere / F46 kézi)."""
    idx = {}
    for d in _tsv_olvas(F34_CSERE):
        k = ref_kulcs(d.get('uj', ''))
        if d.get('dontes') == 'JAVIT' and k:
            idx.setdefault((d['szocikk_id'], k), 'F34 (naplok/F34_M2_csere.tsv, JAVIT)')
    for ut, nev in ((F46_CSERE, 'F46 (naplok/BDB_KONYVFELOLDAS_csere.tsv)'), (F46_KEZI, 'F46 (naplok/BDB_KONYVFELOLDAS_kezi.tsv)')):
        for d in _tsv_olvas(ut):
            k = ref_kulcs(d.get('javasolt_forras_alak', ''))
            if k:
                idx.setdefault((d['strong'], k), nev)
    return idx


def token_elofordulas(szoveg, token):
    """Az egész-token (szóközzel határolt) előfordulások kezdőpozíciói."""
    return [m.start() for m in re.finditer(r'(?<!\S)' + re.escape(token) + r'(?!\S)', szoveg)]


def strong_nezet(sorok):
    """A Strong nézet-szövege (jel + szoveg, egy szóközzel) és a sorhatárok."""
    darabok, hatar, p = [], [], 0
    for x in sorok:
        t = ' '.join(y for y in (x['jel'], x['szoveg']) if y)
        if not t:
            continue
        if darabok:
            p += 1
        hatar.append((p, p + len(t), x))
        darabok.append(t)
        p += len(t)
    return ' '.join(darabok), hatar


def hivatkozas_sorok(stat, ts):
    import json
    sys.path.insert(0, ITT)
    import bont
    import forras_osszevetes
    import difflib
    with open(TSV, encoding='utf-8', newline='') as f:
        tsv = {s.split('\t')[0]: s.split('\t')[2] for s in f.read().split('\n')[1:] if s}
    with open(bont.JSON_UT, encoding='utf-8') as f:
        ujra = {}
        for item in json.load(f):
            m = re.match(r'^H(\d+)', item.get('top', ''))
            if m:
                ujra['H%04d' % int(m.group(1)) + item['top'][len(m.group(0)):]] = forras_osszevetes.strip_html_142ad625(item['def'])
    tabla = collections.OrderedDict()
    for r in tabla_sorok():
        tabla.setdefault(r['strong'], []).append(r)
    idx = forrasjavitas_index()
    ki = []
    for st in tabla:
        if st not in tsv or st not in ujra or _ws(tsv[st]) == _ws(ujra[st]):
            continue
        a, b = _ws(ujra[st]).split(' '), _ws(tsv[st]).split(' ')
        nezet, hatar = strong_nezet(tabla[st])
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == 'equal':
                continue
            x, y = ' '.join(a[i1:i2]), ' '.join(b[j1:j2])
            # hányadik előfordulás a JSON-szövegben (a nézetben ugyanannyiadik)
            elotte = ' '.join(a[:i1])
            k = len(token_elofordulas(elotte + ' ' + x, x)) if x else 0
            poz = token_elofordulas(nezet, x) if x else []
            sor = next((h[2] for h in hatar if poz and len(poz) >= k and h[0] <= poz[k - 1] < h[1]), None)
            # az új hivatkozás: ha a szakasz csak könyvnév, a fejezet:vers a TSV következő tokenje
            if not re.search(r'\d+:\d+', y):
                uj_ref = y + ' ' + (b[j2] if j2 < len(b) else '')
            elif not re.search(r'[A-Za-z]{2,}\.?\s+\d+:\d+', y) and j1 > 0:
                uj_ref = b[j1 - 1] + ' ' + y          # csak fejezet:vers változott: a könyvnév az előző token
            else:
                uj_ref = y
            forras = idx.get((st, ref_kulcs(uj_ref))) or GIT_FORRAS.get((st, x, y))
            if sor is None:
                allapot, indok = 'jelolt_marad', 'a forrás-alak a tábla nézet-szövegében nem található (%d. előfordulás)' % k
                stat['hivatkozas_jelolt_marad'] += 1
            else:
                allapot = 'javitva'
                indok = 'a TSV utólagos hivatkozás-javítása (a nyers JSON-ban nincs): %s' % (forras or 'a forrásjavítás-naplóban nem azonosított')
                stat['hivatkozas_javitva'] += 1
                if not forras:
                    stat['hivatkozas_forras_nem_azonositott'] += 1
            ki.append([st, sor['sorszam'] if sor else '', sor['bdb_id'] if sor else '', 'hivatkozas', '', str(k), x, y,
                       allapot, indok,
                       'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc): BDB_teljes_unabridged.tsv ↔ DictBDB.json, %s | ts=%s'
                       % (st, (forras or 'F34/F46').split(' ')[0], ts)])
    return ki


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
    # F107 javítókör (ELLENOR_F107 szúrópróba, 2026-10-18): mindkettő a DictBDB.json-ban ÉS a BDB.lexicon-ban igazolva
    ('H6440', '= presence, person', 'hamis_jelolo', '— See further below </p><p><b>7. 2. a.</b> = <i>presence, person</i>', '-/2/a',
     'a „See further below 7” hivatkozás „7.”-e a 2. jelentés a. alpontjának félkövér fejébe olvadt mindkét forrásban (lexikon: '
     '„See further below </div><div class="point"><b>7. 2. a.</b>”); az útvonal (-/2/a, I. szakasz) helyes, a „7.” a fejben hamis'),
    ('H6440', '(a) in the face of, mostly', 'hamis_jelolo', 'see II. אֵת <b>4a. 3.</b> בִּפְנֵי: <i>(a) in the face of</i>', '-/3',
     'a „see II. אֵת 4a” hivatkozás „4a.”-ja a II. szakasz 3. jelentésének (בִּפְנֵי) fejébe olvadt mindkét forrásban (lexikon: '
     '„see II. אֵת </div><div class="point"><b>4 a. 3.</b> בִּפְנֵי”); a JSON-ban a fej a bekezdés közepén, héber szó után áll, ezért a '
     'tábla nem nyit szakaszt: a II/3 csomópont hiányzik (aranyminta: II -/3; a szakaszt figyelmen kívül hagyó összevető ezt az I/3-mal '
     'fedte, l. napló, Javítókör)'),
]


# DT381 (a) (felhasználó, 2026-10-28): kézi hivatkozás-javítás (`hivatkozas_kezi`). A BDB forrásszövege (a DictBDB.json és a
# BDB_teljes_unabridged.tsv is) létező, de hibás verset idéz; a 2.23 (`bdb_igehely_javitas.tsv`) csak nem létező fejezetet javít,
# ezért kézi sor. `allapot=kezi`, proveniencia `manual`; a `forras_alak` / `javitott_alak` a fejezet:vers token, az `elofordulas` a
# `forras_alak` hányadik egész-token előfordulása a Strong nézet-szövegében. A szöveg-nézet (nezet_general.py, szakasz_bemenet.py)
# NEM alkalmazza (a fordító bemenete változatlan); a 2.29 kinyerője (olvaso_szerver/bdb_vers_jelentes.py) olvassa, és a feloldott
# verset javítja. (strong, horgony, forras_alak, javitott_alak, indok)
KEZI_HIVATKOZAS = [
    ('H8034', 'in worship, so 12:8; 13:4; 21:33; 26:35', '26:35', '26:25',
     'a BDB „call with … the name ׳י in worship, so 12:8; 13:4; 21:33; 26:35” sora (1Móz) a 26:35-öt idézi; ott a שֵׁם nem áll '
     '(Ézsau feleségei), a TAHOT szerint az 1Móz 26:25-ben áll a קָרָא mellett (H7121 + H8034), és a szövegkörnyezet (oltárt épít, '
     'segítségül hívja az Úr nevét) a 12:8; 13:4; 21:33 formulája: sajtóhiba a forrásban, 26:35 → 26:25 (DT381 (a))'),
    # F123 (felhasználó, 2026-10-29, a #123 ALVIL-001 ciklusában): a H7585 3/b pontja „׳שׁ וַאֲבַדּוֺן Prov 25:11”
    ('H7585', 'Prov 25:11, see', '25:11', '15:11',
     'a BDB „׳שׁ וַאֲבַדּוֺן Prov 25:11” sora a Péld 25:11-et idézi; ott a שְׁאוֹל nem áll (aranyalma ezüst tányéron), a TAHOT '
     'szerint a „Seól és Abaddón” párosa a Péld 15:11-ben áll (H7585 + H0011), és a BDB a 27:20-at (a pár másik helyét) a '
     'szócikk 1. pontjában külön idézi: sajtóhiba a forrásban, 25:11 → 15:11 (a DT381 (a) mintájára)'),
    # F12 (DT-F12b (1), az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával): a H8414 2. pontja
    ('H8414', 'worthlessness 49:19', '49:19', '49:4',
     'a BDB „worthlessness 49:19 ׳לְת כִלֵּיתִי כֹּחִי וְהֶבֶל” sora (Ézs) a 49:19-et idézi; ott a תֹּהוּ nem áll (a TAHOT '
     'Ézs 49:19 versében nincs H8414-token), a TAHOT szerint az idézett „לְתֹהוּ וְהֶבֶל כֹּחִי כִלֵּיתִי” az Ézs 49:4-ben áll '
     '(H8414), és a heber_sorrend sor is a TAHOT Ézs 49:4 versével igazolja a szórendet: sajtóhiba a forrásban, '
     '49:19 → 49:4 (a DT381 (a) mintájára)'),
]


def kezi_hivatkozas_sorok(stat):
    tabla = collections.OrderedDict()
    for r in tabla_sorok():
        tabla.setdefault(r['strong'], []).append(r)
    ki = []
    for st, horgony, forras_alak, javitott, indok in KEZI_HIVATKOZAS:
        nezet, hatar = strong_nezet(tabla.get(st, []))
        h = next((h for h in hatar if horgony in nezet[h[0]:h[1]]), None)
        if h is None:
            raise SystemExit('HIBA: a kézi hivatkozás-sor horgonya nem található: %s %r' % (st, horgony))
        # F123: a vers-token után írásjel is állhat („Prov 25:11, see …”); a hivatkozás-javítás csak a fejezet:vers alakot keresi
        poz = [m.start() for m in re.finditer(r'(?<!\S)' + re.escape(forras_alak) + r'(?![^\s,;.)\]])', nezet)]
        k = next((i for i, p in enumerate(poz, 1) if h[0] <= p < h[1] and p >= h[0] + nezet[h[0]:h[1]].find(horgony)), None)
        if k is None:
            raise SystemExit('HIBA: a kézi hivatkozás-sor forrás-alakja nem található a horgonyban: %s %r' % (st, forras_alak))
        stat['hivatkozas_kezi'] += 1
        ki.append([st, h[2]['sorszam'], h[2]['bdb_id'], 'hivatkozas_kezi', '', str(k), forras_alak, javitott, 'kezi', indok,
                   'manual'])
    return ki


# F123.GENKOR (DT-F181a): kézi szöveghelyesbítés a lapon álló, a szabályos osztályokon kívül eső forráshibákra. Mindkét nyers
# forrás (DictBDB.json és BDB.lexicon) ugyanígy hibás, ezért gépi igazolás nincs; a sor a betűkészlet torz átírását (`atiras`, a
# DT581 osztálya; a teljes betűkészlet-tábla visszafejtése N89) vagy a digitalizálásban elveszett zárójelet (`zarojel`) javítja.
# `allapot=javitva`, proveniencia `manual`; a megjelenítés (bdb_rovidites.atiras_javit, ill. zarojel_javit) részszöveg szerint
# cserél. Egy sor = egy alak: az angol forrásszövegé, vagy — a zárójelnél, ahol a fordítás más szöveg — a magyar fordításé (az
# `indok` megnevezi); a `sorszam` a horgonyt (az angol részszöveget) hordozó táblasor. (strong, horgony, hiba, forras_alak,
# javitott_alak, indok)
KEZI_SZOVEG = [
    ('H7121', "'†or°¹n", 'atiras', "'†or°¹n", 'Qorʾân',
     'a „read aloud, recite (the \'†or°¹n)” a Korán átírása a betűkészlet torz kódjával (a „†” a Q/Ḳ, a „°” az álef, a „¹” a '
     'hosszú â); a BDB.lexicon ugyanígy torz, de másutt a „Qoran” alakot hordozza (4×), és a forrás a Korán-helyeket „Qor”-ral '
     'idézi (pl. BDB55 „Qor 2:82”); a magyar fordításban „Korán” (bdb_rovidites.ATIRAS_MAGYAR)'),
    ('H7121', '†or°a¹n', 'atiras', '†or°a¹n', 'Qorʾân',
     'ugyanannak a szónak („the †or°a¹n”, a kiesett arab főnév fordítása) második torz alakja; l. az előző sort'),
    ('H2416', 'Leµi', 'atiras', 'Leµi', 'Leḥi',
     'a „rightly read לֶ֫חְיָה to Leµi, compare Judg 15:9” a Lehi helynév átírása a torz „µ” (ḥ) kóddal; a BDB.lexicon a helynevet '
     'másutt „Lehi” alakban hordozza (3×), és a Bír 15:9 Lehit nevezi meg; a magyar fordításban „Lehi”'),
    ('H7121', 'be read aloud compare Qal 4)', 'zarojel', 'be read aloud compare Qal 4)', 'be read aloud (compare Qal 4)',
     'angol forrásszöveg: a „(compare Qal 4)” nyitó zárójele a digitalizálásban elveszett (a DictBDB.json-ban és a BDB.lexicon-ban '
     'is „compare Qal 4 ):”); a párhuzamos a. és c. pont „(compare Qal 3)”, „(compare Qal 5” alakja'),
    ('H7121', 'be read aloud compare Qal 4)', 'zarojel', 'felolvastatni vö. Qal 4)', 'felolvastatni (vö. Qal 4)',
     'a magyar fordítás ugyanezen helye (l. az előző sort)'),
    ('H7121', 'be summoned (compare Qal 5:', 'zarojel', 'be summoned (compare Qal 5:', 'be summoned (compare Qal 5):',
     'angol forrásszöveg: a „(compare Qal 5)” záró zárójele a digitalizálásban elveszett (a DictBDB.json-ban és a BDB.lexicon-ban '
     'is „(compare Qal 5 : Isa 31:4”); a párhuzamos a., b. és d. pont a hivatkozást zárójelben zárja'),
    ('H7121', 'be summoned (compare Qal 5:', 'zarojel', 'megidéztetni (vö. Qal 5:', 'megidéztetni (vö. Qal 5):',
     'a magyar fordítás ugyanezen helye (l. az előző sort)'),
]


def kezi_szoveg_sorok(stat):
    sorok = tabla_sorok()
    ki = []
    for st, horgony, hiba, forras_alak, javitott, indok in KEZI_SZOVEG:
        r = next((x for x in sorok if x['strong'] == st and horgony in x['szoveg']), None)
        if r is None:
            raise SystemExit('HIBA: a kézi szövegsor horgonya nem található: %s %r' % (st, horgony))
        stat['%s_kezi' % hiba] += 1
        ki.append([st, r['sorszam'], r['bdb_id'], hiba, '', '', forras_alak, javitott, 'javitva', indok, 'manual'])
    return ki


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


def fajl_szoveg(sorok, ts, ts_heber=None, ts_atiras=None, ts_vers=None):
    fej = ['# GENERÁLT: eszkozok/bdb_jelolt/forras_javit.py --ts %s%s — kézzel nem szerkesztendő (F107, DT228 (a); séma: adat/SEMA.md, bdb_forras_javitas.tsv). A héber alakok NFD-ben (a heber_sorrend sorok a forrás alakjában).'
           % (ts, (' --ts-heber-sorrend %s' % ts_heber if ts_heber else '') + (' --ts-atiras %s' % ts_atiras if ts_atiras else '')
              + (' --ts-hivatkozott-vers %s' % ts_vers if ts_vers else '')),
           '# forras: adat/bdb_szakaszok.tsv@%s + konkordancia/lexikonok_nyers/BDB.lexicon@%s (csak igazolás és darabhatár) + '
           'konkordancia/lexikonok_nyers/DictBDB.json@%s + konkordancia/TAHOT_kivonat.tsv@%s (heber_sorrend) + '
           'konkordancia/BDB_teljes_unabridged.tsv@%s + adat/bdb_vers_jelentes.tsv@%s (adatsorok, a fejléc nélkül; heber_sorrend, hivatkozott vers; F105) + kód@%s'
           % (sha256_fajl(TABLA)[:12], sha256_fajl(LEX_UT)[:12], sha256_fajl(JSON_UT)[:12], sha256_fajl(TAHOT_UT)[:12],
              sha256_fajl(BDB_EN_UT)[:12], sha256_adatsorok(VJ_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--ts-heber-sorrend', help='a heber_sorrend sorok proveniencia-ts-e (alap: --ts)')
    ap.add_argument('--ts-atiras', help='az atiras sorok proveniencia-ts-e (alap: --ts)')
    ap.add_argument('--ts-hivatkozott-vers', help='a hivatkozott-vers-próbával javított heber_sorrend sorok ts-e (alap: --ts; F105)')
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    sorok, stat = general(a.ts, a.ts_heber_sorrend, a.ts_atiras, a.ts_hivatkozott_vers)
    print('sor: %d (pe_mem + kezi); %s; érintett Strong (javitva): %d' % (
        len(sorok), dict(stat), len(set(s[0] for s in sorok if s[8] == 'javitva'))))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, a.ts, a.ts_heber_sorrend, a.ts_atiras, a.ts_hivatkozott_vers)
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
