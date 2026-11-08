#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
megfelelo_kinyer.py -- a visszhang-blokk kinyerő táblája (F178.5, FELADATOK #178): `adat/visszhang_megfelelok.tsv`.

A lap visszhang-blokkja lánc-szavanként azt mutatja, hogy az ókori fordító (Targum, Vulgata, LXX) ugyanazzal a szóval
adja-e vissza a lánc szavát minden láncversben (DT639). Szóillesztés nincs, ezért a fordítás szavát egy tábla hordozza
(SEMA 2.53). Három út:

    beolvas  KINYERT.tsv --ellenor MODELL --atnezes ATN.tsv [--lemma-javitas JAV.tsv] [--lemma-megerosites MEG.tsv]
             a modell-kinyerés (Targum, Vulgata, BDB rokon nyelv; `kinyeres`=modell) sorai a táblába. A másik kéz
             (`--ellenor`: a tényleges modellnév, nem a kinyerőé) ellenőrzése két rész: gépi — a nem üres `alak`
             szó szerint a forrás versszövegében (Targum, Vulgata) vagy a BDB-szócikkben / a rokon írások
             gyorsítótárában áll-e (üres alak nem egyezés); kézi — az ellenőr soronkénti ítélete az `--atnezes`
             bemenetben. A kód a kézi átnézést nem állítja, csak a bemenet sorát írja át (ELLENOR_F178 4.); átnézés
             nélkül, elvetett vagy gépileg nem egyező sorral az `ellenorzes` üres (ellenőrizetlen sor nem renderel). A
             `--lemma-javitas` (motivum, strong, igehely, forras, lemma, indok) az ellenőr lemma-egységesítése (pl. a
             gyök egy alakra), a `megjegyzes` mezőben jelölve; az ilyen sor csak egy harmadik kéz (nem az ellenőr)
             megerősítésével (`--lemma-megerosites`) ellenőrzött (ELLENOR_F178 3.). Az arámi kiejtés gépi
             (`heber_kiejtes.kiejt(aram=True)`).
    lxx      --motivum ID
             a LXX-oszlop gépileg: a tábla nem LXX láncsoraiban álló (strong, igehely) párokra a `LXX_OS` versének
             azon lemmái, amelyek a héber szó versszintű LXX-párjai között (`LXX_versszintu_parok.tsv`) a leggyakoribb
             öt közt állnak; egyetlen lemma (vagy egy szócsalád): `kinyeres`=gepi, ellenőrzött; több vagy egy sem:
             a sor alak nélkül, a `megjegyzes` kimondja, ellenőrizetlen (modell-kinyerésre vár).
    ellenoriz
             a tábla szerkezete: oszlopszám, zárt értékek, kulcs-egyediség, proveniencia; kilépési kód 1 hibánál.

TSV: split('\\t') / '\\t'.join(), a csv modul nem használható (CLAUDE.md). Írás előtt a régi sorokkal összevetve.
"""
import argparse
import datetime
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

TABLA = os.path.join(GYOKER, 'adat', 'visszhang_megfelelok.tsv')
OSZLOPOK = ['motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas', 'megjegyzes',
            'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
FORRASOK = ('targum', 'vulgata', 'lxx', 'bdb')
KINYERES = ('gepi', 'modell', 'kezi')
FEJ_MEGJ = ('# A visszhang-blokk kinyerő táblája (F178.5). Kulcs: motivum + strong + igehely + forras (+ alak a bdb '
            'soroknál a nyelv és a jelentés is). Séma: adat/SEMA.md 2.53. Ellenőrizetlen sor (üres `ellenorzes`) a lapon nem renderel.')
LXX_TOP = 5
DICE_MIN = 0.05     # a társulás alsó határa (Dice)
DICE_ARANY = 2.0    # a választott lemma legalább ennyiszer erősebb a következő, más családú lemmánál
ELOTAGOK = ('επι', 'κατα', 'κατ', 'δια', 'δι', 'συν', 'εκ', 'απο', 'προ')


def ma():
    return datetime.date.today().isoformat()


def tsv_olvas(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    if not sorok:
        return []
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t') + [''] * (len(fej) - len(s.split('\t'))))) for s in sorok[1:]]


def kulcs(r):
    return (r['motivum'], r['strong'], r['igehely'], r['forras'],
            (r['alak'], r['lemma'], r['jelentes']) if r['forras'] == 'bdb' else '')


def tabla_ir(sorok):
    regi = {kulcs(r): r for r in tsv_olvas(TABLA)}
    uj = {kulcs(r): r for r in sorok}
    if len(uj) != len(sorok):
        raise SystemExit('HIBA: a kulcs nem egyedi az írandó sorokban')
    valt = sum(1 for k in uj if k in regi and regi[k] != uj[k])
    sorrend = sorted(uj.values(), key=lambda r: (r['motivum'], FORRASOK.index(r['forras']), r['strong'],
                                                 r['igehely'], r['alak']))
    with open(TABLA, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJ_MEGJ + '\n' + '\t'.join(OSZLOPOK) + '\n')
        for r in sorrend:
            f.write('\t'.join(r.get(o, '') for o in OSZLOPOK) + '\n')
    print('  %s: %d sor (új %d, változott %d, változatlan %d)' % (os.path.relpath(TABLA, GYOKER), len(uj),
          sum(1 for k in uj if k not in regi), valt, sum(1 for k in uj if k in regi and regi[k] == uj[k])))


def versszoveg(forras):
    if forras == 'targum':
        return {r['igehely']: r['szoveg'] for r in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'Targum_PD.tsv'))
                if r['targum'] == 'Onkelos'}
    if forras == 'vulgata':
        return {r['igehely']: r['szoveg']
                for r in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'Vulgata_Clementina.tsv'))}
    return {}


def kanon(s):
    """Összevetési alak: NFD, a betűnkénti mellékjelek kódpont-sorrendben (a pontozás sorrendje forrásonként eltér)."""
    import unicodedata
    ki, jelek = [], []
    for c in unicodedata.normalize('NFD', s or ''):
        if unicodedata.combining(c) or '֑' <= c <= 'ׇ':
            jelek.append(c)
            continue
        ki.extend(sorted(jelek))
        jelek = []
        ki.append(c)
    ki.extend(sorted(jelek))
    return ''.join(ki)


def bdb_szoveg(strong):
    t = ''
    for r in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')):
        if r.get('Strong_eredeti') == strong or r.get('Strong_padded') == strong:
            t += r.get('Teljes_szocikk', '')
    for r in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'BDB_rokon_irasok.tsv')):
        if r.get('strong') == strong:
            t += ' ' + r.get('szoalak', '') + ' ' + r.get('kontextus', '')
    return t


LEMMA_JEL = '[ellenőri lemma-egységesítés'


def atnezes_kulcs(r):
    return (r['motivum'], r['strong'], r['igehely'], r['forras'], r.get('alak', '').strip())


def ellenorzes_mezo(r, jo, atnezes, megerosites, ellenor, datum):
    """(az `ellenorzes` mező, az ellenőrizetlenség oka vagy None) — ELLENOR_F178 4.: a kód csak azt írja be, ami
    megtörtént. A gépi összevetés csak nem üres alakon egyezés (üres alak nem egyezik semmivel); a kézi átnézést nem a
    kód állítja, hanem az átnézés-bemenet sora (`--atnezes`: az ellenőr soronkénti ítélete); az ellenőr lemma-
    egységesítése csak egy harmadik kéz (nem az ellenőr) megerősítésével (`--lemma-megerosites`) renderelhető
    (ELLENOR_F178 3.). Ellenőrizetlen sor: üres mező (a lapon nem renderel)."""
    if r['modell'] == ellenor:
        return '', 'a kinyerő és az ellenőr ugyanaz: %s' % ellenor   # aki kinyer (vagy kézzel javít), nem ellenőriz
    if r['alak'] and not jo:
        return '', 'az alak nem áll a forrásban'
    at = atnezes.get(atnezes_kulcs(r))
    if not at or at.get('itelet') != 'jo':
        return '', 'nincs kézi átnézés' if not at else 'az átnézés elvetette (%s)' % at.get('megjegyzes', '')
    if at.get('atnezo') != ellenor or at.get('atnezo') == r['modell']:
        return '', 'az átnéző (%s) nem az ellenőr, vagy azonos a kinyerővel' % at.get('atnezo')
    if LEMMA_JEL in r['megjegyzes']:
        m = megerosites.get((r['motivum'], r['strong'], r['igehely'], r['forras']))
        if not m or m.get('itelet') != 'megerosit' or m.get('lemma_a_tablaban') != r['lemma'] \
                or m.get('modell') in ('', ellenor):
            return '', 'az ellenőri lemma-egységesítést harmadik kéz nem erősítette meg'
    reszek = ['%s, %s: kézi átnézés (az átnézés-bemenet szerint)' % (ellenor, datum)]
    reszek.append('az alak a forrásban szó szerint áll (gépi összevetés)' if r['alak']
                  else 'alak nélküli sor: a gépi összevetés nem alkalmazható')
    return '; '.join(reszek), None


def beolvas(a):
    import heber_kiejtes as HK
    kinyert = tsv_olvas(a.kinyert)
    jav = {(r['motivum'], r['strong'], r['igehely'], r['forras']): r for r in tsv_olvas(a.lemma_javitas)} \
        if a.lemma_javitas else {}
    atnezes = {atnezes_kulcs(r): r for r in tsv_olvas(a.atnezes)} if a.atnezes else {}
    megerosites = {(r['motivum'], r['strong'], r['igehely'], r['forras']): r
                   for r in tsv_olvas(a.lemma_megerosites)} if a.lemma_megerosites else {}
    szov = {f: versszoveg(f) for f in ('targum', 'vulgata')}
    bdb = {}
    meglevo = {kulcs(r): r for r in tsv_olvas(TABLA)}
    ki, hibas = [], []
    for r in kinyert:
        r = {o: (r.get(o) or '').strip() for o in OSZLOPOK}
        if r['forras'] not in FORRASOK or r['kinyeres'] not in KINYERES:
            raise SystemExit('HIBA: zárt érték: %s / %s' % (r['forras'], r['kinyeres']))
        j = jav.get((r['motivum'], r['strong'], r['igehely'], r['forras']))
        if j:
            r['lemma'] = j['lemma']
            r['megjegyzes'] = (r['megjegyzes'] + ' ' if r['megjegyzes'] else '') + \
                '%s: %s]' % (LEMMA_JEL, j['indok'])
        m = megerosites.get((r['motivum'], r['strong'], r['igehely'], r['forras']))
        if m and LEMMA_JEL in r['megjegyzes'] and m.get('itelet') == 'megerosit' \
                and m.get('lemma_a_tablaban') == r['lemma'] and '[lemma megerősítve' not in r['megjegyzes']:
            r['megjegyzes'] += ' [lemma megerősítve: %s, %s]' % (m['modell'], ma())
        if r['forras'] == 'targum' and r['alak']:
            r['kiejtes'] = ' · '.join(HK.kiejt(x.strip(), aram=True) for x in r['alak'].split('·'))
        if r['forras'] == 'lxx':
            if 'lxx' not in szov:
                szov['lxx'] = {}
                for f in os.listdir(os.path.join(GYOKER, 'konkordancia', 'LXX_OS')):
                    if f.endswith('.tsv'):
                        for t in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'LXX_OS', f)):
                            h = t.get('igehely_karoli', '')
                            szov['lxx'][h] = szov['lxx'].get(h, '') + ' ' + t.get('szoalak', '')
            vers = kanon(szov['lxx'].get(r['igehely'], ''))
            jo = gepi_egyezik(r['alak'], vers, kanon)
        elif r['forras'] in ('targum', 'vulgata'):
            vers = kanon(szov[r['forras']].get(r['igehely'], ''))
            jo = gepi_egyezik(r['alak'], vers, kanon)
        else:
            if r['strong'] not in bdb:
                bdb[r['strong']] = bdb_szoveg(r['strong'].split('+')[0])
            jo = bool(r['alak']) and (r['alak'].replace('ḳ', '‡').replace('q', '‡') in bdb[r['strong']]
                                      or gepi_egyezik(r['alak'], bdb[r['strong']], lambda x: x))
        r['ellenorzes'], ok = ellenorzes_mezo(r, jo, atnezes, megerosites, a.ellenor, ma())
        if ok:
            hibas.append('%s %s %s: %s (%s)' % (r['strong'], r['igehely'], r['forras'], r['alak'] or '—', ok))
        ki.append(r)
    for k, r in meglevo.items():
        if k not in {kulcs(x) for x in ki}:
            ki.append(r)
    tabla_ir(ki)
    for h in hibas:
        print('  ELLENŐRIZETLEN: %s' % h)
    return 0


def gepi_egyezik(alak, szoveg, norm):
    """A gépi összevetés: minden ` · `-tal elválasztott alak szó szerint áll a szövegben. Üres alak nem egyezés
    (ELLENOR_F178 4.): az alak nélküli sor hiányát gép nem igazolja, csak a kézi átnézés."""
    reszek = [x.strip() for x in (alak or '').split('·')]
    return bool(alak and alak.strip()) and all(x and norm(x) in szoveg for x in reszek)


def szocsalad(lemma):
    """A görög lemma előtag nélküli tövei (ékezet nélkül, 3 betű): két lemma egy szócsalád, ha metszenek
    (φθείρω ~ καταφθείρω; ἐπικατάρατος ~ καταράομαι)."""
    import unicodedata
    t = ''.join(c for c in unicodedata.normalize('NFD', lemma.lower()) if not unicodedata.combining(c))
    tovek, sor = set(), [t]
    while sor:
        x = sor.pop()
        tovek.add(x[:3])
        for e in ELOTAGOK:
            if x.startswith(e) and len(x) > len(e) + 2:
                sor.append(x[len(e):])
    return tovek


def szocsalad_g(g, vers_tok):
    l = next((t['lemma'] for t in vers_tok if ('G%04d' % int(t['strong'])) == g), '')
    return szocsalad(l) if l else set()


def lxx(a):
    import lexikon_general as LG
    tabla = tsv_olvas(TABLA)
    parok = LG.lxx_versszintu_parok()
    lxx_os = {}
    for f in os.listdir(os.path.join(GYOKER, 'konkordancia', 'LXX_OS')):
        if f.endswith('.tsv'):
            for r in tsv_olvas(os.path.join(GYOKER, 'konkordancia', 'LXX_OS', f)):
                lxx_os.setdefault(r.get('igehely_karoli', ''), []).append(r)
    betoldott = {(r['strong'], r['igehely']) for r in tabla if r['motivum'] == a.motivum and r['betoldas'] == 'igen'}
    kezi = {(r['strong'], r['igehely']) for r in tabla
            if r['motivum'] == a.motivum and r['forras'] == 'lxx' and r['kinyeres'] == 'kezi'}
    # a betoldás-sor és a kézi LXX-sor nem gépi (a betoldott szónak nincs héber párja a versben)
    parok_szuksegesek = sorted({(r['strong'], r['igehely']) for r in tabla
                                if r['motivum'] == a.motivum and r['forras'] in ('targum', 'vulgata') and r['igehely']}
                               - betoldott - kezi)
    # a görög lemmák versgyakorisága a teljes LXX_OS-ben (a Dice-arány nevezőjéhez)
    g_versek = {}
    for hely_, toks in lxx_os.items():
        for g in {t.get('strong') for t in toks if (t.get('strong') or '').isdigit()}:
            g_versek['G%04d' % int(g)] = g_versek.get('G%04d' % int(g), 0) + 1
    uj = [r for r in tabla if not (r['motivum'] == a.motivum and r['forras'] == 'lxx' and r['kinyeres'] != 'kezi')]
    for strong, hely in parok_szuksegesek:
        # a héber szó és a vers görög lemmáinak társulása (Dice: 2·közös / (héber versei + görög versei)); a
        # leggyakoribb szavak (γῆ, λέγω, κύριος) így nem nyernek a puszta együtt-előfordulással
        dice = {}
        for h in strong.split('+'):
            e = parok.get(h)
            if not e:
                continue
            n_h = len(e['versek'])
            kozos = {}
            for gs in e['versek'].values():
                for g in set(gs or []):
                    kozos[g] = kozos.get(g, 0) + 1
            for g, k in kozos.items():
                dice[g] = max(dice.get(g, 0), 2.0 * k / (n_h + g_versek.get(g, k)))
        vers_tok = [t for t in lxx_os.get(hely, []) if (t.get('strong') or '').isdigit()]
        pont = sorted({('G%04d' % int(t['strong'])): dice.get('G%04d' % int(t['strong']), 0) for t in vers_tok}.items(),
                      key=lambda x: -x[1])
        valasztott = []
        if pont and pont[0][1] >= DICE_MIN:
            valasztott = [g for g, d in pont if d >= DICE_MIN and szocsalad_g(g, vers_tok) & szocsalad_g(pont[0][0], vers_tok)]
            masodik = next((d for g, d in pont if g not in valasztott), 0)
            if masodik and pont[0][1] < DICE_ARANY * masodik:
                valasztott = []
        tok = [t for t in vers_tok if ('G%04d' % int(t['strong'])) in valasztott]
        lemmak = list(dict.fromkeys(t['lemma'] for t in tok))
        csaladok = [szocsalad(l) for l in lemmak]
        egy = bool(lemmak) and all(csaladok[0] & c for c in csaladok[1:])
        prov = ('scope=%s lánc-szó %s %s | forras=LXX_OS (lxx-morph, CC BY 4.0) + LXX_versszintu_parok.tsv (a héber '
                'szó versszintű párjai, Dice ≥ %.2f, %.0f×-os különbség) | ts=%s' % (a.motivum, strong, hely, DICE_MIN,
                                                                            DICE_ARANY, ma()))
        r = {'motivum': a.motivum, 'strong': strong, 'igehely': hely, 'forras': 'lxx', 'betoldas': 'nem',
             'kinyeres': 'gepi', 'modell': '', 'proveniencia': prov, 'jelentes': '', 'megjegyzes': ''}
        if egy:
            alak = ' · '.join(dict.fromkeys(t['szoalak'] for t in tok))
            r.update(alak=alak, lemma=' · '.join(lemmak),
                     kiejtes=' · '.join(LG.gorog_magyaros(LG.gepi_atiras(x)) for x in lemmak),
                     jelentes=' · '.join(LG.rovid_jelentes('G%04d' % int(tok[[t['lemma'] for t in tok].index(l)]['strong']))[0]
                                         for l in lemmak),
                     ellenorzes='gépi: a versben egyetlen lemma (vagy szócsalád) társul egyértelműen a héber '
                                'szóval, %s' % ma())
        else:
            r.update(alak='', lemma='', kiejtes='', ellenorzes='',
                     megjegyzes=('a gépi kinyerés nem egyértelmű: %s' % ', '.join(
                         '%s %.2f' % (next((t['lemma'] for t in vers_tok if ('G%04d' % int(t['strong'])) == g), g), d)
                         for g, d in pont[:3])))
        uj.append(r)
    tabla_ir(uj)
    return 0


def ellenoriz(_a):
    hibak = []
    with open(TABLA, encoding='utf-8') as f:
        nyers = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    if not nyers or nyers[0].split('\t') != OSZLOPOK:
        hibak.append('a fejléc nem a séma szerinti')
    for i, s in enumerate(nyers[1:], 2):
        if len(s.split('\t')) != len(OSZLOPOK):
            hibak.append('%d. sor: oszlopszám %d' % (i, len(s.split('\t'))))
    sorok = tsv_olvas(TABLA)
    if len({kulcs(r) for r in sorok}) != len(sorok):
        hibak.append('a kulcs nem egyedi')
    for r in sorok:
        if r['forras'] not in FORRASOK or r['kinyeres'] not in KINYERES or r['betoldas'] not in ('igen', 'nem', ''):
            hibak.append('zárt érték: %s' % (kulcs(r),))
        if not r['proveniencia'].startswith('scope=') or 'ts=' not in r['proveniencia']:
            hibak.append('proveniencia: %s' % (kulcs(r),))
        if r['kinyeres'] == 'modell' and not r['modell']:
            hibak.append('modell-kinyerés modellnév nélkül: %s' % (kulcs(r),))
    for h in hibak:
        print('HIBA:', h)
    print('visszhang_megfelelok.tsv: %d sor, %d hiba' % (len(sorok), len(hibak)))
    return 1 if hibak else 0


def main():
    ap = argparse.ArgumentParser(description='a visszhang-blokk kinyerő táblája (F178.5)')
    al = ap.add_subparsers(dest='parancs', required=True)
    b = al.add_parser('beolvas')
    b.add_argument('kinyert')
    b.add_argument('--lemma-javitas', default=None)
    b.add_argument('--atnezes', default=None, help='az ellenőr soronkénti kézi ítélete (motivum, strong, igehely, forras, '
                   'alak, atnezo, itelet=jo|elvet, megjegyzes); csak az itt jóváhagyott sor ellenőrzött')
    b.add_argument('--lemma-megerosites', default=None, help='az ellenőri lemma-egységesítés megerősítése egy harmadik '
                   'kéztől (motivum, strong, igehely, forras, lemma_a_tablaban, itelet, javasolt_lemma, modell, indok)')
    b.add_argument('--ellenor', required=True, help='az ellenőrző tényleges modellneve (nem a kinyerőé)')
    x = al.add_parser('lxx')
    x.add_argument('--motivum', required=True)
    al.add_parser('ellenoriz')
    a = ap.parse_args()
    return {'beolvas': beolvas, 'lxx': lxx, 'ellenoriz': ellenoriz}[a.parancs](a)


if __name__ == '__main__':
    sys.exit(main())
