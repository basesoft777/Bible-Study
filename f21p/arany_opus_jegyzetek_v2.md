# f21p/arany_opus_jegyzetek_v2.md — kísérőjegyzet az Opus-aranyhoz, v2 (F21 P3c)

> **v2 (2026.09.30, F21.41).** Az 1–7. szakasz a v1 jegyzet (`f21p/arany_opus_jegyzetek.md`,
> érintetlen) szó szerinti szövege, a v1 címsora nélkül. Új a 8. szakasz: a felhasználó
> DT21 a–e döntései (PD13) konvencióként; ahol a 8. szakasz és a 2. szakasz eltér, a 8.
> szakasz az irányadó. A 6. táblázat nem bővül (PD10, PD12). Az arany v3-ra gyakorolt hatás
> javaslat, jóváhagyásig nem fagy be: `naplok/F21P_arany_v3_diff.md`.
>
> *(A v1 címsora: „f21p/arany_opus_jegyzetek.md — kísérőjegyzet az Opus-aranyhoz (F21 P1)”.)*

*Forrás: `f21p/arany_opus.jsonl` (60 vers), `f21p/opus_arany_kivalasztas.tsv`. A párosítás
kézi ítélet a `prompt_v1.md` szabályai szerint, a modellválaszok ismerete nélkül. Ez a
jegyzet nem dönt: a nyitott kérdéseket jelzi, opciókkal. Ellenőrzést nem helyettesít.*

Gépi állapot (szkriptkimenet, `python eszkozok/karoli_strong/arany_ellenoriz.py`):
60 vers, 60/60 átmegy a kapun (mind az öt pont), 1044 link; rétegcsoportok R1=20,
R2+R3=20, R4=20; `[nem TR]` jelölésű eredeti szó nincs párosítva.

## 1. A kiválasztás

`eszkozok/karoli_strong/arany_kivalaszt.py`, mag 20260930. Rétegcsoportonként két teljes
10 verses köteg (a köteghatár nem törik): R1: két köteg két különböző könyvből; R2+R3: egy
tisztán R2-es és egy tisztán R3-as köteg; R4: egy evangéliumi és egy levél-köteg. Húzott
kötegek: **6, 10** (R1: 2Móz 10 + Péld 10), **12, 15** (R2: Jób 2 + Zsolt 8; R3: Jer 2 + Ez 8),
**16, 20** (R4: Mt 7 + Mk 3; Jak 5 + 1Pét 3 + 2Pét 1 + 1Ján 1).

Következmények, döntésre:

- **A 60 versben nincs 1Mózes-vers**, tehát a régi arany (`Karoli_Strong_kivonat.tsv`) és
  az Opus-arany között nincs átfedés. A „régi arany egyezés” mérőszámot ez nem érinti (az a
  200 versen mér), de az Opus-arany és a régi arany egymáshoz nem kalibrálható.
  Opció: (a) így marad; (b) az R1 párhúzását egy 1Móz-kötegre kötni (a szkriptben egy
  feltétel). Javaslat: (a), mert a brief nem kéri az átfedést.
- A könyvarány (40/30/30) egész kötegekkel nem tartható; az R1 két könyvet fed le.

## 2. Egységesen alkalmazott konvenciók (a prompt értelmezése)

A prompt ezeket nem rögzíti betű szerint; a mérés szempontjából számít, hogy a modellek
ugyanígy olvassák-e. Mindegyik opció átmegy a kapun.

1. **Névelők.** Az önálló magyar *a/az* mindig `betoldas`, a héber H9009 és a görög névelő
   `forditatlan` — kivéve, ha névmásként áll (vonatkozó *a ki, a mely, a kik*; görög
   *ὁ δέ* = *Ő pedig*; *τοῦ εὐθύνοντος* = *kormányos*; *τὸν [fiát]*). Ilyenkor a
   párosítás a magyar névmásra (ha kettéírt, mindkét tokenre) megy. 16 ilyen eset van
   (az ellenőrző tájékoztató listája).
2. **Kettéírt Károli-kötőszók** (*a mint, a hogy, a miképen, a mely*): ha van eredeti
   megfelelő (*כַּאֲשֶׁר, ὡς, ἧς*), mindkét token arra; ha nincs (a vonatkozó mondat egy
   héber melléknévi igenevet fordít: Péld 28:17 *a kit*, 29:5 *a ki*, 30:17 *mely*, Ez 22:25
   *mely*, 2Móz 26:13 *a mi*, Zsolt 18:1 *a melyen*, Mt 4:4 *a mely*, Mt 21:4 *a ki*),
   `betoldas`. Opció: az igenévhez kötni.
3. **Tárgyjelölő névmási raggal** (*אֹתָם, אֶתְהֶן, אוֹתָךְ*): az *'et* `forditatlan`, a
   magyar névmás (*azt, őket, téged, azokat, őt*) csak a ragra (H90xx) megy. Érintett:
   2Móz 20:25, 29:4, 30:3, Zsolt 18:1, Ez 16:57, 33:31. Opció: a névmás az *'et*-re és a
   ragra együtt.
4. **Birtokos és névmási ragok** (H9020–H9040): a birtokos személyragot viselő magyar szóhoz
   (*fiam* ← בְּנִ + י), és ha a magyar külön névmást is kitesz (*az ő ura, az én
   kősziklám*), a névmáshoz is (egy eredeti több párban).
5. **Igekötő különírva** (*meg, el, ki, le, fel, be, által, oda, alá*): az ige eredetijéhez
   párosítva, nem `betoldas`. Opció: `betoldas`.
6. **Külön kitett magyar alanyi névmás** eredeti névmás nélkül (Zsolt 16:11 *Te*, Jób 34:28
   *ő*, Ez 46:12 *ő*, 2Móz 25:8 *ő*, Zsolt 22:32 *ő*): `betoldas`.
7. **Segédige** (*vala, fog, fogunk, van, vannak, volna, lészen* ahol nincs הָיָה): `betoldas`;
   kivétel Mt 4:4 *Meg van írva*, ahol mindhárom token a γέγραπται-ra megy.
8. **H9012 / H9013** (nyomatékos *-āh*, paragogikus *nun*): `forditatlan`.
9. **Le nem fordított *ve-* / *καί***: `forditatlan`; ha a magyarban *pedig, s, is, de, hogy*
   áll a helyén, arra párosítva.
10. **Összeolvadt névelő + elöljáró** (*בַּ* [in the], τῆς): ha Károli *e/ez* mutató névmással
    adja (Péld 23:19 *ez úton*, Mk 2:10 *e földön*), a mutató névmás az elöljáró/névelő
    sorára megy.

## 3. TAHOT változatsorok (X, Q(K), Q(k))

A 60 vers nyers TAHOT-csoportjaiban (STEPBible-Data, `Translators Amalgamated OT+NT`)
**X-típusú sor nincs**. Három Qere/Ketiv-eset:

| Vers | Nyers sor | A kivonatban | Kezelés az aranyban | Kérdés |
|---|---|---|---|---|
| Péld 24:1 | `Pro.24.1#06=Q(k)` תִּתְאָו | a Qere sor (8), H0183 | szokásos párosítás: *kivánj* → 8 | nincs (a kis *k* csak helyesírási eltérés) |
| Péld 25:24 | `Pro.25.24#07=Q(K)` מִדְיָנִים; K= מְדוֹנִים H4066 | csak a Qere sor (8), H4079; a Ketiv-szó nem sor | *háborgó* → 8 | a KJV-támpont mindkét Strongot mutatja (`{H4079} {H4066}`); a mérés a Qere H4079-et veszi |
| Jer 51:3 | `Jer.51.3#03=Q(K)` üres Qere-helyőrző; K= יִדְרֹךְ | a kivonat kihagyja (a Ketiv második igéje nem sor) | *kézívesre* → 1, *kézíves* → 4, *vonja fel* → 2 | l. lent |

**Jer 51:3 részletesen.** Károli a Ketivet követi (*A kézívesre kézíves vonja fel íjját*: a
kettőzött *yidrokh* egyike a *kézívesre* része), és az első és hatodik *אֶל* szót „felé,
ellen” értelemben olvassa (*kézívesre, arra*), a TAHOT viszont H0408 (*ne*) címkét ad
nekik. Az aranyban a *kézívesre* → 1 és az *arra* → 8 párosítás így a mérőszkriptben H0408
Strongot kap, holott Károli értelmezésében H0413. Opció: (a) így marad (a párosítás a
sorszámra helyes, a Strong a TAHOT-é); (b) a vers kizárása a pontossági mérésből; (c) a
két link `forditatlan`/`betoldas`-ra cserélése. Javaslat: (a), a jelentésben jelölve.

## 4. A `[nem TR]` jelölés hibája (P0-hatás, nem az arany hibája)

> **Lezárva (F21.6, a felhasználó döntése alapján):** a `tokenek.py` a „TR»N” / „TR«N”
> tagot TR-nek számítja; a „más helyen” tokenek TR-helyes aranya átvezetve (a 7. pont
> mutatja, régi → új); a három „eltérő alak” token az `f21p/meres_kizaras.tsv` szerint
> kimarad a pontossági mérésből. Az alábbi szöveg az F21.4-es állapotot írja le.

A `tokenek.betolt_eredeti` a `[nem TR]` jelzőt így számolja: `'TR' not in r[7].split('+')`.
Ez két esetben téves:

- **„TR»N” / „TR«N”** (a szó a TR-ben is megvan, csak más helyen áll): a `split('+')`
  után a tag `TR»3`, nem `TR`, ezért a szó `[nem TR]` jelölést kap.
- **A TR eltérő alakot olvas** (`N(k)O` típus, a variánsoszlopban „in: TR”): a TR-alak
  nem külön sor, így a Károli által fordított szónak nincs sora; a meglévő sor valóban
  nem TR-es, de a magyar szónak így nincs eredetije.

Szkriptkimenet a 200 verses minta R4-rétegére (scratch-szkript, a nyers TAGNT
`editions` oszlopával összevetve): 31 `[nem TR]` sor; ebből **5 valódi**, **11 „TR-ben más
helyen”**, **15 „TR-ben eltérő alak”**. Az aranyba eső 60 versben 10 ilyen sor, 6 versben:
Mt 4:4 (11 ὁ — valódi), Mk 2:10 (12 — más helyen), Mk 2:23 (7, 15 — más helyen), Jak 3:4
(9 — más helyen; 22 — eltérő alak), Jak 3:8 (5 — más helyen; 8 — eltérő alak), 1Pét 5:12
(23 — eltérő alak).

**Az aranyban a prompt 5. szabálya szerint jártam el** (minden `[nem TR]` sor
`forditatlan`, a hozzá tartozó magyar szó `betoldas`), mert a modellek ugyanezt a bemenetet
és szabályt kapják. Ez öt versben nyelvileg hibás párosítást ad (pl. Mk 2:10 *bűnöket*,
Mk 2:23 *megy … által*, *kezdék*, Jak 3:8 *fékezhetetlen*). **Döntés szükséges** (nem az
én hatásköröm): (a) a `tokenek.py` javítása („TR»/«” TR-nek számít) a P3 előtt, és az öt
versre az alábbi alternatív arany; (b) a jelenlegi állapot marad, a jelentés jelöli;
(c) az érintett versek kizárása a pontossági mérésből. Javaslat: (a) a „más helyen” esetre;
az „eltérő alak” esetre a TR-alak nem pótolható sor nélkül, ott (b) vagy (c).

Alternatív (TR-helyes) arany az öt versre, mind átmegy a kapun (a `[nem TR]` ellenőrzés
nélkül; scratch-szkripttel ellenőrizve):

```
{"vers":"Mk 2:10","parok":[[1,[1]],[2,[2]],[3,[3]],[4,[4]],[6,[10]],[7,[8]],[8,[6]],[9,[5]],[10,[14]],[11,[13,15]],[13,[12]],[14,[11]],[15,[16]],[17,[18]]],"betoldas":[5,12,16],"forditatlan":[7,9,17]}
{"vers":"Mk 2:23","parok":[[1,[1]],[2,[2]],[4,[4,6]],[6,[10]],[7,[8]],[8,[7]],[10,[7]],[11,[11]],[13,[14]],[14,[13,14]],[15,[16,17]],[17,[20]],[18,[15]],[20,[18]]],"betoldas":[3,5,9,12,16,19],"forditatlan":[3,5,9,12,19]}
{"vers":"Jak 3:4","parok":[[1,[1]],[3,[4]],[4,[2]],[5,[6]],[6,[5]],[7,[5]],[8,[7]],[9,[10]],[10,[8,9]],[11,[11]],[13,[14]],[14,[14]],[15,[13,15]],[16,[16]],[17,[12]],[18,[16]],[19,[16,17]],[21,[20,21]],[22,[19]],[23,[22]]],"betoldas":[2,12,20],"forditatlan":[3,18]}
{"vers":"Jak 3:8","parok":[[1,[2]],[3,[3]],[5,[7]],[6,[7]],[7,[4]],[8,[4]],[9,[5,6]],[10,[5]],[11,[8]],[12,[9]],[14,[12]],[15,[11]],[16,[10]]],"betoldas":[2,4,13],"forditatlan":[1]}
{"vers":"1Pét 5:12","parok":[[1,[2]],[2,[1]],[3,[4]],[4,[4]],[5,[7]],[6,[7]],[7,[8]],[8,[5]],[9,[6]],[10,[9,10]],[11,[11]],[12,[12]],[13,[13]],[14,[14]],[15,[14]],[16,[16]],[17,[15]],[19,[20]],[20,[17]],[21,[18]],[22,[22]],[23,[21,22]],[24,[23]]],"betoldas":[18],"forditatlan":[3,19]}
```

(Jak 3:4 22, Jak 3:8 8 és 1Pét 5:12 23 esetén az alternatíva a TR eltérő alakját a meglévő
sorra köti. A Strong-szám Jak 3:4-ben (G1014) és 1Pét 5:12-ben (G2476) azonos, **Jak 3:8-ban
nem**: a TR-alak ἀκατάσχετον G0183, a sor ἀκατάστατον G0182 — ott az alternatív link rossz
Strongot adna.)

## 5. Károli értelmező vagy eltérő olvasatai (a párosítás megtartva)

- 2Móz 21:6 *bírák* ← הָאֱלֹהִים (H0430): Károli értelmező fordítása, párosítva.
- Jób 33:13 *beszédedre* (2. sz.) ← דְּבָרָיו „az ő szavai”; Jób 34:28 *hozzájok* (tsz.) ←
  עָלָיו „hozzá”; Ez 16:57 *körülötted* (2. sz.) ← סְבִיבוֹתֶיהָ „körülötte”: a személyrag
  eltér, a párosítás a raggal együtt megtartva.
- Ez 22:25 *Pártosok* ← קֶשֶׁר „összeesküvés”; Ez 30:5 *libiaiak* ← פוּט, *Kúb* ← כּוּב
  (a tükörfordítás „Libya”).
- Ez 39:13 *Úr* ← אֲדֹנָי, *Isten* ← יְהוִה (H3069).
- 1Pét 4:11: Károli a második *ὁ θεὸς*-t (21–22) nem fordítja → `forditatlan`; a *szólja*,
  *szolgáljon* kiegészítés → `betoldas`.

## 6. Bizonytalan egyedi döntések (versenként)

| Vers | Döntés | Alternatíva |
|---|---|---|
| 2Móz 20:25 | *a mint* (13–14) `betoldas`; *faragó vasadat* mindkettő → 14 | *a mint* → 13 (כִּי) |
| 2Móz 21:26 | *úgy* (10) `betoldas`; a kezdő *ve-* (1) `forditatlan` | *Ha* → 1, 2 |
| 2Móz 25:8 | *ő* (7) `betoldas` (a *hogy ő közöttök lakozzam* névmása nem illik az 1. sz. igéhez) | — |
| 2Móz 25:40 | *arra* → 7 (-ām „azok”) | *arra* `betoldas` |
| 2Móz 26:13 | *Egy* (1, 6) → אַמָּה; *is* (23, 25) `betoldas` | *Egy* `betoldas` |
| 2Móz 30:3 | *is* (17) → *ve-* (19) | *is* `betoldas`, 19 `forditatlan` |
| Péld 28:17 | *be-* (3) `forditatlan`; *senki* → 9, 10 | *vér* → 3, 4 |
| Péld 30:17 | *iránt való* (10–11) `betoldas` | → 7 (*li-*) |
| Péld 31:5 | *mikor* (2) `betoldas`, *ve-* (3) `forditatlan`; mindkét *ne* → פֶּן | *mikor* → 3 |
| Péld 31:8 | *a mellett* (6 `betoldas`, 7 → 4); *és* (11) `betoldas`; *azoknak* → 8, 9; *adattak* → 9 | *adattak* `betoldas` |
| Zsolt 18:1 | *azon* (14) `betoldas` | → 18 |
| Zsolt 22:32 | *utánok való* → נוֹלָד (8); *ő* (8) `betoldas` | *utánok való* `betoldas` |
| Zsolt 59:8 | *úgy mond* (8–9) `betoldas` | — |
| Ez 11:3 | a névelő-vonatkozó הָ (1) `forditatlan`, *Mondván* → 2; *város* (9) `betoldas`, *ez* → הִיא | *Mondván* → 1, 2; *város* → 8 |
| Ez 16:57 | *te* (7), *vagy* (10) `betoldas`; *most* → עֵת | — |
| Ez 33:31 | *azokat* (29) → a 22. ragra; הֵמָּה (30) `forditatlan`; *szokott* (9), *mint* (15) `betoldas`; a *nyereség* ragja (34) `forditatlan` | *azokat* → 30 |
| Ez 39:13 | *ezt mondja* mindkettő → נְאֻם | *ezt* `betoldas` |
| Ez 46:12 | *szokta tenni* mindkettő → יַעֲשֶׂה (34) | *szokta* `betoldas` |
| Mt 21:4 | *a ki így* (10–12) `betoldas`, *szólott* → λέγοντος | — |
| Mt 5:34 | *az* (13, „az [ti. az ég]”) → ἐστὶν | `betoldas` |
| Jak 1:18 | *ő akarata* (2–3) → βουληθεὶς | *ő* `betoldas` |
| 1Pét 5:12 | ὑμῖν (3) `forditatlan`; *hogy* → εἶναι | *hogy* `betoldas` |
| Mk 2:23 | αὐτὸν (3) `forditatlan` | *megy* → 3 |

## 7. F21.6 — a „TR-ben más helyen” tokenek átvezetése (régi → új)

A felhasználó döntése: a `tokenek.py` javítása („TR»N” / „TR«N” TR-es), a TR-helyes arany
átvétele a „más helyen” tokenekre, az „eltérő alak” tokenek kizárása a mérésből
(`f21p/meres_kizaras.tsv`). Csak az alábbi négy vers sora változott az
`f21p/arany_opus.jsonl`-ben; a másik 56 bájtra azonos. A Jak 3:4 és a Jak 3:8 „eltérő alak”
tokenje (#22, ill. #8) változatlanul `forditatlan`, a hozzá tartozó magyar szó (*akarja*,
ill. *fékezhetetlen*) változatlanul `betoldas`, ezért ezekben a versekben a 4. pont
alternatívájának csak a „más helyen” része került át. Az 1Pét 5:12 nem változott (csak
„eltérő alak” tokenje van).

| Vers | Érintett eredeti token | Régi | Új |
|---|---|---|---|
| Mk 2:10 | #12 ἁμαρτίας | 13 *bűnöket* `betoldas`; 12 `forditatlan` | 13 *bűnöket* → [12] |
| Mk 2:23 | #7 παραπορεύεσθαι | 8 *megy*, 10 *által* `betoldas`; 7 `forditatlan` | 8 *megy* → [7], 10 *által* → [7] |
| Mk 2:23 | #15 ἤρξαντο | 18 *kezdék* `betoldas`; 15 `forditatlan` | 18 *kezdék* → [15] |
| Jak 3:4 | #9 ἀνέμων | 10 *szelektől* → [8]; 9 `forditatlan` | 10 *szelektől* → [8, 9] |
| Jak 3:8 | #5 δαμάσαι | 9 *szelidítheti* → [6]; 10 *meg* `betoldas`; 5 `forditatlan` | 9 *szelidítheti* → [5, 6]; 10 *meg* → [5] |

A mérésből kizárt tokenek (`f21p/meres_kizaras.tsv`): Jak 3:4 #22, Jak 3:8 #8, 1Pét 5:12
#23. A 60 versű aranyban más „eltérő alak” token nincs. A 200 verses minta további 12
„eltérő alak” tokenje (Mk 13:21, Mk 14:44, Luk 1:75, Luk 9:27, Ján 10:12, Zsid 8:5, Zsid 9:6)
az aranyon kívül esik; a kizárásba nem vettem fel őket.

## 8. v2 — a DT21 a–e döntések (2026.09.30)

*Forrás: a felhasználó DT21 a–e döntése (`DONTESEK.md` DT21, pilot-brief PD13). A
döntések szövege a felhasználóé; az alábbi konvencióvá fogalmazás, a határesetek és az
arany v2-re gyakorolt hatás kézi ítélet (Opus), nem mérés. A konvenció-számozás a 2.
szakaszé; a K11 új.*

### 8.1 A konvenciók v2-es megfogalmazása

**K7 v2 — Segédige (DT21 a: a jegyzet az irányadó, a prompt kivétele szűkül).** A 2.
szakasz 7. pontja változatlan: a segédige (*vala, fog, fogunk, van, vannak, volna,
lészen*), ha az eredetiben nincs külön ige (nincs הָיָה, εἰμί stb.), `betoldas`. A kivétel
kizárólag a 7. pontban megnevezett eset: az egyetlen eredeti igealakot visszaadó
többtagú magyar igei szerkezet, amelyben a segédige maga az igealak (idő, szenvedő alak)
fordítása (Mt 4:4 *Meg van írva* ← γέγραπται: mindhárom token az egy eredeti igére).
Nem kivétel, tehát `betoldas`:
- az ige mellé tett múlt idejű *vala* (*tudja vala*, *megy vala*, *kezdék vala*), a jövő
  idejű *fog/fogunk*, a feltételes *volna*;
- a szerkezet nem igei szava: a kivétel nem terjed ki határozószóra (*jól tudja vala*),
  kötőszóra (*lőn, hogy*) vagy más Károli-betoldásra.

Ha az eredetiben van külön ige, és Károli azt segédigével vagy létigével adja vissza
(*ítéletünk lészen* ← λημψόμεθα, *van hatalma* ← ἔχει), a szó az igéhez kötődik: ez nem
segédige-betoldás, a K7 nem érinti.

**K3 v2 — Tárgyjelölő névmási raggal (DT21 b: a névmás csak *'et* + rag esetén megy az
eredetire, máshol `betoldas`).** A 2. szakasz 3. pontja változatlan (*'et* `forditatlan`,
a magyar névmás csak a ragra). Pontosítás: a C szabály kizárólag az *'et* + névmási rag
esetére szól; a magyar tárgyi névmás (*azt, ezt, őt, őket, téged, engem, azokat* stb.),
ha az eredetiben nincs *'et* + rag, és más eredeti névmási elem sincs, **`betoldas`**: nem
kötődik az igéhez (*azt mondom* ← λέγω: *azt* `betoldas`), és nem kötődik az ige
körüli más szóhoz sem (*ezt mondja* ← נְאֻם: *ezt* `betoldas`, *mondja* → נְאֻם).
Változatlanul kötődik: az önálló eredeti névmáshoz (αὐτόν, ἡμᾶς), és — a K4 szerint — az
igén vagy elöljárón álló névmási raghoz (H9030–H9040; *vigye őt* ← -ô, *támogassa őt*
← בּוֹ). Ez utóbbi olvasat a 8.3 pont 1. kérdése (a döntés szó szerinti szövege szűkebb is
lehet).

**K4 v2 — Birtokos és névmási ragok (DT21 e: a rag arra a magyar szóra megy, amelyik a
megfelelő személyragot viseli).** A 2. szakasz 4. pontja pontosítva: a rag (H9020–H9040)
arra a magyar szóra megy, amelyiknek a személyragja **ugyanarra a személyre utal**, mint az
eredeti rag. Birtokláncban (két személyragos magyar szó egymás mellett) nem a közelebbi
vagy a tárgyragos szó kapja, hanem a megfelelő: *szolgálójának szemét* ← עֵין אֲמָתוֹ „az ő
[a férfi] szolgálójának szeme”: a -ô a *szolgálójának*-ra (az ő szolgálója), nem a
*szemét*-re (annak -é- személyragja a szolgálóra utal, nem a férfira). A külön kitett
névmás (*az ő ura*) a 2. szakasz 4. pontja szerint továbbra is kapja a ragot. A személy
vagy szám Károli értelmező fordításában eltérhet (5. szakasz: *beszédedre*, *hozzájok*,
*körülötted*): ilyenkor a raggal ugyanazt a birtokost jelölő magyar szó a megfelelő.

**K11 (új) — Korrelatív mutató névmás a *hogy* előtt (DT21 c: „azt/azért … hogy”).** Az
*azt … hogy*, *azért … hogy* szerkezetben a mutató névmás (*azt, azért*) `betoldas`, ha
nincs külön eredetije; a *hogy* a kötőszóra (כִּי, ἵνα, ὅτι, *ve-* stb.) megy. Ha a mutató
névmásnak van eredetije (eredeti mutató névmás, pl. τοῦτο), arra kötődik (a K11 csak a
megfelelő nélküli korrelátumra szól). Egységesen: a v1-ben a *tudván azt, hogy* (*azt*
`betoldas`) és a *Mindez pedig azért lett, hogy* (*azért* → ἵνα) eltérően kezelt volt.

**2Móz 26:13 *is* (DT21 d: marad).** A 6. táblázat 2Móz 26:13 sora (*is* (23, 25)
`betoldas`) és az arany v2 minimális javítása (a וּ (26) `forditatlan`, l.
`naplok/F21P_arany_v2_diff.md`) változatlan; a K9 v2-ben nem módosul, az arany ezen a
ponton nem változik.

### 8.2 A v1-hez viszonyított változások

| Pont | v1 (2. szakasz) | v2 (8.1) | DT21 |
|---|---|---|---|
| K3 | *'et* + rag: a névmás csak a ragra | + a névmás *'et* + rag (és más eredeti névmási elem) nélkül `betoldas`, nem az igéhez | b |
| K4 | a birtokos személyragot viselő magyar szóhoz | a raggal azonos személyre utaló személyragot viselő szóhoz (birtokláncban a megfelelő szó) | e |
| K7 | segédige `betoldas`, kivétel Mt 4:4 | változatlan; a kivétel kifejezetten szűk (nem: *vala*, *fog*, *volna*, határozószó, kötőszó) | a |
| K11 | — | új: korrelatív *azt/azért … hogy*: a mutató névmás `betoldas`, a *hogy* a kötőszóra | c |
| 6. táblázat | 23 sor | változatlan, nem bővül (a 2Móz 26:13 *is* sora marad) | d, PD10 |

A többi konvenció (K1, K2, K5, K6, K8, K9, K10) és az 1., 3.–7. szakasz változatlan.

**Hatás az aranyra (javaslat, jóváhagyásig nem fagy be).** Az arany v2
(`f21p/arany_opus_v2.jsonl`, befagyasztva) három versében ütközik egy-egy link a v2
konvenciókkal: Jób 33:13 *Azért* (K11), Mt 21:4 *azért* (K11), Ez 39:13 *ezt* (K3 v2).
A javasolt arany v3: `f21p/arany_opus_v3_javaslat.jsonl`, a versenkénti diff:
`naplok/F21P_arany_v3_diff.md`. A K4 v2 és a K7 v2 az arany v2 egyik linkjét sem
érinti. Az Ez 39:13 *ezt mondja* sora a 6. táblázatban változatlanul áll (a v1/v2
döntését dokumentálja); a v3-javaslat a táblázat ott megnevezett alternatíváját (*ezt*
`betoldas`) veszi át, mert a K3 v2 ezt írja elő.

### 8.3 Nyitott kérdések (felhasználói döntésre, `javaslat` jelöléssel)

1. **A DT21 b hatóköre.** A döntés szövege: „a névmás csak ott megy az igére, ahol *'et* +
   rag áll”. Két olvasat: (a) a döntés a megfelelő nélküli (betoldott) tárgyi névmásra
   szól, az igén álló névmási rag (H9030–H9040) külön kitett magyar névmása a K4 szerint a
   raghoz kötődik (a 8.1 K3 v2 így fogalmaz, az arany v2 így párosít); (b) szó szerint:
   *'et* + rag nélkül minden tárgyi névmás `betoldas`, az igei rag `forditatlan`. A (b)
   az arany v2-ben hét magyar szó linkjét változtatná (2Móz 20:25 *azt* (19), 2Móz 21:6
   *őt* (3, 29), 2Móz 21:26 *azt* (16), 2Móz 26:13 *azt* (28), Zsolt 6:5 *engem* (9),
   Zsolt 16:11 *engem* (3); az elöljárós Péld 28:17 *őt* ← בּוֹ esettel nyolcét), és a DT20 a) (tárgyrag az igén) kérdését is érintené. Javaslat: (a).
2. **DT20 c) — igei személyrag (Ez 39:13 *megdicsőítem*).** A K4 v2 a személyrag
   „megfelelő” voltát a birtokosra/személyre köti; hogy az igei személyrag (a
   *megdicsőítem* -em ragja) is megfelelő lehet-e a H9040 (*magamat*) mellett, a DT21 e
   nem mondja ki. Az arany v2 (csak *magamat*) marad. Javaslat: marad, nyitott.
3. **2Móz 25:40 *arra* → -ām (6. táblázat).** A K4 v2 szerint egyik magyar szó sem visel a
   -ām-nak megfelelő személyragot (*arra a formára*); a 6. táblázat sora az *arra*-t a
   raghoz köti, alternatívája `betoldas`. A DT21 e birtokláncra szól, ezt az esetet nem
   nevezi meg; az arany nem változik. Javaslat: marad (a 6. táblázat szerint).
4. **DT20 a) és b)** (tárgyrag az igén külön névmás nélkül; a *való*): a DT21 a–e nem
   érinti, nyitott marad.
