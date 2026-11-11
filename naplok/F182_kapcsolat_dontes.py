# -*- coding: utf-8 -*-
"""F182 HAMART-001, 1. fázis, F16 — a kapcsolat-jelöltek döntése (DT-F182e) és a kapcsolatok.tsv sorai.

Bemenet: naplok/F182_kapcsolat_jeloltek.tsv (naplok/F182_kapcsolat.py: TSK, Károli-KH, a 1/a próza
igehely-hivatkozásai és a tematikus sorok gerinc_elem-je mint jelöltforrás; a mért lexikai bizonyíték).

Döntési szabály (DT-F182e; a végrehajtó levezetése, a SEMA 2.3 bizonyosság-mezőjére):
  magas    — a két sor közös lánc-szópárt (árar+adámá, „föld színe”, málé+chámász, kóc+dardar) vagy legalább két
             közös lánc-szót hordoz, vagy a nyelvközi párnál a LXX két lánc-szava áll az újszövetségi versben,
             vagy a két versben legalább két további, nem köznapi szó szó szerint visszatér;
  közepes  — egy közös lánc-szó, illetve egy közös görög szócsalád (κατάρα, φθείρω), és a párt a TSK legalább 3
             szavazattal, a Károli-KH vagy a lap 1/a prózája köti össze; vagy tematikus sor és az a láncvers,
             amelyet az adat gerinc-eleme név szerint megnevez;
  küszöb alatt (elutasítva, SEMA 2.3) — egy közös lánc-szó, csak 1–2 TSK-szavazattal;
  elutasítva — közös lánc-szó, szópár, szócsalád és szó szerinti visszatérés nélkül (csak tematikus
             rokonság: a fölérendelt fogalom felé hígítana);
  elutasítva (redundáns) — két nem genezisi hely, amelyeket csak ugyanaz a lánc-szó vagy szópár köt össze:
             mindkettő a genezisi forrásverssel áll kapcsolatban, a köztük lévő él nem mond újat.
A típus (Előkép · Párhuzam · Beteljesedés · Kontraszt · Variáns; a definíció:
motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md 6. pont) és a funkció a beépülő párokon kézi (manual).

Írás: a kapcsolatok.tsv végére a HAMART-001 sorai (előtte 0 sor); a meglévő sorok bájtra változatlanok
(összevetés). A jelöltnapló kiegészül a döntés oszlopaival. A `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F182_kapcsolat_dontes.py [--ir]"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'HAMART-001'
JEL = 'naplok/F182_kapcsolat_jeloltek.tsv'
KAP = 'adat/kapcsolatok.tsv'
DT = 'DT-F182e'
TS = '2026-11-10'

KOZNAPI = {'H3068', 'H0430', 'H0559', 'H3605', 'H0776', 'H0120', 'H1961', 'H6213', 'H2009', 'H0854', 'H0935',
           'H0834', 'H3651', 'H2416', 'H5750', 'H3254', 'G1093', 'G2316'}
LANC = {'H0779', 'H0127', 'H6093', 'H2403', 'H2555', 'H7843', 'H6975', 'H1863', 'H4390', 'H4393', 'H8085', 'H6440',
        'G1944', 'G2671', 'G2672', 'G5351', 'G5356', 'G1311', 'G0173', 'G5146'}
SZO = {
    'H0779': 'az átok igéje, az אָרַר (árar)',
    'H0127': 'a föld, az אֲדָמָה (adámá)',
    'H6093': 'a fáradság szava, az עִצָּבוֹן (iccávón)',
    'H2555': 'az erőszak, a חָמָס (chámász)',
    'H7843': 'a romlás igéje, a שָׁחַת (sáchat)',
    'H6975': 'a tövis, a קוֹץ (kóc)',
    'H1863': 'a bogáncs, a דַּרְדַּר (dardar)',
}
FORDULAT = {
    'árar+adámá': 'az átok és a föld együttállása',
    'föld színe (H6440+H0127)': 'a „föld színe” fordulat (פְּנֵי הָאֲדָמָה, pené háadámá)',
    'málé+chámász': 'a „megtelt erőszakkal” szópár (מָלֵא + חָמָס, málé + chámász)',
    'kóc+dardar': 'a tövis és bogáncs szópárja (קוֹץ וְדַרְדַּר, kóc vedardar)',
}
GOROG = {  # nyelvközi és újszövetségi párok: a görög bizonyíték olvasói alakja (a TAGNT és a LXX mért szavai)
    ('1Móz 3:17', 'Zsid 6:7-8'): 'a görög Ószövetség itt az ἐπικατάρατος (epikataratosz), a Zsid 6:8 a κατάρα (katara) szót hozza, ugyanabból a szócsaládból',
    ('1Móz 3:18', 'Zsid 6:7-8'): 'a görög Ószövetség tövis és bogáncs szópárja, az ἄκανθα (akantha) és a τρίβολος (tribolosz) szó szerint áll a Zsid 6:8-ban',
    ('1Móz 6:11', 'Jel 19:2'): 'a görög Ószövetség romlás-igéje, a φθείρω (ftheiró) ugyanaz, mint a Jel 19:2-ben, és mindkettő a földre szól',
    ('1Móz 6:12', 'Jel 11:18'): 'a görög Ószövetség a καταφθείρω (kataftheiró), a Jel 11:18 a διαφθείρω (diaftheiró) igét hozza, mindkettő a φθείρω-családból',
    ('1Móz 6:13', 'Jel 11:18'): 'a görög Ószövetség a καταφθείρω (kataftheiró), a Jel 11:18 a διαφθείρω (diaftheiró) igét hozza, mindkettő a φθείρω-családból',
    ('1Móz 12:3', 'Gal 3:13-14'): 'a görög Ószövetség itt a καταράομαι (kataraomai) igét, a Gal 3:13 az ἐπικατάρατος (epikataratosz) és a κατάρα (katara) szót hozza, ugyanabból a szócsaládból',
    ('Jel 11:18', 'Jel 19:2'): 'a διαφθείρω (diaftheiró) és a φθείρω (ftheiró) ugyanabból a szócsaládból',
}
# beépülő pár -> (típus, funkció); a PaRDeS-szint minden soron Remez (a meglévő kapcsolat-sorok mintájára)
KEZI = {
    ('1Móz 3:14', '1Móz 4:10-11'): ('Párhuzam', 'az „átkozott vagy” kimondása: előbb a kígyóra, azután Kainra'),
    ('1Móz 3:16', '1Móz 3:17'): ('Párhuzam', 'a fáradság szava az asszony és a férfi ítéletében'),
    ('1Móz 3:16', '1Móz 4:7'): ('Variáns', 'a vágyódás és az uralkodás szava más szereposztásban: az asszony vágya a férfira, a bűn vágya Kainra'),
    ('1Móz 3:16', '1Móz 5:29'): ('Párhuzam', 'a fáradság szavának első és harmadik előfordulása'),
    ('1Móz 3:17', '1Móz 4:10-11'): ('Variáns', 'az átok és a föld felcserélt szerepben: a föld átkozott az ember miatt, Kain átkozott a föld felől'),
    ('1Móz 3:17', '1Móz 4:12'): ('Párhuzam', 'a föld művelése: a fáradságból Kainnál meddőség lesz'),
    ('1Móz 3:17', '1Móz 5:29'): ('Párhuzam', 'Lámek egy mondatban idézi vissza a 3:17 három szavát: az átkot, a földet és a fáradságot'),
    ('1Móz 3:17', '1Móz 8:21'): ('Kontraszt', 'a föld átka, majd az ígéret, hogy Isten többé nem átkozza meg a földet (más igével)'),
    ('1Móz 3:17', '5Móz 28:18'): ('Párhuzam', 'az átok és a föld a szövetség átkai között, a föld termésére'),
    ('1Móz 3:17', 'Ézs 24:5-6'): ('Párhuzam', 'a föld átka a lakói miatt, más átok-szóval'),
    ('1Móz 3:17', 'Hós 4:1-3'): ('Párhuzam', 'a lakók bűne miatt búsul a föld, a lánc szavai nélkül'),
    ('1Móz 3:17', 'Zsid 6:7-8'): ('Párhuzam', 'az átok a föld termésén: a Genezis ítélete és a levél példázata'),
    ('1Móz 3:17', 'Jel 22:3'): ('Kontraszt', 'a föld átka és a kánon zárómondata: semmi elátkozott nem lesz többé'),
    ('1Móz 3:18', 'Hós 10:8'): ('Párhuzam', 'a tövis és bogáncs az átkozott földön, majd Izrael oltárain'),
    ('1Móz 3:18', 'Zsid 6:7-8'): ('Párhuzam', 'a tövis és bogáncs mint a föld rossz termése, a példázatban'),
    ('1Móz 3:19', '1Móz 3:23'): ('Párhuzam', 'a föld, amelyből az ember vétetett: az ítéletben és a kiűzetésben'),
    ('1Móz 3:19', '1Móz 4:12'): ('Párhuzam', 'a föld az ember életének terhe; Kainnál megtagadja a termést'),
    ('1Móz 3:19', '1Móz 5:29'): ('Párhuzam', 'a föld mint az ember munkájának és életének terhe'),
    ('1Móz 3:23', '1Móz 4:12'): ('Párhuzam', 'a föld művelése a kiűzetés után és Kain büntetésében'),
    ('1Móz 4:10-11', '1Móz 5:29'): ('Párhuzam', 'az átok és a föld együtt: Kain átka a föld felől, Lámek szava a föld átkáról'),
    ('1Móz 4:12', '1Móz 4:14'): ('Párhuzam', 'a „bujdosó és vándorló” ítélet kimondása és Kain panaszában'),
    ('1Móz 4:12', '1Móz 5:29'): ('Párhuzam', 'a föld terhe Kain büntetésében és Lámek panaszában'),
    ('1Móz 4:14', '1Móz 6:7'): ('Párhuzam', 'a föld színéről: egy ember elűzése, majd minden élő eltörlése'),
    ('1Móz 5:29', '1Móz 7:23'): ('Párhuzam', 'Noé és a föld: a vigasztalás-várás, majd Noé megmaradása az eltörléskor'),
    ('1Móz 5:29', '1Móz 8:21'): ('Kontraszt', 'a föld, „melyet megátkozott az Úr”, és az ígéret, hogy többé nem átkozza meg'),
    ('1Móz 6:5', '1Móz 8:21'): ('Kontraszt', 'ugyanaz az indok, a szív gonosz gondolata: ott az ítélet, itt a kímélet oka'),
    ('1Móz 6:7', '1Móz 7:4'): ('Párhuzam', 'a föld színéről való eltörlés: a szándék és a napra kitűzött bejelentés'),
    ('1Móz 6:7', '1Móz 7:23'): ('Párhuzam', 'a 6:7 ítélete és végrehajtása, ugyanazzal a felsorolással'),
    ('1Móz 6:7', 'Hós 4:1-3'): ('Párhuzam', 'a mezei vad és az ég madarai az ítéletben'),
    ('1Móz 6:7', 'Sof 1:2-3'): ('Párhuzam', 'a föld színéről való eltörlés és a felsorolás (ember, barom, madár) a próféta ítéletében'),
    ('1Móz 6:11', '1Móz 6:13'): ('Párhuzam', 'a föld megtelt erőszakkal: az elbeszélő megállapítása és Isten szava'),
    ('1Móz 6:11', '1Móz 6:17'): ('Variáns', 'a romlás igéje: a föld megromlott, Isten elveszti'),
    ('1Móz 6:11', 'Zsolt 14:1'): ('Párhuzam', 'a romlás igéje az emberek egyetemes romlására'),
    ('1Móz 6:11', 'Ézs 60:18'): ('Kontraszt', 'az erőszakkal megtelt föld és a föld, amelyen többé nem hallatszik erőszak'),
    ('1Móz 6:11', 'Jer 6:7'): ('Párhuzam', 'az erőszak: a megtelt föld és a városban hallatszó erőszak'),
    ('1Móz 6:11', 'Ez 7:23'): ('Párhuzam', 'a „megtelt erőszakkal” szópár Jeruzsálemre'),
    ('1Móz 6:11', 'Ez 8:17'): ('Párhuzam', 'Júda háza megtölti a földet erőszakkal'),
    ('1Móz 6:11', 'Ez 12:19'): ('Párhuzam', 'a föld a lakói erőszaka miatt üresedik ki'),
    ('1Móz 6:11', 'Ez 28:16'): ('Párhuzam', 'a „megtelt erőszakkal” szópár egy uralkodóra'),
    ('1Móz 6:11', 'Hab 1:2'): ('Párhuzam', 'az erőszak: a megtelt föld és a próféta panasza'),
    ('1Móz 6:11', 'Jel 19:2'): ('Párhuzam', 'a föld megrontása: az özönvíz előtt és a nagy parázna ítéletében'),
    ('1Móz 6:12', '1Móz 6:13'): ('Variáns', 'ugyanaz az ige az emberre és Istenre: minden test megrontotta útját, Isten elveszti őket'),
    ('1Móz 6:12', '1Móz 6:17'): ('Variáns', 'ugyanaz az ige a vétekre és az özönvíz céljára'),
    ('1Móz 6:12', '1Móz 9:15'): ('Kontraszt', 'minden test megrontotta útját; nem lesz többé özönvíz minden test elvesztésére'),
    ('1Móz 6:12', 'Zsolt 14:1'): ('Párhuzam', 'ugyanaz az igealak (hif\'íl) az egyetemes romlásra'),
    ('1Móz 6:12', 'Jel 11:18'): ('Variáns', 'ugyanaz az ige a vétekre és az ítéletre: a föld megrontói és elpusztításuk'),
    ('1Móz 6:13', '1Móz 6:17'): ('Párhuzam', 'Isten kimondja az elvesztést, majd bejelenti az özönvizet'),
    ('1Móz 6:13', 'Ez 8:17'): ('Párhuzam', 'a föld megtelt erőszakkal: az özönvíz előtti ítélet és Júda háza'),
    ('1Móz 6:13', 'Ez 12:19'): ('Párhuzam', 'az erőszakkal megtelt földet éri az ítélet'),
    ('1Móz 6:13', 'Jel 11:18'): ('Párhuzam', 'Isten ítélete azokon, akik a földet megrontják'),
    ('1Móz 6:17', '1Móz 9:11'): ('Kontraszt', 'az özönvíz bejelentése a föld elvesztésére, majd a szövetség: soha többé'),
    ('1Móz 7:4', '1Móz 7:23'): ('Párhuzam', 'a föld színéről való eltörlés bejelentése és végrehajtása'),
    ('1Móz 12:3', 'Gal 3:13-14'): ('Párhuzam', 'Ábrahám áldása a nemzetekre: az ígéret és Pál áldás-mondata (határeset)'),
    ('Zsolt 14:1', 'Zsolt 53:2'): ('Párhuzam', 'ugyanaz a zsoltár-mondat kétszer, ugyanazzal az igealakkal'),
    ('Hós 4:1-3', 'Sof 1:2-3'): ('Párhuzam', 'a föld élőinek elvétele (mezei vad, ég madarai, tenger halai) a lakók bűne miatt'),
    ('Jel 11:18', 'Jel 19:2'): ('Párhuzam', 'a föld megrontóinak ítélete, a romlás szócsaládjával'),
}


def tsv(ut):
    sorok = open(ut, encoding='utf-8', newline='').read().split('\n')
    return sorok


def felsorol(lista):
    if len(lista) == 1:
        return lista[0]
    return ', '.join(lista[:-1]) + ' és ' + lista[-1]


def minosit(d):
    a, b, f = d['forras_sor'], d['cel_sor'], d['jelolt_forras']
    szav = [int(x) for x in re.findall(r'Votes=(\d+)', f)]
    mv = max(szav) if szav else 0
    proza, kh, ger = 'próza' in f, 'Károli-KH' in f, 'gerinc_elem' in f
    lanc = [x for x in d['kozos_lanc_strong'].split(',') if x]
    ford = [x for x in d['kozos_fordulat'].split(',') if x]
    hid = [x for x in d['lxx_hid'].split(',') if x and x != 'G1093']
    csal = d['gorog_szocsalad']
    szoszer = [x for x in d['kozos_tartalmi_strong'].split(',') if x and x not in KOZNAPI and x not in LANC]
    gen = a.startswith('1Móz') or b.startswith('1Móz')
    v = len(szoszer) >= 2
    if ford or len(lanc) >= 2 or len(hid) >= 2 or v:
        biz = 'magas'
    elif lanc or csal:
        biz = 'közepes' if (mv >= 3 or proza or kh) else 'alacsony'
    elif ger:
        biz = 'közepes'
    else:
        biz = None
    # indoklás-elemek (olvasói)
    elem = []
    if ford:
        elem.append(felsorol([FORDULAT[x] for x in ford]))
    lanc_nev = [SZO[x] for x in lanc if x in SZO and not (ford and x in ('H0127', 'H0779', 'H2555', 'H6975', 'H1863'))]
    if lanc_nev:
        elem.append('közös szavuk ' + felsorol(lanc_nev))
    if (a, b) in GOROG:
        elem.append(GOROG[(a, b)])
    if v:
        elem.append('a két helyen további %d szó szó szerint visszatér' % len(szoszer))
    mut = []
    if mv:
        mut.append('a TSK (%d szavazat)' % mv)
    if kh:
        mut.append('a Károli kereszthivatkozása')
    if proza:
        mut.append('a lap prózája')
    if ger and (lanc or csal or ford or v):
        mut.append('a tematikus sor megjelölése')
    if biz is None:
        dontes, ok = 'elutasítva', ('a két versben nincs közös lánc-szó, szópár, görög szócsalád vagy szó szerinti '
                                    'visszatérés; a kapcsolat csak tematikus rokonságon állna, a fölérendelt fogalom felé')
    elif biz == 'alacsony':
        dontes, ok = 'elutasítva', ('küszöb alatt: egy közös lánc-szó (%s), és a párt csak a TSK %d szavazata köti össze'
                                    % (felsorol([SZO.get(x, x) for x in lanc]) if lanc else 'görög szócsalád', mv))
    elif not gen and not v:
        dontes, ok = 'elutasítva', ('redundáns: a két hely közös szava vagy szópárja mindkettőt a genezisi forrásvershez '
                                    'köti, a kapcsolat ott áll; a köztük lévő él nem mond újat')
    else:
        dontes = 'beépítve'
        ok = None
    return dontes, biz, elem, mut, ok, ger and not (lanc or csal or ford or v)


def main(ir):
    sorok = tsv(JEL)
    fej = sorok[1].split('\t')
    uj_fej = fej[:8] + ['dontes', 'bizonyossag', 'tipus', 'indoklas']
    elso = sorok[0].split(' | döntés:')[0].rstrip()
    ki_jel = [elso + ' | döntés: naplok/F182_kapcsolat_dontes.py (%s)' % DT, '\t'.join(uj_fej)]
    kap_sorok = []
    latott = set()
    for l in sorok[2:]:
        if not l:
            continue
        d = dict(zip(fej, l.split('\t')))
        a, b = d['forras_sor'], d['cel_sor']
        dontes, biz, elem, mut, ok, csak_tem = minosit(d)
        if dontes == 'beépítve':
            assert (a, b) in KEZI, ('nincs kézi típus/funkció', a, b)
            latott.add((a, b))
            tipus, funk = KEZI[(a, b)]
            if csak_tem:
                ind = ('A tematikus sor („tematikus, nem lexikai” jelöléssel) a láncnak ezt a versét nevezi meg; közös '
                       'lánc-szó nincs.%s Innen a közepes bizonyosság.'
                       % ((' Összeköti még: %s.' % felsorol(mut)) if mut else ''))
            else:
                ind = ('Mért: %s. Összeköti: %s; innen a %s bizonyosság.'
                       % ('; '.join(elem), felsorol(mut), biz))
            ind = ind[0].upper() + ind[1:]
            ind += ' | %s | scope=manual | forras=%s (bizonyíték: TSK, Károli-KH, TAHOT, TAGNT, LXX; naplok/F182_kapcsolat.py) | ts=%s' % (DT, JEL, TS)
            kap_sorok.append((a, b, tipus, funk, biz, ind))
            ki_jel.append('\t'.join([d[k] for k in fej[:8]] + ['beépítve', biz, tipus, ind.split(' | ')[0]]))
        else:
            ki_jel.append('\t'.join([d[k] for k in fej[:8]] + ['elutasítva', biz or '', '', ok[0].upper() + ok[1:] + '.']))
    hiany = set(KEZI) - latott
    assert not hiany, ('kézi sor jelölt nélkül', hiany)
    # kapcsolatok.tsv
    eredeti = tsv(KAP)
    kfej = eredeti[1].split('\t')
    assert kfej == ['forras_igehely', 'cel_igehely', 'id', 'tipus', 'funkcio', 'bizonyossag', 'pardes_szint', 'indoklas'], kfej
    assert not any(l.split('\t')[2:3] == [ID] for l in eredeti[2:] if l), 'a HAMART-001-nek már van kapcsolat-sora'
    vegso = [l for l in eredeti]
    while vegso and vegso[-1] == '':
        vegso.pop()
    for a, b, tipus, funk, biz, ind in kap_sorok:
        vegso.append('\t'.join([a, b, ID, tipus, funk, biz, 'Remez', ind]))
    vegso.append('')
    nem_ures = [x for x in eredeti if x != '']
    assert vegso[:len(nem_ures)] == nem_ures, 'a meglévő sorok változnának'
    n_be = len(kap_sorok)
    n_el = len(ki_jel) - 2 - n_be
    from collections import Counter
    print('jelölt: %d · beépítve: %d (%s) · elutasítva: %d' % (
        len(ki_jel) - 2, n_be, dict(Counter(k[4] for k in kap_sorok)), n_el))
    print('típus:', dict(Counter(k[2] for k in kap_sorok)))
    if ir:
        open(JEL, 'w', encoding='utf-8', newline='').write('\n'.join(ki_jel) + '\n')
        open(KAP, 'w', encoding='utf-8', newline='').write('\n'.join(vegso))
        print('írva: %s, %s' % (JEL, KAP))
    else:
        print('(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
