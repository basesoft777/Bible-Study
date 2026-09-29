# F06_felmeres.md — 0. lépés: felmérés (csak olvas)

*F06_FORRASFELMERES_BRIEF.md v1 · ág: `claude/f06-forrasfelmeres` · 2026.09.29.*
*Számadat csak szkriptkimenetből vagy lekérdezésből; a korábbi jelentésekből átvett állítás „nem újramért” jelöléssel áll.*

## 1. Beolvasott bemenetek

`naplok/FORRAS_jelentes.md`, `NYITOTT_FELADATOK.md` N27–N31, `naplok/FORRAS_FJ1_lxx_jeloltek.tsv`, `konkordancia/Konyv_normalizalo_tabla.tsv`,
továbbá a hivatkozott `naplok/FORRAS_FJ0_hozzaferes.md`, `FORRAS_FJ3_kjv_bsb.md`, `FORRAS_FJ4_nave.md`, `FORRAS_FJ1_mtlxx_macula.md`, `FORRAS_FJ1_macula_illesztes.py`.

## 2. A 87 függő LXX-hely forrása (lekérdezéssel ellenőrizve)

- **Fájl:** `naplok/FORRAS_FJ1_lxx_jeloltek.tsv`; a sor kulcsa a `motivum` + `igehely` oszlop (Károli-számozású igehely), a kereső-oszlopok a `heber_kulcsszo` és a `heber_strong`.
- **Eredet:** a `lexikon/*_TUDOMANYOS.md` 3. szakaszának táblázata, ahol az 5. oszlop `kutatói azonosítás függőben` (a szűrő azonos a `naplok/FORRAS_FJ1_87_jelolt_general.py`-ével).
- **Ellenőrzés:** `python naplok/F06_0_87_ellenorzes.py`, kimenete szó szerint:

```
lexikon-tablasorok (5. oszlop == függőben): 87 ; egyedi (motivum, igehely): 87
munkalap: adatsor=87 ; egyedi (motivum, igehely)=87 ; egyedi igehely=86
munkalap == lexikon-lista (halmazként): True
```

  Tehát valóban **87 sor**, 87 egyedi (motívum, igehely) pár és 86 egyedi igehely (egy igehely két motívumnál szerepel). A két forrás halmazként azonos.
- **Figyelmeztetés a méréshez:** a `grep -c "kutatói azonosítás függőben"` a lexikonfájlokon 95-öt ad; ez nem a 87, mert a szöveg a táblán kívül is előfordul. A helyes szűrő a táblaoszlop (fent).
- A munkalap `heber_strong` oszlopa nem minden sorban kitöltött; ezekben a szkript (`macula.py`) az ékezet nélküli héber szóalakra esik vissza, és az `azonositas` oszlopban jelöli (`strong` / `szoalak`).

## 3. Az OpenRouter-hívó (`eszkozok/fordit.py`) — újrafelhasználás

- `_valodi_http_kuldo(model_id, uzenetek, api_key, extra_parameterek)`: `requests.post` az OpenRouter chat/completions végpontra, `temperature=0`, `usage={'include': True}`, `reasoning={'enabled': False}` (kivéve a `GONDOLKODAS_KOTELEZO_MODELLEK` halmaz), mentsvár-időkorlát 300 mp.
- `_hatarido_vel_hivas`: valódi falióra-határidő (alap 120 mp) daemon szálban; `_http_post_nyers`: visszalépéses újrapróbálás (429/5xx/hálózati hiba), 4xx-nél azonnali `OpenRouterHiba`.
- **Usage-naplózás:** a válasz `usage` mezője (`prompt_tokens`, `completion_tokens`, `cost`); a `Koltsegnaplo` osztály és az `openrouter_hivas` összegzése fordítás-specifikus (fix JSON-séma `fordit_kimenet`), ezért **nem használható változtatás nélkül**.
- **Döntés:** a 4. lépés (`eszkozok/fj2/licenc.py`) **importálja** a `fordit._http_post_nyers`-t és az `OpenRouterHiba`-t (új HTTP-kliens nincs); a saját JSON-sémát, a kapu-logikát és a hívásonkénti költségnaplót maga vezeti. Ha a MiniMax elutasítja a `reasoning: disabled` paramétert (HTTP 400, „reasoning”), a szkript futásidőben felveszi a modellt a `GONDOLKODAS_KOTELEZO_MODELLEK` halmazba; ha a `response_format` a hiba oka, azt nélkülözve újrapróbál. A `fordit.py` nem módosul.

## 4. Forrásjelöltek

| Cél | Jelölt | URL | Megjegyzés (a korábbi FJ-jelentések szerint, **nem újramért**) |
|---|---|---|---|
| Nave (N27) | `basokant/nave` | https://github.com/basokant/nave | az FJ4 „nem létezik” állítását a `git ls-remote` cáfolta (N27); szerkezete ismeretlen |
| Nave | `theonize/bible_database` | https://github.com/theonize/bible_database | `Topics.csv`, `TopicIndex.csv`, `MainIndex.csv`; GPLv3, a Nave-eredet nem nevesített |
| Nave | `elcafe7/lex` | https://github.com/elcafe7/lex | `runtime-data/naves.db` (SQLite); eredet dokumentálatlan |
| KJV/ASV (N29) | studybible.info | https://studybible.info/KJV_Strongs/Genesis%201 , `…/ASV_Strongs/Genesis%201` | a meglévő 1Móz/2Móz/Péld táblák forrása (`konkordancia/README.md`); az FJ3-ban proxy-blokk |
| KJV/ASV | eBible.org | https://ebible.org/Scriptures/ (USFM-zip: `eng-kjv_usfm.zip`, `eng-asv_usfm.zip`, a pontos fájlnevek a mérésben derülnek ki) | az FJ3-ban proxy-blokk; a szkript több névváltozatot próbál |
| KJV/ASV | GitHub-keresés | https://api.github.com/search/repositories (4 lekérdezés) + ismert jelölt `scrollmapper/bible_databases` | az FJ3 mind a `STEPBible-Data`-t (nincs KJV/ASV), mind a `crizin/bible-db`-t (vers-szintű, Strong nélkül) elvetette; a keresés ezeken túlmutat |
| BSB (N30) | `BSB-publishing/bsb-data-output` | https://github.com/BSB-publishing/bsb-data-output | `base/display/<KÖNYV>/<KÖNYV><fej>.json`, CC0 (FJ3); commit az FJ3-ban `e1b254cef86d0e65b1a5d1a94b8b112d0f296a2c` |
| Macula (N31) | `Clear-Bible/macula-hebrew` | https://github.com/Clear-Bible/macula-hebrew | `WLC/lowfat/NN-Könyv-FFF-lowfat.xml`, CC BY 4.0 (FJ1) |

### 4.1 KJV/ASV — GitHub-alternatíva keresése és eredménye

A brief kéri, hogy a felmérés rögzítse, mit találtam GitHubon. **A GitHub-keresést a 0. lépésben nem futtattam le** (a hálózati lekérdezés ebben a sessionben nem volt elérhető; N29 szerint a cloud proxy korábban is blokkolt), ezért a keresés a 3. lépés része (`kjv_asv.py`: 4 lekérdezés, találatonként licenc/méret/frissítés, a legjobb jelöltek klónozása és Strong-címke-minta keresése a KJV/ASV nevű fájlokban). Amit a felmérésben ismert: a `STEPBible-Data` és a `crizin/bible-db` kizárva (FJ3), a `scrollmapper/bible_databases` nem vizsgált. A keresés eredménye a `naplok/F06_kjv_asv.tsv`-ben lesz.

### 4.2 Két kockázat, amit a felmérés talált

1. **Az FJ1 Macula-fájlmintája valószínűleg elveszítette az 1Sám–2Krón fájlokat.** Az `FORRAS_FJ1_macula_illesztes.py` és az `…_87_jelolt_general.py` fájlnév-mintája `^\d+-([A-Za-z]+)-(\d+)-lowfat\.xml$`, ami **számjegyre kezdődő könyvkódot** (`1Sam`, `2Kron` típusú fájlkód) nem illeszt. Ez lehet az N31 „hiányzó” könyveinek oka (nem letöltési hiba). Ez **hipotézis**: a `macula.py` a fájlnév `NN-` előtagját (kanonikus sorszám) használja kulcsnak, és `repo_fajl_osszesen` oszlopban a teljes repó fájlleltárát is méri, ezért a 3. lépés eldönti.
2. **Számozás:** a 87 hely igehelyei Károli-számozásúak, a Macula héber (BHS). A `macula.py` számozás-átalakítás nélkül keres; a nem talált verset `NINCS_VERS`-ként jelöli, és a jelentésben külön kezelendő (N28 szerint a Károli-kulcs a KK-menet témája).

## 5. Elkészült szkriptek (1. lépés) és ellenőrzésük

`eszkozok/fj2/`: `kozos.py`, `nave.py`, `kjv_asv.py`, `bsb.py`, `macula.py`, `licenc.py`, `futtat.py`, `onteszt.py`. Workflow: `.github/workflows/f06_forrasfelmeres.yml`.

- `python eszkozok/fj2/futtat.py --szaraz --lepes meres` és `--lepes licenc`: a szerkezet rendben (letöltés és API-hívás nélkül).
- `python eszkozok/fj2/onteszt.py`: a licencbeli idézetkapu, a BSB-elemzés, a Macula-feldolgozás (szintetikus adaton, a szám nem kerül a jelentésbe) és a BSB-futás logikája `onteszt: rendben`.
- Mérést **nem** futtattam (a brief 2. lépése előtt tilos).
- **Kapu a szkriptben:** `futtat.py` (nem `--szaraz` módban) nem indul, ha nincs `eszkozok/fj2/kuszob.txt` és a jelen fájlban `## ⛔ Válasz` szakasz.
- **Trigger:** a workflow-fájl a válasz előtt szándékosan csak az `eszkozok/fj2/futtatas.txt`-re indul (a fájl a válaszig nem létezik), így a push nem indít mérést. A válasz után egy külön commit (F06.2) bővíti az útvonalakat (`eszkozok/fj2/**`, workflow-fájl, `futtatas.txt`), és létrehozza a `kuszob.txt`-t és a `futtatas.txt`-t.

## 6. ⛔ Előfeltételek a felhasználótól (a brief 2. lépése)

**Állapot: a válasz még nincs meg; mérés nem indult.**

1. **BSB-küszöb (N30).** Javaslat, a mérés előtt rögzítendő:
   - *egyezés definíciója:* a vers TAHOT Strong-halmaza **része** a BSB Strong-halmazának, a 9000-es (és afeletti) STEPBible-prefixkódok nélkül;
   - *küszöb:* **95%**;
   - *nevező (kiegészítés a briefhez):* a TAHOT-tal rendelkező versek; a TAHOT-ból hiányzó versek (az N-lista szerint legalább 1Móz 32) külön listára kerülnek, nem számítanak eltérésnek. A jelentés mindkét arányt közli (TAHOT-lefedett és összes vers), de az elfogadás a rögzített nevezőn dől el.
   - A küszöböt a mérés előtt rögzítjük, utána nem módosítjuk.
2. **Secret:** az `OPENROUTER_API_KEY` repo-secret (Settings → Secrets and variables → Actions) beállítva-e.

A válasz rögzítése ebben a fájlban, a `## ⛔ Válasz` szakaszban történik.
