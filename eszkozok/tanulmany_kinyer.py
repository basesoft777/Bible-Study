#!/usr/bin/env python3
"""tanulmany_kinyer.py — az igeszakasz-tanulmány igehelyenkénti jelölt blokkjainak kinyerése (F205 M3, DT803).

A tanulmány (`genezis/`, `ujszovetseg/`, `melyelemzesek/` … `*_bovitett.md`) a szakasz verseit egyszer, alaposan
olvassa; a 2. sablon 4/b. pontja szerint igehelyenként egy blokkban rögzíti azt, amit a motívumcikk átvehet
(`sablonok/2_PaRDeS_bovitett_sablon.md` 4/b.). Ez az eszköz a blokkokból **csak jelölt-sort** készít az
`adat/jeloltek.tsv`-be, `dontes=nyitva` értékkel és `manual` provenienciával (CLAUDE.md 2. szabály, DT28: a blokk
támasz, nem ítélet; a döntés a motívum menetében születik). Más táblát nem ír, a tanulmányba nem ír vissza.

A blokk alakja (a 2. sablon 4/b.; a jelölők saját sorban):

  <!-- IGEHELY-BLOKK: [igehely] | motivum: [ID | új | —] | gerinc: [gerinc_elem | —] -->
  - **funkció:** … | üres — [ok]
  - **negatív próba:** [igen | nem] — [indoklás] | üres — [ok]
  - **jelentéspont:** [Strong] · szótár: […] · olvasat: […] · eltér: [igen — mert … | nem | nem mérhető — ok]
  - **vita:** [cím] · [képviselő(k)] · [egy mondat]
  - **visszhang:** [gorog | latin | szir | rabbinikus] · [tanú] · [mű] · [egy saját szavas mondat] · [forrás]
  - **versszámozás:** [azonos | az eltérés leírása] [proveniencia]
  <!-- IGEHELY-BLOKK-VÉGE -->

Pontonként (DT803 (a)):
  - **funkció + negatív próba** → egy `elofordulas` jelölt-sor; az `indoklas` a két olvasói mondat, a gerinc-elem és
    a próba értéke a `dontes_ref`-ben. A sor a `general.py` JELÖLT-szabályain megy át (`kinyeres_elemez`: igehely,
    gerinc-elem, indoklás, tabulátor, ütközés a meglévő kulccsal): importálva, nem másolva;
  - **jelentéspont, vita, visszhang** → `jelentespont` / `vita` / `visszhang` jelölt-sor, `targy` kulcsmezővel
    (Strong; a vita címe; `hagyomany:tanu`);
  - **versszámozás** → az ÓSZ-ben gépi: a `Karoli_versmegfeleltetes.tsv` (+ `_javitas`) ellen csak összevetés; ha a
    blokk a táblától eltér, az ELTÉR-sor és `versszam` jelölt (a tábla vitatása). Az ÚSZ-ben nincs megfeleltető tábla:
    a kitöltött pont `versszam` jelölt. Az LXX-oldalt (`pardes.db` `lxx_versszam`) az eszköz nem veti össze.

Az új jelölt-fajták (`jelentespont`, `vita`, `visszhang`, `versszam`) és a `targy` oszlop a DT803 sémája; a sémát a
F205 M5 hozza (`general.JELOLT_TIPUSOK`, `ellenoriz.py` 2/b., `adat/SEMA.md` 2.4). Amíg a tábla fejlécében nincs
`targy`, vagy a típus nincs a `general.JELOLT_TIPUSOK`-ban, az ilyen sor **várakozik**: a jelentésben áll, a táblába
nem íródik, és a séma után az újrafuttatás veszi fel. Az `elofordulas` sor a mai sémán is íródik.

Megállás (hiba, `--ir` mellett sem ír): párosítatlan vagy egymásba ágyazott jelölő, hibás fejléc, hiányzó, ismeretlen,
rossz sorrendű vagy nem ismételhetőként ismételt pont, `üres` ok nélkül, hibás mezőszám, ismeretlen motívum-ID,
hiányzó gerinc-elem az `elofordulas`-nál, a JELÖLT-szabályok hibája, és az olvasói szövegkapu BUKÁS-a a blokk
olvasói szövegén (`olvasoi_kapu.py`: BELSO, MUNKASZO, NYERS_JEL, NEVELO, INDOKLAS; importálva). `új` vagy `—`
motívumú blokkból sor nem készül, csak a jelentés nevezi meg.

Jelentés-szintű jelzés (nem bukás): a tanulmány 4. pontjában („Kapcsolódó igehelyek”, a 🔗 és a „További igazolt
kapcsolódások” sorai) idézett hely, amely a szakasz valamely versének Károli-kereszthivatkozása, de a javított
indexben (`konkordancia/Karoli_KH_javitott.tsv`) nem `megerositett`, hanem `kiesik` vagy `jelolt` (a STEPBible-alakra
a `Konyv_normalizalo_tabla.tsv`-n át normalizálva).

  python eszkozok/tanulmany_kinyer.py genezis/1Moz_8v20-22_bovitett.md [--jelentes FÁJL] [--ir]
         [--jeloltek TÁBLA] [--motivumok TÁBLA] [--ts ÉÉÉÉ-HH-NN]

Alapból száraz futás: a jelentés a kimenetre (vagy `--jelentes` fájlba) megy, tábla nem íródik. `--ir` mellett a
táblát csak hibátlan futás írja, a `general.jeloltek_hozzafuz` bájt-összevetésével (eltérésnél visszaáll).
TSV: split('\\t') / '\\t'.join, csv modul nélkül. Kilépési kód: 0 rendben, 1 hiba.
"""
import argparse
import io
import os
import re
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import general as G  # noqa: E402
import olvasoi_kapu as OK  # noqa: E402
import tanulmany_regiszter as TR  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KONKORDANCIA = os.path.join(GYOKER, 'konkordancia')
VERSMEGF_TSV = os.path.join(KONKORDANCIA, 'Karoli_versmegfeleltetes.tsv')
VERSMEGF_JAVITAS_TSV = os.path.join(KONKORDANCIA, 'Karoli_versmegfeleltetes_javitas.tsv')
KH_JAVITOTT_TSV = os.path.join(KONKORDANCIA, 'Karoli_KH_javitott.tsv')

PONTOK = ('funkció', 'negatív próba', 'jelentéspont', 'vita', 'visszhang', 'versszámozás')
ISMETELHETO = ('jelentéspont', 'vita', 'visszhang')
UJ_TIPUS = {'jelentéspont': 'jelentespont', 'vita': 'vita', 'visszhang': 'visszhang', 'versszámozás': 'versszam'}
HAGYOMANYOK = ('gorog', 'latin', 'szir', 'rabbinikus')
SEP = ' · '

BLOKK_KEZDET = re.compile(r'^<!-- IGEHELY-BLOKK: (.*) -->$')
BLOKK_VEGE = '<!-- IGEHELY-BLOKK-VÉGE -->'
PONT_SOR = re.compile(r'^- \*\*([^*]+):\*\* (.*)$')
URES = re.compile(r'^üres — (\S.*)$')
NEGATIV = re.compile(r'^(igen|nem) — (\S.*)$')
ELTER = re.compile(r'^(?:igen — \S.*|nem|nem mérhető — \S.*)$')
PROV = re.compile(r'\s*\[(scope=[^\]]*)\]')
STRONG = re.compile(r'^[HG]\d{4}[a-z]?$')
MOTIVUM_ID = re.compile(r'^[A-ZÁÉÍÓÖŐÚÜŰ]{3,}-\d{3}$')
MONDATVEG = re.compile(r'[.!?…]["”»)]?$')
KH_SOR = re.compile(r'🔗|További igazolt kapcsolódások')


# ---------------------------------------------------------------------------
# a blokkok elemzése
# ---------------------------------------------------------------------------

def _pont_elemez(pont, ertek):
    """(adat, hiba) — egy pont értékének mezői; `üres` esetén {'ures': ok}."""
    if ertek == 'üres' or ertek.startswith('üres ') or ertek.startswith('üres—'):
        m = URES.match(ertek)
        if not m:
            return None, '`üres` pont ok nélkül vagy hibás alakban (alak: `üres — [ok]`, sablon 4/b. K3)'
        return {'ures': m.group(1).strip()}, None
    if not ertek.strip():
        return None, 'üres érték: a pont tartalmat vagy `üres — [ok]` jelölést kap (K3)'
    if pont == 'funkció':
        if not MONDATVEG.search(ertek):
            return None, 'a funkció nem kerek mondat (mondatvégi írásjel nélkül; az 1/a mércéje)'
        return {'mondat': ertek}, None
    if pont == 'negatív próba':
        m = NEGATIV.match(ertek)
        if not m:
            return None, 'a negatív próba alakja: `igen — [indoklás]` vagy `nem — [indoklás]`'
        return {'ertek': m.group(1), 'indoklas': m.group(2).strip()}, None
    reszek = [r.strip() for r in ertek.split(SEP)]
    if pont == 'jelentéspont':
        if len(reszek) != 4:
            return None, 'a jelentéspont négy mezője (` · `): Strong · szótár: … · olvasat: … · eltér: …'
        strong, szotar, olvasat, elter = reszek
        if not STRONG.match(strong):
            return None, 'a jelentéspont első mezője nem Strong-szám: %r' % strong
        if not szotar.startswith('szótár: ') or not olvasat.startswith('olvasat: ') \
                or not elter.startswith('eltér: '):
            return None, 'a jelentéspont mezőnevei: `szótár:`, `olvasat:`, `eltér:`'
        szotar, olvasat, elter = (szotar[len('szótár: '):].strip(), olvasat[len('olvasat: '):].strip(),
                                  elter[len('eltér: '):].strip())
        if not szotar or not olvasat:
            return None, 'a jelentéspont `szótár:` vagy `olvasat:` mezője üres'
        if not ELTER.match(elter):
            return None, 'az `eltér:` értéke: `igen — mert …` | `nem` | `nem mérhető — [ok]`'
        return {'strong': strong, 'szotar': szotar, 'olvasat': olvasat, 'elter': elter}, None
    if pont == 'vita':
        if len(reszek) != 3 or not all(reszek):
            return None, 'a vita három mezője (` · `): cím · nevesített képviselő(k) · a vita egy mondatban'
        return {'cim': reszek[0], 'kepviselo': reszek[1], 'mondat': reszek[2]}, None
    if pont == 'visszhang':
        if len(reszek) != 5 or not all(reszek):
            return None, 'a visszhang öt mezője (` · `): hagyomány · tanú · mű · egy saját szavas mondat · forrás'
        if reszek[0] not in HAGYOMANYOK:
            return None, 'ismeretlen hagyomány: %r (%s)' % (reszek[0], ' | '.join(HAGYOMANYOK))
        return {'hagyomany': reszek[0], 'tanu': reszek[1], 'mu': reszek[2], 'mondat': reszek[3],
                'forras': reszek[4]}, None
    # versszámozás
    prov = PROV.search(ertek)
    szoveg = PROV.sub('', ertek).strip()
    if not szoveg:
        return None, 'a versszámozás pontja üres szöveggel áll'
    return {'szoveg': szoveg, 'prov': prov.group(1) if prov else '',
            'azonos': szoveg.startswith('azonos')}, None


def blokkok_elemez(szoveg):
    """(blokkok, hibak). A kódblokk (```) belseje nem számít: a sablon mintája ott áll.

    blokk = {'sor', 'igehely', 'motivum', 'gerinc', 'pontok': [{'pont', 'sor', 'adat'}]}"""
    blokkok, hibak = [], []
    akt = None
    kod = False
    for i, sor in enumerate(szoveg.replace('\r\n', '\n').split('\n'), start=1):
        if sor.strip().startswith('```'):
            kod = not kod
            continue
        if kod:
            continue
        mk = BLOKK_KEZDET.match(sor)
        if mk:
            if akt is not None:
                hibak.append('%d. sor: új IGEHELY-BLOKK a %d. sor blokkjának zárása előtt (párosítatlan jelölő)'
                             % (i, akt['sor']))
            reszek = [r.strip() for r in mk.group(1).split(' | ')]
            if len(reszek) != 3 or not reszek[1].startswith('motivum:') or not reszek[2].startswith('gerinc:'):
                hibak.append('%d. sor: hibás IGEHELY-BLOKK fejléc (alak: <!-- IGEHELY-BLOKK: [igehely] | '
                             'motivum: [ID | új | —] | gerinc: [gerinc_elem | —] -->): %s' % (i, sor))
                akt = {'sor': i, 'hibas': True, 'pontok': []}
                continue
            akt = {'sor': i, 'igehely': reszek[0], 'motivum': reszek[1][len('motivum:'):].strip(),
                   'gerinc': reszek[2][len('gerinc:'):].strip(), 'pontok': [], 'hibas': False}
            continue
        if sor == BLOKK_VEGE:
            if akt is None:
                hibak.append('%d. sor: IGEHELY-BLOKK-VÉGE nyitó jelölő nélkül' % i)
            elif not akt['hibas']:
                blokkok.append(akt)
            akt = None
            continue
        if 'IGEHELY-BLOKK' in sor:
            hibak.append('%d. sor: IGEHELY-BLOKK-jelölő nem a saját sorában vagy hibás alakban: %s' % (i, sor))
            continue
        if akt is None:
            continue
        if not sor.strip():
            continue
        mp = PONT_SOR.match(sor)
        if not mp or mp.group(1) not in PONTOK:
            hibak.append('%d. sor: a blokkban ismeretlen sor vagy pont (a hat pont: %s): %s'
                         % (i, ', '.join(PONTOK), sor))
            continue
        pont = mp.group(1)
        adat, hiba = _pont_elemez(pont, mp.group(2).strip())
        if hiba:
            hibak.append('%d. sor (%s): %s' % (i, pont, hiba))
            continue
        akt['pontok'].append({'pont': pont, 'sor': i, 'adat': adat})
    if akt is not None:
        hibak.append('a fájl végén nyitva maradt a %d. sor IGEHELY-BLOKK jelölője' % akt['sor'])
    for b in blokkok:
        hibak.extend(_blokk_teljes(b))
    return blokkok, hibak


def _blokk_teljes(b):
    """A hat pont megléte, sorrendje és ismétlése egy blokkban."""
    hibak = []
    latott = [p['pont'] for p in b['pontok']]
    hianyzo = [p for p in PONTOK if p not in latott]
    if hianyzo:
        hibak.append('%d. sor (%s): hiányzó pont: %s (sem tartalom, sem `üres`; K3)'
                     % (b['sor'], b['igehely'], ', '.join(hianyzo)))
    for p in PONTOK:
        if p not in ISMETELHETO and latott.count(p) > 1:
            hibak.append('%d. sor (%s): a(z) %s pont többször áll' % (b['sor'], b['igehely'], p))
    for p in ISMETELHETO:
        if latott.count(p) > 1 and any('ures' in x['adat'] for x in b['pontok'] if x['pont'] == p):
            hibak.append('%d. sor (%s): a(z) %s pont `üres` és kitöltött is' % (b['sor'], b['igehely'], p))
    sorszam = [PONTOK.index(p) for p in latott]
    if sorszam != sorted(sorszam):
        hibak.append('%d. sor (%s): a pontok sorrendje nem a sabloné (%s)'
                     % (b['sor'], b['igehely'], ', '.join(PONTOK)))
    return hibak


def pontjai(b, pont):
    return [p for p in b['pontok'] if p['pont'] == pont and 'ures' not in p['adat']]


# ---------------------------------------------------------------------------
# olvasói szövegkapuk (olvasoi_kapu.py, importálva)
# ---------------------------------------------------------------------------

def olvasoi_szovegek(b):
    """[(pont, szöveg)] — a blokk olvasói szövegei (a lapra kerülhetnek)."""
    ki = []
    for p in b['pontok']:
        a = p['adat']
        if 'ures' in a:
            continue
        if p['pont'] == 'funkció':
            ki.append((p['pont'], a['mondat']))
        elif p['pont'] == 'negatív próba':
            ki.append((p['pont'], a['indoklas']))
        elif p['pont'] == 'jelentéspont':
            ki.append((p['pont'], a['olvasat']))
            if a['elter'].startswith('igen — '):
                ki.append((p['pont'], a['elter'][len('igen — '):]))
        elif p['pont'] == 'vita':
            ki.append((p['pont'], a['mondat']))
        elif p['pont'] == 'visszhang':
            ki.append((p['pont'], a['mondat']))
    return ki


def szovegkapuk(blokkok):
    """(bukasok, figyelmeztetesek) — szövegenként külön bekezdésként, az új szerkezetű lap szigorával."""
    szovegek = []   # [(blokk, pont, szöveg)]
    for b in blokkok:
        szovegek += [(b, p, t) for p, t in olvasoi_szovegek(b)]
    if not szovegek:
        return [], []
    sorok_szoveg = '\n\n'.join(t.replace('\n', ' ') for _, _, t in szovegek)
    regi = OK.KIVETEL_NELKUL
    OK.KIVETEL_NELKUL = True
    try:
        sorok = OK.tagol(sorok_szoveg)
        talalatok = (OK.ell_belso(sorok) + OK.ell_munkaszo(sorok) + OK.ell_nyers_jel(sorok)
                     + OK.ell_nevelo(sorok))
        for n, (_, _, t) in enumerate(szovegek):
            sor = 2 * n + 1
            for f in OK.iras_kiejtes_nelkul(t):
                talalatok.append(OK.talalat('INDOKLAS', OK.BUKAS, sor, f, 'írás kiejtés nélkül', f))
            for rx, nev in OK.INDOKLAS_TILOS:
                for mm in rx.finditer(t):
                    talalatok.append(OK.talalat('INDOKLAS', OK.BUKAS, sor, OK.kornyezet(t, mm), nev, mm.group(0)))
    finally:
        OK.KIVETEL_NELKUL = regi
    bukas, figy = [], []
    for t in talalatok:
        idx = (t['sor'] - 1) // 2
        b, pont, _ = szovegek[idx]
        uzenet = '%d. sor (%s, %s): %s — %s: „%s”' % (b['sor'], b['igehely'], pont, t['azonosito'],
                                                      t['uzenet'], t['idezet'])
        (bukas if t['sulyossag'] == OK.BUKAS else figy).append(uzenet)
    return bukas, figy


# ---------------------------------------------------------------------------
# versszámozás (ÓSZ: összevetés a Károli-versmegfeleltetéssel)
# ---------------------------------------------------------------------------

def versmegfeleltetes(fo=VERSMEGF_TSV, javitas=VERSMEGF_JAVITAS_TSV):
    """{Károli-igehely: sor} — a javítótábla sora felülírja a fő tábláét (F117)."""
    _, sorok = G.tsv_beolvas(fo)
    ki = {s['igehely_karoli']: s for s in sorok}
    if javitas and os.path.exists(javitas):
        _, jav = G.tsv_beolvas(javitas)
        ki.update({s['igehely_karoli']: s for s in jav})
    return ki


def tabla_elter(sor):
    """True, ha a Károli-vers a KJV- vagy a kitöltött MT-versszámtól eltér."""
    vers = sor['igehely_karoli'].split(' ', 1)[1] if ' ' in sor['igehely_karoli'] else ''
    kjv, mt = sor.get('igehely_kjv', ''), sor.get('igehely_mt', '')
    return (kjv and kjv != vers) or (mt and mt != vers)


def tabla_leiras(sor):
    vers = sor['igehely_karoli'].split(' ', 1)[1]
    return 'Károli %s, KJV %s, MT %s' % (vers, sor.get('igehely_kjv') or '—', sor.get('igehely_mt') or vers)


# ---------------------------------------------------------------------------
# Károli-KH a javított index ellen
# ---------------------------------------------------------------------------

def step_konyvek():
    _, sorok = G.tsv_beolvas(G.KONYV_NORMALIZALO_TSV)
    return {s['Magyar rövidítés']: s['STEPBible-rövidítés'] for s in sorok}


def _step_hely(s):
    m = re.match(r'^(\w+)\.(\d+)\.(\d+)$', s)
    return (m.group(1), (int(m.group(2)), int(m.group(3)))) if m else None


def kh_index(ut=KH_JAVITOTT_TSV):
    """{STEP-igehely: [(konyv, kezdet, veg, szint, kapcsolodo)]}"""
    _, sorok = G.tsv_beolvas(ut)
    ki = {}
    for s in sorok:
        reszek = s['kapcsolodo'].split('-')
        a = _step_hely(reszek[0])
        b = _step_hely(reszek[-1]) if len(reszek) == 2 else a
        if a is None or b is None or a[0] != b[0]:
            continue
        ki.setdefault(s['igehely'], []).append((a[0], a[1], b[1], s['szint'], s['kapcsolodo']))
    return ki


def kh_osszevet(szoveg, blokkok, karoli=None, index=None):
    """(jelzesek, osszesites, figyelmeztetesek). A 4. pont 🔗 és „További igazolt kapcsolódások” soraiban idézett
    hely, ha a szakasz valamely versének Károli-KH-ja, de nem `megerositett` szintű: jelzés (nem bukás)."""
    figy = []
    kar = karoli or TR.Karoli(TR.karoli_kulcsok())
    step = step_konyvek()
    forras = set()
    cimsor = TR.elso_cimsor(szoveg)
    tart = TR.tartomany_cimsorbol(cimsor, kar) if cimsor else None
    if tart:
        for konyv, kez, veg in tart:
            a, b = kar.poz.get((konyv, kez[0], kez[1])), kar.poz.get((konyv, veg[0], veg[1]))
            forras.update(kar.lista[a:b + 1])
    else:
        figy.append('a tanulmány első címsorából a tartomány nem olvasható; a Károli-KH összevetése a blokkok '
                    'verseire szűkül')
    forras.update(b['igehely'] for b in blokkok)
    negyedik = [s for h, cim, s in TR.szakaszok(szoveg) if cim.startswith('4. Kapcsolódó igehelyek')]
    if not negyedik:
        return [], {'idezett': 0, 'megerositett': 0, 'nem_kh': 0}, figy
    sorok = [s for s in '\n'.join(negyedik).split('\n') if KH_SOR.search(s)]
    idezett = []
    for s in sorok:
        talalt = TR.hivatkozasok_szovegbol(s, None, None, kar)
        if not talalt:
            figy.append('a 4. pont sorában nincs feloldható igehely, a Károli-KH összevetése kihagyja: %s'
                        % s.strip()[:100])
        for kulcs, _, ref in talalt:
            if kulcs not in idezett and kulcs not in forras:
                idezett.append(kulcs)
    idx = index if index is not None else kh_index()

    def step_kulcs(kulcs):
        k, f, v = TR._kulcs_hely(kulcs)
        return step.get(k), (f, v)
    jelzesek, megerositett, nem_kh = [], 0, 0
    for c in idezett:
        ck, cfv = step_kulcs(c)
        talalat = []
        for f in sorted(forras):
            fk, ffv = step_kulcs(f)
            if fk is None:
                continue
            for konyv, kez, veg, szint, kapcs in idx.get('%s.%d.%d' % (fk, ffv[0], ffv[1]), ()):
                if konyv == ck and kez <= cfv <= veg:
                    talalat.append((f, szint, kapcs))
        if not talalat:
            nem_kh += 1
        elif any(sz == 'megerositett' for _, sz, _ in talalat):
            megerositett += 1
        else:
            jelzesek.append({'idezett': c, 'talalat': talalat})
    return jelzesek, {'idezett': len(idezett), 'megerositett': megerositett, 'nem_kh': nem_kh}, figy


# ---------------------------------------------------------------------------
# a kinyerés
# ---------------------------------------------------------------------------

def _mondat(t):
    t = t.strip()
    if t and t[0].islower():
        t = t[0].upper() + t[1:]
    if t and not MONDATVEG.search(t):
        t += '.'
    return t


def forras_nev(ut):
    teljes = os.path.abspath(ut)
    try:
        rel = os.path.relpath(teljes, GYOKER)
    except ValueError:
        rel = None
    if rel is None or rel.startswith('..'):
        return os.path.basename(teljes)
    return rel.replace('\\', '/')


def kinyer(szoveg, forras, jeloltek_fejlec, jeloltek, motivum_idk, datum, versmegf=None, kh=None):
    """A blokkok feldolgozása; nem ír semmit.

    Visszaad: dict — uj_sorok (írható), varakozo (a séma még nem fogadja), utkozesek, ellenorzo (versszámozás),
    eltérések, kihagyott (új / — motívum), kh (jelzések, összesítés), hibak, figyelmeztetesek, blokkok."""
    e = {'uj_sorok': [], 'varakozo': [], 'utkozesek': [], 'ellenorzo': [], 'elteresek': [], 'kihagyott': [],
         'kh': ([], {'idezett': 0, 'megerositett': 0, 'nem_kh': 0}), 'hibak': [], 'figyelmeztetesek': [],
         'blokkok': 0}
    blokkok, hibak = blokkok_elemez(szoveg)
    e['blokkok'] = len(blokkok)
    e['hibak'].extend(hibak)
    konyv_sorrend = G.konyv_sorrend_betolt()
    bukas, figy = szovegkapuk(blokkok)
    e['hibak'].extend('szövegkapu BUKÁS: %s' % b for b in bukas)
    e['figyelmeztetesek'].extend('szövegkapu: %s' % f for f in figy)

    def forras_kereses(igehely):
        return 'scope=manual | forras=%s#%s | ts=%s' % (forras, igehely, datum)
    targy_kesz = 'targy' in jeloltek_fejlec
    meglevo_uj = {(j.get('id'), j.get('igehely'), j.get('jelolt_tipus'), j.get('targy', ''))
                  for j in jeloltek if j.get('jelolt_tipus') in UJ_TIPUS.values()}
    latott_blokk, latott_uj = {}, set()
    jelolt_sorok = {}   # motívum -> [(blokk, JELÖLT-sor)]
    for b in blokkok:
        hiba = G.igehely_ellenoriz(b['igehely'], konyv_sorrend)
        if hiba:
            e['hibak'].append('%d. sor: %s' % (b['sor'], hiba))
            continue
        m = b['motivum']
        if m in ('új', '—', ''):
            e['kihagyott'].append({'sor': b['sor'], 'igehely': b['igehely'], 'motivum': m or '—'})
            continue
        if not MOTIVUM_ID.match(m) or m not in motivum_idk:
            e['hibak'].append('%d. sor (%s): a motívum nincs az adat/motivumok.tsv-ben: %r (SEMA 3/1)'
                              % (b['sor'], b['igehely'], m))
            continue
        kulcs = (m, b['igehely'])
        if kulcs in latott_blokk:
            e['hibak'].append('%d. sor (%s): ugyanehhez a vershez és motívumhoz már áll blokk (%d. sor); egy blokk = '
                              'egy vers és egy motívum' % (b['sor'], b['igehely'], latott_blokk[kulcs]))
            continue
        latott_blokk[kulcs] = b['sor']
        # funkció + negatív próba -> elofordulas (a general.py JELÖLT-szabályain át)
        funk, neg = pontjai(b, 'funkció'), pontjai(b, 'negatív próba')
        if funk or neg:
            if b['gerinc'] in ('—', ''):
                e['hibak'].append('%d. sor (%s): a funkció vagy a negatív próba kitöltött, de a gerinc-elem hiányzik '
                                  '(CLAUDE.md: minden előfordulás-sor megnevezi a gerinc-elemét)'
                                  % (b['sor'], b['igehely']))
            else:
                reszek = [_mondat(p['adat']['mondat']) for p in funk] + \
                         [_mondat(p['adat']['indoklas']) for p in neg]
                indoklas = ' '.join(reszek)
                if '-->' in indoklas or '\n' in indoklas:
                    e['hibak'].append('%d. sor (%s): a funkció vagy a próba szövegében `-->` áll'
                                      % (b['sor'], b['igehely']))
                else:
                    jelolt_sorok.setdefault(m, []).append(
                        (b, neg[0]['adat']['ertek'] if neg else '',
                         '<!-- JELÖLT: %s | gerinc: %s | %s -->' % (b['igehely'], b['gerinc'], indoklas)))
        # jelentéspont, vita, visszhang, versszámozás -> új jelölt-fajták
        uj = []
        for p in pontjai(b, 'jelentéspont'):
            a = p['adat']
            indok = _mondat(a['olvasat'])
            if a['elter'].startswith('igen — '):
                indok += ' A szótártól eltér: %s' % _mondat(a['elter'][len('igen — '):])
            uj.append((p, a['strong'], indok,
                       'szotar: %s; elter: %s' % (a['szotar'], a['elter'].split(' — ')[0])))
        for p in pontjai(b, 'vita'):
            a = p['adat']
            uj.append((p, a['cim'], '%s: %s' % (a['kepviselo'], _mondat(a['mondat'])), ''))
        for p in pontjai(b, 'visszhang'):
            a = p['adat']
            uj.append((p, '%s:%s' % (a['hagyomany'], a['tanu']), _mondat(a['mondat']),
                       'mu: %s; forras: %s' % (a['mu'], a['forras'])))
        for p in pontjai(b, 'versszámozás'):
            a = p['adat']
            ref = 'versszámozás: %s' % (a['prov'] or 'scope=manual')
            if G.konyv_teszamentum(G.konyv_token(b['igehely'])) == 'ÚSZ':
                uj.append((p, '', _mondat(a['szoveg']), ref))
                continue
            if not a['prov']:
                e['figyelmeztetesek'].append('%d. sor (%s, versszámozás): az ÓSZ-ben a pont lekérdezésből jön, de '
                                             'nincs mellette proveniencia-sor (CLAUDE.md 1. szabály)'
                                             % (p['sor'], b['igehely']))
            vm = (versmegf if versmegf is not None else {}).get(b['igehely'])
            if vm is None:
                e['ellenorzo'].append({'sor': p['sor'], 'igehely': b['igehely'], 'blokk': a['szoveg'],
                                       'tabla': '—', 'allapot': 'nincs a táblában (nem ellenőrizhető)'})
                continue
            tabla_azonos = not tabla_elter(vm)
            if tabla_azonos == a['azonos']:
                e['ellenorzo'].append({'sor': p['sor'], 'igehely': b['igehely'], 'blokk': a['szoveg'],
                                       'tabla': tabla_leiras(vm), 'allapot': 'egyezik'})
            else:
                e['ellenorzo'].append({'sor': p['sor'], 'igehely': b['igehely'], 'blokk': a['szoveg'],
                                       'tabla': tabla_leiras(vm), 'allapot': 'ELTÉR'})
                e['elteresek'].append('%d. sor (%s): a blokk szerint „%s”, a tábla szerint %s'
                                      % (p['sor'], b['igehely'], a['szoveg'], tabla_leiras(vm)))
                uj.append((p, '', _mondat(a['szoveg']), ref + '; tabla: ' + tabla_leiras(vm)))
        for p, targy, indok, dref in uj:
            tipus = UJ_TIPUS[p['pont']]
            k = (m, b['igehely'], tipus, targy)
            if '\t' in indok or '\t' in targy or '\t' in dref:
                e['hibak'].append('%d. sor: tabulátor a pontban (TSV-mezőbe nem írható)' % p['sor'])
                continue
            if k in latott_uj:
                e['hibak'].append('%d. sor (%s): a(z) %s pont ugyanazzal a tárggyal (%s) ismétlődik'
                                  % (p['sor'], b['igehely'], p['pont'], targy or '—'))
                continue
            latott_uj.add(k)
            if k in meglevo_uj:
                e['utkozesek'].append({'sor': p['sor'], 'igehely': b['igehely'], 'tipus': tipus, 'targy': targy})
                continue
            sor = {'id': m, 'igehely': b['igehely'], 'forras_kereses': forras_kereses(b['igehely']),
                   'dontes': 'nyitva', 'indoklas': indok, 'dontes_ref': dref, 'karoli_szo': '',
                   'azonositas_modja': '', 'megbizhatosag': '', 'datum': datum, 'jelolt_tipus': tipus,
                   'targy': targy, '_sor': p['sor']}
            if targy_kesz and tipus in G.JELOLT_TIPUSOK:
                e['uj_sorok'].append(sor)
            else:
                e['varakozo'].append(sor)
    # az elofordulas jelöltek: a general.py kinyerési szabályai, motívumonként
    elof = G.elofordulas_jeloltek(jeloltek)
    for m, lista in jelolt_sorok.items():
        r = G.kinyeres_elemez('\n'.join(s for _, _, s in lista), m, elof, konyv_sorrend, datum)
        for h in r['hibak']:
            mh = re.match(r'^(\d+)\. sor: (.*)$', h)
            if mh:
                b = lista[int(mh.group(1)) - 1][0]
                e['hibak'].append('%d. sor (%s): %s' % (b['sor'], b['igehely'], mh.group(2)))
            else:
                e['hibak'].append(h)
        for u in r['utkozesek']:
            b = lista[u['sor'] - 1][0]
            e['utkozesek'].append({'sor': b['sor'], 'igehely': b['igehely'], 'tipus': 'elofordulas',
                                   'targy': '', 'dontes': u['dontes']})
        for s in r['uj_sorok']:
            b, neg_ertek, _ = lista[s['_sor'] - 1]
            s['forras_kereses'] = forras_kereses(b['igehely'])
            if neg_ertek:
                s['dontes_ref'] += '; negativ_proba: %s' % neg_ertek
            s['_sor'] = b['sor']
            s.pop('_gerinc', None)
            e['uj_sorok'].append(s)
    e['uj_sorok'].sort(key=lambda s: s['_sor'])
    e['varakozo'].sort(key=lambda s: s['_sor'])
    try:
        jelz, ossz, kh_figy = kh_osszevet(szoveg, blokkok, karoli=kh[0] if kh else None,
                                          index=kh[1] if kh else None)
        e['kh'] = (jelz, ossz)
        e['figyelmeztetesek'].extend(kh_figy)
    except (OSError, ValueError) as exc:
        e['figyelmeztetesek'].append('a Károli-KH összevetése nem futott: %s' % exc)
    return e


# ---------------------------------------------------------------------------
# jelentés és futtatás
# ---------------------------------------------------------------------------

def _cella(x):
    return G._md_cella(x)


def jelentes(forras, e, irt):
    s = ['# Kinyerési jelentés — `%s`' % forras, '',
         '*Az igehelyenkénti jelölt blokkok kinyerése (F205, DT803; `sablonok/2_PaRDeS_bovitett_sablon.md` 4/b.). '
         'A kinyerés csak jelölt-sort ír a `jeloltek.tsv`-be, `dontes=nyitva` értékkel és `manual` provenienciával; '
         'a sorról a motívum menetében születik döntés.*', '',
         '| | db |', '|---|---|',
         '| blokk | %d |' % e['blokkok'],
         '| új jelölt-sor (írható) | %d |' % len(e['uj_sorok']),
         '| várakozó jelölt-sor (a séma még nem fogadja; M5) | %d |' % len(e['varakozo']),
         '| ütközés (a kulcs már létezik, nem írva) | %d |' % len(e['utkozesek']),
         '| kihagyott blokk (új vagy — motívum) | %d |' % len(e['kihagyott']),
         '| versszámozás: összevetés / ELTÉR | %d / %d |' % (len(e['ellenorzo']), len(e['elteresek'])),
         '| Károli-KH jelzés (nem `megerositett`) | %d |' % len(e['kh'][0]),
         '| hiba | %d |' % len(e['hibak']), '']
    if e['hibak']:
        allapot = 'a futás megállt (hiba), tábla nem íródott'
    elif irt:
        allapot = 'az írható jelölt-sorok a táblába íródtak (`--ir`)'
    else:
        allapot = 'javaslat: a tábla nem íródott (`--ir` nélkül)'
    s += ['**Állapot:** %s.' % allapot, '']

    def sortabla(cim, sorok):
        s.extend(['## %s' % cim, ''])
        if not sorok:
            s.extend(['*(nincs)*', ''])
            return
        s.append('| forrás-sor | igehely | motívum | jelolt_tipus | targy | indoklas | dontes_ref |')
        s.append('|---|---|---|---|---|---|---|')
        for r in sorok:
            s.append('| %d | %s | %s | %s | %s | %s | %s |' % (
                r['_sor'], r['igehely'], r['id'], r['jelolt_tipus'], _cella(r.get('targy', '')),
                _cella(r['indoklas']), _cella(r['dontes_ref'])))
        s.append('')
    sortabla('Új jelölt-sorok', e['uj_sorok'])
    sortabla('Várakozó jelölt-sorok (a `targy` oszlop és az új jelölt-fajták a F205 M5 sémájával)', e['varakozo'])
    s.extend(['## Ütközések és kihagyott blokkok', ''])
    tetelek = ['- %d. sor: `%s` %s%s már a táblában%s: nem írva.' % (
        u['sor'], u['igehely'], u['tipus'], (' (%s)' % u['targy']) if u['targy'] else '',
        (' (`dontes=%s`)' % u['dontes']) if u.get('dontes') else '') for u in e['utkozesek']]
    tetelek += ['- %d. sor: `%s` motívuma `%s`: sor nem készül; az ID kiosztása után az újrafuttatás veszi fel.'
                % (k['sor'], k['igehely'], k['motivum']) for k in e['kihagyott']]
    s.extend((tetelek or ['*(nincs)*']) + [''])
    s.extend(['## Versszámozás (ÓSZ: összevetés a `Karoli_versmegfeleltetes.tsv` + `_javitas` táblával)', ''])
    if e['ellenorzo']:
        s.append('| forrás-sor | igehely | a blokk | a tábla | állapot |')
        s.append('|---|---|---|---|---|')
        for r in e['ellenorzo']:
            s.append('| %d | %s | %s | %s | %s |' % (r['sor'], r['igehely'], _cella(r['blokk']), _cella(r['tabla']),
                                                    r['allapot']))
        s.append('')
        s.append('*Az LXX-versszámot az eszköz nem veti össze (`pardes.db` `lxx_versszam`).*')
    else:
        s.append('*(nincs)*')
    s.append('')
    jelz, ossz = e['kh']
    s.extend(['## Károli-kereszthivatkozások a javított index ellen (4. pont)', '',
              'Idézett hely: %d; ebből a szakasz Károli-KH-ja és `megerositett`: %d; nem Károli-KH: %d; jelzés: %d.'
              % (ossz['idezett'], ossz['megerositett'], ossz['nem_kh'], len(jelz)), ''])
    for j in jelz:
        s.append('- `%s`: %s' % (j['idezett'], '; '.join('%s → %s: `%s`' % (f, k, sz) for f, sz, k in j['talalat'])))
    if jelz:
        s.extend(['', '*A jelzés nem bukás: a hely a javított indexben nem megerősített (`kiesik` vagy `jelolt`); '
                      'a tanulmány maga dönt, megtartja-e.*'])
    s.append('')
    s.extend(['## Hibák', ''] + (['- %s' % h for h in e['hibak']] or ['*(nincs)*']) + [''])
    s.extend(['## Figyelmeztetések', ''] + (['- %s' % f for f in e['figyelmeztetesek']] or ['*(nincs)*']))
    return '\n'.join(s) + '\n'


def futtat(argv=None):
    p = argparse.ArgumentParser(prog='tanulmany_kinyer.py', description=__doc__.split('\n')[0])
    p.add_argument('tanulmany', help='az igeszakasz-tanulmány (.md)')
    p.add_argument('--ir', action='store_true', help='az írható jelölt-sorok hozzáfűzése a táblához (hibátlan futásnál)')
    p.add_argument('--jeloltek', default=G.JELOLTEK_TSV, help='a jelölt-tábla (alap: adat/jeloltek.tsv)')
    p.add_argument('--motivumok', default=G.MOTIVUMOK_TSV, help='a motívumtábla (alap: adat/motivumok.tsv)')
    p.add_argument('--jelentes', help='a jelentés fájlja (alap: a kimenet)')
    p.add_argument('--ts', default=G.TS, help='a futás napja (ÉÉÉÉ-HH-NN)')
    a = p.parse_args(argv)
    if not os.path.exists(a.tanulmany):
        print('HIBA: a tanulmány nem létezik: %s' % a.tanulmany, file=sys.stderr)
        return 1
    szoveg = io.open(a.tanulmany, encoding='utf-8', newline='').read()
    fejlec, jeloltek = G.tsv_beolvas(a.jeloltek)
    motivum_idk = {m['id'] for m in G.tsv_beolvas(a.motivumok)[1]}
    forras = forras_nev(a.tanulmany)
    e = kinyer(szoveg, forras, fejlec, jeloltek, motivum_idk, G.datum_iso_bol(a.ts), versmegf=versmegfeleltetes())
    kod = 1 if e['hibak'] else 0
    irt = False
    if a.ir and kod:
        print('--ir: a futásban hiba van, a tábla NEM íródik.', file=sys.stderr)
    elif a.ir and e['uj_sorok']:
        kod, uzenet = G.jeloltek_hozzafuz(a.jeloltek, e['uj_sorok'])
        print(uzenet, file=sys.stderr if kod else sys.stdout)
        irt = not kod
    szoveg_j = jelentes(forras, e, irt)
    if a.jelentes:
        with io.open(a.jelentes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg_j)
    else:
        sys.stdout.write(szoveg_j)
    print('kinyerés: %d blokk, %d új jelölt-sor, %d várakozó, %d ütközés, %d ELTÉR, %d KH-jelzés, %d hiba'
          % (e['blokkok'], len(e['uj_sorok']), len(e['varakozo']), len(e['utkozesek']), len(e['elteresek']),
             len(e['kh'][0]), len(e['hibak'])), file=sys.stderr)
    for h in e['hibak']:
        print('  HIBA: %s' % h, file=sys.stderr)
    return kod


if __name__ == '__main__':
    sys.exit(futtat())
