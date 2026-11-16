"""lapgen.regresszio — az új lap összevetése a referenciával (F218a brief 8.1).

    python eszkozok/lapgen/regresszio.py --id <ID> --uj <könyvtár> [--teljes] [--reszletes <fájl>]

Mit ellenőriz:
1. **Bemenet-hash őr.** A `naplok/F218_referencia.tsv` rögzíti a referencialap és a mérce minden
   bemenetének hash-ét (sorvég-normalizált tartalomból). Ha egy hash eltér, a mérés megáll:
   „a mérce bemenete megváltozott”. Az új generátor olvasási naplója (`<ID>_olvasasi_naplo.tsv` a lap
   mellett) is összevetődik a táblával: ha az új generátor olyan fájlt olvasott, amely nincs a táblában,
   vagy más tartalommal olvasta, a mérés megáll.
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
        if sor['utvonal'] == NEM_FAJL:
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
# szeletétől az S8-ig részleges (a pontjai több szeletben készülnek; a „Miért fontos ez a lelet” rés a kereté).
RESZLEGES_SZAKASZOK = ('4. Szótári háttér',)
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


def main(argv=None):
    p = argparse.ArgumentParser(description='Az új lap összevetése a referenciával')
    p.add_argument('--id', required=True)
    p.add_argument('--uj', required=True, help='az új generátor kimeneti könyvtára')
    p.add_argument('--teljes', action='store_true', help='a hiányzó szakasz is BUKÁS (teljes lap)')
    p.add_argument('--reszletes', help='az engedély nélküli diff-sorok ebbe a fájlba kerülnek')
    p.add_argument('--hash-or-nelkul', action='store_true', help='csak fejlesztés közben: a hash-őr kihagyása')
    a = p.parse_args(argv)
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
