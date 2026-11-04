#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indoklas_szetvalaszt.py -- a `jeloltek.tsv` `indoklas` mezőjének szétválasztása (F123.INDOKLAS).

Az `indoklas` a munkafolyamat naplója is volt: döntés-azonosítót (DT/N/F), fájlnevet, `manual` proveniencia-sort,
„gerinc”-et hordozott. A lapon ez az olvasónak érthetetlen, a nyílt adat kutatójának pedig a nyom maga az érték
(#86 terv 1.5, 1.7). Ezért nem törlés, hanem szétválasztás:

    indoklas    olvasható magyar szöveg: a döntés tartalma kimondva (pl. „csak ahol a név után JHVH áll”)
    dontes_ref  a gépi nyom: döntés-azonosító(k), hivatkozott fájl(ok), az indoklás proveniencia-sora(i), ` · `-tal

A belső jelet az `olvasoi_kapu.BELSO` mintái mérik (ugyanez a mérce az `ellenoriz.py` 31. szabályában). Az átírás
szabályalapú (ATIRAS) és soronként rögzített (KEZI: a szabályokkal nem kezelhető sorok szövege); a futás minden
érintett sorra igazolja, hogy
    1. az új `indoklas` nem hordoz belső jelet;
    2. az elutasítás oka a mintaszótár szerint (`szerep_kizart.elutasitas_oka`) ugyanaz, mint a régi szövegé;
    3. a kulcs (id + igehely + jelolt_tipus + cel_id) és a többi mező változatlan;
    4. a nem érintett sorok bájtra azonosak (az új oszlop üres).
Eltérésnél nem ír. A napló: `naplok/INDOKLAS_szetvalasztas.md` (régi → új, soronként).

Használat:
    python eszkozok/indoklas_szetvalaszt.py            # próba: csak kiírja az összesítést
    python eszkozok/indoklas_szetvalaszt.py --ir       # a tábla és a napló írása
TSV: split('\\t') / '\\t'.join(), csv modul nélkül (CLAUDE.md).
"""
import argparse
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import olvasoi_kapu as K       # noqa: E402
import szerep_kizart as SZKZ   # noqa: E402

TABLA = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
NAPLO = os.path.join(GYOKER, 'naplok', 'INDOKLAS_szetvalasztas.md')
UJ_OSZLOP = 'dontes_ref'
SEP = ' · '


def belso_jelek(szoveg):
    return [nev + ': ' + m.group(0) for rx, nev in K.BELSO for m in rx.finditer(szoveg or '')]


# --- a proveniencia-sorok kiemelése -----------------------------------------------------------------------------------
_P = r'scope=[^|]*?(?:\s\|\s(?!scope=)[a-z_]+=[^|]*?)*?\s\|\sts=[0-9T:Z.-]+(?:\s\|\scsatorna=[a-z_]+)?'
PROV = re.compile(r'(?:\s\|\s)?(?:(?:Károli-proveniencia \(lekerdez\.py karoli\)|Mérés \d{4}-\d{2}-\d{2}):\s)?'
                  + _P + r'(?:\s·\s' + _P + r')*')


def prov_ki(t, ref):
    def el(m):
        ref.append(m.group(0).lstrip(' |'))
        return ''
    return PROV.sub(el, t)


# --- szabályalapú átírás: (minta, csere, a nyomba kerülő szöveg vagy None = a találat maga) --------------------------
JHVH = 'A motívumba csak az a hely tartozik, ahol a besém után az Úr neve, a JHVH áll'
ATIRAS = [
    # DT478 / DT476 K4 (a JHVH-szabály)
    (r'^DT478 \(a felhasználó, 2026-11-01: „Csak ahol JHVH áll”; alkalmazásra jóváhagyva 2026-11-02: „Igen, mind”\): ',
     JHVH + ' (a felhasználó döntése, 2026-11-01: „Csak ahol JHVH áll”; az alkalmazását 2026-11-02-én '
     'jóváhagyta: „Igen, mind”): ', 'DT478'),
    (r'^DT478 \(a felhasználó, 2026-11-01: „Csak ahol JHVH áll”\): ',
     JHVH + ' (a felhasználó döntése, 2026-11-01: „Csak ahol JHVH áll”): ', 'DT478'),
    (r'^DT476 K4 és DT478 \(a felhasználó, 2026-11-01: „itt ez az elhatárolás”; „Csak ahol JHVH áll”\): ',
     JHVH + ' (a felhasználó döntése, 2026-11-01: „itt ez az elhatárolás”; „Csak ahol JHVH áll”): ',
     'DT476 K4' + SEP + 'DT478'),
    # DT476 K1, K2, K5
    (r'^DT476 K2 \(a felhasználó, 2026-11-01: („[^”]*”)\): ἐπικαλέομαι ὄνομα \(G3686\) nélkül; a név nélküli segítségül '
     r'hívás a tágabb körbe tartozik \(`motivumok\.tsv` `folerendelt_fogalom`\)',
     r'A név nélküli görög sorok nem tartoznak a motívumba (a felhasználó döntése, 2026-11-01: \1): a versben '
     r'ἐπικαλέομαι áll, de ὄνομα (G3686) nélkül; a név nélküli segítségül hívás a tágabb körbe, a motívum '
     r'fölérendelt fogalmához tartozik', 'DT476 K2' + SEP + 'motivumok.tsv folerendelt_fogalom'),
    (r'^DT476 K1 \(a felhasználó, 2026-11-01: („[^”]*”)\): ',
     r'A hely nem tartozik a motívumba (a felhasználó döntése, 2026-11-01: \1): ', 'DT476 K1'),
    (r'Kontraszt \(DT476 K5; a felhasználó, 2026-11-01: ', 'Kontraszt (a felhasználó döntése, 2026-11-01: ',
     'DT476 K5'),
    # DT479 (a motívumközi jelölt saját előfordulása)
    (r'^DT479 \(a felhasználó, 2026-11-01: „Igen, \(b\)”; a motívumközi rész az elfogadott javaslat \(i\) szerint\): '
     r'a (Róm 10:1[24]) a DT476 K2 óta nem ISTENTISZT-001-előfordulás, a motívumközi jelölt pedig az `id` motívum '
     r'előfordulásán áll \(SEMA 2\.4\)',
     r'A motívumközi jelölt csak a saját motívumának előfordulásán állhat (a felhasználó döntése, 2026-11-01: '
     r'„Igen, (b)”): a \1 2026-11-01 óta nem az ISTENTISZT-001 előfordulása (a vers kikerült a motívumból)',
     'DT479' + SEP + 'DT476 K2' + SEP + 'SEMA 2.4'),
    # DT280 (a pilot motívumközi jelöltjei)
    (r'(^| \| korábban \(nyitva, 2026\.10\.20\): )DT280 \(felhasználó, 2026-10-20, chat\): ',
     r'\1A felhasználó döntése (2026-10-20): ', 'DT280'),
    (r'nyitva: az alponthoz kötött jelölt a DT277 \(C\) szerint, amíg az ALVIL-001 alpontjának nincs adatbeli '
     r'azonosítója \(a #123 ALVIL-001-ciklusa vezeti be\)\.',
     'nyitva: az alponthoz kötött jelölt nyitva marad, amíg az ALVIL-001 alpontjának nincs adatbeli azonosítója (a '
     'motívumközi kapcsolat célja csak létező alpont-azonosító lehet; az azonosítót az ALVIL-001 feldolgozása vezeti '
     'be).', 'DT277 (C)' + SEP + '#123'),
    (r'↳ alpontja \(a #123 Seól-határ-döntése, DT-F123d\); az alpontnak még nincs adatbeli azonosítója, ezért a jelölt '
     r'a DT277 \(C\) szerint nyitva marad\.',
     '↳ alpontja (a Seól-határ döntése szerint); az alpontnak még nincs adatbeli azonosítója, ezért a jelölt nyitva '
     'marad.', 'DT-F123d (#123)' + SEP + 'DT277 (C)'),
    (r' \(felmérés: (naplok/PROZA_FELMERES_ISTENTISZT-001_20261019\.md \d\.)\)', '', None),
    (r'a célversek az ALVIL-001 tanulmányának 1\. táblájában a motívum gerincén állnak',
     'a célversek az ALVIL-001 tanulmányának 1. táblájában a motívum lexikai magján állnak', None),
    (r'beépítve egyoldalú értelmezés töltene ki hiányt \(CLAUDE\.md 3\. szabály\)',
     'beépítve egyoldalú értelmezés töltene ki hiányt, ezt pedig a módszer tiltja', 'CLAUDE.md 3. szabály'),
    (r'F1: három jelölt', 'Három jelölt', 'DT280 F1'),
    (r'Mért \(B2\): (?=Mért szomszédság)', '', None),
    (r'Mért \(B2\): ', 'Mért: ', None),
    # DT283 (F110: a G1941 / H7121+H8034 szűrő-szabály)
    (r'F110 szűrő \(DT283\), K1_passziv: passzív/megnevezett \(([^)]*)\)',
     lambda m: 'A szűrő-szabály szerint passzív vagy megnevező alak (a görög ige tükörfordítása: „%s”)'
     % ANGOL_HU[m.group(1)], 'F110' + SEP + 'DT283 K1'),
    (r'F110 szűrő \(DT283\), K3_jogi: jogi fellebbezés: Kaisar/Szebasztosz a környezetben \(([^)]*)\)',
     lambda m: 'A szűrő-szabály szerint jogi fellebbezés: a környezetben a császár (Kaisar/Szebasztosz) áll (a görög '
     'ige tükörfordítása: „%s”)' % ANGOL_HU[m.group(1)], 'F110' + SEP + 'DT283 K3'),
    (r'F110 szűrő \(DT283\), ([AB]) osztály, kézi olvasás: ',
     lambda m: 'A szűrő-szabály %s osztálya (%s), kézi olvasással: ' % (m.group(1), OSZTALY[m.group(1)]),
     'F110' + SEP + 'DT283'),
    (r'Döntés \(felhasználó, 2026-10-29, orkesztrátor-chat, szó szerint: ',
     'Döntés (a felhasználó, 2026-10-29, szó szerint: ', 'orkesztrátor-chat 2026-10-29'),
    (r'A szabály átengedi; elbírálatlan, a motívum-menet dönt', 'A szabály átengedi; elbírálatlan, a motívum '
     'feldolgozása dönt', None),
    # N59 (Zsolt 99:6)
    (r'^N59, kézi olvasás: ', 'Kézi olvasás (a lefedetlen helyek vizsgálata): ', 'N59'),
    (r'\(adat/motivumok\.tsv: ', '(a motívum negatív kritériuma: ', 'motivumok.tsv negativ_kriterium'),
    (r'Előzmény: DT283 \(', 'Előzmény: a szűrő-szabály döntése (', 'DT283'),
    # DT542 (HAMART-001 X.A)
    (r'kollokáció \(1Móz 3:18 gerinc-pár\)', 'kollokáció (az 1Móz 3:18 lexikai szópárja)', None),
    (r'; F123 X\.A \(DT542\), elbírálatlan$', '; a negatív kritérium mérhető kitételének új helyeként felvéve '
     '(2026-11-02), elbírálatlan', 'F123 X.A' + SEP + 'DT542'),
    # DT588 (ANTROP-001 U3)
    (r' — 2026-11-03 \(F123 ANTROP-001 új cikk, U3; DT588 \(4\)\): a sor kapcsolodas és funkcio mezője nulláról '
     r'újraírva, a régi szöveg archívumban \((archivum/ANTROP-001/ANTROP-001_1a_proza_regi\.tsv)\); döntés: '
     r'beépítve, a hely és a gerinc-elem nem változott\.',
     ' — 2026-11-03: a hely kapcsolódás-leírása és funkciója a cikk új kiadásához újraírva, a régi szöveg '
     'archívumban; döntés: beépítve, a hely és a lexikai mag eleme, amelyen áll, nem változott.',
     'F123 ANTROP-001 U3' + SEP + 'DT588 (4)' + SEP + 'archivum/ANTROP-001/ANTROP-001_1a_proza_regi.tsv'),
    (r'A negatív kritérium név szerinti kivétele \(DT588 \(1\)\): ',
     'A negatív kritérium név szerinti kivétele (a 2026-11-03-i döntés): ', 'DT588 (1)'),
    # DT184, F108
    (r'^F108 újrascan: a hely a mai TAHOT/TAGNT-on gerinc-Strongot hordoz, de sem az elofordulasok\.tsv-ben, sem a '
     r'jeloltek\.tsv-ben nem szerepelt; elbírálatlan \(DT184\)',
     'A motívum újrakeresése szerint a hely a mai héber és görög szövegben (TAHOT/TAGNT) a motívum lexikai magjának '
     'egyik szavát hordozza, de sem az előfordulások, sem a jelöltek között nem szerepelt; elbírálatlan',
     'F108' + SEP + 'DT184' + SEP + 'elofordulasok.tsv' + SEP + 'jeloltek.tsv'),
    (r' DT184\.$', '', 'DT184'),
    # F87, F114 (javítási jegyzetek)
    (r' \[F87: (igehely és karoli_szo|karoli_szo|igehely) javítva, l\. (naplok/KAROLI_ELTERES_ITELET_zaras\.md)\]',
     lambda m: ' (Javítva a Károli-eltérések ellenőrzésekor: %s.)' % JAVITVA[m.group(1)],
     'F87' + SEP + 'naplok/KAROLI_ELTERES_ITELET_zaras.md'),
    (r' \[F114: igehely javítva, a TSK KJV-kulcsa volt \(([^)]*)\), DT199, l\. naplok/TSK_VERSSZAM_felmeres\.md C\. '
     r'rész\]',
     r' (Az igehely javítva: a TSK az angol, KJV-versszámozás szerint adta meg, \1.)',
     'F114' + SEP + 'DT199' + SEP + 'naplok/TSK_VERSSZAM_felmeres.md C. rész'),
    # N-F63a
    (r'de az elofordulasok\.tsv-ben nincs sor;', 'de az előfordulások között nincs;', 'elofordulasok.tsv'),
    (r'de a jeloltek\.tsv-ben és az elofordulasok\.tsv-ben nincs sor;', 'de sem a jelöltek, sem az előfordulások '
     'között nincs;', 'jeloltek.tsv' + SEP + 'elofordulasok.tsv'),
    (r'; elbírálás: N-F63a$', '; az elbírálása nyitott kérdés', 'N-F63a'),
    # gerinc
    (r'a jelen gerinchez nem tartozik', 'a motívum jelenlegi lexikai magjához nem tartozik', None),
    # fájlnevek a szövegben
    (r' \(adat/thayer_szakaszok\.tsv, (G4151 -/2/-, G5590 -/2/-)\)', '',
     'adat/thayer_szakaszok.tsv G4151 -/2/-, G5590 -/2/-'),
    (r' \(l\. adat/motivumok\.tsv HODIT-001 sora\)', '', 'motivumok.tsv HODIT-001'),
    (r'a TAHOT_kivonat\.tsv szerint', 'a héber szöveg (TAHOT) szerint', 'TAHOT_kivonat.tsv'),
    (r'külön elofordulasok-sorként bekerült', 'külön előfordulásként bekerült', None),
    (r'a negatív kritérium \(motivumok\.tsv\) kizárja', 'a motívum negatív kritériuma kizárja',
     'motivumok.tsv negativ_kriterium'),
    (r'\(motivumok\.tsv, fölérendelt fogalom\)', '(a motívum fölérendelt fogalma felé)',
     'motivumok.tsv folerendelt_fogalom'),
    (r', l\. ((?:Isten_fiai_Nefilim_Gibborim|Rafaim)_kereszthivatkozas_naplo\.md)$', '', None),
    (r'^A study \(Segitsegul_hivni_az_Urat_tematikus\.md\) kapcsolat-táblája szerint a Jóel 2:32 szó szerinti '
     r'LXX-idézete',
     'A tematikus tanulmány kapcsolat-táblája szerint a Jóel 2:32 szó szerinti Septuaginta-idézete',
     'Segitsegul_hivni_az_Urat_tematikus.md'),
    (r'; az F3\.1 betöltés a Jóel 2:32 sorba vonta össze', '; az első adatbetöltés a Jóel 2:32 sorába vonta össze',
     'F3.1'),
    # a „study” angol szó (az olvasói kapu ANGOL-szabálya), ahol a sort amúgy is átírjuk
    (r'\bstudy\b', 'tanulmány', None),
]

# a TAGNT angol tükörfordításának magyar megfelelője (a fordítás a görög alak értelme, nem a Károli szövege)
ANGOL_HU = {'was called': 'hívták', 'having been called': 'akit hívtak', 'is called': 'hívják',
            'is being called': 'hívják', 'has been called': 'hívattatott', 'to be called': 'hívattatni',
            'I appeal!': 'fellebbezek!', 'You have appealed,': 'fellebbeztél', 'having appealed for': 'fellebbezve',
            'having appealed to': 'fellebbezve', 'he had appealed': 'fellebbezett', 'to appeal to': 'fellebbezni'}
OSZTALY = {'A': 'aktív ige, isteni névvel', 'B': 'aktív ige, isteni név nélkül'}
JAVITVA = {'igehely és karoli_szo': 'az igehely és a Károli-szóalak', 'karoli_szo': 'a Károli-szóalak',
           'igehely': 'az igehely'}


def atir(indoklas):
    """(új indoklás, dontes_ref) a szabályok szerint."""
    ref = []
    t = indoklas
    # a proveniencia-sorok a szabályok előtt kerülnek a nyomba, hogy a „ | korábban” bevezetés a szöveghez érjen
    t = prov_ki(t, ref)
    for minta, csere, nyom in ATIRAS:
        rx = re.compile(minta)
        m = rx.search(t)
        if not m:
            continue
        # a nyom: a szabály megnevezett hivatkozása, vagy (None) a minta első csoportja, ha az fájlt / helyet rögzít
        if nyom:
            ref.extend(x for x in nyom.split(SEP) if x not in ref)
        elif m.groups() and m.group(1) and belso_jelek(m.group(1)):
            ref.append(m.group(1))
        t = rx.sub(csere, t)
    if re.search(r'\bgerinc', indoklas, re.I):
        ref.append('gerinc')   # a belső szó maga is nyom: a motívum Strong-magja (CLAUDE.md, kutatási menet 1.)
    t = re.sub(r'\s{2,}', ' ', t).strip()
    return t, ref


# az elutasítás okát a fő ág mintaszótára és a párhuzamos ágak változata (OKOK_EXTRA, ha megadva) szerint is mérjük
OKOK_TABLAK = [SZKZ.OKOK] + [x for x in os.environ.get('OKOK_EXTRA', '').split(os.pathsep) if x]


def ok_mint(indoklas, minta):
    """Az elutasítás oka az indoklás fő részéből (a ` | ` előtti szöveg, ahogy a generátor olvassa)."""
    try:
        return SZKZ.elutasitas_oka(indoklas.partition(' | ')[0], minta)
    except ValueError:
        return 'BE NEM SOROLHATÓ'


def beolvas():
    with io.open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()
    return nyers.split('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    sorok = beolvas()
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].rstrip('\r').split('\t')
    if UJ_OSZLOP in fej:
        print('a(z) %s oszlop már megvan: nincs teendő' % UJ_OSZLOP)
        return 0
    i_ind = fej.index('indoklas')
    uj_sorok = list(sorok)
    uj_sorok[fej_i] = '\t'.join(fej + [UJ_OSZLOP]) + ('\r' if sorok[fej_i].endswith('\r') else '')
    naplo, hibak = [], []
    for i in range(fej_i + 1, len(sorok)):
        s = sorok[i]
        if not s.strip() or s.startswith('#'):
            continue
        cr = '\r' if s.endswith('\r') else ''
        m = s.rstrip('\r').split('\t')
        m += [''] * (len(fej) - len(m))
        d = dict(zip(fej, m))
        regi = m[i_ind]
        if not belso_jelek(regi):
            uj_sorok[i] = '\t'.join(m + ['']) + cr
            continue
        uj, ref = atir(regi)
        if belso_jelek(uj):
            hibak.append('%d. sor (%s %s): belső jel maradt: %s' % (i + 1, d['id'], d['igehely'],
                                                                     '; '.join(belso_jelek(uj))))
        if d['dontes'] == 'elutasítva':
            for ut in OKOK_TABLAK:
                minta = SZKZ.okok(d['id'], ut)
                ok_regi, ok_uj = ok_mint(regi, minta), ok_mint(uj, minta)
                if ok_regi != ok_uj:
                    hibak.append('%d. sor (%s %s): az elutasítás oka változna (%s): %r -> %r'
                                 % (i + 1, d['id'], d['igehely'], os.path.basename(ut), ok_regi, ok_uj))
        # a régi szöveg minden belső jele a nyomban van (a nyom nem vész el)
        for rx, _nev in K.BELSO:
            for x in rx.finditer(regi):
                if x.group(0).lower() not in SEP.join(ref).lower():
                    hibak.append('%d. sor (%s %s): a belső jel nem került a nyomba: %s'
                                 % (i + 1, d['id'], d['igehely'], x.group(0)))
        if '\t' in uj or '\t' in ''.join(ref):
            hibak.append('%d. sor: tab a szövegben' % (i + 1))
        m2 = list(m)
        m2[i_ind] = uj
        uj_sorok[i] = '\t'.join(m2 + [SEP.join(ref)]) + cr
        # 3. igazolás: minden más mező változatlan
        vissza = uj_sorok[i].rstrip('\r').split('\t')
        if vissza[:i_ind] + vissza[i_ind + 1:len(fej)] != m[:i_ind] + m[i_ind + 1:]:
            hibak.append('%d. sor: más mező is változott' % (i + 1))
        naplo.append((i + 1, d, regi, uj, SEP.join(ref)))
    # 4. igazolás: a nem érintett sorok csak az üres új oszloppal bővültek
    erintett = {n - 1 for n, *_ in naplo}
    for i in range(fej_i + 1, len(sorok)):
        if i in erintett or not sorok[i].strip() or sorok[i].startswith('#'):
            if not (i in erintett) and uj_sorok[i] != sorok[i]:
                hibak.append('%d. sor: megjegyzés/üres sor változott' % (i + 1))
            continue
        if uj_sorok[i].rstrip('\r') != sorok[i].rstrip('\r') + '\t' * (len(fej) - len(sorok[i].rstrip('\r').split('\t')) + 1):
            hibak.append('%d. sor: nem érintett sor változott' % (i + 1))
    print('érintett sor: %d; hiba: %d' % (len(naplo), len(hibak)))
    for h in hibak:
        print('  HIBA: ' + h)
    if hibak:
        return 1
    if not args.ir:
        for n, d, regi, uj, ref in naplo:
            print('\n%d %s %s (%s)\n  ÚJ:  %s\n  REF: %s' % (n, d['id'], d['igehely'], d['dontes'], uj, ref))
        return 0
    with io.open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj_sorok))
    naplo_ir(naplo)
    print('írva: %s, %s' % (os.path.relpath(TABLA, GYOKER), os.path.relpath(NAPLO, GYOKER)))
    return 0


def naplo_ir(naplo):
    ki = ['# Az `indoklas` szétválasztása (F123.INDOKLAS)', '',
          '*Generálta: `eszkozok/indoklas_szetvalaszt.py --ir`. A `adat/jeloltek.tsv` `indoklas` mezőjéből a belső jel '
          '(az `olvasoi_kapu.BELSO` mintái szerint: döntés-azonosító, F-/N-tétel, fájlnév, `manual`, „gerinc”) az új '
          '`dontes_ref` oszlopba került; az `indoklas` olvasható szöveget kapott, amely a döntés tartalmát kimondja. '
          'Igazolva soronként: nincs belső jel az új szövegben; az elutasítás oka a mintaszótár szerint változatlan; '
          'a kulcs és a többi mező változatlan; a nem érintett sorok csak az üres új oszloppal bővültek.*', '',
          '*Proveniencia: `scope=adat/jeloltek.tsv (%d sor) | forras=manual (átírási szabályok: '
          'eszkozok/indoklas_szetvalaszt.py ATIRAS; a döntések szövege: DONTESEK.md) | ts=2026-11-04`*' % len(naplo), '']
    for n, d, regi, uj, ref in naplo:
        ki += ['## %d. sor — %s · %s · %s (%s)' % (n, d['id'], d['igehely'], d['jelolt_tipus'], d['dontes']), '',
               '- **régi `indoklas`:** %s' % regi.replace('\n', ' '),
               '- **új `indoklas`:** %s' % uj,
               '- **`dontes_ref`:** %s' % (ref or '—'), '']
    with io.open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki))


if __name__ == '__main__':
    sys.exit(main())
