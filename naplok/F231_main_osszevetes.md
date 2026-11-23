# F231.17 — a #810 és a main összevetése: mi tűnt el vagy került lenyíló mögé, és mi lett vele

2026-11-23 · `claude-opus-5-5` · ág: `claude/olvaso-egyben-3464e1` · a main állapota: `7371ebb8` (`origin/main`, külön worktree-ben)

**A szabály** (a szerkesztő, 2026-11-23): amit a main a lapon mutatott, az maradjon látható; „Igen, hozza vissza”. A hibalista
kifogását javítjuk, nem a blokkot vesszük el. Ahol egy eltűnés szerintem indokolt, nem döntöttem: „döntésre vár” jellel áll lent.

## Hogyan mértem

1. **Blokkfej-összevetés** (a kapu, `eszkozok/olvaso_szerver/teszt_blokkfej.py`): rögzített 20 oldal (verssor és a fülei,
   szónézetek, köztük a H4325, a H8415, a G3056 a Jn 1:1-ben és a G0264 a Róm 3:23-ban, valamint a F232 pillanatképeinek szó-lapjai),
   alap- és kutatói szinten. Elemenként: blokk, jelleg-címke a címsorban, rövid forrásmegjegyzés, forrássor, „Nincs adat” sor,
   címsor és lenyíló-felirat, táblázatfej — láthatósággal (látható / csukott / rejtett). A main állapota a
   `merce/blokkfej_alap.tsv`-ben (generált, a main worktree-jéből: `teszt_blokkfej.py --alap-ment <worktree>`).
2. **Soronkénti szövegösszevetés** ugyanezen a 20 oldalon (egyszeri, nem kapu): a main látható sorai közül melyiknek nincs meg a
   szövege (betűre) az ág látható szövegében. Ez fogta meg a csukott táblázatokat és a súgóba vitt angol szavakat.
3. **Bekötési leltár** (`bekotesi_leltar.py`, `c368ff19`, a repón kívül futtatva, a main és az ág állapotán): a „látszik” oszlop
   **nem tér el** (adatkészlet 46, tábla 54, blokk 56 mindkettőn). A leltár a csukott állapotot nem méri (a saját leírása szerint),
   ezért az alábbi eltűnéseket nem láthatta. Eltérés csak a bekötésben: a `szo.usz` az UBS-táblákat is olvassa, a `szo.bdb_angol`
   a BDB-szakasztáblákat már nem; a blokkcímeket az ágon `None`-nak olvassa (a cím a fordítótáblából jön, a leltár ezt még nem követi).

A javítás előtt a kapu 570 eltérést talált (jelleg-címke 265, forrássor 198, megjegyzés 47, fej 36, blokk 24). Utána: 0 hiba,
50 eltérés a kivétellistán (a `merce/blokkfej_kivetel.tsv` 15 sora; ebből 28 „döntésre vár”). Az integrátor döntései után (F231.21):
0 hiba, 28 eltérés a kivétellistán (10 sor, mindegyik indokkal: „átalakítva”, egy „eldöntve”).

## Visszaállítva (a main szerinti láthatóság)

| # | Mi | Hol | Melyik commit / tétel vitte el | Most |
|---|---|---|---|---|
| 1 | „Apparátus és szövegkritika” lenyíló a jelentéseknél | szónézet, pl. /1Moz/1/7?szo=H4325&ful=szo (10), /1Moz/1/2?szo=H8415&ful=szo (2) | `b537aea8`, #10 | vissza, csukva, ahogy a main-en; a darabszám felirattal („2 tétel”, a #10 kifogása); a forrásjel a helyével („2Móz 10:13 (J) · 3Móz 6:2 (P)”, a #15 kifogása); a darabszám mind a 6 BDB-lapon egyezik a main-nel |
| 2 | Jelleg-címkék („forrásadat”, „gépi feldolgozás”, „modell-kimenet”) és a rövid forrásmegjegyzés („üres eredmény nem negatív lelet”, „a Strong-címkék GPL-eredetűek …”) a blokkcím mellett | minden blokk | `e0c23f15`, #45, #49 | vissza a címsorba, súgóval |
| 3 | Forrás- és licencsor | minden blokk alján | `e0c23f15`, #46 | nyitva, ahogy a main-en; olvasói névvel (a #46 kifogása), a belső nevű teljes sor a súgóban |
| 4 | Az üres eredményű blokkok (címmel, címkével, forrássorral, „Nincs adat” sorral) | pl. /Jan/1/1: 11 blokk; a 20 lapon 24 | `e0c23f15`, #47 | vissza a helyükre; az összesítő sor megszűnt |
| 5 | A versnézet táblázatai (Károli–Strong, TAHOT/TAGNT, Macula ×2, LXX-szavak, igealak) | /1Moz/1/1, /1Moz/1/7, /Zsolt/22/2, /Jan/1/1 | #36 | a „Táblázatos nézet” lenyíló alapból nyitva (becsukható) |
| 6 | A görög szó-lap forrásszövegei (TBESG, Thayer angol, LSJ, SECE) | /szo/G0264, /szo/G3056 | #21 | a lenyíló alapból nyitva; a #21 új blokksorrendje marad |
| 7 | Az angol eredeti a magyar mellett („reggel morning”, „víz water”, a tW-címszavak angolja) | Strong-szótár, TBESH, „Ebben a versben”, SDBH, SDGNT, tW, UBS | #58 | vissza a magyar mellé, kisebben (a súgó helyett) |
| 8 | A versszámozás-tábla („Osztály · KJV · MT · A megfeleltetés forrása”) és az LXX-versszám táblája („Forrás · LXX-versszám”) | minden verslap | #37 | DT-F231d (F231.21): az egysoros összefoglaló alatt a main táblázata; a megfeleltetés forrása olvasói néven („versszámlálás”, „Septuaginta-etalon (LXX_OS)”), a belső kód a súgóban |
| 9 | Az SDBH/SDGNT doménkód és az UBS DBH/DNTG azonosító | szónézetek | #27 | DT-F231e (F231.21): a „Domén kód” és az „Azonosító” oszlop vissza; a tagolt UBS DNTG-listában jelentésenként „azonosító: …” |

## Átalakítva (a tartalom más alakban látszik; a kapu kivétellistáján „átalakítva”)

- „még N hely” gomb (5 lap): a szótár szövege jelentésenként egyben áll, minden hely látszik (#1–#3).
- A H8415 jelentésének felirata: „a BDB itt idézi ezt a verset” helyett „a BDB besorolása ennél a versnél” (DT914, #16); ugyanígy a „kétes pontjai „vonatkozhat” jelölést kapnak” mondat (a jelölés megszűnt).
- „Előfordulások (az első N)” felirat (UBS DNTG): mondat lett („Az első N vers áll az M közül.”, #28).
- A G3056 Thayer-kártyája: a „(fordításra vár)” helyőrzők helyén az angol eredeti (#22); a csukott „Szótári apparátus: a teljes magyar Thayer-szöveg” lenyíló tartalma a nyitott, tagolt szövegben áll (53 sorából csak a helyőrzők és a belső nevű forrássor nincs meg; #21); a „a szócikk eleje —” címke nem áll a szöveg előtt.
- A Károli–Strong táblázat „Bizonyosság” oszlopa helyén a mért pontosság (#38); a magyar szó szerinti összevonás (#30).
- Átfogalmazott feliratok és mondatok: „PaRDeS olvasó” → „Biblialex olvasó” (#51), a szintnevek ékezettel (#52), a szó-lap alcíme (#50), „A 66 feldolgozott könyv (…)” → „Mind a 66 könyv …” (#57), a TSK darabszám-mondata (#43), a BDB-szöveg olvasói alakja („szemben X-val” → „ellentétben: X”, „&” → „és”; #2, #3, #5).

## Döntésre várt — az integrátor döntött (2026-11-23)

Az első két pont visszaállítva (8–9. sor fent), a harmadik nem jön vissza. A döntések: `dontesek/uj/olvaso-egyben-3464e1.md`.

1. **Versszámozás (#37) — DT-F231d: vissza.** a „Versszámozás (MT / KJV)” és az „LXX-versszám” táblázata helyén egysoros összefoglaló áll. A versszámok látszanak; az „Osztály” és „A megfeleltetés forrása” oszlop (pl. „szamlalas”) és az LXX „Forrás” oszlopa (LXX_OS, ez a forrássorban megvan) nem. Indok, hogy nem állítottam vissza: a #37 a pilot egysoros alakját kérte, és a két oszlop belső módszerkód.
2. **Doménkódok és UBS-azonosítók (#27) — DT-F231e: vissza.** az SDBH/SDGNT „Domén kód”, az UBS DBH és DNTG „Azonosító” oszlopa a súgóba került. Indok: a #27 a nyers 15 jegyű azonosítót kifogásolta; a domén, a glossza, a definíció és a hivatkozás látszik.
3. **A G0264 Thayer-blokkjának „modell-kimenet” címkéje — DT-F231f: nem jön vissza.** a G0264-nek nincs magyar Thayer-fordítása, a blokk az angol eredetit mutatja; a main a címkét fordítás nélkül is kiírta. Indok: a visszaállítása hamis jelölés lenne.

## Az integrátori összevetés új hibája (javítva, F231.21)

A H8415 2. jelentéscsoportjának címe (/1Moz/1/2?szo=H8415&ful=szo) a main „—” jele helyett csonka töredék volt: „mély) tenger, amely
elborítja Tírust (párhuzamban”. Ok: a #810 új pótcím-szabálya (`szokartya_szoveg.elso_tagmondat`, a meghatározás nélküli pont címe a
szöveg első tagmondatából) mindkét végről levágta a zárójelet, a tagmondat-határ pedig a „(párhuzamban:” közepén vágott. Javítás: a
zárójel ép marad, a félbevágott zárójeles rész kimarad; a cím most „(mély) tenger, amely elborítja Tírust” (a teljes, ép tagmondat).

## A kapu

`teszt_blokkfej.py` (a `teszt_futtat.py` gyors készletében): bukik, ha a main látható vagy csukott eleme az ágon hiányzik vagy
rosszabb láthatósággal áll, kivéve, ha a `merce/blokkfej_kivetel.tsv` indokkal megnevezi (állapot: „átalakítva” / „döntésre vár” /
„eldöntve” / „a main-en sem látszott”). Az elavult kivétel is bukás. A blokkot, a forrássort és a jelleg-címkét azonosító szerint, a többit
szöveg szerint veti össze; a szöveg más címsorszinten vagy tagolásban is elfogadott, ha a betűi ugyanolyan láthatósággal állnak.
Az alapfájlt a main változásakor a main worktree-jéből kell újraírni (`--alap-ment`).
