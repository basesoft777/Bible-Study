"""lapgen.regresszio — az új lap összevetése a referenciával (F218a brief 8.1).

    python eszkozok/lapgen/regresszio.py --id <ID> --uj <könyvtár> [--teljes] [--reszletes <fájl>]

Mit ellenőriz:
1. **Bemenet-hash őr.** A `naplok/F218_referencia.tsv` rögzíti a referencialap és a mérce minden
   bemenetének hash-ét (sorvég-normalizált tartalomból). Ha egy hash eltér, a mérés megáll:
   „a mérce bemenete megváltozott”. Az új generátor olvasási naplója (`<ID>_olvasasi_naplo.tsv` a lap
   mellett) is összevetődik a táblával: ha az új generátor olyan fájlt olvasott, amely nincs a táblában,
   vagy más tartalommal olvasta, a mérés megáll. Kivétel a `HASH_OR_KIVETEL` (a B51, N240): a lapon használt
   része a szakasz-diffben mérődik.
2. **Szakasz-diff.** A lap a 2. szintű címsoroknál szakaszokra bomlik; az új lap minden szakasza
   soronként összevetődik a referencia azonos című szakaszával. `--teljes` nélkül a hiányzó szakasz
   „nincs kész” (részleges lap), `--teljes` mellett BUKÁS.
   **Részleges szakasz.** A `RESZLEGES_SZAKASZOK` listában álló szakasz alblokkonként készül el (alblokk: a 3. és
   a 4. szintű címsor alatti rész, és a generált blokk záró jelölője). `--teljes` nélkül az ilyen szakasznak csak
   azok az alblokkjai vetődnek össze, amelyek az új lapon is állnak; a többi „nincs kész”, és a jelentés
   megszámolja. `--teljes` mellett a lista nem számít: a szakasz egésze vetődik össze.
3. **Engedély-összevetés.** Minden diff-sor pontosan egy engedélysorhoz tartozzon
   (`naplok/F218_elteres_engedely.tsv`); az engedélysor tényleges darabszáma egyezzen az elvárttal.
   A fel nem használt és a túlhasznált engedélysor is BUKÁS.

Az engedélyfájl oszlopai: `id` · `fajl` · `szakasz` · `mechanizmus` · `kotes` (`sor` | `minta`) · `regi` · `uj`
· `elvart_db` · `ok`. `sor` kötésnél a `regi` és az `uj` a sor sha256-ának első 16 jegye (`-`: nincs ilyen
oldal, azaz tiszta beszúrás vagy törlés); `minta` kötésnél a `regi` reguláris kifejezés, az `uj` a csere:
a diff-sor akkor illik, ha a minta illik a régi sorra, és a cserével épp az új sort adja.

Kilépési kód: 0 rendben, 1 BUKÁS, 2 a mérce nem futtatható (hash-őr, hiányzó fájl).
"""
import argparse
import difflib
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REFERENCIA_TSV = 'naplok/F218_referencia.tsv'
ENGEDELY_TSV = 'naplok/F218_elteres_engedely.tsv'
REFERENCIA_KONYVTAR = 'lexikon'
NEZETEK = ('TUDOMANYOS', 'KIZARASOK')
ELOSZO = '(a lap eleje)'
ENGEDELY_OSZLOPOK = ('id', 'fajl', 'szakasz', 'mechanizmus', 'kotes', 'regi', 'uj', 'elvart_db', 'ok')
REFERENCIA_OSZLOPOK = ('tipus', 'b_id', 'utvonal', 'sha256', 'meret')
NAPLO_FAJLNEV = '%s_olvasasi_naplo.tsv'   # egyezik a `konfig.NAPLO_FAJLNEV` értékével (teszt őrzi)
NAPLO_OSZLOPOK = ('b_id', 'utvonal', 'sha256')
NEM_FAJL = '-'
# A bemenet-hash őr kivételei (N240, DT920 szerint technikai döntés, S9c): a B51 (`DONTESEK.md`, `dontesek/uj/*.md`)
# minden számkiosztásnál és minden új ág-döntésnél megváltozik, így a fájlszintű hash minden merge után eltörne
# (N200). A lap a B51-ből csak a hivatkozott döntések dátumát és érvényességét olvassa; ha ezek közül bármelyik
# megváltozik, a lap szövege változik, és azt a szakasz-diff méri. A referencia-táblában ezért B51-sor nem áll, és
# az olvasási napló B51-sorai nem vetődnek össze.
HASH_OR_KIVETEL = frozenset({'B51'})


class MerceHiba(Exception):
    """A mérce nem futtatható (megváltozott bemenet, hiányzó fájl)."""


def _olvas(utvonal):
    with open(utvonal, 'rb') as f:
        return f.read().replace(b'\r\n', b'\n')


def _tsv(utvonal, oszlopok):
    sorok = [s for s in _olvas(utvonal).decode('utf-8').split('\n') if s and not s.startswith('#')]
    fejlec = tuple(sorok[0].split('\t'))
    if fejlec != oszlopok:
        raise MerceHiba('%s: a fejléc eltér a várttól: %r' % (utvonal, fejlec))
    ki = []
    for sor in sorok[1:]:
        mezok = sor.split('\t')
        mezok += [''] * (len(oszlopok) - len(mezok))
        ki.append(dict(zip(oszlopok, mezok)))
    return ki


def sor_hash(sor):
    return hashlib.sha256(sor.encode('utf-8')).hexdigest()[:16]


def hash_or(gyoker=GYOKER):
    """A referencia és a mérce bemeneteinek hash-ellenőrzése. Eltérésnél MerceHiba a fájlok listájával."""
    elteres = []
    sorok = _tsv(os.path.join(gyoker, *REFERENCIA_TSV.split('/')), REFERENCIA_OSZLOPOK)
    for sor in sorok:
        if sor['b_id'] in HASH_OR_KIVETEL:
            raise MerceHiba('a referencia-táblában a hash-őr kivétele áll (%s %s): a sor törlendő (N240)'
                            % (sor['b_id'], sor['utvonal']))
        teljes = os.path.join(gyoker, *sor['utvonal'].split('/'))
        if not os.path.isfile(teljes):
            elteres.append('%s %s (hiányzik)' % (sor['b_id'], sor['utvonal']))
            continue
        if hashlib.sha256(_olvas(teljes)).hexdigest() != sor['sha256']:
            elteres.append('%s %s' % (sor['b_id'], sor['utvonal']))
    if elteres:
        raise MerceHiba('a mérce bemenete megváltozott: ' + '; '.join(elteres))
    return len(sorok)


def naplo_or(motivum, uj_konyvtar, gyoker=GYOKER):
    """Az új generátor olvasási naplójának összevetése a referencia-táblával: minden olvasott fájlnak a
    táblában kell állnia, ugyanazzal a hash-sel. Hiányzó napló vagy eltérés MerceHiba. Visszaadja az
    összevetett fájlok számát."""
    ut = os.path.join(uj_konyvtar, NAPLO_FAJLNEV % motivum)
    if not os.path.isfile(ut):
        raise MerceHiba('hiányzik az új generátor olvasási naplója: %s' % ut)
    rogzitett = {sor['utvonal']: sor['sha256']
                 for sor in _tsv(os.path.join(gyoker, *REFERENCIA_TSV.split('/')), REFERENCIA_OSZLOPOK)}
    elteres, db = [], 0
    for sor in _tsv(ut, NAPLO_OSZLOPOK):
        if sor['utvonal'] == NEM_FAJL or sor['b_id'] in HASH_OR_KIVETEL:
            continue
        db += 1
        if sor['utvonal'] not in rogzitett:
            elteres.append('%s %s (nincs a referencia-táblában)' % (sor['b_id'], sor['utvonal']))
        elif rogzitett[sor['utvonal']] != sor['sha256']:
            elteres.append('%s %s (más tartalommal olvasva)' % (sor['b_id'], sor['utvonal']))
    if elteres:
        raise MerceHiba('az új generátor olvasott bemenete nincs rögzítve a mércében: ' + '; '.join(elteres))
    return db


_CIMSOR_RX = re.compile(r'^## (?!#)')
# Alblokkonként készülő szakaszok: amíg a szakasz minden alblokkja el nem készül. A „4. Szótári háttér” a 218a S3
# szeletétől az S8b-ig volt részleges (a pontjai több szeletben készültek; az utolsó a „Miért fontos ez a lelet” rés);
# az S8b óta egészben mérődik. A gépezet megmarad a későbbi, alblokkonként készülő szakaszokhoz.
RESZLEGES_SZAKASZOK = ()
_ALBLOKK_RX = re.compile(r'^(?:#{3,4} |<!-- GENERÁLT-VÉGE: )')


def alblokkok(sorok):
    """A szakasz alblokkjai: [(kulcs, sorok)]. Az alblokk a 3. vagy a 4. szintű címsornál, illetve a generált blokk
    záró jelölőjénél kezdődik; a kulcsa (a 3. szintű cím, a kezdősor), a szakasz eleje (None, None)."""
    ki, harmadik = [((None, None), [])], None
    for sor in sorok:
        if _ALBLOKK_RX.match(sor):
            if sor.startswith('### '):
                harmadik = sor
                ki.append(((harmadik, None), []))
            else:
                ki.append(((harmadik, sor), []))
        ki[-1][1].append(sor)
    return ki


def szakaszol(szoveg):
    """A lap szakaszai a 2. szintű címsorok szerint: [(cím, sorok)]; az első a címsor előtti rész."""
    szakaszok = [(ELOSZO, [])]
    sorok = szoveg.split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    for sor in sorok:
        if _CIMSOR_RX.match(sor):
            szakaszok.append((sor[3:].strip(), []))
        szakaszok[-1][1].append(sor)
    return szakaszok


def sor_diff(regi, uj):
    """A két sorlista eltérései: [(régi sor vagy None, új sor vagy None)]."""
    ki = []
    illeszto = difflib.SequenceMatcher(a=regi, b=uj, autojunk=False)
    for muvelet, a1, a2, b1, b2 in illeszto.get_opcodes():
        if muvelet == 'equal':
            continue
        r, u = regi[a1:a2], uj[b1:b2]
        if muvelet == 'replace' and len(r) == len(u):
            ki.extend(zip(r, u))
        else:
            ki.extend((sor, None) for sor in r)
            ki.extend((None, sor) for sor in u)
    return ki


def _illik(engedely, regi, uj):
    if engedely['kotes'] == 'sor':
        return (engedely['regi'] == (sor_hash(regi) if regi is not None else '-')
                and engedely['uj'] == (sor_hash(uj) if uj is not None else '-'))
    if engedely['kotes'] == 'minta':
        if regi is None or uj is None:
            return False
        minta = re.compile(engedely['regi'])
        return bool(minta.search(regi)) and minta.sub(engedely['uj'], regi) == uj
    raise MerceHiba('ismeretlen kötés az engedélyfájlban: %r (%s)' % (engedely['kotes'], engedely['id']))


def osszevet(fajl, referencia_szoveg, uj_szoveg, engedelyek, teljes=False):
    """Egy nézet összevetése. Visszaad: (szakasz-jelentések, engedély nélküli diff-sorok, használat).

    A szakasz-jelentés: (cím, állapot, diff-sorok száma, engedély nélküliek száma)."""
    regi = dict(szakaszol(referencia_szoveg))
    uj_szakaszok = [(c, s) for c, s in szakaszol(uj_szoveg) if s or c != ELOSZO]
    uj = dict(uj_szakaszok)
    hasznalat = {e['id']: 0 for e in engedelyek}
    jelentes, engedely_nelkul = [], []
    for cim, regi_sorok in szakaszol(referencia_szoveg):
        if cim not in uj:
            if cim == ELOSZO and not teljes:
                continue
            jelentes.append((cim, 'BUKÁS: hiányzik' if teljes else 'nincs kész', len(regi_sorok) if teljes else 0,
                             len(regi_sorok) if teljes else 0))
            if teljes:
                engedely_nelkul.extend((fajl, cim, sor, None) for sor in regi_sorok)
            continue
        nincs_kesz = 0
        if cim in RESZLEGES_SZAKASZOK and not teljes:
            kesz = {kulcs for kulcs, _sorok in alblokkok(uj[cim])}
            regi_al = alblokkok(regi_sorok)
            nincs_kesz = sum(1 for kulcs, _sorok in regi_al if kulcs not in kesz)
            regi_sorok = [sor for kulcs, sorok in regi_al if kulcs in kesz for sor in sorok]
        diff = sor_diff(regi_sorok, uj[cim])
        kint = 0
        for regi_sor, uj_sor in diff:
            illok = [e for e in engedelyek
                     if e['fajl'] == fajl and e['szakasz'] in (cim, '*') and _illik(e, regi_sor, uj_sor)]
            if len(illok) == 1:
                hasznalat[illok[0]['id']] += 1
            else:
                kint += 1
                engedely_nelkul.append((fajl, cim, regi_sor, uj_sor))
        allapot = 'egyezik' if not diff else ('engedéllyel' if not kint else 'BUKÁS')
        if nincs_kesz:
            allapot += ' (részleges: %d alblokk nincs kész)' % nincs_kesz
        jelentes.append((cim, allapot, len(diff), kint))
    for cim, sorok in uj_szakaszok:
        if cim not in regi:
            jelentes.append((cim, 'BUKÁS: a referenciában nincs ilyen szakasz', len(sorok), len(sorok)))
            engedely_nelkul.extend((fajl, cim, None, sor) for sor in sorok)
    return jelentes, engedely_nelkul, hasznalat


def engedelyek_betolt(gyoker=GYOKER):
    utvonal = os.path.join(gyoker, *ENGEDELY_TSV.split('/'))
    if not os.path.isfile(utvonal):
        return []
    sorok = _tsv(utvonal, ENGEDELY_OSZLOPOK)
    for sor in sorok:
        sor['elvart_db'] = int(sor['elvart_db'])
    return sorok


def meres(motivum, uj_konyvtar, gyoker=GYOKER, teljes=False, hash_ellenorzes=True):
    """A teljes mérés egy motívumra. Visszaad egy szótárt a jelentéshez; a `bukas` kulcs a végeredmény."""
    if hash_ellenorzes:
        hash_or(gyoker)
        naplo_or(motivum, uj_konyvtar, gyoker)
    engedelyek = engedelyek_betolt(gyoker)
    hasznalat = {e['id']: 0 for e in engedelyek}
    jelentesek, engedely_nelkul = {}, []
    for nezet in NEZETEK:
        fajlnev = '%s_%s.md' % (motivum, nezet)
        uj_ut = os.path.join(uj_konyvtar, fajlnev)
        if not os.path.isfile(os.path.join(gyoker, REFERENCIA_KONYVTAR, fajlnev)):
            if os.path.isfile(uj_ut):
                raise MerceHiba('az új lapnak nincs referenciája: %s' % fajlnev)
            continue
        if not os.path.isfile(uj_ut):
            if teljes:
                raise MerceHiba('hiányzik az új lap: %s' % uj_ut)
            continue
        referencia = _olvas(os.path.join(gyoker, REFERENCIA_KONYVTAR, fajlnev)).decode('utf-8')
        jel, kint, haszn = osszevet(nezet, referencia, _olvas(uj_ut).decode('utf-8'), engedelyek, teljes)
        jelentesek[nezet] = jel
        engedely_nelkul.extend(kint)
        for azonosito, db in haszn.items():
            hasznalat[azonosito] += db
    kesz_szakaszok = {(nezet, cim) for nezet, jel in jelentesek.items() for cim, allapot, _d, _k in jel
                      if allapot != 'nincs kész'}
    engedely_hiba = []
    for e in engedelyek:
        erintett = teljes or any(n == e['fajl'] and (e['szakasz'] in (c, '*')) for n, c in kesz_szakaszok)
        if erintett and hasznalat[e['id']] != e['elvart_db']:
            engedely_hiba.append((e['id'], e['elvart_db'], hasznalat[e['id']]))
    return {
        'jelentesek': jelentesek,
        'engedely_nelkul': engedely_nelkul,
        'hasznalat': hasznalat,
        'engedely_hiba': engedely_hiba,
        'bukas': bool(engedely_nelkul or engedely_hiba),
    }


def jelentes_szoveg(eredmeny):
    sorok = []
    for nezet, jel in eredmeny['jelentesek'].items():
        sorok.append('== %s' % nezet)
        for cim, allapot, diff_db, kint in jel:
            sorok.append('  %-60s %-12s diff-sor: %d, engedély nélkül: %d' % (cim[:60], allapot, diff_db, kint))
    if eredmeny['hasznalat']:
        sorok.append('== engedélysorok (tényleges / elvárt)')
        hibas = {h[0] for h in eredmeny['engedely_hiba']}
        for azonosito, db in sorted(eredmeny['hasznalat'].items()):
            sorok.append('  %s: %d%s' % (azonosito, db, '  ← ELTÉR' if azonosito in hibas else ''))
    for azonosito, elvart, tenyleges in eredmeny['engedely_hiba']:
        sorok.append('BUKÁS: a(z) %s engedélysor elvárt darabszáma %d, a tényleges %d' % (azonosito, elvart, tenyleges))
    sorok.append('EREDMÉNY: %s (engedély nélküli diff-sor: %d)' % (
        'BUKÁS' if eredmeny['bukas'] else 'RENDBEN', len(eredmeny['engedely_nelkul'])))
    return '\n'.join(sorok)


def reszletes_szoveg(eredmeny):
    """Az engedély nélküli diff-sorok teljes listája (fájlba, nem a konzolra)."""
    sorok = []
    for fajl, cim, regi, uj in eredmeny['engedely_nelkul']:
        sorok.append('@@ %s | %s' % (fajl, cim))
        sorok.append('- [%s] %s' % (sor_hash(regi) if regi is not None else '-', regi if regi is not None else ''))
        sorok.append('+ [%s] %s' % (sor_hash(uj) if uj is not None else '-', uj if uj is not None else ''))
    return '\n'.join(sorok) + '\n'


# --- A 8.2/1 független számlálói ----------------------------------------------------------------------------------
# A lapon kimondott számok összevetése a regresszió saját, egyszerű számlálásával az adattáblákból (nem a generátor
# kódjával). A számok a kész lap szövegéből jönnek (a mondatok alakja a sablontáblából), a számlálás a táblákból,
# `split('\t')`-vel.

ELOFORDULAS_TSV = 'adat/elofordulasok.tsv'
JELOLT_TSV = 'adat/jeloltek.tsv'
BLOKK_TSV = 'naplok/F123_teljesseg_%s_blokkok.tsv'
KONYV_TSV = 'konkordancia/Konyv_normalizalo_tabla.tsv'
TAHOT_TSV = 'konkordancia/TAHOT_kivonat.tsv'
TSK_TSV = 'konkordancia/TSK_kereszthivatkozasok.tsv'
MEGFELELTETES_TSV = 'konkordancia/Karoli_versmegfeleltetes.tsv'
KAROLI_KH_TSV = 'konkordancia/Karoli_KH_javitott.tsv'
LXX_KONYVTAR = 'konkordancia/LXX_OS'
LXX_DONTES_TSV = 'adat/lxx_dontesek.tsv'
LXX_MINUSZ = 'lxx_minusz'
_OSSZESITES_RX = re.compile(r'\*Összesítés: ([^*\n]+)\.\*')
_OSSZ_ELEM_RX = re.compile(r'([^=,]+)=(\d+)')
_MEGALLAPITOTT_RX = re.compile(r'ezek (\d+) megállapított versében')
# A független számlálás ismert, döntésre váró eltérései (motívum, számláló) → a nyitott tétel: a sor „ELTÉR (ismert)”
# jelzést kap, és nem buktat. Csak a megnevezett számra és értékpárra szól (más eltérés BUKÁS marad). Üres: az
# egyetlen tétele (N196) szerkesztői döntéssel (2026-11-23, részenként) megszűnt.
ISMERT_ELTERES = {}
TSK_KUSZOB = 15   # egyezik a `konfig.TSK_SZAVAZAT_KUSZOB` értékével (a régi Votes ≥ 15)
_KH_RX = re.compile(r'A motívum (\d+) helyéből (\d+) helyről mutat utalás[^.]*, összesen (\d+)')
OSZ_KONYVEK_SZAMA = 39
_TARTOMANY_RX = re.compile(r'(.+ \d+):(\d+)[-–](\d+)$')
_CSOPORT_RX = re.compile(r'blokk-(?:kizárás|sor)[^:|]*:\s*(\d+) vers')
_LISTA_RX = re.compile(r'\b(blokk|osztaly)=([^),\s]+)')
_HALO_RX = re.compile(r'halo=(\w+)')
_SZAM = r'(\d[\d\u00a0 ]*)'
_OSSZEADAS_RX = re.compile(r'\*\*Összeadás:\*\* ' + _SZAM + r' \(a motívumhoz tartozik\) \+ ' + _SZAM
                           + r' \(csoportosan kizárva\) \+ ' + _SZAM + r' \(egyenként elutasítva\) = ' + _SZAM
                           + r' megvizsgált vers\. Döntés nélkül maradt vers: ' + _SZAM + r'\.')
_OSZ_VERSEK_RX = re.compile(r'A motívum ószövetségi helyei (\d+) versre terjednek')
_IGE_VERSEK_RX = re.compile(r'amelyekben az ige a héber szövegben áll \((\d+) vers\)')
_TABLA_HELY_RX = re.compile(r'^\| \[([^\]]+)\]\(#ige-')


def _szam(szoveg):
    return int(re.sub(r'\D', '', szoveg))


def _tabla_sorai(utvonal):
    """Egy tábla sorai szótárként (a fejléc az első nem megjegyzés sor), `split('\\t')`-vel."""
    sorok = [s for s in _olvas(utvonal).decode('utf-8').split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def _versek(kod):
    m = _TARTOMANY_RX.match(kod.strip())
    if m and int(m.group(2)) <= int(m.group(3)):
        return ['%s:%d' % (m.group(1), v) for v in range(int(m.group(2)), int(m.group(3)) + 1)]
    return [kod.strip()]


def _szakasz_szovege(lap, sorszam):
    kezd = lap.find('\n## %d. ' % sorszam)
    if kezd < 0:
        return ''
    veg = lap.find('\n## ', kezd + 1)
    return lap[kezd:veg if veg >= 0 else len(lap)]


def _szamolt_dontesi_ut(motivum, gyoker, bent):
    """(csoport, egyen, nyitva) a döntésnaplóból és a csoportlistából: minden vers egyszer számít; a két csoportban
    is álló vers az előbb álló csoportnál; az egyenként elbírált vers, ha a motívumhoz tartozik, nem számít."""
    jeloltek = [r for r in _tabla_sorai(os.path.join(gyoker, JELOLT_TSV))
                if r['id'] == motivum and r.get('jelolt_tipus') == 'elofordulas'
                and r['dontes'] in ('elutasítva', 'nyitva')]
    blokk_ut = os.path.join(gyoker, BLOKK_TSV % motivum)
    lista = _tabla_sorai(blokk_ut) if os.path.isfile(blokk_ut) else []
    kulon = {r['igehely'] for r in jeloltek
             if 'külön sor' in r['forras_kereses'] and not _CSOPORT_RX.search(r['forras_kereses'].split(' | ')[0])}
    latott, csoport, nyitva = set(), 0, 0
    egyen = {}
    for r in jeloltek:
        m = _CSOPORT_RX.search(r['forras_kereses'].split(' | ')[0])
        if m is None:
            for v in _versek(r['igehely']):
                if v not in bent:
                    egyen.setdefault(v, set()).add(r['dontes'])
            continue
        n = int(m.group(1))
        lk, hk = _LISTA_RX.search(r['forras_kereses']), _HALO_RX.search(r['forras_kereses'])
        tagok = None
        if lk and lista:
            tagok = sorted({s['igehely'] for s in lista if s.get(lk.group(1)) == lk.group(2)
                            and (hk is None or 'halo' not in s or s['halo'] == hk.group(1))} - kulon)
            if len(tagok) != n:
                tagok = None
        uj = n if tagok is None else len([t for t in tagok if t not in latott])
        if tagok is not None:
            latott.update(tagok)
        if r['dontes'] == 'nyitva':
            nyitva += uj
        else:
            csoport += uj
    nyitva += sum(1 for d in egyen.values() if 'nyitva' in d)
    return csoport, sum(1 for d in egyen.values() if 'nyitva' not in d), nyitva


def _szamolt_kh(gyoker, helyek):
    """(hány helyről van utalás, az utalások száma) a TSK-ból (legalább `TSK_KUSZOB` szavazat, a Károli-vers
    KJV-kulcsán, a célvers Károli-megfelelőinként) és a Károli-KH javított táblájának megerősített soraiból; a
    tartomány-igehely nem vizsgálható."""
    konyv = {r['Magyar rövidítés']: r['STEPBible-rövidítés'] for r in _tabla_sorai(os.path.join(gyoker, KONYV_TSV))}
    megf = {r['igehely_karoli']: r['igehely_kjv'] for r in _tabla_sorai(os.path.join(gyoker, MEGFELELTETES_TSV))}
    kjv_karoli = {}
    for karoli, kjv in megf.items():
        kjv_karoli.setdefault(karoli.rsplit(' ', 1)[0] + ' ' + kjv, []).append(karoli)
    tsk = {}
    for r in _tabla_sorai(os.path.join(gyoker, TSK_TSV)):
        tsk.setdefault(r['Igehely'], []).append((r['Kapcsolódó igehely'], int(r['Votes'] or 0)))
    kh = {}
    for r in _tabla_sorai(os.path.join(gyoker, KAROLI_KH_TSV)):
        if r['szint'] == 'megerositett':
            kh.setdefault(r['igehely'], set()).add(r['kapcsolodo'])
    van, osszes = 0, 0
    for hely in helyek:
        if _TARTOMANY_RX.match(hely):
            continue
        konyvnev, fv = hely.rsplit(' ', 1)
        kjv = konyvnev + ' ' + megf.get(hely, fv)
        n = 0
        if hely in kjv_karoli.get(kjv, [hely]):
            n += sum(max(1, len(kjv_karoli.get(cel, [cel]))) for cel, sz in tsk.get(kjv, ()) if sz >= TSK_KUSZOB)
        n += len(kh.get('%s.%s' % (konyv[konyvnev], fv.replace(':', '.')), ()))
        osszes += n
        van += 1 if n else 0
    return van, osszes


def _lxx_egyezo(gyoker, versek, gorog):
    """Az ószövetségi versek közül azok, amelyeknek Septuaginta-szövegében a motívum valamely görög Strong-száma áll
    (a Septuaginta könyvenkénti fájljai, a Károli-kulcson; a generátor kódja nélkül)."""
    ki = set()
    for nev in sorted(os.listdir(os.path.join(gyoker, *LXX_KONYVTAR.split('/')))):
        if not nev.endswith('.tsv'):
            continue
        fej = None
        for sor in _olvas(os.path.join(gyoker, *LXX_KONYVTAR.split('/'), nev)).decode('utf-8').split('\n'):
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fej is None:
                fej = mezok
                if 'igehely_karoli' not in fej or 'strong' not in fej:
                    break          # a könyvtár segédtáblája, nem szövegkönyv
                k, s = fej.index('igehely_karoli'), fej.index('strong')
                continue
            if len(mezok) > s and mezok[k] in versek and re.sub(r'\D', '', mezok[s]) \
                    and int(re.sub(r'\D', '', mezok[s])) in gorog:
                ki.add(mezok[k])
    return ki


def szamlalok(motivum, uj_konyvtar, gyoker=GYOKER):
    """A 8.2/1 számlálói: [(név, a lapon, számolva)]; a lapon nem álló szám None (a mondat a lapon nem szerepel)."""
    lap = _olvas(os.path.join(uj_konyvtar, '%s_TUDOMANYOS.md' % motivum)).decode('utf-8')
    elof = [r for r in _tabla_sorai(os.path.join(gyoker, ELOFORDULAS_TSV)) if r['id'] == motivum]
    osz = {r['Magyar rövidítés'] for r in _tabla_sorai(os.path.join(gyoker, KONYV_TSV))[:OSZ_KONYVEK_SZAMA]}
    ki = []
    # az igehelyek halmaza: a 2. szakasz táblája és az előfordulás-tábla
    helyek = [m.group(1) for m in (_TABLA_HELY_RX.match(s) for s in _szakasz_szovege(lap, 2).split('\n')) if m]
    ki.append(('előfordulás-sorok (2. szakasz)', len(helyek), len(elof)))
    ki.append(('az igehelyek halmaza egyezik (2. szakasz)', int(sorted(helyek) == sorted(r['igehely'] for r in elof)),
               1))
    # a Döntési út összeadása
    bent = []
    for r in elof:
        bent.extend(v for v in _versek(r['igehely']) if v not in bent)
    m = _OSSZEADAS_RX.search(_szakasz_szovege(lap, 1))
    csoport, egyen, nyitva = _szamolt_dontesi_ut(motivum, gyoker, set(bent))
    lapon = [_szam(x) for x in m.groups()] if m else [None] * 5
    for nev, a, b in zip(('motívum versei (1.)', 'csoportosan kizárva (1.)', 'egyenként elutasítva (1.)',
                          'megvizsgált versek (1.)', 'döntés nélkül (1.)'),
                         lapon, (len(bent), csoport, egyen, len(bent) + csoport + egyen + nyitva, nyitva)):
        ki.append((nev, a, b))
    # a kereszthivatkozások: hány helyről van utalás, és összesen hány
    m = _KH_RX.search(_szakasz_szovege(lap, 6))
    van, osszes = _szamolt_kh(gyoker, [r['igehely'] for r in elof])
    ki.append(('KH: helyek utalással (6.)', int(m.group(2)) if m else None, van))
    ki.append(('KH: utalások összesen (6.)', int(m.group(3)) if m else None, osszes))
    # az LXX-összesítés: a motívum ószövetségi versei
    osz_versek = [v for v in bent if v.rsplit(' ', 1)[0] in osz]
    m = _OSZ_VERSEK_RX.search(_szakasz_szovege(lap, 5))
    ki.append(('ószövetségi versek (5.)', int(m.group(1)) if m else None, len(osz_versek)))
    # az LXX-összesítés részei (N238): az egyező versek (a Septuaginta-versben a motívum görög szava) és az LXX-minusz
    # (a döntéstábla sora) saját számlálással; az összesítés összege a motívum ószövetségi verseinek száma. A „szócsalád”
    # felosztás a generátor szótő-algoritmusa: azt a számláló nem ismétli meg, csak a megállapított versek számának
    # azonosságát méri a lap saját összesítésével (egyező + szócsalád + eltérő)
    otodik = _szakasz_szovege(lap, 5)
    m = _OSSZESITES_RX.search(otodik)
    if m:
        ertek = {k.strip(): int(v) for k, v in _OSSZ_ELEM_RX.findall(m.group(1))}
        ki.append(('LXX: az összesítés összege (5.)', sum(ertek.values()), len(osz_versek)))
        gorog = {int(t[1:]) for r in elof for t in re.findall(r'\bG\d{1,4}\b', r['strong'] + ' ' + r['gerinc_elem'])}
        egyezo = _lxx_egyezo(gyoker, set(osz_versek), gorog)
        ki.append(('LXX: egyező versek (5.)', ertek.get('egyező'), len(egyezo)))
        minusz = {r['igehely'] for r in _tabla_sorai(os.path.join(gyoker, LXX_DONTES_TSV))
                  if r['tipus'].strip() == LXX_MINUSZ and r['igehely'] in osz_versek and r['igehely'] not in egyezo}
        ki.append(('LXX: LXX-minusz (5.)', ertek.get('LXX-minusz'), len(minusz)))
        m2 = _MEGALLAPITOTT_RX.search(otodik)
        if m2:
            ki.append(('LXX: megállapított = egyező + szócsalád + eltérő (5.)', int(m2.group(1)),
                       ertek.get('egyező', 0) + ertek.get('ugyanaz a szócsalád', 0) + ertek.get('eltérő', 0)))
    # a szópár-lánc: a szópár első (ige) tagja a héber szövegben
    par = next((r['gerinc_elem'].split('+')[0] for r in elof if '+' in r.get('gerinc_elem', '')), None)
    m = _IGE_VERSEK_RX.search(_szakasz_szovege(lap, 9))
    if par is not None or m is not None:
        tahot = {}
        if par is not None:
            halmaz = set(osz_versek)
            for s in _olvas(os.path.join(gyoker, TAHOT_TSV)).decode('utf-8').split('\n')[1:]:
                mezok = s.split('\t')
                if len(mezok) > 1 and mezok[0] in halmaz and mezok[1] == par:
                    tahot[mezok[0]] = True
        ki.append(('a szópár igéje a héber szövegben (9.)', int(m.group(1)) if m else None, len(tahot)))
    return ki


def szamlalo_jelentes(sorok, motivum=None):
    ki, hiba = [], False
    for nev, lapon, szamolt in sorok:
        if lapon is None:
            ki.append('  %-45s a lapon nem áll · számolva: %d' % (nev, szamolt))
            continue
        jo = lapon == szamolt
        ismert = None if jo else ISMERT_ELTERES.get((motivum, nev, lapon, szamolt))
        hiba = hiba or (not jo and ismert is None)
        ki.append('  %-45s lapon: %d · számolva: %d%s' % (
            nev, lapon, szamolt, '' if jo else ('  ← ELTÉR (ismert: %s)' % ismert if ismert else '  ← ELTÉR')))
    ki.append('SZÁMLÁLÓK: %s' % ('BUKÁS' if hiba else 'RENDBEN'))
    return '\n'.join(ki), hiba


def main(argv=None):
    p = argparse.ArgumentParser(description='Az új lap összevetése a referenciával')
    p.add_argument('--id', required=True)
    p.add_argument('--uj', required=True, help='az új generátor kimeneti könyvtára')
    p.add_argument('--teljes', action='store_true', help='a hiányzó szakasz is BUKÁS (teljes lap)')
    p.add_argument('--reszletes', help='az engedély nélküli diff-sorok ebbe a fájlba kerülnek')
    p.add_argument('--hash-or-nelkul', action='store_true', help='csak fejlesztés közben: a hash-őr kihagyása')
    p.add_argument('--szamlalok', action='store_true',
                   help='csak a 8.2/1 független számlálói (a referencia-diff nélkül; a második mintalap mércéje)')
    a = p.parse_args(argv)
    if a.szamlalok:
        szoveg, hiba = szamlalo_jelentes(szamlalok(a.id, a.uj), a.id)
        print(szoveg)
        return 1 if hiba else 0
    try:
        eredmeny = meres(a.id, a.uj, teljes=a.teljes, hash_ellenorzes=not a.hash_or_nelkul)
    except MerceHiba as hiba:
        print('A MÉRCE NEM FUTTATHATÓ: %s' % hiba)
        return 2
    print(jelentes_szoveg(eredmeny))
    if a.reszletes:
        with open(a.reszletes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(reszletes_szoveg(eredmeny))
    return 1 if eredmeny['bukas'] else 0


if __name__ == '__main__':
    sys.exit(main())
