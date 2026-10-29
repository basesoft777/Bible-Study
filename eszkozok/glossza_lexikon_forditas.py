#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/glossza_lexikon_forditas.py -- F121 GLOSSZA_FORDITAS (DT-F121c: a #140 eszkozetol kulon fajl):
a lexikonoldalak "(forditasra var)" jelolesu szotari egysegeinek listaja es rogzitese.

  lista --id ISTENTISZT-001 [--kimenet <repon kivuli konyvtar>]
      A generator sajat forditas_ehhez() hivasait naplozza egy repon kivuli lexikon-renderben, igy a
      kulcs es a forrasszoveg pontosan az, amit a lap keres. Kimenet: naplok/F121_GLOSSZA_FORDITAS_lista.tsv
      (kulcs, forrasszoveg, forras_hash, allapot: megvan / hianyzik / elavult).
  A forrasszoveg-feloldo (forras_szoveg) a 13. szabaly (ellenoriz.py) forrasa is: egy feloldo, nem ket masolat.

Olvasas split('\\t')-bel (CLAUDE.md: a csv modul tilos).
"""
import sys
import os
import hashlib
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(GYOKER, 'konkordancia')
LISTA = os.path.join(GYOKER, 'naplok', 'F121_GLOSSZA_FORDITAS_lista.tsv')
DBH_JELENTESEK = os.path.join(KONKORDANCIA, 'UBS_DBH_jelentesek.tsv')
FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forras_hossz',
          'allapot', 'forrasszoveg']
EM_DASH = '—'

# szotar -> melyik forrasoszlopbol szarmazik a mezo forrasszovege (SEMA 2.14)
DBH_MEZOK = {'definicio_hu': 'definicio_rovid', 'glosszak_hu': 'glosszak'}


def sha1(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def tsv_sorok(path):
    """Fejlecsoros TSV, '#'-megjegyzessorok nelkul; split('\\t')."""
    with open(path, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


_dbh_idx = None


def dbh_forras_idx(konkordancia_dir=KONKORDANCIA):
    """{(strong, lexid, mezo): forrasszoveg} az UBS_DBH_jelentesek.tsv-bol (strongonkent az elso sor)."""
    global _dbh_idx
    idx = {}
    for r in tsv_sorok(os.path.join(konkordancia_dir, 'UBS_DBH_jelentesek.tsv')):
        for mezo, oszlop in DBH_MEZOK.items():
            idx.setdefault((r['strong'], r['lexid'], mezo), r.get(oszlop, ''))
    return idx


def forras_szoveg_dbh(sor, idx):
    """Az UBS_DBH forditasok.tsv-sor forrasszovege (entry_id = lexid, jelentes_szam = '—'), kulonben None."""
    if sor.get('szotar') != 'UBS_DBH' or sor.get('jelentes_szam') != EM_DASH:
        return None
    return idx.get((sor['strong'], sor['entry_id'], sor['mezo']))


def lista_keszit(motivum_id, kimenet):
    """A generator forditas_ehhez() hivasait naplozva rendereli a lapot kimenet-be (repon kivuli konyvtar)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
    import lexikon_general as lg
    import general
    hivasok = {}
    eredeti = lg.forditas_ehhez

    def naplozo(szotar, strong, entry_id, jelentes_szam, mezo):
        hu = eredeti(szotar, strong, entry_id, jelentes_szam, mezo)
        hivasok.setdefault((szotar, strong, entry_id, jelentes_szam, mezo), bool(hu))
        return hu

    lg.forditas_ehhez = naplozo
    regi_argv = sys.argv
    sys.argv = ['general.py', '--cel', 'lexikon', '--id', motivum_id, '--kimenet', kimenet]
    try:
        general.main()
    finally:
        sys.argv = regi_argv
        lg.forditas_ehhez = eredeti
    return hivasok


def lista(motivum_id, kimenet=None):
    kimenet = kimenet or tempfile.mkdtemp(prefix='F121_lista_')
    if os.path.abspath(kimenet).startswith(GYOKER):
        raise SystemExit('a --kimenet a repon kivuli konyvtar legyen')
    hivasok = lista_keszit(motivum_id, kimenet)
    dbh = dbh_forras_idx()
    dntg = {(r['strong'], r['lexid'], r['entry_kod']): r for r in tsv_sorok(os.path.join(KONKORDANCIA, 'UBS_DNTG_jelentesek.tsv'))}
    kimeneti = []
    for kulcs, van in sorted(hivasok.items()):
        szotar, strong, entry_id, jsz, mezo = kulcs
        if van:
            continue
        forras = None
        if szotar == 'UBS_DBH':
            forras = dbh.get((strong, entry_id, mezo))
        elif szotar == 'UBS_DNTG':
            r = dntg.get((strong, entry_id, jsz))
            if r:
                forras = r.get({'definicio_hu': 'definicio_rovid', 'glosszak_hu': 'glosszak'}.get(mezo, ''), None)
        kimeneti.append((kulcs, forras))
    with open(LISTA, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(FEJLEC) + '\n')
        for kulcs, forras in kimeneti:
            if forras is None:
                sor = list(kulcs) + ['', '', 'nincs_forras', '']
            else:
                sor = list(kulcs) + [sha1(forras), str(len(forras)), 'hianyzik', forras.replace('\t', ' ')]
            f.write('\t'.join(sor) + '\n')
    print('hianyzo egyedi egyseg: %d (lista: %s; render: %s)' % (len(kimeneti), LISTA, kimenet))
    for kulcs, forras in kimeneti:
        print(' ', kulcs, '' if forras is not None else '-- nincs forrasszoveg')
    return kimeneti


# ---------------------------------------------------------------------------
# F121 mankók (brief 2a, DT239–DT242; a felhasználó 2026-10-29: „nem engedem el”): `manko`, `szojegyzek`, `visszamenoleges`.
# A mankó javasol és jelez, NEM ír át: az eltérő sor kézi ítéletre áll meg.
# ---------------------------------------------------------------------------
import re
from collections import Counter, defaultdict

FORDITASOK = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
TERMINOLOGIA = os.path.join(GYOKER, 'adat', 'terminologia.tsv')
GLOSSZAK_HEBER = os.path.join(GYOKER, 'adat', 'glosszak_heber_hu.tsv')
KAROLI_PAROK = os.path.join(GYOKER, 'adat', 'karoli_strong')
MANKO_KI = os.path.join(GYOKER, 'naplok', 'F121_GLOSSZA_FORDITAS_manko.tsv')
SZOJEGYZEK_KI = os.path.join(GYOKER, 'naplok', 'F121_GLOSSZA_FORDITAS_szojegyzek_javaslat.tsv')
VISSZA_KI = os.path.join(GYOKER, 'naplok', 'F121_GLOSSZA_FORDITAS_visszamenoleges.tsv')
SZAMJEL = ('F121 (DT393)', 'F121.8')          # a megjegyzes mező eleje: a menet új / cserélt sorai
KOTOSZO = {'valaki', 'valakinek', 'valakit', 'valakivel', 'valakire', 'valahol', 'valamit', 'valaminek', 'lenni', 'szó',
           'szerint', 'innen', 'olyan', 'amellyel', 'cselekvés', 'állapot', 'folyamat', 'egy', 'vagy', 'azt', 'hogy'}


def elemek(glossza):
    """A ';'-tagolt glossza elemei, a zárójeles pontosítás nélkül: 'nevezni; nevet adni' -> ['nevezni', 'nevet adni']."""
    ki = [re.sub(r'\([^)]*\)', '', e).strip() for e in glossza.split(';')]
    return [e for e in ki if e]


def tovek(szoveg, minhossz=4):
    """A tartalmas szavak tövei (első 4 betű): a magyar toldalékolás ellen, a Károli-alakokkal való összevetéshez."""
    return {w[:4] for w in re.findall(r'[a-záéíóöőúüű]+', szoveg.lower()) if len(w) >= minhossz and w not in KOTOSZO}


def ellenorzendo_szavak(mezo, hu):
    """Az a magyar szövegrész, amelynek szóhasználatát a szójegyzék/Károli/BDB ellen mérjük: glosszánál az egész, definíciónál
    a „szó szerint: …;” rész (a leíró „olyan cselekvés, amellyel…” rész nem szójegyzéki szó). Üres, ha nincs ilyen."""
    if mezo == 'glosszak_hu':
        return hu
    m = re.match(r'szó szerint:\s*([^;]+);', hu)
    return m.group(1) if m else ''


def egyenertek_tabla():
    """{angol_elem: Counter(magyar_elem)} a gyorsítótár már elfogadott glosszáiból: UBS_DNTG (angol glosszák ';'-elemei, elemszám
    egyezésénél páronként), a TBESH-glosszák (glosszak_heber_hu, fo=igen) és a v1–v4 terminológia. A menet saját sorai kimaradnak."""
    d = defaultdict(Counter)
    dntg = {(r['strong'], r['lexid'], r['entry_kod']): r['glosszak']
            for r in tsv_sorok(os.path.join(KONKORDANCIA, 'UBS_DNTG_jelentesek.tsv'))}
    for r in tsv_sorok(FORDITASOK):
        if r['szotar'] == 'UBS_DNTG' and r['mezo'] == 'glosszak_hu' and not r['megjegyzes'].startswith(SZAMJEL):
            en = [e.strip() for e in dntg.get((r['strong'], r['entry_id'], r['jelentes_szam']), '').split(';') if e.strip()]
            hu = [e.strip() for e in r['forditas_hu'].split(';') if e.strip()]
            if en and len(en) == len(hu):
                for a, b in zip(en, hu):
                    d[a.lower()][b.lower()] += 1
    for r in tsv_sorok(GLOSSZAK_HEBER):
        if r['glossza_en'] and r['glossza_hu'] and r['fo'] == 'igen':
            d[r['glossza_en'].lower()][r['glossza_hu'].lower()] += 1
    for r in tsv_sorok(TERMINOLOGIA):
        d[r['angol'].lower()][r['magyar'].lower()] += 1
    return d


def szojegyzek_ellenorzes(sor, angol, tabla):
    """-> (allapot, reszlet). A sor glosszaelemei közül azokat nézi, amelyeknek az angol megfelelője a táblában már szerepel:
    egyezik / utkozik (versengő magyar alak) / nincs_adat; definíciónál nem_glossza."""
    if sor['mezo'] != 'glosszak_hu':
        return 'nem_glossza', ''
    en = [e.lower() for e in elemek(angol)]
    hu = [e.strip().lower() for e in sor['forditas_hu'].split(';')]
    van, utkozes = 0, []
    for e in en:
        if e not in tabla:
            continue
        van += 1
        elfogadott = tabla[e]
        if not any(h == a or h in a or a in h for a in elfogadott for h in hu):
            utkozes.append('%s: a tábla %s, a sor %s' % (e, '/'.join('%s×%d' % x for x in elfogadott.most_common(3)), '; '.join(hu)))
    if utkozes:
        return 'utkozik', ' | '.join(utkozes)
    return ('egyezik', '%d elem egyezik' % van) if van else ('nincs_adat', '')


def karoli_alakok_strongra(strong, mappa=None):
    """Counter(kisbetűs Károli-alak) a #22 párosításból (adat/karoli_strong/parok_*.tsv) — H és G Strongra is; a Strong
    nullával kitöltött és kitöltetlen alakja is egyezik (H0430 ~ H430)."""
    mappa = mappa or KAROLI_PAROK
    cel = strong[0] + str(int(strong[1:5]))
    c = Counter()
    for fn in sorted(os.listdir(mappa)):
        if not fn.startswith('parok_'):
            continue
        with open(os.path.join(mappa, fn), encoding='utf-8') as f:
            for l in f:
                if l.startswith('#') or l.startswith('vers\t'):
                    continue
                m = l.rstrip('\n').split('\t')
                if len(m) > 5 and len(m[5]) >= 5 and m[5][1:5].isdigit() and m[5][0] + str(int(m[5][1:5])) == cel:
                    c[m[2].lower()] += 1
    return c


def karoli_ellenorzes(sor, karoli):
    """egyezik: a vizsgált magyar szövegrész valamelyik töve megvan a Strong Károli-alakjai között; nem_talal: nincs
    (a leggyakoribb alakok a részletben); nincs_ellenorzendo: leíró definíció."""
    t = tovek(ellenorzendo_szavak(sor['mezo'], sor['forditas_hu']))
    if not t:
        return 'nincs_ellenorzendo', ''
    talalat = Counter()
    for alak, n in karoli.items():
        if alak[:4] in t:
            talalat[alak[:4]] += n
    if talalat:
        return 'egyezik', ', '.join('%s×%d' % x for x in talalat.most_common(3))
    return 'nem_talal', 'a Strong leggyakoribb Károli-alakjai: ' + ', '.join('%s×%d' % x for x in karoli.most_common(6))


def bdb_hu_szoveg(strong):
    """A Strong BDB-magyar szövege a gyorsítótárból (a nem elavult sorok összefűzve) -- a rangsor 3. szintje."""
    return ' '.join(r['forditas_hu'] for r in tsv_sorok(FORDITASOK)
                    if r['szotar'] == 'BDB' and r['strong'] == strong and r['allapot'] != 'elavult')


def bdb_ellenorzes(sor, bdb_szoveg):
    if not sor['strong'].startswith('H'):
        return 'nem_heber', ''
    t = tovek(ellenorzendo_szavak(sor['mezo'], sor['forditas_hu']))
    if not t:
        return 'nincs_ellenorzendo', ''
    kozos = sorted(t & tovek(bdb_szoveg))
    return ('egyezik', ', '.join(kozos)) if kozos else ('nem_talal', 'a vizsgált tövek: ' + ', '.join(sorted(t)))


def menet_sorai():
    return [r for r in tsv_sorok(FORDITASOK) if r['megjegyzes'].startswith(SZAMJEL)]


def parancs_manko():
    sorok = menet_sorai()
    tabla = egyenertek_tabla()
    forras = {}
    for r in tsv_sorok(os.path.join(KONKORDANCIA, 'UBS_DBH_jelentesek.tsv')):
        for mezo, o in DBH_MEZOK.items():
            forras.setdefault(('UBS_DBH', r['strong'], r['lexid'], EM_DASH, mezo), r[o])
    for r in tsv_sorok(os.path.join(KONKORDANCIA, 'UBS_DNTG_jelentesek.tsv')):
        for mezo, o in DBH_MEZOK.items():
            forras.setdefault(('UBS_DNTG', r['strong'], r['lexid'], r['entry_kod'], mezo), r[o])
    karoli_cache, bdb_cache = {}, {}
    testver = defaultdict(set)      # lexid -> a lexidet osztó Strongok (az UBS egy jelentést több Strongnak ad: qara I/II, H7121/H7122/H7125)
    for fn in ('UBS_DBH_jelentesek.tsv', 'UBS_DNTG_jelentesek.tsv'):
        for r_ in tsv_sorok(os.path.join(KONKORDANCIA, fn)):
            testver[r_['lexid']].add(r_['strong'])
    ki = []
    for s in sorok:
        k = (s['szotar'], s['strong'], s['entry_id'], s['jelentes_szam'], s['mezo'])
        angol = forras.get(k, '')
        strongok = sorted(testver.get(s['entry_id'], set()) | {s['strong']})
        for st in strongok:
            if st not in karoli_cache:
                karoli_cache[st] = karoli_alakok_strongra(st)
                bdb_cache[st] = bdb_hu_szoveg(st) if st.startswith('H') else ''
        karoli = sum((karoli_cache[st] for st in strongok), Counter())
        sz = szojegyzek_ellenorzes(s, angol, tabla)
        ka = karoli_ellenorzes(s, karoli)
        bd = bdb_ellenorzes(s, ' '.join(bdb_cache[st] for st in strongok))
        eltero = [n for n, (a, _) in (('szojegyzek', sz), ('karoli', ka), ('bdb', bd)) if a in ('utkozik', 'nem_talal')]
        ki.append(list(k) + [s['forditas_hu'], '%s: %s' % sz, '%s: %s' % ka, '%s: %s' % bd,
                             ('kezi_iteletre: ' + ','.join(eltero)) if eltero else 'egyezik'])
    with open(MANKO_KI, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forditas_hu', 'szojegyzek', 'karoli',
                           'bdb', 'osszegzes']) + '\n')
        for r in ki:
            f.write('\t'.join(c.replace('\t', ' ') for c in r) + '\n')
    szamlalo = Counter(r[-1].split(':')[0] for r in ki)
    print('mankó: %d sor; %s (%s)' % (len(ki), dict(szamlalo), MANKO_KI))
    return ki


def parancs_szojegyzek():
    """DT240: a gyorsítótárból kigyűjti azokat az angol glosszaelemeket, amelyek többféle magyar alakot kaptak."""
    tabla = egyenertek_tabla()
    verseng = [(en, c) for en, c in sorted(tabla.items()) if len(c) > 1]
    with open(SZOJEGYZEK_KI, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['angol_kulcs', 'magyar_alakok_gyakorisaggal', 'javasolt_sor']) + '\n')
        for en, c in verseng:
            f.write('\t'.join([en, '; '.join('%s×%d' % x for x in c.most_common()), c.most_common(1)[0][0]]) + '\n')
    print('szójegyzék-javaslat: %d versengő angol kulcs (%s)' % (len(verseng), SZOJEGYZEK_KI))
    return verseng


def parancs_visszamenoleges():
    """DT242: (a) a tiltott fordulatok mintái a teljes gyorsítótáron; (b) az új v4 `deity` -> `istenség` sor a régi sorokon
    (a forrásszöveg-feloldó az ellenoriz.py 13. szabályáé: egy feloldó). Csak javaslat, a táblát nem írja."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
    import ellenoriz as E
    import forditas_kapuk as K
    adat = os.path.join(GYOKER, 'adat')
    idx = E._forditasok_forras_szoveg_idx(adat)
    teljes_c, szak_c = {}, {}
    tiltott = K.tiltott_betolt()
    deity = re.compile(r'(?<![A-Za-z])deity(?![A-Za-z])')
    ki = []
    for s in tsv_sorok(FORDITASOK):
        if s['megjegyzes'].startswith(SZAMJEL):
            continue
        kulcs = (s['szotar'], s['strong'], s['entry_id'], s['jelentes_szam'], s['mezo'])
        for alak, minta, helyette, _v in tiltott:
            m = minta.search(s['forditas_hu'])
            if m:
                ki.append(list(kulcs) + ['DT241 tiltott', m.group(0), helyette, 'tiltott minta: ' + alak])
        forras = idx.get(kulcs)
        if forras is None:
            forras = E._teljes_szocikk(adat, s, teljes_c)
        if forras is None:
            forras = E._szakasz_szoveg(adat, s, szak_c)
        if forras and deity.search(forras) and 'istenség' not in s['forditas_hu'].lower():
            ki.append(list(kulcs) + ['DT238 deity -> istenség', s['forditas_hu'][:80],
                                     '(kézi ítélet: a „deity” itt más alakban áll)', 'a forrásban „deity” áll, a fordításban „istenség” nincs'])
    with open(VISSZA_KI, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'elv', 'mai_alak', 'javasolt_alak', 'indoklas']) + '\n')
        for r in ki:
            f.write('\t'.join(c.replace('\t', ' ').replace('\n', ' ') for c in r) + '\n')
    print('visszamenőleges felmérés: %d tétel (%s)' % (len(ki), VISSZA_KI))
    return ki


def main():
    a = sys.argv[1:]
    if a and a[0] == 'manko':
        return parancs_manko()
    if a and a[0] == 'szojegyzek':
        return parancs_szojegyzek()
    if a and a[0] == 'visszamenoleges':
        return parancs_visszamenoleges()
    if not a or a[0] != 'lista' or '--id' not in a:
        raise SystemExit('hasznalat: glossza_lexikon_forditas.py lista --id <ID> [--kimenet <konyvtar>] | manko | szojegyzek | visszamenoleges')
    kim = a[a.index('--kimenet') + 1] if '--kimenet' in a else None
    lista(a[a.index('--id') + 1], kim)


if __name__ == '__main__':
    main()
