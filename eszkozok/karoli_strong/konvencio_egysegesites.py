#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V28 — konvenció-egységesítés: a Károli 1908 – Strong párosítás 1.1-es állapotának törlőlistája.

A döntés: DT-F175vr (dontesek/uj/johd-validacio-70cc1f.md; a végleges módszer). A párosítási prompt
(`f21p/prompt_v3.md`) A szabálya szerint a héber határozott névelő (H9009) és a görög névelő (G3588) `forditatlan`,
kivéve a névmási szerepet; a C szabály szerint a tárgyjelölő ʾet (H0853) `forditatlan`. A 2. szabályt (a H9xxx előtag a
ragos magyar szóhoz tartozik) a párosító modell a névelőre is alkalmazta. Az 1.1 a validáció előtt ezeket a
kapcsolatokat törli.

A szabály (egyetlen gépi kritérium, a pár rögzített jegyeiből: Strong-szám, magyar szó, a versben előtte és utána álló
magyar szó, a köztük álló írásjel):
  1. névelő (H9009, G3588): a kapcsolat csak akkor marad, ha a magyar szó (kisbetűsítve) névmás — zárt szólista
     (NEVMAS: vonatkozó, mutató, személyes, kérdő és határozatlan névmások ragos alakjaikkal; csak főnévi és
     melléknévi névmás, névmási határozószó nem), vagy az „a”, ha utána vonatkozó névmás áll (VONATKOZO: a ki, a mely,
     a mi …; az „a” a kettéírt vonatkozó névmás része, prompt_v3 B);
  2. szűrők: (a) minden „ki” marad, két tételes kivétellel (KI_IGEKOTO: 2Sám 5:2, 2Sám 13:17), ahol igekötő.
     (b) A szóvégi kérdő „-e/-é” leválasztódik (maga soha nem illeszkedik, pl. „megmentheted-e”: törlődik); a maradék
     szó illeszkedik a listára (pl. „azokra-é”: marad). Más kötőjeles szó a teljes alakjával illeszkedik. (c) A „mind” + listás alak
     (mindazok, mindezt …) általános szabályként a listán van. (d) Az önálló „az” marad, ha utána mássalhangzóval kezdődő szó, írásjel, versvég, vagy „a”/„az” áll; magánhangzóval
     kezdődő szó előtt törlődik (névelőként kezelve). Az -ért ragos alakok (ezért, azért …) túlnyomóan határozószói
     szerepük miatt nincsenek a listán.
  3. ʾet (H0853): minden kapcsolata törlődik;
  4. egyetlen-pár védelem nincs: ha a magyar szó pár nélkül marad, az ismert kimaradás.
Csak törlő javítás: új pár nem keletkezik, a megmaradó `parok`-sorok bájtra változatlanok. A `szavak_*.tsv`-ben a
két érintett token partnerlistája szűkül; ha üres lesz, a magyar token `betoldas`, az eredeti `forditatlan` lesz; a
magyar token `strong` mezője a megmaradó partnerekből vezetődik le (mint az `egyesit.py`-ban); a token
`bizonyossag` és `forras` mezője változatlan (a két modell döntését írja le, nem a takarítást). A szabály idempotens:
az 1.1-re futtatva a törlőlista üres.

Módok (az `--alap DIR` a bemenő 1.0 táblák helye, alapértelmezés: adat/karoli_strong):
  --felmeres [--letet DIR]  a felhasználó szúrópróbájához, MIND a repón kívüli letétbe (alapértelmezés:
                            ~/Bible-Study-letet/konvencio_11_szuro/; meglévő, eltérő tartalmú fájlt nem ír felül):
                            a megtartott és a törölt kapcsolatok magyar szótípusai darabszámmal, az ismert kimaradások
                            könyvcsoportonként, a magánhangzó előtt törölt „az”-ok listája versszöveggel, összefoglaló
  --general DIR             az 1.1 `parok_*.tsv` és `szavak_*.tsv` táblái DIR-be (DIR ≠ --alap); utána --ellenoriz
  --torolt-ki DIR           a törlőlista (`torolt_kapcsolatok.tsv`) DIR-be (a letétbe; felülírás nélkül)
  --kimaradas-ki DIR        az ismert kimaradások (a törléssel pár nélkül maradó magyar szavak) DIR-be, a pár nélküli
                            validációs keret kizárási szabályával (`keret_kizarasi_ok`), és rétegenkénti összesítéssel
  --tos-bovitett DIR        a bővített tövekkel futtatott tábla (`6_tos_bovitett.tsv`, a `korabban` oszloppal az
                            `5_tos_teljesseg.tsv`-hez képest), és az általános névmások ismert kimaradása
  --tos-tabla DIR           a lista teljességének tőszerinti táblája (`5_tos_teljesseg.tsv`) DIR-be (a letétbe)
  --ellenoriz DIR           egy előállított 1.1 ellenőrzése az --alap 1.0-hoz képest: a párok részhalmaz, minden
                            megmaradó sor bájtra azonos, a törölt sorok pontosan a törlőlista, minden megmaradó
                            névelő-pár megfelel a szabálynak, 0 ʾet-pár, a szótábla konzisztens
  --hash                    a törlőlista SHA-256-ja (a kanonikus `torolt_kapcsolatok.tsv` bájtjain)

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (a `csv` modul tilos, CLAUDE.md).
"""
import argparse
import collections
import glob
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402  (a Károli-tokenizálás: ugyanaz a sorszám, mint a szótáblában)
from pontossag_minta import CSOPORT  # noqa: E402  (fájlnév-könyv -> könyvcsoport)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALAP = os.path.join(GYOKER, 'adat', 'karoli_strong')
KAROLI = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')
LETET = os.path.join(os.path.expanduser('~'), 'Bible-Study-letet', 'konvencio_11_szuro')

NEVELO = ('G3588', 'H9009')
ET = 'H0853'
CEL_STRONG = (ET,) + NEVELO
MAGANHANGZO = frozenset('aáeéiíoóöőuúüű')

# --- a névmáslista (rögzített; a változtatás a törlőlista hash-ét is változtatja) ---------------------------------
# Csak főnévi és melléknévi névmás; névmási határozószó nem (DT-F175vr).
_KI = ('ki kik kit kiket kinek kiknek kiben kikben kinél kiknél kitől kiktől kihez kikhez kivel kikkel kié kiké '
       'kiért kikért kiből kikből kire kikre kiről kikről kin kiken')
_MELY = ('mely melyek melyet melyeket melynek melyeknek melyben melyekben melynél melyeknél melytől melyektől '
         'melyhez melyekhez mellyel melylyel melyekkel melyért melyekért melyből melyekből melyre melyekre melyről '
         'melyekről melyen melyeken')
_MI = 'mi mik mit miket minek miknek miben miből mire miről mitől mihez mié mivel mitek'
_A_ELOTAGU = 'aki akik akit akiket akinek akiknek amely amelyek amelyet amelyeket amelynek ami amit amik'
_VALA = 'valaki valakik valakit valakinek valami valamit'
_EZ = ('e ez ezt ezek ezeket ennek ezeknek ebben ezekben ezen ezeken ezzel ezekkel erre ezekre ebből ezekből ettől '
       'ezektől ehhez ezekhez erről ezekről ezé ezeké')
_AZ = ('azt azok azokat annak azoknak abban azokban azon azokon azzal azokkal arra azokra abból azokból attól '
       'azoktól ahhoz azokhoz azokért arról azokról azé azoké')
_AMA = 'ama amaz amazok amazokat amazt amannak amazoknak'
_UGYAN = 'ugyanaz ugyanazt ugyanazon ugyanazok ugyanannak ugyanez ugyanezt ugyanezen ugyanebben ugyanabban'
_ILYEN = 'ilyen ilyenek ilyent olyan olyanok olyant'
_SZEMELYES = ('én engem nékem te téged néked ő őt néki őnéki ők őket nékik őnékik minket nékünk ti titeket néktek '
              'övé övéi vele velök velem veled velünk veletek tőle tőlök tőlem hozzá hozzájok érette érettök róla '
              'rajta benne bennök belőle')
_HATAROZATLAN = 'némelyek némelyeket mások'
# a második célzott ellenőrzés után felvett alakok (a felhasználó döntése, 2026-11-18): a testvéralakjuk listás
_TOS_BOVITES2 = 'övéit nekünk ugyanezeket valakinél'
# a névutós személyes névmási sorok kiegészítése (a sor egy tagja már listás volt; Károli-alak és mai alak is)
_NEVUTOS = ('előttem előtted előtte előttünk előttetek előttük előttök '
            'tőled tőlünk tőletek tőlük '
            'hozzám hozzád hozzánk hozzátok hozzájuk '
            'érettem éretted érettünk érettetek érettük '
            'rólam rólad rólunk rólatok róluk rólok '
            'rajtam rajtad rajtunk rajtatok rajtuk rajtok '
            'bennem benned bennünk bennetek bennük '
            'belőlem belőled belőlünk belőletek belőlük belőlök '
            'velük')
# a tőszerinti tábla átnézése után felvett alakok (a testvéralakjuk már listás; a felhasználó döntése, 2026-11-17)
_TOS_BOVITES = ('abba annál azéi amazoké enyéim enyéimet enyémből tiédet mieink ilyeneket ilyeneké ilyenfélékkel '
                'ilyesmiket melyik ugyanazokat másik másiknak másiknál másikra mást másé másokét magaméval')

VONATKOZO = frozenset((_KI + ' ' + _MELY + ' ' + _MI).split())
NEVMAS = frozenset(' '.join((_KI, _MELY, _MI, _A_ELOTAGU, _VALA, _EZ, _AZ, _AMA, _UGYAN, _ILYEN, _SZEMELYES,
                             _HATAROZATLAN, _TOS_BOVITES, _TOS_BOVITES2, _NEVUTOS)).split())
# általános névmás (mind-, minden-): nincs a listán; ha a törléssel pár nélkül marad, ismert kimaradás

TORLO_FEJ = ['vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong']

# A „ki” két tételes kivétele (vers, magyar sorszám): itt a „ki” igekötő, a kapcsolata törlődik. Az 58 nem „a” utáni
# „ki”-esetet egyenként ellenőriztük: 56 névmás, 2 igekötő (a felhasználó döntése, 2026-11-17).
KI_IGEKOTO = frozenset({('2Sám 5:2', 10), ('2Sám 13:17', 12)})
# a szóvégi kérdő „-e/-é”: leválasztódik, a maradék szó illeszkedik a listára; maga soha nem illeszkedik
KERDO_E = frozenset(('e', 'é'))


HATAROZATLAN_TOVEK = ('egyik', 'egyéb', 'egyeb')   # egyik, egyiket, egyiknek, egyikünk …; egyéb, egyebeknek …


def nevmas_e(s):
    """A (kisbetűs) szó a névmáslistán van-e: a lista eleme, „mind” + listás alak (mindazok, mindezt …), vagy az egyik-,
    egyéb- határozatlan névmás valamely alakja (a „más/másik” mintájára)."""
    return (s in NEVMAS or (s.startswith('mind') and (s[4:] in NEVMAS or s[4:] == 'az'))
            or s.startswith(HATAROZATLAN_TOVEK))


def dontes(strong, hu_szo, elozo, kovetkezo, koztes, elotte=' ', teljes=None):
    """(megtartás oka | None, törlés oka | None) egy CEL_STRONG-párra.

    elozo / kovetkezo: a versben előtte / utána álló magyar token (None: verskezdet/-vég); koztes: a magyar szó és a
    következő token közti szöveg, elotte: az előző token és a magyar szó közti szöveg (írásjel-vizsgálathoz); teljes: a
    kötőjeles teljes alak (a kötőjellel kapcsolt tokenek a kötőjelekkel), ha a szó kötőjeles alak része."""
    if strong == ET:
        return None, 'et'
    if teljes and teljes != hu_szo:
        # kötőjeles alak: csak a teljes alak illeszkedhet a listára (pl. „megmentheted-e”: törlődik)
        return ('nevmas', None) if nevmas_e(teljes.lower()) else (None, 'kotojeles')
    s = hu_szo.lower()
    k = (kovetkezo or '').lower()
    if s == 'az':
        if kovetkezo is None:
            return 'az_versveg', None
        if koztes.strip():
            return 'az_irasjel_elott', None
        if k in ('a', 'az'):
            return 'az_nevelo_elott', None
        if k[:1] not in MAGANHANGZO:
            return 'az_massalhangzo_elott', None
        return None, 'az_maganhangzo_elott'
    if s == 'a':
        return ('a_vonatkozo', None) if k in VONATKOZO else (None, 'nem_nevmas')
    if nevmas_e(s):
        return 'nevmas', None
    return None, 'nem_nevmas'


def tabla_olvas(ut):
    """(proveniencia-sor, fejléc, sorok[list], nyers sorok[str]) — az első sor `#`-kezdetű proveniencia."""
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read().split('\n')
    if nyers and nyers[-1] == '':
        nyers = nyers[:-1]
    if not nyers or not nyers[0].startswith('#'):
        raise SystemExit('nincs proveniencia-sor: %s' % ut)
    fej = nyers[1].split('\t')
    adat = nyers[2:]
    return nyers[0], fej, [s.split('\t') for s in adat], adat


def konyvek(alap):
    """A könyvek nevei (a fájlnév `parok_` utáni része), rendezve."""
    nevek = sorted(os.path.basename(p)[len('parok_'):-len('.tsv')] for p in glob.glob(os.path.join(alap, 'parok_*.tsv')))
    if not nevek:
        raise SystemExit('nincs parok_*.tsv: %s' % alap)
    for n in nevek:
        if not os.path.exists(os.path.join(alap, 'szavak_%s.tsv' % n)):
            raise SystemExit('hiányzó szavak_%s.tsv' % n)
    return nevek


_KAROLI = {}


def karoli_versek():
    if not _KAROLI:
        with open(KAROLI, encoding='utf-8') as f:
            for i, sor in enumerate(f):
                if i == 0:
                    continue
                m = sor.rstrip('\n').split('\t')
                if len(m) >= 2:
                    _KAROLI[m[0]] = m[1]
    return _KAROLI


def vers_tokenek(vers):
    """[(token, kezdet, vég)] a Károli-versből, a szótábla sorszámozásával (index + 1)."""
    return [(m.group(0), m.start(), m.end()) for m in tokenek._TOKEN.finditer(karoli_versek()[vers])]


def konyv_dontes(alap, konyv):
    """Egy könyv párjai a döntéssel: [(sor, nyers, (megtart, torol) | None)] és a pár környezete (előző, következő)."""
    _, pfej, psorok, pnyers = tabla_olvas(os.path.join(alap, 'parok_%s.tsv' % konyv))
    pi = {k: i for i, k in enumerate(pfej)}
    tok = {}
    ki = []
    for r, ny in zip(psorok, pnyers):
        st = r[pi['strong']]
        if st not in CEL_STRONG:
            ki.append((r, ny, None, None))
            continue
        v = r[pi['vers']]
        if v not in tok:
            tok[v] = vers_tokenek(v)
        t = tok[v]
        h = int(r[pi['hu_sorszam']])
        if h > len(t) or t[h - 1][0] != r[pi['hu_szo']]:
            raise SystemExit('a Károli-token eltér a pártáblától: %s %d %s' % (v, h, r[pi['hu_szo']]))
        szoveg = karoli_versek()[v]
        i = h - 1
        elozo = t[i - 1][0] if i >= 1 else None
        elotte = szoveg[t[i - 1][2]:t[i][1]] if i >= 1 else ''
        # a kötőjeles teljes alak: balra és jobbra, amíg a tokeneket pontosan egy kötőjel köti össze
        a_, b_ = i, i
        while a_ > 0 and szoveg[t[a_ - 1][2]:t[a_][1]] == '-':
            a_ -= 1
        while b_ + 1 < len(t) and szoveg[t[b_][2]:t[b_ + 1][1]] == '-':
            b_ += 1
        # a szóvégi kérdő „-e/-é” leválasztódik: maga soha nem illeszkedik; a maradék szó a saját szabályai szerint,
        # és a „következő” szó a leválasztott végződés utáni szó
        kerdo = b_ > a_ and t[b_][0].lower() in KERDO_E
        if kerdo and i == b_:
            d = (None, 'kerdo_e') if st != ET else (None, 'et')
            ki.append((r, ny, d, (elozo or '', t[i + 1][0] if i + 1 < len(t) else '')))
            continue
        vege = b_ - 1 if kerdo else b_
        utana = vege + 1 + (1 if kerdo else 0)   # a következő szó indexe
        kov = t[utana][0] if utana < len(t) else None
        koztes = szoveg[t[utana - 1][2]:t[utana][1]] if utana < len(t) else ''
        teljes = szoveg[t[a_][1]:t[vege][2]]
        if r[pi['hu_szo']].lower() == 'ki' and (v, h) in KI_IGEKOTO and st != ET:
            d = (None, 'ki_igekoto')
        else:
            d = dontes(st, r[pi['hu_szo']], elozo, kov, koztes, elotte, teljes)
        ki.append((r, ny, d, (elozo or '', kov or '')))
    return pi, ki


def torlolista(alap=ALAP):
    """(törlendő sorok, megtartott sorok): TORLO_FEJ + [ok, előző, következő, könyv], könyv- és fájlsorrendben."""
    torol, megtart = [], []
    for kv in konyvek(alap):
        pi, dontesek = konyv_dontes(alap, kv)
        for r, _, d, kor in dontesek:
            if d is None:
                continue
            sor = [r[pi['vers']], r[pi['hu_sorszam']], r[pi['hu_szo']], r[pi['er_sorszam']], r[pi['er_szo']],
                   r[pi['strong']]]
            if d[0] is None:
                torol.append(sor + [d[1], kor[0], kor[1], kv])
            else:
                megtart.append(sor + [d[0], kor[0], kor[1], kv])
    return torol, megtart


def torlolista_bajtok(torol):
    return ('\t'.join(TORLO_FEJ) + '\n' + ''.join('\t'.join(s[:6]) + '\n' for s in torol)).encode('utf-8')


def torlolista_hash(torol=None, alap=ALAP):
    if torol is None:
        torol, _ = torlolista(alap)
    return hashlib.sha256(torlolista_bajtok(torol)).hexdigest()


# --- az 1.1 előállítása -------------------------------------------------------------------------------------------

def hu_strong(strongok):
    """A magyar token `strong` mezője: a partnerek Strong-számai ismétlés nélkül, sorrendben, `+`-szal (egyesit.py)."""
    ut = []
    for x in strongok:
        if x not in ut:
            ut.append(x)
    return '+'.join(ut)


def szavak_szukit(sfej, ssorok, torolt):
    """A szótábla az 1.1 szerint. torolt: {(vers, hu_sorszam, er_sorszam)}. Visszaad: új sorok (list)."""
    si = {k: i for i, k in enumerate(sfej)}
    er_strong = {}
    for r in ssorok:
        if r[si['oldal']] == 'er':
            er_strong[(r[si['vers']], int(r[si['sorszam']]))] = r[si['strong']]
    hu_vesz = collections.defaultdict(set)
    er_vesz = collections.defaultdict(set)
    for v, h, e in torolt:
        hu_vesz[(v, h)].add(e)
        er_vesz[(v, e)].add(h)
    uj = []
    for r in ssorok:
        v, old, n = r[si['vers']], r[si['oldal']], int(r[si['sorszam']])
        vesz = (hu_vesz if old == 'hu' else er_vesz).get((v, n))
        if not vesz:
            uj.append(r)
            continue
        regi = [int(x) for x in r[si['partner_sorszam']].split(',') if x]
        if not vesz <= set(regi):
            raise SystemExit('a törlendő partner nincs a szótáblában: %s %s %d %s' % (v, old, n, sorted(vesz)))
        marad = [x for x in regi if x not in vesz]
        r2 = list(r)
        r2[si['partner_sorszam']] = ','.join(str(x) for x in marad)
        if old == 'hu':
            r2[si['strong']] = hu_strong(er_strong[(v, x)] for x in marad)
            if not marad:
                r2[si['allapot']] = 'betoldas'
        elif not marad:
            r2[si['allapot']] = 'forditatlan'
        uj.append(r2)
    return uj


def general(cel, alap=ALAP):
    if os.path.abspath(cel) == os.path.abspath(alap):
        raise SystemExit('a cél nem lehet a bemenet (előbb ideiglenes könyvtárba, ellenőrzés, utána másolás)')
    os.makedirs(cel, exist_ok=True)
    torol_mind, _ = torlolista(alap)
    h = hashlib.sha256(torlolista_bajtok(torol_mind)).hexdigest()
    for kv in konyvek(alap):
        pprov, pfej, _, _ = tabla_olvas(os.path.join(alap, 'parok_%s.tsv' % kv))
        sprov, sfej, ssorok, _ = tabla_olvas(os.path.join(alap, 'szavak_%s.tsv' % kv))
        pi, dontesek = konyv_dontes(alap, kv)
        torolt = set()
        marad = []
        for r, ny, d, _ in dontesek:
            if d is not None and d[0] is None:
                torolt.add((r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])))
            else:
                marad.append(ny)
        jel = ('# GENERÁLT: eszkozok/karoli_strong/konvencio_egysegesites.py — 1.1 (konvenció-egységesítés: a névelő- '
               'és ʾet-kapcsolatok törlése a névmáslista kivételével) | torlolista_sha256=%s | az 1.0 proveniencia-'
               'sora: ' % h)
        with open(os.path.join(cel, 'parok_%s.tsv' % kv), 'w', encoding='utf-8', newline='') as f:
            f.write(jel + pprov.lstrip('# ') + '\n' + '\t'.join(pfej) + '\n' + ''.join(s + '\n' for s in marad))
        uj = szavak_szukit(sfej, ssorok, torolt)
        with open(os.path.join(cel, 'szavak_%s.tsv' % kv), 'w', encoding='utf-8', newline='') as f:
            f.write(jel + sprov.lstrip('# ') + '\n' + '\t'.join(sfej) + '\n' + ''.join('\t'.join(s) + '\n' for s in uj))
    print('1.1 előállítva: %s · törölt kapcsolat: %d · torlolista_sha256=%s' % (cel, len(torol_mind), h))
    return ellenoriz(cel, alap)


def ellenoriz(cel, alap=ALAP):
    """Az 1.1 (cel) és az 1.0 (alap) összevetése, és a szabály újraellenőrzése az 1.1-en. Visszaad: hibák száma."""
    hibak = []
    torol, _ = torlolista(alap)
    vart_torolt = set((s[0], int(s[1]), int(s[3])) for s in torol)
    talalt_torolt = set()
    osszes_10 = osszes_11 = 0
    for kv in konyvek(alap):
        _, pfej, _, n10 = tabla_olvas(os.path.join(alap, 'parok_%s.tsv' % kv))
        _, pfej11, _, n11 = tabla_olvas(os.path.join(cel, 'parok_%s.tsv' % kv))
        if pfej11 != pfej:
            hibak.append('parok_%s: a fejléc eltér' % kv)
        pi = {k: i for i, k in enumerate(pfej)}
        osszes_10 += len(n10)
        osszes_11 += len(n11)
        # részhalmaz, sorrendtartó, bájtra azonos sorok
        j = 0
        for ny in n10:
            if j < len(n11) and n11[j] == ny:
                j += 1
                continue
            r = ny.split('\t')
            talalt_torolt.add((r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])))
            if r[pi['strong']] not in CEL_STRONG:
                hibak.append('parok_%s: nem névelő/ʾet sor tűnt el: %s' % (kv, ny[:80]))
        if j != len(n11):
            hibak.append('parok_%s: az 1.1-ben az 1.0-ban nem szereplő vagy átrendezett sor áll (%d/%d)' % (kv, j, len(n11)))
        # a szabály az 1.1-en: minden megmaradó névelő-pár megtartható, ʾet-pár nincs
        _, d11 = konyv_dontes(cel, kv)
        for r, _, d, _ in d11:
            if d is not None and d[0] is None:
                hibak.append('parok_%s: az 1.1-ben szabálysértő pár maradt (%s): %s %s %s' % (
                    kv, d[1], r[pi['vers']], r[pi['hu_szo']], r[pi['strong']]))
        # szótábla: minden token egyszer, szimmetrikus partnerség a pártáblával, a hu strong levezethető
        _, sfej, s10, _ = tabla_olvas(os.path.join(alap, 'szavak_%s.tsv' % kv))
        _, sfej11, s11, _ = tabla_olvas(os.path.join(cel, 'szavak_%s.tsv' % kv))
        si = {k: i for i, k in enumerate(sfej)}
        if sfej11 != sfej or len(s10) != len(s11):
            hibak.append('szavak_%s: fejléc vagy sorszám eltér' % kv)
            continue
        par11 = collections.defaultdict(set)
        er11 = collections.defaultdict(set)
        for ny in n11:
            r = ny.split('\t')
            v, h, e = r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])
            par11[(v, h)].add(e)
            er11[(v, e)].add(h)
        er_strong = {(r[si['vers']], int(r[si['sorszam']])): r[si['strong']] for r in s11 if r[si['oldal']] == 'er'}
        for a, b in zip(s10, s11):
            kulcs_a = (a[si['vers']], a[si['oldal']], a[si['sorszam']], a[si['szo']])
            kulcs_b = (b[si['vers']], b[si['oldal']], b[si['sorszam']], b[si['szo']])
            if kulcs_a != kulcs_b:
                hibak.append('szavak_%s: a tokensor eltér: %s' % (kv, kulcs_a))
                continue
            for mezo in ('bizonyossag', 'forras'):
                if a[si[mezo]] != b[si[mezo]]:
                    hibak.append('szavak_%s: %s változott: %s' % (kv, mezo, kulcs_a))
            v, old, n = b[si['vers']], b[si['oldal']], int(b[si['sorszam']])
            if a[si['allapot']] == 'fuggoben':
                if b != a:
                    hibak.append('szavak_%s: függőben lévő token változott: %s' % (kv, kulcs_a))
                continue
            p = sorted(int(x) for x in b[si['partner_sorszam']].split(',') if x)
            vart = sorted((par11 if old == 'hu' else er11).get((v, n), ()))
            if p != vart:
                hibak.append('szavak_%s: partnerlista ≠ pártábla: %s %s %s' % (kv, kulcs_a, p, vart))
            p10 = set(int(x) for x in a[si['partner_sorszam']].split(',') if x)
            if not set(p) <= p10:
                hibak.append('szavak_%s: új partner: %s' % (kv, kulcs_a))
            if old == 'hu':
                if b[si['strong']] != hu_strong(er_strong[(v, x)] for x in p):
                    hibak.append('szavak_%s: a hu strong nem a partnerekből vezethető le: %s' % (kv, kulcs_a))
                vart_all = 'parositva' if p else 'betoldas'
            else:
                if b[si['strong']] != a[si['strong']]:
                    hibak.append('szavak_%s: az er strong változott: %s' % (kv, kulcs_a))
                vart_all = 'parositva' if p else 'forditatlan'
            if b[si['allapot']] != vart_all:
                hibak.append('szavak_%s: állapot %s, várt %s: %s' % (kv, b[si['allapot']], vart_all, kulcs_a))
            if p10 == set(p) and b != a:
                hibak.append('szavak_%s: érintetlen token változott: %s' % (kv, kulcs_a))
    if talalt_torolt != vart_torolt:
        hibak.append('a törölt sorok halmaza ≠ törlőlista (%d vs %d)' % (len(talalt_torolt), len(vart_torolt)))
    if osszes_10 - osszes_11 != len(vart_torolt):
        hibak.append('párszám: %d − %d ≠ %d' % (osszes_10, osszes_11, len(vart_torolt)))
    for hb in hibak[:40]:
        print('HIBA:', hb)
    print('ellenőrzés: 1.0 pár %d → 1.1 pár %d (törölt %d) · %d hiba' % (osszes_10, osszes_11, osszes_10 - osszes_11,
                                                                          len(hibak)))
    return len(hibak)


# --- letét (felülírás nélkül) ------------------------------------------------------------------------------------

def letet_ir(ut, adat):
    """Új letétfájl írása; meglévő, eltérő tartalmú fájlt nem ír felül (a letét csak bővül, DT-F175vl)."""
    if isinstance(adat, str):
        adat = adat.encode('utf-8')
    if os.path.exists(ut):
        if open(ut, 'rb').read() == adat:
            return
        raise SystemExit('a letétfájl már létezik, eltérő tartalommal (nem írom felül): %s' % ut)
    with open(ut, 'wb') as f:
        f.write(adat)


def torolt_ki(letet, alap=ALAP):
    os.makedirs(letet, exist_ok=True)
    torol, _ = torlolista(alap)
    letet_ir(os.path.join(letet, 'torolt_kapcsolatok.tsv'), torlolista_bajtok(torol))
    print('törlőlista: %s · %d sor · sha256=%s' % (letet, len(torol), torlolista_hash(torol)))


# a lista teljességének ellenőrzéséhez (5_tos_teljesseg.tsv): a névmáslista tövei; minden TÖRÖLT magyar szótípus, amely
# ilyen tővel kezdődik, a táblába kerül (a leghosszabb illeszkedő tő alatt), hogy a lista hiányai láthatók legyenek
LISTAS_TOVEK = ('ez', 'az', 'eb', 'ab', 'an', 'en', 'er', 'ar', 'et', 'at', 'eh', 'ah', 'öv', 'enyé', 'tié', 'mié',
                'mind', 'mely', 'ami', 'ame', 'aki', 'mi', 'ki', 'ama', 'ugyan', 'ily', 'oly', 'vala', 'ő', 'én', 'eng',
                'nék', 'tég', 'ti', 'vel', 'től', 'hozz', 'érett', 'ról', 'rajt', 'benn', 'belő', 'ném', 'más')


BOVITETT_TOVEK = LISTAS_TOVEK + ('ily', 'oly', 'ugyan', 'más', 'ném', 'vala', 'akár', 'bár', 'sem', 'sen', 'maga',
                                  'egymás', 'ön', 'én', 'te', 'ő', 'ti', 'kicsoda', 'micsoda')


def tos_tabla(letet, alap=ALAP, fajl='5_tos_teljesseg.tsv', tovek=None, elozo=None):
    """A lista teljességének táblája (a felhasználó átnézéséhez, a letétbe): a törölt magyar szótípusok, amelyek
    listás tővel kezdődnek, darabszámmal, a törlés okával és egy példaverssel. elozo: egy korábbi tőtábla útvonala; a
    `korabban` oszlop jelöli, ha a típus már ott is szerepelt."""
    os.makedirs(letet, exist_ok=True)
    torol, _ = torlolista(alap)
    tovek = sorted(tovek or LISTAS_TOVEK, key=len, reverse=True)
    regi = set()
    if elozo:
        with open(elozo, encoding='utf-8') as f:
            regi = {x.split('\t')[1] for x in f.read().split('\n')[1:] if x}
    db = collections.defaultdict(collections.Counter)
    pelda = {}
    for s in torol:
        w = s[2].lower()
        to = next((x for x in tovek if w.startswith(x)), None)
        if to is None:
            continue
        db[(to, w)][s[6]] += 1
        pelda.setdefault((to, w), (s[0], s[5]))
    versek = karoli_versek()
    sorok = []
    for (to, w) in sorted(db, key=lambda k: (k[0], -sum(db[k].values()), k[1])):
        v, st = pelda[(to, w)]
        sor = [to, w, sum(db[(to, w)].values()), ', '.join('%s %d' % x for x in sorted(db[(to, w)].items())),
               v, st, versek.get(v, '?')]
        if elozo:
            sor.insert(4, 'igen' if w in regi else '')
        sorok.append(sor)
    fej = ['to', 'hu_szo', 'db', 'torles_oka', 'pelda_vers', 'pelda_strong', 'pelda_karoli_vers']
    if elozo:
        fej.insert(4, 'korabban')
    letet_ir(os.path.join(letet, fajl), _tsv(fej, sorok))
    print('tőszerinti tábla: %s · %d típus, %d pár%s · torlolista_sha256=%s' % (
        os.path.join(letet, fajl), len(sorok), sum(r[2] for r in sorok),
        (' (új a korábbi táblához képest: %d típus)' % sum(1 for r in sorok if not r[4])) if elozo else '',
        torlolista_hash(torol)))


def altalanos_kimaradas(alap=ALAP):
    """Az általános névmások (mind-, minden-; nincsenek a listán), amelyek a törléssel pár nélkül maradnak."""
    return collections.Counter(s[2].lower() for s in ismert_kimaradasok(alap)
                               if s[2].lower().startswith('mind') and not nevmas_e(s[2].lower()))


USZ_CSOPORTOK = ('USZ_evangelium', 'USZ_level', 'USZ_jelenesek')
CSOPORTOK = ('OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta') + USZ_CSOPORTOK


def ismert_kimaradasok(alap=ALAP):
    """A törléssel pár nélkül maradó magyar szavak: [vers, hu_sorszam, hu_szo, könyv, könyvcsoport, kizárási ok].

    A kizárási ok a pár nélküli validációs keret szabálya (karoli_strong_validacio_minta.kizarasi_ok, DT-F175vb):
    ha van, a szó a keretbe nem esik (pl. „a”, „az”, „azt”)."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from karoli_strong_validacio_minta import kizarasi_ok
    torol, _ = torlolista(alap)
    torolt_hu = collections.defaultdict(set)
    for s in torol:
        torolt_hu[(s[0], int(s[1]))].add(s[3])
    ki = []
    for kv in konyvek(alap):
        _, sfej, ssorok, _ = tabla_olvas(os.path.join(alap, 'szavak_%s.tsv' % kv))
        si = {k: i for i, k in enumerate(sfej)}
        versenkent = collections.defaultdict(list)
        for r in ssorok:
            if r[si['oldal']] == 'hu':
                versenkent[r[si['vers']]].append(r)
        for v, hu in versenkent.items():
            for i, r in enumerate(hu):
                vesz = torolt_hu.get((v, int(r[si['sorszam']])))
                if not vesz:
                    continue
                p = set(x for x in r[si['partner_sorszam']].split(',') if x)
                if p and p <= vesz:
                    ok = kizarasi_ok(r[si['szo']], [y[si['szo']].casefold() for y in hu[i + 1:]])
                    ki.append([v, r[si['sorszam']], r[si['szo']], kv, CSOPORT[kv], ok or ''])
    return ki


def kimaradas_ki(letet, alap=ALAP):
    os.makedirs(letet, exist_ok=True)
    km = ismert_kimaradasok(alap)
    letet_ir(os.path.join(letet, 'ismert_kimaradasok.tsv'),
             _tsv(['vers', 'hu_sorszam', 'hu_szo', 'konyv', 'konyvcsoport', 'keret_kizarasi_ok'], km))
    ossz = collections.Counter(s[4] for s in km)
    keret = collections.Counter(s[4] for s in km if not s[5])
    sorok = [[cs, 'ÚSZ' if cs in USZ_CSOPORTOK else 'ÓSZ', ossz[cs], keret[cs]] for cs in CSOPORTOK]
    for t in ('ÓSZ', 'ÚSZ'):
        sorok.append([t, t, sum(s[2] for s in sorok[:len(CSOPORTOK)] if s[1] == t),
                      sum(s[3] for s in sorok[:len(CSOPORTOK)] if s[1] == t)])
    sorok.append(['osszesen', '', len(km), sum(keret.values())])
    letet_ir(os.path.join(letet, 'ismert_kimaradasok_retegenkent.tsv'),
             _tsv(['konyvcsoport', 'testamentum', 'pár nélkül marad', 'a pár nélküli keretbe esik'], sorok))
    for s in sorok:
        print('\t'.join(str(x) for x in s))
    return sorok


def _tsv(fej, sorok):
    return '\t'.join(fej) + '\n' + ''.join('\t'.join(str(x) for x in s) + '\n' for s in sorok)


def felmeres(letet, alap=ALAP):
    os.makedirs(letet, exist_ok=True)
    torol, megtart = torlolista(alap)
    h = torlolista_hash(torol)
    # a magyar tokenek partnerei (az új pár nélküli szavakhoz) és az eredeti tokenek száma
    hu_partner = {}
    er_ossz = collections.Counter()
    for kv in konyvek(alap):
        _, sfej, ssorok, _ = tabla_olvas(os.path.join(alap, 'szavak_%s.tsv' % kv))
        si = {k: i for i, k in enumerate(sfej)}
        for r in ssorok:
            if r[si['oldal']] == 'hu':
                hu_partner[(r[si['vers']], r[si['sorszam']])] = (
                    set(x for x in r[si['partner_sorszam']].split(',') if x), r[si['szo']], kv)
            elif r[si['strong']] in CEL_STRONG:
                er_ossz[r[si['strong']]] += 1

    # (1) megtartott típusok; az „a” és „az” a környezettel részletezve
    mt = collections.defaultdict(collections.Counter)
    reszl = collections.defaultdict(collections.Counter)
    for s in megtart:
        w = s[2].lower()
        mt[(w, s[6])][s[5]] += 1
        if w in ('a', 'az'):
            reszl[(w, s[6])][s[8].lower() or '(versvég)'] += 1
        elif w == 'ki':
            reszl[(w, s[6])]['előtte: ' + s[7].lower()] += 1
    sorok = []
    for (w, ok) in sorted(mt, key=lambda k: (-sum(mt[k].values()), k)):
        c = mt[(w, ok)]
        r = reszl.get((w, ok))
        sorok.append([w, sum(c.values()), c['H9009'], c['G3588'], ok,
                      ', '.join('%s %d' % kv for kv in r.most_common(15)) if r else ''])
    letet_ir(os.path.join(letet, '1_megtartott_tipusok.tsv'),
             _tsv(['hu_szo', 'db', 'H9009', 'G3588', 'megtartas_oka', 'kornyezet (az utana allo szo; ki: az elotte allo)'],
                  sorok))

    # (2) törölt típusok; jelölve, ha a szó maga a névmáslistán van (a szűrő törölte)
    tt = collections.defaultdict(collections.Counter)
    tok = collections.defaultdict(collections.Counter)
    for s in torol:
        w = s[2].lower()
        tt[w][s[5]] += 1
        tok[w][s[6]] += 1
    sorok = []
    for w in sorted(tt, key=lambda w: (-sum(tt[w].values()), w)):
        c = tt[w]
        sorok.append([w, sum(c.values()), c['H9009'], c['G3588'], c['H0853'],
                      ', '.join('%s %d' % kv for kv in sorted(tok[w].items())),
                      'igen' if (w in NEVMAS or w in ('a', 'az', 'ki')) else ''])
    letet_ir(os.path.join(letet, '2_torolt_tipusok.tsv'),
             _tsv(['hu_szo', 'db', 'H9009', 'G3588', 'H0853', 'torles_oka', 'a_szo_a_nevmaslistan_vagy_szurt'], sorok))

    # (3) ismert kimaradások: magyar szó, amely a törléssel pár nélkül marad, könyvcsoportonként
    torolt_hu = collections.defaultdict(set)
    for s in torol:
        torolt_hu[(s[0], s[1])].add(s[3])
    kim = collections.defaultdict(collections.Counter)
    for k, vesz in torolt_hu.items():
        p, szo, kv = hu_partner[k]
        if p and p <= vesz:
            kim[CSOPORT[kv]][szo.lower()] += 1
    csoportok = ['OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta', 'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']
    sorok = []
    for cs in csoportok:
        for w, n in sorted(kim[cs].items(), key=lambda x: (-x[1], x[0])):
            sorok.append([cs, w, n])
    letet_ir(os.path.join(letet, '3_ismert_kimaradasok.tsv'), _tsv(['konyvcsoport', 'hu_szo', 'db'], sorok))

    # (4) a magánhangzó előtt törölt „az”-ok versszöveggel
    versek = karoli_versek()
    sorok = [[s[0], s[1], s[2], s[8], s[4], s[5], versek.get(s[0], '?')] for s in torol if s[6] == 'az_maganhangzo_elott']
    letet_ir(os.path.join(letet, '4_az_maganhangzo_elott_torolt.tsv'),
             _tsv(['vers', 'hu_sorszam', 'hu_szo', 'utana_allo_szo', 'er_szo', 'strong', 'karoli_vers'], sorok))
    n_az = len(sorok)

    st_t = collections.Counter(s[5] for s in torol)
    st_m = collections.Counter(s[5] for s in megtart)
    ok_m = collections.Counter(s[6] for s in megtart)
    ok_t = collections.Counter(s[6] for s in torol)
    nem_tipus = sum(1 for w in tt if w in NEVMAS or w in ('a', 'az', 'ki'))
    t = ['# Konvenció-egységesítés (1.1, végleges módszer) — szúrópróba-táblák\n',
         'Letétanyag, a repóba nem kerül. Előállítva: `eszkozok/karoli_strong/konvencio_egysegesites.py --felmeres`. '
         'A törlőlista SHA-256-ja (még nem fagyasztott): `%s`.\n' % h,
         '| Strong | eredeti token az 1.0-ban | pár az 1.0-ban | törlődik | megmarad |',
         '|---|---:|---:|---:|---:|']
    for st in CEL_STRONG:
        t.append('| %s | %d | %d | %d | %d |' % (st, er_ossz[st], st_t[st] + st_m[st], st_t[st], st_m[st]))
    t.append('| összesen | %d | %d | %d | %d |\n' % (sum(er_ossz.values()), len(torol) + len(megtart), len(torol),
                                                     len(megtart)))
    t.append('Megtartás oka: %s.\n' % ', '.join('%s %d' % kv for kv in sorted(ok_m.items())))
    t.append('Törlés oka: %s.\n' % ', '.join('%s %d' % kv for kv in sorted(ok_t.items())))
    t.append('Ismert kimaradás (a törléssel pár nélkül maradó magyar szó): %s; összesen %d.\n' % (
        ', '.join('%s %d' % (cs, sum(kim[cs].values())) for cs in csoportok), sum(sum(c.values()) for c in kim.values())))
    t.append('A szúrópróbához: `1_megtartott_tipusok.tsv` (%d típus — van-e köztük nem névmás; az „a”, „az”, „ki” '
             'sorában a környezet), `2_torolt_tipusok.tsv` (%d típus — van-e köztük névmás; az utolsó oszlop jelöli a '
             '%d típust, amely maga a listán van vagy szűrő törölte), `3_ismert_kimaradasok.tsv`, '
             '`4_az_maganhangzo_elott_torolt.tsv` (%d sor).\n' % (len(mt), len(tt), nem_tipus, n_az))
    letet_ir(os.path.join(letet, 'OSSZEFOGLALO.md'), '\n'.join(t))
    print('felmérés: %s · törlendő %d, megtartott %d · torlolista_sha256=%s' % (letet, len(torol), len(megtart), h))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--felmeres', action='store_true')
    g.add_argument('--general', metavar='DIR')
    g.add_argument('--torolt-ki', metavar='DIR')
    g.add_argument('--kimaradas-ki', metavar='DIR')
    g.add_argument('--tos-tabla', metavar='DIR')
    g.add_argument('--tos-bovitett', metavar='DIR')
    g.add_argument('--ellenoriz', metavar='DIR')
    g.add_argument('--hash', action='store_true')
    ap.add_argument('--letet', default=LETET)
    ap.add_argument('--alap', default=ALAP)
    a = ap.parse_args()
    if a.felmeres:
        felmeres(a.letet, a.alap)
    elif a.general:
        sys.exit(1 if general(a.general, a.alap) else 0)
    elif a.torolt_ki:
        torolt_ki(a.torolt_ki, a.alap)
    elif a.kimaradas_ki:
        kimaradas_ki(a.kimaradas_ki, a.alap)
    elif a.tos_tabla:
        tos_tabla(a.tos_tabla, a.alap)
    elif a.tos_bovitett:
        tos_tabla(a.tos_bovitett, a.alap, '6_tos_bovitett.tsv', BOVITETT_TOVEK,
                  os.path.join(a.tos_bovitett, '5_tos_teljesseg.tsv'))
        c = altalanos_kimaradas(a.alap)
        print('általános névmás (mind-, minden-), amely a törléssel pár nélkül marad (ismert kimaradás): %d (%s)'
              % (sum(c.values()), ', '.join('%s %d' % x for x in c.most_common())))
    elif a.ellenoriz:
        sys.exit(1 if ellenoriz(a.ellenoriz, a.alap) else 0)
    else:
        print(torlolista_hash(alap=a.alap))


if __name__ == '__main__':
    main()
