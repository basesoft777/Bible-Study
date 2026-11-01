#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motivum_hatar.py -- F151 (FELADATOK #151) gepi resze: masodik velemeny egy lezart motivum hataarol.
MINDEN talalat KERDES a felhasznalonak, nem javitas; adatot, motivumfajlt, lexikont nem ir. Kimenet:
`naplok/HATAR_<ID>.md` "Gepi resz" szakasza (a "Modelles resz" szakaszhoz a szkript nem nyul: ha a fajlban
mar van `<!-- MODELLES-KEZDET -->` ... `<!-- MODELLES-VEGE -->` tartalom, azt megorzi).

Ket determinisztikus vizsgalat (modell es API nelkul):

 1. RESZHALMAZ (CLAUDE.md "Uj motivum-ID", 4. kerdes). A motivum beepitett igehely-halmaza
    (`elofordulasok.tsv`, tartomany versekre bontva: `lexikon_general.igehely_lista`) minden mas motivumeval
    osszevetve, MINDKET iranyban. Kerdes lesz belole, ha A <= B (reszhalmaz) vagy |A & B| / |A| >= 0,8 (atfedes);
    a kozos helyek ket idezett sorral, mellettuk a `motivum_kapcsolatok.tsv` meglevo kapcsolata, ha van.

 2. NEGATIV KRITERIUM a BEEPITETT soron -- csak `azonossag_tipusa=formulaikus` hordozon. A #150 szokapcsolat-
    probaja (`jelolt_eloszures.vizsgal`): ha a beepitett sor versenek (tartomanynal az osszes versenek)
    Strong-halmazaban egyetlen gerinc-kombinacio sincs meg teljesen, kerdes (a sor es a `negativ_kriterium`
    idezesevel). Nem formulaikus hordozon a proba NEM fut, es ezt a kimenet kimondja. Ahol nincs szovegadat
    (TAHOT/TAGNT), a sor "nem ellenorizheto" -- a hiany nem negativ lelet.

Proveniencia: `ts` a bemeneti fajlok utolso git-commitjanak ideje (nem a futase) -> ugyanarra a bemenetre
bajtra azonos kimenet.

    python eszkozok/motivum_hatar.py [--motivum ID ...] [--adat adat] [--kimenet naplok]

TSV: split('\\t'), '\\t'.join; csv modul nelkul.
"""
import argparse
import collections
import datetime
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import jelolt_eloszures as JE  # noqa: E402  (a #150 probaja: importalva, nem masolva)
import lexikon_general as LG  # noqa: E402  (igehely_lista)
import szerep_karoli as SZK  # noqa: E402

ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')
ALAPERTELMEZETT_KIMENET = os.path.join(ROOT, 'naplok')
ALAPERTELMEZETT_MOTIVUMOK = ['ISTENTISZT-001', 'HAMART-001']
ATFEDES_KUSZOB = 0.8
FORMULAIKUS = 'formulaikus'
OK_NEM_FUT = 'a hordozó %s: a gépi negatív-kritérium próba nem fut'
MODELLES_KEZDET = '<!-- MODELLES-KEZDET -->'
MODELLES_VEGE = '<!-- MODELLES-VEGE -->'
MODELLES_HELYORZO = 'nem futott (DT-F151a után)'
IDEZET_HOSSZ = 90
BEMENETI_FAJLOK = [
    'adat/elofordulasok.tsv', 'adat/motivumok.tsv', 'adat/motivum_kapcsolatok.tsv',
    'adat/grammatikai_strongok.tsv', 'konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv',
    'konkordancia/Karoli_1908.tsv',
]
SCOPE = ('elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) '
         '+ motivum_kapcsolatok.tsv')
FORRAS = ('motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; '
          'lexikon_general.igehely_lista)')


# ---------------------------------------------------------------------------------------------------------------
# beolvasas (sorszammal)
# ---------------------------------------------------------------------------------------------------------------

def beolvas_sorszammal(ut):
    """[(fajlbeli_sorszam (1-tol), dict)] -- split('\\t'); a '#' kommentsorok es az ures sorok kimaradnak, de a
    sorszam a fajl TENYLEGES sora (a kommentsorokkal egyutt)."""
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = None
    ki = []
    for i, s in enumerate(sorok, 1):
        s = s.rstrip('\r')
        if not s.strip() or s.startswith('#'):
            continue
        if fej is None:
            fej = s.split('\t')
            continue
        ki.append((i, dict(zip(fej, s.split('\t')))))
    return ki


# ---------------------------------------------------------------------------------------------------------------
# 1. reszhalmaz
# ---------------------------------------------------------------------------------------------------------------

def vers_lista(igehely, bonto=None):
    """Egy igehely -> [vers-kulcs] (tartomany: minden vers). A bontast a `bonto` (alap: LG.igehely_lista) adja."""
    return (bonto or LG.igehely_lista)(igehely.replace('–', '-'))


def motivum_versek(sorok, mot_id, bonto=None):
    """{vers: [(sorszam, igehely)]} a motivum beepitett soraibol (sorok: [(sorszam, dict)])."""
    d = collections.OrderedDict()
    for ln, r in sorok:
        if r.get('id') != mot_id:
            continue
        for v in vers_lista(r['igehely'], bonto):
            d.setdefault(v, []).append((ln, r['igehely']))
    return d


def reszhalmaz_viszony(a, b, kuszob=ATFEDES_KUSZOB):
    """(tipus, arany) az A halmaz viszonya B-hez, vagy None. a, b: vers-halmazok.
    'azonos': A == B; 'reszhalmaz': A < B; 'atfedes': |A & B| / |A| >= kuszob; egyébként None (üres A vagy üres közös: None)."""
    a, b = set(a), set(b)
    if not a or not b:
        return None
    kozos = a & b
    if not kozos:
        return None
    if a == b:
        return 'azonos', 1.0
    arany = len(kozos) / len(a)
    if a <= b:
        return 'reszhalmaz', arany
    if arany >= kuszob:
        return 'atfedes', arany
    return None


def parok_tabla(cel_id, sorok, kapcsolatok, bonto=None):
    """[(masik_id, |A|, |B|, kozos_db, |A&B|/|A|, |A&B|/|B|, [kapcsolat-sorszamok])] -- minden mas motivumra (átlátható
    ellenőrzés: az üres eredmény mellett is látszik, mit vetett össze a szkript)."""
    idk = []
    for _ln, r in sorok:
        if r['id'] not in idk:
            idk.append(r['id'])
    a_v = set(motivum_versek(sorok, cel_id, bonto))
    ki = []
    for b_id in sorted(i for i in idk if i != cel_id):
        b_v = set(motivum_versek(sorok, b_id, bonto))
        k = len(a_v & b_v)
        ki.append((b_id, len(a_v), len(b_v), k, (k / len(a_v)) if a_v else 0.0, (k / len(b_v)) if b_v else 0.0,
                   [ln for ln, c in kapcsolatok if {c.get('id_a'), c.get('id_b')} == {cel_id, b_id}]))
    return ki


def reszhalmaz_kerdesek(cel_id, sorok, kapcsolatok, bonto=None, kuszob=ATFEDES_KUSZOB):
    """[dict] -- a cel_id motivum minden mas motivummal, mindket iranyban. A kimenet rendezett (motivum, irany).
    Az 'azonos' halmaz egyszer szerepel (irany='ket_irany')."""
    idk = []
    for _ln, r in sorok:
        if r['id'] not in idk:
            idk.append(r['id'])
    a_v = motivum_versek(sorok, cel_id, bonto)
    ki = []
    for b_id in sorted(i for i in idk if i != cel_id):
        b_v = motivum_versek(sorok, b_id, bonto)
        kapcs = [(ln, k) for ln, k in kapcsolatok if {k.get('id_a'), k.get('id_b')} == {cel_id, b_id}]
        elo = reszhalmaz_viszony(a_v.keys(), b_v.keys(), kuszob)
        vissza = reszhalmaz_viszony(b_v.keys(), a_v.keys(), kuszob)
        if elo and elo[0] == 'azonos':
            vissza = None
            irany = 'ket_irany'
        else:
            irany = None
        for viszony, jel, kisebb, nagyobb in ((elo, irany or 'A_B', a_v, b_v), (vissza, 'B_A', b_v, a_v)):
            if not viszony:
                continue
            kozos = [v for v in kisebb if v in nagyobb]
            ki.append({
                'cel': cel_id, 'masik': b_id, 'irany': jel, 'tipus': viszony[0], 'arany': viszony[1],
                'kisebb_db': len(kisebb), 'nagyobb_db': len(nagyobb), 'a_db': len(a_v), 'b_db': len(b_v),
                'kozos': [(v, a_v[v], b_v[v]) for v in kozos if v in a_v and v in b_v],
                'kapcsolatok': kapcs,
            })
    return ki


# ---------------------------------------------------------------------------------------------------------------
# 2. negativ kriterium a beepitett soron
# ---------------------------------------------------------------------------------------------------------------

def negativ_kriterium_futtat(cel_id, hordozo, sorok, vers_st):
    """(fut: bool, [(sorszam, sor, megvan, ok)]) -- fut=False, ha a hordozó nem formulaikus (a próba nem fut).
    megvan: True / False / None (nincs szövegadat vagy nincs gerinc-kombináció)."""
    if hordozo != FORMULAIKUS:
        return False, []
    komb = JE.kombinaciok([r for _ln, r in sorok]).get(cel_id, [])
    ki = []
    for ln, r in sorok:
        if r.get('id') != cel_id:
            continue
        megvan, ok = JE.vizsgal(r['igehely'], komb, vers_st)
        ki.append((ln, r, megvan, ok))
    return True, ki


# ---------------------------------------------------------------------------------------------------------------
# kimenet
# ---------------------------------------------------------------------------------------------------------------

def vag(s, n=IDEZET_HOSSZ):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


def idez_elo(ln, r, fajl='adat/elofordulasok.tsv'):
    return '`%s:%d` „%s | %s | %s”' % (fajl, ln, r.get('id', ''), r.get('igehely', ''), vag(r.get('kapcsolodas', '')))


def idez_mot(ln, r, fajl='adat/motivumok.tsv'):
    return '`%s:%d` „%s | negativ_kriterium: %s”' % (fajl, ln, r.get('id', ''), vag(r.get('negativ_kriterium', ''), 260))


def _git(args, root):
    return JE._git(args, root)


def bemenet_azonosito(root):
    """(bemenet-szöveg, ts): a bemeneti fájlok HEAD-blobjai és utolsó commitjuk ideje (nem a futásé)."""
    resz = []
    for f in BEMENETI_FAJLOK:
        h = _git(['rev-parse', 'HEAD:%s' % f], root)
        resz.append('%s@%s' % (f, h[:10] if h else 'nincs-git'))
    ep = _git(['log', '-1', '--format=%ct', '--'] + BEMENETI_FAJLOK, root)
    ts = (datetime.datetime.fromtimestamp(int(ep), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
          if ep and ep.isdigit() else 'ismeretlen')
    return ','.join(resz), ts


def tabla_szoveg(cel_id, tabla):
    """Az összevetés teljes táblája (nem kérdés: a kimenet átláthatósága)."""
    if not tabla:
        return []
    ki = ['Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):', '',
          '| másik motívum | %s versei | másik versei | közös | közös/%s | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |' % (cel_id, cel_id),
          '|---|---|---|---|---|---|---|']
    for b, an, bn, k, ra, rb, kl in tabla:
        ki.append('| %s | %d | %d | %d | %d%% | %d%% | %s |' % (
            b, an, bn, k, round(ra * 100), round(rb * 100), ', '.join(str(x) for x in kl) if kl else 'nincs'))
    ki.append('')
    return ki


def resz1_szoveg(kerdesek, cel_id, a_db, tabla=()):
    """Az 1. szakasz sorai."""
    ki = ['### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)', '']
    ki.append('Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), %s összes '
              'beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ %d%% '
              '(A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).' % (cel_id, int(ATFEDES_KUSZOB * 100)))
    ki.append('')
    if not kerdesek:
        ki.append('**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥%d%% átfedés (%d beépített vers '
                  'vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az '
                  'igehely-halmazra.' % (int(ATFEDES_KUSZOB * 100), a_db))
        ki.append('')
        ki += tabla_szoveg(cel_id, tabla)
        return ki
    for i, k in enumerate(kerdesek, 1):
        a, b = k['cel'], k['masik']
        if k['tipus'] == 'azonos':
            allitas = ('%s és %s beépített vers-halmaza azonos (%d vers): egy motívum két néven, vagy mindkettő külön funkcióval?'
                       % (a, b, k['kisebb_db']))
        else:
            kisebb, nagyobb = (a, b) if k['irany'] == 'A_B' else (b, a)
            if k['tipus'] == 'reszhalmaz':
                allitas = ('%s mind a %d beépített verse benne van a(z) %s %d versében: részhalmaz-e / ↳ alpont-e?'
                           % (kisebb, k['kisebb_db'], nagyobb, k['nagyobb_db']))
            else:
                allitas = ('%s %d beépített versének %d%%-a (%d/%d) benne van a(z) %s %d versében: részhalmaz-e / ↳ alpont-e?'
                           % (kisebb, k['kisebb_db'], round(k['arany'] * 100), len(k['kozos']), k['kisebb_db'], nagyobb, k['nagyobb_db']))
        ki.append('- **K%d (%s)** %s' % (i, k['tipus'], allitas))
        if k['kapcsolatok']:
            ki.append('  - meglévő kapcsolat (`motivum_kapcsolatok.tsv`, %d sor): %s' % (
                len(k['kapcsolatok']),
                '; '.join('`adat/motivum_kapcsolatok.tsv:%d` (%s: %s ↔ %s)' % (
                    ln, c.get('tipus', ''), c.get('igehely_a', ''), c.get('igehely_b', '')) for ln, c in k['kapcsolatok'])))
        else:
            ki.append('  - meglévő kapcsolat (`motivum_kapcsolatok.tsv`): nincs a két motívum között')
        ki.append('  - közös helyek (%d), soronként a két idézett sor:' % len(k['kozos']))
        for v, a_sorok, b_sorok in k['kozos']:
            ki.append('    - %s — %s: `adat/elofordulasok.tsv:%d` „%s | %s” · %s: `adat/elofordulasok.tsv:%d` „%s | %s”' % (
                v, a, a_sorok[0][0], a, a_sorok[0][1], b, b_sorok[0][0], b, b_sorok[0][1]))
    ki.append('')
    ki += tabla_szoveg(cel_id, tabla)
    return ki


def resz2_szoveg(cel_id, mot_ln, mot, fut, eredmenyek, hordozo):
    """A 2. szakasz sorai."""
    ki = ['### 2. Negatív kritérium a beépített sorokon', '']
    if not fut:
        ki.append('**%s.** A hordozó (`azonossag_tipusa`) = `%s` (`adat/motivumok.tsv:%d`). A #150 szókapcsolat-próbája '
                  'csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). '
                  'A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.'
                  % (OK_NEM_FUT % hordozo, hordozo, mot_ln))
        ki.append('')
        return ki
    kerdes = [e for e in eredmenyek if e[2] is False]
    nem = [e for e in eredmenyek if e[2] is None]
    ok = [e for e in eredmenyek if e[2] is True]
    ki.append('Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi '
              '(`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének '
              'Strong-halmazában (TAHOT+TAGNT). Hordozó: `%s`.' % hordozo)
    ki.append('')
    ki.append('Összesítés: %d beépített sor; gerinc-kombináció megvan: %d; **kérdés (hiányzik): %d**; nem ellenőrizhető '
              '(nincs szövegadat / nincs kombináció): %d.' % (len(eredmenyek), len(ok), len(kerdes), len(nem)))
    ki.append('')
    if not kerdes:
        ki.append('**0 kérdés.** Mind a %d ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.' % len(ok))
        ki.append('')
    for i, (ln, r, _m, why) in enumerate(kerdes, 1):
        ki.append('- **N%d** A(z) %s beépített sor versében nincs meg a gerinc-kombináció (%s): a sor belefér-e a negatív kritériumba?'
                  % (i, r['igehely'], why))
        ki.append('  - sor: %s' % idez_elo(ln, r))
        ki.append('  - negatív kritérium: %s' % idez_mot(mot_ln, mot))
    for i, (ln, r, _m, why) in enumerate(nem, 1):
        ki.append('- **E%d** (nem ellenőrizhető, nem kérdés) %s: %s — sor: %s' % (i, r['igehely'], why, idez_elo(ln, r)))
    if kerdes or nem:
        ki.append('')
    return ki


def modelles_resz(regi_tartalom=None):
    """A „Modelles rész” blokkja; ha a régi fájlban van már tartalom a jelölők között, azt megőrzi."""
    tartalom = MODELLES_HELYORZO
    if regi_tartalom and MODELLES_KEZDET in regi_tartalom and MODELLES_VEGE in regi_tartalom:
        resz = regi_tartalom.split(MODELLES_KEZDET, 1)[1].split(MODELLES_VEGE, 1)[0].strip('\n')
        if resz.strip():
            tartalom = resz
    return ['## Modelles rész', '', MODELLES_KEZDET, tartalom, MODELLES_VEGE, '']


def motivum_szoveg(cel_id, adat, bemenet, ts, vers_st, regi=None, bonto=None):
    """(markdown-szöveg, összesítő-dict) egy motívumra."""
    sorok = beolvas_sorszammal(os.path.join(adat, 'elofordulasok.tsv'))
    mots = beolvas_sorszammal(os.path.join(adat, 'motivumok.tsv'))
    kapcs = [(ln, k) for ln, k in beolvas_sorszammal(os.path.join(adat, 'motivum_kapcsolatok.tsv'))]
    mot_ln, mot = next(((ln, r) for ln, r in mots if r['id'] == cel_id), (0, None))
    if mot is None:
        raise ValueError('ismeretlen motívum: %s' % cel_id)
    hordozo = mot.get('azonossag_tipusa', '?')
    a_v = motivum_versek(sorok, cel_id, bonto)
    kerdesek = reszhalmaz_kerdesek(cel_id, sorok, kapcs, bonto)
    fut, ered = negativ_kriterium_futtat(cel_id, hordozo, sorok, vers_st)
    prov = 'scope=%s | forras=%s | motivum=%s | ts=%s' % (SCOPE, FORRAS, cel_id, ts)
    ki = ['# HATAR_%s.md — motívum-határ ellenőrzés (F151, #151)' % cel_id, '',
          '*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum %s`, determinisztikus; újrafuttatáskor felülíródik); '
          'a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; '
          'adatot, motívumfájlt, lapot ez a fájl nem módosít.*' % cel_id, '',
          '*(proveniencia: %s | bemenet=%s)*' % (prov, bemenet), '',
          '**Motívum:** %s — %s · hordozó: `%s` · fölérendelt fogalom: %s · beépített sor: %d (%d vers)' % (
              cel_id, mot.get('cim', ''), hordozo, vag(mot.get('folerendelt_fogalom', ''), 160),
              sum(1 for _l, r in sorok if r['id'] == cel_id), len(a_v)),
          '', '## Gépi rész', '']
    ki += resz1_szoveg(kerdesek, cel_id, len(a_v), parok_tabla(cel_id, sorok, kapcs, bonto))
    ki += resz2_szoveg(cel_id, mot_ln, mot, fut, ered, hordozo)
    ki += modelles_resz(regi)
    ossz = {
        'hordozo': hordozo, 'sorok': sum(1 for _l, r in sorok if r['id'] == cel_id), 'versek': len(a_v),
        'k_reszhalmaz': sum(1 for k in kerdesek if k['tipus'] == 'reszhalmaz'),
        'k_atfedes': sum(1 for k in kerdesek if k['tipus'] == 'atfedes'),
        'k_azonos': sum(1 for k in kerdesek if k['tipus'] == 'azonos'),
        'negativ_fut': fut, 'n_kerdes': sum(1 for e in ered if e[2] is False),
        'n_megvan': sum(1 for e in ered if e[2] is True), 'n_nem_ellenorizheto': sum(1 for e in ered if e[2] is None),
    }
    return '\n'.join(ki).rstrip('\n') + '\n', ossz


def futtat(motivumok, adat=ALAPERTELMEZETT_ADAT, kimenet=None, root=ROOT, vers_st=None, bemenet_fn=None, bonto=None):
    """{motivum: (szöveg, összesítő)}; ha `kimenet` van, a fájlokat (LF) ki is írja."""
    bemenet, ts = (bemenet_fn or bemenet_azonosito)(root)
    vers_st = vers_st if vers_st is not None else SZK.vers_strongok()
    ki = collections.OrderedDict()
    for m in motivumok:
        ut = os.path.join(kimenet, 'HATAR_%s.md' % m) if kimenet else None
        regi = None
        if ut and os.path.exists(ut):
            with open(ut, encoding='utf-8', newline='') as f:
                regi = f.read()
        sz, ossz = motivum_szoveg(m, adat, bemenet, ts, vers_st, regi, bonto)
        ki[m] = (sz, ossz)
        if ut:
            os.makedirs(kimenet, exist_ok=True)
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(sz)
    return ki


def main():
    ap = argparse.ArgumentParser(description='F151 -- motívum-határ: gépi rész (részhalmaz, negatív kritérium)')
    ap.add_argument('--motivum', nargs='+', default=ALAPERTELMEZETT_MOTIVUMOK, help='motívum-ID-k')
    ap.add_argument('--adat', default=ALAPERTELMEZETT_ADAT)
    ap.add_argument('--kimenet', default=ALAPERTELMEZETT_KIMENET, help='alapértelmezés: naplok/')
    args = ap.parse_args()
    for m, (_sz, o) in futtat(args.motivum, args.adat, args.kimenet).items():
        print('  HATAR_%s.md: hordozó=%s, részhalmaz %d, átfedés %d, azonos %d; negatív-kritérium: %s' % (
            m, o['hordozo'], o['k_reszhalmaz'], o['k_atfedes'], o['k_azonos'],
            ('kérdés %d, megvan %d, nem ellenőrizhető %d' % (o['n_kerdes'], o['n_megvan'], o['n_nem_ellenorizheto']))
            if o['negativ_fut'] else 'nem fut (nem formulaikus hordozó)'), file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
