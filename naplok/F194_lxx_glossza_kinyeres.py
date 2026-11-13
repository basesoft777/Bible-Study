#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F194_lxx_glossza_kinyeres.py -- F194.16: az ISTENTISZT-001 visszhang-rétegének második adag első keze (claude-opus-5-5).

1. A H7121 14 ószövetségi LXX-sora, amelyet a `megfelelo_kinyer.py lxx` nem tudott eldönteni (N-F194e: az ἐπικαλέω és
   az ὄνομα a szópár miatt azonos súllyal áll): modell-kinyerés a `konkordancia/LXX_OS` versszövegéből (a HAMART-001
   1Móz 3:23, 4:12, 9:15 sorainak mintájára, `kinyeres=modell`). Kimenet: `naplok/F194_lxx_kinyert.tsv`.
2. A Glossa Ordinaria átnézése a 15 Remez-helyen (K67d: tanú csak Remez/Sod-helyen; a HAMART-001 F183 mintája):
   helyenkénti nyom `naplok/F194_glossza_atnezes.tsv`, és a 2Móz 33:19 latin tanújelöltje `naplok/F194_glossza_kinyert.tsv`
   (a második kéz elvetette, a táblába nem kerül).

A szöveg (alak, megjegyzés, kapcsolat) a kinyerő munkája, a szkript csak rögzíti és a forrásban ellenőrzi: minden nem
üres alak szó szerint áll az LXX_OS versében, különben megáll. A második kéz külön fut (claude-sonnet-5-5).
TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = '2026-11-12'
MODELL = 'claude-opus-5-5'
MOT = 'ISTENTISZT-001'

M_OSZL = ['motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas', 'megjegyzes',
          'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
T_OSZL = ['motivum', 'igehely', 'tanu_hely', 'hagyomany', 'tanu', 'mu', 'kor', 'kapcsolat', 'forras', 'forras_url',
          'lekerdezve', 'biblindex', 'kinyeres', 'modell', 'ellenorzes', 'proveniencia']

EPI = ('ἐπικαλέω', 'epikaleó', 'segítségül hív')

# (igehely, alak, lemma, kiejtés, jelentés, megjegyzés)
LXX = [
    ('1Móz 4:26', 'ἐπικαλεῖσθαι') + EPI + (
        'a görög fordító a héber „akkor kezdték” helyén azt mondja, hogy Énós „remélte” (ἤλπισεν, élpiszen) '
        'segítségül hívni az Úr nevét: a mondat alanya maga Énós, a segítségül hívás szava viszont a formuláé',),
    ('1Móz 12:8', 'ἐπεκαλέσατο') + EPI + (
        'Ábrám az oltárnál hívja segítségül az Urat; a név elöljárós alakban áll (ἐπὶ τῷ ὀνόματι κυρίου, '
        'epi tó onomati küriú, „az Úr nevén”), a pátriárka-helyek közül csak itt',),
    ('1Móz 13:4', 'ἐπεκαλέσατο') + EPI + (
        'ugyanaz az ige és ugyanaz a tárgyas szerkezet (τὸ ὄνομα κυρίου), mint az 1Móz 21:33-ban és a 26:25-ben '
        '(a 12:8-ban elöljárós alak áll); az ige és a tárgy közé a hely (ἐκεῖ, ekei) és az alany (Αβραμ, Abram) kerül',),
    ('1Móz 21:33', 'ἐπεκαλέσατο') + EPI + (
        'a név mellett az isteni jelző is megmarad: θεὸς αἰώνιος (theosz aióniosz, „örökkévaló Isten”), '
        'a héber אֵל עוֹלָם (él olám) megfelelője',),
    ('1Móz 26:25', 'ἐπεκαλέσατο') + EPI + (
        'Izsák oltáránál ugyanaz az ige és ugyanaz a tárgy áll (ἐπεκαλέσατο τὸ ὄνομα κυρίου), mint Ábrahámnál '
        'az 1Móz 13:4-ben és a 21:33-ban; itt a tárgy közvetlenül az ige után következik',),
    ('1Kir 18:24', 'βοᾶτε · ἐπικαλέσομαι', 'βοάω · ἐπικαλέω', 'boaó · epikaleó', 'kiált · segítségül hív',
     'a versben kétszer áll a héber hívás-ige; a görög fordító kettéválasztja: a Baál-próféták hívását a kiáltás '
     'igéje (βοᾶτε, boate), Illésének segítségül hívását az ἐπικαλέσομαι adja vissza'),
    ('1Kir 18:25', 'ἐπικαλέσασθε') + EPI + (
        'Illés felszólítása a Baál-prófétákhoz: itt már a segítségül hívás igéje áll, egyes számú „istenetek” '
        'nevével (ἐν ὀνόματι θεοῦ ὑμῶν, en onomati theú hümón)',),
    ('1Kir 18:26', 'ἐπεκαλοῦντο') + EPI + (
        'folyamatos múlt idő: a Baál-próféták reggeltől délig hívják segítségül a Baál nevét (ἐν ὀνόματι τοῦ Βααλ)',),
    ('2Kir 5:11', 'ἐπικαλέσεται') + EPI + (
        'Naámán elvárása; a görög szövegben a név után csak „az ő Istene” áll (ἐν ὀνόματι θεοῦ αὐτοῦ), az Úr '
        'neve (κυρίου) nem, holott a héber „az Úr, az ő Istene” nevét mondja',),
    ('Jóel 2:32', 'ἐπικαλέσηται') + EPI + (
        'a görög számozás szerint Jóel 3:5; ezt a görög mondatot idézi szó szerint az ApCsel 2:21 és a Róm 10:13 '
        '(πᾶς ὃς ἂν ἐπικαλέσηται τὸ ὄνομα κυρίου)',),
    ('Sof 3:9', 'ἐπικαλεῖσθαι') + EPI + (
        'Isten nyelvet (γλῶσσαν, glósszan) fordít a népek felé, hogy mindnyájan (πάντας, pantasz) segítségül hívják '
        'az Úr nevét; a héber „tiszta” jelzőjének a görög versben nincs megfelelője',),
    ('Zsolt 116:4', 'ἐπεκαλεσάμην') + EPI + (
        'a görög számozás szerint Zsolt 114:4; a zsoltáros első személyben hívja segítségül az Úr nevét',),
    ('Zsolt 116:13', 'ἐπικαλέσομαι') + EPI + (
        'a görög számozás szerint Zsolt 115:4; a szabadulás poharánál jövő idejű fogadalom: segítségül hívom az Úr nevét',),
    ('Zsolt 116:17', '', '', '', '',
     'hiány: az LXX_OS versében (görög számozással Zsolt 115:8) csak a vers első fele áll (σοὶ θύσω θυσίαν αἰνέσεως, '
     'szoi thüszó thüszian aineszeósz, „neked áldozom a dicséret áldozatát”); a segítségül hívás mondata ebben a '
     'szövegben nincs meg, ezért megfelelő szó sincs'),
]

# A Glossa átnézése a 15 Remez-helyen: (igehely, Glossa-kulcs, jegyzet_db, ítélet)
GLOSSZA = [
    ('1Kir 18:24', '1Kir 18:24', 0, 'nincs jegyzet'),
    ('1Kir 18:25', '1Kir 18:25', 0, 'nincs jegyzet'),
    ('1Kir 18:26', '1Kir 18:26', 0, 'nincs jegyzet'),
    ('2Kir 5:11', '2Kir 5:11', 0, 'nincs jegyzet'),
    ('Sof 3:9', 'Sof 3:9', 0, 'nincs a forrásban: a Glossa-fájl a kispróféták könyveit nem tartalmazza'),
    ('Zsolt 116:4', 'Zsolt 114:4, Zsolt 114:5', 2,
     'nem tanú: a Glossa zsoltárkulcsai egy verssel el vannak tolva, ezért mindkét szomszédos kulcs átnézve; a '
     '114:4 jegyzete a szorongatás és a fájdalom hasznáról, a 114:5-é a szabadításért kiáltó könyörgésről és az Úr '
     'irgalmáról szól; az Úr nevét és a formulát egyik sem érinti'),
    ('Zsolt 116:13', 'Zsolt 115:3, Zsolt 115:4', 1,
     'nem tanú: a vers jegyzete a 115:3 kulcson áll (a szabadulás pohara mint a szenvedés képe), a segítségül '
     'hívásról nem szól'),
    ('Zsolt 116:17', 'Zsolt 115:7, Zsolt 115:8', 2,
     'nem tanú: a 115:7 jegyzete a bilincsek széttöréséről, a 115:8-é a következő vers fogadalmáról szól; a '
     'segítségül hívásról egyik sem'),
    ('Jóel 2:32', 'Jóel 2:32', 0, 'nincs a forrásban: a Glossa-fájl a kispróféták könyveit nem tartalmazza'),
    ('1Kor 1:2', '1Kor 1:2', 1, 'nem tanú: a jegyzet a levél címzettjeiről szól (Korinthus környéke), a név '
     'segítségül hívásáról nem'),
    ('ApCsel 22:16', 'ApCsel 22:16', 0, 'nincs jegyzet'),
    ('2Móz 33:19', '2Móz 33:19', 1, 'nem tanú: az Ágoston-jegyzet (quaest. 154) a cselekvő igealakot magyarázza, '
     'és csak feltételesen olvassa bele, hogy az Urat minden nép hívja; a nevet és a formula szerkezetét nem '
     'érinti (a tanújelöltet a második kéz elvetette, naplok/F194_glossza_tanu_atnezes.tsv)'),
    ('2Móz 34:5', '2Móz 34:5', 0, 'nincs jegyzet'),
    ('ApCsel 2:21', 'ApCsel 2:21', 0, 'nincs jegyzet'),
    ('Róm 10:13', 'Róm 10:13', 0, 'nincs jegyzet'),
]

TANU = {
    'motivum': MOT, 'igehely': '2Móz 33:19', 'tanu_hely': '2Móz 33:19', 'hagyomany': 'latin',
    'tanu': 'Glossa Ordinaria',
    'mu': 'Glossa Ordinaria, jegyzet a 2Móz 33:19-hez (AUG., quaest. 154 jelzéssel; Migne, 1880)', 'kor': '',
    'kapcsolat': 'Ágoston nyomán megjegyzi, hogy Isten itt szokatlan módon cselekvő igét mond a szenvedő helyett, '
                 'és ebben azt látja, hogy maga Isten éri el kegyelmével, hogy minden nép között az Urat hívják.',
    'forras': 'glossa', 'forras_url': 'https://ebible.org/Scriptures/latVUC_usfm.zip', 'lekerdezve': TS,
    'biblindex': '', 'kinyeres': 'modell', 'modell': MODELL, 'ellenorzes': '',
    'proveniencia': 'scope=Glossa_Ordinaria.tsv 2Móz 33:19 (sorszam 1) | forras=konkordancia/Glossa_Ordinaria.tsv '
                    '(eBible latVUC, sha256=5d73ce3473e40b70cfcc976b967e0f259cbb031d6c0cd4f9798fbabf9f5b4e6c; '
                    'Public Domain) | ts=' + TS,
}


def lxx_versek():
    d, fajl = {}, {}
    k = os.path.join(GYOKER, 'konkordancia', 'LXX_OS')
    for f in sorted(os.listdir(k)):
        if not f.endswith('.tsv'):
            continue
        fej = None
        with open(os.path.join(k, f), encoding='utf-8') as h:
            for s in h:
                if s.startswith('#'):
                    continue
                c = s.rstrip('\r\n').split('\t')
                if fej is None:
                    fej = c
                    continue
                r = dict(zip(fej, c))
                v = r.get('igehely_karoli', '')
                d.setdefault(v, []).append(r.get('szoalak', ''))
                fajl.setdefault(v, f)
    return d, fajl


def glossza_db():
    d = {}
    with open(os.path.join(GYOKER, 'konkordancia', 'Glossa_Ordinaria.tsv'), encoding='utf-8') as h:
        for s in h:
            c = s.rstrip('\r\n').split('\t')
            d[c[0]] = d.get(c[0], 0) + 1
    return d


def ir(ut, oszl, sorok, fejsor=None):
    with open(os.path.join(GYOKER, ut), 'w', encoding='utf-8', newline='\n') as h:
        if fejsor:
            h.write(fejsor + '\n')
        h.write('\t'.join(oszl) + '\n')
        for r in sorok:
            h.write('\t'.join(r[o] for o in oszl) + '\n')


def main():
    versek, fajl = lxx_versek()
    ki = []
    for hely, alak, lemma, kiejt, jel, megj in LXX:
        szavak = versek.get(hely)
        if not szavak:
            raise SystemExit('HIBA: nincs LXX_OS-vers: %s' % hely)
        for a in [x.strip() for x in alak.split('·') if x.strip()]:
            if a not in szavak:
                raise SystemExit('HIBA: az alak nem áll a versben: %s %s' % (hely, a))
        ki.append({
            'motivum': MOT, 'strong': 'H7121', 'igehely': hely, 'forras': 'lxx', 'alak': alak, 'lemma': lemma,
            'kiejtes': kiejt, 'jelentes': jel, 'betoldas': 'nem', 'megjegyzes': megj, 'kinyeres': 'modell',
            'modell': MODELL, 'ellenorzes': '',
            'proveniencia': 'scope=K66 modell-kinyerés: LXX_OS versszöveg + TAHOT (a gépi kinyerés nem volt '
                            'egyértelmű, N-F194e) | forras=konkordancia/LXX_OS/%s (lxx-morph, CC BY 4.0) | ts=%s'
                            % (fajl[hely], TS),
        })
    ir('naplok/F194_lxx_kinyert.tsv', M_OSZL, ki)
    db = glossza_db()
    nyom = []
    for hely, kulcs_, n, itelet in GLOSSZA:
        van = sum(db.get(k.strip(), 0) for k in kulcs_.split(','))
        if van != n:
            raise SystemExit('HIBA: a Glossa-jegyzetek száma eltér: %s (%s): %d ≠ %d' % (hely, kulcs_, van, n))
        nyom.append({'igehely': hely, 'pardes_szint': 'Remez', 'glossza_kulcsok': kulcs_, 'jegyzet_db': str(n),
                     'itelet': itelet})
    ir('naplok/F194_glossza_atnezes.tsv', ['igehely', 'pardes_szint', 'glossza_kulcsok', 'jegyzet_db', 'itelet'], nyom,
       '# F194 — a Glossa Ordinaria átnézése az ISTENTISZT-001 15 Remez-helyén (K67d; a HAMART-001 F183 mintája). '
       'Forrás: konkordancia/Glossa_Ordinaria.tsv; a zsoltároknál a Vulgata számozása. Ítélet: %s (kinyerő), %s. '
       'A Drash-szintű 5 hely (1Móz 4:26, 12:8, 13:4, 21:33, 26:25) a K67d szerint nem kap tanút.' % (MODELL, TS))
    ir('naplok/F194_glossza_kinyert.tsv', T_OSZL, [TANU])
    print('LXX: %d sor (alakkal %d); Glossa: %d hely, ebből jegyzet %d, tanú 0'
          % (len(ki), sum(1 for r in ki if r['alak']), len(nyom), sum(1 for r in nyom if r['jegyzet_db'] != '0')))


if __name__ == '__main__':
    main()
