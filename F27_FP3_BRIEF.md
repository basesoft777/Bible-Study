---
feladat: 27
cim: "Thayer-fordítás Sonnettel: felmérés és mérő adag a BDB-menet szerint"
kod: FP3
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: "a Thayer Sonnet-fordításának mért alapja a #7-hez: az eszközlánc Thayer-hiányai, gyakorisági sorrend és adagterv, egy kb. 150 ezer karakteres mérő adag az adat/forditasok.tsv-ben (allapot=sonnet), aranyminta-összevetés, keretmérés és kivetítés a teljes Thayerre"
kovetkezo: "halasztva (D46): a #7-tel együtt veszi elő a felhasználó; a v2 (DT121) szerint csak Sonnet, a BDB-menet (#38) mintájára"
olvas: [F38_BDB_FORDITAS_BRIEF.md, naplok/BDB_FORDITAS_naplo.md, naplok/EMELES_naplo.md, konkordancia/Thayer_teljes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/SEMA.md, adat/karoli_strong/, forditas/prompt_v4.md, eszkozok/emeles.py, eszkozok/normalizal.py, eszkozok/forditas_kapuk.py, DONTESEK.md]
ir: [adat/forditasok.tsv, naplok/FP3_naplo.md, naplok/FP3_sorrend.tsv, naplok/FP3_hibas.tsv, naplok/FP3_M0.py, naplok/FP3_arany.md, DONTESEK.md]
fugg: []
---

# F27_FP3_BRIEF.md — Thayer-fordítás Sonnettel: felmérés és mérő adag a BDB-menet szerint

*FELADATOK #27 · Modell: sonnet · v2 · 2026.10.12 · a #7 (Thayer éles) briefjét készíti elő*

**Módosítva (2026.10.12, DT121): csak Sonnet.** Az Opus–Gemini összevetés és a Max-keret mérése (v1) elmarad. A Thayer ugyanazzal a modellel és menettel fordul, mint a BDB (#38, DT-F38e): Sonnet, egy végrehajtó, a #28 eszközlánca, kapuk és normalizáló, adagonként megállás. Ez a feladat a BDB-menet M0-ját és M1-ét végzi el a Thayeren. A teljes futás (M2 … Mn, Mz) a #7 dolga; annak briefje ennek az eredményéből készül.

## 1. Cél

Két kérdésre ad mért választ:

1. **Alkalmasság:** a BDB-hez kiérlelt eszközlánc (prompt v4.x, helyőrző, javítóréteg, 1–13. kapu, normalizáló, terminológia v3) mennyire viszi a Thayert változtatás nélkül, és hol kell hozzányúlni?
2. **Mennyiség:** egy mérő adag alapján mennyi keretet és időt kíván a teljes Thayer (5 426 szócikk, 4,44 millió karakter) Sonnettel?

A #7 fejlécéhez és csonkjához ez a feladat nem nyúl.

## 2. Hatókör

**Benne van:** M0 felmérés (csak olvas és mér), M1 mérő adag (kb. 150 000 forráskarakter, Sonnet, `allapot=sonnet`), aranyminta-összevetés, keretmérés, jelentés, döntési tétel.

**Nincs benne:** más modell (Opus, Gemini, OpenRouter); az M1 utáni adagok; az `F07_THAYER_ELES_BRIEF.md` módosítása; új eszköz vagy kapu fejlesztése; a `kezi` és az `opus` Thayer-sorok (14 sor) módosítása; a forrás javítása.

## 3. Kiinduló tények (a BDB-menetből és a #28-ból; a menet újraméri, eltérésnél a saját mérése az irányadó, és naplózza)

| Tétel | Érték |
|---|---|
| Thayer | 5 426 szócikk, 4 440 084 karakter; 85 szócikk 6 000, 10 szócikk 20 000 karakter fölött (a leghosszabb 34 670) |
| Hosszkategóriák (FP2) | rövid ≤ 300; közepes 300–2000; hosszú > 2000 karakter |
| Kész Thayer-sor | 14 `teljes` (5 `kezi`: G1941, G1944, G5590, G0282, G4151; 9 `opus`) — kimaradnak |
| BDB-mérés (#38 M4) | kb. 2,6 token / forráskarakter a teljes session-rezsivel, kontextusszámlálóból (nem számlázott token); kimenet/forrás 1,02–1,07 |
| Eszközlánc Thayer-támogatása | `forditas_kapuk.py --szotar Thayer`; a 10. kapu (igetörzs) csak BDB; a `normalizal.py` Thayer-ága: `kk_k`, `szerzonevek`, `igehely_rov`, `konyvnevek`, külön `FORRAS_ALIAS`-ág; az `Esdr.` alias hiányzik (107 előfordulás); az `emeles.py` adatblokkja csak H-Strongra készül, ezért a Thayer Károli-alakot nem kap |
| Prompt | `forditas/prompt_v4.md`: a törzs eredetileg Thayer-prompt (FP2 v3, G26 példapár); a v4.1 (kötelező alakok) és a v4.2 (adatblokk) BDB-re szól |
| Hivatkozásformák | STEPBible-alak (`Mat 5:43ff`, `1Jo 4:7f`, `Wis. 3:9`, `Song of Solomon 2:4`); kritikai sziglák (`L T Tr WH`); klasszikus szerzők c:v nélkül (Herodotus, Xenophon, Josephus); `1 Cor. 20, 5` = Római Kelemen, nem bibliai hely |

## 4. Lépések

### M0 — Felmérés (csak olvas és mér; `naplok/FP3_M0.py`, eredmény a `naplok/FP3_naplo.md`-be)

1. **Eszközlánc-próba szárazon.** A BDB szócikkenkénti lánca (`emeles.py kotelezo` → `helyorzo` → vázlat → `ellenoriz` → `rogzit` → `beir`, utána a normalizáló) G-Strongon lépésenként: melyik lépés fut változtatás nélkül, melyik ad hibát vagy üres eredményt. Próbaanyag: a 14 kész Thayer-sor forrása (a meglévő fordítás a kapukon: hány jelzés, melyik kapun). Táblázat: lépés · fut-e · eltérés.
2. **Könyv- és hivatkozásfedés.** A Thayer igehely-előtti könyvalakjai közül melyiket nem képezi le a `Konyv_normalizalo_tabla.tsv` és a `normalizal.py` (a BDB-menet „nem leképezett könyvalakok” mérése mintájára, `naplok/BDB_FORDITAS_naplo.md` F38.13). Külön sor: `Esdr.`, a Kelemen-hivatkozás, a klasszikus szerzők.
3. **Terminológia.** Az `adat/terminologia.tsv` görög/Thayer-releváns sorai; a Thayer leggyakoribb angol szakkifejezései közül melyiknek nincs sora (javaslatlista, a fájl nem változik).
4. **Sorrend** (`naplok/FP3_sorrend.tsv`: `sorszam`, `strong`, `gyakorisag`, `karakter`, `adag`). Károli ÚSZ Strong-gyakoriság szerint csökkenő (`adat/karoli_strong/` ÚSZ-könyvei; ha valamelyik ÚSZ-könyv párosítása hiányzik, a TAGNT a tartalék, és ez a naplóba kerül). Egyenlőségnél a Strong-szám. A kész 14 sor kimarad.
5. **Szegmenshatárok** a 20 000 karakter fölötti szócikkekre, jelentésszámok mentén (ahogy a #28 a G4151-nél).
6. **Adagterv:** M1 kb. 150 000 karakter, utána kb. 500 000 karakteres adagok (a #7-nek). A Károli-lefedettségi feltétel (DT56) a mai eszközzel a Thayerre nem értelmezhető, mert az adatblokk csak H-Strongra készül; az M0 ezt rögzíti, és a ⛔ M1 tételébe kérdésként viszi (kell-e G-adatblokk a #7 előtt).

**Megállás az M0 után csak akkor**, ha az 1. pont szerint a lánc valamelyik lépése G-Strongon nem fut (blokkoló hiány). Ekkor ⛔: jelentés, és a felhasználó dönt (eszközjavítás külön feladatban, vagy leállás). Egyébként az M1 azonnal indul.

### M1 — Mérő adag

1. **Keret-alapállapot ⛔:** a felhasználó leolvassa a keretet (kredit vagy `/usage`, ahol a session fut) — ez az egyetlen indulás előtti várakozás. Az M1 alatt más Code-munka ne fusson.
2. Az első kb. 150 000 forráskarakter fordítása a BDB-menet szerint (l. 5. pont), szócikkenként; `emeles.py rogzit --modell claude-sonnet-5-5`, `allapot=sonnet`.
3. **Aranyminta** (`naplok/FP3_arany.md`): az 5 `kezi` Thayer-szócikket (G1941, G1944, G5590, G0282, G4151) a menet ugyanígy lefordítja, **csak a naplóba**, az `adat/forditasok.tsv`-be nem írja. Szócikkenként forrás, `kezi` és Sonnet egymás alatt, a kapueredmény, és a feltűnő eltérések felsorolása (ítélet nélkül).
4. **Keret-záróállapot ⛔:** a felhasználó újra leolvassa. A jelentésbe a session kontextusszámlálója is bekerül (a BDB M4 mértékegységével összevethetően).
5. **Kivetítés** a teljes Thayerre hosszkategóriánként, a mért adagból, a valódi szócikkhosszakkal (nem átlag × darabszám; a F21 PD4 tanulsága). Ablak- vagy keretújraindulás jelölve, becslés nem kerül mért érték helyére.

### ⛔ M1 — Jelentés és döntés

A szokásos adagjelentésen felül (`naplok/FP3_naplo.md`):
- az adag szócikkszáma, karakterszáma, kapueredmények kapunként, az önújrapróbák és a hibás lista (`naplok/FP3_hibas.tsv`: strong, kapu, szegmens, ok) összesítése, külön a BDB M2-elemzés kategóriái szerint (téves riasztás / valódi hiba);
- 5 véletlen szócikk (seed = 27, hossz szerinti harmadokból) forrás és fordítás egymás alatt, hogy a felhasználó beleolvashasson;
- az aranyminta-összevetés;
- a keretmérés és a kivetítés;
- egy `DONTESEK.md`-tétel (`DT-F27b`) a felhasználó döntéseivel: (a) a #7 indulhat-e ezzel a lánccal, (b) a M0-ban talált hiányok közül mit kell a #7 előtt javítani (normalizáló-alias, terminológia, prompt-blokk a Thayerre, G-adatblokk), külön feladatként vagy a #7 M0-jában, (c) a D46-halasztás feloldása.

## 5. Szabályok a BDB-menetből (#38) és a #28-ból

- **Egy session = egy ág = egy PR.** Ágnév: `claude/f27-fp3`.
- **Egy végrehajtó, egy kontextus, subagent nélkül** (a terminológia egysége; a párhuzamos futtatás elvetve, DT56).
- **A modellcímke a valódi modell** (`--modell` kötelező; a BDB-ben a hamis `opus` alapérték három javítókört okozott).
- **A prompt, a terminológia és a kapuk futás közben nem változnak.** Javítás csak a ⛔ M1 után, jóváhagyással; az M1 sorait ez nem fordítja újra, csak ha a felhasználó kéri.
- **Kapuhiba:** egy önújrapróba; ha az sem megy át, a szócikk a hibás listára kerül, és a futás továbbmegy.
- **Kis/nagybetű:** az 5. kapu csak kis/nagybetű-eltérésnél gépi cserét végez és naplóz (DT-F38c (d)).
- **Szellem-szabály** (DT25, DT-F38g): az dönt, kire vonatkozik a szó; az isteni πνεῦμα „Isten Szelleme”, „Szent Szellem”, „a Szellem”, minden más kisbetűs; a kétséges a listára kerül. A G4151 kész (`kezi`), de a rokon szócikkekben a szabály él.
- **Ami R. V. / A. V. után áll, angolul, szó szerint marad** (DT-F38f 5; a prompt Thayer-törzse is így rendelkezik).
- **Forráshiba:** a fordítás hűen viszi, a 13. kapu jelzése a naplóba kerül.
- **Szócikkszintű terminológia-kivétel** csak a felhasználó jóváhagyásával; ha egy kulcsnál 5 fölé nő, környezetfüggő kapu kell (BDB-tanulság), az a #7 előtti javítás.
- **Commit** szócikk-csoportonként (4–9 szócikk, mint az M6-tól), és az adag végén; minden commit után push. A scratchpadben nem maradhat semmi, ami kell.
- **`kezi` és `opus` sorhoz** a menet nem nyúl.
- **Shell:** magyar, görög vagy héber szöveget tartalmazó szkript fájlból fusson.

## 6. Munkaszabályok

1. **Számok** csak a menetben futtatott parancsból vagy a felhasználó leolvasásából; becslés nem kerül mért érték helyére.
2. **Megállás** az M1 két keret-leolvasásánál, a ⛔ M1-nél, és az M0 után csak blokkoló hiánynál. Minden más kérdés a DT-F27b-be gyűlik (D19).
3. **Zárás a `/kovetkezo` szerint:** `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc frissítése.

## 7. Kész, ha

- K1: `naplok/FP3_naplo.md` M0-szakasza a hat ponttal; `naplok/FP3_sorrend.tsv` a teljes, kész sorok nélküli sorrenddel.
- K2: az M1 sorai az `adat/forditasok.tsv`-ben (`allapot=sonnet`, `modell=claude-sonnet-5-5`); a kapusor, az `ellenoriz.py` és a tesztek zöldek.
- K3: `naplok/FP3_arany.md` az 5 szócikkel.
- K4: a két keret-leolvasás és a kivetítés a naplóban.
- K5: a DT-F27b nyitva.
- K6: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | Opus–Gemini összevetés, Max-keret méréssel, 40 szócikkes mintán, vak pontozással és vak olvasással | C út kihagyva; helyi gép |
| v2 | 2026.10.12 | **Csak Sonnet**; a BDB-menet (#38) M0–M1-e a Thayeren: eszközlánc-próba, sorrend, mérő adag, aranyminta, keretmérés. Az `fp3/` kimenet, a prompt v4-kiegészítés, az OpenRouter és a vak összevetés elmarad. | DT121 (felhasználó, 2026.10.12); a v1 szövege a git-történetben |
