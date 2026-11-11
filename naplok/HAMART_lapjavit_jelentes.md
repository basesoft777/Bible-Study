# /lap-javit HAMART-001 — jelentés és változáslista

*2026-11-11 · végrehajtó: claude-opus-5-5 (a kért modell: opus) · ág: `claude/lap-javit-hamart` · bemenet: a lektor listája (`naplok/KIADAS_HAMART-001_lektor.md`, a #696 ágán; 46 tétel: 43 lektori, 3 orkesztrátori), az orkesztrátori névelő-tétel, a lapnézet kommentjei (https://claude.ai/artifact/39x5VLDvyq9z2AJ9zjww3K: komment nem volt). A döntések: a felhasználó (az orkesztrátor továbbításában, 2026-11-11): „mehet a javaslatokkal”, a határkérdésekre „a/a”; a 18. tételben orkesztrátori döntés. A próza egy kézben (K1): a teljes kézi forrás (`motivumok/HAMART-001.md`) elolvasva, a javítás tételenként, az értelmező szakaszok nem íródtak újra egészben.*

## Összegzés

- A határ nem változott: a 47 hely, 54 vers és a kizárt helyek ugyanazok. A 6. (A) és a 11. (A) döntés a Kivonat indoklását és a meghatározás szövegét pontosította.
- Próza (a kézi forrás): 23 hely. Adat: 9 hely — az előfordulás-tábla 6 kapcsolódás-szövege és 1 funkciója a jelöltek beépített során át, a `motivumok.tsv` negatív kritériuma, a kapcsolat-tábla 56 indoklás-szövege. Generátor és kapu: 16 hely. Napló: `adat/lap_javitasok.tsv`, 48 sor.
- Két tétel gyökérokkal, gépi védelemmel (második előfordulás):
  - **15.** A Károli-kereszthivatkozás részlista-másolata. A szabály a teljes táblán +27 forrásverset szűr. A KH_MASOLT kapu eddig az új szerkezetű lapon nem futott (a „4.” szakaszszámot kereste), most az új szerkezetű lapon BUKÁS.
  - **Névelő.** A forrásnév a generátor táblájában névelő nélkül áll, a generált lista- és táblaelemről a generátor elhagyja a névelőt, a LISTA_NEVELO kapu BUKÁS. Javítás előtt a kapu 464 elemet talált a lapon, utána 0-t.
- Kapuk:
  - olvasói kapu: 0 BUKÁS, 14 figyelmeztetés (előtte 15);
  - `ellenoriz.py`: 0 SÉRTÉS;
  - nyílt mag kapu: 0 BUKÁS. A hat változott magyar szöveg angol párja a F170 útján újra fordítva: claude-sonnet-5-5, a végrehajtó átnézésével; egy hozzátoldott magyar zárójel kivéve.
- Tesztek: `teszt_kesz_lap_hamart` 42 OK (3 új, rontott bemenettel), `teszt_olvasoi_kovetkeztetes` 13 OK, `teszt_karoli_kh_gyanus` 3 OK, `teszt_nyilt_mag` (a futás a commit előtt).

## A 12 nyitott tétel — mit döntöttem, és miért

A lektor 2. köre 12 tételnél nem adott szöveget, csak a javítás feltételét; a mondatot a próza gazdája írja. A 6. és a 11. tétel határkérdés: a felhasználó döntött. A 18. tételben az orkesztrátor döntött.

| Tétel | A döntés | Miért |
|---|---|---|
| 1. A lap eleje, „A motívum.” | A címismétlés helyett az azonosság hordozója áll: „Szerkezeti motívum: azonosságát nem egyetlen szó adja, hanem egy szerkezet, amelyet több szó együtt hordoz.” A szöveg az adatból jön (`azonossag_tipusa`), öt típusra egy-egy mondat. | A cím a címsorban már áll. Az azonosság hordozója az új ID első kérdése (CLAUDE.md), ezt a cím nem mondja. A bekezdés-forma (DT781) marad. |
| 2. A lap eleje, a második címke | A címke „Mi tartozik ide, és mi nem.” lett. A lánc első említése önmagában érthető: „az 1Mózes 3–9. fejezetének szóláncából (átok, föld, fáradság, bűn, erőszak, romlás)”. A lap eleje és a Kivonat ugyanazt a szabályt mondja: a kizárás oka a szövetség rendje, és az erőszak a hallás igéjével ugyanabban a versben. | A negatív kritérium a hely minimális jegye, ezért a pozitív feltételt is tartalmazza. A „Negatív elhatárolás” címke ezt nem fedte. |
| 4. „Fölérendelt fogalom”, zárójel | „(a tágabb kategória: ha egy hely csak ezen át tartozna ide, kimarad)” | A zárójel második fele a „hígulna” szó nélkül is érthető, ezért a belső szó kimaradt; a mondat a zárójelben marad. |
| 6. 1Kir 13:34, 2Kir 17:23 (határ, A) | A két hely kizárva marad. A Kivonat mondata: „a szövetség rendjében, a szövetség megszegésének büntetéseként mondja ki, és nem a Genezis láncára utal vissza … Az utóbbi kettőben a föld szava (adámá) áll; a kizárás oka nem a szó hiánya …”. A helyek a saját tartalmuk szerint vannak megnevezve: Jeroboám háza, Izrael fogsága „az ő földéből”. | A „föld szava nélkül” állítás hamis volt (TAHOT: adámá mindkettőben). A felhasználó döntése: (A), a határ nem változik. |
| 9. Jer 6:7 | A vers két állítása külön áll: a városban hallatszik az erőszak, Isten előtt „betegség és vereség” van. Az „ítélet ennek a hangnak felel” mondat kimaradt. | A versben nincs ítélet-szó. Az összevont mondat a versnél többet mondott. |
| 11. Hab 1:2 (határ, A) | A hely bent marad. A meghatározás: „az erőszak szava a hallás igéjével ugyanabban a versben (hallatszik az erőszak, vagy az erőszak miatt kiáltó szó nem talál meghallgatásra)”. A Hab 1:2 szövege kimondja, hogy a „nem hallgatsz meg” alanya Isten, és az erőszak a kiáltás oka. A Jer 6:7-tel azonos záró mondat megszűnt. | A felhasználó döntése (A): a szöveg pontosul, a határ nem változik. A kitágított meghatározás a ma bent álló helyeket fedi. A kizárt Hab 2:8 és 2:17 kint marad, mert ott a hallás igéje nem áll. |
| 15. Sof 1:9, Károli-KH | Generátor és kapu: részlista-szabály (DT-F125i). A lapon a Sof 1:9 KH-listája kimaradt, a bevezető megnevezi a gazdáját (a Mt 12:22 listája). A számok újraszámolva: 26 hely, 112 utalás, 55%. | A lista a Mt 12:22 listájának része, ezért a csak teljes egyezést kereső szabály nem fogta meg. A Sof 1:2-3 sora több versre terjed, ezért a lapon nincs KH-listája; a lektor nyitott kérdése így tárgytalan. |
| 18. A kapcsolat PaRDeS-szintje | A szint a kapcsolat jellegét írja le (orkesztrátori döntés). A Kapcsolatok blokk jegyzete egy helyen kimondja az oszlop jelentését. A három tematikus sor indoklása: „A kapcsolat szintje (Remez) azt írja le, hogy a két hely egymásra mutat; a célhely saját szintje a 2. szakaszban áll.” | Így a szint sem az adatban, sem a lapon nem változik, csak az értelmezése lesz kimondott. |
| 19. Alátámasztás, a „lap prózája” | Az 56 indoklás új szövege: „A … bizonyosság ezen a mért egyezésen áll.” A hagyományos gyűjtemény (TSK, Károli) csak ott áll tanúként, ahol valóban összeköti a két helyet; ahol nem, a szöveg ezt kimondja. A lap prózája tanúként nem szerepel. | A lap nem hivatkozhat önmagára. A döntések (DT748) és a bizonyosság nem változtak, csak a szöveg (`naplok/F125_lapjavit_kapcsolat.py`). |
| 35. Drash, zárómondat | „a szöveg nem állítja, hogy minden szenvedés egy konkrét bűn következménye; a lap helyei azt mutatják, hogy a bűn következményei kiterjednek az elkövetőn túl.” | A „mindig” általános tétel volt, amelyet a lap a szövegnek tulajdonított. A mondat most a lap másik helyének mértéke szerint, a lap olvasataként áll. |
| 36. Sod, a „visszavonás” | „Az átok szavát tehát a lap helyein senki nem vonja vissza; mellette egy másik szó hangzik el: … Hogy az átok mint állapot megszűnt-e, azt a lap nem dönti el (l. a vitatott pontokat).” Az Ézs 60:18 funkciója: „a földön többé nem hallatszik erőszak: a lánc erőszak-szavának végidei megfordítása”. | A „visszavonás” így a lapon egy dolgot jelent (az átok igéjét), és a Sod-mondat az ige szintjén marad. A Vitatott pontok nyitva hagyott kérdését nem dönti el. |
| 45. A chattát rokon nyelvi sora (4.8) | „Nincs rokon nyelvi alak a BDB szócikkében; az igei tő, a חָטָא (chátá) szócikke ad rokon alakokat, ezek a táblában nem szerepelnek.” A tő sorainak felvétele külön tétel (N-F125f). | A cella a szóról szól, nem a munka állapotáról. A tő sorait két kézzel kell kinyerni, ez a lapjavításban nem fér el. |

## Tételenként — mi változott

| # | Hely | Típus | Változás |
|---|---|---|---|
| 1, 2, 4 | A lap eleje | generátor + adat | l. fent; `egyszerusitett_kolofon`, `AZONOSSAG_OLVASOI`, `motivumok.tsv` `negativ_kriterium` |
| 3 | A lap eleje, tematikus helyek | adat | „A lánc szavai nélkül csak az a néhány hely tartozik ide, amely ugyanezt a szerkezetet más szavakkal mondja ki; ezeket a lap egyenként, tematikus helyként veszi fel.” |
| 5 | Kivonat, Ez 7:23, 8:17 | próza | „Júda háza erőszakkal tölti meg a földet (Ez 8:17), és … a város tele van erőszakkal (Ez 7:23)” |
| 6 | Kivonat | próza | l. fent |
| 7 | Kivonat, Ez 12:19, Sof 1:2-3 | próza | kimondja, hogy a két hely a listán áll, és a szövetségi átokkal szemben a Genezis láncát hozza vissza |
| 8 | Kivonat | próza | „a lánc hat héber és három görög szavának, illetve szócsaládjának” |
| 9–14 | 2.1, Jer 6:7, Hab 1:2, Jer 51:46, Ez 28:16, Sof 1:9 (és az azonos mintájú Mik 6:12) | adat | a kapcsolódás-szöveg a vers szerint. Jer 51:46: a föld itt erec, a felvétel alapja az erőszak. Ez 28:16: Tírus királya (Ez 28:12), a Károli névalakja. Ez 28:16, Sof 1:9, Mik 6:12: a „maga utal vissza” helyett a föld szava nélküli kötés kimondva. |
| 15 | 6. Kereszthivatkozások | generátor + kapu | l. fent |
| 16 | 6. Kereszthivatkozások, jegyzet | generátor | olvasói jegyzet: a gyűjtemények neve, a 15 olvasói szavazat, a 6 több versre terjedő hely okkal, a kimaradt listák gazdájával |
| 17 | 7. Kapcsolatok, következtetés | generátor | „a motívum helyeit túlnyomórészt párhuzam köti össze: a későbbi hely ugyanazt a szót vagy szerkezetet hozza vissza …, és a kapcsolatok többsége közepes bizonyosságú” |
| 18–20, 32 | 7. Kapcsolatok, Alátámasztás | adat + generátor | l. fent. A visszatérő szavak nevükkel (pl. „szó szerint visszatér az uralkodás igéje (מָשַׁל, másal) és a vágyódás (תְּשׁוּקָה, tesúká)”). A sorvégi döntés- és forrásfarok egyszer, a blokk alatt áll. Ez 12:19: „az erőszak szava (חָמָס, chámász) és a teljesség főneve (מְלֹא, meló), a megtelés igéjének tövéből”. |
| 21 | Miért fontos, adámá | próza | „a lánc legtöbbször visszatérő szava: a lap genezisi helyei közül 12 versben áll …; az 1Móz 6:11-13 »földje« … az erec” (lekérdezés: TAHOT, 13 vers) |
| 22 | Miért fontos, Károli-szavak | próza | a felsorolás teljes: „erőszak” (Hab 1:2, Sof 1:9), „erőszaktétel” (Ézs 60:18) |
| 23–27, 44 | 9. Hatástörténet | generátor | bevezetők és jegyzetek olvasói nyelven, a munkamenet leírása nélkül; az egyverses szó (chattát) a számlálásból kimarad (Targum 3, Vulgata 2, LXX 4 az 5-ből); a tematikus Jel 22:3 kimaradása kimondva; „Előkép” helyett „Ugyanez a szó a Genezis-lánc Septuagintájában”; a tanú-bevezető teljes mondattal, az olvasat-állítás a megnevezett helyre szűkítve |
| 28 | Peshat, hordozó | próza | a 6:11-13 földje erec: „a hordozó jelentésében folytatódik, szavában nem” |
| 29 | Peshat és Drash, 6:12 | próza | a vers szövege szerint („minden test megrontotta vala az ő útát a földön”); az alany-sorban a 6:13 |
| 30 | Peshat, tükörítélet | próza | „a lap ebből azt olvassa ki …” (olvasatként) |
| 31 | Remez, 12:3 | próza | az „először” helyett: Isten áldás-ígéretének egy mondatában; Noé szavában (9:25-26) két külön kimondás |
| 32 | Remez, Ezékiel | próza | a három hely a saját tárgyával (föld, város, kiürülő föld) |
| 33 | Remez, Róm 8:20-21 | próza | „a lap nem dönti el; a vitatott pontok az 1Móz 8:21 hatókörénél érvként hivatkoznak rá” |
| 34 | Drash, 4:10-11 | próza | „Ábel vére a földről kiált, és Kain átkozott lesz »e földön, mely megnyitotta az ő száját«” |
| 37 | Vitatott pontok, forrásrétegek | próza | Carr állítása (az özönvíz-elbeszélés két forrása) külön, a szó–forrás megosztás olvasatként, „forrásonként nem vizsgálta” |
| 38, 39 | Módszertan, keresések | próza | a szókeresés köre (a két korábbi lánc-szóval együtt); „a szókeresés verseiből 577-ben …”, egységes megnevezés |
| 40 | Módszertan, TR | próza | „öt lexikai újszövetségi helyén”, a Jel 22:3 tematikus |
| 41 | Nyitott kérdések, 1. pont és a cím | próza | a „föld színéről” csak az 1Kir 13:34-ben és az Ámós 9:8-ban; a cím „Nyitott kérdések” (a „séma-korlátok” kimaradt) |
| 42 | Nyitott kérdések, 2. pont | próza | a két Jób-hely külön (16:18: erec, vér; 31:38: adámá, vér nélkül) |
| 43 | Nyitott kérdések, 3. pont | próza | „ugyanazzal a »vég« szóval (kéc); ez a szó azonban nem tartozik a lánc hat szava közé” |
| 45 | 4.8 | generátor | l. fent |
| 46 | 2. Előfordulások, Jel 22:3 | generátor | „(tematikus hely: a lánc szava nélkül áll a lapon, l. a Kivonatot)” |
| névelő | minden generált lista és tábla | generátor + kapu | DT-F125g |

A Kolofon új sora (DT599): „Emberi lektorálás | 32 hely (2026.11.11)” — a nem `generátor` típusú sorokból.

## Nyitott (külön tétel)

- N-F125f: a chattát tövének rokon nyelvi sorai.
- N-F125g: a részlista-szabály hatása a régi lapokra és a #177 MEK-összevetésre.
- N-F125h: az ISTENTISZT-001 négy ismétlődő kulcsa a `lap_javitasok.tsv`-ben.
