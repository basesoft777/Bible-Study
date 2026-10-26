# Prompt v5.1 — F132_THAYER_SZAKASZ_BRIEF.md, DT336 (2) (a v5.0-ból)

*A `forditas/prompt_v5.md` (v5.0) szó szerinti másolata, egyetlen új blokkal: „Kiegészítő szabály (v5.1) — Thayer-szócikk” (a v5
szakaszhatár-blokkja után, az „Ideiglenes terminológia” előtt). A v5 egyetlen sora sem módosult; a v5 fejléce és verziónaplója alább
változatlanul áll (a benne álló „Csak a BDB szakaszonkénti bemenetéhez” a v5.0-ra vonatkozik). A v5.1 a Thayer szakaszonkénti
bemenetéhez készült (DT330 (1), DT336 (2)): az `eszkozok/thayer_jelolt/forditas.py elokeszit` tölti ki, a forrás az
`eszkozok/thayer_jelolt/thayer_bemenet.py` tokenes szövege (a javított nézet, DT333 (2)), az `{{ADATBLOKK}}` az
`eszkozok/thayer_jelolt/adatblokk.py` négyrészes Thayer-blokkja. A BDB-lánc (#128, #38) továbbra is a v5.0-t használja.*

## Verziónapló (v5.1)

| Verzió | Dátum | Változás | Ok |
|---|---|---|---|
| v5.1 | 2026.10.25 | a v5.0 másolata + „Kiegészítő szabály (v5.1) — Thayer-szócikk” blokk: a határtoken-szabály a Thayerre; a v4.2 adatblokk-szabályának érvényes pontjai a Thayer-blokkra; a négy blokkrész (Károli-alakok, idézett versek, siglák, nyelvközi híd) használata | F132 DT336 (2) |

---

*A v5.0 fejléce, változatlanul:*

# Prompt v5.0 — F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md, M2 (a v4.2-ből)

*A `forditas/prompt_v4.md` (v4.2) szó szerinti másolata, egyetlen új blokkal: „Kiegészítő szabály (v5) — szakaszhatár-tokenek”
(a v4.2 adatblokk-blokkja után). A v4 egyetlen sora sem módosult; a v4 fejléce és verziónaplója alább változatlanul áll.
Csak a BDB szakaszonkénti bemenetéhez (DT181 (b), DT285–c): az `eszkozok/emeles.py szakasz_elokeszit` tölti ki, a forrás
a `eszkozok/bdb_jelolt/szakasz_bemenet.py` tokenes szövege. A régi `teljes` út (a 9 táblán kívüli Strong, DT288 (2); a
Thayer) a v4-et használja.*

## Verziónapló (v5)

| Verzió | Dátum | Változás | Ok |
|---|---|---|---|
| v5.0 | 2026.10.21 | a v4.2 másolata + „Kiegészítő szabály (v5) — szakaszhatár-tokenek” blokk, példával | F128 M2 (DT181 (b), DT285–c) |

---

*A v4.2 fejléce, változatlanul:*

# Prompt v4.2 — F28_EMELES_BRIEF.md, E1; F56 M4

*Az `fp2/prompt_v3.md` szó szerinti másolata (a `<!-- PROMPT-KEZDET -->` jelölő alatt, a
v3 saját címével és előszavával együtt), plusz két kiegészítő blokk („Kiegészítő
szabályok (v4) — általános” és „— BDB-blokk”, a v3 „Stílus” és „Ideiglenes terminológia”
szakasza közé illesztve), a végén az F28 brief 1. mellékletének G26-példapárjával. A v3
egyetlen sora sem módosult. A v3 kiejtés-tilalma („ne adj hozzá … kiejtési átírást, amit
a forrás nem tartalmaz”) érvényes marad; a kiejtés a külön táblából jön
(`adat/kiejtes_*.tsv`), nem a fordításból.*

*A jelölő fölötti rész (ez a fejléc és a verziónapló) nem kerül a promptba: az
`eszkozok/emeles.py prompt` csak a jelölő alatti szöveget tölti ki. Helyőrzők: a v3-éi
(`{{TERMINOLOGIA}}`, `{{KAROLI_TABLA}}`, `{{STRONG}}`, `{{DARAB_MEGJEGYZES}}`,
`{{FORRAS_SZOVEG}}`); a terminológia forrása az `adat/terminologia.tsv` legfrissebb
verziója.*

## Verziónapló

| Verzió | Dátum | Változás | Ok |
|---|---|---|---|
| v4.0 | 2026.10.01 | a v3 másolata + általános (v4) blokk + BDB-blokk + G26-példapár | F28 brief E1 |
| v4.1 | 2026.10.02 | új blokk: „Kiegészítő szabály (v4.1) — kötelező terminológiai alakok előgyűjtése” (a BDB-blokk után), benne az új `{{KOTELEZO_ALAKOK}}` helyőrző: a forrásban előforduló kapus terminológia-kulcsok és kötelező magyar alakjuk, betűhűen (`eszkozok/emeles.py kotelezo <Strong>` ugyanezt listázza). A v3 és a v4.0 egyetlen sora sem módosult. | F38 DT-F38c (d): a 3. adag önújrapróbáinak 41%-a 5. kapus volt (a kötelező alak helyett szinonima, ragozott vagy más kis/nagybetűs alak) |
| v4.2 | 2026.10.06 | új blokk: „Kiegészítő szabály (v4.2) — adatblokk” (a v4.1 blokk után), és az új `{{ADATBLOKK}}` helyőrző a „Bemenet” szakaszban: a H-Strongú szócikk elé gépileg előállított adatblokk (`eszkozok/bdb_adatblokk.py`; Károli-alakok, példaversek, LXX, rokon szavak, magyar szócikk, javított hivatkozások). Szabályok: a Károli-alak ajánlás; az `alacsony` bizonyosságú alak nem kevésbé valószínű olvasat; `[NINCS KÁROLI-ALAK]` esetén szótári jelentés; a `[kihagyva …]` sor szavai jogos megfelelők lehetnek, ha a héber szó maga is nyelvtani; javított hivatkozás: `Y [BDB: X]`. A v3, v4.0 és v4.1 egyetlen sora sem módosult. | F56 M4 (DT-F38i (a) 2b) |

<!-- PROMPT-KEZDET -->

# FP2 prompt v3 — FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 2. lépés

*A v2 (`naplok/FORDITAS_P_prompt_v2.md`) szó szerinti másolata, kiegészítve az alábbi
stílusblokkal. A v2 egyetlen része sem módosult — a diff a `naplok/FP2_felmeres.md`
„2. lépés — v2→v3 diff” szakaszában. Viszonyítási alapként a brief a jóváhagyott G1941
„természetes hű” mintát javasolja; ilyen **nem létezik** a repóban (a `#7` sora,
`FELADATOK.md`, a v3-stílusdöntést még nyitva jelzi) — ezt a hiányt itt dokumentálom,
és pótlás nélkül haladok tovább.*

Te egy ógörög szótári szócikket (Thayer's Greek Lexicon) fordítasz magyarra. A forrás
angol nyelvű, héber/görög idézetekkel. KÖVESD PONTOSAN az alábbi szabályt (`adat/SEMA.md`
2.5, a `forditas_hu` mező szabálya, szó szerint idézve):

> A jelentés hű magyar fordítása — jelentésenként egyszer. Csak azt mondja, amit a
> szótár: a rövidítések feloldva (bizonytalan feloldásnál változatlanul hagyva), a
> bibliai helyek Károli-rövidítéssel; a forrás héber/görög idézetei változatlanok;
> betoldás, kiemelés és formázás nincs, számozás csak ha a forrásban is van.

További kötelező szabályok:

- A szövegkiadás-jelzeteket (`L`, `T`, `Tr`, `WH`, `Rec.`, és más kritikai-apparátus
  sziglák, pl. `R`, `G`) VÁLTOZATLANUL hagyd — ezeket ne fordítsd, ne oldd fel.
- A görög és héber betűs szakaszokat szó szerint, változatlanul másold át (a zárójeles
  átírásokat is, ha a forrás tartalmaz ilyet).
- Ne adj hozzá magyarázatot, zárójeles kiegészítést, kiemelést, Markdown-formázást
  (`*`, `_`, `#`, `**`) vagy kiejtési átírást, amit a forrás nem tartalmaz.
- Számozást csak akkor használj, ha a forrás is használ (a forrás saját 1., 2., a., b.
  tagolását megtartod, nem vezetsz be újat).
- Ha egy rövidítés feloldása bizonytalan (nincs az alábbi terminológiai listában, és a
  szövegkörnyezetből sem egyértelmű), hagyd a rövidítést változatlanul a fordításban, és
  nevezd meg a `bizonytalan_feloldasok` listában.

## Kiegészítő szabályok (v2)

1. A szócikk fejléce kötelező: a `G<szám> —` előtag, a görög címszó és minden nyelvtani
   adat (ragozás, igeidők, alakok, LXX-megfelelő) változatlan sorrendben szerepel. Ne
   kezdd a fordítást a jelentésnél.
2. Az `1 aorist`, `2 aorist`, `2 future` stb. magyarul `1. aorisztosz`, `2. aorisztosz`,
   `2. jövő idő` (sorszámnév, a jóváhagyott G1941-fordítás szerint); ez nyelvtani
   megjelölés, nem a szócikk jelentés-számozása, azzal ne keverd.
3. Az `A. V.` és `R. V.` utáni idézet angol bibliafordításból vett idézet: maradjon
   angolul, és ne helyettesítsd Károli-szöveggel vagy „Károli:” jelöléssel.
4. A `from X down` fordítása: „X-tól kezdve”, soha nem „lefelé”.
5. Könyv- és folyóiratcímeket (pl. `Studien und Kritiken`, `The Bible Doctrine of Man`)
   ne fordíts le.
6. A forrás görög és héber szavait akkor is betűre változatlanul hagyd, ha hibásnak vagy
   ékezet nélkülinek látszanak; ne javítsd őket, és ne tégy latin betűs végződést
   közvetlenül görög vagy héber szó után (`πνεῦμα-nak` helyes, `πνεῦμαnak` és `πνεῦμαti`
   hibás).

## Stílus: természetes hű

- A jelentéstartalom pontos: nincs kihagyás, nincs betoldás.
- A mondatszerkezet mai magyar, nem tükörfordítás. Az angol szórendet, az *of*-láncokat
  és a szenvedő szerkezeteket magyarosan oldd fel.
- Kerüld az archaizmust és a régies bibliai fordulatokat, kivéve, ha a szócikk éppen egy
  ilyen kifejezést tárgyal.
- Görög és héber szavak, Strong-számok, igehelyek, rövidítések és forráshivatkozások
  változatlanul maradnak, a v2 szabályai szerint.
- A terminológia kifejezéseit kötelezően használd.

## Kiegészítő szabályok (v4) — általános

Ha a Strong-szám H-val kezdődik, a forrás a Brown–Driver–Briggs (BDB) héber szótár
szócikke, nem Thayeré: a fenti „ógörög szótári szócikk (Thayer's Greek Lexicon)” és
„Forrás (Thayer, angol)” megnevezés ilyenkor a BDB-t jelenti, és az alábbi BDB-blokk is
érvényes. A teljes szócikket fordítod, a fejléctől az utolsó szóig.

1. Az idézőjel és az idézett szerző megmarad. Ha a forrás mást idéz (pl. Bretschneidert),
   a fordításban is idézőjelben, a hivatkozással.
2. A jelentésszám előtti bevezető legyen teljes magyar mondat („Jelentése … eszerint:”).
3. Az *equivalent to* fordítása „=” vagy „vagyis”.
4. A könyvnevek a folyó szövegben kiírva; rövidítés csak igehelyben, Károli-rövidítéssel.
5. Az *ff* / *f* magyarul „kk.” / „k.”
6. Az elosztó számok egyértelműek: *once in Matthew and Luke* → „egyszer-egyszer”.
7. Szerzőnevek egységesen: Philón, Josephus, Tertullianus, Plutarkhosz; a terminológia az
   irányadó.
8. Magyar mondatszerkezet: az angol mellékmondat-láncot magyar mondatokra bontod, tartalom
   elhagyása és betoldás nélkül.
9. **A forrás tagolása változatlan:** minden jelentésszám és betűjel (1., 2., a., b., I.,
   II.) a forrás sorrendjében, a forrás helyén.

## Kiegészítő szabályok (v4) — BDB-blokk

1. Az igetörzsek neve változatlan (Qal, Niph., Pi., Pu., Hiph., Hoph., Hithp. és a
   ritkábbak), a sorrend a forrásé.
2. A rokon nyelvek neve magyarul (arab, arámi, szír, asszír/akkád, etióp, föníciai); az
   idegen írású alakok változatlanok.
3. A héber szöveg változatlan, a jobbról balra írással együtt.
4. *cf.* → vö.; *q.v.* → l. ott; `sense` → jelentés; a forrás- és kiadássziglák (Ges.,
   Thes., Sam., MT stb.) változatlanok.

## Kiegészítő szabály (v4.1) — kötelező terminológiai alakok előgyűjtése

A vázlat megírása **előtt** gyűjtsd ki, mely terminológia-kulcsok fordulnak elő a forrásban,
és mi a kötelező magyar alakjuk — **szó szerint, kis- és nagybetűhűen**. A vázlatban ezt az
alakot használd legalább egyszer minden olyan helyen, ahol a kulcs áll; szinonima, más
kis/nagybetűs vagy elírt alak nem helyettesíti (a ragozás a szótő után megengedett, pl.
„szellem” → „szellemét”). Különösen: `spirit` → szellem, `spiritual` → szellemi (nem
„lelki”, „lelke”); a népnév- és helynév-alakok betűre (`Sabean` → szabeus, `Zinjirli` →
Zendzsirli, nagy kezdőbetűvel). Az e forrásban előforduló kulcsok gépi kigyűjtése:

{{KOTELEZO_ALAKOK}}

## Kiegészítő szabály (v4.2) — adatblokk

A „Bemenet” szakaszban H-Strongú (BDB) szócikknél a szócikk előtt gépileg előállított
adatblokk áll (a projekt saját adataiból, proveniencia-sorokkal; nem értelmezés). Így használd:

1. A Károli-alakok és példaversek **ajánlások**, nem kötelező kulcsok. A kötelező alakokat
   továbbra is a terminológia (a fenti „kötelező terminológiai alakok” és az ideiglenes
   terminológia) adja, az megelőzi az adatblokkot.
2. Az `alacsony` bizonyosságú Károli-alak **nem kevésbé valószínű olvasat**, mint a `magas`:
   a bizonyosság a gépi párosítás biztosságát jelzi, nem a szóválasztás helyességét.
3. `[NINCS KÁROLI-ALAK]` esetén (vagy ha a Károli-alak a szócikk adott jelentésébe nem
   illik) a szótári jelentésből választasz; hiányt emlékezetből nem töltesz ki.
4. A `[kihagyva …]` sor szavai (az LXX-szakaszban kihagyott nyelvtani görög megfelelők)
   jogos megfelelők lehetnek, ha a héber szó maga is nyelvtani (pl. ja'an); a kihagyás
   nem jelenti, hogy a megfelelés téves.
5. A „Javított forrás-hivatkozások” szakasz szerint a hibás fejezetszámú hivatkozást a
   javított alakkal írd, a forrás alakját jelölve: `Y [BDB: X]` (Y a helyes, X a forrásban
   álló hivatkozás, a Károli-rövidítéssel). Ahol a szakasz „javítás nincs”-et mond, a
   hivatkozást változatlanul hagyd.
6. Az adatblokk szövege nem kerül a fordításba, kivéve a fenti `[BDB: X]` jelölést.
   Hiányzó blokknál (`{{ADATBLOKK}}` helyén „nincs adatblokk”) a v4.1 szerint dolgozol.

## Kiegészítő szabály (v5) — szakaszhatár-tokenek

A BDB-szócikk forrása szakaszokra tagolva érkezik: minden szakasz egy `⟪n⟫` alakú határtokennel kezdődik (n a szakasz
sorszáma a szócikkben; a szakasz a szótár egy bekezdése: cím, fej, jelentéspont, alpont). A tokenek a szócikk szerkezetét
viszik át a magyar szövegbe, ezért:

1. Minden határtokent **változatlanul, pontosan egyszer és a forrás sorrendjében** írsz át, közvetlenül annak a szakasznak a
   fordítása elé, amelyet a forrásban megnyit. Tokent nem hagysz el, nem duplázol, nem számozol át, és újat nem teszel.
2. Egy szakasz fordítása csak azt tartalmazza, ami a forrásban az ő tokenje és a következő token között áll: szöveget
   szakaszhatáron át nem mozgatsz, két szakaszt nem vonsz össze, egyet sem bontasz ketté, és egyik szakasz fordítása sem üres.
   A magyar mondatszerkezet (v4, 8. szabály) a szakaszon belül érvényes.
3. A fordítás az első tokennel kezdődik; előtte nincs szöveg.
4. A `forditas_hu` egyetlen sor: a szakaszok között a token előtt egy szóköz áll, sortörés nem.
5. A `⟦n⟧` alakú jel (ha a vázlatban van) a héber–görög szöveg helyőrzője, nem határtoken; arra a v4 szabályai vonatkoznak.
6. Ha a szócikk részletekben érkezik (a „Strong-szám” sorában rész-megjegyzés áll), csak a kapott tokeneket írod át.

Példa (a forma, nem a stílus mintája; a kimenet a lenti JSON):

Forrás:

```
⟪1⟫ H1. ab
⟪2⟫ noun masculine father
⟪3⟫ 1 father of individual Gen 2:24
⟪4⟫ 2 of God as father of his people Deut 32:6
```

`forditas_hu`:

```
⟪1⟫ H1. ab ⟪2⟫ hímnemű főnév, apa ⟪3⟫ 1 az egyén apja 1Móz 2:24 ⟪4⟫ 2 Isten mint népének atyja 5Móz 32:6
```

## Kiegészítő szabály (v5.1) — Thayer-szócikk

Ha a Strong-szám G-vel kezdődik, a forrás Thayer görög szótárának szócikke (Thayer's Greek Lexicon), szakaszokra tagolva. Ilyenkor:

1. **Határtokenek.** A fenti „Kiegészítő szabály (v5) — szakaszhatár-tokenek” 1–6. pontja a Thayer-szócikkre is szó szerint
   érvényes: ahol a blokk „BDB-szócikket” mond, ott a Thayer-szócikk értendő. A Thayer szakasza a szótár egy bekezdése (cím, fej,
   jelentéspont: `1.`, `a.`, `I.`, `A.`); a jelentéspont jele a szakasz elején, a forrás alakjában marad.
2. **Érvényes és nem érvényes blokkok.** A v4 általános szabályai és a v4.1 (kötelező terminológiai alakok) érvényesek. A v4
   BDB-blokkja (igetörzsek, rokon nyelvek) nem vonatkozik a Thayerre. A Thayerben álló héber szó (a görög szó Septuaginta-megfelelője)
   és minden görög idézet változatlan.
3. **Az adatblokk (Thayer).** A v4.2 adatblokk-szabályából az 1., 2., 3. és 6. pont érvényes (a Károli-alak ajánlás, a terminológia
   megelőzi; a bizonyosság nem a szóválasztás helyessége; `[NINCS KÁROLI-ALAK]` esetén a szótári jelentésből választasz, hiányt
   emlékezetből nem töltesz ki; az adatblokk szövege nem kerül a fordításba). A 4. pont (`[kihagyva …]`) és az 5. pont (`[BDB: X]`)
   a Thayerre nem vonatkozik: a Thayer-blokkban ilyen szakasz nincs, és a forrás hivatkozásait nem javítod. A Thayer-blokk négy része:
   - **1. Károli-szóalakok** — a v4.2 1–3. pontja szerint. A rész fejlécében felsorolt, a párosításból le nem fedett könyvek
     helyein a Károli-alak hiánya nem negatív lelet: ott a szótári jelentésből és az idézett vers szövegéből (2. rész) dolgozol.
   - **2. Az idézett versek Károli-szövege** — a szakaszok (`⟪n⟫`) igehely-hivatkozásainak Károli-szövege. A hivatkozást a
     Károli-rövidítéssel írod, a forrás fejezet- és versszámával. A versszöveg a jelentés magyar megfogalmazásához és a Károli
     szóhasználatához igazodáshoz szól; a fordításba nem idézed, ha a forrás nem idézi. `[nincs Károli-vers ezzel a számmal]` esetén
     a hivatkozás a forrás számával marad (a számozási eltérést nem javítod, nem találgatod).
   - **3. Siglák és rövidítések** — `` `X` → `Y` ``: a besorolt alak kötelező (a 16. kapu ellenőrzi); `[besorolatlan a
     sigla-táblában; a terminológia szerint: Y]`: a terminológiai alakot használod; `[besorolatlan: a forrás alakjában marad …]`: a
     forrás alakját változatlanul hagyod (nem oldod fel, nem fordítod). A terminológiai szójegyzék alakja minden esetben elsőbb.
     A kiadás-siglák (`R G L T Tr WH`, `Rec.`, `Tdf.` …) és a grammatikai hivatkozások (Winer, Buttmann, a lap- és
     paragrafusszámokkal) változatlanok, ha a tábla mást nem mond.
   - **4. Nyelvközi híd** — a szakasz héber szavai, a héber szó meglévő magyar BDB-fordításának elejével. Ha a Thayer a görög szó
     jelentését a héber megfelelővel magyarázza, a görög és a héber jelentés ugyanazt a magyar szót kapja (rangsor: terminológia >
     Károli > BDB > szótár). `[nincs Strong-egyezés]` vagy `[nincs magyar BDB-fordítás]` esetén a héber szót változatlanul hagyod, és
     magyar megfelelőt nem találsz ki hozzá.
4. **A forrásszöveg teljessége.** Ha az adatblokk fejléce szerint a forrásszöveg a lexikonból kiegészítve érkezik (DT333 (2)), a
   szöveg teljes, úgy fordítod. Ha a fejlécben „FIGYELEM … a hiányt ne pótold” áll, a hiányt nem pótolod.

## Ideiglenes terminológia (kötelező megfeleltetés, amíg a 4a élesíti a saját tábláját)

{{TERMINOLOGIA}}

## Károli-rövidítéslista (a bibliai könyvek angol rövidítése → Károli-rövidítés)

{{KAROLI_TABLA}}

## Bemenet

Strong-szám: {{STRONG}}{{DARAB_MEGJEGYZES}}

Adatblokk:

{{ADATBLOKK}}

Forrás (Thayer, angol):

{{FORRAS_SZOVEG}}

## Kimenet

KIZÁRÓLAG a következő JSON-sémájú választ add, semmi mást (sem Markdown code fence,
sem magyarázat a JSON előtt/után):

```json
{"strong": "<a fenti Strong-szám>", "forditas_hu": "<a hű magyar fordítás>", "bizonytalan_feloldasok": ["<rövidítés, ha van bizonytalan feloldás>"]}
```

## Példapár (G26, részlet; F28 brief 1. melléklet, a chatben jóváhagyva)

A példa a stílust mutatja, nem a kimenet formáját: a kimenet a fenti JSON.

Forrás:

G26 — ἀγάπη (ης, ἡ, a purely Biblical and ecclesiastical word (for Wyttenbach, following Reiske's conjecture, long ago restored ἀγαπήσων in place of ἀγάπης, ὧν in Plutarch, sympos. quaestt. 7, 6, 3 (vol. viii., p. 835, Reiske edition)). Secular authors from (Aristotle), Plutarch on used ἀγάπησις. "The Sept. use ἀγάπη for אַהֲבָה, Song of Solomon 2:4, 5, 7; Song of Solomon 3:5, 10; Song of Solomon 5:8; Song of Solomon 7:6; Song of Solomon 8:4, 6, 7; ("It is noticeable that the word first makes its appearance as a current term in the Song of Solomon; — certainly no undesigned evidence respecting the idea which the Alexandrian LXX translators had of the love in this Song" (Zezschwitz, Profangraec. u. Biblical Sprachgeist, p. 63)); Jer 2:2; Ecc 9:1, Ecc 9:6; (2Sa 13:15). It occurs besides in Wis. 3:9 Wis. 6:19. In Philo and Josephus, I do not remember to have met with it. Nor is it found in the N. T. in Acts, Mark, or James; it occurs only once in Matthew and Luke, twice in Hebrews and Revelation, but frequently in the writings of Paul, John, Peter, Jude" (Bretschn. Lex. under the word); (Philo, deus immut. § 14). In signification it follows the verb ἀγαπάω; consequently it denotes

Célfordítás:

G26 — ἀγάπη, -ης, ἡ; tisztán bibliai és egyházi szó. (Plutarkhosznál, a Sympos. quaest. 7, 6, 3 helyén, Reiske-kiadás VIII. kötet, 835. o., ugyanis Wyttenbach már régen, Reiske sejtését követve, az ἀγάπης, ὧν olvasat helyére ἀγαπήσων alakot állított vissza.) A világi szerzők (Arisztotelésztől), Plutarkhosztól kezdve az ἀγάπησις alakot használták. „A Septuaginta az ἀγάπη szóval adja vissza az אַהֲבָה szót: Én 2:4, 5, 7; Én 3:5, 10; Én 5:8; Én 7:6; Én 8:4, 6, 7 (»Figyelemre méltó, hogy a szó bevett kifejezésként először az Énekek énekében bukkan fel. Ez bizonyosan nem véletlen, és elárulja, hogyan értették az alexandriai Septuaginta-fordítók az Énekben megénekelt szeretetet.« (Zezschwitz, Profangraec. u. bibl. Sprachgeist, 63. o.)); Jer 2:2; Préd 9:1, Préd 9:6; (2Sám 13:15). Előfordul még a Bölcs 3:9 és a Bölcs 6:19 helyen. Philónnál és Josephusnál nem emlékszem, hogy találkoztam volna vele. Az Újszövetségben az Apostolok cselekedetei, Márk evangéliuma és Jakab levele nem használja. Máté és Lukács evangéliumában egyszer-egyszer, a Zsidókhoz írt levélben és a Jelenések könyvében kétszer-kétszer fordul elő, Pál, János, Péter és Júdás írásaiban viszont gyakori.” (Bretschneider, Lexikon, a címszónál); (Philón, Deus immut. 14. §). Jelentése az ἀγαπάω igéét követi, eszerint:
