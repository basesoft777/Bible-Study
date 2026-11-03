# Prompt glossza v2 — F161_GLOSSZA_LANC_BRIEF.md (a v1-ből: kiegészítő szabály a UBS-definíciókra)

*Rögzítve: 2026-11-03, az éles futás előtt. A lánc (`eszkozok/glossza_api_koteg.py`) a `<!-- PROMPT-KEZDET -->` jelölő utáni szöveget
küldi, a helyőrzők kitöltésével; ugyanez a szöveg megy a Batch API-ra és az előfizetői subagentnek (bájtra azonos
kérés, `szaraz` → `keresek.jsonl`). Az első próba után a szöveg nem változik: változtatás csak új verzióként
(`prompt_glossza_v2.md`), naplózva.*

## Verziónapló

- v1 (2026-11-03, F161): az első változat. Forrása a v5.2 (`forditas/prompt_v5_2.md`) azon szabályai, amelyek egy
  rövid glosszára értelmezhetők: SEMA 2.5 hű fordítás, terminológia (v4.1: kötelező alakok betűhűen), tiltott
  fordulatok, a görög/héber szó és a ⟦n⟧ helyőrző érintetlen, a forrás idézőjelei (v5.2). Új: glosszaelemenként egy
  magyar megfelelő (az elemszám a forrásé), szótári alak, mankó (Károli-alakok, elfogadott egyenértékek), az olvasói
  kapu tiltásai (angol maradék, belső jel), egységenkénti JSON-kimenet.

<!-- PROMPT-KEZDET -->

Bibliai szótárak rövid angol glosszáit fordítod magyarra egy magyar nyelvű bibliai lexikon számára. A glossza egy
szótári jelentés néhány szavas megadása (pl. `demon; evil spirit`), nem folyó szöveg. Minden egységet önállóan
fordítasz; a kontextus csak a jelentés megértését segíti.

A források: UBS Dictionary of the Greek New Testament (UBS DNTG; Louw–Nida-doménekkel), UBS Dictionary of Biblical
Hebrew (UBS DBH), Translator's Brief lexicon of Extended Strongs for Greek (TBESG, rövid jelentés).

## A fordítás szabálya

Az `adat/SEMA.md` 2.5 szabálya: a jelentés hű magyar fordítása. Csak azt mondja, amit a szótár; betoldás, kiemelés és
formázás nincs; a forrás görög és héber szavai változatlanok.

1. **Csak a „Fordítandó” sort fordítod.** A kontextus (címszó, domén, definíció, mankó) nem kerül a kimenetbe.
2. **Elemenként.** A forrás „;”-vel elválasztott elemeit a forrás sorrendjében, elemenként egy magyar megfelelővel adod
   vissza, „; ” elválasztással. Az elemszám pontosan a forrásé: nem vonsz össze, nem bontasz szét, nem hagysz ki és nem
   teszel hozzá elemet. Ha két elem magyarul azonos szóra jönne ki, a második elemnél a forrás árnyalatát keresd.
3. **Szótári alak.** Főnév alanyesetben, melléknév alapfokban, ige főnévi igenévvel (`to die` → meghalni, `to be humble`
   → alázatosnak lenni). Az angol névelő nem kerül át (`a human` → ember). A `someone`, `oneself`, `one's` magyarul
   valakit/valakinek, magát/önmagát, saját (vagy a magyar szerkezet szerint); a magyar szórend természetes.
4. **Zárójeles pontosítás.** A forrás zárójeles megszorítása magyarul, zárójelben, ugyanazon az elemen marad. Zárójelet
   magadtól nem teszel.
5. **Terminológia (kötelező).** Az alábbi listában szereplő angol kulcs kötelező magyar alakját betűhűen, kis- és
   nagybetűhűen használod (a ragozás a szótő után megengedett). Különösen: `spirit` → szellem, `Spirit` (Isten Lelke)
   → Szellem, `Holy Spirit` → Szent Szellem, `spiritual` → szellemi (nem „lelki”), `soul` → lélek. A „Szentlélek”
   alakot nem használod.
6. **Tiltott fordulatok.** Tükörfordítás nincs; a `surname` nem „melléknév”, a `to put a name upon` nem „nevet tenni
   valakire”.
7. **Görög, héber, helyőrző.** A forrás görög és héber szavai ⟦n⟧ helyőrzőként érkeznek; minden helyőrzőt pontosan
   egyszer, változatlanul, a forrás sorrendjében átveszel. Görög vagy héber szót magadtól nem írsz, és átírást
   (kiejtést) nem teszel hozzá.
8. **Idézőjel.** Glosszára idézőjelet nem teszel. Ha a forrásban ASCII-idézőjeles (`"…"`) idézet áll, magyarul `„…”`,
   a párok száma egyezik; egyenes `"` a kimenetben nem lehet.
9. **Olvasói tiltások.** A kimenetben nem maradhat angol szó (sem a forrás szava, sem angol névelő, elöljáró vagy
   kötőszó: `the`, `of`, `to`, `and`, `or`, `one's` …), és nem lehet benne belső jel (fájlnév, Strong-szám,
   döntés- vagy feladatazonosító, `manual`, Markdown-jel `*`, `_`, `#`). Igehely nincs a glosszákban; ha mégis van,
   Károli-rövidítéssel (`1Móz 3:16`, `Mt 24:38`).
10. **Mankó.** Az egységnél álló mankó javaslat, nem kötelező, és a terminológia fölötte áll (rangsor: terminológia >
    elfogadott egyenérték > Károli-alak). A „Károli-alakok” a szó Károli-fordításbeli leggyakoribb alakjai; ha a glossza
    jelentése megengedi, ezekből válassz. Az „elfogadott egyenérték” a lexikonban ugyanerre az angol elemre már
    jóváhagyott magyar alak; ugyanazt a jelentést ugyanazzal a magyar szóval add vissza. Héber és görög szó azonos
    jelentésére azonos magyar szó áll.
11. **Bizonytalanság.** Ha egy rövidítés vagy elem jelentése a kontextusból sem egyértelmű, a legvalószínűbb hű
    fordítást adod, és az angol elemet a `bizonytalan_feloldasok` listában megnevezed.

## Kiegészítő szabály (v2) — UBS-definíció

Ha az egység mezője „definíció”, a „Fordítandó” sor a szótár meghatározása, nem glossza. Ilyenkor:

1. A 2. szabály (elemszám) nem vonatkozik rá: a meghatározást hű, természetes magyar mondatrészként adod vissza,
   tartalom elhagyása és betoldás nélkül; az angol tagmondat-láncot magyarosan oldod fel.
2. **A UBS jelei a helyükön, változatlanul:** `=` (a meghatározás kezdete), `≈` (tágabb jelentés), `◄` és `►`
   (kiegészítő megjegyzés), „;” a részek határán. Új jelet nem teszel, meglévőt nem hagysz el.
3. `literally: X; hence:` → „szó szerint: X; innen:”; `plural with singular meaning:` → „többes szám egyes jelentéssel:”;
   `plural with plural meaning:` → „többes szám többes jelentéssel:”; `see` → „l.”.
4. **A hivatkozás-jelölés betűre változatlan:** a `{L:…<SDBH:…>}` (és `{L:…}`) szerkezetet a benne álló névvel és
   héber alakkal együtt pontosan átmásolod (pl. `◄ territory of {L:Naphtali<SDBH:⟦1⟧>}` → `◄ {L:Naphtali<SDBH:⟦1⟧>} területe`);
   a magyar mondatrész a jelölés köré épül.
5. A meghatározás leíró szavaira is a terminológia és az olvasói tiltások érvényesek (angol szó a jelölésen kívül nem maradhat).

## Terminológia (a kérés forrásaiban előforduló kötelező kulcsok)

{{TERMINOLOGIA}}

## Egységek

{{EGYSEGEK}}

## Kimenet

KIZÁRÓLAG a következő JSON-objektumot add vissza, semmi mást (sem Markdown code fence, sem magyarázat előtte vagy
utána). Minden egység pontosan egyszer, a fenti sorrendben, az `id`-jével:

{"egysegek": [{"id": "<az egység azonosítója>", "forditas_hu": "<a magyar glossza>", "bizonytalan_feloldasok": []}]}
