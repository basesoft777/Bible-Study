---
feladat: 161
cim: Fordítási lánc a lexikonlapok rövid szótári glosszáihoz (UBS DNTG, UBS DBH, TBESG), a BDB/Thayer API-lánc mintájára
kod: GLOSSZA_LANC
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: megallt
ag: claude/glossza-lanc-1a9f9f
ad: "eszkozok/glossza_api_koteg.py: rögzített prompt (forditas/prompt_glossza_v2.md; v1 + UBS-definíció), mankó, szaraz / prompt / bekuld / begyujt / bevesz / kapuz / javit / rogzit / beir; a #121 lista közös feloldója (TBESG); 21 teszt; a 9 lexikonlap hiányzó UBS- és TBESG-glosszái: 366 sor az adat/forditasok.tsv-ben (Sonnet subagent, 366/366 kapun át); TBESH-ellenőrzés (naplok/F161_GLOSSZA_LANC_naplo.md)"
kovetkezo: "Te: draft PR; a merge a felhasználóé; utána az ANTROP-001 lapja a #608 ágán újragenerálódik (az ANTROP-001 sessionje), a többi hét lap a saját új-cikk sessionjében"
olvas: [F121_GLOSSZA_FORDITAS_BRIEF.md, eszkozok/glossza_lexikon_forditas.py, naplok/F121_GLOSSZA_FORDITAS_manko.tsv, eszkozok/thayer_api_koteg.py, eszkozok/thayer_jelolt/forditas.py, eszkozok/bdb_api_koteg.py, eszkozok/forditas_kapuk.py, eszkozok/olvasoi_kapu.py, eszkozok/emeles.py, forditas/prompt_v5_2.md, adat/terminologia.tsv, adat/tiltott_fordulatok.tsv, adat/forditasok.tsv, adat/SEMA.md]
ir: [F161_GLOSSZA_LANC_BRIEF.md, eszkozok/glossza_api_koteg.py, eszkozok/teszt_glossza_api_koteg.py, forditas/prompt_glossza_v1.md, forditas/prompt_glossza_v2.md, adat/forditasok.tsv, eszkozok/glossza_lexikon_forditas.py, naplok/F161_GLOSSZA_LANC_naplo.md, dontesek/uj/glossza-lanc-1a9f9f.md, nyitott/uj/glossza-lanc-1a9f9f.md]
fugg: []
nem_fugg: [7, 38, 121, 153, 154, 158, 178]
---

# F161_GLOSSZA_LANC_BRIEF.md — fordítási lánc a rövid szótári glosszákhoz

*FELADATOK #161 · Modell: opus · v1 · 2026.11.03*

## 0. Befogadás

A felhasználó jóváhagyása szó szerint (2026-11-03): „de csnáljuk rá láncot manköt mint a bdb nél”. Előzmény: az
ANTROP-001 lapján 54 glossza „(fordításra vár)” (UBS DNTG 30, UBS DBH 3, TBESG 21), és a felhasználó döntése:
„minden forditunk”, „54 db”; a fordítás „ugyanazzal a promptal és szabályokkal mint a batch api-t”. A feladatot az
orkesztrátor adta ki (a felhasználó felhatalmazásával); a merge és a pénzköltés a felhasználóé.

A `nem_fugg` sorai: a #121 eszköze (lista, mankó) a main-en kész, a #161 a #121 lezárására nem vár; a #7/#158 (Thayer), a #38 (BDB) és a #154 eszközei és táblái csak minták vagy olvasott bemenetek;
ez a feladat egyiket sem írja. A #153 a `glossza_lexikon_forditas.py`-t csak olvassa.

## 1. Cél

A BDB és a Thayer fordítása saját API-láncon fut (rögzített prompt, mankó, kapuk, javító kör, beírás); a rövid UBS-
és TBESG-glosszákra ilyen lánc nincs, csak a #121 lista- és rögzítő eszköze. A cél: egy lánc, amely

- a #121 `lista` kimenetéből (a lap által keresett pontos kulcs és forrásszöveg) dolgozik;
- **egyetlen, verziózott prompttal** (`forditas/prompt_glossza_v1.md`) fordít, amely a v5.2 szabályaival összhangban
  van (terminológia, tiltott fordulatok, Károli-alakok, a görög/héber szó és a helyőrzők érintetlenül, az olvasói kapu
  tiltásai), glosszánként rövid, egységes JSON-kimenettel;
- **API-n (Batch) és előfizetői subagenttel is** futtatható, bájtra azonos kéréssel;
- kapuz, legfeljebb egyszer javít, rögzít, és az `adat/forditasok.tsv`-be ír (`allapot` a modell szerint, forrás-hash,
  proveniencia-sor).

## 2. Mit épít

1. **A #121 feloldója (TBESG).** A `lista` eddig csak az UBS-t oldotta fel; a TBESG rövid jelentése `nincs_forras`
   maradt, pedig a 13. szabály feloldója (`tovabbi_forras`) ismeri. Új `forras_szoveg(sor)`: UBS_DBH, UBS_DNTG, minden más
   a `tovabbi_forras`; a `lista` és a lánc ezt hívja. Egy feloldó marad; forrást nem talál ki (ami nem oldható fel,
   `nincs_forras`).
2. **Prompt glossza v1**, egyszer rögzítve; az első próba után nem változik, változás csak új verzióként, naplózva.
3. **Mankó egységenként a kérésben:** a kötelező terminológia (`emeles.kotelezo_alakok`, az 5. kapu illesztése), a
   Strong leggyakoribb Károli-alakjai (#22 párosítás) és az angol elemek elfogadott magyar egyenértékei
   (`egyenertek_tabla`); kontextusként a címszó, a domén és a definíció (és, ha van, a jóváhagyott magyar definíció).
4. **`szaraz`:** az egységek és a kérések hálózat nélkül, kötegelve (azonos Strong egy kérésben, kérésenként legfeljebb
   20 egység), egy repón kívüli munkakönyvtárba (`egysegek.tsv`, `keresek.jsonl`). A `bekuld` a fájlt csak akkor küldi,
   ha az újraépített kéréssel bájtra egyezik; a subagent a `prompt` paranccsal ugyanannak a kérésnek a user-szövegét kapja.
5. **`bekuld` / `allapot` / `begyujt`:** a Thayer-lánc mintájára (`PARDES_API_KEY`, plafon nélkül tilos, futásnapló).
   **`bevesz`:** a subagent válasza, a ténylegesen futott modell nevével.
6. **`kapuz`:** JSON → helyőrző-visszaállítás → javítóréteg (#132 kis/nagybetű-csere) → a meglévő fordítási kapuk
   (`forditas_kapuk.kapuk_futtat`, gátló a `GATOLO` szerint) + a glosszakapuk: elemszám, angol maradék (az olvasói kapu
   szólistája, angol funkciószó, a forrás szava), belső jel (az olvasói kapu `BELSO` mintái), egyenes idézőjel. A
   #121 mankója (szójegyzék, Károli) a kész sorra: a szójegyzéki ütközés jelzés, a beírás csak kézi átnézés után.
7. **`javit`** (legfeljebb egyszer): az eredeti kérés + a korábbi válasz + a kapu hibaüzenete, csak a bukott egységekre.
   **`rogzit`:** az átment egységek sorai a munkakönyvtárba (`rogzitett.tsv`, a `forditasok.tsv` sémája), a kétszer
   bukottak a `bukottak.tsv`-be. **`beir`:** a `forditasok.tsv`-be; `kezi` sor védett, meglévő sor csak `--felulir`-ral,
   a forrás mai hash-e ellenőrizve, a többi sor bájtra változatlan.
8. **Tesztek:** `eszkozok/teszt_glossza_api_koteg.py`.

## 3. Próba és határ

**Hatókör-módosítás (2026-11-03, a felhasználó szavai az orkesztrátoron át, szó szerint):** „ubs re kértem forditást most /
az lánc szerint”, „minden kész lexikoncikk hiányzó UBS-eleme / mind a 7 lexikoncikk” (az orkesztrátor értelmezésében a
`lexikon/` mind a 9 lapja), és a TBESG-ről: „menjen ez is”. A TBESH-et csak ellenőrizni kell (kulcshiba-e), fordítás
nélkül. A fordítás tehát most fut, a lánccal, előfizetői keretből (kérésenként egy `general-purpose` Sonnet subagent, a
kérés szó szerint); a 400 egység fölött előbb a számok mennek az orkesztrátornak. Csak az ISTENTISZT-001 és az ALVIL-001
lapja generálódhat újra ebben a PR-ban, próza-nulla-diffel; a többi lap a saját sessionjében. Az alábbi eredeti
próba-pontokat ez felváltja.


- A `szaraz` az ANTROP-001 54 egységén (a #608 ágának állapotán, repón kívüli munkafában); utána egy kis próba: 5
  glossza `general-purpose` Sonnet subagenttel, a kérés user-szövege szó szerint, majd `kapuz` (és `rogzit` a
  munkakönyvtárba). A `beir` nem fut; az eredmény nem kerül a repóba.
- Az 54 tényleges fordítását az ANTROP-001 sessionje végzi a lánccal, a #608 ágán, e PR merge-e után.
- A `bekuld`/`begyujt` most nem fut (az API-keret üres; a pénzköltés a felhasználóé).
- Ütközés: a `thayer_api_koteg.py`, a `forditas_kapuk.py` (PR #600), a `lexikon_general.py` és az `adat/forditasok.tsv`
  (PR #608) nem változik; a lánc a kapukat módosítás nélkül hívja.

## 4. Eredmény

`naplok/F161_GLOSSZA_LANC_naplo.md`; döntések: `dontesek/uj/glossza-lanc-1a9f9f.md`; nyitott tételek:
`nyitott/uj/glossza-lanc-1a9f9f.md`.
