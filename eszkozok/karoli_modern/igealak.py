#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.2 — a modernizált Károli-réteg igealak-lépcsője és a *vala* (DT128, DT-F96d, DT-F96e c, DT-F96f).

A .1 (helyesírás, `helyesiras.py`) kimenetére épül: a .1-et a saját függvényeivel újraszámolja, és
összeveti a kiadott `adat/karoli_modern/helyesiras_tokenek.tsv`-vel; eltérésnél megáll, és nem ír.
Determinisztikus, API és Hunspell nélkül. Az LLM-es ellenőrzés (DT-F96d: az előfizetésből, Claude
Code-ból, API nélkül) külön lépés: a `--llm-kerdes` kiírja a kérdéseket (repón kívülre), a modell
válaszait a `--llm-valasz` olvassa be az `adat/karoli_modern/igealak_llm.tsv`-be; a generátor ezt
csak olvassa, a tő-őrön át.

Csak olvas: `konkordancia/Karoli_1908.tsv`, `adat/szoto/karoli_szotari_alak.tsv` (#94),
`adat/karoli_modern/helyesiras_tokenek.tsv` (.1), `adat/karoli_modern/igealak_llm.tsv` (ha van).
A tokenizálás a `tokenizal` (a #22 `hu_sorszam`-a): a réteg Strongot nem tárol (DT-F96f).

Alakszintű döntés (az osztály a `fedettseg.py osztalyoz` szerint):

  igealak_gyakori   régies jegy a 200 leggyakoribb jegyes alakon (DT140): a jegy szerinti mai alak,
                    automatikus csere (a hibás jegyű és rosszul képzett alak a KEZI táblában)
  regies_lista      lőn → lett, lőnek → lettek, vagyon → van (névelő után főnév, marad), a vala-család
                    tokenszinten (l. lent)
  regies_gyanu_kezi a jegy nélküli régies alakok kézzel átnézett, gyakori része (GYANU_KEZI: jő → jön,
                    mondák → mondták …; N-F96b): automatikus csere
  igealak_ritka,    jelölt (N-F94h: a ritka alak jegye ~6%-ban hibás): a szabály, a sonnet és az opus
  regies_gyanu      jelöltje a `jelolt` oszlopban; a modern szöveg a DT-F96l szerint változik, ha kettő
                    egyezik és a tő-őr átengedi
  felszolito.E2     -jál/-jél → -j: nem cserél (DT-F96k a), jelölt
  kotohang_mult     mondotta → mondta (DT-F96k b); mult_E1_targyas: mondám → mondtam (N-1); ok_birtokos:
                    szívök → szívük (DT-F96p)

Tokenszintű döntés:

  vala-család       létigei → volt / voltak / voltam …; segédigei (közvetlenül előtte, egy szóközzel,
                    véges igealak) → kiesik (`kieso=segedige`): ha az ige jelen idejű, múlt időbe kerül
                    (lebeg vala → lebegett, mondja vala → mondta); ha múlt idejű, csak a vala esik ki;
                    ha a jelen idő nem elemezhető, mindkettő marad (`bizonytalan=vala_segedige`).
                    Igenév után (írva vala) létigei: volt.
  tárgyas/alanyi    a T/3, E/2, T/1, T/2 régies alakja a ragozást nem jelöli: határozott tárgy a
                    tagmondatban (azt, ezt, őt, őket, a/az + -t, birtokos -t, utána „, hogy”) → tárgyas;
                    különben alanyi; a mond mindig tárgyas (DT128: monda → mondta)
  -ék E/1 vagy T/3  magas hangrendű igén (kérék): E/1, ha a tagmondatban E/1 névmás áll (én, engem, nekem …),
                    vagy a token mondatszakaszában (.;:!? között) E/1 igealak (mondám, valék, vagyok) vagy
                    előtte E/1 névmás, a birtokos „az én” nélkül (N-F96f); a tárgyatlan felelék, -jövék mindig
                    E/1; különben T/3 tárgyas (`bizonytalan=ek_E1_T3`)
  3. kör (DT-F96q)  a modern szövegben változatlanul maradt régies alak (regies_szken.py, igealak_llm_kor3.tsv):
                    ha az opus és a szabály-jelölt egyezik, és a tő-őr átengedi → csere (`kor3:szabaly+opus`);
                    szabály-jelölt nélkül a tő-őrön átment opus-alak cserél (`kor3:opus`,
                    `bizonytalan=kor3_csak_opus`); eltérésnél jelölt marad (`jelolt`: kor3_szabaly, kor3_opus).
                    A létigeinek vett vala előtti igén az opus dönt (szabály-jelölt nincs): a vala kiesik
                    (`vala_segedige_kor3`, `bizonytalan=kor3_csak_opus`); a homográf (mert) csak tagadószó után
  4. kör (DT-F96r)  ugyanígy az igealak_llm_kor4.tsv-ből (`kor4:…`, `kor4_csak_opus`), a .1 utáni alakon, a .2
                    döntése nélküli tokenen (a .1-ben változott tokenen a tő-őr a .1 utáni alakon is mér); a
                    `vala_nem_elemezheto` vala is (létige → volt); a `jelolt` típus a DT-F96l opus-szavazata, ahol
                    az igealak_llm_opus.tsv nem szavazott. A .1 cseréje a .2 eredményén is (h1_atvisz: reáveté →
                    rávetette, nem reávetette)
  5. kör (DT-F96u)  tokenszintű opus-válasz a teljes verssel (igealak_llm_kor5.tsv): csere, ha egy meglévő
                    jelölttel egyezik és a tő-őr átengedi (`kor5:token_opus+meglevo`, `bizonytalan=token_opus`)
  jelölt-kör        (DT-F96s) ha a szabály-jelölt a korpuszban nem áll, az opus-alak igen, és a tő-őr átengedi:
                    az opus-alak cserél (`…:opus_tanusitott`, `bizonytalan=szabaly_nem_tanusitott`; kizárva az
                    -á/-é nem -a/-e végű, az E/1-környezetű -ék nem E/1 alakja és a -nd- jövő); a szavazás előtt a
                    .1 cseréje a jelölteken is; a sonnet–opus T/3 alanyi–tárgyas pár a tagmondat szerint
                    (`tobbseg:alanyi_targyas`)

Önellenőrzés (K2): a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern alakjait
adja, sorrendben; a nem-betű váz a kieső tokenek egy-egy szóközén kívül változatlan.

Ír (generált, kézzel nem szerkeszthető):
  adat/karoli_modern/igealak_alakok.tsv    alakonként: osztály, jegy, szabály-jelölt, LLM-jelölt, döntés
  adat/karoli_modern/igealak_tokenek.tsv   a .1 + .2 után változó, kieső, bizonytalan vagy jelölt tokenek; a
                                           kieső token `kieso_gazda` oszlopa a gazdaszó sorszáma (DT-F96o)
  adat/karoli_modern/igealak_minta.tsv     rögzített magú minta (--minta; --minta-frissit)
  adat/karoli_modern/igealak_minta2.tsv    a lefedettséget is mérő minta (N-F96g; --minta2; --minta-frissit)

Használat:
    python eszkozok/karoli_modern/igealak.py
    python eszkozok/karoli_modern/igealak.py --minta | --minta2 | --minta-frissit
    python eszkozok/karoli_modern/igealak.py --kimenet <könyvtár>          (próba a repón kívülre)
    python eszkozok/karoli_modern/igealak.py --llm-kerdes <könyvtár> [--koteg N]
    python eszkozok/karoli_modern/igealak.py --llm-valasz <könyvtár> --modell <név>
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_modern'))
import tokenek  # noqa: E402
import fedettseg  # noqa: E402
import helyesiras  # noqa: E402
import igeragozas as ir  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KAROLI = fedettseg.KAROLI
SZOTARI = fedettseg.SZOTARI
KI_DIR = os.path.join('adat', 'karoli_modern')
H_TOKENEK = os.path.join(KI_DIR, 'helyesiras_tokenek.tsv')
LLM_TABLA = os.path.join(KI_DIR, 'igealak_llm.tsv')
LLM_NAPLO = os.path.join(KI_DIR, 'igealak_llm_hivasok.jsonl')
# A második, opus-ellenőrzés a vitatott alakokon (a szabály és a sonnet nem egyezik, vagy a tő-őr bukott)
LLM2_TABLA = os.path.join(KI_DIR, 'igealak_llm_opus.tsv')
LLM2_NAPLO = os.path.join(KI_DIR, 'igealak_llm_opus_hivasok.jsonl')
# A 3. ellenőri kör (N-F96d/e, DT-F96q): a régies-szken kérdései, szabály-jelöltje és az opus válasza
# (regies_szken.py --llm-valasz)
KOR3_TABLA = os.path.join(KI_DIR, 'igealak_llm_kor3.tsv')
# A 4. kör (DT-F96r, 2. opció): a 3. kör után mért kihagyás-osztályok; a kulcs a .1 utáni alak; a `jelolt` típus a
# DT-F96l többségének opus-szavazata, ahol az igealak_llm_opus.tsv nem szavazott
KOR4_TABLA = os.path.join(KI_DIR, 'igealak_llm_kor4.tsv')
# Az 5. kör (DT-F96u, 1. opció): tokenszintű opus-válasz a teljes verssel; kulcs: (igehely, sorszám)
KOR5_TABLA = os.path.join(KI_DIR, 'igealak_llm_kor5.tsv')
SZKRIPT = 'eszkozok/karoli_modern/igealak.py'
MODUL = 'eszkozok/karoli_modern/igeragozas.py'
MAG = 20261024
BETU = helyesiras.BETU

JEGY_SZEM = {
    'mult.alanyi.E3': ('E3', False), 'mult.targyas.E3': ('E3', True), 'mult.E3': ('E3', False),
    'mult.E1': ('E1', None), 'mult.E2': ('E2', None), 'mult.T1': ('T1', None), 'mult.T2': ('T2', None),
    'mult.T3': ('T3', None),
}
VALA = {'vala': ('E3', 'volt'), 'valának': ('T3', 'voltak'), 'valék': ('E1', 'voltam'),
        'valál': ('E2', 'voltál'), 'valánk': ('T1', 'voltunk'), 'valátok': ('T2', 'voltatok')}
LON = {'lőn': 'lett', 'lőnek': 'lettek'}
TARGYAS_MINDIG = {'mond'}  # DT128: monda → mondta (az idézett beszéd tárgy)
HATAROZOTT_TARGY = {'azt', 'ezt', 'őt', 'őket', 'magát', 'magokat', 'magukat', 'azokat', 'ezeket', 'mindazt',
                    'amazt', 'önmagát', 'mindezt', 'mindazokat', 'mindezeket', 'magamat', 'magadat'}
BIRTOKOS_TARGY = re.compile(r'(ját|jét|mat|met|dat|det|nkat|nket|tokat|teket|ukat|üket|jukat|jüket|'
                            r'imat|imet|idat|idet|ait|eit|jait|jeit)$')
# N-F96f: a versben álló, egyértelmű E/1 igealak (az -ék E/1 vagy T/3 választásához; felelék … mondám)
E1_IGE = {'valék', 'vagyok', 'leszek', 'lészek', 'voltam', 'valám'}
# N-F96f: a tárgyatlan ige -ék alakja mindig E/1 (a T/3 tárgyas felelték, eljötték nem lehetséges; a T/3 alanyi
# régies alakja -ének): felelék → feleltem, eljövék → eljöttem
E1_MINDIG_VEG = ('felelék', 'jövék')
# A 3. kör vala-párjai alakszintűek; a homográf ige csak a tagadószó után ige (nem mert vala → nem mert; a „Mert
# vala néki …” kötőszó)
KOR3_VALA_HOMOGRAF = {'mert': ('nem', 'sem', 'se')}
E1_JEL = {'én', 'engem', 'nekem', 'nékem', 'velem', 'tőlem', 'hozzám', 'bennem', 'belőlem', 'rám', 'reám',
          'rólam', 'előttem', 'magam', 'magamat', 'enyém', 'nálam', 'értem', 'utánam', 'ellenem', 'mellettem',
          # ELLENOR_F96 4. kör, 1.: a visszaható E/1 névmás ragos alakjai is E/1 jelzők (Préd 2:5 építék magamnak
          # házakat → építettem, nem építették)
          'magamnak', 'magamban', 'magamba', 'magamra', 'magamhoz', 'magammal', 'magamtól', 'magamért', 'magamról',
          'magamnál', 'magamon', 'magamból'}
MAGAM_E1 = {w for w in E1_JEL if w.startswith('magam')}
# A „nyíllal lőnek” (lő ige, nem lőn → lettek) kivétele: a vers egy szava a nyíl/íj szócsaládból, egész szóként
# (ELLENOR_F96 4. kör, 3.: a részszó-keresés a megnyilatkozék szóra is illeszkedett, Jel 11:19); a nyílik, nyilt,
# nyilván, nyílás és a megnyilatkoz- nem tartozik ide
NYIL_IJ = re.compile(r'(?:nyíl|nyil)(?:a|ai|aid|aidat|aim|aimat|ait|aival|ak|akat|akba|akkal|aknak|at|át|lal|lá|tól|'
                     r'okat|azók|asok|lövésnyi)?|(?:íj|íjj|ijj)(?:at|ját|aim|im|dal|ász|ászok|ászai|ászokhoz|ászszá)?')
# A fedettseg.igei_tovek próbáján igeinek látszó, de vala előtt névszói szavak (köz → között, hely → helyett).
NEM_IGE = {'köz', 'hely', 'nyíl', 'erős', 'fel', 'meg', 'el', 'körül', 'szerint', 'mellett', 'között', 'mell', 'ala',
           'felett', 'alatt', 'előtt', 'helyett', 'ott', 'itt', 'fia', 'fiai', 'neve', 'feje'}

# A gyakori jegyes alakok kézi felülbírálása (modell-átnézés, F96.2): alak (kisbetűs) → mai alak, vagy
# None = a jegy hibás (nem régies igealak, nem változik). A szabály jelöltje itt nem jó.
KEZI = {
    'megkérdé': 'megkérdezte',  # a #94 lemmája: megkérd; a mai ige megkérdez
    'áldozék': 'áldozott',  # áldozik, E/3 (1Móz 8:20: és áldozék égőáldozattal)
    'eltemeték': 'eltemették',  # eltemet, T/3 tárgyas (1Móz 25:9: eltemeték őt ... az ő fiai)
    'eltemetteték': 'eltemettetett',  # szenvedő E/3 (1Móz 35:19: és eltemetteték)
    'megjelenék': 'megjelent',  # megjelenik, E/3 (1Móz 12:7: megjelenék az Úr)
    'érte': None,  # névutós névmás (érte = őérte), a jegy hibás
    'hivatá': 'hívatta',  # hivat → hívat (helyesírás) + tárgyas E/3
}
# A jegy nélküli régies gyanú (regies_gyanu) kézzel átnézett, gyakori alakjai (N-F96b): kisbetűs → mai.
GYANU_KEZI = {
    # jő-család (jön régies alakja) és a lészen (lesz)
    'jő': 'jön', 'eljő': 'eljön', 'kijő': 'kijön', 'feljő': 'feljön', 'bejő': 'bejön', 'jőnek': 'jönnek',
    'eljőnek': 'eljönnek', 'jőjjön': 'jöjjön', 'jőjj': 'jöjj', 'jőjjenek': 'jöjjenek',
    'lészen': 'lesz', 'meglészen': 'meglesz', 'lésznek': 'lesznek',
    # vőn, tőn (vesz, tesz régi múltja)
    'vőn': 'vett', 'tőn': 'tett', 'vőnek': 'vettek', 'tőnek': 'tettek',
    # -ák: tárgyas T/3 elbeszélő múlt (a #94 értékkészletéből hiányzik, N-F96b)
    'mondák': 'mondták', 'megmondák': 'megmondták', 'elmondák': 'elmondták', 'adák': 'adták',
    'találák': 'találták', 'láták': 'látták', 'megláták': 'meglátták', 'hallák': 'hallották',
    'meghallák': 'meghallották', 'elhozák': 'elhozták', 'kihozák': 'kihozták', 'előhozák': 'előhozták',
    'akarák': 'akarták', 'elbocsáták': 'elbocsátották', 'hagyák': 'hagyták', 'állíták': 'állították',
    'meghajták': 'meghajtották', 'elfoglalák': 'elfoglalták', 'megfogák': 'megfogták', 'imádák': 'imádták',
    'hányák': 'hányták', 'csinálák': 'csinálták',
    # alanyi E/3 és T/3 elbeszélő múlt jegy nélkül
    'álla': 'állt', 'állának': 'álltak', 'síra': 'sírt', 'sírának': 'sírtak', 'tére': 'tért',
    # v-tövű és szenvedő elbeszélő múlt
    'megharaguvék': 'megharagudott', 'megesküvék': 'megesküdött', 'elaluvék': 'elaludt', 'feküvék': 'feküdt',
    'lefeküvék': 'lefeküdt', 'találtaték': 'találtatott', 'vetteték': 'vettetett',
    'várván': 'várva',
    # a fedettség „valtozatlan/lexikon” osztályába sorolt, de régies igealakok: az ejendő-család
    # (eszik: 1Móz 2:17, 3:5; 2Móz 12:15, 19), a -éndik/-endenek feltételes jövő (jelen idejűre), a -teték/-aték
    # szenvedő és a -ának/-ének T/3 elbeszélő múlt, a vevén-típusú határozói igenév
    'ejéndel': 'eszel', 'ejéndetek': 'esztek', 'ejéndik': 'eszik',
    'imádkozándik': 'imádkozik', 'könyörgéndenek': 'könyörögnek', 'megtéréndenek': 'megtérnek',
    'megtérendenek': 'megtérnek', 'megtéréndetek': 'megtértek', 'megtérendetek': 'megtértek',
    'teéndenek': 'tesznek', 'elviéndik': 'elviszik', 'viendik': 'viszik', 'vétkezéndenek': 'vétkeznek',
    'vétkezéndik': 'vétkezik', 'vétkezendik': 'vétkezik', 'megőrizéndik': 'megőrzik', 'hiendenek': 'hisznek',
    'leendenek': 'lesznek',
    'bevégezteték': 'bevégeztetett', 'végezteték': 'végeztetett', 'erősítteték': 'erősíttetett',
    'feldolgoztaték': 'feldolgoztatott', 'felriasztaték': 'felriasztatott',
    'elhányattaték': 'elhányattatott', 'eltávolíttaték': 'eltávolíttatott', 'igazoltaték': 'igazoltatott',
    'eltapostaték': 'eltapostatott', 'taníttaték': 'taníttatott', 'elárultaték': 'elárultatott',
    'elmozdíttaték': 'elmozdíttatott', 'megemlítteték': 'megemlíttetett',
    'felveheték': 'felvehették', 'készítheték': 'készíthették', 'végezheték': 'végezhették',
    'kiteregeték': 'kiteregették', 'kérdezgeték': 'kérdezgették', 'begöngyölgeték': 'begöngyölgették',
    'tetteték': 'tették', 'megvesszőzteték': 'megvesszőzték',
    'hálának': 'háltak', 'elindúlának': 'elindultak', 'borúlának': 'borultak', 'leborúlának': 'leborultak',
    'eredének': 'eredtek', 'megállapodának': 'megállapodtak', 'megzavarodának': 'megzavarodtak',
    'megoldódának': 'megoldódtak', 'elhagyatvák': 'elhagyattak',
    # -ándod/-éndesz-féle E/1, E/2 feltételes jövő (jelen idejűre)
    'mondándok': 'mondok', 'menéndek': 'megyek', 'visszamenéndek': 'visszamegyek', 'hozándok': 'hozok',
    'bocsátandok': 'bocsátok', 'nyomorgatándod': 'nyomorgatod', 'megtartándod': 'megtartod', 'adándod': 'adod',
    'hallándod': 'hallod', 'keresénded': 'keresed', 'elhagyándod': 'elhagyod', 'helyezénded': 'helyezed',
    'megtanítándod': 'megtanítod', 'elvetended': 'elveted', 'megcselekedénded': 'megcselekszed',
    'cselekedénded': 'cselekszed', 'imádkozándanak': 'imádkoznak',
    'menéndesz': 'mész', 'elmenéndesz': 'elmész', 'kimenéndesz': 'kimész', 'általmenéndesz': 'általmész',
    'járándasz': 'jársz', 'szólándasz': 'szólsz', 'mondándasz': 'mondasz', 'meglátándasz': 'meglátsz',
    'látándasz': 'látsz', 'jutándasz': 'jutsz', 'hallándasz': 'hallasz', 'hallgatándasz': 'hallgatsz',
    'fordulándasz': 'fordulsz', 'engedéndesz': 'engedsz', 'veéndesz': 'veszel', 'leéndesz': 'leszel',
    'leendesz': 'leszel', 'eljövéndesz': 'eljössz', 'cselekedéndesz': 'cselekszel', 'adándasz': 'adsz',
    'iván': 'ive', 'elvevén': 'elvéve', 'felvevén': 'felvéve', 'fölvevén': 'fölvéve', 'elővevén': 'elővéve',
    'észrevevén': 'észrevéve',
}
# ELT-1: a #94 által elemezetlen (vagy hibás lemmájú) -ik végű jelen idejű ige a segédigei vala előtt; a mai
# múlt idejű alak kézzel átnézve (a 37 „-ik + vala” esetből a 29 igei alak; a kik, második, kisebbik, betegeik,
# kérdéseik, mellvértjeik nem ige). A vala kiesik.
VALA_ELOTT_KEZI = {
    'szégyenlik': 'szégyenlették', 'megehetik': 'megehették', 'leeresztik': 'leeresztették',
    'kötözgetik': 'kötözgették', 'hallgatózik': 'hallgatózott', 'terjeszkedik': 'terjeszkedett',
    'emésztetik': 'emésztetett', 'nyugoszik': 'nyugodott', 'szomjúhozik': 'szomjúhozott', 'késik': 'késett',
    'őrlik': 'őrölték', 'erősbödik': 'erősbödött', 'merik': 'merték', 'befedezik': 'befedezték',
    'érthetik': 'érthették', 'töredezik': 'töredezett', 'legelészik': 'legelészett', 'letelepszik': 'letelepedett',
    'verdesik': 'verdesték', 'lesik': 'lesték', 'megérthetik': 'megérthették', 'feküszik': 'feküdt',
    'igyekszik': 'igyekezett', 'szakadozik': 'szakadozott', 'élelmeztetik': 'élelmeztetett',
    'hivattatik': 'hivattatott', 'mívelik': 'mívelték', 'könnyebbítik': 'könnyebbítették', 'kínlódik': 'kínlódott',
    # a 2. ellenőri kör (ELT-1 maradéka): a létigeinek vett vala előtti, nem -ik végű jelen idejű igék (a 255
    # jelölt szóból kézzel átnézve; a többi névszó: fiai, olyanok, velük …, ott a vala helyesen volt)
    'meri': 'merte', 'erőlteti': 'erőltette', 'megbotránkoznak': 'megbotránkoztak', 'alkalmaznak': 'alkalmaztak',
    'becsapnak': 'becsaptak', 'bujkálsz': 'bujkáltál', 'csikorgatják': 'csikorgatták',
    'dolgoztatnak': 'dolgoztattak', 'emelheti': 'emelhette', 'gyötri': 'gyötörte', 'hihetnek': 'hihettek',
    'háborognak': 'háborogtak', 'járkálnak': 'járkáltak', 'kényszeríti': 'kényszerítette',
    'lakhatunk': 'lakhattunk', 'legelésznek': 'legelésztek', 'megkedvelnek': 'megkedveltek',
    'megnyiratja': 'megnyiratta', 'megvilágosítja': 'megvilágosította', 'nyalják': 'nyalták',
    'repdesnek': 'repdestek', 'rágják': 'rágták', 'sajdítanak': 'sajdítottak', 'suttogja': 'suttogta',
    'szegdelnek': 'szegdeltek', 'szemlélődnek': 'szemlélődtek', 'szikráznak': 'szikráztak',
    'sínlődnek': 'sínlődtek', 'tanulhatja': 'tanulhatta', 'táncolnak': 'táncoltak', 'vesztegeti': 'vesztegette',
    'vigasztalják': 'vigasztalták', 'vonszolják': 'vonszolták', 'vész': 'veszett', 'ásnak': 'ástak',
    'őrzi': 'őrizte', 'lőnek': 'lőttek',  # 1Krón 12:2: nyíllal lőnek vala
    'ellenek': 'elltek',  # N-2: a juhok ellenek vala (1Móz 30:39, 31:8), nem E/1
}
# A vala előtti, már múlt idejű, de a próbán át nem ismert igék: csak a vala esik ki.
VALA_ELOTT_MULT_KEZI = {'tusakodtatok', 'etettelek', 'tévelyegtem', 'vendégeskedtek'}
# N-1: az E/1 tárgyas elbeszélő múlt (-ám/-ém: mondám → mondtam), ha az E/3 tárgyas párja (mondá) jegyes; a 131
# alak kézzel átnézve. Felülbírálás: a #94 hibás töve (elvégzik, kérd); kimarad az értém (értem 'miattam' is).
E1_TARGYAS_KEZI = {'elvégzém': 'elvégeztem', 'kérdém': 'kérdeztem', 'értém': None}
# ELT-4: tokenszintű kivételek (igehely, sorszám) → mai alak, vagy None = változatlan (a szövegkörnyezet dönt;
# kézzel átnézve az evék és a tevék minden előfordulásán): a tevék főnév (tevék jőnek, tevék legelőjévé); az
# evék T/3 (a ti atyáitok evék, az Izráel fiai evék), a tevék E/1 (bizonyságot tevék, és mondám).
TOKEN_KIVETEL = {
    ('1Móz 24:63', 16): None, ('Ez 25:5', 4): None,
    ('Ján 6:58', 18): 'ették', ('2Móz 16:35', 8): 'ették',
    ('ApCsel 13:36', 13): 'helyeztetett',  # helyhezteték: másutt tárgyas T/3 (helyezték), itt szenvedő E/3
    ('Neh 13:21', 3): 'tettem', ('Dán 9:4', 10): 'tettem', ('Jer 35:5', 13): 'tettem',
}
# DT-F96p: a j nélküli birtokos T/3 -ök → -ük, ahol a tő többes száma a korpuszban -ek (szív → szívek, ezért a
# szívök csak birtokos); a nemök (a nemek nem áll a korpuszban) kézi listából. Kimarad a múlt idejű T/2 ige
# (ültök, jöttök, megöltök: a ragtalan -tök t-végű tövön), kivéve az érettök, értök névmást.
OK_RAG = ('', 'et', 'nek', 'ben', 'be', 'ből', 're', 'ről', 'hez', 'höz', 'től', 'kel', 'ért', 'ön', 'ig')
OK_KEZI = {'nemök': 'nemük'}
OK_NEVMAS = {'érettök', 'értök'}
# A határozói igenév kivételei: a mai irodalmi alak is -vén (lévén), nem változik.
IGENEV_KIVETEL = {'lévén', 'jövén', 'eljövén', 'feljövén', 'kijövén', 'bejövén', 'visszajövén', 'előjövén'}


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def nagy(minta, uj):
    return uj[:1].upper() + uj[1:] if minta[:1].isupper() else uj


def magas(szo):
    return ir.hang(szo) != 'o'


class Alakok:
    """Alakszintű igealak-jelöltek (szövegkörnyezet nélkül) és osztályok."""

    def __init__(self, tabla, gy, kis_szavak):
        self.tabla = tabla
        self.kis_szavak = kis_szavak
        self.igei = fedettseg.igei_tovek(tabla, kis_szavak)
        kis_gy = collections.Counter()
        for t, n in gy.items():
            kis_gy[t.lower()] += n
        jegyes_kis = {}
        for alak, s in tabla.items():
            if s['regies_jegy']:
                jegyes_kis[alak.lower()] = kis_gy.get(alak.lower(), 0)
        self.gyakori = set(k for k, _ in sorted(jegyes_kis.items(), key=lambda x: (-x[1], x[0]))[:fedettseg.GYAKORI_JEGYES])
        self.oszt = {}
        for alak in gy:
            sor = fedettseg.tablasor(tabla, alak)
            o, reszlet, _ = fedettseg.osztalyoz(alak, sor, self.gyakori, self.igei)
            self.oszt[alak] = (o, reszlet, sor)

    def bontas(self, alak, sor):
        """(igekötő, alapige) a lemma mai alakjából."""
        lemma = (sor['szotari_alak_mai'] or sor['szotari_alak']).lower()
        return ir.szetbont(lemma, self.kis_szavak)

    def jegy_jeloltek(self, alak, sor):
        """A jegy szerinti mai alak(ok): {'': x} egyértelműen, {'alanyi': x, 'targyas': y} vagy
        {'E1': x, 'T3': y} szövegkörnyezetfüggően; None, ha a szabály nem képez alakot."""
        jegy = sor['regies_jegy']
        kis = alak.lower()
        if jegy == 'hatarozoi_igenev':
            if kis in IGENEV_KIVETEL or not kis.endswith(('ván', 'vén')):
                return {}
            return {'': nagy(alak, kis[:-3] + ('va' if kis.endswith('ván') else 've'))}
        if jegy == 'felszolito.E2':
            return None  # DT-F96k (🟡): külön jelölt, nem csere
        if jegy not in JEGY_SZEM:
            return None
        kot, alap = self.bontas(alak, sor)
        if not kis.startswith(kot):
            return None
        szem, targy = JEGY_SZEM[jegy]
        if jegy in ('mult.E1', 'mult.E3') and kis.endswith(('taték', 'teték')):
            # szenvedő E/3 (kiadaték → kiadatott, elemészteték → elemésztetett), nem E/1
            to = kis[:-3]
            return {'': nagy(alak, to + ir.kotohang(to))}
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        if (jegy == 'mult.E1' and kis.endswith('ék') and not self.targyas_kepes(kot, alap)
                and ((kot + v + 'ik') in self.kis_szavak or (v + 'ik') in self.kis_szavak)):
            m = ir.mult(alap, 'E3', False)  # -ik-es ige E/3-a (elutazék → elutazott), nem E/1
            return {'': nagy(alak, kot + m)} if m else None
        if alap in TARGYAS_MINDIG:
            targy = True
        if jegy == 'mult.E1' and magas(alap) and kis.endswith('ék') and self.targyas_kepes(kot, alap):
            e1, t3 = ir.mult(alap, 'E1', False), ir.mult(alap, 'T3', True)
            if e1 and t3:
                return {'E1': nagy(alak, kot + e1), 'T3': nagy(alak, kot + t3)}
            return None
        if targy is None:
            a, t = ir.mult(alap, szem, False), ir.mult(alap, szem, True)
            if not a:
                return None
            if a == t or not self.targyas_kepes(kot, alap):
                return {'': nagy(alak, kot + a)}
            return {'alanyi': nagy(alak, kot + a), 'targyas': nagy(alak, kot + t)}
        m = ir.mult(alap, szem, targy)
        return {'': nagy(alak, kot + m)} if m else None

    def targyas_kepes(self, kot, alap):
        """Tárgyas-e az ige: tárgyas jelen (mondja, kéri, hozza) vagy tárgyas múlt (mondta) a korpuszban."""
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        jel = [v + 'ja', v + 'ják', v + 'i', ir.mult(alap, 'E3', True) or '']
        if v[-1:] in ('s', 'z'):
            jel += [v + v[-1] + 'a', v + v[-1] + 'ák']
        return any(j and ((kot + j) in self.kis_szavak or j in self.kis_szavak) for j in jel)

    def felszolito_jelolt(self, alak, sor):
        kis = alak.lower()
        if sor and sor['regies_jegy'] == 'felszolito.E2' and kis.endswith(('ál', 'él')):
            return alak[:-2]
        return None

    def gyanu_jelolt(self, alak, sor, reszlet):
        """A jegy nélküli régies gyanú szabály-jelöltje (az -ák/-ék T/3 tárgyas, a -taték, a jő-család)."""
        kis = alak.lower()
        if kis in GYANU_KEZI:
            return {'': nagy(alak, GYANU_KEZI[kis])}
        if reszlet in ('elemezetlen:-ák', 'elemezetlen:-ék'):
            kot, alap = ir.szetbont(kis[:-2], self.kis_szavak)
            m = ir.mult(alap, 'T3', True)
            return {'': nagy(alak, kot + m)} if m else None
        if reszlet.startswith('vegzodes:-'):
            veg = reszlet.split('-', 1)[1]
            kot, alap = self.bontas(alak, sor)
            szem = {'á': ('E3', True), 'é': ('E3', True), 'a': ('E3', False), 'e': ('E3', False),
                    'ának': ('T3', None), 'ének': ('T3', None), 'ák': ('T3', True), 'ék': ('T3', True),
                    'ál': ('E2', None), 'él': ('E2', None), 'ánk': ('T1', None), 'énk': ('T1', None),
                    'átok': ('T2', None), 'étek': ('T2', None)}.get(veg)
            if not szem or not kis.startswith(kot):
                return None
            s, t = szem
            m = ir.mult(alap, s, bool(t))
            return {'': nagy(alak, kot + m)} if m else None
        return None


def to_or(llm, alak_h, sor, alakok, reszlet=''):
    """DT-F96d tő-őr: az LLM-alak egy token, a kezdőbetű-állás egyezik, és hordozza az igekötőt és az
    igetövet (a rendhagyó igén a múlt tövét is); a változatlan válasz átmegy."""
    if not llm:
        return False
    if tokenek.tokenizal(llm) != [llm] or llm[:1].isupper() != alak_h[:1].isupper():
        return False
    o, a = llm.lower(), alak_h.lower()
    if o == a:
        return True
    tovek = []
    if sor and sor['szotari_alak'].lower() != a:
        kot, alap = alakok.bontas(alak_h, sor)
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        tovek.append(kot + v[:max(2, len(v) - 1)])
        if alap in ir.RENDHAGYO:
            e3, t = ir.RENDHAGYO[alap]
            tovek += [kot + e3[:max(2, len(e3) - 2)], kot + t[:max(2, len(t) - 1)]]
    else:
        veg = reszlet.split('-', 1)[1] if '-' in reszlet else ''
        to = a[:-len(veg)] if veg and a.endswith(veg) else a[:max(2, len(a) - 3)]
        tovek.append(to[:max(2, len(to) - 1)])
    return any(o.startswith(t) for t in tovek) and abs(len(o) - len(a)) <= 5


def llm_beolvas(tabla=LLM_TABLA):
    ut = os.path.join(ROOT, tabla)
    ki = {}
    if not os.path.exists(ut):
        return ki
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            ki[d['alak']] = d
    return ki


def tagmondat(spans, szoveg, i, irany):
    """Az i. token tagmondatbeli szomszédai (írásjelig, legfeljebb 7) az adott irányban."""
    ki = []
    j = i
    while len(ki) < 7:
        k = j + irany
        if k < 0 or k >= len(spans):
            break
        koz = szoveg[spans[j][1]:spans[k][0]] if irany > 0 else szoveg[spans[k][1]:spans[j][0]]
        if re.search(r'[.;:!?]', koz):
            break
        ki.append(k)
        j = k
    return ki


VONATKOZO_TARGY = {'melyet', 'melyeket', 'kit', 'kiket', 'mit', 'miket', 'amelyet', 'amelyeket', 'akit', 'akiket',
                   'amit', 'amiket'}
ALANYI_TARGY = {'engem', 'engemet', 'téged', 'tégedet', 'minket', 'minket', 'titeket', 'bennünket', 'benneteket'}


def tagmondat_szuk(spans, szoveg, i, irany, n):
    """Mint a tagmondat, de vesszőnél és az „és” kötőszónál is megáll, legfeljebb n token."""
    ki = []
    j = i
    while len(ki) < n:
        k = j + irany
        if k < 0 or k >= len(spans):
            break
        koz = szoveg[spans[j][1]:spans[k][0]] if irany > 0 else szoveg[spans[k][1]:spans[j][0]]
        if re.search(r'[.,;:!?]', koz) or spans[k][2].lower() == 'és':
            break
        ki.append(k)
        j = k
    return ki


def targyas_e(spans, szoveg, i):
    """Határozott tárgy a tagmondatban (heurisztika, manual). Alanyi, ha a tárgy vonatkozó névmás (a melyet …
    adának → amelyet adtak) vagy 1./2. személyű névmás (engem); a tagmondat a vesszőig és az „és”-ig tart."""
    koz_utan = szoveg[spans[i][1]:spans[i + 1][0]] if i + 1 < len(spans) else ''
    if any(spans[j][2].lower() in VONATKOZO_TARGY for j in tagmondat_szuk(spans, szoveg, i, -1, 30)):
        return False
    kornyezet = tagmondat_szuk(spans, szoveg, i, 1, 5) + tagmondat_szuk(spans, szoveg, i, -1, 4)
    if any(spans[j][2].lower() in ALANYI_TARGY for j in kornyezet):
        return False
    if i + 1 < len(spans) and ',' in koz_utan and spans[i + 1][2].lower() == 'hogy':
        return True
    for j in kornyezet:
        w = spans[j][2].lower()
        if w in HATAROZOTT_TARGY:
            return True
        elo = spans[j - 1][2].lower() if j > 0 else ''
        if elo in ('a', 'az') and w.endswith('t') and len(w) > 2 and targyrag(w):
            return True
        if BIRTOKOS_TARGY.search(w) and len(w) > 4:
            return True
    return False


SZAVAK = set()  # a korpusz kisbetűs szavai (a Feldolgozo tölti)
EKEZET_VISSZA = str.maketrans({'á': 'a', 'é': 'e'})


def targyrag(w):
    """A -t tárgyrag-e: a -t / -at / -et / -ot / -öt nélküli tő (az á/é rövidülésével is) szó a korpuszban
    (földet → föld, urat → ura, fát → fa); a kárpit, a fiat nem tárgy."""
    for n in (1, 2):
        t = w[:-n]
        if len(t) >= 2 and (t in SZAVAK or (t[:-1] + t[-1:].translate(EKEZET_VISSZA)) in SZAVAK):
            return True
    return False


def alanyi_targyas_par(a, b):
    """(alanyi, tárgyas), ha a két alak csak a T/3 alanyi és tárgyas ragban tér el (hittek / hitték, adtak /
    adták); különben None."""
    for x, y in ((a, b), (b, a)):
        xl, yl = x.lower(), y.lower()
        if xl[:-2] == yl[:-2] and len(xl) > 4 and (xl[-2:], yl[-2:]) in (('ek', 'ék'), ('ak', 'ák')):
            return x, y
    return None


def h1_atvisz(r1, r2, uj):
    """A .1 cseréje (reá → rá, dí → di) a .2 eredményén is: ha a .2-alak az 1908-as alak .1 előtti részével kezdődik
    (a szavazat az 1908-as alakra jött: reáveté → reávetette), a .1 szerinti részre cseréljük (rávetette)."""
    a, b, u = r1.lower(), r2.lower(), uj.lower()
    j = 0
    while j < min(len(a), len(b)) and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
        j += 1
    ea, eb = a[:len(a) - j], b[:len(b) - j]
    if ea != eb and u.startswith(ea) and not (len(eb) >= len(ea) and u.startswith(eb)):
        return nagy(uj, eb + uj[len(ea):])
    return uj


def kor5_beolvas():
    """Az 5. kör táblája: (igehely, sorszám) → (meglévő jelöltek listája, opus-alak)."""
    ki = {}
    ut = os.path.join(ROOT, KOR5_TABLA)
    if not os.path.exists(ut):
        return ki
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            ki[(d['igehely'], d['sorszam'])] = (d['meglevo_jeloltek'].split('|'), d['opus_alak'])
    return ki


def kor3_beolvas(tabla=KOR3_TABLA):
    """A 3. (4.) kör táblája: (alak → (szabály-jelölt dict vagy None, opus-alak), vala-pár → opus-alak,
    jelölt alak → opus-alak)."""
    alak, vala, jelolt = {}, {}, {}
    ut = os.path.join(ROOT, tabla)
    if not os.path.exists(ut):
        return alak, vala, jelolt
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            if d['tipus'] == 'vala':
                vala[d['kerdes']] = d['opus_alak']
                continue
            if d['tipus'] == 'jelolt':
                jelolt[d['kerdes']] = d['opus_alak']
                continue
            jel = None
            if d['szabaly_jelolt']:
                jel = dict((x.split('=', 1) if '=' in x else ('', x)) for x in d['szabaly_jelolt'].split('|'))
            alak[d['kerdes']] = (jel, d['opus_alak'])
    return alak, vala, jelolt


MAGANHANGZO = set('aáeéiíoóöőuúüű')


def nevelo_utan(spans, szoveg, i):
    """Az igealak-jelölt névelő után, egy szóközzel áll: főnév (a tevék, egy tevének, a küldöttek); ilyenkor a
    .2 szabálya, a 3. és a 4. kör nem cserél (bizonytalan=nevelo_utan; a 10.3 óta működő, ott le nem írt
    kizárás, napló 15.2). A névelő az „a” csak mássalhangzóval, az „az” csak magánhangzóval kezdődő szó előtt; a
    mássalhangzós szó előtti „az” névmás (az monda, az méne, az felele: ő mondta), a magánhangzós előtti „a” nem
    névelő, ott a kizárás nem érvényes (ELLENOR_F96 4. kör, 2.). Az „egy” mindkét esetben névelő."""
    if i == 0 or szoveg[spans[i - 1][1]:spans[i][0]] != ' ':
        return False
    elo = spans[i - 1][2].lower()
    mgh = spans[i][2][:1].lower() in MAGANHANGZO
    return elo == 'egy' or (elo == 'a' and not mgh) or (elo == 'az' and mgh)


def mondatszakasz(spans, szoveg, i):
    """Az i. token mondatszakaszának (a .;:!? jelek között) tokenindexei, az i. nélkül."""
    eleje = i
    while eleje > 0 and not re.search(r'[.;:!?]', szoveg[spans[eleje - 1][1]:spans[eleje][0]]):
        eleje -= 1
    vege = i
    while vege + 1 < len(spans) and not re.search(r'[.;:!?]', szoveg[spans[vege][1]:spans[vege + 1][0]]):
        vege += 1
    return [j for j in range(eleje, vege + 1) if j != i]


def e1_e(spans, szoveg=None, i=None):
    """Egyes szám első személy a tagmondatban (vesszőig, „és”-ig); tagmondat nélkül az egész versben."""
    if szoveg is None:
        return any(s[2].lower() in E1_JEL for s in spans)
    return any(spans[j][2].lower() in E1_JEL
               for j in tagmondat_szuk(spans, szoveg, i, 1, 8) + tagmondat_szuk(spans, szoveg, i, -1, 8))


class Feldolgozo:
    def __init__(self, alakok, alakszotar, dont, llm):
        self.a = alakok
        self.alakszotar = alakszotar
        self.dont = dont
        self.llm = llm
        self.llm2 = llm_beolvas(LLM2_TABLA)
        self.kor3_alak, self.kor3_vala, _ = kor3_beolvas()
        self.kor4_alak, self.kor4_vala, self.kor4_jelolt = kor3_beolvas(KOR4_TABLA)
        self.kor5 = kor5_beolvas()
        SZAVAK.update(alakok.kis_szavak)
        self.alak_dontes = {}  # alak → (alkalmazas, jeloltek, szabaly)
        self.szamlalo = collections.Counter()

    def alak_info(self, alak):
        """(alkalmazás, jelöltek dict vagy None, szabály-címke) alakonként, gyorsítótárral.
        alkalmazás: 'szabaly' (automatikus), 'jelolt' (nem automatikus), 'vala', 'lon', 'vagyon', ''."""
        if alak in self.alak_dontes:
            return self.alak_dontes[alak]
        o, reszlet, sor = self.a.oszt[alak]
        kis = alak.lower()
        ki = ('', None, '')
        if kis in VALA:
            ki = ('vala', None, 'vala')
        elif kis in LON:
            ki = ('lon', {'': nagy(alak, LON[kis])}, 'lon')
        elif kis == 'vagyon':
            ki = ('vagyon', {'': nagy(alak, 'van')}, 'vagyon')
        elif kis in GYANU_KEZI:
            ki = ('szabaly', {'': nagy(alak, GYANU_KEZI[kis])}, 'gyanu_kezi')
        elif o == 'igealak_gyakori':
            if kis in KEZI:
                ki = ('szabaly', {'': nagy(alak, KEZI[kis])}, 'igealak_kezi') if KEZI[kis] else ('', None, 'jegyhiba_kezi')
            else:
                j = self.a.jegy_jeloltek(alak, sor)
                if j == {}:
                    ki = ('', None, 'igenev_kivetel')
                elif j:
                    ki = ('szabaly', j, 'igealak:' + sor['regies_jegy'])
                elif sor['regies_jegy'] == 'felszolito.E2':
                    f = self.a.felszolito_jelolt(alak, sor)
                    ki = ('jelolt', {'': f} if f else None, 'felszolito_E2')
                else:
                    ki = ('jelolt', None, 'igealak_nincs_szabaly')
        elif o == 'igealak_ritka':
            if sor['regies_jegy'] == 'felszolito.E2':
                f = self.a.felszolito_jelolt(alak, sor)
                ki = ('jelolt', {'': f} if f else None, 'felszolito_E2')
            else:
                j = self.a.jegy_jeloltek(alak, sor)
                ki = ('', None, 'igenev_kivetel') if j == {} else ('jelolt', j, 'igealak_ritka:' + sor['regies_jegy'])
        elif o == 'regies_gyanu':
            m = ir.kotohang_mult(self.alakszotar[alak][0], sor['szotari_alak_mai'] or sor['szotari_alak'],
                                 self.a.kis_szavak) if sor else None
            if m and m in self.a.kis_szavak:
                ki = ('szabaly', {'': nagy(alak, m)}, 'kotohang_mult')  # DT-F96k b (mondotta → mondta)
            else:
                ki = ('jelolt', self.a.gyanu_jelolt(alak, sor, reszlet), 'gyanu:' + reszlet)
        if not ki[0]:
            m = self.e1_targyas(self.alakszotar[alak][0])  # N-1 (2. ellenőri kör)
            if m:
                ki = ('szabaly', {'': nagy(alak, m)}, 'mult_E1_targyas')
        if not ki[0]:
            m = self.ok_birtokos(self.alakszotar[alak][0])  # DT-F96p
            if m:
                ki = ('szabaly', {'': nagy(alak, m)}, 'ok_birtokos')
        if not ki[0] and sor and o in ('valtozatlan', 'regies_gyanu', 'helyesiras_tabla', 'helyesiras_szabaly'):
            # DT-F96k (🟡): a régies, kötőhangzós múlt (mondotta → mondta, szólott → szólt) jelölt, nem csere
            m = ir.kotohang_mult(self.alakszotar[alak][0], sor['szotari_alak_mai'] or sor['szotari_alak'],
                                 self.a.kis_szavak)
            if m and m in self.a.kis_szavak:
                ki = ('szabaly', {'': nagy(alak, m)}, 'kotohang_mult')  # DT-F96k b: automatikus csere
        self.alak_dontes[alak] = ki
        return ki

    def e1_targyas(self, alak_h):
        """N-1: az E/1 tárgyas elbeszélő múlt (-ám/-ém) mai alakja, ha az E/3 tárgyas pár jegyes; különben None."""
        w = alak_h.lower()
        if w in E1_TARGYAS_KEZI:
            return E1_TARGYAS_KEZI[w]
        if not w.endswith(('ám', 'ém')) or len(w) < 4:
            return None
        s = fedettseg.tablasor(self.a.tabla, w[:-1])
        if not s or s['regies_jegy'] != 'mult.targyas.E3':
            return None
        kot, alap = self.a.bontas(w[:-1], s)
        m = ir.mult(alap, 'E1', True)
        return kot + m if m and w.startswith(kot) else None

    def ok_birtokos(self, alak_h):
        """DT-F96p: a j nélküli birtokos T/3 -ök mai -ük alakja, ha a tő többese -ek; különben None."""
        w = alak_h.lower()
        if w in OK_KEZI:
            return OK_KEZI[w]
        for r in OK_RAG:
            veg = 'ök' + r
            if not w.endswith(veg) or len(w) <= len(veg) + 1 or w[-len(veg) - 1] == 'j':
                continue
            to = w[:-len(veg)]
            if not ((to + 'ek') in self.a.kis_szavak or (to + 'ek' + r) in self.a.kis_szavak):
                return None
            if r == '' and to.endswith('t') and w not in OK_NEVMAS:
                return None  # ültök, jöttök: múlt idejű T/2 ige
            return to + 'ük' + r
        return None

    def llm_jelolt(self, alak, alak_h, masodik=False):
        """(llm-alak, tő-őr) az LLM-táblából (kisbetűs kulcs; masodik: az opus-tábla); ('', '') ha nincs."""
        d = (self.llm2 if masodik else self.llm).get(alak.lower())
        if not d and masodik and alak.lower() in self.kor4_jelolt:
            d = {'llm_alak': self.kor4_jelolt[alak.lower()]}  # a 4. kör opus-szavazata (DT-F96r)
        if not d:
            return '', ''
        llm = nagy(alak_h, d['llm_alak'])
        o, reszlet, sor = self.a.oszt[alak]
        ok = to_or(llm, alak_h, sor, self.a, reszlet)
        if not ok and alak.lower() != alak_h.lower():
            # DT-F96s: a .1-ben változott alakon (dícsérvén → dicsérvén) a tő-őr a .1 utáni alakon is mér
            ok = to_or(llm, alak_h, None, self.a, '')
        return llm, 'ok' if ok else 'bukott'

    def vers(self, igehely, szoveg):
        sorok_h, modern_h = helyesiras.vers_feldolgoz(igehely, szoveg, self.alakszotar, self.dont)
        spans = [(m.start(), m.end(), m.group(0)) for m in BETU.finditer(szoveg)]
        # [sorszam, 1908, .1-alak, modern, kieso, szabaly(.1), szabaly(.2), bizonytalan(.1), bizonytalan(.2), jelolt]
        t = [[s[0], s[1], s[2], s[2], s[3], s[4], '', s[5], '', ''] for s in sorok_h]
        for i, r in enumerate(t):
            if r[4]:
                continue
            alk, jel, cim = self.alak_info(r[1])
            if (igehely, r[0]) in TOKEN_KIVETEL:  # ELT-4: tokenszintű, kézzel átnézett kivétel
                cel = TOKEN_KIVETEL[(igehely, r[0])]
                r[3] = nagy(r[1], cel) if cel else r[2]
                r[6] = 'token_kivetel'
                continue
            if alk in ('szabaly', 'lon', 'vagyon') and jel:
                if alk == 'vagyon' and i > 0 and spans[i - 1][2].lower() in ('a', 'az'):
                    r[6] = 'vagyon_fonev_marad'
                    continue
                if alk == 'lon' and r[1].lower() == 'lőnek' and any(NYIL_IJ.fullmatch(s[2].lower()) for s in spans):
                    r[8] = 'lonek_lo'
                    continue
                if alk == 'szabaly' and cim != 'ok_birtokos' and nevelo_utan(spans, szoveg, i):
                    r[8] = 'nevelo_utan'  # a tevék, egy tevének, a küldöttek: főnév, nem igealak
                    continue
                r[3], r[6] = self.valaszt(jel, spans, szoveg, i, r, t), cim
            elif alk == 'jelolt':
                jl = []
                if jel:
                    jl.append('szabaly:' + '|'.join('%s%s' % (k + '=' if k else '', v) for k, v in jel.items()))
                llm, tor = self.llm_jelolt(r[1], r[2])
                if llm:
                    jl.append('llm:%s(%s)' % (llm, 'tő-őr ok' if tor == 'ok' else 'tő-őr bukott'))
                llm2, tor2 = self.llm_jelolt(r[1], r[2], True)
                if llm2:
                    jl.append('opus:%s(%s)' % (llm2, 'tő-őr ok' if tor2 == 'ok' else 'tő-őr bukott'))
                r[9] = '; '.join(jl)
                r[6] = cim
                # DT-F96l (2. opció): a három forrásból (szabály, sonnet, opus) legalább kettő egyezik, és a
                # tő-őr átengedi → csere; a felszólító -jál a DT-F96k a szerint marad
                if not cim.startswith('felszolito') and not nevelo_utan(spans, szoveg, i):
                    # DT-F96s (3. opció): a szabály-jelöltre a .1 cseréje (dícsérve → dicsérve), mielőtt szavaz
                    jel_n = {k: h1_atvisz(r[1], r[2], v) for k, v in jel.items()} if jel else jel
                    l1 = h1_atvisz(r[1], r[2], llm) if tor == 'ok' else ''
                    l2 = h1_atvisz(r[1], r[2], llm2) if tor2 == 'ok' else ''
                    tobb = self.tobbseg(jel_n, l1, l2)
                    if tobb:
                        ertek, forrasok = tobb
                        r[3] = self.valaszt(ertek, spans, szoveg, i, r, t) if isinstance(ertek, dict) else ertek
                        if not isinstance(ertek, dict):
                            r[3] = self.ek_e1_fordit(r, r[3], t, spans, szoveg, i)
                        r[6] = cimke(cim, 'tobbseg:' + forrasok)
                    elif l1 and l2 and alanyi_targyas_par(l1, l2):
                        # a sonnet és az opus csak a T/3 alanyi–tárgyas ragozásban tér el (hittek / hitték): a
                        # tagmondat tárgya dönt (targyas_heur)
                        par = alanyi_targyas_par(l1, l2)
                        r[3] = self.valaszt({'alanyi': par[0], 'targyas': par[1]}, spans, szoveg, i, r, t)
                        r[6] = cimke(cim, 'tobbseg:alanyi_targyas')
                    elif cim != 'gyanu:nd_jovo' and l2 and self.tanusitott(l2) and not any(self.tanusitott(v) for v in (jel_n or {}).values()) \
                            and not (l1 and l1 != l2 and self.tanusitott(l1)) and self.tanusitott_ok(r, l2, t, spans, szoveg, i):
                        # a szabály-jelölt a korpuszban nem áll, az opus-alak igen (és a sonnet nem mond mást)
                        r[3] = l2
                        r[6] = cimke(cim, 'tobbseg:opus_tanusitott')
                        r[8] = 'szabaly_nem_tanusitott'
            elif alk == 'vala':
                self.vala(t, spans, szoveg, i)
                self.kor3_vala_alkalmaz(t, spans, szoveg, i)
                self.kor3_vala_alkalmaz(t, spans, szoveg, i, 4)
            if alk != 'vala' and not cim.startswith('felszolito') and cim != 'gyanu:nd_jovo':
                self.kor3_alkalmaz(t, spans, szoveg, i)
                self.kor3_alkalmaz(t, spans, szoveg, i, 4)
        for r in t:
            self.kor5_alkalmaz(igehely, r)
            if not r[4] and r[3] != r[2] and r[2] != r[1]:
                r[3] = h1_atvisz(r[1], r[2], r[3])
        modern = self.szoveg(szoveg, spans, t)
        self.k2(igehely, szoveg, modern, t)
        return t, modern

    def tobbseg(self, jel, llm, llm2):
        """DT-F96l: (érték, források) a többségi jelöltre, vagy None. A szövegkörnyezetfüggő szabály-jelölt
        (alanyi/tárgyas, E/1/T/3) akkor szavaz, ha az LLM-alak az egyik értéke: ekkor a csere tokenenként a
        heurisztika szerint (valaszt) megy, és bizonytalannak jelölt."""
        szab = set(jel.values()) if jel else set()
        if llm and llm2 and llm == llm2:
            if llm in szab and len(szab) > 1:
                return jel, 'szabaly+sonnet+opus'
            return llm, 'szabaly+sonnet+opus' if llm in szab else 'sonnet+opus'
        for l, nev in ((llm, 'sonnet'), (llm2, 'opus')):
            if l and l in szab:
                return (jel if len(szab) > 1 else l), 'szabaly+' + nev
        return None

    def valaszt(self, jel, spans, szoveg, i, r, t=None):
        if '' in jel:
            return jel['']
        if 'E1' in jel:
            r[8] = 'ek_E1_T3'
            e1 = (r[1].lower().endswith(E1_MINDIG_VEG) or e1_e(spans, szoveg, i)
                  or (t is not None and self.e1_ige(t, i, spans, szoveg)))
            return jel['E1'] if e1 else jel['T3']
        r[8] = 'targyas_heur'
        return jel['targyas'] if targyas_e(spans, szoveg, i) else jel['alanyi']

    def ek_e1_fordit(self, r, uj, t, spans, szoveg, i):
        """ELLENOR_F96 4. kör, 1.: a szabály-jelölt nélküli -ék alakon (ülteték: elemezetlen) a sonnet és az opus
        egyező T/3 tárgyas alakja (ültették) a mondatszakasz E/1 jelzője mellett (Préd 2:5 ülteték magamnak; 2:6
        Csinálék magamnak …, és ülteték) E/1-re fordul: -ták/-ték → -tam/-tem (ültettem), ek_E1_T3 jelöléssel.
        Szűkítve (napló 15.1): csak a visszaható E/1 névmás (MAGAM_E1) jelez, a mondatszakaszban; a tágabb E/1 jelző
        (e1_e, e1_ige) a próbán T/3-at fordított E/1-re (Ez 20:13 ellenem … megveték; Ez 23:38 megfertézteték az én
        …; Józs 24:12 űzék; Zak 5:9 felemelék; 1Móz 47:9 érték)."""
        w, u = r[1].lower(), uj.lower()
        if not (w.endswith('ék') and u.endswith(('ták', 'ték')) and u != r[2].lower()):
            return uj
        szak = mondatszakasz(spans, szoveg, i)
        if not any(spans[j][2].lower() in MAGAM_E1 for j in szak):
            return uj
        r[8] = 'ek_E1_T3'
        return uj[:-2] + ('am' if u.endswith('ták') else 'em')

    def kor5_alkalmaz(self, igehely, r):
        """DT-F96u (1. opció): a tokenszintű opus-válasz cserél, ha egy meglévő jelölttel (szabály, sonnet, korábbi
        opus) egyezik, és a tő-őr átengedi (a DT-F96l kettő-egyezése tokenszinten); különben jelölt marad."""
        k = self.kor5.get((igehely, str(r[0])))
        if not k or r[4] or r[3].lower() != r[2].lower() or r[2].lower().endswith(('jövén', 'jővén', 'lévén')):
            return  # a jövén/lévén igenév a mai irodalmi nyelvben is -vén (IGENEV_KIVETEL)
        meglevo, opus = k
        uj = h1_atvisz(r[1], r[2], nagy(r[1], opus))
        if uj.lower() == r[2].lower():
            return
        o, reszlet, sor = self.a.oszt[r[1]]
        tor = to_or(uj, r[2], sor, self.a, reszlet) or (r[1] != r[2] and to_or(uj, r[2], None, self.a, ''))
        if tor and uj.lower() in {h1_atvisz(r[1], r[2], v).lower() for v in meglevo}:
            r[3] = uj
            r[6] = cimke(r[6], 'kor5:token_opus+meglevo') if r[6] else 'kor5:token_opus+meglevo'
            r[8] = 'token_opus'
        else:
            r[9] = '; '.join(x for x in (r[9], 'kor5_token_opus:%s(%s)' % (uj, 'tő-őr ok' if tor else 'tő-őr bukott')) if x)

    def tanusitott(self, w):
        """A szóalak a Károli 1908 korpuszában áll (kisbetűsen)."""
        return bool(w) and w.lower() in self.a.kis_szavak

    def tanusitott_ok(self, r, uj, t, spans, szoveg, i):
        """DT-F96s: a tanúsított opus-alak csak akkor írja felül a nem tanúsított szabály-jelöltet, ha változtat, és a
        régies végződés ragozását nem sérti: az E/3 tárgyas -á/-é mai alakja -a/-e végű (rombolá → rombolta, nem
        rombolt); az -ék nem E/1 opus-alakja nem fogadható el, ha a mondatszakaszban E/1 jelző áll (aluvék)."""
        w, u = r[1].lower(), uj.lower()
        if u == r[2].lower():
            return False
        if w.endswith(('á', 'é')) and not u.endswith(('a', 'e')):
            return False
        if w.endswith('ék') and not u.endswith('m') and (e1_e(spans, szoveg, i) or self.e1_ige(t, i, spans, szoveg)):
            return False
        return True

    def e1_ige(self, t, i, spans, szoveg):
        """N-F96f: E/1 jelzője a token mondatszakaszában (a .;:!? jelek között; a másik mondat és az idézett beszéd
        E/1-e nem számít: elnyelék a … gabonafejek. És elmondám; kezdék …: Én vagyok-é): az egyértelmű E/1 igealak
        (-ám/-ém E/1 tárgyas elbeszélő múlt: mondám, N-1, vagy a régies-szken E/1 jelöltje; valék, vagyok, leszek:
        felelék, és mondám) vagy a token előtt álló E/1 névmás (E1_JEL; a tagmondaton belül utána is, e1_e), a birtokos
        „az én” nélkül (megszentségteleníték az én …; ölék meg, csak én magam: T/3)."""
        szak = [0] * len(spans)
        n = 0
        for j in range(1, len(spans)):
            if re.search(r'[.;:!?]', szoveg[spans[j - 1][1]:spans[j][0]]):
                n += 1
            szak[j] = n
        for j, q in enumerate(t):
            if j == i or q[4] or szak[j] != szak[i]:
                continue
            w = q[1].lower()
            if w in E1_JEL and j < i and not (w == 'én' and j > 0 and t[j - 1][1].lower() in ('az', 'a')):
                return True
            if w in E1_IGE:
                return True
            if w.endswith(('ám', 'ém')):
                if self.alak_info(q[1])[2] == 'mult_E1_targyas':
                    return True
                k = self.kor3_alak.get(w)
                if k and k[0] and '' in k[0] and k[1].lower() == k[0][''].lower() and k[1].lower().endswith('m'):
                    return True
        return False

    def kor3_alkalmaz(self, t, spans, szoveg, i, kor=3):
        """DT-F96q: a modern szövegben változatlanul maradt régies alak a 3. kör táblájából. Ha az opus és a
        szabály-jelölt egyezik, és a tő-őr átengedi: csere (szöveg-környezetfüggő jelöltnél a tagmondat vagy a vers
        dönt); ha szabály-jelölt nincs: a tő-őrön átment opus-alak cserél, bizonytalan jelöléssel; ha eltérnek:
        jelölt marad. A 4. kör (DT-F96r) ugyanígy, a .1 utáni alakon, a .2 döntése nélküli tokenen."""
        r = t[i]
        if kor == 4:
            if r[4] or r[3].lower() != r[2].lower() or r[6] or r[8] == 'nevelo_utan':
                return
            k = self.kor4_alak.get(r[2].lower())
        else:
            if r[4] or r[3].lower() != r[1].lower() or r[6] == 'token_kivetel' or r[8] == 'nevelo_utan':
                return
            k = self.kor3_alak.get(r[1].lower())
        if not k or r[1].lower() in IGENEV_KIVETEL or r[2].lower() in IGENEV_KIVETEL:
            return
        nev = 'kor%d' % kor
        jel, opus = k
        opus_h = nagy(r[1], opus)
        if opus_h.lower() in (r[1].lower(), r[2].lower()):
            return
        o, reszlet, sor = self.a.oszt[r[1]]
        tor = to_or(opus_h, r[2], sor, self.a, reszlet)
        if not tor and kor == 4 and r[2] != r[1]:
            # a .1-ben változott tokenen (reáadá → ráadá, harczolának → harcolának) a tő-őr a .1 utáni alakon mér
            tor = to_or(opus_h, r[2], None, self.a, '')
        if jel:
            jel_h = {kk: h1_atvisz(r[1], r[2], nagy(r[1], v)) for kk, v in jel.items()}
        if jel and opus_h in jel_h.values() and tor:
            r[3] = self.valaszt(jel_h, spans, szoveg, i, r, t)
            r[6] = cimke(r[6], nev + ':szabaly+opus') if r[6] else nev + ':szabaly+opus'
        elif not jel and tor:
            r[3] = opus_h
            r[6] = cimke(r[6], nev + ':opus') if r[6] else nev + ':opus'
            r[8] = cimke(r[8], nev + '_csak_opus') if r[8] else nev + '_csak_opus'
        elif tor and self.tanusitott(opus_h) and not any(self.tanusitott(v) for v in jel_h.values()) \
                and self.tanusitott_ok(r, opus_h, t, spans, szoveg, i):
            # DT-F96s (3. opció): a szabály-jelölt a korpuszban nem áll (bévevte, megnyugovtam), az opus-alak igen
            r[3] = opus_h
            r[6] = cimke(r[6], nev + ':opus_tanusitott') if r[6] else nev + ':opus_tanusitott'
            r[8] = cimke(r[8], 'szabaly_nem_tanusitott') if r[8] else 'szabaly_nem_tanusitott'
        else:
            jl = [r[9]] if r[9] else []
            if jel:
                jl.append(nev + '_szabaly:' + '|'.join('%s%s' % (kk + '=' if kk else '', v) for kk, v in jel_h.items()))
            jl.append(nev + '_opus:%s(%s)' % (opus_h, 'tő-őr ok' if tor else 'tő-őr bukott'))
            r[9] = '; '.join(jl)

    def kor3_vala_alkalmaz(self, t, spans, szoveg, i, kor=3):
        """DT-F96q, N-F96e: a létigeinek vett vala előtti ige a 3. kör táblájából. Szabály-jelölt itt nincs: a
        tő-őrön átment opus-alak dönt (a vala kiesik, az ige múlt időbe kerül), bizonytalan jelöléssel."""
        r = t[i]
        if i == 0 or t[i - 1][4] or not (r[6].startswith('vala_letige') or (kor == 4 and r[6] == 'vala_nem_elemezheto')):
            return
        tabla, nev = (self.kor4_vala, 'kor4') if kor == 4 else (self.kor3_vala, 'kor3')
        if szoveg[spans[i - 1][1]:spans[i][0]] != ' ':
            return
        e = t[i - 1]
        h = KOR3_VALA_HOMOGRAF.get(e[3].lower())
        if h and (i < 2 or t[i - 2][1].lower() not in h):
            return
        opus = tabla.get(e[3].lower() + ' ' + r[1].lower()) or tabla.get(e[2].lower() + ' ' + r[1].lower())
        if opus == '-' and r[6] == 'vala_nem_elemezheto':
            r[3], r[6], r[8] = nagy(r[1], VALA[r[1].lower()][1]), 'vala_letige_' + nev, nev + '_csak_opus'
            return
        if not opus or opus == '-':
            return
        uj = nagy(e[3], opus)
        o, reszlet, sor = self.a.oszt[e[1]]
        if not (to_or(uj, e[2], sor, self.a, reszlet) or to_or(uj, e[3], sor, self.a, reszlet)):
            r[9] = '; '.join(x for x in (r[9], '%s_opus:%s (tő-őr bukott)' % (nev, uj)) if x)
            return
        if uj != e[3]:
            e[3] = uj
            e[6] = cimke(e[6], 'jelen_mult_vala') if e[6] else 'jelen_mult_vala'
            e[8] = cimke(e[8], nev + '_csak_opus') if e[8] else nev + '_csak_opus'
        self.kiesik(r, 'vala_segedige_' + nev)
        r[8] = nev + '_csak_opus'

    def vala(self, t, spans, szoveg, i):
        r = t[i]
        kis = r[1].lower()
        szem, volt = VALA[kis]
        elo_ok = i > 0 and szoveg[spans[i - 1][1]:spans[i][0]] == ' ' and not t[i - 1][4]
        if not elo_ok:
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        e = t[i - 1]
        ealak = e[1]
        o, reszlet, sor = self.a.oszt[ealak]
        ek = e[2].lower()  # a .1 utáni alak (szűlt → szült)
        if sor is None:
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        lemma = (sor['szotari_alak_mai'] or sor['szotari_alak']).lower()
        jegy = sor['regies_jegy']
        sajat_mult = False
        if not jegy and not (self.a.igei(lemma) or ir.ige_e(ir.szetbont(lemma, self.a.kis_szavak)[1], self.a.kis_szavak)):
            # a #94 elemezetlen vagy hibás sora (ülnek, jöttek, hallotta, szeret → szer): saját tőkeresés
            sajat_mult = ir.mult_lemma_nelkul(ek, self.a.kis_szavak)
            if not sajat_mult:
                for l in ir.lemma_jeloltek(ek, self.a.kis_szavak):
                    if ir.jelen_elemez(ek, l, self.a.kis_szavak):
                        lemma = l
                        break
        if jegy == 'hatarozoi_igenev' or (ek.endswith(('va', 've')) and ek != lemma and self.a.igei(sor['szotari_alak'])):
            r[3], r[6] = nagy(r[1], volt), 'vala_letige_igenev'
            return
        if jegy.startswith('mult.') or ek in VALA or (e[3] != e[2] and e[6] and ir.mult_alak_e(e[3], e[2])):
            self.kiesik(r, 'vala_segedige_mult')  # régies vagy a .2 által múltba tett ige (illeték → illették)
            return
        if ek in VALA_ELOTT_MULT_KEZI:
            self.kiesik(r, 'vala_segedige_mult')
            return
        if ek in VALA_ELOTT_KEZI:  # ELT-1: elemezetlen jelen idejű ige (szégyenlik vala → szégyenlették)
            e[3] = nagy(e[2], VALA_ELOTT_KEZI[ek])
            e[6] = cimke(e[6], 'jelen_mult_vala')
            self.kiesik(r, 'vala_segedige_jelen')
            return
        if sajat_mult and ek not in ir.IGEKOTOK and lemma not in NEM_IGE:
            self.kiesik(r, 'vala_segedige_mult')
            return
        kot, alap = ir.szetbont(lemma, self.a.kis_szavak)
        if (ek in ir.IGEKOTOK or lemma in NEM_IGE or lemma in ('van', 'lesz') or ek.endswith('ni')
                or not (self.a.igei(lemma) or ir.ige_e(alap, self.a.kis_szavak))):
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        if self.mult_e(ek, kot, alap) or ir.mult_alak_e(ek, lemma, self.a.kis_szavak):
            self.kiesik(r, 'vala_segedige_mult')
            return
        je = ir.jelen_elemez(e[2], lemma, self.a.kis_szavak)
        if not je and o == 'regies_gyanu':
            self.kiesik(r, 'vala_segedige_mult')  # régies, nem jelen idejű igealak (írának vala)
            return
        if je:
            k2, alap2, sz, tg = je
            m = ir.mult(alap2, sz, tg)
            if m:
                uj = nagy(e[2], k2 + m)
                e[3] = uj
                e[6] = cimke(e[6], 'jelen_mult_vala')
                if uj.lower() not in self.a.kis_szavak:
                    e[8] = 'mult_korpuszban_nincs'
                self.kiesik(r, 'vala_segedige_jelen')
                return
        r[8] = 'vala_segedige'
        r[6] = 'vala_nem_elemezheto'

    def mult_e(self, ek, kot, alap):
        if not ek.startswith(kot):
            return False
        tv = ir.mult_tovek(alap)
        if tv is None:
            return False
        e3, to = tv
        resz = ek[len(kot):]
        if resz == e3 or resz.startswith(to):
            return True
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        return resz.startswith(v + ir.kotohang(v))  # mondotta, megmondotta, állottak

    def kiesik(self, r, cim):
        r[3] = ''
        r[4] = 'segedige'
        r[6] = cim

    def szoveg(self, szoveg, spans, t):
        ki = []
        poz = 0
        for i, (a, b, w) in enumerate(spans):
            if t[i][4] == 'osszevonva':
                ki.append(szoveg[poz:a])
                poz = spans[i + 1][0]
                continue
            if t[i][4] == 'segedige':
                poz = b  # az előtte álló egy szóköz és a vala kiesik
                continue
            ki.append(szoveg[poz:a])
            ki.append(t[i][3])
            poz = b
        ki.append(szoveg[poz:])
        return ''.join(ki)

    def k2(self, igehely, szoveg, modern, t):
        vart = [r[3] for r in t if not r[4]]
        if tokenek.tokenizal(modern) != vart:
            raise SystemExit('K2 hiba (tokenek): %s' % igehely)
        ves = sum(1 for r in t if r[4])
        vaz_e, vaz_m = BETU.sub('', szoveg), BETU.sub('', modern)
        if len(vaz_e) - len(vaz_m) != ves or vaz_m.replace(' ', '') != vaz_e.replace(' ', ''):
            raise SystemExit('K2 hiba (írásjel-váz): %s' % igehely)


def cimke(a, b):
    return a + '+' + b if a else b


def h_tokenek_beolvas():
    ki = []
    with open(os.path.join(ROOT, H_TOKENEK), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#') or l.startswith('igehely\t'):
                continue
            ki.append(tuple(l.rstrip('\n').split('\t')))
    return ki


def elokeszit():
    tabla = fedettseg.tabla_beolvas()
    versek = []
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            m = l.rstrip('\n').split('\t')
            if len(m) >= 2:
                versek.append((m[0], m[1]))
    gy = collections.Counter(t for _, sz in versek for t in tokenek.tokenizal(sz))
    kis_szavak = set(t.lower() for t in gy)
    alakszotar = {a: helyesiras.alak_modern(a, fedettseg.tablasor(tabla, a), kis_szavak) for a in gy}
    dont = helyesiras.ami_proba_keszit(tabla, fedettseg.igei_tovek(tabla, kis_szavak))
    alakok = Alakok(tabla, gy, kis_szavak)
    return tabla, versek, gy, kis_szavak, alakszotar, dont, alakok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', action='store_true')
    ap.add_argument('--minta-frissit', action='store_true')
    ap.add_argument('--minta2', action='store_true', help='a lefedettséget is mérő minta (N-F96g) kiválasztása')
    ap.add_argument('--kimenet', default=None)
    ap.add_argument('--llm-kerdes', default=None, help='az LLM-kérdések könyvtára (a repón kívül)')
    ap.add_argument('--koteg', type=int, default=560)
    ap.add_argument('--llm-valasz', default=None, help='az LLM-válaszok könyvtára (a repón kívül)')
    ap.add_argument('--modell', default=None)
    ap.add_argument('--opus', action='store_true', help='a --llm-valasz az opus-táblába ír (igealak_llm_opus.tsv)')
    a = ap.parse_args()
    tabla, versek, gy, kis_szavak, alakszotar, dont, alakok = elokeszit()
    if a.llm_kerdes:
        llm_kerdes(a.llm_kerdes, a.koteg, versek, gy, alakok, alakszotar)
        return
    if a.llm_valasz:
        llm_valasz(a.llm_valasz, a.modell, alakok, alakszotar,
                   (LLM2_TABLA, LLM2_NAPLO, 'a vitatott jelöltek (a szabály és a sonnet nem egyezik, vagy a tő-őr bukott)')
                   if a.opus else (LLM_TABLA, LLM_NAPLO, 'a nem automatikus (jelölt) igealakok'))
        return
    fd = Feldolgozo(alakok, alakszotar, dont, llm_beolvas())
    h_vart = set(h_tokenek_beolvas())
    h_kapott = set()
    vers_ki = {}
    for igehely, sz in versek:
        t, modern = fd.vers(igehely, sz)
        vers_ki[igehely] = (sz, modern, t)
        for r in t:
            if r[1] != r[2] or r[4] == 'osszevonva' or r[7]:
                h_kapott.add((igehely, str(r[0]), r[1], r[2] if r[4] != 'osszevonva' else '',
                              'osszevonva' if r[4] == 'osszevonva' else '', r[5], r[7]))
    if h_kapott != h_vart:
        raise SystemExit('a .1 újraszámolása eltér a %s-től: %d / %d sor eltér'
                         % (H_TOKENEK, len(h_kapott - h_vart), len(h_vart - h_kapott)))
    print('a .1 újraszámolva, egyezik a %s-vel (%d sor)' % (H_TOKENEK, len(h_vart)))
    kiir(vers_ki, gy, alakok, fd, a)


def bemenet_hash():
    return ('%s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s)%s'
            % (KAROLI, sha(KAROLI)[:12], SZOTARI, sha(SZOTARI)[:12], H_TOKENEK, sha(H_TOKENEK)[:12],
               SZKRIPT, sha(SZKRIPT)[:12], MODUL, sha(MODUL)[:12],
               ''.join(' + %s (sha256:%s)' % (t, sha(t)[:12]) for t in (LLM_TABLA, LLM2_TABLA, KOR3_TABLA, KOR4_TABLA, KOR5_TABLA)
                       if os.path.exists(os.path.join(ROOT, t)))))


def kiir(vers_ki, gy, alakok, fd, a):
    ki_dir = a.kimenet or os.path.join(ROOT, KI_DIR)
    os.makedirs(ki_dir, exist_ok=True)
    hk = bemenet_hash()
    fejlec = ('# GENERÁLT: %s (F96.2) — kézzel nem szerkeszthető; a javítás a szabályban vagy a kivételtáblában '
              '(KEZI, GYANU_KEZI, VALA_ELOTT_KEZI, VALA_ELOTT_MULT_KEZI, TOKEN_KIVETEL, E1_TARGYAS_KEZI, OK_KEZI, '
              'E1_MINDIG_VEG, KOR3_VALA_HOMOGRAF) | '
              'forras=%s | a .1 (helyesiras.py) kimenetére épül, újraszámolva és összevetve | tokenizálás: tokenizal '
              '(a #22 hu_sorszam-a; Strong token-kulcson illeszthető, DT-F96f) | a ritka jegyes és a régies gyanús '
              'alak a DT-F96l szerint cserél (a szabály, a sonnet és az opus közül kettő egyezik, tő-őrrel), különben '
              'a jelolt oszlopban marad; a 3. kör (DT-F96q) a változatlanul maradt régies alakon a szabály és az opus '
              'egyezésével cserél | LLM: az igealak_llm.tsv, az igealak_llm_opus.tsv, az igealak_llm_kor3.tsv, _kor4.tsv és _kor5.tsv '
              '(DT-F96d, előfizetés, API nélkül) | ts=%s\n'
              % (SZKRIPT, hk, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
    tok_ki = []
    for igehely, (sz, modern, t) in vers_ki.items():
        for r in t:
            if r[1] != r[3] or r[4] or r[7] or r[8] or r[9]:
                # DT-F96o: a kieső token gazdaszava (a kereső ide köti a kieső token Strongját): az összevont
                # „a”-é a következő (a névmás), a segédigei valáé az előző (az ige) token
                gazda = str(r[0] + 1) if r[4] == 'osszevonva' else (str(r[0] - 1) if r[4] == 'segedige' else '')
                tok_ki.append([igehely, str(r[0]), r[1], r[2], r[3], r[4], cimke(r[5], r[6]) if r[5] and r[6] else (r[5] or r[6]),
                               cimke(r[7], r[8]) if r[7] and r[8] else (r[7] or r[8]), r[9], gazda])
    with open(os.path.join(ki_dir, 'igealak_tokenek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a .1 + .2 után változó, kieső, bizonytalan vagy jelölt tokenek (%d) a %d '
                               'tokenből\n' % (len(tok_ki), sum(gy.values()))))
        f.write('\t'.join(['igehely', 'sorszam', 'alak_1908', 'alak_helyesiras', 'alak_modern', 'kieso', 'szabaly',
                           'bizonytalan', 'jelolt', 'kieso_gazda']) + '\n')
        for r in tok_ki:
            f.write('\t'.join(r) + '\n')
    # alakonként
    alak_ki = []
    for alak in sorted(gy):
        alk, jel, cim = fd.alak_info(alak)
        o, reszlet, sor = alakok.oszt[alak]
        if not (alk or o in ('igealak_gyakori', 'igealak_ritka', 'regies_gyanu', 'regies_lista')):
            continue
        llm, tor = fd.llm_jelolt(alak, fd.alakszotar[alak][0])
        sz = '|'.join('%s%s' % (k + '=' if k else '', v) for k, v in jel.items()) if jel else ''
        egy = ''
        if llm and jel:
            egy = 'egyezik' if llm in jel.values() else 'elter'
        llm2, tor2 = fd.llm_jelolt(alak, fd.alakszotar[alak][0], True)
        egy2 = ''
        if llm2:
            egy2 = '+'.join(x for x, ok in (('szabaly', bool(jel) and llm2 in jel.values()), ('sonnet', llm2 == llm)) if ok) or 'egyik_sem'
        alak_ki.append([alak, str(gy[alak]), o, reszlet, sor['regies_jegy'] if sor else '',
                        sor['szotari_alak'] if sor else '', alk or 'valtozatlan', cim, sz, llm, tor, egy,
                        llm2, tor2, egy2])
    with open(os.path.join(ki_dir, 'igealak_alakok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=az igealak-osztályú és a vala/lőn/vagyon alakok (%d); alkalmazas: '
                               'szabaly = automatikus csere; jelolt = a szabály, a sonnet és az opus jelöltje, a modern '
                               'szöveg a DT-F96l többségi szabálya szerint változik (tobbseg:<források>)\n'
                               % len(alak_ki)))
        f.write('\t'.join(['alak', 'gyakorisag', 'osztaly', 'reszlet', 'regies_jegy', 'szotari_alak', 'alkalmazas',
                           'szabaly', 'szabaly_jelolt', 'llm_alak', 'to_or', 'egyezes', 'opus_alak', 'opus_to_or',
                           'opus_egyezik']) + '\n')
        for r in alak_ki:
            f.write('\t'.join(r) + '\n')
    osszesit(vers_ki, gy, alakok, fd, alak_ki)
    if a.minta:
        minta(vers_ki, ki_dir, fejlec, fd)
    elif a.minta2:
        minta2(vers_ki, ki_dir, fejlec)
    elif a.minta_frissit:
        minta_frissit(vers_ki, ki_dir, fejlec, fd)
        if os.path.exists(os.path.join(ki_dir, MINTA2)):
            minta_frissit(vers_ki, ki_dir, fejlec, fd, MINTA2)
    print('bemenet: %s' % hk)


def osszesit(vers_ki, gy, alakok, fd, alak_ki):
    tokszam = sum(gy.values())
    valt_vers = sum(1 for v in vers_ki.values() if v[0] != v[1])
    c = collections.Counter()
    kieso = collections.Counter()
    biz = collections.Counter()
    marad = collections.Counter()
    marad_jelolt = collections.Counter()
    nem_regies = collections.Counter()
    for sz, modern, t in vers_ki.values():
        for r in t:
            if r[4]:
                kieso[r[4]] += 1
            if r[6]:
                c[r[6].split(':')[0] if not r[6].startswith('igealak:') else r[6]] += 1
            if r[8]:
                biz[r[8]] += 1
            if not r[4] and r[3].lower() == r[2].lower():
                o = alakok.oszt[r[1]][0]
                kis = r[1].lower()
                if o in ('igealak_gyakori', 'igealak_ritka', 'regies_gyanu') or kis in VALA or kis in LON or kis == 'vagyon':
                    alk, _, cim = fd.alak_info(r[1])
                    if alk == 'szabaly' and r[3] == r[2] and not r[8]:
                        continue
                    if 'tobbseg:' in r[6]:
                        nem_regies[o] += 1  # a többség szerint nem régies igealak (tett, leszek, halál): változatlan
                        continue
                    if cim.startswith('felszolito'):
                        o = 'felszolito_E2 (DT-F96k a: marad)'
                    elif cim == 'gyanu:nd_jovo':
                        o = 'nd_jovo (egy szóban nem írható át)'
                    marad[o if o != 'regies_lista' else 'regies_lista:' + kis] += 1
                    if r[9]:
                        marad_jelolt[o] += 1
    print('versek: %d, tokenek: %d; változó vers (.1 + .2): %d' % (len(vers_ki), tokszam, valt_vers))
    print('.2-szabályonként (token): %s' % dict(sorted(c.items(), key=lambda x: -x[1])))
    print('kieső token: %s' % dict(kieso))
    print('.2 bizonytalan (token): %s' % dict(biz))
    print('LEFEDETTSÉG — régies igealak a modern szövegben (token): %s; ebből jelölttel: %s'
          % (dict(sorted(marad.items(), key=lambda x: -x[1])), dict(marad_jelolt)))
    print('a többség szerint nem régies, változatlan (token): %s' % dict(nem_regies))
    print('alakonként: %s' % dict(collections.Counter((r[2], r[6]) for r in alak_ki)))
    eg = collections.Counter((r[2], r[10], r[11]) for r in alak_ki if r[9])
    if eg:
        print('LLM: osztály × tő-őr × egyezés (alak): %s' % dict(sorted(eg.items())))
    eg2 = collections.Counter((r[2], r[13], r[14]) for r in alak_ki if r[12])
    if eg2:
        print('opus: osztály × tő-őr × kivel egyezik (alak): %s' % dict(sorted(eg2.items())))


# ---- LLM (DT-F96d) -------------------------------------------------------------------------------

UTASITAS = """A Károli-biblia 1908-as szövegének szóalakjait modernizáljuk: csak a helyesírás és az igealak változik; a szókincs, a szórend és az írásjel NEM.
Minden sorban egy (már helyesírásilag javított) szóalak, a #94 szótári alakja, a régies jegy (ha van) és a versrészlet, amelyben az alak először áll (a szó ott [szögletes zárójelben]).
Feladat: add meg a szó mai alakját.
- Régies igealak → mai igealak, ugyanazzal az igével és igekötővel, személlyel és számmal: elbeszélt múlt (teremté → teremtette, felele → felelt, monda → mondta, mondának → mondták/mondtak, láték → láttam, lőn → lett, vevé → vette, adaték → adatott), határozói igenév (mondván → mondva), jő → jön. A tárgyas/alanyi ragozást a versrészlet szerint válaszd.
- Ha a szó nem régies igealak (főnév, névutó, mai alak, a -jék felszólító), a mai alak maga a szó, változatlanul.
- Egy szóból egy szó lesz: nem toldasz be és nem hagysz el szót, a szóválasztás marad (nem cseréled más igére). A kezdőbetű marad.
Kimenet: soronként `id<TAB>mai alak`, minden bemeneti sorra pontosan egy, más szöveg nélkül."""


def llm_kerdes(ki, koteg, versek, gy, alakok, alakszotar):
    """A nem automatikus (jelölt) alakok kérdései kisbetűs alakonként, az első előfordulás versrészletével."""
    if os.path.abspath(ki).startswith(ROOT):
        raise SystemExit('a kérdések a repón kívülre mennek')
    fd = Feldolgozo(alakok, alakszotar, None, {})
    kell = {}
    for alak in sorted(gy, key=lambda x: (x.lower(), x)):
        alk, jel, cim = fd.alak_info(alak)
        if alk == 'jelolt' and cim.startswith(('igealak_ritka', 'gyanu:')):  # a felszólító és a kötőhangzós múlt: DT-F96k
            kell.setdefault(alak.lower(), alak)
    elso = {}
    for igehely, sz in versek:
        sp = [m.group(0) for m in BETU.finditer(sz)]
        for i, w in enumerate(sp):
            k = w.lower()
            if k in kell and k not in elso:
                elso[k] = (igehely, ' '.join(sp[max(0, i - 8):i]) + ' [' + w + '] ' + ' '.join(sp[i + 1:i + 9]))
    sorok = []
    for n, k in enumerate(sorted(kell), 1):
        alak = kell[k]
        o, reszlet, sor = alakok.oszt[alak]
        sorok.append(['L%04d' % n, alakszotar[alak][0].lower(), sor['szotari_alak'] if sor else '',
                      sor['regies_jegy'] if sor else '', elso[k][1]])
    os.makedirs(ki, exist_ok=True)
    nk = 0
    for s in range(0, len(sorok), koteg):
        nk += 1
        with open(os.path.join(ki, 'kerdes_%02d.tsv' % nk), 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\talak\tszotari_alak\tjegy\tversreszlet\n')
            for r in sorok[s:s + koteg]:
                f.write('\t'.join(r) + '\n')
    with open(os.path.join(ki, 'utasitas.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(UTASITAS + '\n')
    with open(os.path.join(ki, 'kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        for r in sorok:
            f.write('%s\t%s\n' % (r[0], r[1]))
    print('LLM-kérdés: %d alak, %d köteg → %s' % (len(sorok), nk, ki))


def llm_valasz(ki, modell, alakok, alakszotar, cel=(LLM_TABLA, LLM_NAPLO, 'a nem automatikus (jelölt) igealakok')):
    """A válaszfájlok (valasz_NN.tsv) és a hívásnapló (hivasok.jsonl) beolvasása az igealak_llm.tsv-be."""
    if not modell:
        raise SystemExit('--modell kötelező (a ténylegesen futott modell neve)')
    kulcs = {}
    with open(os.path.join(ki, 'kulcs.tsv'), encoding='utf-8') as f:
        for l in f:
            i, al = l.rstrip('\n').split('\t')
            kulcs[i] = al
    valasz = {}
    hibas = []
    for fn in sorted(os.listdir(ki)):
        if not re.match(r'valasz_\d+\.tsv$', fn):
            continue
        with open(os.path.join(ki, fn), encoding='utf-8') as f:
            for l in f:
                m = l.rstrip('\n').split('\t')
                if len(m) < 2 or m[0] not in kulcs:
                    if l.strip() and not l.startswith('id\t'):
                        hibas.append(l.rstrip('\n'))
                    continue
                valasz[m[0]] = m[1].strip()
    hiany = sorted(set(kulcs) - set(valasz))
    hivasok = []
    if os.path.exists(os.path.join(ki, 'hivasok.jsonl')):
        with open(os.path.join(ki, 'hivasok.jsonl'), encoding='utf-8') as f:
            hivasok = [json.loads(l) for l in f if l.strip()]
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    tabla, naplo, hatokor = cel
    ut = os.path.join(ROOT, tabla)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --llm-valasz (F96.2, DT-F96d) — modell-kimenet (modell_ellenorizetlen), kézzel nem '
                'szerkeszthető | modell=%s (Claude Code, előfizetés, API nélkül) | scope=%s '
                'kisbetűsen (%d kérdés, %d válasz, %d hiányzó) | token: %s | ts=%s\n'
                % (SZKRIPT, modell, hatokor, len(kulcs), len(valasz), len(hiany),
                   sum(h.get('total_tokens', 0) for h in hivasok), ts))
        f.write('alak\tllm_alak\tkerdes_id\n')
        for i in sorted(kulcs):
            if i in valasz:
                f.write('%s\t%s\t%s\n' % (kulcs[i], valasz[i], i))
    with open(os.path.join(ROOT, naplo), 'w', encoding='utf-8', newline='\n') as f:
        for h in hivasok:
            f.write(json.dumps(h, ensure_ascii=False) + '\n')
    print('LLM-válasz: %d / %d; hiányzik: %d %s; értelmezhetetlen sor: %d %s'
          % (len(valasz), len(kulcs), len(hiany), hiany[:10], len(hibas), hibas[:5]))
    print('token (a hívásnaplóból): %d' % sum(h.get('total_tokens', 0) for h in hivasok))


# ---- minta -------------------------------------------------------------------------------------

RETEGEK = [  # (réteg, darab)
    ('igealak:mult.targyas.E3', 8), ('igealak:mult.alanyi.E3', 8), ('igealak:mult.E3', 4),
    ('igealak:mult.T3', 6), ('igealak:mult.E1', 4), ('igealak:hatarozoi_igenev', 6), ('igealak_egyeb', 4),
    ('targyas_heur', 8), ('ek_E1_T3', 4), ('lon', 6), ('vagyon', 2), ('gyanu_kezi', 6),
    ('vala_letige', 10), ('vala_segedige_mult', 8), ('vala_segedige_jelen', 10), ('vala_bizonytalan', 4),
    ('jelolt_ritka', 8), ('jelolt_gyanu', 6), ('felszolito_E2', 4), ('kotohang_mult', 4), ('valtozatlan', 4),
]


def minta_retegek(t):
    rek = set()
    for r in t:
        c = r[6]
        if c.startswith('igealak:'):
            j = c.split('+')[0]
            rek.add(j if j in ('igealak:mult.targyas.E3', 'igealak:mult.alanyi.E3', 'igealak:mult.E3',
                               'igealak:mult.T3', 'igealak:mult.E1', 'igealak:hatarozoi_igenev') else 'igealak_egyeb')
        for k in ('lon', 'vagyon', 'gyanu_kezi', 'vala_letige', 'vala_segedige_mult', 'vala_segedige_jelen',
                  'felszolito_E2', 'kotohang_mult'):
            if c.split('+')[0].startswith(k):
                rek.add(k if k != 'vala_letige' or c.startswith('vala_letige') else k)
        if r[8] in ('targyas_heur', 'ek_E1_T3'):
            rek.add(r[8])
        if r[8] == 'vala_segedige':
            rek.add('vala_bizonytalan')
        if r[9] and c.startswith('igealak_ritka'):
            rek.add('jelolt_ritka')
        if r[9] and c.startswith('gyanu:'):
            rek.add('jelolt_gyanu')
    return rek


def minta(vers_ki, ki_dir, fejlec, fd):
    rnd = random.Random(MAG)
    jelolt = collections.defaultdict(list)
    for ih, (sz, modern, t) in vers_ki.items():
        rek = minta_retegek(t)
        if not rek and sz == modern:
            rek.add('valtozatlan')
        for r in rek:
            jelolt[r].append(ih)
    valasztott, hasznalt = [], set()
    for reteg, db in RETEGEK:
        l = sorted(jelolt[reteg])
        rnd.shuffle(l)
        n = 0
        for ih in l:
            if n >= db:
                break
            if ih in hasznalt:
                continue
            hasznalt.add(ih)
            valasztott.append((reteg, ih))
            n += 1
    sorok = [minta_sor('G%03d' % i, reteg, ih, vers_ki) + ['', ''] for i, (reteg, ih) in enumerate(valasztott, 1)]
    minta_ir(sorok, ki_dir, fejlec, '')


MINTA2 = 'igealak_minta2.tsv'
MAG2 = 20261025
RETEGEK2 = [('veletlen', 100), ('kor3', 20), ('kor3_vala', 10), ('ek_E1_T3', 10)]
MINTA2_SCOPE = ('rögzített magú (%d) minta (N-F96g), %d vers: a veletlen réteg az összes vers egyenletes mintája (a '
                'lefedettség mércéje), a többi a 3. kör cseréinek és az -ék E/1–T/3 választásnak a rétege; az '
                'ellenorzes és a megjegyzes oszlopot a felhasználó tölti, vagy a felhasználó által elfogadott '
                'modell-ellenőrzés (DT-F96n): a vers minden régies igealakja számít, a rossz csere hibás, a '
                'modern szövegben változatlanul maradt régies alak kihagyás (jó / hibás / kihagyás; a megjegyzésben '
                'csere=<n> hiba=<n> kihagyas=<n>)')


def minta2(vers_ki, ki_dir, fejlec):
    """N-F96g: a K1 a lefedettséget is méri: egyenletes véletlen versek, és a 3. kör cseréinek rétegei."""
    rnd = random.Random(MAG2)
    jelolt = collections.defaultdict(list)
    for ih, (sz, modern, t) in vers_ki.items():
        jelolt['veletlen'].append(ih)
        if any('kor3:' in r[6] for r in t):
            jelolt['kor3'].append(ih)
        if any(r[6] == 'vala_segedige_kor3' for r in t):
            jelolt['kor3_vala'].append(ih)
        if any(r[8] == 'ek_E1_T3' for r in t):
            jelolt['ek_E1_T3'].append(ih)
    valasztott, hasznalt = [], set()
    for reteg, db in RETEGEK2:
        l = sorted(jelolt[reteg])
        rnd.shuffle(l)
        n = 0
        for ih in l:
            if n >= db:
                break
            if ih in hasznalt:
                continue
            hasznalt.add(ih)
            valasztott.append((reteg, ih))
            n += 1
    sorok = [minta_sor('H%03d' % i, reteg, ih, vers_ki) + ['', ''] for i, (reteg, ih) in enumerate(valasztott, 1)]
    minta_ir(sorok, ki_dir, fejlec, '', MINTA2, MINTA2_SCOPE % (MAG2, len(sorok)))


def minta_frissit(vers_ki, ki_dir, fejlec, fd, nev='igealak_minta.tsv'):
    ut = os.path.join(ki_dir, nev)
    regi = helyesiras.felhasznaloi_oszlopok(ut, ('minta_id',), ('reteg', 'igehely', 'ellenorzes', 'megjegyzes'))
    sorok = [minta_sor(k[0], v[0], v[1], vers_ki) + [v[2], v[3]] for k, v in sorted(regi.items())]
    minta_ir(sorok, ki_dir, fejlec, ' | a kiválasztás változatlan, a szabály szerint újraszámolva (--minta-frissit)',
             nev, MINTA2_SCOPE % (MAG2, len(sorok)) if nev == MINTA2 else None)


def minta_sor(mid, reteg, ih, vers_ki):
    sz, modern, t = vers_ki[ih]
    valt, alt = [], []
    for r in t:
        if r[4] == 'osszevonva':
            valt.append('%d:%s→(összevonva)' % (r[0], r[1]))
        elif r[4] == 'segedige':
            valt.append('%d:%s→(kiesik, segédige)' % (r[0], r[1]))
        elif r[1] != r[3]:
            valt.append('%d:%s→%s%s' % (r[0], r[1], r[3], ' [.2]' if r[3] != r[2] else ''))
        if r[8]:
            valt.append('%d:%s?(%s)' % (r[0], r[1], r[8]))
        if r[9]:
            alt.append('%d:%s→ %s' % (r[0], r[1], r[9]))
    return [mid, reteg, ih, sz, modern, '; '.join(valt), ' | '.join(alt)]


def minta_ir(sorok, ki_dir, fejlec, megj, nev='igealak_minta.tsv', scope=None):
    if scope is None:
        scope = ('rögzített magú (%d) rétegzett minta, %d vers; az ellenorzes és a megjegyzes oszlopot a felhasználó '
                 'tölti, vagy a felhasználó által elfogadott modell-ellenőrzés (DT-F96n; jó / hibás; a jelölt soron '
                 'A = a jelölt jó, B = maradjon)' % (MAG, len(sorok)))
    with open(os.path.join(ki_dir, nev), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=%s%s\n' % (scope, megj)))
        f.write('\t'.join(['minta_id', 'reteg', 'igehely', 'szoveg_1908', 'szoveg_modern', 'valtozasok', 'jelolt',
                           'ellenorzes', 'megjegyzes']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    print('minta: %d vers; rétegenként: %s' % (len(sorok), dict(collections.Counter(s[1] for s in sorok))))


if __name__ == '__main__':
    main()
