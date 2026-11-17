#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — az emberi validáció kiértékelése (Károli 1908 – Strong szópárosítás).

Bemenet:
  * az online felület (Cloudflare Worker, DT-F175vp) admin-exportja (`--szerver-export`): a külső ellenőr és a
    második ítélő utolsó érvényes válaszai és a teljes append-only napló; a szerepeket az export adja, a
    próba-ellenőrök kimaradnak, az utolsó érvényes válaszokat a kiértékelő a naplóból újraszámolja; vagy
  * egy vagy két ellenőr exportja (`<ellenor>_valaszok.json`, az offline `ellenorzo.html` írja). Két külső ellenőrnél
    az eltérő tételeket harmadik döntés zárja le; ha a második ítélő a szerző (`--szerzo 1|2`: a hányadik fájl
    az övé), vagy általában ha a második ítélő nem független (`--kulso 1|2`: a hányadik fájl a külső ellenőré,
    `--masodik`: a második jelölése, alapértelmezés „hozzátartozó”), döntnök nincs: a fő szám a külső ellenőré,
    a második külön sorban áll. Kappa csak két ítélőnél, a közös tételeken: az alappárokon és azok könyvcsoportjain (`kozos` oszlop).
    A minta lehet a minimumváltozat is (kevesebb alapminta-pár, csali réteg: `reszminta` = csali, felismerési
    arány; a csali a becslésekbe nem számít);
  * a minta: a letétbeli minta.tsv és csalilista (`~/Bible-Study-letet/`; a repóbeli LEKOTES.md SHA-256-jával
    ellenőrizve; a JSON `minta_hash`-ének egyeznie kell);
  * opcionálisan a harmadik döntés (`--dontes`): az előző futás `eltero_tetelek.tsv`-je
    kitöltött `dontes` oszloppal (helyes | hibas | bizonytalan);
  * opcionálisan a modell-ellenőr ítéletei:
      --modell-f172      a párokra a #172 vak Opus-ellenőr meglévő ítélete (f172/itelet_par.tsv,
                         a minta `f172_id` oszlopán át; a 300 pár mind a #172 mintájából való);
      --modell-valasz D  a pár nélküli szavakra az új vak futás válaszai (D/koteg_NNN.json, a
                         #172 formájában; a szó ítélete `helyes`, ha a modell üres listát jelölt);
      --modell TSV       általános alak: `tetel_id<TAB>modell_itelet` (helyes | hibas) soronként.
    A modell-ellenőr bemenetét a `--modell-bemenet D` írja (a pár nélküli 80 szó, a #172
    utasításával és versblokk-formájával); a futtatás nem ennek a szkriptnek a dolga.

Kimenet (`--kimenet`, alapértelmezés: kozlemeny/data_paper/validacio/eredmeny/):
  * kiertekeles.md     — emberi pontosság Wilson 95%-kal az alapmintán (300 pár; pár nélküli szavak:
                          kimaradási arány), külön sorban a konzervatív becslés (bizonytalan = hibás);
                          kétfázisú, súlyozott becslés az alapminta + a #172 összes modell-eltérése
                          (túlminta) alapján (`ketfazisu`); ellenőrönként és a döntött mintán; Cohen-kappa
                          a két ítélő között; a modell és az ember egyezése az alapmintán és a #172
                          eltérésein (tévesztési mátrix);
  * eltero_tetelek.tsv — a két ember eltérő tételei a harmadik döntéshez (`dontes` oszlop üres);
  * karoli_szabad_forditas.tsv — a „Károli itt szabadon vagy pontatlanul fordít” jelölővel ellátott tételek
                          (fordítói észrevétel, nem a párosítás hibája; a pontosságba nem számít).

Az ítélet jelentése mindkét típusnál: helyes-e a gép döntése (pár: a pár helyes; pár nélküli szó:
valóban nincs eredetije). A `bizonytalan` a pontosság nevezőjéből kimarad, külön számoljuk, és a
konzervatív alsó becslés hibásnak veszi.

Olvasás split('\\t'), írás '\\t'.join() (a csv modul tilos, CLAUDE.md).

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_kiertekel.py A_valaszok.json B_valaszok.json
    python eszkozok/karoli_strong_validacio_kiertekel.py A.json B.json --dontes eltero_tetelek.tsv --modell-f172
    python eszkozok/karoli_strong_validacio_kiertekel.py --modell-bemenet <könyvtár>
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
VALIDACIO = os.path.join(GYOKER, 'kozlemeny', 'data_paper', 'validacio')
LETET_DIR = os.path.join(os.path.expanduser('~'), 'Bible-Study-letet')   # a repón kívüli letét (DT-F175vh)
MINTA = os.path.join(LETET_DIR, 'minta.tsv')
LEKOTES = os.path.join(VALIDACIO, 'LEKOTES.md')
CSALI_KUSZOB = 0.8   # ha egy ítélő a csalik 80%-ánál (20-ból 16-nál) kevesebbet ismer fel, a számai csak fenntartással
F172_ITELET = os.path.join(GYOKER, 'f172', 'itelet_par.tsv')
Z95 = 1.959963984540054
ITELETEK = ('helyes', 'hibas', 'bizonytalan')
ELTERO_FEJ = ['tetel_id', 'tipus', 'vers', 'hu_szo', 'er_szo', 'strong',
              'A_itelet', 'A_hibatipus', 'A_helyes_forras', 'A_megjegyzes',
              'B_itelet', 'B_hibatipus', 'B_helyes_forras', 'B_megjegyzes', 'dontes', 'dontes_indok']


# ---------------------------------------------------------------- beolvasás

def tabla(ut):
    fej, sorok = None, []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
            else:
                sorok.append(dict(zip(fej, m)))
    return fej, sorok


def minta_hash(sorok):
    """Az ellenorzo.html MINTA_HASH-e (32 bites FNV-1a az UTF-16 kódegységeken, hexában)."""
    s = ';'.join('%s|%s|%s|%s' % (r['tetel_id'], r['vers'], int(r['hu_sorszam']),
                                  int(r['er_sorszam']) if r['er_sorszam'] else 0) for r in sorok)
    h = 0x811c9dc5
    b = s.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 0x01000193) & 0xffffffff
    return '%x' % h


def valaszok_olvas(ut, minta, hash_):
    with open(ut, encoding='utf-8') as f:
        d = json.load(f)
    return valaszok_ellenoriz(d, ut, minta, hash_)


SZERVER_FORMATUM = 'F175V-szerver-export/1'


def naplobol_utolso(naplo):
    """Az append-only naplóból ellenőrönként és tételenként az utolsó érvényes válasz, a Worker `utolso`
    nézetének szabálya szerint (a kliens ideje, majd a napló sorszáma szerint a legkésőbbi)."""
    ki_ = {}
    for r in naplo:
        if r.get('esemeny') != 'valasz':
            continue
        k = (r['ellenor'], r['tetel'])
        kulcs = (r.get('kliens_ido') or '', r['n'])
        if k not in ki_ or kulcs > ki_[k][0]:
            ki_[k] = (kulcs, r['valasz'])
    return {k: v for k, (_, v) in ki_.items()}


def szerver_export_olvas(ut, minta, hash_):
    """Az online felület (Worker) admin-exportja (DT-F175vp) -> [(név, válaszok, jelöltek)], a külső ellenőr elöl,
    utána (ha van) a második ítélő; a próba-ellenőrök (`szerep` = proba) kimaradnak. Az ellenőrönkénti
    „utolsó érvényes” válaszokat a teljes naplóból újraszámolja, és eltérésnél megáll."""
    with open(ut, encoding='utf-8') as f:
        d = json.load(f)
    if d.get('formatum') != SZERVER_FORMATUM:
        raise SystemExit('%s: nem a Worker exportja (formatum: %r, várt: %s)' % (ut, d.get('formatum'), SZERVER_FORMATUM))
    utolso = naplobol_utolso(d.get('naplo') or [])
    ell = [e for e in d.get('ellenorok') or [] if e.get('szerep') != 'proba']
    for e in ell:
        sajat = {t: v for (en, t), v in utolso.items() if en == e['ellenor']}
        if sajat != (e.get('valaszok') or {}):
            raise SystemExit('%s: a(z) %s ellenőr válaszai nem egyeznek a naplóból számolttal' % (ut, e['ellenor']))
    kulso = [e for e in ell if e.get('szerep') == 'kulso']
    masodik = [e for e in ell if e.get('szerep') == 'masodik']
    if len(kulso) != 1 or len(masodik) > 1 or len(ell) != len(kulso) + len(masodik):
        raise SystemExit('%s: pontosan egy külső ellenőr és legfeljebb egy második ítélő kell (van: %s)'
                         % (ut, ', '.join('%s=%s' % (e['ellenor'], e.get('szerep')) for e in ell)))
    return [valaszok_ellenoriz(e, '%s#%s' % (ut, e['ellenor']), minta, hash_) for e in kulso + masodik]


def valaszok_ellenoriz(d, ut, minta, hash_):
    """Egy ellenőr válaszai (az oldal exportja, vagy a Worker-export egy ellenőre) -> (név, ítéletek, jelöltek)."""
    # a teljes oldal (külső ellenőr) vagy a második ítélő oldala (az alapminta-párok és a csalijai)
    elfogadott = {hash_, minta_hash([r for r in minta if r.get('kozos') == '1'])}   # a második ítélő oldala: alappárok + csalijai
    if d.get('minta_hash') not in elfogadott:
        raise SystemExit('%s: a minta_hash (%s) nem ezé a mintáé (%s)' % (ut, d.get('minta_hash'), hash_))
    ids = {r['tetel_id'] for r in minta}
    ki, karoli = {}, {}
    for k, v in (d.get('valaszok') or {}).items():
        if k not in ids:
            raise SystemExit('%s: ismeretlen tétel: %s' % (ut, k))
        it = v.get('itelet', '')
        if it and it not in ITELETEK:
            raise SystemExit('%s: ismeretlen ítélet %r (%s)' % (ut, it, k))
        if it:
            ki[k] = v
        if v.get('karoli') or (v.get('segedeszkoz') or '').strip():
            karoli[k] = v
    return d.get('ellenor') or os.path.basename(ut), ki, karoli


KAROLI_FEJ = ['tetel_id', 'tipus', 'vers', 'hu_szo', 'er_szo', 'strong', 'A_jelolte', 'A_itelet', 'A_megjegyzes',
              'B_jelolte', 'B_itelet', 'B_megjegyzes']


def karoli_szabad(minta, ellenorok):
    """A „Károli itt szabadon vagy pontatlanul fordít” jelölő: nem a párosítás hibája, külön lista és számolás.
    ellenorok: [(címke, válaszok, jelöltek), ...] (egy vagy két ellenőr; a TSV B-oszlopai egy ellenőrnél üresek)."""
    tip = {r['tetel_id']: r['tipus'] for r in minta}
    ellenorok = [(nev, v, {t: x for t, x in k.items() if x.get('karoli')}) for nev, v, k in ellenorok]
    sor = ['## 6. Fordítói észrevétel: „Károli itt szabadon vagy pontatlanul fordít”\n',
           'Ez a jelölő nem a párosítás ítélete, a pontosságba nem számít; a tételek a `karoli_szabad_forditas.tsv`-ben.\n',
           '| | jelölt tétel | ebből pár | ebből pár nélküli | ugyanott az ítélet „helyes” |', '|---|---|---|---|---|']
    for nev, v, k in ellenorok:
        sor.append('| %s | %d | %d | %d | %d |' % (nev, len(k), sum(tip[t] == 'par' for t in k),
                                                  sum(tip[t] == 'parnelkuli' for t in k),
                                                  sum(1 for t in k if v.get(t, {}).get('itelet') == 'helyes')))
    ures = ('', {}, {})
    (_, a, ka), (_, b, kb) = (ellenorok + [ures])[:2]
    if len(ellenorok) == 2:
        sor.append('\nMindkét ítélő jelölte: %d tétel; csak az egyik: %d.\n' % (len(set(ka) & set(kb)), len(set(ka) ^ set(kb))))
    by = {r['tetel_id']: r for r in minta}
    sorok = []
    for t in sorted(set(ka) | set(kb)):
        r = by[t]
        sorok.append([t, r['tipus'], r['vers'], r['hu_szo'], r['er_szo'], r['strong'],
                      '1' if t in ka else '0', a.get(t, {}).get('itelet', ''), _egysor((ka.get(t) or {}).get('karoli_megj', '')),
                      ('1' if t in kb else '0') if len(ellenorok) == 2 else '', b.get(t, {}).get('itelet', ''),
                      _egysor((kb.get(t) or {}).get('karoli_megj', ''))])
    return '\n'.join(sor), sorok


def gepi_olvas(ut, sha_vart, minta):
    """A külső gépi bírálók fagyasztott táblája (SHA-256-tal ellenőrizve) -> ({tetel_id: helyesnek ítélő bírálók
    száma}, bírálók száma). A tábla a párt (vers, hu_sorszam, er_sorszam) azonosítja; a bírálók száma a `helyes_db`
    oszlop, vagy a `biralo_*` oszlopok 1-eseinek összege."""
    import hashlib
    with open(ut, 'rb') as f:
        h = hashlib.sha256(f.read()).hexdigest()
    if h != sha_vart:
        raise SystemExit('a gépi tábla SHA-256-ja (%s) nem egyezik a fagyasztottal (%s)' % (h, sha_vart))
    fej, sorok = tabla(ut)
    biralok = [k for k in fej if k.startswith('biralo')] or [k for k in fej if k.endswith('_helyes') and k != 'tobbseg_helyes']
    n_biralo = len(biralok) or 3
    kulcs = {(r['vers'], r['hu_sorszam'], r['er_sorszam']): r['tetel_id'] for r in minta if r['tipus'] == 'par'}
    ki = {}
    for r in sorok:
        t = kulcs.get((r['vers'], r['hu_sorszam'], r['er_sorszam']))
        if t is None:
            continue
        if 'helyes_db' in r and r['helyes_db'] != '':
            ki[t] = int(r['helyes_db'])
        else:
            ki[t] = sum(1 for b in biralok if r.get(b) == '1')
    return ki, n_biralo


def tajekoztato(minta, kulso_nev, kulso_it, kulso_v, gepi, csali):
    """A külső ellenőrre vonatkozó tájékoztató szakaszok: ember–gép eltérések, érzékenységi forgatókönyvek és a
    „hibás” ítéletek együttjárása. A fő számot egyik sem módosítja."""
    tip = {r['tetel_id']: r['tipus'] for r in minta}
    resz = {r['tetel_id']: r['reszminta'] for r in minta}
    sor = []
    if gepi:
        g, nb = gepi
        sor.append('## 8. Ember–gép eltérések (tájékoztató; a fő számot nem módosítja)\n')
        sor.append('A külső ellenőr (%s) ítélete × a párt helyesnek ítélő gépi bírálók száma (0–%d; a fagyasztott gépi tábla). '
                   'A tételeket mindkét emberi ítélettel közöljük; a becslést nem igazítjuk.\n' % (kulso_nev, nb))
        for cimke, rsz in (('alapminta', 'alap'), ('túlminta', 'tulminta')):
            ts = [t for t in g if resz.get(t) == rsz and t in kulso_it]
            sor.append('%s (%d pár):\n' % (cimke.capitalize(), len(ts)))
            sor.append('| emberi ítélet | ' + ' | '.join('gép %d/%d' % (k, nb) for k in range(nb + 1)) + ' | összesen |')
            sor.append('|---|' + '---|' * (nb + 2))
            for it in ITELETEK:
                sz = [sum(1 for t in ts if kulso_it[t] == it and g[t] == k) for k in range(nb + 1)]
                sor.append('| %s | %s | %d |' % (it, ' | '.join(map(str, sz)), sum(sz)))
            sor.append('')
        ts = [t for t in g if resz.get(t) == 'alap' and t in kulso_it]
        k_ = sum(1 for t in ts if kulso_it[t] == 'hibas')
        j_ = sum(1 for t in ts if kulso_it[t] == 'hibas' and g[t] == nb)
        i_ = sum(1 for t in ts if kulso_it[t] == 'helyes' and g[t] == 0)
        sor.append('A külső ellenőr %d párt ítélt hibásnak (alapminta); ezek közül %d-t mind a(z) %d modell-bíráló '
                   'helyesnek ítélte. A fordított eset %d pár. A tételeket mindkét emberi ítélettel közöljük; a becslést '
                   'nem igazítjuk.\n' % (k_, j_, nb, i_))

    sor.append('## 9. Érzékenységi forgatókönyvek (tájékoztató; nem becslés)\n')
    h = [kulso_it[t] for t in kulso_it if tip[t] == 'par' and resz.get(t) == 'alap']
    hl, hb, bz = h.count('helyes'), h.count('hibas'), h.count('bizonytalan')
    m_csali = None
    cs = [kulso_it[t] for t in kulso_it if t in csali]
    if cs and cs.count('hibas') + cs.count('helyes'):
        m_csali = cs.count('helyes') / (cs.count('hibas') + cs.count('helyes'))
    sor.append('Képlet (előre rögzítve, a protokoll 1.3 pontja): π = (p − m) / (1 − f − m), ahol p a külső ellenőr (%s) 2a-pontossága, '
               'f a téves riasztás (helyes párt hibásnak ítél), m az elnézés (hibás párt helyesnek ítél); f ∈ {0, 2, 5}%%, '
               'm ∈ {0, 20}%%. A csalikból mért elnézés%s csak durva hibán mér, ezért nem helyettesíti az m-et.\n'
               % (kulso_nev, ' (%.1f%%)' % (100 * m_csali) if m_csali is not None else ''))
    sor.append('| p | f | m | π |\n|---|---|---|---|')
    for cimke, p_ in (('2a', hl / (hl + hb) if hl + hb else float('nan')),
                      ('2a konzervatív', hl / (hl + hb + bz) if hl + hb + bz else float('nan'))):
        for f_ in (0.0, 0.02, 0.05):
            for m_ in (0.0, 0.20):
                pi = (p_ - m_) / (1 - f_ - m_) if (1 - f_ - m_) > 0 else float('nan')
                ertek = ('nem értelmezhető (π > 100%: a forgatókönyv nem fér össze a mért p-vel)' if pi == pi and pi > 1
                         else szazalek(max(0.0, pi) if pi == pi else pi))
                sor.append('| %s = %s | %s | %s | %s |' % (cimke, szazalek(p_), szazalek(f_), szazalek(m_), ertek))
    sor.append('')

    sor.append('## 10. A „hibás” ítéletek együttjárása (tájékoztató)\n')
    sor.append('A külső ellenőr (%s) pár-ítéletei (alapminta és túlminta): a „Károli itt szabadon vagy pontatlanul fordít” jelölő és a '
               'hibatípus szerint. A téves riasztásra ez nem mérőeszköz, csak jelző.\n' % kulso_nev)
    ts = [t for t in kulso_it if tip[t] == 'par' and resz.get(t) in ('alap', 'tulminta')]
    sor.append('| ítélet | n | ebből „Károli szabadon fordít” jelölővel |\n|---|---|---|')
    for it in ITELETEK:
        tt = [t for t in ts if kulso_it[t] == it]
        sor.append('| %s | %d | %d |' % (it, len(tt), sum(1 for t in tt if (kulso_v.get(t) or {}).get('karoli'))))
    sor.append('')
    tipusok = _szamlal((kulso_v[t].get('hibatipus') or '(nincs megadva)') for t in ts if kulso_it[t] == 'hibas')
    sor.append('| hibatípus | n | ebből jelölővel |\n|---|---|---|')
    for ht, n in sorted(tipusok.items(), key=lambda x: -x[1]):
        jel = sum(1 for t in ts if kulso_it[t] == 'hibas' and (kulso_v[t].get('hibatipus') or '(nincs megadva)') == ht
                  and kulso_v[t].get('karoli'))
        sor.append('| %s | %d | %d |' % (ht, n, jel))
    sor.append('')
    return '\n'.join(sor)


TILALMAK = ('Tilos (a kiértékelési protokoll 3.3 pontja): az elsődleges mutató cseréje; tétel utólagos kizárása; új '
            'ellenőr ugyanarra a mintára; konvenció utólagos módosítása újrapontozással; „a 95% inkább alsó becslés”; '
            'a megerősített érték fő számként. Az ember–gép tábla sem a fő számot, sem a sávot nem módosítja; az eltérő '
            'tételekről nincs visszajelzés és második kör.')


def ket_emberes(a_it, b_it, tetelek):
    """Kétemberes sáv a közösen ítélt tételeken: (szigorú, megerősített) ítéletlisták.
    Szigorú: hibás, ha bármelyik hibásnak mondta; helyes, ha mindkettő helyesnek; különben bizonytalan.
    Megerősített: hibás, ha mindkettő hibásnak mondta; bizonytalan, ha mindkettő bizonytalan; különben helyes."""
    szig, meg = [], []
    for t in tetelek:
        if t not in a_it or t not in b_it:
            continue
        x, y = a_it[t], b_it[t]
        szig.append('hibas' if 'hibas' in (x, y) else ('helyes' if x == y == 'helyes' else 'bizonytalan'))
        meg.append('hibas' if x == y == 'hibas' else ('bizonytalan' if x == y == 'bizonytalan' else 'helyes'))
    return szig, meg


def dontesi_sav(p):
    """A protokoll 3. pontjának döntési sávja a 2a-pontosságra."""
    if p != p:
        return '–'
    if p >= 0.93:
        return '≥ 93%: közlés decemberben'
    if p >= 0.90:
        return ('90–93%: közlés decemberben; kötelező hibatípus-bontás; címben és kivonatban nincs „95%”; a gépi '
                'mérés „felülbecsül”')
    return ('< 90%: hibaelemzés; ha a hibák legalább harmada egy lekérdezhető osztály: javítás, új mérés, beküldés '
            'januárban; különben beküldés a mért számmal, „validated” nélkül')


JAVITAS_FEJ = ['tetel_id', 'tipus', 'reszminta', 'vers', 'hu_szo', 'er_szo', 'strong', 'kulso_itelet', 'kulso_hibatipus',
               'kulso_helyes_forras', 'masodik_itelet', 'masodik_hibatipus', 'masodik_helyes_forras', 'eredet']


def javitas_listak(minta, kulso, masodik):
    """A protokoll 4.1–4.2 pontja: javítható, ahol a külső ellenőr megjelölte a helyes forrásszót, vagy mindkét ember
    „hibás”; a többi eltérő vagy bizonytalan tétel vitatott (változtatás nélkül). Az eredetjelző a javítás okát mondja.
    A csali nem kerül a listákba. Visszaad: (javítható sorok, vitatott sorok)."""
    jav, vit = [], []
    for r in minta:
        t = r['tetel_id']
        if r['reszminta'] == 'csali':
            continue
        a = kulso.get(t) or {}
        b = masodik.get(t) or {}
        ia, ib = a.get('itelet', ''), b.get('itelet', '')
        if not (ia in ('hibas', 'bizonytalan') or ib in ('hibas', 'bizonytalan')):
            continue
        eredet = ''
        if ia == 'hibas' and a.get('helyes_forras'):
            eredet = 'kulso_jelolte'
        elif ia == 'hibas' and ib == 'hibas':
            eredet = 'ket_ember_hibas'
        sor = [t, r['tipus'], r['reszminta'], r['vers'], r['hu_szo'], r['er_szo'], r['strong'],
               ia, a.get('hibatipus', ''), ','.join(map(str, a.get('helyes_forras') or [])),
               ib, b.get('hibatipus', ''), ','.join(map(str, b.get('helyes_forras') or [])), eredet or 'vitatott']
        (jav if eredet else vit).append(sor)
    return jav, vit


SEGED_FEJ = ['tetel_id', 'tipus', 'vers', 'ellenor', 'segedeszkoz', 'itelet']


def segedeszkoz(minta, ellenorok):
    """A „Használtam segédeszközt” mező: ítélőnként a kitöltött tételek (lista és darabszám)."""
    by = {r['tetel_id']: r for r in minta}
    sor = ['## 7. Segédeszköz („Használtam segédeszközt”)\n',
           '| | kitöltött tétel | leggyakoribb megnevezés |', '|---|---|---|']
    sorok = []
    for nev, v, k in ellenorok:
        tk = {t: (x.get('segedeszkoz') or '').strip() for t, x in k.items() if (x.get('segedeszkoz') or '').strip()}
        gyak = sorted(_szamlal(tk.values()).items(), key=lambda x: -x[1])[:3]
        sor.append('| %s | %d | %s |' % (nev, len(tk), ', '.join('%s (%d)' % g for g in gyak) or '–'))
        for t in sorted(tk):
            r = by[t]
            sorok.append([t, r['tipus'], r['vers'], nev, _egysor(tk[t]), v.get(t, {}).get('itelet', '')])
    return '\n'.join(sor), sorok


# ---------------------------------------------------------------- statisztika

def wilson(x, n, z=Z95):
    if n == 0:
        return (float('nan'), float('nan'), float('nan'))
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def kappa(parok, kategoriak):
    """Cohen-kappa a (a, b) címkepárokon; (kappa, megfigyelt egyezés, n)."""
    n = len(parok)
    if n == 0:
        return (float('nan'), float('nan'), 0)
    po = sum(a == b for a, b in parok) / n
    pe = sum((sum(a == k for a, _ in parok) / n) * (sum(b == k for _, b in parok) / n) for k in kategoriak)
    k = float('nan') if pe == 1 else (po - pe) / (1 - pe)
    return (k, po, n)


def szazalek(x):
    return '–' if x != x else '%.2f%%' % (100 * x)


def szam(x):
    return '–' if x != x else '%.3f' % x


# ---------------------------------------------------------------- kiértékelés

def pontossag_sor(cimke, itelet_lista, konzervativ=False):
    """itelet_lista: ['helyes'|'hibas'|'bizonytalan', ...] -> táblasor. konzervativ: a bizonytalan hibásnak számít."""
    h = itelet_lista.count('helyes')
    b = itelet_lista.count('hibas')
    u = itelet_lista.count('bizonytalan')
    p, lo, hi = wilson(h, h + b + u) if konzervativ else wilson(h, h + b)
    return '| %s | %d | %d | %d | %d | %s | %s–%s |' % (
        cimke, h + b + u, h, b, u, szazalek(p), szazalek(lo), szazalek(hi))


FEJ_P = ('| | n | helyes | hibás | bizonytalan | pontosság | Wilson 95% |\n'
         '|---|---|---|---|---|---|---|')


def kimaradas_sor(cimke, itelet_lista, konzervativ=False):
    h = itelet_lista.count('helyes')
    b = itelet_lista.count('hibas')
    u = itelet_lista.count('bizonytalan')
    p, lo, hi = wilson(b + u, h + b + u) if konzervativ else wilson(b, h + b)
    return '| %s | %d | %d | %d | %d | %s | %s–%s |' % (
        cimke, h + b + u, h, b, u, szazalek(p), szazalek(lo), szazalek(hi))


def dontott(minta, a, b, dontes):
    """A döntött minta (két külső ellenőr): egyező ítéletnél a közös, eltérőnél a harmadik döntés (ha van)."""
    ki, hianyzo = {}, []
    for r in minta:
        t = r['tetel_id']
        if t not in a or t not in b:
            continue
        ia, ib = a[t]['itelet'], b[t]['itelet']
        if ia == ib:
            ki[t] = ia
        elif dontes.get(t):
            ki[t] = dontes[t]
        else:
            hianyzo.append(t)
    return ki, hianyzo


# ---------------------------------------------------------------- kétfázisú, súlyozott becslés

def f172_fazis1():
    """A #172 mintája mint első fázis: rétegenként n' (a mintapárok száma), d (a modell-ellenőr eltérései)
    és W (a keret pársúlya)."""
    _, itel = tabla(F172_ITELET)
    n1, d = {}, {}
    for r in itel:
        n1[r['reteg']] = n1.get(r['reteg'], 0) + 1
        if r['helyes'] == '0':
            d[r['reteg']] = d.get(r['reteg'], 0) + 1
    _, keret = tabla(os.path.join(GYOKER, 'f172', 'keret.tsv'))
    db = {r['reteg']: int(r['parsor']) for r in keret if r['reteg'] in n1}
    w = {h: x / sum(db.values()) for h, x in db.items()}   # a keret pársúlya (a kerekített `suly` helyett)
    return n1, d, w


def ketfazisu(minta, itelet, konzervativ=False, fazis1=None):
    """Kétfázisú (rétegzésre szolgáló kettős mintavétel) becslés a párok pontosságára.

    1. fázis: a #172 rétegzett mintája (rétegenként n'), két csoportra bontva: „eltérő” az a pár, amelyet bármelyik vak
    gépi bíráló (Opus, Gemini, GPT) hibásnak jelölt (`elteres` = 1; 87 pár, mind a mintában: alapminta vagy túlminta);
    „egyező” a többi. 2. fázis: az egyező párokból
    az alapminta (véletlen részminta), az eltérő párokból mind. d_h (az eltérők száma rétegenként) a mintából
    számolódik, mert az unió minden eleme pontosan egyszer szerepel benne. Rétegenként p_h = (1 − d/n')·p_egyezo + (d/n')·p_eltero, összesen Σ W_h·p_h, ahol W_h a keret
    pársúlya. Variancia (Cochran 12.: kettős mintavétel rétegzéshez), rétegenként:
    V_h = p_h(1−p_h)/n' + Σ_g w_g·S²_g·(1/ν_g − 1)/n', ν_g = n_g/(n'·w_g); az összes: Σ W_h²·V_h.
    Visszaad: (becslés, alsó95, felső95, megjegyzés) vagy None-t, ha egy réteg nem becsülhető."""
    n1, _d172, w = fazis1 or f172_fazis1()
    d = {}
    for r in minta:
        if r['tipus'] == 'par' and r['reszminta'] in ('alap', 'tulminta') and r['elteres'] == '1':
            d[r['f172_reteg']] = d.get(r['f172_reteg'], 0) + 1
    ert = {}
    for r in minta:
        if r['tipus'] != 'par':
            continue
        it = itelet.get(r['tetel_id'])
        if it == 'helyes':
            y = 1.0
        elif it == 'hibas' or (it == 'bizonytalan' and konzervativ):
            y = 0.0
        else:
            continue
        if r['reszminta'] == 'csali' or r['reszminta'] == 'nehez':
            continue
        csop = 'eltero' if r['elteres'] == '1' else ('egyezo' if r['reszminta'] == 'alap' else None)
        if csop:
            ert.setdefault(r['f172_reteg'], {}).setdefault(csop, []).append(y)
    osszeg, var, hiany = 0.0, 0.0, []
    for h, nn in n1.items():
        wd = d.get(h, 0) / nn
        reszek = (('egyezo', 1 - wd), ('eltero', wd))
        ph, vh_resz = 0.0, 0.0
        for g, wg in reszek:
            if wg == 0:
                continue
            ys = ert.get(h, {}).get(g, [])
            if not ys:
                hiany.append('%s/%s' % (h, g))
                continue
            pg = sum(ys) / len(ys)
            ph += wg * pg
            nu = min(1.0, len(ys) / (nn * wg))
            vh_resz += wg * pg * (1 - pg) * (1 / nu - 1) / nn
        vh = ph * (1 - ph) / nn + vh_resz
        osszeg += w[h] * ph
        var += w[h] ** 2 * vh
    if hiany:
        return None, 'nem becsülhető (ítélet nélküli réteg: %s)' % ', '.join(hiany)
    se = math.sqrt(var)
    return (osszeg, max(0.0, osszeg - Z95 * se), min(1.0, osszeg + Z95 * se)), ''


def ketfazisu_sor(cimke, minta, itelet, konzervativ, fazis1):
    e, megj = ketfazisu(minta, itelet, konzervativ, fazis1)
    if e is None:
        return '| %s | – | – | %s |' % (cimke, megj)
    return '| %s | %s | %s–%s | |' % (cimke, szazalek(e[0]), szazalek(e[1]), szazalek(e[2]))


# ---------------------------------------------------------------- modell–ember

def modell_osszevet(minta, emberi, modell, szuro):
    """Modell vs. emberi ítélet a szűrt tételeken (a bizonytalan emberi ítélet kimarad)."""
    parok = []
    for r in minta:
        t = r['tetel_id']
        if not szuro(r) or t not in modell or emberi.get(t) not in ('helyes', 'hibas'):
            continue
        parok.append((modell[t], emberi[t]))
    k, po, n = kappa(parok, ('helyes', 'hibas'))
    m = {(x, y): sum(1 for p in parok if p == (x, y)) for x in ('helyes', 'hibas') for y in ('helyes', 'hibas')}
    return k, po, n, m


def modell_f172(minta):
    _, sorok = tabla(F172_ITELET)
    by = {r['minta_id']: r for r in sorok}
    ki = {}
    for r in minta:
        if r['tipus'] == 'par' and r['f172_id'] in by:
            ki[r['tetel_id']] = 'helyes' if by[r['f172_id']]['helyes'] == '1' else 'hibas'
    return ki


def modell_valasz(minta, konyvtar):
    """A pár nélküli szavak vak modell-ítélete a koteg_*.json válaszokból (a #172 formája)."""
    cel = {}
    for r in minta:
        if r['tipus'] == 'parnelkuli':
            cel[(r['vers'], int(r['hu_sorszam']))] = r['tetel_id']
    ki = {}
    for fn in sorted(os.listdir(konyvtar)):
        if not (fn.startswith('koteg_') and fn.endswith('.json')):
            continue
        with open(os.path.join(konyvtar, fn), encoding='utf-8') as f:
            d = json.load(f)
        for v in d.get('versek', []):
            for hu, er in v.get('jeloles', []):
                t = cel.get((v.get('vers'), hu))
                if t:
                    ki[t] = 'helyes' if not er else 'hibas'
    return ki


def modell_tsv(ut):
    _, sorok = tabla(ut)
    ki = {}
    for r in sorok:
        if r.get('modell_itelet') not in ('helyes', 'hibas'):
            raise SystemExit('%s: ismeretlen modell_itelet %r (%s)' % (ut, r.get('modell_itelet'), r.get('tetel_id')))
        ki[r['tetel_id']] = r['modell_itelet']
    return ki


def kiertekel(minta, ellenorok, dontes, modell, szerzoi=False):
    """A jelentés szövege és az eltérő tételek sorai.

    ellenorok: [(címke, válaszok), ...], egy vagy két elem. Két külső ellenőrnél a döntött minta (egyező ítélet,
    eltérésnél harmadik döntés) is ítélő; szerzői ellenőrnél (szerzoi=True) döntnök nincs, a két ítélet külön áll."""
    tip = {r['tetel_id']: r['tipus'] for r in minta}
    csop = {r['tetel_id']: r['csoport'] for r in minta}
    alap = {r['tetel_id'] for r in minta if r['reszminta'] == 'alap'}
    elter = {r['tetel_id'] for r in minta if r['elteres'] == '1'}
    tul = {r['tetel_id'] for r in minta if r['reszminta'] == 'tulminta'}
    opus72 = {r['tetel_id'] for r in minta if r.get('opus_elteres') == '1'}
    nehez = {r['tetel_id'] for r in minta if r['reszminta'] == 'nehez'}
    kozos_blokk = {r['tetel_id'] for r in minta if r.get('kozos') == '1'}
    csali = {r['tetel_id'] for r in minta if r['reszminta'] == 'csali'}
    ket = len(ellenorok) == 2
    sor = ['> ' + TILALMAK + '\n', '## 1. Kitöltöttség és felállás\n']
    if not ket:
        sor.append('Egy ellenőr: kappa és harmadik döntés nincs.\n')
    elif szerzoi:
        sor.append('Egy külső ellenőr és egy nem független második ítélő (%s): a fő szám a külső ellenőré; a második '
                   'ítélő külön sorban áll; döntnök nincs, a vitás tételeknél a két ítélet külön szerepel; a kappa a '
                   'kettejük közös tételein (az alappárokon, könyvcsoportonként is).\n' % ellenorok[1][0])
    else:
        sor.append('Két külső ellenőr; az eltérő tételeket harmadik döntés zárja le (a döntött minta).\n')
    for nev, v in ellenorok:
        sor.append('- %s: %d / %d tétel (alapminta-pár %d, túlminta-pár %d, nehéz pár %d, pár nélküli %d, '
                   'kimaradt-pár %d, csali %d)' % (
            nev, len(v), len(minta), sum(tip[t] == 'par' and t in alap for t in v),
            sum(t in tul for t in v), sum(t in nehez for t in v),
            sum(tip[t] == 'parnelkuli' for t in v), sum(tip[t] == 'kimaradt' for t in v), sum(t in csali for t in v)))
    sor.append('')

    itelok = [(nev, {t: x['itelet'] for t, x in v.items()}) for nev, v in ellenorok]
    dont, hianyzo = {}, []
    if ket and not szerzoi:
        dont, hianyzo = dontott(minta, ellenorok[0][1], ellenorok[1][1], dontes)
        itelok.append(('**döntött minta**', dont))
    fo_nev, fo = itelok[-1] if (ket and not szerzoi) else itelok[0]

    sor.append('## 2. Párok: emberi pontosság\n')
    sor.append('**Elsődleges szám:** a 2a alapminta-pontosság (%s), mellette mindig a konzervatív sor. A többi becslés '
               'kiegészítő.\n' % fo_nev)
    sor.append('### 2a. Alapminta (%d pár, a keret arányos rétegzett mintája)\n' % len([t for t in alap if tip[t] == 'par']))
    sor.append('A „konzervatív” sor a bizonytalant hibásnak számolja.\n')
    sor.append(FEJ_P)
    for nev, it in itelok:
        lista = [it[t] for t in it if tip[t] == 'par' and t in alap]
        sor.append(pontossag_sor(nev, lista))
        sor.append(pontossag_sor(nev + ' · konzervatív', lista, konzervativ=True))
    sor.append('')
    fo_lista = [fo[t] for t in fo if tip[t] == 'par' and t in alap]
    fo_p = fo_lista.count('helyes') / (fo_lista.count('helyes') + fo_lista.count('hibas')) if (
        fo_lista.count('helyes') + fo_lista.count('hibas')) else float('nan')
    sor.append('**Döntési sáv** (a protokoll 3. pontja; %s, 2a = %s): %s\n' % (fo_nev, szazalek(fo_p), dontesi_sav(fo_p)))
    if ket:
        (na_, va_), (nb_, vb_) = ellenorok
        szig, meg = ket_emberes({t: x['itelet'] for t, x in va_.items()}, {t: x['itelet'] for t, x in vb_.items()},
                                [t for t in alap if tip[t] == 'par'])
        sor.append('### 2a+. Kétemberes sáv a közösen ítélt alappárokon (tájékoztató; a megerősített érték nem fő szám)\n')
        sor.append('Szigorú: hibás, ha bármelyik ítélő hibásnak mondta; megerősített: hibás, ha mindkettő. A közös '
                   'félreértést egyik sem szűri; a második ítélő nem független.\n')
        sor.append(FEJ_P)
        sor.append(pontossag_sor('szigorú', szig))
        sor.append(pontossag_sor('szigorú · konzervatív', szig, konzervativ=True))
        sor.append(pontossag_sor('megerősített', meg))
        sor.append(pontossag_sor('megerősített · konzervatív', meg, konzervativ=True))
        sor.append('')
    sor.append('### 2b. Kétfázisú, súlyozott becslés (alapminta + a túlminta-réteg: bármelyik gépi bíráló hibásnak jelölte)\n')
    sor.append('Első fázis: a #172 rétegzett mintája; „eltérő” az a pár, amelyet bármelyik vak gépi bíráló (Opus, Gemini, '
               'GPT) hibásnak jelölt; második fázis: az egyező párokból az alapminta, az eltérő párokból mind. A túlminta '
               'így nem torzítja a becslést (Cochran, kettős mintavétel rétegzéshez; normál 95%).\n')
    sor.append('| | becslés | 95% | megjegyzés |\n|---|---|---|---|')
    f1 = f172_fazis1()
    for nev, it in itelok:
        sor.append(ketfazisu_sor(nev, minta, it, False, f1))
        sor.append(ketfazisu_sor(nev + ' · konzervatív', minta, it, True, f1))
    sor.append('')
    sor.append('### 2c. Nehéz réteg: az 1–2Móz párjai, ahol a két párosító modell nem egyezett (%d pár)\n' % len(nehez))
    sor.append('Egyszerű véletlen minta ebből a keretből (bizonyosság ≠ magas); külön becslés, az összesítőbe nem számít.\n')
    if nehez:
        sor.append(FEJ_P)
        for nev, it in itelok:
            lista = [it[t] for t in it if t in nehez]
            sor.append(pontossag_sor(nev, lista))
            sor.append(pontossag_sor(nev + ' · konzervatív', lista, konzervativ=True))
    else:
        sor.append('Ebben a mintában nincs nehéz réteg.\n')
    sor.append('')
    if csali:
        sor.append('### 2d. Csalik (elültetett hibás párok): felismerési arány (%d tétel)\n' % len(csali))
        sor.append('A csali a becslésekbe nem számít; a „hibás” ítélet a felismerés. A „konzervatív” sor a bizonytalant '
                   'nem felismertnek veszi.\n')
        sor.append('| | n | felismerte (hibás) | nem ismerte fel (helyes) | bizonytalan | felismerési arány | Wilson 95% |\n'
                   '|---|---|---|---|---|---|---|')
        for nev, it in itelok:
            lista = [it[t] for t in it if t in csali]
            hb, hl, bz = lista.count('hibas'), lista.count('helyes'), lista.count('bizonytalan')
            for cimke, n in ((nev, hb + hl), (nev + ' · konzervatív', hb + hl + bz)):
                p_, lo, hi = wilson(hb, n)
                sor.append('| %s | %d | %d | %d | %d | %s | %s–%s |' % (cimke, hb + hl + bz, hb, hl, bz, szazalek(p_), szazalek(lo), szazalek(hi)))
        sor.append('')
        for nev, it in itelok:
            lista = [it[t] for t in it if t in csali]
            if lista and lista.count('hibas') < CSALI_KUSZOB * len(csali):
                sor.append('**Figyelem:** %s a csalik közül %d / %d-t ismert fel (a küszöb %d): a számai csak fenntartással '
                           'közölhetők.\n' % (nev, lista.count('hibas'), len(csali), math.ceil(CSALI_KUSZOB * len(csali))))
    sor.append('Könyvcsoportonként (%s, alapminta; a csoportbecslések kis n-en állnak, rétegszintű szám nem közölhető):\n' % fo_nev)
    sor.append(FEJ_P)
    for cs in sorted({csop[t] for t in fo if tip[t] == 'par'}, key=_csoport_sorrend):
        sor.append(pontossag_sor(cs, [fo[t] for t in fo if tip[t] == 'par' and t in alap and csop[t] == cs]))
    sor.append('')
    tsz = {r['tetel_id']: (r.get('tobbszavas') or '') for r in minta}
    sor.append('Többszavas megfelelés szerint (%s, alapminta; 1:n = a magyar szónak több eredetije van, n:1 = a '
               'forrásszónak több magyar párja, n:m = mindkettő):\n' % fo_nev)
    sor.append(FEJ_P)
    for cimke, felt in (('egyszavas (1:1)', lambda x: x == ''), ('többszavas, összesen', lambda x: x != ''),
                        ('· 1:n', lambda x: x == '1:n'), ('· n:1', lambda x: x == 'n:1'), ('· n:m', lambda x: x == 'n:m')):
        sor.append(pontossag_sor(cimke, [fo[t] for t in fo if tip[t] == 'par' and t in alap and felt(tsz.get(t, ''))]))
    sor.append('')
    sor.append('Hibatípusok (a hibás páron, alapminta és túlminta, ellenőrönként): ' + '; '.join(
        '%s: %s' % (nev, ', '.join('%s %d' % (k, n) for k, n in sorted(_szamlal(
            v[t].get('hibatipus') or '(nincs megadva)' for t in v
            if tip[t] == 'par' and (t in alap or t in tul) and v[t]['itelet'] == 'hibas').items())) or '–')
        for nev, v in ellenorok) + '\n')

    sor.append('## 3. Pár nélküli szavak: kimaradási arány\n')
    sor.append('A keret: a párosítatlan magyar szavak a szabály által eldöntött esetek nélkül (önálló névelő, segédige, '
               'alanyi és tárgyi névmás, korrelatív „azért … hogy”); az arány erre a keretre szól. A „konzervatív” sor '
               'a bizonytalant kimaradásnak számolja.\n')
    sor.append('| | n | nincs eredetije (helyes) | van eredetije (kimaradt) | bizonytalan | kimaradási arány | Wilson 95% |\n'
               '|---|---|---|---|---|---|---|')
    for nev, it in itelok:
        lista = [it[t] for t in it if tip[t] == 'parnelkuli']
        sor.append(kimaradas_sor(nev, lista))
        sor.append(kimaradas_sor(nev + ' · konzervatív', lista, konzervativ=True))
    sor.append('')

    sor.append('### 3b. Kimaradt párok: a fordítatlannak jelölt forrásszavak (recall-becslés)\n')
    sor.append('A keret: a `forditatlan` héber és görög szavak a szabály szerinti esetek nélkül (névelő, ʾet, -āh, paragogikus '
               'nun, kötőszó nélküli ve-/καί, [nem TR]). „Van párja”: a gép kihagyott egy párt; az arány a kihagyott párok '
               'aránya ezen a kereten. A „konzervatív” sor a bizonytalant kihagyásnak számolja.\n')
    sor.append('| | n | nincs párja (helyes) | van párja (kimaradt) | bizonytalan | kimaradási arány | Wilson 95% |\n'
               '|---|---|---|---|---|---|---|')
    if any(tip[t] == 'kimaradt' for t in tip):
        for nev, it in itelok:
            lista = [it[t] for t in it if tip[t] == 'kimaradt']
            sor.append(kimaradas_sor(nev, lista))
            sor.append(kimaradas_sor(nev + ' · konzervatív', lista, konzervativ=True))
    else:
        sor.append('| (ebben a mintában nincs ilyen tétel) | | | | | | |')
    sor.append('')

    eltero = []
    if ket:
        (na, a), (nb, b) = ellenorok
        kozos = [r['tetel_id'] for r in minta if r['tetel_id'] in a and r['tetel_id'] in b]
        sor.append('## 4. A két ítélő egyezése (Cohen-kappa)\n')
        sor.append('| tételek | n | megfigyelt egyezés | kappa (3 kategória) | kappa (helyes/hibás; bizonytalan nélkül) | PABAK (helyes/hibás) |')
        sor.append('|---|---|---|---|---|---|')
        # a két ítélő közös tételei az alappárok (a második ítélő csomagja; DT-F175vm): kappa és PABAK az alapmintán
        # és annak könyvcsoport-rétegein, csalik nélkül
        szurok = [('párok, alapminta (csalik nélkül)', lambda t: tip[t] == 'par' and t in alap)]
        for cs_ in sorted({csop[t] for t in alap if tip[t] == 'par'}, key=_csoport_sorrend):
            szurok.append(('· alapminta, %s' % cs_, lambda t, cs_=cs_: tip[t] == 'par' and t in alap and csop[t] == cs_))
        for cimke, szuro in szurok:
            ts = [t for t in kozos if szuro(t)]
            p3 = [(a[t]['itelet'], b[t]['itelet']) for t in ts]
            k3, po3, n3 = kappa(p3, ITELETEK)
            p2 = [x for x in p3 if 'bizonytalan' not in x]
            k2, po2, n2 = kappa(p2, ('helyes', 'hibas'))
            sor.append('| %s | %d | %s | %s | %s (n=%d) | %s |' % (cimke, n3, szazalek(po3), szam(k3), szam(k2), n2,
                                                                  szam(2 * po2 - 1 if n2 else float('nan'))))
        sor.append('')
        elt = [t for t in kozos if a[t]['itelet'] != b[t]['itelet']]
        if szerzoi:
            sor.append('Eltérő tétel: %d (`eltero_tetelek.tsv`); döntnök nincs (nem független második ítélő), '
                       'mindkét ítélet külön közlendő, a konzervatív becsléssel.\n' % len(elt))
        else:
            sor.append('Eltérő tétel: %d; harmadik döntéssel lezárva: %d; döntésre vár: %d (`eltero_tetelek.tsv`).\n' % (
                len(elt), sum(1 for t in elt if dontes.get(t)), len(hianyzo)))
        minta_by = {r['tetel_id']: r for r in minta}
        for t in sorted(elt):
            r = minta_by[t]
            eltero.append([t, r['tipus'], r['vers'], r['hu_szo'], r['er_szo'], r['strong'],
                           a[t]['itelet'], a[t].get('hibatipus', ''), ','.join(map(str, a[t].get('helyes_forras') or [])),
                           _egysor(a[t].get('megjegyzes', '')),
                           b[t]['itelet'], b[t].get('hibatipus', ''), ','.join(map(str, b[t].get('helyes_forras') or [])),
                           _egysor(b[t].get('megjegyzes', '')), '' if szerzoi else dontes.get(t, ''), ''])

    sor.append('## 5. A modell-ellenőr és az ember egyezése\n')
    if not modell:
        sor.append('Nincs modell-ítélet megadva (`--modell-f172`, `--modell-valasz`, `--modell`).\n')
    else:
        sor.append('A modell itt a #172 vak Opus-ellenőre. A bizonytalan emberi ítélet kimarad. Az alapmintán a modell–ember '
                   'egyezés reprezentatív; a 72 Opus-eltérésen (mind „modell: hibás”) a tévesztési mátrix azt mutatja, hány '
                   'modell-eltérést erősít meg az ember; a túlminta-rétegen (bármelyik gépi bíráló hibásnak jelölte) mindkét '
                   'irány előfordul.\n')
        sor.append('| ítélő · tételek | n | egyezés | kappa | modell helyes / ember helyes | modell helyes / ember hibás | modell hibás / ember helyes | modell hibás / ember hibás |')
        sor.append('|---|---|---|---|---|---|---|---|')
        for nev, it in itelok:
            for cimke, szuro in (('párok, alapminta', lambda r: r['tipus'] == 'par' and r['reszminta'] == 'alap'),
                                 ('párok, a 72 Opus-eltérés', lambda r: r.get('opus_elteres') == '1'),
                                 ('párok, a túlminta-réteg (%d)' % len(elter), lambda r: r['elteres'] == '1'),
                                 ('pár nélküli szavak', lambda r: r['tipus'] == 'parnelkuli')):
                k, po, n, m = modell_osszevet(minta, it, modell, szuro)
                if n == 0:
                    continue
                sor.append('| %s · %s | %d | %s | %s | %d | %d | %d | %d |' % (
                    nev, cimke, n, szazalek(po), szam(k), m[('helyes', 'helyes')], m[('helyes', 'hibas')],
                    m[('hibas', 'helyes')], m[('hibas', 'hibas')]))
            bz = sum(1 for t in elter if it.get(t) == 'bizonytalan')
            if bz:
                sor.append('| %s · a túlminta-réteg bizonytalanja | %d | | | | | | |' % (nev, bz))
        sor.append('')
    return '\n'.join(sor), eltero


def _szamlal(it):
    d = {}
    for x in it:
        d[x] = d.get(x, 0) + 1
    return d


def _egysor(s):
    return ' '.join((s or '').replace('\t', ' ').split())


_SORREND = ['OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta', 'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']


def _csoport_sorrend(cs):
    return _SORREND.index(cs) if cs in _SORREND else len(_SORREND)


LETET_ALAP = os.path.join(LETET_DIR, 'F175V_csalik.tsv')


def lekotes_ellenoriz(ut, fn):
    """A letétfájl SHA-256-ja egyezik-e a repóbeli nyilvános lekötéssel (LEKOTES.md); eltérésnél leáll."""
    if not os.path.exists(LEKOTES) or not os.path.exists(ut):
        return
    import hashlib
    with open(LEKOTES, encoding='utf-8') as f:
        for sor in f:
            m = re.match(r'^\| `([^`]+)` \| `([0-9a-f]{64})` \|', sor)
            if m and m.group(1) == fn:
                with open(ut, 'rb') as g:
                    h = hashlib.sha256(g.read()).hexdigest()
                if h != m.group(2):
                    raise SystemExit('a letétbeli %s SHA-256-ja (%s) nem egyezik a nyilvános lekötéssel (%s)' % (fn, h, m.group(2)))


def csali_hozzaad(minta_ut, minta, letet_ut):
    """A minta kiegészítése a csalikkal a letétfájlból, ha a minta.tsv fejléce csalit jelez (csali_sha256=…).
    A letétfájl SHA-256-jának egyeznie kell a fejlécben lekötöttel. letet_ut=None: csalik nélkül."""
    with open(minta_ut, encoding='utf-8') as f:
        fej = f.readline()
    m = re.search(r'csali_sha256=([0-9a-f]{64})', fej)
    if not m or letet_ut is None:
        return minta
    if not os.path.exists(letet_ut):
        raise SystemExit('a minta csalit tartalmaz, de nincs meg a letétfájl: %s (--csali; próbához --csali-nelkul)' % letet_ut)
    import hashlib
    with open(letet_ut, 'rb') as f:
        h = hashlib.sha256(f.read()).hexdigest()
    if h != m.group(1):
        raise SystemExit('a letétfájl SHA-256-ja (%s) nem egyezik a minta.tsv fejlécében lekötöttel (%s)' % (h, m.group(1)))
    _, csalik = tabla(letet_ut)
    return sorted(minta + csalik, key=lambda r: r['tetel_id'])


def dontes_olvas(ut):
    _, sorok = tabla(ut)
    ki = {}
    for r in sorok:
        d = (r.get('dontes') or '').strip()
        if d and d not in ITELETEK:
            raise SystemExit('%s: ismeretlen döntés %r (%s)' % (ut, d, r.get('tetel_id')))
        if d:
            ki[r['tetel_id']] = d
    return ki


def git_head():
    try:
        return subprocess.check_output(['git', '-C', GYOKER, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:  # noqa: BLE001
        return 'ismeretlen'


# ---------------------------------------------------------------- modell-bemenet

def modell_bemenet(minta, konyvtar, koteg=25):
    """A pár nélküli szavak vak modell-ellenőrzésének bemenete, a #172 formájában
    (utasitas.md + koteg_NNN.txt; a CÉL a pár nélküli szó sorszáma)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'karoli_strong'))
    import bemenet  # noqa: E402
    import pontossag_ellenor as pe  # noqa: E402
    cel = {}
    for r in minta:
        if r['tipus'] == 'parnelkuli':
            cel.setdefault(r['vers'], set()).add(int(r['hu_sorszam']))
    versek = sorted(cel)
    os.makedirs(konyvtar, exist_ok=True)
    with open(os.path.join(konyvtar, 'utasitas.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(pe.FELADAT.replace('{SZABALYOK}', pe.utasitas()))
    n = 0
    for k in range(0, len(versek), koteg):
        n += 1
        blokk = [bemenet.versblokk(v, kjv=False) + '\nCÉL (Károli-sorszámok): ' + ', '.join(map(str, sorted(cel[v])))
                 for v in versek[k:k + koteg]]
        with open(os.path.join(konyvtar, 'koteg_%03d.txt' % n), 'w', encoding='utf-8', newline='\n') as f:
            f.write('KÖTEG: %d\n\n' % n + '\n\n'.join(blokk) + '\n')
    return len(versek), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('valaszok', nargs='*', help='egy vagy két ellenőr JSON-exportja (az offline oldalé)')
    ap.add_argument('--szerver-export', help='az online felület (Worker) admin-exportja (F175.V21); a külső ellenőr '
                                             'és a második ítélő szerepét az export adja (= --kulso 1)')
    ap.add_argument('--minta', default=MINTA)
    ap.add_argument('--csali', default=LETET_ALAP,
                    help='a csalik letétfájlja (a repón kívül); kell, ha a minta.tsv fejléce csalit jelez')
    ap.add_argument('--csali-nelkul', action='store_true',
                    help='a csalik nélkül (próbához: ilyenkor az oldal exportja nem illeszkedik a mintához)')
    ap.add_argument('--kulso', type=int, choices=(1, 2),
                    help='a hányadik válaszfájl a külső (független) ellenőré; a fő szám ebből jön, a másik ítélő '
                         'külön sorban áll, döntnök nincs')
    ap.add_argument('--ket-kulso', action='store_true',
                    help='két független külső ellenőr: az eltéréseket harmadik döntés zárja le (--dontes)')
    ap.add_argument('--masodik', default='hozzátartozó',
                    help='a nem független második ítélő jelölése --kulso mellett (alapértelmezés: hozzátartozó)')
    ap.add_argument('--szerzo', type=int, choices=(1, 2),
                    help='a hányadik válaszfájl a szerzőé (= --kulso a másik, --masodik szerző)')
    ap.add_argument('--dontes')
    ap.add_argument('--modell-f172', action='store_true')
    ap.add_argument('--modell-valasz')
    ap.add_argument('--modell')
    ap.add_argument('--modell-bemenet')
    ap.add_argument('--gepi', help='a külső gépi bírálók fagyasztott táblája (vers, hu_sorszam, er_sorszam, helyes_db '
                                   'vagy biralo_* oszlopok); csak a --gepi-sha256-tal együtt')
    ap.add_argument('--gepi-sha256', help='a fagyasztott gépi tábla lekötött SHA-256-ja')
    ap.add_argument('--kimenet', default=os.path.join(VALIDACIO, 'eredmeny'))
    a = ap.parse_args()

    if not os.path.exists(a.minta):
        raise SystemExit('nincs meg a minta: %s (a letétben; másik helyről: --minta)' % a.minta)
    # a nyilvános lekötés a letétbeli fájlokra szól (más --minta, pl. próbaminta, nem ellenőrizhető vele)
    if os.path.abspath(a.minta) == os.path.abspath(MINTA):
        lekotes_ellenoriz(a.minta, 'minta.tsv')
    if not a.csali_nelkul and os.path.abspath(a.csali) == os.path.abspath(LETET_ALAP):
        lekotes_ellenoriz(a.csali, 'F175V_csalik.tsv')
    _, minta = tabla(a.minta)
    minta = csali_hozzaad(a.minta, minta, None if a.csali_nelkul else a.csali)
    if a.modell_bemenet:
        nv, nk = modell_bemenet(minta, a.modell_bemenet)
        print('modell-bemenet: %d vers, %d köteg -> %s' % (nv, nk, a.modell_bemenet))
        if not a.valaszok and not a.szerver_export:
            return
    if a.szerver_export:
        if a.valaszok or a.szerzo or a.ket_kulso or a.kulso:
            raise SystemExit('a --szerver-export mellett nincs válaszfájl, --kulso, --szerzo vagy --ket-kulso: a '
                             'szerepeket az export adja')
        szerver = szerver_export_olvas(a.szerver_export, minta, minta_hash(minta))
        a.valaszok = [a.szerver_export] * len(szerver)
        if len(szerver) == 2:
            a.kulso = 1
    if len(a.valaszok) not in (1, 2):
        raise SystemExit('egy vagy két válaszfájl kell')
    if a.szerzo:
        if a.kulso:
            raise SystemExit('a --szerzo és a --kulso közül csak az egyik adható meg')
        a.kulso, a.masodik = 3 - a.szerzo, 'szerző'
    if a.kulso and a.kulso > len(a.valaszok):
        raise SystemExit('--kulso %d, de csak %d válaszfájl van' % (a.kulso, len(a.valaszok)))
    if len(a.valaszok) == 2 and not a.kulso and not a.ket_kulso:
        raise SystemExit('két válaszfájlnál meg kell mondani a felállást: --kulso 1|2 (külső + nem független második '
                         'ítélő, döntnök nélkül) vagy --ket-kulso (két független külső ellenőr, harmadik döntéssel)')
    szerzoi = bool(a.kulso) and len(a.valaszok) == 2   # nem független második ítélő: döntnök nincs
    if a.dontes and (szerzoi or len(a.valaszok) == 1):
        raise SystemExit('harmadik döntés csak két külső ellenőrnél van (nem független második ítélőnél nincs döntnök)')
    h = minta_hash(minta)
    beolv = szerver if a.szerver_export else [valaszok_olvas(u, minta, h) for u in a.valaszok]
    if len(beolv) == 2 and beolv[0][0] == beolv[1][0]:
        raise SystemExit('a két válaszfájl ugyanattól az ellenőrtől való: %s' % beolv[0][0])
    cimkek = []
    for i, (nev, _, _) in enumerate(beolv, 1):
        szerep = '' if not a.kulso else (', külső' if i == a.kulso else ', ' + a.masodik)
        cimkek.append('%s (%s%s)' % ('AB'[i - 1], nev, szerep))
    if a.kulso == 2 and len(beolv) == 2:   # a külső ellenőr áll elöl: a fő szám az övé
        beolv, cimkek = beolv[::-1], cimkek[::-1]
    dontes = dontes_olvas(a.dontes) if a.dontes else {}
    modell = {}
    if a.modell_f172:
        modell.update(modell_f172(minta))
    if a.modell_valasz:
        modell.update(modell_valasz(minta, a.modell_valasz))
    if a.modell:
        modell.update(modell_tsv(a.modell))

    szoveg, eltero = kiertekel(minta, [(c, v) for c, (_, v, _) in zip(cimkek, beolv)], dontes, modell, szerzoi)
    k_szoveg, k_sorok = karoli_szabad(minta, [(c, v, k) for c, (_, v, k) in zip(cimkek, beolv)])
    s_szoveg, s_sorok = segedeszkoz(minta, [(c, v, k) for c, (_, v, k) in zip(cimkek, beolv)])
    if bool(a.gepi) != bool(a.gepi_sha256):
        raise SystemExit('a --gepi és a --gepi-sha256 csak együtt adható meg')
    gepi = gepi_olvas(a.gepi, a.gepi_sha256, minta) if a.gepi else None
    kulso_v = beolv[0][1]   # a külső (vagy az egyetlen, vagy két külsőnél az első) ellenőr válaszai
    t_szoveg = tajekoztato(minta, cimkek[0], {t: x['itelet'] for t, x in kulso_v.items()},
                           {**beolv[0][2], **kulso_v}, gepi, {r['tetel_id'] for r in minta if r['reszminta'] == 'csali'})
    kulso_teljes = {**beolv[0][2], **beolv[0][1]}
    masodik_teljes = {**beolv[1][2], **beolv[1][1]} if len(beolv) == 2 else {}
    jav, vit = javitas_listak(minta, kulso_teljes, masodik_teljes)
    j_szoveg = ('## 11. Javítás (a protokoll 4.1–4.2 pontja)\n\nJavítható: %d tétel (`javithato.tsv`; eredet: a külső '
                'ellenőr megjelölte a helyes forrásszót %d, mindkét ember hibásnak mondta %d). Vitatott: %d tétel '
                '(`vitatott.tsv`), változtatás nélkül. A javított sor eredetjelzőt kap; a validált tételek a letétben '
                'jelölve.\n' % (len(jav), sum(1 for x in jav if x[-1] == 'kulso_jelolte'),
                                sum(1 for x in jav if x[-1] == 'ket_ember_hibas'), len(vit)))
    szoveg = szoveg + '\n' + k_szoveg + '\n\n' + s_szoveg + '\n\n' + t_szoveg + '\n' + j_szoveg
    head = git_head()
    forras = [os.path.relpath(x, GYOKER).replace(os.sep, '/') if os.path.abspath(x).startswith(GYOKER) else os.path.basename(x)
              for x in [a.minta] + sorted(set(a.valaszok)) + ([a.dontes] if a.dontes else [])]
    prov = ('# MANUAL: scope=F175.V emberi validáció kiértékelése | forras=%s%s @ %s | ts=git:%s | manual '
            '(determinisztikus számítás: eszkozok/karoli_strong_validacio_kiertekel.py; az ítéletek emberi ellenőröké)'
            % (', '.join(forras), ', f172/itelet_par.tsv' if a.modell_f172 else '', head, head))
    os.makedirs(a.kimenet, exist_ok=True)
    with open(os.path.join(a.kimenet, 'kiertekeles.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('<!-- %s -->\n\n# Emberi validáció — kiértékelés\n\n' % prov[2:] + szoveg + '\n')
    with open(os.path.join(a.kimenet, 'eltero_tetelek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(ELTERO_FEJ) + '\n')
        for s in eltero:
            f.write('\t'.join(s) + '\n')
    with open(os.path.join(a.kimenet, 'karoli_szabad_forditas.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(KAROLI_FEJ) + '\n')
        for s in k_sorok:
            f.write('\t'.join(s) + '\n')
    for fn, sorok_ in (('javithato.tsv', jav), ('vitatott.tsv', vit)):
        with open(os.path.join(a.kimenet, fn), 'w', encoding='utf-8', newline='\n') as f:
            f.write(prov + '\n')
            f.write('\t'.join(JAVITAS_FEJ) + '\n')
            for s_ in sorok_:
                f.write('\t'.join(_egysor(x) for x in s_) + '\n')
    with open(os.path.join(a.kimenet, 'segedeszkoz.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(SEGED_FEJ) + '\n')
        for s in s_sorok:
            f.write('\t'.join(s) + '\n')
    print(szoveg)
    print('\n-> %s' % os.path.join(a.kimenet, 'kiertekeles.md'))


if __name__ == '__main__':
    main()
