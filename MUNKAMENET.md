# Munkamenet — a tanulmánytól a lexikon-oldalig

*Készült: F7 (chat-menet, Sonnet), 2026-09-20, a mérés forrása `F7_BRIEF.md` §1.*

## Mire való, mire nem

Ez a fájl az `ATALAKITASI_TERV.md.md` 7. pontjának („Az új munkamenet") 23
lépését rögzíti egy táblában, lépésenként: ki végzi, mi a kimenete, és **ma**
mivel fut. Nem specifikáció-forrás — a lépések tartalmát és sorrendjét a terv
7. pontja adja, ez a fájl csak a mai üzemi állapotot vetíti rá.

**Ami itt NEM szerepel, csak hivatkozásként:**
- a hét lépéses determinisztikus kutatási protokoll (gerinc-metszet →
  szemantikai mező-hipotézis → teljes scan → kollokáció → igealak-ellenőrzés
  → LXX-híd → nevesített tanító) — l. `CLAUDE.md`, „Kutatási menet — a hét
  lépés";
- a 4.6 motívum-gate négy kérdése (azonosság hordozója, negatív kritérium,
  funkció-különbség, részhalmaz) — l. `CLAUDE.md`, „Új motívum-ID kiosztása —
  négy kérdés, kötelezően".

Mindkettő egy igazság-forrásból él; ez a fájl nem másolja őket.

## A „ma mivel fut" oszlop értékei

Az oszlop kizárólag három alakot vehet fel:
1. **konkrét, ma létező parancs** — a hivatkozott szkript/cél ma is fut, `test -f`-fel ellenőrizve;
2. **kézi** — a lépés emberi/kutatói munka, nincs is szüksége eszközre;
3. **`F8 — nincs eszköz`** — a terv „végrehajtó" szerepet ír elő, de a hozzá tartozó eszköz (script, subagent, minta) ma nem létezik.

Nem létező eszköz **kizárólag** az `F8 — nincs eszköz`
jelöléssel szerepel — futtathatóként sehol nem áll.

## A) szakasz — tanulmány: a motívum felismerése

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| A1 💎 | a szakasz feldolgozása, PaRDeS-kifejtés | kutató | tanulmány prózája | kézi | drága modell (l. lent) |
| A2 💎 | 2. pont kulcsszó-táblázata | kutató | kulcsszavak, Strong-számmal | kézi | drága modell |
| A3 | a kulcsszó-táblázat sorainak kiírása a táblába | végrehajtó | `kulcsszavak.tsv` sorok | `eszkozok/betolt.py kulcsszo --study … --konyv …` | átmeneti tábla, `id` nélkül (SEMA 2.8); a motívum-ID az A4-ben, a `jeloltek.tsv`-ben születik |
| A3b | jelölt-generálás meglévő motívumokhoz → **gerinc-kártya** (a vak olvasás után) | végrehajtó (`gerinc_kartya.py`) | automatikus jelöltlista | `python eszkozok/gerinc_kartya.py --szakasz "…" --osszevet <tanulmány>` | az A1–A2 kártya nélkül készül (A4 torzítás); a kártya csak jelölt, `--ir` csak `új` sort ír `nyitva`-val, a kiszűrt és a `szuretlen_tag` sor soha nem íródik be; a `jelolt.py` régi kimenete megmarad |
| A3c | kártya ↔ kulcsszó-táblázat összevetés | végrehajtó (`gerinc_kartya.py --osszevet`) + kutató | két lista a kereszthivatkozás-naplóba, üresen is (explicit „üres” jelöléssel) | `python eszkozok/gerinc_kartya.py --szakasz "…" --osszevet <tanulmány>` | az „olvasás talált, kártya nem” lista az A4 ⛔ bemenete. Ha a `kulcsszavak.tsv`-ben nincs sor a tanulmányhoz, az összevetés nem végezhető el (az A3 még nem futott); a kártya ezt kiírja, a listák nem töltendők ki |
| A4 💎 ⛔ | motívum-felismerés: új ID vagy meglévő ID új előfordulása | kutató javasol + **ember dönt** | `motivumok.tsv` + `elofordulasok.tsv` | kézi | **kötelező megállási pont — l. lent** |
| A5 | 3/b pont kereszthivatkozásai | kutató + végrehajtó | `kapcsolatok.tsv` | `eszkozok/lekerdez.py tsk` / `eszkozok/lekerdez.py karoli` | a lekérdezés fut; a `kapcsolatok.tsv`-be írás kézi; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| A6 💎 | előrejelzett motívum rögzítése (státusz = *előrejelzett*) | kutató | `motivumok.tsv` | kézi | drága modell |
| A6b | új ID esetén a 4.6 gate négy kérdésének megválaszolása | kutató + ember | `motivumok.tsv` mezői | kézi | `eszkozok/gate.py` az ütközés-/részhalmaz-jelentést adja (4. kérdés támpontja), a döntést nem helyettesíti |
| A7 | motívumnapló, index, sorozat-tábla újragenerálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel naplo --ir` és `--cel index --ir` | a sorozat-tábla = a napló „Feldolgozott igeszakaszok listája", kézi (l. N10, N11, `ATALAKITASI_TERV.md.md` A7); csak a napló és az index rész generált |

## B) szakasz — küszöbátlépés és tematikus study

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| B1 | küszöbfigyelő jelzi a ⭐ 3+ átlépést | audit | jelentés | `eszkozok/kuszob.py` | a ⭐ számítás a `general.py`-ban marad, a `kuszob.py` importálja; átlépés = ≥ 3 és üres `forras_study`; kód 1 = van átlépés |
| B2 | gerinc-metszet + grammatikai szűrés | végrehajtó | kivonat | `eszkozok/lekerdez.py gerinc` | a grammatikai szűrés (`adat/grammatikai_strongok.tsv`) be van építve; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| B3 💎 | szemantikai mező-hipotézis | kutató | mező-szavak listája | kézi | drága modell — a menet egyetlen generatív lépése |
| B4 | teljes scan + kollokáció + igealak + LXX-híd | végrehajtó | jelölt-halmaz provenienciával | `eszkozok/lekerdez.py scan` / `kollokacio` / `igealak` / `lxx-hid` | mind a négy parancs fut, mindegyik saját provenienciát ír; burkoltan a `lexikai-scan` subagent (`.claude/agents/lexikai-scan.md`) is futtathatja; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| B5 💎 ⛔ | jelöltek minősítése | **ember** + kutató javaslattal | `jeloltek.tsv` kitöltve | kézi | **kötelező megállási pont — l. lent** |
| B6 | beépített sorok átvezetése | végrehajtó | `elofordulasok` + `kapcsolatok` | `eszkozok/betolt.py beepit --munkalap …` | csak `beépítve` sort léptet elő; a `kapcsolatok` kézi (G10) |
| B7 | study 1. pont, kereszthivatkozás-napló, index generálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel study`; `--cel naplok`; `--cel index --ir` | a `study` és a `naplok` cél **nem élesíthető** — csak `--kimenet` alá termel próbát; kizárólag az `index` írható közvetlenül élesen |
| B8 💎 | 2-5. pont megírása | kutató | PaRDeS-próza | kézi | drága modell |
| ~~B9~~ | *(kivezetve, F178.4, 2026-11-08)* nevesített tanítói menet | — | — | — | A lexikonlapról a nevesített tanítói rész kikerült (F178.4, a felhasználó jóváhagyásával: „minden itteni javaslatod a lexikon ág lezárására”); új tanítói menet nem indul. A sablon archív jelöléssel megmarad (`sablonok/7_PaRDeS_tanitoi_kereses_sablon.md`), a meglévő tanítói fájlok archívumként. A recepció helye a visszhang-réteg (a lap 4.11 blokkja). |
| B10 | Q-kapu + konzisztencia-ellenőrzés | audit | jelentés | `eszkozok/ellenoriz.py [--study …]` | Q2–Q6 és a `felteteles` datasetek és a 8/c kézi; hook nincs (F8 §3) |

## C) szakasz — lexikon-oldal

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| C0 ⛔ | szótári szócikkek emelése: új motívum vagy előfordulás után a lexikon minden Thayer/BDB Strong-számának teljes szócikke magyarul (F28_EMELES_BRIEF.md E7, D48) | végrehajtó (Opus) + **ember** a szúrópróbánál | `adat/forditasok.tsv` `teljes` sorok (`opus`, a jóváhagyottak `kezi`) | `eszkozok/emeles.py lista` (a `kimarad=nem` sorok a hiányzók; új vagy megváltozott forrás-hash is ide kerül), majd szócikkenként `emeles.py prompt` / `helyorzo` → fordítás (`vegrehajto-opus` subagent, `.claude/agents/vegrehajto-opus.md`) → `emeles.py ellenoriz` (javítóréteg + kapuk) → `rogzit` → `beir --allapot opus`; szúrópróba: `emeles.py minta` + `naplo_nezet` | az F28 E4–E5 folyamata: kapuhibánál egy önújrapróba, utána `naplok/EMELES_bukottak.tsv`; a szúrópróba (10%, de legalább 5, rétegzetten) **kötelező megállási pont**, 20% fölötti kifogásnál prompttétel. A CI E19 HIBA-t ad, ha egy Thayer/BDB `lexikon_hivatkozasok`-sorhoz nincs `opus`/`kezi` fordítás. A forrássablonba (#23) nem került hivatkozás: a #23 még nem indult |
| C-x | szakaszcímke (⛔ csak eltérésnél) | végrehajtó + kutató eltérésnél | `jelentes_szam`-ból levezetett szótári szakasz és címke | `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id [ID]` | Az előfordulás-sorok `jelentes_szam`-ából a szótári szakaszt és a címkét a `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id [ID]` vezeti le. Jelzés nélkül az `--ir` rögzíti. Jelzésnél (a szótár példahelye más pontra mutat, két pont, üres mező, nincs útvonal, tagolatlan szócikk, minősítő) a menet megáll, és a kutató dönt; kitöltés nem gyenge vagy asszociatív anyaggal történik. |
| C-y | fordítás a lap előtt | végrehajtó | `adat/forditasok.tsv` | `python eszkozok/glossza_lexikon_forditas.py lista --id [ID]` | A lap generálása előtt a `python eszkozok/glossza_lexikon_forditas.py lista --id [ID]` listázza a lap fordítatlan szótári egységeit. A hiányzókat a #121 eszköze és kapui rögzítik az `adat/forditasok.tsv`-be. Ami a lapon fordítatlan marad, `(fordításra vár)` jelölést kap. A gépi mérése nyitott (N-F148a: a 21. szabály (iii) pontja nem lett SÉRTÉS-szabály); addig `python naplok/F148_meres.py --forditas`. |
| C1 | lexikon TUDOMÁNYOS szakaszainak + a törzscikk generálása (render) | végrehajtó | generált fájlok | `eszkozok/general.py --cel lexikon --ir`; `eszkozok/general.py --cel torzscikk --ir` | RENDER_BRIEF.md v5 (2. menet, R2.3) óta mind a 8 motívum lexikonoldalán a 10 generált blokk MELLETT a rések (felsorolásuk: `adat/SEMA.md` 2.12) is generáltak: `adat/res_forras.tsv` + a tanulmány/napló `<!-- RÉS-KEZDET/VÉGE -->` jelölői közötti törzse, vagy (`alatamasztas`-nál, 0-kapcsolatú motívumoknál és KIRALY-001-nél) egy adatból vezetett mondat alapján (G1/G2/G16). A `_TORZSCIKK.md` a lexikonoldalból renderel ("render a renderből", G7) — nem önálló lépés |
| C2 💎 | a rések megírása **a tanulmányban**, nem a lexikonoldalon | kutató | tanulmány-rés (a tematikus tanulmány vagy a kereszthivatkozás-napló `<!-- RÉS-KEZDET/VÉGE -->` jelölői között) | kézi | drága modell — a rések: `adat/SEMA.md` 2.12. **A lexikonoldal kézzel nem szerkeszthető** (RENDER_BRIEF.md G4); a `ellenoriz.py` 11. szakasza SÉRTÉSnek jelzi az eltérést |
| C3 💎 | ~~lexikon OLVASHATÓ megírása~~ — MEGSZŰNT (2026.09.21, felhasználói döntés): a lexikon-oldal egyetlen változata a _TUDOMANYOS.md | kutató | kézi fájl | kézi | drága modell; az első (ISTENTISZT-001) átemelve a pilotból, a többi a célvonal-döntéstől függ |
| C-z | a próza-lefedettségi lista átnézése a lezárás előtt | végrehajtó | napló | `python eszkozok/proza_lefedettseg.py <ID>` | A tanulmány vagy a lap lezárása előtt a végrehajtó lefuttatja a `python eszkozok/proza_lefedettseg.py <ID>` parancsot (lefedettség: a próza által meg nem nevezett előfordulás, kapcsolat, motívumközi kapcsolat, nyitott jelölt; egyenetlenség: blokkonként a karakter/elem, küszöb: 150 karakter alatt „kevés”, a blokk-medián 4×-ánál távolabb „egyenetlen”, legalább 3 elem; a gyűjtő mondat külön kategória; DT471). A kimenet a naplóba kerül; a „kész” állapot feltétele, hogy a lista üres vagy minden tétele indokolt. |
| C-w | a próza gazdája | értelmező | prózafeladat | kézi | Ha a motívum adata érdemben változik (új előfordulás, új kapcsolat, új jelölt-döntés), a lezárás előtt **kötelező egy értelmező prózafeladat**: ő nézi át a C-z listáját, és a prózát kiegészíti. Az adatot író feladat nem zárhat le prózafeladat nélkül. **Új cikknél** (és 2. kiadásnál, ha a próza újraíródik) a próza nulláról, egy kézből, a `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md` promptjával készül (F178.3; a HAMART-001 mint arany). **U2/U3 szétválasztás** (F178.2): `sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pont, „A HAMART-001 mint arany”, 1. szabály. |
| C-vh | a visszhang kinyerő tábla (4.11) | Targum, Vulgata: modell (Sonnet) + **másik kéz** ellenőrzi; LXX: gépi | `adat/visszhang_megfelelok.tsv` (SEMA 2.53) | `python eszkozok/visszhang/megfelelo_kinyer.py beolvas <kinyert.tsv> --ellenor <a tényleges modellnév> --atnezes <átnézés.tsv>`; `… lxx --motivum [ID]`; `… ellenoriz` | F178.5 (DT639, DT645, DT646, DT648). A lánc (lánc-szavak, láncversek) a motívumadatból jön, a generátor vezeti le, nem a kinyerés választja; a szabály: `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` „A 4.11 visszhang-blokk szabályai” 0. pont. A kinyerő ezekre a (lánc-szó, láncvers) párokra emeli ki a megfelelőt (a hiányzó párok: a lap 4.11 „kinyerése még nem történt meg” cellái). A kinyerés és az ellenőrzés két kézzel, soronkénti átnézés-bemenettel: `adat/SEMA.md` 2.53 „Két kéz”. A LXX-oszlop és az alapvonal gépi; a BDB rokon nyelvi háttere (`forras=bdb`) ugyanebben a lépésben. **Hol történik:** új cikknél a próza (C-w) előtt, a motívum lezárásának menetében; a meglévő lapoknál a motívumonkénti lezárás (#10) lépése — addig a blokk kimondja, hogy a Targum- és a Vulgata-megfelelő kinyerése még nem történt meg (nem kitöltés). Kapu: olvasói kapu VISSZHANG (a V-alszabályok: `adat/SEMA.md` 3.11). |
| C-g | gépi kapuk a generált lapon | végrehajtó | napló; a kapuk kimenete | `python eszkozok/ellenoriz.py` (24. és 25. szabály); `python eszkozok/proza_1a.py [ID] --reszletes`; `python eszkozok/muhely_allapot.py --motivum [ID]` (6. kapu) | A próza (C-w) és a lap újragenerálása (C1) után, a határ- és lektori kör (C-h) előtt. Feltétel: a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` Minőségi kapujának L8 pontja (24. és 25. szabály, új cikknél a teljesség-mérés, olvasói kapu); a C-z listája üres vagy indokolt. Bukásnál a próza gazdája javít (C-w), nem a kapu-futtató; a C-h csak zöld gépi kapuk után indul (DT546). |
| C-h ⛔ | határ-ellenőrzés a lezárás előtt | gépi rész: végrehajtó; modelles rész: `hatar-ellenor` subagent (Fable), **a felhasználó indítja, minden futás előtt az ő jóváhagyásával** (kreditből fizetendő, a havi csomagba nem fér; DT546); döntés: **ember** | `naplok/HATAR_<ID>.md` (Gépi rész, Modelles rész) | `python eszkozok/motivum_hatar.py --motivum [ID]`; utána a `hatar-ellenor` subagent (`.claude/agents/hatar-ellenor.md`) | A motívum adatának és prózájának elkészülte (C-z, C-w) után, a lezárás (C5) előtt. A gépi rész determinisztikus (részhalmaz; negatív kritérium a beépített soron). A modelles rész friss kontextusú második vélemény (következetlen határ, hígulás). A `hatar-ellenor`-t a felhasználó indítja, a `/kiadas` lektorával (C-k) egy menetben is. Egyik sem javít, mindkettő kérdést ad; a kérdések a Kiadóba (felület) kerülnek (C-l). A határ-kérdés (`forras=hatar`) a lezárást blokkolja (Feed 5. kapu). **Kötelező, és minden sor-változás után újrafuttatandó** (F178.1): a frissesség szabálya és jele `sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pont, „A HAMART-001 mint arany”, 2. szabály (`ellenoriz.py` 39., Feed 5). Az U2/U3 szétválasztás miatt (C-w) a C-h a próza előtt is lefut, ha a határt és a prózát egy session viszi. |
| C-l ⛔ | döntések a Kiadóban (felület) | **ember** | `naplok/LEKTOR_<ID>.tsv` (`valasz`, `allapot`) | `python eszkozok/lektor_kerdesek.py --motivum [ID]`; a felület: `python eszkozok/lektor_felulet/epit.py <kimenet.html> --motivum [ID]` | A motívum ellenőrző kérdései (határ, lektor, próza-lefedettség, próza-javaslat) egy sémában, motívumonként egy táblában; a döntések helye a Kiadó (felület; F157). A választ az átvezető feladat viszi az adatba (a `jeloltek.tsv`-n át) vagy a prózába (C-w). A megválaszolt határ-kérdés nem nyitott (Feed 5. és 7. kapu). |
| C-o | olvasói kapu (Feed 9) | végrehajtó | a kapu jelentése | `python eszkozok/olvasoi_kapu.py` (a Feed 9. kapuja: `python eszkozok/muhely_allapot.py --motivum [ID]`) | A Kiadó-döntések (C-l) átvezetése és a lap újragenerálása után, a vizuális átnézés (C-v) előtt. A 2026-11-02-i lap-átvilágítás gépesíthető olvasói hibaosztályait méri (belső jelölés és régi pontszám az olvasói prózában, egyenes idézőjel, átírás- és rövidítés-egység, BDB-szövegtisztaság, Kivonat ↔ adat számszerű egyezés, kolofon-teljesség stb.). Feltétel: 0 BUKÁS. A DT497 (3) visszavonásával (DT547) ez a Feed 9. kapuja; bukásnál vissza a C-w-re. |
| C-v ⛔ | a felhasználó vizuális átnézése | **ember** | a jóváhagyás rögzítve (a #123-ban: `naplok/F123_atnezes_<ID>.md`: dátum, szó szerinti idézet, a nézet azonosítója), és egy sor az `adat/lap_atnezesek.tsv`-ben (SEMA 2.48, DT554: `ki` = felhasználó, `idezet` szó szerint, `lap_commit` a lap mai commitja, `forras` a naplóra mutat) — a Feed 9. kapuja ezt a sort olvassa | a renderelt lap friss nézete (a mai generátorral, a kolofonnal együtt) | A lezárás (C5) előtti utolsó lépés: a felhasználó maga nézi át a renderelt lapot, nem a markdownt és nem egy session jelentését (DT547: „lap megnyitása merge előtt”). A jóváhagyás nélkül nincs 1. kiadás; kifogásnál vissza a C-w-re, utána újra C-g és C-o. Lapot érintő PR „mergelhető” jelzése is csak a renderelt lap átnézése után adható. |
| C5 ⛔ | lezárás: Feed 9/9, 1. kiadás, verzió-emelés | végrehajtó + **ember** (jóváhagyás) | `adat/kiadasok.tsv` 1. kiadás sora; `adat/motivumok.tsv` `statusz_verzio` + `statusz_datum`; a lap újragenerálva | `python eszkozok/muhely_allapot.py --motivum [ID]`; a két tábla sora kézzel (SEMA 2.46, 2.1); `python eszkozok/general.py --cel lexikon --id [ID] --ir` | **Kész** = a Feed (`muhely_allapot.py`, F156) mind a 9 kapuja zöld (a 9. az olvasói kapu, C-o; DT547), és a felhasználó vizuális átnézése (C-v) rögzítve; a kapuk pontosítása: DT-F156b (`naplok/MUHELY_FEED_STASH_naplo.md`). **Lezárás** = az 1. kiadás sora az `adat/kiadasok.tsv`-ben (`kiadas=1`; a `proza_modell` a tényleges modellnév vagy `manual`, DT492) és a `motivumok.tsv` verzió-emelése (`statusz_verzio` +1, `statusz_datum` a lezárás napja; az állapot `publikálható` marad; minta: ISTENTISZT-001 v4, DT486). Mindkét tábla írása előtt soronkénti összevetés az eredetivel. Utána a lap újragenerálása, hogy a kolofon a kiadás sorát mutassa. A lezárásnak nem feltétele a `/kiadas` (C-k). **A tanítói rés kivezetése (DT643, lépcsős):** a motívum `tanitoi` sora az `adat/res_forras.tsv`-ből és a tanítói fájlja (`motivumok/naplok/<ID>_tanitoi_kereses.md`, ha van: `git mv` az `archivum/<ID>/` alá, ARCHÍV fejléccel, a NYITOTT_FELADATOK.md és a briefek `olvas` mezőjének hivatkozásaival együtt) a lap e lépésbeli újragenerálásával **egy commitban** kerül ki; a régi lap a teljes folyamaton kívül nem változik. Az utolsó motívum után a CLAUDE.md és a SEMA 2.12 „kilenc rés” mondata „nyolc rés”. |
| C-k | `/kiadas` — a 2. kiadás bemenete | a felhasználó indítja | `naplok/KIADAS_<ID>_lista.md`, `naplok/KIADAS_<ID>_lektor.md`; a Kiadó (felület) `forras=lektor` kérdései | `/kiadas [ID]` (`.claude/commands/kiadas.md`) | A lezárást nem akasztja (DT486; DT-F156i): a kimenetéből jövő kérdések (`forras=lektor`, `forras=proza_lefedettseg`) a következő kiadás bemenetei, a Feed 7. kapuja nem számolja őket blokkolónak, és „2. kiadáshoz: N kérdés”-ként mutatja. A 2. kiadásban a próza gazdája (C-w) javít, a `/kiadas` 5. lépése új `kiadasok.tsv`-sort ír; a kisebb, helyi javítás útja a C-j (`/lap-javit`). |
| C-j | `/lap-javit` — interaktív lapjavítás, emberi lektorálás | a felhasználó indítja; a parancs (Opus) javasol, **a felhasználó hagy jóvá** | `adat/lap_javitasok.tsv` (SEMA 2.49); a javított forrás; a kolofon „Emberi lektorálás” sora | `/lap-javit [ID]` (`.claude/commands/lap-javit.md`); előnézet: `python eszkozok/lap_javit_proba.py --id [ID] --csere <tmp>/csere.tsv --kimenet <tmp>/proba` | Bármikor, kiadott és nem kiadott lapon (DT599). A felhasználó idézettel rámutat egy helyre; a parancs osztályoz: **próza** (helyben javaslat, írás a forrásba csak jóváhagyás után), **adat** (a `jeloltek.tsv`-n át), **forrás** (a BDB/Thayer javítótábláján át), **generátor** (`N-F…` tétel, külön session). A `gond` zárt: homályos, pontatlan, szakszó, ellentmond az adatnak. A végén újragenerálás, olvasói kapu, `ellenoriz.py` és régi/új lista; kiadott lapnál új `kiadasok.tsv`-sor és új átnézés (C-v), mindkettő csak a felhasználó szavával. A parancs nem commitol. |
| C4 | commit/push, `main` merge | végrehajtó + ember | — | kézi | git-parancsok a `CLAUDE.md` szabálya szerint; nincs önálló script |

💎 = a kilenc, drága modellt igénylő lépés (A1, A2, A4, A5 — a kutatói rész, A6, B3, B8, C2, C3). ⛔ = kötelező emberi megállási pont.

**A lezárás menete motívumonként** (2026-11-02, DT546, DT547; az ISTENTISZT-001 arany lapjának 1. kiadása után kiderült, hogy a lezárás felé vitt lapokon olvasói hibák maradtak, amelyeket a szerkezeti kapuk átengedtek). A lezárás előtti lépések sorrendje kötött:

1. **gépi kapuk — feltétel** (C-g): C-x, C-y → C1 → C-z, C-w → 24. és 25. szabály, Feed 6, új cikknél a teljesség-mérés; **olvasói kapu** (C-o, Feed 9): 0 BUKÁS;
2. **a felhasználó vizuális átnézése** (C-v ⛔) a renderelt lapon (lapnézet), rögzítve;
3. **egy javítókör** az átnézés alapján (C-w), utána a gépi kapuk újra zöldek;
4. **1. kiadás** (C5): Feed zöld, `kiadasok.tsv`-sor, verzió-emelés, a lap újragenerálása.

A lépésszám cikkenként rögzített (DT566, a felhasználó jóváhagyásával, 2026-11-02: „mehet”): második átnézési vagy javítókör nincs. Ami az 1. kiadás után derül ki — a **határ- és lektori kör** (C-h, Fable, **minden futás előtt a felhasználó jóváhagyásával**, kreditből) az új prózán, a Kiadó (C-l) kérdései, későbbi észrevétel —, az a **2. kiadás bemenete**, nem az 1. kiadás feltétele („a lektori átnézés eredménye egy új kiadás”). A régi lektori kérdések (az elavult prózáról) nem ellenőrzési lépés; lezárásuk: az 5. menetszabály lent. Egy lépés csak az előző zöldje után indul; gépi bukásnál vissza a próza gazdájához (C-w). A **C-k** (`/kiadas`) a lezárás után bármikor indítható, és a 2. kiadás bemenete. A hátralévő 8 motívumnál ez a #123 új cikk-menetének vége (`F123_MIGRACIO2_BRIEF.md` 3. szakasz, U4–U6), a #10 a lapok lezártságát méri (`F10_LEXIKON_LEZARAS_BRIEF.md`). Az ISTENTISZT-001 1. kiadása e sorrend előtt készült; hogy a 9. kapu és a C-v rá hogyan vonatkozik, azt a #10 zárómérése rögzíti, vagy ⛔ a felhasználó elé teszi.

**Menetszabályok az új cikkhez** (DT585, az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket és hozza is meg« (2026-11-03); az ALVIL-001 új cikkének tanulsága):

5. **A régi lektori kártyák** (a Kiadón az elavult prózáról feltett kérdések) a Kiadó-lépésben „az újraírás okafogyottá tette” jelöléssel zárulnak, az orkesztrátorral egyeztetve; a **határkártyákra** (`forras=hatar`) a felhasználó dönt, ezeket nem zárja le a menet.
6. **A lapnézet** a C-v-hez: `python C:\Users\bases\pardes_eszkozok\epit_nezet.py lexikon/<ID>_TUDOMANYOS.md <scratchpad>\x.html <commit>`, **privát** artifactként, mindig világos témával; a link az `eszkozok/lektor_felulet/lapnezetek.tsv`-be kerül. A menet a renderelt lapot maga is megnyitja és átnézi, mielőtt kész-nek jelzi.
7. **Átnézés és kiadás csak a felhasználó szavával.** Az `adat/lap_atnezesek.tsv` sora és az 1. kiadás (`adat/kiadasok.tsv`) csak a felhasználó szó szerinti jóváhagyásával íródik. Hogy egy későbbi lapváltozás érvényteleníti-e az átnézést: `adat/SEMA.md` 2.48 „Érvényesség” (DT665).

## A4 és B5 — kötelező megállási pont

**A4** és **B5** nem azért állási pont, mert az ügynök autonóm, hanem mert a
2026.09.11-i modell-összehasonlításban *mindkét* ág átlépett egy besorolási
döntési ponton anélkül, hogy jelezte volna: a Sonnet-ág némán követte a
motívumnapló 5:29-re vonatkozó döntését, az Opus-ág némán felülírta — egyik
sem kérdezett (`ATALAKITASI_TERV.md.md` 520. sor). A menet ezen a két ponton
**megáll és kérdez**, akkor is, ha a válasz nyilvánvalónak látszik.

**Hogyan készítsd elő a döntést (bármely ⛔ pontnál).** A megálló feladat a `DONTESEK.md`-be (az ágon: a `dontesek/uj/<ágnév>.md` PR-fájlba, `CLAUDE.md`) tételt nyit; a döntést a felhasználó hozza. Ha a döntés előkészítéséhez erősebb modell kell (például Opus), azt egy **külön sessionben vagy a chatben** végezd, a [`DONTES_KERDES_SABLON.md`](DONTES_KERDES_SABLON.md) kérdéssablonjával: az Opus javaslatot ad, nem dönt, és a végrehajtó/orkesztrátor modellje (a brief `modell:` sora) ettől nem változik. A döntés egy mondat és az opció száma a tétel „Döntés” oszlopában (🟡 → 🟢); a következő `/kovetkezo` a 2. lépésben onnan folytatja.

## Szereposztás — a mai valóság

A terv 5.1 pontja hat szerepet ír le (fő szál, `lexikai-scan` subagent,
`tanito-kereso` subagent, `szerkeszto` subagent, `ellenor` subagent, ember).
Az F8.9 óta két subagent van definiálva a `.claude/agents/` alatt
(`settings.json` továbbra sincs); a `szerkeszto` és az `ellenor` subagent
nem F8-tárgy (`F8_BRIEF.md` §3). A négy érintett szerep ma:

- **audit (B1, B10)** — nem subagent, hanem szkript-szerep: a B1-hez a
  `kuszob.py`, a B10-hez az `ellenoriz.py` (F7 D3 — az audit determinisztikus,
  a modell csak hibaforrás volna).
- **`lexikai-scan` (B2, B4)** — `.claude/agents/lexikai-scan.md`, haiku;
  kizárólag `lekerdez.py`/`jelolt.py` futtatása, fájlt nem ír.
- **`tanito-kereso` (B9, kivezetve: F178.4)** — `.claude/agents/tanito-kereso.md`, sonnet; a
  `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` (archív) szerint dolgozott, kizárólag a
  `[study-mappa]/naplok/[motívum]_tanitoi_kereses.md` fájlt írta. Új futása nincs.

## Kontextus-őrzés (F32, KONTEXTUS)

Az ISTENTISZT-001 pilot minősége abból jött, hogy egyetlen összefüggő tematikus
tanulmány volt az alap, amelyet egy kéz írt gondolatmenetként, és minden későbbi
lépés ebből renderelt. A munka három fajtája:

- **adat** (import, szótárfordítás, LXX-megfelelő, licenctábla, Károli–Strong, CI,
  szkript): a motívum átlátása nem kell hozzá; csomagmód, modellkiosztás és
  subagent szabadon használható.
- **ertelmezo** (tematikus tanulmány, kereszthivatkozás-napló, értelmezés, kivonat,
  a jelentéstartomány kiválasztása a D50 szerint, a `motivumok/[ID].md` kézi forrása).
- **folyamat** (szabály, sablon, orkesztrátor): csomagolható, ha nem ír motívumfájlt.

A fejléc `munka` mezője (`BRIEF_SABLON.md`) jelöli; a négy szabály:

1. **Az értelmező réteg egy kézben készül.** Egy motívum értelmező rétegének prózáját
   egy brief írja, egy modellel (`DONTESEK.md` DT-F32b: az értelmező modell; jelenleg `opus`).
   Nem kerül csomagba, és nem osztható író subagentekre. A session-határ megengedett:
   ha a kontextus nem fér el, a folytató session ugyanazt a briefet viszi tovább, és a
   3. szabály szerint az egészet olvassa.
   - *Kivétel:* csak olvasó subagent (például `fuggetlen-ellenor`, audit-szkript)
     értelmező menetben is futhat. Író subagent nem futhat.
   - A csomagmódba `munka: adat`, valamint motívumfájlt nem író `munka: folyamat`
     feladat kerülhet.
2. **A forrásdokumentum próza-elsőbbségű.** A `motivumok/[ID].md` összefüggő érvelés
   markerekkel, amelyekből a generátor kinyeri az adatot; nem adatséma, amelybe
   prózamezők vannak beszúrva. Az `adat/SEMA.md` a kinyerést írja le, nem a dokumentum
   szerkezetét. A forrássablon (`9_PaRDeS_motivum_forras_sablon.md`) szakaszsorrendet
   és markereket adhat, mezőhatárokat nem.
3. **Aki motívumba ír, az egészet olvassa.** Ha egy feladat `ir` listájában
   `motivumok/[ID]`, `tematikus_lezart/[ID]*` vagy `lexikon/[ID]*` szerepel, az `olvas`
   listájának kötelezően tartalmaznia kell a motívum teljes tematikus tanulmányát és
   kereszthivatkozás-naplóját. A javító körökre is érvényes. A `feladatok.py`
   ellenőrzi (`ellenoriz`, `fuggesek`; szabályleírás: `naplok/KONTEXTUS_szabalyok.md`).
4. **A lánc próbája megelőzi a szerkezet véglegesítését.** A B-szerkezet forrássablonja
   (#23 M1) csak akkor véglegesíthető, ha (a) egy motívum teljes értelmező rétege a fenti
   szabályok szerint elkészült, és (b) az eredmény hozza az ISTENTISZT-001 mércéjét
   (L1–L7 + a DT2 két rés-szabálya, a #10 szerint; DT68 (2), DT74 (5)). A próba helyéről a `DONTESEK.md` DT-F32a tétele döntött (🟢, 2026.10.04): a #12 kettéválik, a **#12a próza-próba** a #23 M0 és M1 közé esik, éles render nélkül (csak `generalt_proba/`); a #12b élesítés az eredeti helyén marad.

A csomagba sorolást a `python eszkozok/feladatok.py csomag <id> …` ellenőrzi; a
`/kovetkezo` csomagjavaslat előtt kötelezően futtatja.

## Generátor-tények

- `ELESITHETO = {naplo, index, nyitott, lexikon, torzscikk}` — ez az öt
  `general.py --cel` érték írható közvetlenül éles fájlba (`--ir`).
- A `naplok` és a `study` cél **nem élesíthető** ebben a fázisban — csak a
  `--kimenet` könyvtár alá termel próbát, `--ellenoriz`-nél PIROS marad.
- A ⭐ 3+ küszöb-számítás a `general.py`-ban él (`fo_elofordulas_csoportok()`
  + `render_naplo_kuszob()`), nem a `gate.py`-ban és nem a `lekerdez.py`-ban.
  A küszöb-összevetést és a kilépési kódot a `kuszob.py` adja (F8.4).

## C) szakasz — a lexikon-generálás tényleges hatóköre

A terv 462. sora (F6-szakasz) és a C1/C2 sor korábban „0-8. szakasz
generálva"-t és „9. szakasz = Nyitott kérdések"-et állított — ez azóta a
LEXV2_2 (v2 oldalszerkezet) és a RENDER_BRIEF.md v4 (1. menet) miatt kétszer
is módosult. **Ma érvényes állapot** (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`
v3, `eszkozok/lexikon_general.py`):

- **generált** szakaszok (10 blokk, `general.py --cel lexikon`): Tartalomjegyzék,
  Jelmagyarázat, 1. Előfordulások, 1/b. Kizárt és vizsgált helyek, 2. Szótári
  háttér, 3. LXX-fordítói döntések, 4. Kereszthivatkozások, 5. Kapcsolatok,
  8. Irodalom és idézés, Kolofon.
- **rés** (hét, `res_blokkok_alkalmaz()`, RENDER_BRIEF.md G1–G4): `kivonat`,
  `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`,
  `modszertan` — fejlécsoruk a `adat/res_forras.tsv`-ből, törzsük vagy a
  motívum tematikus tanulmányából/kereszthivatkozás-naplójából
  (`forras=tanulmany`), vagy — csak a 0-kapcsolatú motívumok
  `alatamasztas` résénél, és a KIRALY-001 `alatamasztas` résénél —
  a `res_forras.tsv`-be előre rögzített, adatból vezetett mondatból
  (`forras=adat`, G16/D26, RENDER_BRIEF.md D28). A `forras=lap` a
  RENDER_BRIEF.md 2. menetének végére (R2.3) megszűnt: mind az 56 sor
  `tanulmany` vagy `adat` forrású (`adat/res_forras.tsv`). A lexikonoldal
  ezeket a szakaszokat is a generátorral kapja; **kézzel csak a
  tanulmányban szerkeszthetők** (G4). A lexikonoldal első sora fájl-szintű
  gépi jelölést hordoz (`<!-- GENERÁLT: general.py --cel lexikon | rések:
  [forras_study] -->`, R2.5) — nem tévesztendő össze a 10 blokk saját
  GENERÁLT-KEZDET/VÉGE jelölésével.
- a **törzscikk** (`lexikon/[ID]_TORZSCIKK.md`, `general.py --cel torzscikk`)
  a lexikonoldalból renderel, önálló kézi rész nélkül (G7); a törzscikk
  a 【NAPLO...】 folyamat-jelölő blokkokat és a fájl-szintű GENERÁLT-sort
  is eltávolítja (K9: egyik sem jelenhet meg a törzscikkben).

## Mi hiányzik az üzemmenetből ma

Az F8 óta nincs `F8`-jelölt hiány. Nyitva: `NYITOTT_FELADATOK.md` N11, N13, N15 és
az `F8_BRIEF.md` §3 tételei. (N14 lezárva, 2026.09.21.)

A következő igeszakasz kiválasztását a gépi, ütemezett prioritási térkép támogatja (`naplok/GERINC_TERKEP.md`, `eszkozok/gerinc_terkep.py`, GitHub Action); csak jelölt-sűrűséget mutat, a kiválasztás a tanulmány előtt történik.
