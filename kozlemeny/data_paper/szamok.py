"""A data paper számai (F167.2): minden kéziratbeli szám ebből a lekérdezésből jön.

A számok a nyílt mag zárt, hash-elt csomagján futnak (`nyilt_mag/`), nem az élő
táblákon; kivétel az ellenőrzési lánc (kiadás, átnézés, lapjavítás, jelölt-döntés),
amely az adatrétegből (`adat/`) jön, és a teljesség-mérés, amely a naplók
összegző táblájából. Minden kimeneti sor elején a kézirat „Number provenance”
mellékletének kulcsa áll.

Futtatás: python kozlemeny/data_paper/szamok.py
"""
import hashlib
import os
import re
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAG = os.path.join(GYOKER, 'nyilt_mag')
ADAT = os.path.join(GYOKER, 'adat')
NAPLOK = os.path.join(GYOKER, 'naplok')

USZ_KONYVEK = {
    'Mt', 'Mk', 'Lk', 'Luk', 'Jn', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef',
    'Fil', 'Kol', '1Thessz', '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak',
    '1Pét', '2Pét', '1Ján', '2Ján', '3Ján', 'Júd', 'Jel',
}


def tabla(ut):
    """TSV olvasása split('\\t')-vel (a csv modul ezeken a táblákon adatot ront)."""
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def ki(kulcs, ertek, forras):
    print(f'{kulcs}\t{ertek}\t{forras}')


def konyv(igehely):
    return igehely.split(' ')[0]


def main():
    with open(os.path.join(MAG, 'KIADAS.txt'), encoding='utf-8') as f:
        kiadas = dict(s.strip().split(': ', 1) for s in f if ': ' in s)
    ki('P0.kiadas', kiadas['kiadas_azonosito'], 'nyilt_mag/KIADAS.txt')

    # P1 — motívumok
    mot = tabla(os.path.join(MAG, 'motivumok.tsv'))
    ki('P1.motivum', len(mot), 'nyilt_mag/motivumok.tsv, sorok')
    for k, v in sorted(Counter(m['statusz'] for m in mot).items()):
        ki('P1.statusz', f'{k}={v}', 'nyilt_mag/motivumok.tsv, statusz')
    for k, v in sorted(Counter(m['azonossag_tipusa'] for m in mot).items()):
        ki('P1.azonossag', f'{k}={v}', 'nyilt_mag/motivumok.tsv, azonossag_tipusa')
    ures_neg = sum(1 for m in mot if not m['negativ_kriterium'].strip())
    ures_fol = sum(1 for m in mot if not m['folerendelt_fogalom'].strip())
    ki('P1.ures_negativ_kriterium', ures_neg, 'nyilt_mag/motivumok.tsv, negativ_kriterium üres')
    ki('P1.ures_folerendelt', ures_fol, 'nyilt_mag/motivumok.tsv, folerendelt_fogalom üres')
    allapot = {m['motivum_azonosito']: m['feldolgozasi_allapot'] for m in mot}
    for k, v in sorted(Counter(allapot.values()).items()):
        tagok = ', '.join(sorted(i for i, a in allapot.items() if a == k))
        ki('P1.feldolgozasi_allapot', f'{k}={v} ({tagok})', 'nyilt_mag/motivumok.tsv, feldolgozasi_allapot')

    # P2 — előfordulások
    elo = tabla(os.path.join(MAG, 'elofordulasok.tsv'))
    ki('P2.elofordulas_sor', len(elo), 'nyilt_mag/elofordulasok.tsv, sorok')
    usz = sum(1 for e in elo if konyv(e['igehely']) in USZ_KONYVEK)
    ki('P2.osz_sor', len(elo) - usz, 'nyilt_mag/elofordulasok.tsv, igehely könyve nem ÚSZ')
    ki('P2.usz_sor', usz, 'nyilt_mag/elofordulasok.tsv, igehely könyve ÚSZ')
    for k, v in sorted(Counter(e['motivum_azonosito'] for e in elo).items()):
        ki('P2.motivumonkent', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, motivum_azonosito')
    for k, v in sorted(Counter(allapot[e['motivum_azonosito']] for e in elo).items()):
        ki('P2.allapot_szerint', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv × motivumok.tsv, feldolgozasi_allapot')
    kezi = sum(1 for e in elo if e['lekerdezes_tipusa'].startswith('kézi döntés'))
    ki('P2.kezi_dontes', kezi, 'nyilt_mag/elofordulasok.tsv, lekerdezes_tipusa = „kézi döntés, lekérdezés nélkül”')
    ki('P2.lekerdezesbol', len(elo) - kezi, 'nyilt_mag/elofordulasok.tsv, lekerdezes_tipusa egyéb')
    ures_lek = sum(1 for e in elo if not e['lekerdezes_tipusa'].strip())
    ki('P2.ures_lekerdezes_tipusa', ures_lek, 'nyilt_mag/elofordulasok.tsv, lekerdezes_tipusa üres')
    for k, v in sorted(Counter(e['azonositas_modja'] or '(üres)' for e in elo).items()):
        ki('P2.azonositas_modja', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, azonositas_modja')
    for k, v in sorted(Counter(e['igazolas'] or '(üres)' for e in elo).items()):
        ki('P2.igazolas', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, igazolas')
    for k, v in sorted(Counter(e['horgony_tipus'] or '(üres)' for e in elo).items()):
        ki('P2.horgony_tipus', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, horgony_tipus')
    for k, v in sorted(Counter(e['pardes_szint'] or '(üres)' for e in elo).items()):
        ki('P2.pardes_szint', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, pardes_szint')

    for k, v in sorted(Counter(e['megbizhatosag'] or '(üres)' for e in elo).items()):
        ki('P2.megbizhatosag', f'{k}={v}', 'nyilt_mag/elofordulasok.tsv, megbizhatosag')
    ki('P2.karoli_szo_kitoltve', sum(1 for e in elo if e['karoli_szo'].strip()),
       'nyilt_mag/elofordulasok.tsv, karoli_szo nem üres')

    # P9 — a magyar olvasói réteg: a seól/hádész Károli-fordításai (ALVIL-001)
    alvil = [e for e in elo if e['motivum_azonosito'] == 'ALVIL-001']
    for tő in ('sír', 'koporsó', 'pokol', 'seol', 'mélység', 'alvilág'):
        n = sum(1 for e in alvil if tő in e['karoli_szo'].lower())
        ki('P9.alvil_karoli', f'{tő}={n}',
           'nyilt_mag/elofordulasok.tsv, ALVIL-001, karoli_szo kisbetűs részszöveg-egyezés')

    # P10 — a Károli-réteg mint vizsgálati tárgy (F171): kitöltöttség, alakváltozatok, fordítói eljárás
    for k in sorted({e['motivum_azonosito'] for e in elo}):
        sorok = [e for e in elo if e['motivum_azonosito'] == k]
        ki('P10.karoli_motivumonkent', f'{k}={sum(1 for e in sorok if e["karoli_szo"].strip())}/{len(sorok)}',
           'nyilt_mag/elofordulasok.tsv, karoli_szo nem üres / sor')
    egy_strong = Counter(e['strong'] for e in elo
                         if e['karoli_szo'].strip() and e['strong'].strip() and '+' not in e['strong'])
    for s, n in egy_strong.most_common():
        if n < 5:
            continue
        alakok = {e['karoli_szo'].strip().lower() for e in elo
                  if e['strong'] == s and e['karoli_szo'].strip()}
        ki('P10.alak_strongonkent', f'{s}={n} sor / {len(alakok)} különböző alak',
           'nyilt_mag/elofordulasok.tsv, egyetlen Strong-szám, karoli_szo kisbetűsítve (szóalak a versből, nem szótő)')

    def resz(strong, minta):
        return sum(1 for e in elo if e['strong'] == strong and minta(e['karoli_szo'].lower()))

    atiras = lambda s: any(t in s for t in ('réfaim', 'refaim', 'refáim', 'refeus'))
    ki('P10.H7497', f'átírás={resz("H7497", atiras)}; ebből völgy={resz("H7497", lambda s: atiras(s) and "völgy" in s)}; '
       f'óriás={resz("H7497", lambda s: "óriás" in s)}',
       'nyilt_mag/elofordulasok.tsv, H7497, karoli_szo: Réfaim/Refaim/Refáim/Refeus vs óriás')
    ki('P10.H7497_irasmod', ', '.join(sorted({t for e in elo if e['strong'] == 'H7497'
                                              for t in ('Réfaim', 'Refaim', 'Refáim', 'Refeus')
                                              if t in e['karoli_szo']})),
       'nyilt_mag/elofordulasok.tsv, H7497, karoli_szo: az átírás írásmódjai')
    ki('P10.H7496', f'árny={resz("H7496", lambda s: "árny" in s)}; élet nélkül={resz("H7496", lambda s: "élet nélkül" in s)}; '
       f'halott={resz("H7496", lambda s: "halott" in s)}',
       'nyilt_mag/elofordulasok.tsv, H7496, karoli_szo részszöveg')
    ki('P10.H8415', f'mély-={resz("H8415", lambda s: "mély" in s)}; más={resz("H8415", lambda s: "mély" not in s)}',
       'nyilt_mag/elofordulasok.tsv, H8415, karoli_szo: „mély” részszöveg vs egyéb')
    ki('P10.G0086', f'pokol={resz("G0086", lambda s: "pokol" in s)}; sír={resz("G0086", lambda s: "sír" in s)}',
       'nyilt_mag/elofordulasok.tsv, G0086, karoli_szo részszöveg')
    gep = [e for e in elo if e['azonositas_modja'] in ('szó-szintű-gépi', 'kikövetkeztetett')]
    ki('P10.gepi_vagy_kovetkeztetett', f'{len(gep)} sor ({len({e["motivum_azonosito"] for e in gep})} motívum)',
       'nyilt_mag/elofordulasok.tsv, azonositas_modja = szó-szintű-gépi vagy kikövetkeztetett')

    # P3 — kizárások
    kiz = tabla(os.path.join(MAG, 'kizarasok.tsv'))
    csop = tabla(os.path.join(MAG, 'kizaras_csoportok.tsv'))
    egyedi = [k for k in kiz if not k['csoport_versszam'].strip()]
    osszesito = [k for k in kiz if k['csoport_versszam'].strip()]
    csop_vers = sum(int(k['csoport_versszam']) for k in osszesito)
    ki('P3.kizaras_sor', len(kiz), 'nyilt_mag/kizarasok.tsv, sorok')
    ki('P3.egyedi_sor', len(egyedi), 'nyilt_mag/kizarasok.tsv, csoport_versszam üres')
    ki('P3.osszesito_sor', len(osszesito), 'nyilt_mag/kizarasok.tsv, csoport_versszam kitöltve')
    ki('P3.csoport_vers', csop_vers, 'nyilt_mag/kizarasok.tsv, csoport_versszam összege')
    ki('P3.csoport_tabla_sor', len(csop), 'nyilt_mag/kizaras_csoportok.tsv, sorok')
    ki('P3.kizart_vers_osszesen', len(egyedi) + csop_vers,
       'egyedi sor + csoport_versszam összege')
    for k, v in sorted(Counter(k['jelolt_tipus'] for k in kiz).items()):
        ki('P3.jelolt_tipus', f'{k}={v}', 'nyilt_mag/kizarasok.tsv, jelolt_tipus')
    for k, v in Counter(k['keresesi_mod'] or '(üres)' for k in kiz).most_common():
        ki('P3.keresesi_mod', f'{k}={v}', 'nyilt_mag/kizarasok.tsv, keresesi_mod')
    tagok = Counter((c['motivum_azonosito'], c['csoport_sor_igehely']) for c in csop)
    tag_nelkul = [k for k in osszesito if tagok[(k['motivum_azonosito'], k['igehely'])] == 0]
    ki('P3.osszesito_tag_nelkul',
       f'{len(tag_nelkul)} sor / {sum(int(k["csoport_versszam"]) for k in tag_nelkul)} vers '
       f'({", ".join(sorted({k["motivum_azonosito"] for k in tag_nelkul}))})',
       'nyilt_mag/kizarasok.tsv összesítő sorai, amelyeknek nincs tagja a kizaras_csoportok.tsv-ben')
    okok = Counter()
    okok_vers = Counter()
    for k in kiz:
        ok = k['kizaras_oka'].replace(' (összesítő sor)', '').strip() or '(üres)'
        okok[ok] += 1
        okok_vers[ok] += int(k['csoport_versszam']) if k['csoport_versszam'].strip() else 1
    for ok, n in okok.most_common():
        ki('P3.ok', f'{ok}={n} sor / {okok_vers[ok]} vers',
           'nyilt_mag/kizarasok.tsv, kizaras_oka („ (összesítő sor)” levágva)')
    for k, v in sorted(Counter(k['motivum_azonosito'] for k in kiz).items()):
        vers = sum(int(x['csoport_versszam']) if x['csoport_versszam'].strip() else 1
                   for x in kiz if x['motivum_azonosito'] == k)
        ki('P3.motivumonkent', f'{k}={v} sor / {vers} vers', 'nyilt_mag/kizarasok.tsv')

    # P4 — beépítési döntések, kapcsolatok, döntésnapló, kódkönyv, domén
    bee = tabla(os.path.join(MAG, 'beepitesi_dontesek.tsv'))
    ki('P4.beepitesi_dontes', len(bee), 'nyilt_mag/beepitesi_dontesek.tsv, sorok')
    for k, v in sorted(Counter(b['jelolt_tipus'] for b in bee).items()):
        ki('P4.beepites_tipus', f'{k}={v}', 'nyilt_mag/beepitesi_dontesek.tsv, jelolt_tipus')
    ures_ind = sum(1 for b in bee if not b['indoklas'].strip())
    ki('P4.beepites_ures_indoklas', ures_ind, 'nyilt_mag/beepitesi_dontesek.tsv, indoklas üres')
    ures_kiz = sum(1 for k in kiz if not k['indoklas'].strip())
    ki('P4.kizaras_ures_indoklas', ures_kiz, 'nyilt_mag/kizarasok.tsv, indoklas üres')
    for nev in ('kapcsolatok', 'motivum_kapcsolatok', 'dontesnaplo', 'kodkonyv'):
        ki(f'P4.{nev}', len(tabla(os.path.join(MAG, nev + '.tsv'))), f'nyilt_mag/{nev}.tsv, sorok')
    dom = tabla(os.path.join(MAG, 'cc_by_sa_reteg', 'szemantikai_domenek.tsv'))
    ki('P4.domen_sor', len(dom), 'nyilt_mag/cc_by_sa_reteg/szemantikai_domenek.tsv, sorok')

    # P5 — források és licencek
    forr = tabla(os.path.join(MAG, 'forrasok_es_licencek.tsv'))
    ki('P5.forras_sor', len(forr), 'nyilt_mag/forrasok_es_licencek.tsv, sorok')
    for k, v in sorted(Counter(f['szerepe_a_csomagban'] for f in forr).items()):
        ki('P5.szerep', f'{k}={v}', 'nyilt_mag/forrasok_es_licencek.tsv, szerepe_a_csomagban')
    for k, v in Counter(f['ok'] for f in forr if f['szerepe_a_csomagban'] == 'kizárva').most_common():
        ki('P5.kizart_ok', f'{k}={v}', 'nyilt_mag/forrasok_es_licencek.tsv, szerep = kizárva, ok')
    hasznalt = [f['dataset'] + ' (' + f['licenc'] + ')' for f in forr
                if f['szerepe_a_csomagban'].startswith('forrás')]
    ki('P5.hasznalt_forras', '; '.join(hasznalt), 'nyilt_mag/forrasok_es_licencek.tsv, szerep = forrás')

    # P6 — csomag-fájlok
    fajlok = []
    for gy, _, nevek in os.walk(MAG):
        fajlok += [os.path.relpath(os.path.join(gy, n), MAG) for n in nevek]
    ki('P6.fajl', len(fajlok), 'nyilt_mag/ fájljai (rekurzívan)')
    meret = 0
    for f in fajlok:
        with open(os.path.join(MAG, f), 'rb') as g:
            meret += len(g.read().replace(b'\r\n', b'\n'))
    ki('P6.meret_bajt', meret, 'nyilt_mag/ fájlméret összege, LF-re normalizált bájtokon')
    datumok = []
    for nev in ('motivumok', 'elofordulasok', 'beepitesi_dontesek', 'kizarasok', 'kapcsolatok',
                'motivum_kapcsolatok', 'dontesnaplo'):
        for s in tabla(os.path.join(MAG, nev + '.tsv')):
            for mezo in ('datum', 'statusz_datum'):
                d = s.get(mezo, '').strip().replace('.', '-')
                if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
                    datumok.append(d)
    ki('P6.datum_tartomany', f'{min(datumok)} – {max(datumok)} ({len(datumok)} dátummező)',
       'nyilt_mag/*.tsv, datum és statusz_datum mezők')
    with open(os.path.join(MAG, 'ELLENORZO_OSSZEG.sha256'), encoding='utf-8') as f:
        osszegek = [s.split() for s in f if s.strip()]
    rossz = 0
    for h, nev in osszegek:
        with open(os.path.join(MAG, nev), 'rb') as g:
            # a csomag LF-sorvégű; Windows-checkouton (core.autocrlf) a .md CRLF lehet
            if hashlib.sha256(g.read().replace(b'\r\n', b'\n')).hexdigest() != h:
                rossz += 1
    ki('P6.sha256_ellenorzott', f'{len(osszegek)} fájl, {rossz} eltérés',
       'nyilt_mag/ELLENORZO_OSSZEG.sha256, LF-re normalizált bájtokon')

    # P7 — ellenőrzési lánc (adatréteg)
    kiad = tabla(os.path.join(ADAT, 'kiadasok.tsv'))
    ki('P7.kiadas_sor', len(kiad), 'adat/kiadasok.tsv, sorok')
    ki('P7.kiadott_motivum', ', '.join(sorted({k['id'] for k in kiad})), 'adat/kiadasok.tsv, id')
    for k, v in sorted(Counter(k['proza_modell'] for k in kiad).items()):
        ki('P7.proza_modell', f'{k}={v}', 'adat/kiadasok.tsv, proza_modell')
    atn = tabla(os.path.join(ADAT, 'lap_atnezesek.tsv'))
    ki('P7.atnezes_sor', len(atn), 'adat/lap_atnezesek.tsv, sorok')
    for k, v in sorted(Counter(a['id'] for a in atn).items()):
        ki('P7.atnezes_motivum', f'{k}={v}', 'adat/lap_atnezesek.tsv, id')
    jav = tabla(os.path.join(ADAT, 'lap_javitasok.tsv'))
    ki('P7.lapjavitas_sor', len(jav), 'adat/lap_javitasok.tsv, sorok')
    for k, v in sorted(Counter(j['gond'] for j in jav).items()):
        ki('P7.lapjavitas_gond', f'{k}={v}', 'adat/lap_javitasok.tsv, gond')
    for k, v in sorted(Counter(j['jovahagyta'] for j in jav).items()):
        ki('P7.lapjavitas_jovahagyta', f'{k}={v}', 'adat/lap_javitasok.tsv, jovahagyta')
    jel = tabla(os.path.join(ADAT, 'jeloltek.tsv'))
    mag_mot = {m['motivum_azonosito'] for m in mot}
    elo_jel = [j for j in jel if j['jelolt_tipus'] == 'elofordulas' and j['id'] in mag_mot]
    for k, v in sorted(Counter(j['dontes'] for j in elo_jel).items()):
        ki('P7.jelolt_dontes', f'{k}={v}',
           'adat/jeloltek.tsv, jelolt_tipus=elofordulas, a csomag 9 motívuma, dontes (sor, nem vers)')
    nyitva = sum(1 for j in jel if j['dontes'] == 'nyitva' and j['id'] in mag_mot)
    ki('P7.nyitva_minden_tipus', nyitva, 'adat/jeloltek.tsv, dontes=nyitva, a csomag motívumai, minden jelolt_tipus')

    # P8 — teljesség-mérés: a naplók 1. összegző táblája
    for m in ('ALVIL-001', 'ANTROP-001', 'HAMART-001', 'ISTENTISZT-001'):
        ut = os.path.join(NAPLOK, f'F123_teljesseg_{m}.md')
        with open(ut, encoding='utf-8') as f:
            szoveg = f.read()
        blokk = szoveg.split('## 1. Összegzés', 1)[1].split('\n## ', 1)[0]
        for s in blokk.splitlines():
            if not s.startswith('|'):
                continue
            cellak = [c.strip() for c in s.strip().strip('|').split('|')]
            if re.match(r'^(\d\.|fordított)', cellak[0]):
                halo = cellak[0].split(' (')[0]
                if halo.startswith('fordított'):
                    ki('P8.' + m, f'fordított irány (E-vers, amelyet egyik háló sem ad): {cellak[4].strip("*")}',
                       f'naplok/F123_teljesseg_{m}.md, 1. Összegzés')
                else:
                    ki('P8.' + m, f'{halo}: találat={cellak[1]}; E={cellak[2]}; '
                       f'ELTÉRÉS={cellak[4].strip("*")}; ebből motívum-jegy={cellak[5]}',
                       f'naplok/F123_teljesseg_{m}.md, 1. Összegzés')


if __name__ == '__main__':
    main()
