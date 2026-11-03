# -*- coding: utf-8 -*-
"""F123 ANTROP-001 új cikk, U2–U3 — a döntések átvezetése és a lap olvasói adatmezői, nulláról.

Ír (a nem érintett sorok bájtra egyezésének kontrolljával, split('\\t'), CLAUDE.md):
  - adat/elofordulasok.tsv: a 8 ANTROP-001-sor `kapcsolodas`, `funkcio`, `karoli_szo` mezője (kerek mondat;
    „címke — magyarázat”), a `strong` a versben álló Strong (DT502), a szótári gerinc mezői
    (`lexikon_szotar`, `lexikon_entry_id`, `jelentes_szam`); három új sor (1Kor 15:44, 15:46, Júd 1:19);
  - adat/jeloltek.tsv: a 12 `nyitva` jelölt döntése (U2), a Jób 12:10 és a Jón 4:8 külön sora, és a
    teljesség-mérés eltéréseinek lexémánkénti blokk-sorai (`9_` v1, 2. szabály; DT503 mintája);
  - adat/elutasitasi_okok.tsv: az ANTROP-001 saját elutasítási okai (`9_` v1, 1. szabály);
  - adat/motivumok.tsv: `negativ_kriterium`, `folerendelt_fogalom` olvasói nyelven, `forras_study`;
  - adat/szotar_szakasz_cimke.tsv: a gerinc szakaszcímkéi (Thayer G4151, G4152, G5590, G5591; BDB H5315);
  - adat/res_forras.tsv: a rések a `motivumok/ANTROP-001.md`-re mutatnak, a generált rések `adat`;
  - adat/funkcio_kapcsolok.tsv: SZOTARI_GERINC ANTROP-001 `kivetel` → `aktiv` (X.K);
  - adat/lexikon_hivatkozasok.tsv: a gerinc jelentésszámainak kulcssora (a szakasz angol szövege a
    adat/thayer_szakaszok.tsv-ből, illetve a adat/bdb_szakaszok.tsv-ből; ellenoriz.py 17. szabály).
Szerző: claude-opus-5-5, egy kézből (F123_MIGRACIO2_BRIEF.md 2a, U3). A régi `kapcsolodas` csak alapanyag
(archívumban: archivum/ANTROP-001/ANTROP-001_1a_proza_regi.tsv).
Döntés: az orkesztrátor döntése a felhasználó felhatalmazásával (2026-11-03), naplok/F123_ANTROP2_naplo.md U2.
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = 'ANTROP-001'
TS = '2026-11-03'
DATUM = '2026.11.03'
FORRAS = 'F123 ANTROP-001 új cikk, U2 (az orkesztrátor döntése a felhasználó felhatalmazásával, 2026-11-03)'

# igehely: dict(kapcsolodas, funkcio, karoli_szo, strong, szotar, entry, jsz, [pardes_szint új sornál])
P = {
'1Móz 2:7': dict(
    k='Az Úr Isten a föld porából formált ember orrába életnek lehelletét leheli, és „Így lőn az ember élő lélekké”. '
      'A héber szöveg itt nem a lélek és a szellem kettősségéről beszél: a נֶפֶשׁ חַיָּה (nefes chajjá, élő lélek) '
      'az egész, eleven ember, akit Isten lehelete tett élővé. A hely azért áll a motívumban, mert Pál az 1Kor 15:45-ben '
      'ezt a mondatot idézi, és ehhez méri az utolsó Ádámot.',
    f='🌱 ószövetségi háttér — az első ember élő lélekként kap életet Isten leheletétől; ehhez a mondathoz méri az Újszövetség a megelevenítő szellemet',
    karoli='élő lélekké', strong='H5315+H2416', szotar='BDB', entry='H5315', jsz='2'),
'Luk 1:46': dict(
    k='Mária énekének első sorában a lélek, a ψυχή (pszükhé) az alany: „Magasztalja az én lelkem az Urat”. '
      'A mondat a következő versben folytatódik, és ott a szellem lesz az alany; a Károli a két görög szót '
      'egyformán „lelkem”-nek fordítja.',
    f='🎵 párhuzamos sor, első tag — a lélek magasztalja az Urat; a mondat a következő versben a szellemmel folytatódik',
    karoli='az én lelkem', strong='G5590', szotar='Thayer', entry='G5590', jsz='2'),
'Luk 1:47': dict(
    k='Az ének második sorában a szellem, a πνεῦμα (pneuma) az alany: „És örvendez az én lelkem az én megtartó Istenemben.” '
      'A két sor egy mondat, és mindkét szónak saját igéje van: a lélek magasztal, a szellem örvendez. Hogy Mária két '
      'külön valóságot nevez-e meg, vagy a héber költészet módján ugyanazt mondja kétszer, azt az értelmezés szakasza tárgyalja.',
    f='🎵 párhuzamos sor, második tag — a szellem örvendez Istenben; az előző verssel együtt egy mondat',
    karoli='az én lelkem', strong='G4151', szotar='Thayer', entry='G4151', jsz='2'),
'1Kor 2:14': dict(
    k='Pál az érzéki emberről, a görögben ψυχικὸς ἄνθρωπος (pszükhikosz anthróposz) emberről mondja, hogy „nem foghatja '
      'meg az Isten Lelkének dolgait”, mert azok neki bolondságok. A ψυχή szóból képzett melléknév itt nem az ember egyik '
      'részét, hanem egy embertípust nevez meg: azt, aki csak a természetes képességeire támaszkodik, és ezért Isten '
      'Lelkének, a πνεῦμα (pneuma) dolgait nem fogadja be.',
    f='🚪 két embertípus, első tag — az érzéki ember nem fogadja be Isten Lelkének dolgait; párja a következő vers',
    karoli='Érzéki; Isten Lelkének', strong='G4151+G5591', szotar='Thayer', entry='G5591', jsz='b'),
'1Kor 2:15': dict(
    k='Az ellentét második tagja a lelki ember, a görögben πνευματικός (pneumatikosz), aki „mindent megítél, de ő '
      'senkitől sem ítéltetik meg”. Ebben a versben csak a πνεῦμα melléknévi alakja áll; a hely az előző verssel '
      'együtt, az ellentét párjaként tartozik a motívumba.',
    f='🚪 két embertípus, második tag — a Lélektől vezetett ember mindent megítél; az előző vers érzéki emberének ellentétpárja',
    karoli='A lelki ember', strong='G4152', szotar='Thayer', entry='G4152', jsz='3.b'),
'1Kor 15:44': dict(
    k='Pál a feltámadásról szólva a vetett és a feltámadó testet állítja szembe: „Elvettetik érzéki test, feltámasztatik '
      'lelki test.” A görögben a ψυχικόν (pszükhikon) és a πνευματικόν (pneumatikon) áll, a két szó melléknévi alakja, '
      'és a szembeállítás a következő vers ádámi ellentétét készíti elő.',
    f='🌾 két test — a vetett érzéki és a feltámadó lelki test szembeállítása; a következő vers ezt az első és az utolsó Ádámmal indokolja',
    karoli='érzéki test; lelki test', strong='G4152+G5591', szotar='Thayer', entry='G4152', jsz='1',
    pardes='Remez/Sod'),
'1Kor 15:45': dict(
    k='Pál az 1Móz 2:7-et idézi, és ellenpárt állít mellé: „Lőn az első ember, Ádám, élő lélekké; az utolsó Ádám '
      'megelevenítő szellemmé.” Az első Ádám élő lélek, a görögben ψυχή (pszükhé) lett, aki életet kapott; az utolsó '
      'Ádám, a feltámadott Krisztus, szellem, πνεῦμα (pneuma), aki életet ad.',
    f='🎯 csúcspont — az első és az utolsó Ádám szembeállítása; itt fut össze az ószövetségi háttér és az újszövetségi megkülönböztetés',
    karoli='élő lélekké; megelevenítő szellemmé', strong='G4151+G5590', szotar='Thayer', entry='G4151', jsz='3.a'),
'1Kor 15:46': dict(
    k='Pál kimondja a két rend sorrendjét: „De nem a lelki az első, hanem az érzéki, azután a lelki.” Az érzéki, a '
      'görögben ψυχικόν (pszükhikon) a teremtés rendje, a lelki, πνευματικόν (pneumatikon) a feltámadásé, és az ember '
      'útja az elsőtől a második felé vezet.',
    f='🔁 sorrend — előbb az érzéki, azután a lelki: a megkülönböztetés időbeli rendje a feltámadásban',
    karoli='a lelki; az érzéki', strong='G4152+G5591', szotar='Thayer', entry='G4152', jsz='1',
    pardes='Remez/Sod'),
'1Thessz 5:23': dict(
    k='Pál áldó imájában Isten az egész embert szenteli meg, és a görög szöveg az ember három részét egymás mellett, '
      'mindegyiket saját névelővel nevezi meg: a szellemet (πνεῦμα, pneuma), a lelket (ψυχή, pszükhé) és a testet '
      '(σῶμα, szóma). A Károli a szellemet „egész valótok”-nak fordítja, ezért a magyar szövegben a hármasság kevésbé látszik.',
    f='🔺 hármas felsorolás — a szellem, a lélek és a test egymás mellett: a megkülönböztetés legvilágosabb helye',
    karoli='valótok; lelketek', strong='G4151+G5590', szotar='Thayer', entry='G4151', jsz='2'),
'Zsid 4:12': dict(
    k='Isten beszéde élesebb minden kétélű fegyvernél, és „elhat a szívnek és léleknek, az ízeknek és a velőknek '
      'megoszlásáig”. A görögben a lélek (ψυχή, pszükhé) és a szellem (πνεῦμα, pneuma) áll, a Károli az előbbit '
      'szívnek, az utóbbit léleknek fordítja. A vers szerint a kettő között határ van, de ezt a határt csak Isten szava hatja át.',
    f='⚔️ szétválasztás — Isten beszéde a lélek és a szellem határáig hatol: a különbség létezik, de csak Isten szava teszi láthatóvá',
    karoli='szívnek; léleknek', strong='G4151+G5590', szotar='Thayer', entry='G4151', jsz='2'),
'Júd 1:19': dict(
    k='Júdás a gyülekezetbe befurakodott szakadárokról mondja: „Ezek azok, a kik különszakadnak, érzékiek, kikben '
      'nincsen Szent Lélek.” A görögben az érzékiek, ψυχικοί (pszükhikoi) mellett a Lélek, πνεῦμα (pneuma) hiánya áll; '
      'a görög szöveg csak Lelket mond, a Károli Szent Lélekként érti.',
    f='⚠️ figyelmeztetés — az érzékiek, akikben nincs Lélek: a két embertípus megkülönböztetése a gyülekezet szakadárain',
    karoli='érzékiek; Szent Lélek', strong='G4151+G5591', szotar='Thayer', entry='G5591', jsz='b',
    pardes='Drash'),
}
UJ = ('1Kor 15:44', '1Kor 15:46', 'Júd 1:19')
SORREND = ['1Móz 2:7', 'Luk 1:46', 'Luk 1:47', '1Kor 2:14', '1Kor 2:15', '1Kor 15:44', '1Kor 15:45', '1Kor 15:46',
           '1Thessz 5:23', 'Zsid 4:12', 'Júd 1:19']
UJ_PROV = 'scope=manual | forras=' + FORRAS + '; jeloltek.tsv beépítve | ts=' + TS

# a nyitott jelöltek döntése (U2)
NEM_EGY = 'A két szó nem egy mondatban áll: '
NEM_MEGK = 'A két szó nem megkülönböztető szerepben áll: '
JELOLT = {
    '1Kor 15:44': ('beépítve', 'A vetett „érzéki test” és a feltámadó „lelki test” szembeállítása: a görögben a ψυχή és a πνεῦμα melléknévi alakja egy mondatban, kifejezett ellentétben áll. Döntés: beépítve.'),
    '1Kor 15:46': ('beépítve', 'Az „érzéki” és a „lelki” sorrendje egy mondatban: a görögben a ψυχή és a πνεῦμα melléknévi alakja, kifejezett ellentétben. Döntés: beépítve.'),
    'Júd 1:19': ('beépítve', 'Az „érzékiek”, akikben „nincsen Szent Lélek”: a ψυχή melléknévi alakja és a πνεῦμα egy mondatban, szembeállítva, az 1Kor 2:14 mintájára. Döntés: beépítve.'),
    'Fil 1:27': ('elutasítva', NEM_MEGK + 'az „egy lélekben, egy érzéssel” két párhuzamos tagja a közösség egységét mondja ki, a görögben a πνεῦμα és a ψυχή itt egymás szinonimája (a Thayer szerint a ψυχή helyén a „szív” is állhatna). Határeset: a lap a módszertani részben megnevezi.'),
    '1Pét 1:22': ('elutasítva', NEM_MEGK + 'a lelket (ψυχή) a Lélek (πνεῦμα), Isten Lelke tisztítja meg, a két szó nem az ember két belső összetevője. A „Lélek által” szavak csak a Károli alapszövegében (Textus Receptus) állnak, a kritikai kiadásokban nincsenek.'),
    'Mt 12:18': ('elutasítva', NEM_MEGK + 'az Ézs 42:1 idézetében mindkét szó Istenről szól („az én lelkem kedvét lelé”, „lelkemet adom ő belé”), nem az ember belső életéről.'),
    'Luk 9:55-56': ('elutasítva', NEM_EGY + 'a „minémű lélek van ti bennetek” és az „emberek lelkét” két külön mondat, és a lélek az egyikben indulat, a másikban élet. A két szó csak a Károli alapszövegében (Textus Receptus) áll, a kritikai kiadásokban nincs.'),
    'ApCsel 4:31-32': ('elutasítva', NEM_EGY + 'a 31. versben a Szent Lélek tölti be a hívőket, a 32. versben a hívők sokaságának „szíve-lelke egy vala”; a két vers két külön mondat.'),
    'ApCsel 20:23-24': ('elutasítva', NEM_EGY + 'a Szent Lélek bizonyságtétele és Pál élete („az én életem sem drága nékem”) két külön mondatban áll.'),
    '2Kor 1:22-23': ('elutasítva', NEM_EGY + 'a „léleknek zálogát” és az „Istent hívom bizonyságul az én lelkemre” két külön mondat.'),
    '1Pét 3:19-20': ('elutasítva', NEM_MEGK + 'a „tömlöczben lévő lelkek” (πνεῦμα) és a bárkában megmenekült „nyolcz lélek” (ψυχή) két külön csoport, a mondat nem az ember belső életét tagolja.'),
    'Júd 1:19-20': ('elutasítva', 'Ugyanaz a hely, mint a Júd 1:19 sora: a 20. vers csak a Szent Lelket nevezi meg, a ψυχή nem áll benne.'),
}
KULON = {
    'Jób 12:10': ('A Septuaginta többlete: a görög fordítás a ψυχή és a πνεῦμα szót hozza („minden élő állatnak élete, és minden egyes embernek a lelke”), a héber szövegben viszont a nefes és a rúah áll. A motívum az eredeti szövegre épül, ezért a hely nem előfordulás; a lap tényként említi.', 'élete; lelke'),
    'Jón 4:8': ('A Septuaginta többlete: a görög fordításban a ψυχή és a πνεῦμα áll, de a πνεῦμα itt a keleti szél („tikkasztó keleti szelet”), nem az ember szelleme. Döntés: elutasítva.', ''),
}
KULON_FK = ('F123 U1 teljesség-mérés, szópár-háló, a héber pár Septuaginta-hídja (DT503 külön sora; naplok/F123_teljesseg_ANTROP-001.md 4.) '
            '| scope=manual | forras=eszkozok/teljesseg_meres.py, naplok/F123_adat_keszito.py lxx | ts=' + TS)

# a teljesség-mérés eltéréseinek lexémánkénti blokkjai (a teljesseg_ANTROP-001_blokkok.tsv osztálya szerint)
BLOKK = [
    ('heber_par', 'lélek', 'a héber nefes és chajjá („élő lélek”, „élet”) egy versben áll, a görög szópár nélkül; a motívum a görög szópár megkülönböztető együttállására épül, ezért a héber kifejezés önmagában nem tartozik ide (az 1Móz 2:7 kivétel, mert az 1Kor 15:45 idézi)'),
    ('ruah_nefes', 'lélek', 'a héber rúah és nefes egy versben áll; a motívum a görög szópár megkülönböztető együttállására épül, a héber szópár a tágabb körbe tartozik'),
    ('csak_pneuma', 'lélek, szellem', 'csak a πνεῦμα (pneuma) áll a versben, a ψυχή nem; legtöbbször a Szent Lélekről'),
    ('csak_pszukhe', 'lélek', 'csak a ψυχή (pszükhé) áll a versben, a πνεῦμα nem; legtöbbször az élet vagy a személy értelmében'),
    ('csak_pneumatikosz', 'lelki', 'csak a πνευματικός (pneumatikosz) áll a versben, a ψυχή és a ψυχικός nem'),
    ('csak_pszukhikosz', 'testi', 'csak a ψυχικός (pszükhikosz) áll a versben, a πνεῦμα és a πνευματικός nem'),
    ('nefes', 'lélek', 'csak a héber nefes áll a versben'),
    ('ruah', 'lélek', 'csak a héber rúah áll a versben'),
    ('chajja', '', 'csak a héber chaj, chajjá (élő, élet) áll a versben; a szótár idézi'),
    ('mas_heber', 'lélek', 'a Károli „lélek” szava vagy a szótár idézete más héber szót (például nesámá, lehelet; lév, szív) fordít, a motívum szava nincs a versben'),
    ('mas_gorog', 'lélek, lelki', 'a Károli „lélek” szava vagy a szótár idézete más görög szót fordít, a motívum szava nincs a versben'),
]
BLOKK_KIVEVE = {'Jób 12:10', 'Jón 4:8'}  # a heber_par két külön sora

OKOK = [
    ('1', '^a két szó nem egy mondatban', 'a két szó nem egy mondatban áll', 'a ψυχή és a πνεῦμα két külön mondatban áll'),
    ('2', '^a két szó nem megkülönböztető', 'a két szó nem megkülönböztető szerepben', 'a két szó egy mondatban áll, de nem az ember két belső összetevőjét különbözteti meg'),
    ('3', '^a septuaginta többlete', 'a Septuaginta többlete, az eredetiben nincs a szópár', 'a görög fordítás hozza a szópárt, az eredeti szövegben nem áll'),
    ('4', '^ugyanaz a hely', 'a hely egy másik sorban áll', 'a versablak tartomány-sora; a hely a saját sorában szerepel'),
    ('5', '^összesítő sor', 'csak az egyik szó vagy más szó áll a versben (összesítő sor)', 'lexémánként egy blokk-sor a teljesség-mérés eltéréseire'),
]

NEGATIV = ('A versben (vagy a két versen átnyúló egy mondatban) a görög πνεῦμα (pneuma, szellem) és ψυχή (pszükhé, lélek) — '
           'vagy melléknévi alakjuk, a πνευματικός (pneumatikosz, lelki) és a ψυχικός (pszükhikosz, érzéki) — együtt áll, és a '
           'mondat a kettőt megkülönbözteti vagy szembeállítja. Az újszövetségi helyeken a Károli alapszövege, a Textus Receptus '
           'a mérce; ahol a kritikai kiadások eltérnek, a lap jelöli. Nem tartozik ide a vers, amelyben csak az egyik szó áll, '
           'amelyben a két szó két külön mondatban áll, vagy amelyben a kettő egymás szinonimája, illetve nem az ember belső '
           'életéről szól. Kivétel az 1Móz 2:7: a héber נֶפֶשׁ חַיָּה (nefes chajjá, élő lélek) azért tartozik ide, mert az '
           '1Kor 15:45 ezt idézi, és ennek ellenpárjaként mondja ki a megelevenítő szellemet.')
FOLERENDELT = 'az ember belső élete, lelke és szelleme általában, a két szó megkülönböztető együttállása nélkül'

CIMKE = [
    ('Thayer', 'G4151', '-/2/-', '2', 'az ember szelleme: az élet és a gondolkodás elve'),
    ('Thayer', 'G4151', '-/3/-', '', 'szellem mint önálló, anyagtalan lény'),
    ('Thayer', 'G4151', '-/3/a', '3.a', 'szellem általában; a feltámadt Krisztusról: megelevenítő szellem'),
    ('Thayer', 'G5590', '-/2/-', '2', 'a lélek mint az érzelmek és a vágyak székhelye'),
    ('Thayer', 'G4152', '-/1/-', '1', 'az ember szellemére vonatkozó, a lélekkel szembeállítva'),
    ('Thayer', 'G4152', '-/3/-', '', 'az isteni Lélekhez tartozó'),
    ('Thayer', 'G4152', '-/3/b', '3.b', 'Isten Lelkétől betöltött és vezetett ember'),
    ('Thayer', 'G5591', '-/-/b', 'b', 'az érzéki természettől vezérelt'),
    ('BDB', 'H5315', '-/2/-', '2', 'Isten leheletétől élő lénnyé lett lélek'),
]
CIMKE_PROV = 'scope=manual | forras=' + FORRAS + ' (a szakasz szövege: adat/thayer_szakaszok.tsv, adat/bdb_szakaszok.tsv) | ts=' + TS

RES_TANULMANY = ('kivonat', 'miert_fontos', 'ertelmezes', 'alkalmazas', 'modszertan')
RES_ADAT = {'2b': '### 2/b. Kiegészítő szótári adatok *(generált)*', 'minosites': '### Minősítés *(generált)*',
            'alatamasztas': '### Alátámasztás *(generált)*'}
TANITOI = 'Ehhez a motívumhoz nevesített tanítói egyezés még nem került a lapra; a hiány nincs kitöltve.'


def nyit(ut):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers.split(nl), nl


def ir(ut, sorok, nl):
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


def fej_ix(sorok, kezd):
    i = next(k for k, s in enumerate(sorok) if s.startswith(kezd))
    return i, {n: j for j, n in enumerate(sorok[i].split('\t'))}


def kontroll(regi, uj, erintett):
    a = [s for k, s in enumerate(regi) if k not in erintett]
    b = [s for k, s in enumerate(uj) if k not in erintett]
    if a != b:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')


def kitolt(m, ix, ige):
    d = P[ige]
    m[ix['kapcsolodas']], m[ix['funkcio']], m[ix['karoli_szo']] = d['k'], d['f'], d['karoli']
    m[ix['strong']] = d['strong']
    m[ix['lexikon_szotar']], m[ix['lexikon_entry_id']], m[ix['jelentes_szam']] = d['szotar'], d['entry'], d['jsz']


def elofordulasok():
    ut = os.path.join(GY, 'adat', 'elofordulasok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    regi_ix, latott, minta = [], set(), None
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and m[0] == ID:
            regi_ix.append(k)
            latott.add(m[ix['igehely']])
            minta = m
    assert latott == set(P) - set(UJ), latott
    # a motívum sorai egy blokkban, kanonikus sorrendben (a régi sorok a helyükön, az újak közéjük)
    assert regi_ix == list(range(regi_ix[0], regi_ix[-1] + 1)), regi_ix
    regi = {sorok[k].split('\t')[ix['igehely']]: sorok[k].split('\t') for k in regi_ix}
    blokk = []
    for ige in SORREND:
        if ige in regi:
            m = list(regi[ige])
        else:
            m = [''] * len(ix)
            m[ix['id']], m[ix['igehely']] = ID, ige
            m[ix['pardes_szint']] = P[ige]['pardes']
            m[ix['gerinc_elem']] = 'G4151+G5590'
            m[ix['azonositas_modja']] = 'tartalom-alapú'
            m[ix['megbizhatosag']] = 'magas'
            m[ix['proveniencia']] = UJ_PROV
            m[ix['igazolas']] = minta[ix['igazolas']]
            m[ix['fo_elofordulas']] = {'Júd 1:19': 'Júd 1:19'}.get(ige, '1Kor 15:44-46')
        kitolt(m, ix, ige)
        blokk.append('\t'.join(m))
    uj = sorok[:regi_ix[0]] + blokk + sorok[regi_ix[-1] + 1:]
    a = sorok[:regi_ix[0]] + sorok[regi_ix[-1] + 1:]
    b = uj[:regi_ix[0]] + uj[regi_ix[0] + len(blokk):]
    if a != b:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
    ir(ut, uj, nl)
    print('elofordulasok.tsv: %d sor (8 átírva, %d új)' % (len(blokk), len(UJ)))


def blokk_versek():
    ut = os.path.join(GY, 'naplok', 'F123_teljesseg_ANTROP-001_blokkok.tsv')
    v = {}
    for s in io.open(ut, encoding='utf-8').read().split('\n'):
        if s.startswith('#') or s.startswith('igehely\t') or not s.strip():
            continue
        m = s.split('\t')
        if m[0] in BLOKK_KIVEVE:
            continue
        v.setdefault(m[2], []).append(m[0])
    return v


def jeloltek():
    ut = os.path.join(GY, 'adat', 'jeloltek.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'id\t')
    uj, erintett, latott, kulcsok, utolso = list(sorok), set(), set(), set(), None
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k <= fi or m[0] != ID:
            continue
        utolso = k
        kulcsok.add((m[ix['igehely']], m[ix['jelolt_tipus']], m[ix['cel_id']]))
        ige = m[ix['igehely']]
        if m[ix['dontes']] == 'nyitva':
            assert ige in JELOLT, ige
            m[ix['dontes']], m[ix['indoklas']] = JELOLT[ige]
            m[ix['datum']] = DATUM
            uj[k] = '\t'.join(m)
            erintett.add(k)
            latott.add(ige)
        elif ige in P and m[ix['dontes']] == 'beépítve':
            pass
    assert latott == set(JELOLT), set(JELOLT) - latott
    kontroll(sorok, uj, erintett)
    hozza = []

    def sor(ige, fk, ind, karoli=''):
        assert (ige, 'elofordulas', '') not in kulcsok, ige
        kulcsok.add((ige, 'elofordulas', ''))
        m = [''] * len(ix)
        m[ix['id']], m[ix['igehely']], m[ix['forras_kereses']] = ID, ige, fk
        m[ix['dontes']], m[ix['indoklas']], m[ix['karoli_szo']] = 'elutasítva', ind, karoli
        m[ix['datum']], m[ix['jelolt_tipus']] = DATUM, 'elofordulas'
        hozza.append('\t'.join(m))

    for ige, (ind, karoli) in KULON.items():
        sor(ige, KULON_FK, ind, karoli)
    versek = blokk_versek()
    for osztaly, karoli, szoveg in BLOKK:
        vl = versek.get(osztaly, [])
        if not vl:
            continue
        fk = ('F123 U1 teljesség-mérés, blokk-kizárás (9_ v1, 2. szabály; DT503 mintája): %d vers, az első itt; a lista: '
              'naplok/F123_teljesseg_ANTROP-001_blokkok.tsv (osztaly=%s), naplok/F123_teljesseg_ANTROP-001.md '
              '| scope=manual | forras=eszkozok/teljesseg_meres.py, naplok/F123_ANTROP2_osztaly.py | ts=%s' % (len(vl), osztaly, TS))
        ind = ('Összesítő sor %d versre (az első itt áll): %s. A motívumhoz az a vers tartozik, amelyben a két szó (vagy '
               'melléknévi alakjuk) egy mondatban, egymástól megkülönböztetve áll, ezért egyik sem tartozik ide; a teljes '
               'lista a lap készítőinek módszertani naplójában.' % (len(vl), szoveg))
        sor(vl[0], fk, ind, karoli)
    uj = uj[:utolso + 1] + hozza + uj[utolso + 1:]
    ir(ut, uj, nl)
    print('jeloltek.tsv: %d döntés, %d új sor (2 külön, %d blokk)' % (len(erintett), len(hozza), len(hozza) - 2))


def elutasitasi_okok():
    ut = os.path.join(GY, 'adat', 'elutasitasi_okok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'sorrend\t')
    assert not any(s.split('\t')[1:2] == [ID] for s in sorok[fi + 1:])
    utolso = max(k for k, s in enumerate(sorok) if s.strip())
    prov = 'scope=manual | forras=' + FORRAS + ' (9_ v1, 1. szabály) | ts=' + TS
    hozza = ['\t'.join([n, ID, minta, cimke, megj, prov]) for n, minta, cimke, megj in OKOK]
    uj = sorok[:utolso + 1] + hozza + sorok[utolso + 1:]
    ir(ut, uj, nl)
    print('elutasitasi_okok.tsv: %d sor' % len(hozza))


def egy_sor(fajl, kezd, feltetel, modosit, varhato=1):
    ut = os.path.join(GY, 'adat', fajl)
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, kezd)
    uj, erintett = list(sorok), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k > fi and feltetel(m, ix):
            modosit(m, ix)
            uj[k] = '\t'.join(m)
            erintett.add(k)
    assert len(erintett) == varhato, (fajl, len(erintett))
    kontroll(sorok, uj, erintett)
    ir(ut, uj, nl)
    print('%s: %d sor' % (fajl, len(erintett)))


def motivumok():
    def mod(m, ix):
        m[ix['negativ_kriterium']], m[ix['folerendelt_fogalom']] = NEGATIV, FOLERENDELT
        m[ix['forras_study']] = 'motivumok/ANTROP-001.md'
    egy_sor('motivumok.tsv', 'id\t', lambda m, ix: m[0] == ID, mod)


def res():
    def mod(m, ix):
        r = m[ix['res']]
        if r in RES_TANULMANY:
            m[ix['forras']], m[ix['tanulmany']] = 'tanulmany', 'motivumok/ANTROP-001.md'
            m[ix['fejlec']] = m[ix['fejlec']].replace('*(generált)*', '*(kézi)*')
        elif r in RES_ADAT:
            m[ix['forras']], m[ix['fejlec']] = 'adat', RES_ADAT[r]
            if r != 'alatamasztas':
                m[ix['tanulmany']] = ''
        elif r == 'tanitoi':
            m[ix['forras']], m[ix['tanulmany']] = 'adat', TANITOI
    egy_sor('res_forras.tsv', 'id\t', lambda m, ix: m[0] == ID, mod, varhato=9)


def kapcsolo():
    def mod(m, ix):
        m[ix['allapot']] = 'aktiv'
        m[ix['indok']] = 'a szótári gerinc a motívumon kész (F123 ANTROP-001 új cikk: a szakaszcímkék és a sorok szótári mezői)'
        m[ix['proveniencia']] = 'scope=manual | forras=' + FORRAS + ' | ts=' + TS
    egy_sor('funkcio_kapcsolok.tsv', 'kapcsolo\t', lambda m, ix: m[0] == 'SZOTARI_GERINC' and m[1] == ID, mod)


def cimke():
    ut = os.path.join(GY, 'adat', 'szotar_szakasz_cimke.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'szotar\t')
    meglevo = {tuple(s.split('\t')[:3]) for s in sorok[fi + 1:] if s.strip()}
    for c in CIMKE:
        assert c[:3] not in meglevo, c
    utolso = max(k for k, s in enumerate(sorok) if s.strip())
    hozza = ['\t'.join([sz, st, ut_, jsz, hu, CIMKE_PROV, '']) for sz, st, ut_, jsz, hu in CIMKE]
    uj = sorok[:utolso + 1] + hozza + sorok[utolso + 1:]
    ir(ut, uj, nl)
    print('szotar_szakasz_cimke.tsv: %d sor' % len(hozza))


def hivatkozas():
    """A szakaszcímkék kutatói kulcsa létező lexikon_hivatkozasok-kulcs legyen (17. szabály): szoveg_en =
    a szakasz szövege a jelével (a G0086 „2” sorának mintája)."""
    def szakaszok(fajl, kulcs_mezok):
        sorok, _ = nyit(os.path.join(GY, 'adat', fajl))
        fi, ix = fej_ix(sorok, 'strong	')
        d = {}
        for s in sorok[fi + 1:]:
            m = s.split('	')
            if len(m) < len(ix):
                continue
            k = (m[ix['strong']], m[ix['utvonal']])
            jel = m[ix['jel']].strip()
            d.setdefault(k, ((jel + ' ') if jel else '') + m[ix['szoveg']])
        return d
    th = szakaszok('thayer_szakaszok.tsv', None)
    bdb = szakaszok('bdb_szakaszok.tsv', None)
    ut = os.path.join(GY, 'adat', 'lexikon_hivatkozasok.tsv')
    sorok, nl = nyit(ut)
    fi, ix = fej_ix(sorok, 'strong	')
    meglevo = {tuple(s.split('	')[:4]) for s in sorok[fi + 1:] if s.strip()}
    hozza = []
    for sz, st, utv, jsz, _hu in CIMKE:
        if not jsz:
            continue
        szoveg = (th if sz == 'Thayer' else bdb)[(st, utv)]
        k = (st, sz, st, jsz)
        assert k not in meglevo, k
        forras = 'adat/thayer_szakaszok.tsv' if sz == 'Thayer' else 'adat/bdb_szakaszok.tsv'
        hozza.append('	'.join([st, sz, st, jsz, szoveg, forras]))
    utolso = max(k for k, s in enumerate(sorok) if s.strip())
    uj = sorok[:utolso + 1] + hozza + sorok[utolso + 1:]
    ir(ut, uj, nl)
    print('lexikon_hivatkozasok.tsv: %d sor' % len(hozza))


if __name__ == '__main__':
    elofordulasok()
    jeloltek()
    elutasitasi_okok()
    motivumok()
    res()
    kapcsolo()
    cimke()
    hivatkozas()
