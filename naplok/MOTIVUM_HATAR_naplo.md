# MOTIVUM_HATAR_naplo.md — F151 (#151) M0: a gépi rész

*Modell: claude-sonnet-5-5 · 2026-11-01 · ág: `claude/f151-motivum-hatar-d33a81` · lépés: 4. szakasz 0. (M0), utána ⛔ DT443.*

*(proveniencia: scope=adat/elofordulasok.tsv (beépített igehelyek, verssé bontva) + adat/motivumok.tsv (`azonossag_tipusa`, `negativ_kriterium`) + adat/motivum_kapcsolatok.tsv | forras=eszkozok/motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | ts=a bemeneti fájlok utolsó commitjának ideje, a kimenetek fejlécében)*

Újrafuttatás: `python eszkozok/motivum_hatar.py [--motivum ID ...]` (alap: ISTENTISZT-001, HAMART-001; a szkript csak a `naplok/HATAR_<ID>.md`-t írja, az adatot nem érinti). Teszt: `python eszkozok/teszt_motivum_hatar.py` (12 teszt, OK). Két egymás utáni futás bájtra azonos kimenetet ad (ellenőrizve).

## 1. Módszer

1. **Részhalmaz** (CLAUDE.md „Új motívum-ID”, 4. kérdés). A motívum beépített igehely-halmaza az `elofordulasok.tsv` soraiból, **versekre bontva** (tartomány = minden vers, `lexikon_general.igehely_lista`; a gondolatjel `–` `-`-ra cserélve, mint a #150-ben). Minden más motívummal összevetve, **mindkét irányban**. Kérdés, ha A ⊆ B (`reszhalmaz`), ha a két halmaz azonos (`azonos`, egyszer jelentve), vagy ha |A ∩ B| / |A| ≥ 80% (`atfedes`; A az ellenőrzött oldal, a fordított irányt külön számolja a szkript). Az átfedés nevezője a *kisebbik* (vizsgált) oldal: a brief „átfedés ≥ 80%” szavát így értelmeztem; ha a felhasználó a Jaccard-hasonlóságot vagy a nagyobbik oldalt akarja nevezőnek, a küszöb átírható (`reszhalmaz_viszony`). Minden kérdés mellé: a közös versek soronként a két idézett `elofordulasok.tsv:sor` hivatkozással, és a `motivum_kapcsolatok.tsv` meglévő kapcsolatai a két motívum között. Az üres eredmény mellett is látszik az összevetés teljes táblája.
2. **Negatív kritérium a beépített sorokon.** Csak `azonossag_tipusa=formulaikus` hordozón. A #150 `jelolt_eloszures.vizsgal` próbáját **importálom, nem másolom**: a beépített sor versében (tartománynál az összes versében) a TAHOT+TAGNT Strong-halmazban megvan-e legalább egy teljes gerinc-kombináció (a motívum `elofordulasok.tsv` `strong` mezői, nyelvtani Strongok nélkül). Ha nincs, kérdés a sor és a `negativ_kriterium` idézésével. Nincs szövegadat → „nem ellenőrizhető”, nem kérdés és nem negatív lelet. Nem formulaikus hordozón a próba nem fut, és a kimenet ezt kimondja.
3. **Sorszámok** a fájl tényleges sorai (a `#` kommentsor is számít), nem az adatsor-index; a TSV olvasása `split('\t')`.
4. **Proveniencia.** A `ts` a bemeneti fájlok utolsó git-commitjának ideje (`2026-10-29T15:36Z`), nem a futásé: determinisztikus.
5. **A „Modelles rész”** a `HATAR_<ID>.md`-ben jelölők között áll (`<!-- MODELLES-KEZDET -->` … `<!-- MODELLES-VEGE -->`), tartalma: „nem futott (DT443 után)”. A szkript újrafuttatáskor a jelölők közötti tartalmat megőrzi.

## 2. Eredmény motívumonként

| motívum | hordozó | beépített sor / vers | részhalmaz | átfedés ≥ 80% | azonos | negatív kritérium |
|---|---|---|---|---|---|---|
| ISTENTISZT-001 | formulaikus | 33 / 33 | **0** | **0** | **0** | 33 sor ellenőrizve: megvan 33, **kérdés 0**, nem ellenőrizhető 0 |
| HAMART-001 | strukturális | 52 / 77 | **0** | **0** | **0** | **nem fut**: „a hordozó strukturális: a gépi negatív-kritérium próba nem fut” |

**Kérdések összesen: 0.** Az összevetés táblája szerint a két motívum igehely-halmaza a többi nyolcéval **egyetlen közös verset sem** tartalmaz (közös = 0 minden párban). Meglévő kapcsolat a `motivum_kapcsolatok.tsv`-ben: ISTENTISZT-001 ↔ ALVIL-001 két `szomszédos` sor (`adat/motivum_kapcsolatok.tsv:3` ApCsel 2:27 ↔ 2:21, `:4` ApCsel 2:31 ↔ 2:21), HAMART-001 ↔ ISTENTISZT-001 egy (`adat/motivum_kapcsolatok.tsv:5`, 1Móz 12:3 ↔ 12:8); ezek szomszédos, nem közös versek, tehát nem részhalmaz-kérdések.

**Kiegészítő futás (nem commitolt, a repón kívülre, `/tmp`):** mind a kilenc motívumra lefuttattam (`--kimenet` ideiglenes könyvtár). Eredmény: részhalmaz/átfedés/azonos kérdés **0** mind a kilencen; a negatív-kritérium próba csak a két formulaikus motívumon fut (ISTENTISZT-001: 33/33 megvan; TEREMT-002: 3/3 megvan), a hat lexikai és a strukturális motívumon nem. A gépi rész tehát a mai adaton **nem termel kérdést**.

**Orkesztrátori ellenőrzés (független számolás az `elofordulasok.tsv`-ből, `split('\t')`):** a 0 kérdés nem 0 közös verset jelent a két próbamotívumon kívül. Öt közös vers van, mind a 80%-os küszöb alatt: ALVIL-001 ↔ HODIT-001: Péld 9:18, Ézs 14:9 (2/33 = 6%); ALVIL-001 ↔ TEREMT-001: Ez 31:15; HODIT-001 ↔ MENNY-001: 4Móz 13:34 (1/11 = 9%); TEREMT-001 ↔ TEREMT-002: 1Móz 1:2 (1/3 = 33%, a legnagyobb arány). Egyiknek sincs sora a `motivum_kapcsolatok.tsv`-ben. Ez a brief szerint nem kérdés (küszöb alatt), de az M1 vagy a DT-F151b bemenete lehet: egy versben két motívum, a funkció különbözik-e (CLAUDE.md „Új motívum-ID”, 3. kérdés). *(proveniencia: scope=adat/elofordulasok.tsv (id, igehely; versstring-egyezés, tartomány-bontás nélkül) | forras=orkesztrátori ellenőrző szkript (scratchpad, nem commitolt), egyezik a `motivum_hatar.py --kimenet` táblájával | ts=2026-11-01)*

## 3. Mit jelent ez, és mit nem (korlátok)

- **Az üres eredmény nem azt mondja, hogy a határ rendben van**, hanem azt, hogy a két gépileg ellenőrizhető hiba (igehely-halmazok egymásba ágyazódása; beépített sor gerinc-kombináció nélkül) nem áll fenn. A formulaikus ág konstrukciójából következően gyenge szűrő: a gerinc-kombinációk a motívum *saját* beépített soraiból jönnek, így a próba főleg adat/szöveg-eltérést (rossz kulcs, hiányzó TAHOT/TAGNT-sor) fogna meg. Az ISTENTISZT-001-en 0 ilyen van; ez a #150 korábbi mérésével (0 hamis kizárás formulaikus hordozón) egyezik.
- **A részhalmaz-vizsgálat verspontos.** Nem látja a szomszédos vagy átfedő-témájú, de különböző versekből álló motívumokat (pl. ISTENTISZT-001 ↔ ALVIL-001, ApCsel 2); azokat a `motivum_kapcsolatok.tsv` kezeli.
- **A negatív kritérium tartalmi része** (pl. ISTENTISZT-001 névadás/erkölcsi intelem kizárások) nem gépi: azt csak modelles vagy emberi olvasat ítélheti meg. A HAMART-001 strukturális hordozóján a gépi próba eleve nem döntő (a #150 mérése: 83/163 felismert elutasítás, de 5 hamis kizárás).
- A lexikai hordozóra a próba kiterjesztése az **N-F150a** feladata; ide nem vettem be.
- A motívum készítő modelljét a repó adataiból (`motivumok/*.md`, `jeloltek.tsv`) nem tudtam megállapítani (nincs modellnév-mező); a „másik modell” választása ezért a felhasználó tudására épül.

## 4. DT443 — kérdés a felhasználónak (helyőrző; végleges szám a main-en)

**Kérdés:** legyen-e modelles rész (a `hatar-ellenor` subagent: következetlen határ + hígulás), és ha igen, melyik modellel?

**Alap:** a gépi rész a két próbamotívumon és a kiegészítő futásban is 0 kérdést adott, tehát a második vélemény *értékes része* a modelles rész; a gépi rész csak azt igazolja, hogy a mechanikus hibák nem állnak fenn. A modelles rész a havi keretből fut, API-kulcs nélkül, írni csak a `HATAR_<ID>.md` „Modelles rész” szakaszát írhatja, és nem ír prózát (K1).

**Opciók:**
- **(a) Nincs modelles rész.** A gépi rész marad, ingyen és determinisztikusan, és új lezárt motívumnál újrafuttatható. Az #151 itt lezárul. Hátránya: a feladat eredeti célja (a készítő vakfoltja) teljesületlen marad, mert a gépi rész ezt nem látja.
- **(b) Modelles rész, Fable 5.1.** A `hatar-ellenor` `model: fable`; M1 az ISTENTISZT-001-en. Előny: a függetlenség a friss kontextusból és a másik modellből jön; a legerősebb értelmező olvasat a két kérdéshez (hígulás = „csak a fölérendelt fogalmon át tartozik ide”). Hátrány: a legdrágább a havi keretből, és csak akkor „másik modell”, ha a motívumot nem Fable készítette.
- **(c) Modelles rész, Sonnet 5.5.** Olcsóbb a havi keretből; előny, hogy a mérés gyorsan megismételhető több motívumon. Hátrány: csak akkor másik modell, ha a motívumot nem Sonnet készítette; a hígulás-kérdésnél gyengébb ítélet várható.

**Javaslat: (b), az M1-et egyetlen motívumon, az ISTENTISZT-001-en futtatva** (a brief 4. szakasza szerint is), a következő okokból. Az ISTENTISZT-001-nek van mérhető aranystandardja (125 eldöntött jelölt: 33 beépített, 92 elutasított), tehát a hamis riasztás aránya a DT-F151b előtt számolható. A kérdés, amelyre a gép nem tud válaszolni (hígulás), értelmező ítélet: ott a gyengébb modell kockázata nagyobb, mint a havi keret többletköltsége egyetlen motívumon. **Feltétel:** a választás csak akkor jó, ha a motívumot készítő modell nem Fable; ezt a felhasználó tudja (a repó nem rögzíti). Ha a készítő Fable volt, a javaslat (c). A DT-F151b (kiterjesztés) az M1 után.

*Megjegyzés:* a brief a Fable 5.1 / Sonnet 5.5 párt kínálja; egy harmadik modell (pl. Opus, amelyen a `fuggetlen-ellenor` fut) nincs a kínálatban, a döntésnél nem vettem be.

## 5. DT443 — döntés (2026-11-01)

A felhasználó az orkesztrátor chatjében döntött: **(b), modelles rész Fable 5.1-gyel, M1 csak az ISTENTISZT-001-en.** A válasz szó szerint: „Igen, Fable 5.1”. Rögzítve a `DONTESEK.md` DT443 sorában. A feltétel (a motívumot nem Fable készítette) a repóból nem ellenőrizhető; a felhasználó a döntéssel vállalta. A DT-F151b (kiterjesztés) ⛔ marad az M1 után.

## 6. M1 — futás az ISTENTISZT-001-en (2026-11-01)

*Modell: a `hatar-ellenor` szerepet `claude-fable-5-1` töltötte be (a modell-ellenőrzés egyezett a `fable` kéréssel); a futtató és mérő session `claude-sonnet-5-5`. A `hatar-ellenor` definíció ebben a sessionben még nincs regisztrálva az Agent-eszközben, ezért a futás `general-purpose` subagenttel, `model: fable`-lel, a definíciófájl szövegét követve ment; a következő sessiontől a definíció néven is hívható.*

**Eredmény:** 5 kérdés (K1–K3 következetlen határ, K4 hígulás + következetlen határ, K5 hígulás) a `naplok/HATAR_ISTENTISZT-001.md` „Modelles rész” szakaszában. A futás után a `git status` szerint a subagent csak ezt a szakaszt írta (a `DONTESEK.md` és e napló módosítása az enyém).

**Mérés az aranystandardhoz** (`adat/jeloltek.tsv`, ISTENTISZT-001: 133 sor = 35 beépítve + 92 elutasítva + 6 nyitva; a 35 = 33 `elofordulas` + 2 `motivumkozi`, a feladat „33 beépített” számát az `elofordulasok.tsv` adja). *(proveniencia: scope=adat/jeloltek.tsv (id=ISTENTISZT-001) + naplok/HATAR_ISTENTISZT-001.md | forras=scratchpad-szkript, `split('\t')` | ts=2026-11-01)*

- **Idézés-pontosság:** a kérdések 22 különböző `jeloltek.tsv`-sorszámot idéznek; mind a 22 sor ISTENTISZT-001-é, az igehely és a döntés (beépítve/elutasítva/nyitva) egyezik az állítással. Hamis hivatkozás: **0/22**.
- **Lefedettség:** a kérdések 19 eldöntött sort érintenek a 127-ből (15%; 21 sor a 22-ből, ebből 1 nyitva — Ézs 41:25 —, amelyről nem dönt). Nem kérdezett sor: 108 eldöntött.
- **Hamis riasztás aránya:** gépileg nem állapítható meg — a kérdés értelmező ítélet (K1–K5 mindegyike a felhasználó szerint „valódi határ-kérdés” vagy „már eldöntött, tudatos”). Jelölések a lehetséges besoroláshoz: K3 maga jelzi, hogy a Zsolt 99:6 felhasználói döntés (2026-10-29), tehát a felhasználónak ismert kérdés; K5-nél a motívumfájl maga megnevezi a hamis isten nevét tartalmazó két sort (`motivumok/ISTENTISZT-001.md:446`), tehát a kérdés tudatos döntést kérdez újra. **A felhasználó besorolása kell:** kérdésenként „hasznos” / „hamis riasztás”; a rate = hamis / 5.
- **Kimaradt-e valódi probléma** (hamis negatív): az aranystandarddal nem mérhető (nincs ismert hiba-lista); a modell „nem kérdés” felsorolása (35 = 33+2, D-minta, jogi/eskü, tagadó forma) ellenőrizhető, de nem bizonyíték.

**⛔ DT-F151b** (kiterjesztés a többi lezárt motívumra) a felhasználóé; nem indítottam. Más motívumon nem futott a modelles rész.

## 7. K1–K5 besorolás (2026-11-01)

A felhasználó a chatben kérdésenként döntött; a „mehet” a rögzítésre vonatkozott. Tartalom és idézetek a `DONTESEK.md` DT476 sorában és a `naplok/HATAR_ISTENTISZT-001.md` „Felhasználói besorolás” blokkjában. A beszélgetésből két szövegtény: (1) a *besém* után a K4 szerint JHVH (H3068) áll a 2Móz 33:19-ben és 34:5-ben, az Ézs 43:1, 44:5, 45:3-ban nem; (2) a 2Móz 34:5 *vájikrá* alanya a héberben kimondatlan, ezért az „Isten az alany” olvasat a K4-ben nem szöveg, hanem értelmezés, és nem indok. Adat- és prózaváltozás nem készült (jeloltek.tsv, negativ_kriterium, lap): azt a #152 vagy külön tétel végzi. A DT-F151b (kiterjesztés) ⛔ marad.
